from core import *
from time import time, sleep
import display
from enemies import *

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
    
    def write_to_file(self, file_name = None):
        if file_name is None:
            file_name = './data/' + self.stage_name + '.txt'
        with open(file_name, 'w+') as f:
            f.write('StageName: ' + self.stage_name + '\n' + 'Total frames: ' + str(len(self.enemies_data)) + '\n')
            for frame, enemies in enumerate(self.enemies_data):
                for enemy in enemies:
                    f.write(str(frame) + ' ' + enemy.__class__.__name__ + ' ' + str(enemy.__dict__) + '\n')
    
    @classmethod
    def read_from_file(cls, file_name):
        with open(file_name, 'r') as f:
            data = f.readlines()
            stage_name = data[0].split()[1]
            total_frames = int(data[1].split()[2])
            enemies_data = [[] for i in range(total_frames)]
            data = data[2:]
            for line in data:
                frame = int(line.split(' ', 2)[0])
                enemy_name = line.split(' ', 3)[1]
                line = line[line.index('{') + 1: line.index('}')].split(',')
                enemy_dict = eval('{' + ','.join(line) + '}')
                print(enemy_name + '(' + str(enemy_dict) + ')')
                enemies_data[frame].append(eval(enemy_name + '(**' + str(enemy_dict) + ')'))
        return cls(stage_name, enemies_data)



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

class game_with_op(game):
    def __init__(self, player, stage_data):
        super().__init__(player)
        self.stage_data = stage_data
        self.enemies_gen = self.stage_data.get_enemies()
        self.frame = 0

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
        
    def op(self, op):
        try:
            enemies = next(self.enemies_gen)
        except StopIteration:
            return 0, True
        self.frame += 1
        for enemy in enemies:
            self.insert_enemy(enemy)
        if not self.update(op):
            return -100000, True
        return self.evaluate(), False

class OpReplay:
    def __init__(self, op_list, name):
        self.op_list = op_list
        self.name = name
    
    @classmethod
    def read_from_file(cls, file_name):
        with open(file_name, 'r') as f:
            data = f.readlines()
            op_list = []
            for line in data:
                op_list.append(int(line))
        return cls(op_list, file_name[:-4])
    
    def write_to_file(self, file_name):
        with open(file_name, 'w') as f:
            for op in self.op_list:
                f.write(str(op) + '\n')

class Replay(game_with_op):
    def __init__(self, player, stage_data, op_list):
        super().__init__(player, stage_data)
        self.stage_data = stage_data
        self.op_list = op_list

    
    def play_video(self, FPS = 60):
        enemies_gen = self.stage_data.get_enemies()
        ct = -1
        while True:
            ct += 1
            stt = time()
            try:
                enemies = next(enemies_gen)
            except StopIteration:
                return False
            for enemy in enemies:
                self.insert_enemy(enemy)
            op = self.op_list.op_list[ct]
            if not self.update(op):
                return True
            display.display_game(self)
            edt = time()
            if edt - stt < 1 / FPS:
                sleep(max(1 / FPS - edt + stt - 0.0003, 0))
            edt2 = time()
            print('Frame: {}'.format(ct))