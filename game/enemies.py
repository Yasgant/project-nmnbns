from core import *
from danmaku import *

class AimmingEnemy(Enemy):
    def __init__(self, x, y, w = 5, h = 5, vx = 0, vy = 0, shoot_time = 20, alive_time = 5 * 60):
        super().__init__(x, y, w, h, vx, vy)
        self.alive_time = alive_time
        self.shoot_time = shoot_time

    def get_arc(self, player):
        x = self.x - player.x
        y = self.y - player.y
        return np.arctan2(y, x) - np.pi
    
    def shoot(self, player, v = 2):
        arc = self.get_arc(player)
        return [obj_bullet(self.x, self.y, 4, 4, v * np.cos(arc), v * np.sin(arc), 0, 0)]
    
    def update(self, player):
        super().update()
        self.alive_time -= 1
        if self.alive_time <= 0:
            self.alive_time = 0
        if self.alive_time % self.shoot_time == 0:
            return self.shoot(player)

class AimmingEnemy3(Enemy):
    def __init__(self, x, y, w = 5, h = 5, vx = 0, vy = 0, shoot_time = 20, alive_time = 5 * 60):
        super().__init__(x, y, w, h, vx, vy)
        self.alive_time = alive_time
        self.shoot_time = shoot_time

    def get_arc(self, player):
        x = self.x - player.x
        y = self.y - player.y
        return np.arctan2(y, x) - np.pi
    
    def shoot(self, player, v = 2):
        arc = self.get_arc(player)
        bullets = []
        bullets.append(obj_bullet(self.x, self.y, 4, 4, v * np.cos(arc), v * np.sin(arc), 0, 0))
        bullets.append(obj_bullet(self.x, self.y, 4, 4, v * np.cos(arc + np.pi / 12), v * np.sin(arc + np.pi / 12), 0, 0))
        bullets.append(obj_bullet(self.x, self.y, 4, 4, v * np.cos(arc - np.pi / 12), v * np.sin(arc - np.pi / 12), 0, 0))
        return bullets
    
    def update(self, player):
        super().update()
        self.alive_time -= 1
        if self.alive_time <= 0:
            self.alive_time = 0
        if self.alive_time % self.shoot_time == 0:
            return self.shoot(player)

class AimmingEnemy14(Enemy):
    def __init__(self, x, y, w = 5, h = 5, vx = 0, vy = 0, shoot_time = 20, alive_time = 5 * 60):
        super().__init__(x, y, w, h, vx, vy)
        self.alive_time = alive_time
        self.shoot_time = shoot_time

    def get_arc(self, player):
        x = self.x - player.x
        y = self.y - player.y
        return np.arctan2(y, x) - np.pi
    
    def shoot(self, player, v = 2):
        arc = self.get_arc(player)
        bullets = []
        arc -= np.pi * 7 / 18
        for i in range(14):
            bullets.append(obj_bullet(self.x, self.y, 6, 6, v * np.cos(arc), v * np.sin(arc), 0, 0))
            arc += np.pi / 18
        return bullets
    
    def update(self, player):
        super().update()
        self.alive_time -= 1
        if self.alive_time <= 0:
            self.alive_time = 0
        if self.alive_time % self.shoot_time == 0:
            return self.shoot(player)