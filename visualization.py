import cv2
import numpy as np
import time
import getdata

FPS = 60
standard_time = 1 / FPS
state_size = (101, 121, 4)

def show_img(img):
    colored_img = np.zeros((*img.shape, 3), np.uint8)
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j]:
                colored_img[i][j] = (255, 0, 0) if img[i][j] == 0.7 else (0, 0, 255)
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
    st = time()
    show_img(get_img())
    edt = time()
    if edt - st < standard_time:
        time.sleep(standard_time - (edt - st))