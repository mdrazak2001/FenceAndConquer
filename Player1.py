from collections import defaultdict
from itertools import product

import numpy as np

'''
(1, 0) ->
(-1, 0) <-
(0, 1) down
(0, -1) up
'''


def perimeter_covered(corners, B):
    def get_cells_between_coords(corner1, corner2, corner3, corner4, Board):
        cells = []
        initial_corner = corner1.copy()
        while corner1 != corner2:
            cells.append(Board[corner1[0]][corner1[1]])
            corner1[0] += 1
        while corner1 != corner3:
            cells.append(Board[corner1[0]][corner1[1]])
            corner1[1] += 1
        while corner1 != corner4:
            cells.append(Board[corner1[0]][corner1[1]])
            corner1[0] -= 1
        while corner1 != initial_corner:
            cells.append(Board[corner1[0]][corner1[1]])
            corner1[1] -= 1
        return cells

    def get_perimeter_cells(Corners, Board):
        Corners.sort(key=lambda corner: (corner[0], corner[1]))
        a, b, c, d = Corners[0], Corners[1], Corners[2], Corners[3]
        cells = get_cells_between_coords(a, c, d, b, Board)
        return cells

    perimeter_cells = get_perimeter_cells(corners, B)
    return perimeter_cells.count(0) == 0


def distance(x, y, target_x, target_y):
    return abs(x - target_x) + abs(y - target_y)


class player:
    def __init__(self):
        self.enemy_pos = []
        self.visited_cells = []
        self.capturing_square = None

    def get_enemy_pos(self, B):
        B = np.array(B)
        for ix, iy in np.ndindex(B.shape):
            if B[ix, iy] == 2:
                if [ix, iy] not in self.enemy_pos:
                    self.enemy_pos.append([ix, iy])
                    return [ix, iy]
        return self.enemy_pos[-1]

    def square_capture(self, x, y, targets, B):
        print("targets ", targets)
        targets.sort(key=lambda corner: (corner[0], corner[1]))
        shortest_dist = 100
        target = targets[0]
        corners = 0
        for tx, ty in targets:
            if B[tx][ty] == 1:
                corners += 1
        target_conflicts = []
        # print('corners ', corners)
        if corners == 4:
            # print('visited_cells, ', self.visited_cells)
            for visited_cell in self.visited_cells:
                if visited_cell in targets:
                    # print(visited_cell)
                    target_conflicts = [visited_cell]
                    break
        else:
            best_targets = []
            for tx, ty in targets:
                temp_dist = distance(x, y, tx, ty)
                if B[tx][ty] != 1 and temp_dist <= shortest_dist:
                    shortest_dist = temp_dist
                    target = [tx, ty]
                    best_targets.append([target, shortest_dist])
            best_targets = [i for i in best_targets if i[1] == shortest_dist]
            for best_target in best_targets:
                target_conflicts.append(best_target[0])
            # print(shortest_dist, best_targets)

        # print('target_conflicts ', target_conflicts)

        def get_dirs(cur_x, cur_y, Target_conflicts):
            all_dirs = [[cur_x + 1, cur_y], [cur_x - 1, cur_y], [cur_x, cur_y + 1], [cur_x, cur_y - 1]]
            Shortest_dist = 100
            move = (0, 1)
            move_cell = []
            for TARGET in Target_conflicts:
                for new_x, new_y in all_dirs:
                    try:
                        if (0 <= new_x < 30) and (0 <= new_y < 30):
                            new_dist = distance(new_x, new_y, TARGET[0], TARGET[1])
                            if new_dist < Shortest_dist:
                                Shortest_dist = new_dist
                                if new_x == cur_x + 1:
                                    move = (1, 0)
                                    move_cell.append([move, B[cur_x + 1][cur_y], Shortest_dist])
                                elif new_x == cur_x - 1:
                                    move = (-1, 0)
                                    move_cell.append([move, B[cur_x - 1][cur_y], Shortest_dist])
                                elif new_y == cur_y + 1:
                                    move = (0, 1)
                                    move_cell.append([move, B[cur_x][cur_y + 1], Shortest_dist])
                                elif new_y == cur_y - 1:
                                    move = (0, -1)
                                    move_cell.append([move, B[cur_x][cur_y - 1], Shortest_dist])
                    except Exception as e:
                        print(e)
                        continue
            # print('move cells ', move_cell)
            move_cell.sort(key=lambda corner: (corner[2]))
            # move_cell.sort(key=lambda corner: (corner[1], corner[2]))
            # print('move cells ', move_cell)
            return move_cell[0][0]

        return get_dirs(x, y, target_conflicts)

    def rate_squares(self, corners, cur_x, cur_y, Board, enemy_x, enemy_y):
        rating = defaultdict(int)
        alpha, beta, gamma = 1, 1, 1
        for square in corners:
            lu, ld, rd, ru = square
            if [cur_x, cur_y] in square:
                return square
            empty_cells = sum(
                1 for i, j in product(range(lu[0], ld[0] + 1), range(lu[1], ru[1] + 1)) if Board[i][j] == 0)
            tuple_square = tuple(map(tuple, square))
            # rating[tuple_square] += alpha * (empty_cells / ((ru[1] - lu[1] + 1) * (rd[0] - ld[0] + 1)))
            rating[tuple_square] += beta * (1 / distance(cur_x, cur_y, lu[0], lu[1]))
            # rating[tuple_square] += gamma * distance(enemy_x, enemy_y, lu[0], lu[1])

        return max(rating.items(), key=lambda x: x[1])[0]

    def find_squares(self, Board):
        def get_sized_corners(lu, ru, rd, ld):
            corners = []
            for i in range(30):
                lu_copy = lu.copy()
                ru_copy = ru.copy()
                rd_copy = rd.copy()
                ld_copy = ld.copy()
                for j in range(30):
                    try:
                        if not perimeter_covered([lu_copy, ru_copy, rd_copy, ld_copy], Board) \
                                and all(Board[j][i] == 0 for i, j in
                                        product(range(lu_copy[1], ld_copy[1] + 1), range(lu_copy[0], ru_copy[0] + 1))):
                            if [lu_copy.copy(), ru_copy.copy(), rd_copy.copy(), ld_copy.copy()] not in corners:
                                corners.append([lu_copy.copy(), ru_copy.copy(), rd_copy.copy(), ld_copy.copy()])
                    except:
                        continue
                    lu_copy[0] += 1
                    ru_copy[0] += 1
                    rd_copy[0] += 1
                    ld_copy[0] += 1
                    if ru_copy[0] >= 30:
                        break
                lu[1] += 1
                ru[1] += 1
                rd[1] += 1
                ld[1] += 1
                if lu[1] >= 30:
                    break
            return corners

        res_corners = []
        res_corners.extend(get_sized_corners([0, 0], [5, 0], [5, 5], [0, 5]))  # 6x6
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [5, 0], [5, 4], [0, 4]))  # 6x5
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [4, 0], [4, 5], [0, 5]))  # 5x6
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [4, 0], [4, 4], [0, 4]))  # 5x5
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [4, 0], [4, 3], [0, 3]))  # 5x4
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [3, 0], [3, 4], [0, 4]))  # 4x5
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [3, 0], [3, 3], [0, 3]))  # 4x4
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [3, 0], [3, 2], [0, 2]))  # 4x3
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [2, 0], [2, 3], [0, 3]))  # 3x4
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [2, 0], [2, 2], [0, 2]))  # 3x3
        print('corners = ', res_corners)
        return res_corners

    def enemy_entered(self, B):
        lu, ld, rd, ru = self.capturing_square
        return any(B[i][j] == 2 for i, j in product(range(lu[0], ld[0] + 1), range(lu[1], ru[1] + 1)))

    def move(self, B, N, cur_x, cur_y):
        self.visited_cells.append([cur_x, cur_y])
        enemy_head = self.get_enemy_pos(B)
        enemy_x, enemy_y = enemy_head[0], enemy_head[1]
        # print(self.initial_corners)
        if self.capturing_square is None or perimeter_covered(self.capturing_square, B):
            squares = self.find_squares(B)
            corners = self.rate_squares(squares, cur_x, cur_y, B, enemy_x, enemy_y)
            corners = [list(x) for x in corners]
            self.capturing_square = corners
            move = self.square_capture(cur_x, cur_y, self.capturing_square, B)
        else:
            move = self.square_capture(cur_x, cur_y, self.capturing_square, B)
        print(self.capturing_square)
        # print(self.find_squares(B)[0])
        # move = self.square_capture(cur_x, cur_y, corners, B)

        return move
        # move = 1, 0
        # if not perimeter_covered([[0, 0], [5, 0], [5, 5], [0, 5]], B):
        #     move = self.square_capture(cur_x, cur_y, [[0, 0], [5, 0], [5, 5], [0, 5]], B)
        # elif not perimeter_covered([[6, 0], [11, 0], [11, 5], [6, 5]], B):
        #     move = self.square_capture(cur_x, cur_y, [[6, 0], [11, 0], [11, 5], [6, 5]], B)
        # elif not perimeter_covered([[12, 0], [17, 0], [17, 5], [12, 5]], B):
        #     move = self.square_capture(cur_x, cur_y, [[12, 0], [17, 0], [17, 5], [12, 5]], B)
        # return move
