from core import *
from display import *
import numpy as np
from danmaku import *
from enemies import *


data = StageData.empty('Stage1',1000)
data.insert(0, AimmingEnemy(100, 100, shoot_time = 2))
data.insert(10, AimmingEnemy3(120, 100, shoot_time = 2))
data.insert(20, AimmingEnemy(140, 100, shoot_time = 2))
data.insert(30, AimmingEnemy3(160, 100, shoot_time = 2))
data.insert(40, AimmingEnemy(180, 100, shoot_time = 2))
data.insert(50, AimmingEnemy3(200, 100, shoot_time = 2))
data.insert(60, AimmingEnemy3(220, 100, shoot_time = 2))
data.insert(70, AimmingEnemy3(240, 100, shoot_time = 2))
data.insert(80, AimmingEnemy3(260, 100, shoot_time = 2))
data.insert(90, AimmingEnemy14(320, 100, shoot_time = 5))
rep = OpReplay.read_from_file('./data/re1.txt')
G = Replay(Player(320, 400), data, rep)
print(G.play_video())
