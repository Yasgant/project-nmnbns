from core import *
from display import *
import numpy as np
from danmaku import *
from enemies import *


data = StageData.empty('Stage1',1200)
data.insert(0, AimmingEnemy(100, 100))
data.insert(60, AimmingEnemy3(120, 100))
data.insert(120, AimmingEnemy(140, 100))
data.insert(180, AimmingEnemy3(160, 100))
data.insert(240, AimmingEnemy(180, 100))
data.insert(300, AimmingEnemy3(200, 100, shoot_time = 5))
data.insert(360, AimmingEnemy3(220, 100, shoot_time = 5))
data.insert(420, AimmingEnemy3(240, 100, shoot_time = 5))
data.insert(480, AimmingEnemy3(260, 100, shoot_time = 5))
data.insert(540, AimmingEnemy14(320, 100, shoot_time = 20))
data.write_to_file()
Sdata = StageData.read_from_file('./data/Stage1.txt')
G = game_with_play(Player(320, 400), Sdata)
G.play()
