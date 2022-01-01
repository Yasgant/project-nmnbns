import cv2
import numpy as np
from time import time, sleep
import _getdata as getdata

FPS = 60
standard_time = 1 / FPS
state_size = (101, 121, 4)

def show_img(img):
    colored_img = np.full((img.shape[1], img.shape[0], 3), 255, dtype=np.uint8)
    for j in range(len(img)):
        for i in range(len(img[0])):
            if img[j][i]:
                colored_img[i][j] = (0, 0, 255) if img[j][i] == 0.7 else (255, 0, 0)
    cv2.imshow('img', colored_img)
    cv2.waitKey(1)

def get_img():
    img = np.zeros(state_size[:2])
    enemies = getdata.GetEnemies()
    for i in range(0, len(enemies), 2):
        img[round(enemies[i] / 4), round(enemies[i+1] / 4)] = 0.7
    bullets = getdata.GetBullets()
    for i in range(0, len(bullets), 2):
        img[round(bullets[i] / 4), round(bullets[i+1] / 4)] = 0.7
    player = getdata.GetPlayer()
    img[round(player[0] / 4), round(player[1] / 4)] = 0.3
    return img

if not getdata.init():
    raise Exception('Cannot connect to game')

while True:
    sdt = time()
    show_img(get_img())
    edt = time()
    if edt - sdt < standard_time:
        sleep(standard_time - (edt - sdt))