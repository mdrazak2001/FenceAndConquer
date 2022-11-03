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
    if perimeter_cells.count(0):
        return False
    return True


def distance(x, y, target_x, target_y):
    return abs(x - target_x) + abs(y - target_y)


class player:
    def __init__(self):
        self.enemy_pos = []
        self.visited_cells = set()
        self.initial_corners = dict()

    def get_enemy_pos(self, B):
        B = np.array(B)
        for ix, iy in np.ndindex(B.shape):
            if B[ix, iy] == 2:
                if [ix, iy] not in self.enemy_pos:
                    self.enemy_pos.append([ix, iy])
                    return [ix, iy]
        return self.enemy_pos[-1]

    def square_capture(self, x, y, targets, B):
        targets.sort(key=lambda corner: (corner[0], corner[1]))
        shortest_dist = 100
        target = targets[0]
        corners = 0
        for tx, ty in targets:
            if B[tx][ty] == 1:
                corners += 1
        if corners == 1 and [x, y] in targets:
            if str(targets) not in self.initial_corners:
                self.initial_corners[str(targets)] = [x, y]
        target_conflicts = []
        if corners == 4:
            target = self.initial_corners[str(targets)]
            target_conflicts = [target]
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
            move_cell.sort(key=lambda corner: (corner[1], corner[2]))
            return move_cell[0][0]

        return get_dirs(x, y, target_conflicts)

    def wher2go(self, corners, cur_x, cur_y, Board, enemy_x, enemy_y):
        index = 0
        return corners[index]

    def find_squares(self, Board):
        corners = []
        a, b, c, d = [0, 0], [5, 0], [5, 5], [0, 5]
        # print(square_completed([a, b, c, d], Board))
        for i in range(30):
            try:
                a_ = a.copy()
                b_ = b.copy()
                c_ = c.copy()
                d_ = d.copy()
                for j in range(30):
                    if not perimeter_covered([a_, b_, c_, d_], Board):
                        corners.append([a_.copy(), b_.copy(), c_.copy(), d_.copy()])
                    a_[0] += 1
                    b_[0] += 1
                    c_[0] += 1
                    d_[0] += 1
                a[1] += 1
                b[1] += 1
                c[1] += 1
                d[1] += 1
            except:
                continue
        # print('corners = ', corners)
        return corners

    def move(self, B, N, cur_x, cur_y):
        enemy_head = self.get_enemy_pos(B)
        self.find_squares(B)
        print(enemy_head, [cur_x, cur_y])
        move = 1, 0
        if not perimeter_covered([[0, 0], [5, 0], [5, 5], [0, 5]], B):
            move = self.square_capture(cur_x, cur_y, [[0, 0], [5, 0], [5, 5], [0, 5]], B)
        elif not perimeter_covered([[6, 0], [11, 0], [11, 5], [6, 5]], B):
            move = self.square_capture(cur_x, cur_y, [[6, 0], [11, 0], [11, 5], [6, 5]], B)
        elif not perimeter_covered([[12, 0], [17, 0], [17, 5], [12, 5]], B):
            move = self.square_capture(cur_x, cur_y, [[12, 0], [17, 0], [17, 5], [12, 5]], B)
        return move
