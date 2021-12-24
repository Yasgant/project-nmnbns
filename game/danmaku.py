from core import *
from time import time, sleep
import display

class EnemiesData:
    def __init__(self, enemies_data):
        self.enemies_data = enemies_data
    
    @classmethod
    def empty(cls, length):
        return cls([[] for i in range(length)])
    
    def insert(self, index, enemy):
        self.enemies_data[index].append(enemy)
    

class StageData(EnemiesData):
    def __init__(self, stage_name, enemies_data):
        super().__init__(enemies_data)
        self.stage_name = stage_name
    
    @classmethod
    def empty(cls, name, length):
        return cls(name, [[] for i in range(length)])
    
    def get_enemies(self):
        for enemies in self.enemies_data:
            yield enemies



class game_with_play(game):
    def __init__(self, player, stage_data):
        super().__init__(player)
        self.stage_data = stage_data

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
            return 0 <= obj.x < self.map_size[0] and 0 <= obj.y < self.map_size[1]

        for enemy in self.enemy_list:
            bullets = enemy.update(self.player)
            if bullets:
                self.bullet_list.extend(bullets)
        
        for bullet in self.bullet_list:
            bullet.update()
        
        self.bullet_list = [bt for bt in self.bullet_list if in_map(bt)]
        self.enemy_list = [ey for ey in self.enemy_list if in_map(ey) and ey.alive_time > 0]

        self.player.operate(op)
        force_in_map(self.player)
        return not (any(enemy.touch(self.player.x, self.player.y) for enemy in self.enemy_list) or any(bullet.touch(self.player.x, self.player.y) for bullet in self.bullet_list))
        
    def play(self, FPS = 60):
        enemies_gen = self.stage_data.get_enemies()
        ct = 0
        while True:
            ct += 1
            stt = time()
            try:
                enemies = next(enemies_gen)
            except StopIteration:
                break
            for enemy in enemies:
                self.insert_enemy(enemy)
            op = 1 if ct % 40 < 20 else 5
            if not self.update(op):
                #break
                pass
            display.display_game(self)
            edt = time()
            if edt - stt < 1 / FPS:
                sleep(max(1 / FPS - edt + stt - 0.0003, 0))
            edt2 = time()
            print('FPS: {}'.format(1 / (edt2 - stt)))