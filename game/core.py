import numpy as np
from time import time
import matplotlib.pyplot as plt

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
    def __init__(self, player, enemy_list = [], bullet_list = [], map_size = (640, 480)):
        self.player = player.intlize()
        self.enemy_list = [ey.get_enemy() for ey in enemy_list]
        self.bullet_list = [bt.get_bullet() for bt in bullet_list]
        self.map_size = map_size
    
    def evaluate(self, player):
        ans = 0
        for bullet in self.bullet_list:
            if abs(bullet.x - player.x) < 10 * player.w and bullet.y - bullet.h < player.y + player.h + 5 and player.y - bullet.y < 10 * player.h:
                ans -= 10 * player.w - abs(bullet.x - player.x) + 10 * player.h + bullet.y - player.y
        for enemy in self.enemy_list:
            if abs(enemy.x - player.x) < 10 * player.w and enemy.y - enemy.h < player.y + player.h + 5 and player.y - enemy.y < 10 * player.h:
                ans -= 10 * player.w - abs(enemy.x - player.x) + 10 * player.h + enemy.y - player.y
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
            return 0 <= obj.x <= self.map_size[0] and 0 <= obj.y <= self.map_size[1]

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

            