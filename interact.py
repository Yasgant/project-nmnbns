import _getdata as getdata
import tensorflow as tf
import numpy as np
from time import time, sleep
from collections import deque
import ctypes
import win32api
import win32con


stack_size = 4
state_size = (101, 121, stack_size)
FPS = 6

model = tf.keras.models.load_model('./data/model')

stacked_imgs = deque([np.zeros(state_size[:2]) for i in range(stack_size)], maxlen = stack_size)
def stack_img(stacked_imgs, img, fir = False):
    stacked_imgs.append(img)
    if fir:
        for i in range(3):
            stacked_imgs.append(img)
    stacked_img = np.stack(stacked_imgs, axis = 2)
    return stacked_img, stacked_imgs

if not getdata.init():
    raise Exception('Cannot connect to game')
MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA

def press_key(x):
    if x == 'l':
        win32api.keybd_event(0x25, MapVirtualKey(0x25, 0), 0, 0)
    elif x == 'r':
        win32api.keybd_event(0x27, MapVirtualKey(0x27, 0), 0, 0)
    elif x == 'u':
        win32api.keybd_event(0x26, MapVirtualKey(0x26, 0), 0, 0)
    elif x == 'd':
        win32api.keybd_event(0x28, MapVirtualKey(0x28, 0), 0, 0)

def release_key(x):
    if x == 'l':
        win32api.keybd_event(0x25, MapVirtualKey(0x25, 0), win32con.KEYEVENTF_KEYUP, 0)
    elif x == 'r':
        win32api.keybd_event(0x27, MapVirtualKey(0x27, 0), win32con.KEYEVENTF_KEYUP, 0)
    elif x == 'u':
        win32api.keybd_event(0x26, MapVirtualKey(0x26, 0), win32con.KEYEVENTF_KEYUP, 0)
    elif x == 'd':
        win32api.keybd_event(0x28, MapVirtualKey(0x28, 0), win32con.KEYEVENTF_KEYUP, 0)

now = set()
def press(new):
    global now
    for i in new:
        if i not in now:
            press_key(i)
    for i in now:
        if i not in new:
            release_key(i)
    now = new

def take_action(action):
    if action == 0:
        press(set())
    elif action == 1:
        press(set(['l']))
    elif action == 2:
        press(set(['l', 'd']))
    elif action == 3:
        press(set(['d']))
    elif action == 4:
        press(set(['d', 'r']))
    elif action == 5:
        press(set(['r']))
    elif action == 6:
        press(set(['r', 'u']))
    elif action == 7:
        press(set(['u']))
    elif action == 8:
        press(set(['u', 'l']))

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

img = stack_img(stacked_imgs, get_img(), True)
sleep(2)
standard_time = 1/FPS
while True:
    stt = time()
    img, stacked_imgs = stack_img(stacked_imgs, get_img())
    action = np.argmax(model.predict(np.array([img]))[0])
    take_action(action)
    edt = time()
    print('Processing time: {} * {}'.format((edt - stt) / standard_time, standard_time))
    sleep(max(0, standard_time - (edt - stt)))
