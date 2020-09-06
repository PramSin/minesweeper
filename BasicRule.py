from random import sample, choice


class MineSweeper:

    def __init__(self, length, width, number):
        self.length = length
        self.width = width
        self.number = number
        self.boom = 0
        # noinspection PyUnusedLocal
        self.g_map = [[0 for i in range(length)] for j in range(width)]  # 纯方格：0
        self.step = 0
        self.b_num = number
        self.places = [(x, y) for x in range(length) for y in range(width)]
        self.mines = sample(self.places, self.number)
        for coord in self.mines:
            self.g_map[coord[1]][coord[0]] = 1  # 地雷：1

    def refresh(self):
        self.boom = 0
        self.b_num = self.number
        # noinspection PyUnusedLocal
        self.g_map = [[0 for i in range(self.length)] for j in range(self.width)]
        self.step = 0
        self.places = [(x, y) for x in range(self.length) for y in range(self.width)]
        self.mines = sample(self.places, self.number)
        for coord in self.mines:
            self.g_map[coord[1]][coord[0]] = 1  # 地雷：1

    def click(self, pos_x=None, pos_y=None):
        """玩家点击"""

        def count_around(x, y):
            num_of_mines = 0
            for i, j in zip([-1, 0, 1, -1, 1, -1, 0, 1], [1, 1, 1, 0, 0, -1, -1, -1]):
                if 0 <= x + i < self.length and 0 <= y + j < self.width:
                    if self.g_map[y + j][x + i] == 1 or self.g_map[y + j][x + i] == '1$':
                        num_of_mines += 1
            return num_of_mines

        def chain_blank(x, y):
            for i, j in zip([-1, 0, 1, -1, 1, -1, 0, 1], [1, 1, 1, 0, 0, -1, -1, -1]):
                if 0 <= x + i < self.length and 0 <= y + j < self.width and isinstance(self.g_map[y + j][x + i], int):
                    self.g_map[y + j][x + i] = str(count_around(x + i, y + j))
                    if not count_around(x + i, y + j):
                        chain_blank(x + i, y + j)

        while True:
            try:
                if 0 <= pos_x < self.length and 0 <= pos_y < self.width:
                    if self.g_map[pos_y][pos_x] == 0:
                        self.g_map[pos_y][pos_x] = str(count_around(pos_x, pos_y))
                        if not count_around(pos_x, pos_y):
                            chain_blank(pos_x, pos_y)
                        self.step += 1
                        return
                    elif self.g_map[pos_y][pos_x] == 1:
                        if self.step == 0:
                            while True:
                                new_mine = choice(self.places)
                                if new_mine in self.mines:
                                    continue
                                else:
                                    break
                            self.g_map[new_mine[1]][new_mine[0]] = 1
                            self.mines.remove((pos_x, pos_y))
                            self.mines.append(new_mine)
                            self.g_map[pos_y][pos_x] = str(count_around(pos_x, pos_y))
                            if not count_around(pos_x, pos_y):
                                chain_blank(pos_x, pos_y)
                            self.step += 1
                            return
                        else:
                            for coord in self.mines:
                                self.g_map[coord[1]][coord[0]] = '*'
                            self.boom = 1
                            return
                    else:
                        return
            except ValueError:
                continue

    def click_around(self, pos_x=None, pos_y=None):
        def count_around(p_x, p_y):
            num_of_flags = 0
            for i, j in zip([-1, 0, 1, -1, 1, -1, 0, 1], [1, 1, 1, 0, 0, -1, -1, -1]):
                if 0 <= p_x + i < self.length and 0 <= p_y + j < self.width:
                    if self.g_map[p_y + j][p_x + i] in ('0$', '1$'):
                        num_of_flags += 1
            return str(num_of_flags)

        if self.g_map[pos_y][pos_x] == count_around(pos_x, pos_y) \
                and not self.g_map[pos_y][pos_x] in ('0$', '1$'):
            for x, y in zip([-1, 0, 1, -1, 1, -1, 0, 1], [1, 1, 1, 0, 0, -1, -1, -1]):
                if (0 <= pos_x + x < self.length and 0 <= pos_y + y < self.width
                        and not self.g_map[pos_y + y][pos_x + x] in ('0$', '1$')):
                    self.click(pos_x + x, pos_y + y)

    def mark_mine(self, flag_x=None, flag_y=None):
        while True:
            try:
                if 0 <= flag_x < self.length and 0 <= flag_y < self.width:
                    if self.g_map[flag_y][flag_x] == 0:
                        self.g_map[flag_y][flag_x] = '0$'
                        self.b_num -= 1
                        return
                    elif self.g_map[flag_y][flag_x] == 1:
                        self.g_map[flag_y][flag_x] = '1$'
                        self.b_num -= 1
                        return
                    elif self.g_map[flag_y][flag_x] == '0$':
                        self.g_map[flag_y][flag_x] = 0
                        self.b_num += 1
                        return
                    elif self.g_map[flag_y][flag_x] == '1$':
                        self.g_map[flag_y][flag_x] = 1
                        self.b_num += 1
                        return
                    else:
                        return
            except ValueError:
                continue

    def game_judge(self):
        """判断游戏是否继续"""
        for i in range(self.length):
            for j in range(self.width):
                if self.g_map[j][i] == 0 or self.g_map[j][i] == '0$':
                    return 0
        else:
            return 1

    def show(self):
        """显示游戏内容"""
        for row in self.g_map:
            for elem in row:
                if isinstance(elem, int):
                    print('█', end=' ')
                elif isinstance(elem, str):
                    if elem == '0':
                        print(' ', end=' ')
                    else:
                        print('{}'.format(elem), end=' ')
            print()

    def play(self):
        while True:
            self.click()
            if self.boom:
                self.show()
                print('GameOver')
                return
            elif self.game_judge():
                self.show()
                print('You Win!!!')
                return
            self.show()


class EasyMode(MineSweeper):

    def __init__(self):
        super().__init__(9, 9, 10)


class MediumMode(MineSweeper):

    def __init__(self):
        super().__init__(16, 16, 40)


class HardMode(MineSweeper):

    def __init__(self):
        super().__init__(30, 16, 99)
