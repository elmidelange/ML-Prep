import random
import string
import string
import re
import numpy as np
import time
words = string.ascii_lowercase

class Player:
    pass


class Board:
    def __init__(self, n_grid=None):
        if n_grid == None:
            n_grid = 9
        self.n_grid = n_grid
        self.cur = [[' ' for _ in range(self.n_grid)] for _ in range(self.n_grid)]

    def __repr__(self):
        # structured print for the board
        res = ''
        for i in range(2*(self.n_grid+1)):
            if i == 0:
                res += ' ' * 6
                res += '   '.join(words[:self.n_grid])
                res += ' ' * 2
                res += '\n'
                continue
            if i % 2 == 1:
                res += ' ' * 4  + '-'* (4*self.n_grid+1) + '\n'
                continue
            res += str(i//2) + ' '*(4-len(str(i//2))) + '| ' + ' | '.join(self.cur[(i-1)//2]) + ' |\n'
        return res


class MineBoard(Board):
    def __init__(self, n_grid=None):
        super().__init__(n_grid)

    def fill_numbers(self, pos_mines):
        numbers = [[0 for _ in range(self.n_grid)] for _ in range(self.n_grid)]
        # Loop through elements
        for row, col in pos_mines:
            # Increment surrounding counts
            if 0 <= (row -1) <= (self.n_grid - 1) and 0 <= (col-1) <= (self.n_grid - 1):
                numbers[row-1][col-1] += 1
            if 0 <= row <= (self.n_grid - 1) and 0 <= (col-1) <= (self.n_grid - 1):
                numbers[row][col-1] += 1
            if 0 <= (row +1) <= (self.n_grid - 1) and 0 <= (col-1) <= (self.n_grid - 1):
                numbers[row+1][col-1] += 1
            if 0 <= (row -1) <= (self.n_grid - 1) and 0 <= col <= (self.n_grid - 1):
                numbers[row-1][col] += 1
            if 0 <= (row +1) <= (self.n_grid - 1) and 0 <= col <= (self.n_grid - 1):
                numbers[row+1][col] += 1
            if 0 <= (row -1) <= (self.n_grid - 1) and 0 <= (col+1) <= (self.n_grid - 1):
                numbers[row-1][col+1] += 1
            if 0 <= row <= (self.n_grid - 1) and 0 <= (col+1) <= (self.n_grid - 1):
                numbers[row][col+1] += 1
            if 0 <= (row +1) <= (self.n_grid - 1) and 0 <= (col+1) <= (self.n_grid - 1):
                numbers[row+1][col+1] += 1
        self.cur = [[str(numbers[i][j]) if (i,j) not in pos_mines else '*' for i in range(self.n_grid)] for j in range(self.n_grid)]


class DisplayBoard(Board):
    def __init__(self, n_grid=None):
        super().__init__(n_grid)

    def flag(self, row, col):
        if self.cur[row][col] == 'f':
            self.cur[row][col] = ' '
        else:
            self.cur[row][col] = 'f'

    def reveal_bombs(self, pos_mines):
        for row, col in pos_mines:
            self.cur[row][col] = '*'
        print(self.cur)


class Game(Board):
    def __init__(self, n_mines=None, n_grid=None):
        if n_mines is None:
            n_mines = 10
        if n_grid is None:
            n_grid = 9
        self.mine_map = MineBoard(n_grid) # mine board
        self.dis_map = DisplayBoard(n_grid) # display board
        self.n_mines = n_mines
        self.n_grid = n_grid
        # randomly initialize the mine positions
        self.pos_mines = list(map(lambda x: divmod(x, self.n_grid), np.random.choice(self.n_grid**2, self.n_mines, replace=False)))

    def game_over(self):
        return False

    def get_move(self):
        while True:
            coords = input('Enter coordinates (e.g. a5) ')
            if len(coords) in (2,3):
                # Check first character is number, second character is letter
                if not coords[1].isdigit():
                    print('Please enter an integer for the row')
                    continue
                if not 0 <= int(coords[1]) <= 9:
                    print('The row must be between 0 and 1')
                    continue
                if coords[0] not in words[:9]:
                    print('Please enter a row character between a and i')
                    continue
                if len(coords) == 3:
                    if coords[2] != 'f':
                        print("Third character must be 'f' or empty")
                        continue
                    return coords[:2], True
                return coords, False
            else:
                print('Input must be atleast 2 characters')

    def open_square(self, row, col):
        if self.dis_map.cur[row][col] == ' ':
            self.dis_map.cur[row][col] = self.mine_map.cur[row][col]
            if 0 <= (row -1) <= (self.n_grid - 1) and 0 <= (col-1) <= (self.n_grid - 1):
                if self.mine_map.cur[row-1][col-1] == '0':
                    self.open_square(row-1, col-1)
            if 0 <= row <= (self.n_grid - 1) and 0 <= (col-1) <= (self.n_grid - 1):
                if self.mine_map.cur[row][col-1] == '0':
                    self.open_square(row, col-1)
            if 0 <= (row +1) <= (self.n_grid - 1) and 0 <= (col-1) <= (self.n_grid - 1):
                if self.mine_map.cur[row+1][col-1] == '0':
                    self.open_square(row+1, col-1)
            if 0 <= (row -1) <= (self.n_grid - 1) and 0 <= col <= (self.n_grid - 1):
                if self.mine_map.cur[row-1][col] == '0':
                    self.open_square(row-1, col)
            if 0 <= (row +1) <= (self.n_grid - 1) and 0 <= col <= (self.n_grid - 1):
                if self.mine_map.cur[row+1][col] == '0':
                    self.open_square(row+1, col)
            if 0 <= (row -1) <= (self.n_grid - 1) and 0 <= (col+1) <= (self.n_grid - 1):
                if self.mine_map.cur[row-1][col+1] == '0':
                    self.open_square(row-1, col+1)
            if 0 <= row <= (self.n_grid - 1) and 0 <= (col+1) <= (self.n_grid - 1):
                if self.mine_map.cur[row][col+1] == '0':
                    self.open_square(row, col+1)
            if 0 <= (row +1) <= (self.n_grid - 1) and 0 <= (col+1) <= (self.n_grid - 1):
                if self.mine_map.cur[row+1][col+1] == '0':
                    self.open_square(row+1, col+1)

    def check_win(self):
        return False

    def run(self):
        print('='*70)
        print("Starting Minesweeper (with {} mines on {}x{} grid.)".format(self.n_mines, self.n_grid, self.n_grid) + '\n')
        print(self.dis_map)
        print('='*70)

        # Update mine map with bombs and numbers
        self.mine_map.fill_numbers(self.pos_mines)

        # print(self.mine_map)

        while not self.game_over():
            # Ask player for their move
            coords, flag = self.get_move()
            # Convert to array index format
            col = words.index(coords[0])
            row = int(coords[1]) - 1
            # If they choose to open a square
            if not flag:
                # If square is a bomb
                if self.mine_map.cur[row][col] == '*':
                    self.dis_map.reveal_bombs(self.pos_mines)
                    print('You clicked on a mine, you lose! :(')
                    break
                # Already opened
                elif self.dis_map.cur[row][col] != ' ':
                    print('This square is already open! Please choose another one')
                # If square is 0 -> open up all square around it
                else:
                    self.open_square(row, col)
                # If all square in the grid except bombs are open, they win!
                if self.check_win():
                    print('You won!')
            # If they choose to flag it
            elif flag:
                self.dis_map.flag(row, col)
            # Display grid
            print(self.dis_map)

    def play(self):
        """
        Play the game
        """
        play_again = True
        while play_again:
            self.run()
            play_again = input('Play Again? (yes/no) ')
            play_again = True if play_again=='yes' else False


if __name__ == '__main__':
    g = Game(10, 9) # n_mines=15, n_grid=12
    g.play()
