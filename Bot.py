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
    abs_x = abs(x - target_x)
    abs_y = abs(y - target_y)
    return min(abs_x + abs_y, 30 - abs_x + 30 - abs_y,
               30 - abs_x + abs_y, 30 - abs_y + abs_x)


class player:
    def __init__(self):
        self.enemy_pos = []
        self.visited_cells = []
        self.capturing_square = None
        self.step = 0
        self.squares_done = False

    def capture_cells(self, B, cur_x, cur_y):
        def get_dirs(cur_x, cur_y, Target_conflicts):
            all_dirs = [[cur_x + 1, cur_y], [cur_x - 1, cur_y], [cur_x, cur_y + 1], [cur_x, cur_y - 1]]
            Shortest_dist = 100
            move = (0, 1)
            move_cell = []
            for TARGET in Target_conflicts:
                for new_x, new_y in all_dirs:
                    try:
                        if new_x == 30:
                            new_x = 0
                        if new_y == 30:
                            new_y = 0
                        if new_x == -1:
                            new_x = 29
                        if new_y == -1:
                            new_y = 29

                        new_dist = distance(new_x, new_y, TARGET[0], TARGET[1])
                        if new_dist < Shortest_dist:
                            Shortest_dist = new_dist
                            if new_x == cur_x + 1 or (cur_x + 1 == 30 and new_x == 0):
                                move = (1, 0)
                                move_cell.append([move, Shortest_dist])
                            elif new_x == cur_x - 1 or (cur_x - 1 == -1 and new_x == 29):
                                move = (-1, 0)
                                move_cell.append([move, Shortest_dist])
                            elif new_y == cur_y + 1 or (cur_y + 1 == 30 and new_y == 0):
                                move = (0, 1)
                                move_cell.append([move, Shortest_dist])
                            elif new_y == cur_y - 1 or (cur_y - 1 == -1 and new_y == 29):
                                move = (0, -1)
                                move_cell.append([move, Shortest_dist])
                    except Exception as e:
                        print(e)
                        continue
            move_cell.sort(key=lambda corner: (corner[1]))
            return move_cell[0][0]

        cells = [[y, x] for x, y in product(range(30), range(30)) if B[y][x] == 0]
        if not cells:
            return 0, 0
        closest_cell = min(cells, key=lambda x: distance(cur_x, cur_y, x[0], x[1]))
        return get_dirs(cur_x, cur_y, [closest_cell])

    def square_capture(self, x, y, targets, B):
        targets.sort(key=lambda corner: (corner[0], corner[1]))
        shortest_dist = 100
        target = targets[0]
        corners = 0
        for tx, ty in targets:
            if B[tx][ty] == 1:
                corners += 1
        target_conflicts = []
        if corners == 4:
            for visited_cell in self.visited_cells:
                if visited_cell in targets:
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

        def get_dirs(cur_x, cur_y, Target_conflicts):
            all_dirs = [[cur_x + 1, cur_y], [cur_x - 1, cur_y], [cur_x, cur_y + 1], [cur_x, cur_y - 1]]
            Shortest_dist = 100
            move = (0, 1)
            move_cell = []
            for TARGET in Target_conflicts:
                for new_x, new_y in all_dirs:
                    try:
                        if new_x == 30:
                            new_x = 0
                        if new_y == 30:
                            new_y = 0
                        if new_x == -1:
                            new_x = 29
                        if new_y == -1:
                            new_y = 29

                        new_dist = distance(new_x, new_y, TARGET[0], TARGET[1])
                        if new_dist < Shortest_dist:
                            Shortest_dist = new_dist
                            if new_x == cur_x + 1 or (cur_x + 1 == 30 and new_x == 0):
                                move = (1, 0)
                                move_cell.append([move, Shortest_dist])
                            elif new_x == cur_x - 1 or (cur_x - 1 == -1 and new_x == 29):
                                move = (-1, 0)
                                move_cell.append([move, Shortest_dist])
                            elif new_y == cur_y + 1 or (cur_y + 1 == 30 and new_y == 0):
                                move = (0, 1)
                                move_cell.append([move, Shortest_dist])
                            elif new_y == cur_y - 1 or (cur_y - 1 == -1 and new_y == 29):
                                move = (0, -1)
                                move_cell.append([move, Shortest_dist])
                    except Exception as e:
                        continue
            move_cell.sort(key=lambda corner: (corner[1]))
            return move_cell[0][0]

        return get_dirs(x, y, target_conflicts)

    def rate_squares(self, corners, cur_x, cur_y, Board):
        rating = defaultdict(int)
        alpha = 1
        for square in corners:
            lu, ld, rd, ru = square
            if [cur_x, cur_y] in square:
                return square
            tuple_square = tuple(map(tuple, square))
            rating[tuple_square] += alpha * (1 / distance(cur_x, cur_y, lu[0], lu[1]))

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
                        if (Board[lu[0]][lu[1]] == 0 or Board[ru[0]][ru[1]] == 0 or Board[rd[0]][rd[1]] == 0 or Board[ld[0]][ld[1]] == 0)\
                                and all(Board[j][i] == 0 for i, j in product(range(lu_copy[1], ld_copy[1] + 1), range(lu_copy[0], ru_copy[0] + 1))) :
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
            res_corners.extend(get_sized_corners([0, 0], [4, 0], [4, 5], [0, 5]))  # 5x6
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [3, 0], [3, 5], [0, 5]))  # 4x6
            res_corners.extend(get_sized_corners([0, 0], [5, 0], [5, 3], [0, 3]))  # 6x4
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [4, 0], [4, 4], [0, 4]))  # 5x5
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [4, 0], [4, 3], [0, 3]))  # 5x4
            res_corners.extend(get_sized_corners([0, 0], [3, 0], [3, 4], [0, 4]))  # 4x5
        if len(res_corners) == 0:
            res_corners.extend(get_sized_corners([0, 0], [3, 0], [3, 3], [0, 3]))  # 4x4
        return res_corners

    def enemy_entered(self, B):
        lu, ld, rd, ru = self.capturing_square
        return any(B[j][i] == 2 for i, j in product(range(lu[1], ld[1] + 1), range(lu[0], ru[0] + 1)))

    def move(self, B, N, cur_x, cur_y):
        self.step += 1
        self.visited_cells.append([cur_x, cur_y])
        if not self.squares_done:
            squares = self.find_squares(B)
            if not squares:
                self.squares_done = True
        if self.squares_done:
            move = self.capture_cells(B, cur_x, cur_y)
        elif self.capturing_square is None or perimeter_covered(self.capturing_square, B) or self.enemy_entered(B):
            squares = self.find_squares(B)
            corners = self.rate_squares(squares, cur_x, cur_y, B)
            corners = [list(x) for x in corners]
            self.capturing_square = corners
            move = self.square_capture(cur_x, cur_y, self.capturing_square, B)
        else:
            move = self.square_capture(cur_x, cur_y, self.capturing_square, B)
        return move
