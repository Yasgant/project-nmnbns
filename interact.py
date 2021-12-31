import getdata
import tensorflow as tf
import numpy as np
from time import time, sleep
from collections import deque
import pykeyboard


stack_size = 4
state_size = (101, 121, stack_size)
FPS = 60

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
kb = pykeyboard.PyKeyboard()

now = set()
def press(new):
    global now
    for i in new:
        if i not in now:
            kb.press_key(i)
    for i in now:
        if i not in new:
            kb.release_key(i)
    now = new

def take_action(action):
    if action == 0:
        press(set())
    elif action == 1:
        press(set([kb.left_key]))
    elif action == 2:
        press(set([kb.left_key, kb.down_key]))
    elif action == 3:
        press(set([kb.down_key]))
    elif action == 4:
        press(set([kb.down_key, kb.right_key]))
    elif action == 5:
        press(set([kb.right_key]))
    elif action == 6:
        press(set([kb.right_key, kb.up_key]))
    elif action == 7:
        press(set([kb.up_key]))
    elif action == 8:
        press(set([kb.up_key, kb.left_key]))

def get_img():
    img = np.zeros(state_size)
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
    img = stack_img(stacked_imgs, get_img())
    action = np.argmax(model.predict(np.array([img]))[0])
    take_action(action)
    edt = time()
    print('Processing time: {} * {}'.format((edt - stt) / standard_time, standard_time))
    sleep(max(0, standard_time - (edt - stt)))
