from core import *
import numpy as np
import cv2
import pygame
from random import randint
from time import time, sleep
from danmaku import *

def display_game(map):
    def get_blank_img():
        return np.zeros((480, 400, 3), np.uint8)
    img = get_blank_img()
    img.fill(255)
    for enemy in map.enemy_list:
        cv2.rectangle(img, (np.int16(enemy.x - enemy.w / 2), np.int16(enemy.y - enemy.h / 2)), (np.int16(enemy.x + enemy.w / 2), np.int16(enemy.y + enemy.h / 2)), (0, 0, 255), 1)
    for bullet in map.bullet_list:
        cv2.rectangle(img, (np.int16(bullet.x - bullet.w / 2), np.int16(bullet.y - bullet.h / 2)), (np.int16(bullet.x + bullet.w / 2), np.int16(bullet.y + bullet.h / 2)), (0, 0, 255), 1)
    cv2.rectangle(img, (np.int16(map.player.x - map.player.w / 2), np.int16(map.player.y - map.player.h / 2)), (np.int16(map.player.x + map.player.w / 2), np.int16(map.player.y + map.player.h / 2)), (255, 0, 0), 1)
    cv2.imshow('game', img)
    cv2.waitKey(1)
    

def get_random_bullet():
    return obj_bullet(randint(0, 600), randint(0, 440), 5, 5, randint(-25, 25), randint(-25, 25), randint(-5, 5), randint(-5, 5))

class game_with_display(game):
    def __init__(self, player):
        super().__init__(player)
        pygame.init()
        screen = pygame.display.set_mode((int(self.map_size[0] / 2), int(self.map_size[1] / 2)))
        pygame.display.set_caption("Control")

    def get_blank_img(self):
        return np.full((self.map_size[1], self.map_size[0], 3), 255, dtype = np.uint8)
    
    def display(self):
        img = self.get_blank_img()
        map = self.get_map()
        for enemy in map.enemy_list:
            cv2.rectangle(img, (np.int16(enemy.x - enemy.w / 2), np.int16(enemy.y - enemy.h / 2)), (np.int16(enemy.x + enemy.w / 2), np.int16(enemy.y + enemy.h / 2)), (0, 0, 255), 2)
        for bullet in map.bullet_list:
            cv2.rectangle(img, (np.int16(bullet.x - bullet.w / 2), np.int16(bullet.y - bullet.h / 2)), (np.int16(bullet.x + bullet.w / 2), np.int16(bullet.y + bullet.h / 2)), (0, 0, 255), 2)
        cv2.rectangle(img, (np.int16(map.player.x - map.player.w / 2), np.int16(map.player.y - map.player.h / 2)), (np.int16(map.player.x + map.player.w / 2), np.int16(map.player.y + map.player.h / 2)), (255, 0, 0), 2)
        cv2.imshow('game', img)
        cv2.waitKey(1)
    
    
    def play(self, FPS = 60):
        keys = []
        while True:
            st = time()
            event = pygame.event.get()
            for e in event:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        keys.append('left')
                    elif e.key == pygame.K_RIGHT:
                        keys.append('right')
                    elif e.key == pygame.K_UP:
                        keys.append('down')
                    elif e.key == pygame.K_DOWN:
                        keys.append('up')
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_LEFT:
                        keys.remove('left')
                    elif e.key == pygame.K_RIGHT:
                        keys.remove('right')
                    elif e.key == pygame.K_UP:
                        keys.remove('down')
                    elif e.key == pygame.K_DOWN:
                        keys.remove('up')
            op = 0
            if 'left' in keys:
                if 'up' in keys:
                    op = 2
                elif 'down' in keys:
                    op = 8
                else:
                    op = 1
            elif 'right' in keys:
                if 'up' in keys:
                    op = 4
                elif 'down' in keys:
                    op = 6
                else:
                    op = 5
            elif 'up' in keys:
                op = 3
            elif 'down' in keys:
                op = 7
            if 'left' in keys and 'right' in keys:
                op = 0
                if 'up' in keys:
                    op = 3
                elif 'down' in keys:
                    op = 7
            if 'up' in keys and 'down' in keys:
                op = 0
                if 'left' in keys:
                    op = 1
                elif 'right' in keys:
                    op = 5

            for i in range(randint(0, 3)):
                self.insert_bullet(get_random_bullet())
            super().update(op)
            self.display()
            ed = time()
            if ed - st < 1 / FPS:
                sleep(max(1 / FPS - ed + st - 0.0002, 0))
            ed2 = time()
            print('FPS: {}'.format(1 / (ed2 - st)))