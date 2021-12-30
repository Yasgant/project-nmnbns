from core import *
from display import *
import numpy as np
from danmaku import *
from enemies import *


data = StageData.empty('S1',10*60*60)
# 0 ~ 1000
data.insert(0, AimmingEnemy3(100, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))
data.insert(9, AimmingEnemy3(110, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))
data.insert(18, AimmingEnemy3(120, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))
data.insert(27, AimmingEnemy3(130, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))
data.insert(36, AimmingEnemy3(140, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))
data.insert(45, AimmingEnemy3(150, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))
data.insert(54, AimmingEnemy3(160, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))
data.insert(63, AimmingEnemy3(170, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))
data.insert(72, AimmingEnemy3(180, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))
data.insert(81, AimmingEnemy3(190, 100, shoot_time = 10, bullet_speed=10, arc = np.pi / 24, alive_time=10*60))

# 1000 ~ 1500
data.insert(1000, AimmingEnemy(100, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1020, AimmingEnemy(100, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1040, AimmingEnemy(100, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1060, AimmingEnemy(100, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1080, AimmingEnemy(100, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1100, AimmingEnemy(100, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1000, AimmingEnemy(540, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1020, AimmingEnemy(540, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1040, AimmingEnemy(540, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1060, AimmingEnemy(540, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1080, AimmingEnemy(540, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))
data.insert(1100, AimmingEnemy(540, 10, shoot_time = 2, bullet_speed=10, alive_time=3*60, vy = 3))

# 1500 ~ 2500
data.insert(1500, RandomEnemy(320, 100, shoot_time = 5, bullet_speed=5, alive_time=7*60))

# 2500 ~ 3500
data.insert(2500, RandomEnemyWithFall(320, 100, shoot_time = 5, bullet_speed=5, alive_time=7*60))

rep = OpReplay.read_from_file('./data/replay.txt')
G = Replay(Player(320, 400), data, rep)
print(G.play_video())
