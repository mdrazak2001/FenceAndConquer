import random
from time import sleep
import numpy as np

enemy_pos = []

def get_enemy_pos(B):
    B = np.array(B)
    for iy, ix in np.ndindex(B.shape):
        if B[iy,ix] == 2:
            if [iy, ix] not in enemy_pos:
                enemy_pos.append([iy, ix])
                return [iy, ix]
    return enemy_pos[-1]

def distance(x, y, target_x, target_y):
    return abs(x - target_x) + abs(y - target_y)


class player:
    def __init__(self):
        pass

    

    def move(self,B,N,cur_x,cur_y):
        enemy_head = get_enemy_pos(B)
        print(enemy_head, [cur_x, cur_y])
        print(distance(cur_x, cur_y, 0, 0))
        return (-1,0)
        if random.randint(0,2)==0:
            return (0,random.choice([-1,1]))
        else:
            return (random.choice([-1,1]),0)
   