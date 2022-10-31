import random
import numpy as np

'''
(1, 0) ->
(-1, 0) <-
(0, 1) down
(0, -1) up
'''


class player:
    def __init__(self):
        self.enemy_pos = []
        self.visited_vertex_cells = set()
        self.visited_cells = set()
        self.initial_corner = []

    def get_enemy_pos(self, B):
        B = np.array(B)
        for ix, iy in np.ndindex(B.shape):
            if B[ix, iy] == 2:
                if [ix, iy] not in self.enemy_pos:
                    self.enemy_pos.append((ix, iy))
                    return [ix, iy]
        return self.enemy_pos[-1]

    def distance(self, x, y, target_x, target_y):
        return abs(x - target_x) + abs(y - target_y)

    def square_capture(self, x, y, targets, B):

        if (x, y) in self.visited_vertex_cells:
            print("Square Done")
            self.visited_vertex_cells = set()
            return -1
        self.visited_vertex_cells.add((x, y))
        shortest_dist = 100
        target = targets[0]
        corners = 0
        for tx, ty in targets:
            if B[tx][ty] == 1:
                corners += 1

        if corners == 1:
            self.initial_corner = [x, y]

        if corners == 4:
            target = self.initial_corner
        else:
            for tx, ty in targets:
                temp_dist = self.distance(x, y, tx, ty)
                if B[tx][ty] != 1 and temp_dist < shortest_dist:
                    shortest_dist = temp_dist
                    target = [tx, ty]

        all_dirs = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        shortest_dist = 100
        move = (0, 1)
        for new_x, new_y in all_dirs:
            if (0 <= new_x < 30) and (0 <= new_y < 30):
                new_dist = self.distance(new_x, new_y, target[0], target[1])
                if new_dist < shortest_dist:
                    shortest_dist = new_dist
                    if new_x == x + 1:
                        move = (1, 0)
                    elif new_x == x - 1:
                        move = (-1, 0)
                    elif new_y == y + 1:
                        move = (0, 1)
                    else:
                        move = (0, -1)
        return move

    def move(self, B, N, cur_x, cur_y):
        enemy_head = self.get_enemy_pos(B)
        # print(enemy_head, [cur_x, cur_y])
        # print(self.distance(cur_x, cur_y, 0, 0))
        print(cur_x, cur_y)
        move = self.square_capture(cur_x, cur_y, [[0, 0], [5, 0], [5, 5], [0, 5]], B)
        if move == -1:
            move2 = self.square_capture(cur_x, cur_y, [[6, 0], [11, 0], [11, 5], [6, 5]], B)
            return move2
        return move
        # return self.square_capture(cur_x, cur_y, [[0, 23], [6, 23], [6, 29], [0, 29]], B)
