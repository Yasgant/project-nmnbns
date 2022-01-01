import numpy as np
from time import time

class obj:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def touch(self, x, y):
        return self.x - 0.5 * self.w <= x <= self.x + 0.5 * self.w and self.y - 0.5 * self.h <= y <= self.y + 0.5 * self.h

class Bullet(obj):
    pass

class obj_bullet(Bullet):
    def __init__(self, x, y, w, h, vx, vy, ax, ay):
        super().__init__(x, y, w, h)
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay

    def get_bullet(self):
        return Bullet(np.int16(self.x), np.int16(self.y), self.w, self.h)

class Enemy(obj):
    def __init__(self, x, y, w, h, vx, vy):
        super().__init__(x, y, w, h)
        self.vx = vx
        self.vy = vy
    
    def update(self):
        self.x += self.vx
        self.y += self.vy

class obj_enemy(Enemy):
    def __init__(self, x, y, w, h, vx, vy, ax, ay):
        super().__init__(x, y, w, h)
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay

    def get_enemy(self):
        return Enemy(np.int16(self.x), np.int16(self.y), self.w, self.h)

class Player(obj):
    opt = [(0, 0), (-2, 0), (-1.4, 1.4), (0, 2), (1.4, 1.4), (2, 0), (1.4, -1.4), (0, -2), (-1.4, -1.4)]
    def __init__(self, x, y, w = 2, h = 2):
        super().__init__(x, y, w, h)

    def operate(self, op = 0):
        self.x += self.opt[op][0]
        self.y += self.opt[op][1]
    
    def intlize(self):
        return Player(np.int16(self.x), np.int16(self.y), self.w, self.h)



class Map:
    def __init__(self, player, enemy_list = [], bullet_list = [], map_size = (400, 480)):
        self.player = player.intlize()
        self.enemy_list = [ey.get_enemy() for ey in enemy_list]
        self.bullet_list = [bt.get_bullet() for bt in bullet_list]
        self.map_size = map_size
    
    def evaluate(self):
        ans = 200
        for bullet in self.bullet_list:
            if abs(bullet.x - self.player.x) < 20 * self.player.w and bullet.y - bullet.h < self.player.y + self.player.h + 5 and self.player.y - bullet.y < 20 * self.player.h:
                ans -= (20 * self.player.w - abs(bullet.x - self.player.x) + 20 * self.player.h + bullet.y - self.player.y) * 0.1
        for enemy in self.enemy_list:
            if abs(enemy.x - self.player.x) < 20 * self.player.w and enemy.y - enemy.h < self.player.y + self.player.h + 5 and self.player.y - enemy.y < 20 * self.player.h:
                ans -= (20 * self.player.w - abs(enemy.x - self.player.x) + 20 * self.player.h + enemy.y - self.player.y) * 0.1
        if self.player.y < self.map_size[1] / 2:
            ans -= 100
        if min(self.map_size[0] - self.player.x, self.player.x) < 10:
            ans -= 30 - 3 * min(self.map_size[0] - self.player.x, self.player.x)
        if min(self.map_size[1] - self.player.y, self.player.y) < 10:
            ans -= 30 - 3 * min(self.map_size[1] - self.player.y, self.player.y)
        return ans
    
    def fill(self):
        ans = np.zeros(self.map_size)
        ans[np.int16(self.player.x - self.player.w * 0.5):np.int16(self.player.x + self.player.w * 0.5), np.int16(self.player.y - self.player.h * 0.5):np.int16(self.player.y + self.player.h * 0.5)] = 0.3
        for enemy in self.enemy_list:
            ans[np.int16(enemy.x - enemy.w * 0.5):np.int16(enemy.x + enemy.w * 0.5), np.int16(enemy.y - enemy.h * 0.5):np.int16(enemy.y + enemy.h * 0.5)] = 0.7
        for bullet in self.bullet_list:
            ans[np.int16(bullet.x - bullet.w * 0.5):np.int16(bullet.x + bullet.w * 0.5), np.int16(bullet.y - bullet.h * 0.5):np.int16(bullet.y + bullet.h * 0.5)] = 0.7
        return ans
    
    def centered_fill(self):
        ans = np.zeros(self.map_size)
        for enemy in self.enemy_list:
            if -self.map_size[0] / 2 <= enemy.x - self.player.x <= self.map_size[0] / 2 and -self.map_size[1] / 2 <= enemy.y - self.player.y <= self.map_size[1] / 2:
                ans[np.int16(enemy.x - self.player.x + self.map_size[0] / 2), np.int16(enemy.y - self.player.y + self.map_size[1] / 2)] = 1
        for bullet in self.bullet_list:
            if -self.map_size[0] / 2 <= bullet.x - self.player.x <= self.map_size[0] / 2 and -self.map_size[1] / 2 <= bullet.y - self.player.y <= self.map_size[1] / 2:
                ans[np.int16(bullet.x - self.player.x + self.map_size[0] / 2), np.int16(bullet.y - self.player.y + self.map_size[1] / 2)] = 1
        return ans

class game(Map):
    def update(self, op = 0):
        def force_in_map(player):
            if player.x < 0:
                player.x = 0
            elif player.x > self.map_size[0]:
                player.x = self.map_size[0]
            if player.y < 0:
                player.y = 0
            elif player.y > self.map_size[1]:
                player.y = self.map_size[1]
        
        def in_map(obj):
            return -10 <= obj.x <= self.map_size[0]+10 and -10 <= obj.y <= self.map_size[1]+10

        for enemy in self.enemy_list:
            enemy.update()
        for bullet in self.bullet_list:
            bullet.update()
        
        self.bullet_list = [bt for bt in self.bullet_list if in_map(bt)]
        self.enemy_list = [ey for ey in self.enemy_list if in_map(ey)]
        
        self.player.operate(op)
        force_in_map(self.player)
        return not (any(enemy.touch(self.player.x, self.player.y) for enemy in self.enemy_list) or any(bullet.touch(self.player.x, self.player.y) for bullet in self.bullet_list))
    
    def insert_enemy(self, enemy):
        self.enemy_list.append(enemy)
    
    def insert_bullet(self, bullet):
        self.bullet_list.append(bullet)
    
    def get_map(self):
        return Map(self.player, self.enemy_list, self.bullet_list, self.map_size)
    
    def get_img(self):
        def in_map(obj):
            return 0 <= obj.x <= self.map_size[0] and 0 <= obj.y <= self.map_size[1]
        ans = np.zeros((round(self.map_size[0] / 4) + 1, round(self.map_size[1] / 4) + 1))
        for enemy in self.enemy_list:
            if in_map(enemy):
                ans[round(enemy.x / 4), round(enemy.y / 4)] = 0.7
        for bullet in self.bullet_list:
            if in_map(bullet):
                ans[round(bullet.x / 4), round(bullet.y / 4)] = 0.7
        ans[round(self.player.x / 4), round(self.player.y / 4)] = 0.3
        return ans
    
    def get_enemies(self):
        ans = [0 for i in range(2000)]
        eys = []
        if self.player.x > self.map_size[0] / 2:
            ans[0] = 0.501 + (self.map_size[0] - self.player.x) / self.map_size[0]
        else:
            ans[0] = 0.499 - (self.player.x) / self.map_size[0]
        if self.player.y > self.map_size[1] / 2:
            ans[1000] = 0.501 + (self.map_size[1] - self.player.y) / self.map_size[1]
        else:
            ans[1000] = 0.499 - (self.player.y) / self.map_size[1]
        cnt = 1
        for enemy in self.enemy_list:
            eys.append(((1.0*enemy.x - self.player.x + self.map_size[0] ) / (2*self.map_size[0]), (1.0*enemy.y - self.player.y + self.map_size[1] ) / (2*self.map_size[1])))
        for bullet in self.bullet_list:
            eys.append(((1.0*bullet.x - self.player.x + self.map_size[0] ) / (2*self.map_size[0]), (1.0*bullet.y - self.player.y + self.map_size[1] ) / (2*self.map_size[1])))
        eys.sort(key = lambda x: min(abs(x[0] - 0.5), abs(x[1] - 0.5)))
        for ey in eys:
            ans[cnt] = ey[0]
            ans[cnt + 1000] = ey[1]
            if np.random.random() > min(abs(ey[0] - 0.5), abs(ey[1] - 0.5)) * 0.5 - 0.125:
                cnt += 1
            if cnt == 1000:
                return ans
        return ans
    
    def play(self, func, FPS = 60):
        score = 0
        while True:
            start = time()
            op = func(self.get_map())
            if not self.update(op):
                return score
            end = time()
            score += 200 + self.evaluate()
            print("score: {}\n FPS: {}".format(score, 1 / (end - start)))
        raise Exception("Game Over")

            