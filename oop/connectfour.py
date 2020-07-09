class Board:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = self.blank_board()

    def __str__(self):
        # x-axis -> i
        # y-axis -> j
        boardTranspose = list(map(list, zip(*self.board)))
        boardString = ''
        for row in boardTranspose[::-1]:
            boardString += ('\t' + ' | '.join(str(el) for el in row) + '\n')
        boardString += ('\t' + '___' * self.board_size) + '\n'
        boardString += ('\t' + ' | '.join([str(i) for i in range(self.board_size)]) + '\n')
        return boardString

    def set_item(self, column, value):
        # Get the row index of the first empty slot
        j = self.board[column].index(' ')
        self.board[column][j] = value

    def blank_board(self):
        # Blank 4x4 board
        return [[' ' for i in range(self.board_size)] for j in range(self.board_size)]

    def check_move(self, column):
        # Check board size
        if column < 0 or column > self.board_size - 1:
            print(f'Column needs to be in range (0,{self.board_size})')
            return False
        # Check for full column
        if ' ' not in self.board[column]:
            print(f'Column {column} is full! Try another one')
            return False
        return True

    def check_status(self):
        # Check for full column
        for column in self.board:
            if all((el == column[0]) and (el != ' ') for el in column):
                return 'WIN'
        # Check full row
        boardTranspose = map(list, zip(*self.board))
        for row in boardTranspose:
            if all((el == row[0]) and (el != ' ') for el in row):
                return 'WIN'
        # Check diagonal (bottom left to top right)
        diagonal = [r[i] for i, r in enumerate(self.board)]
        if all((el == diagonal[0]) and (el != ' ') for el in diagonal):
            return 'WIN'
        # Check diagonal (top left to bottom right)
        diagonal = [r[-i-1] for i, r in enumerate(self.board)]
        if all((el == diagonal[0]) and (el != ' ') for el in diagonal):
            return 'WIN'
        # Check for full board
        if not ' ' in (item for sublist in self.board for item in sublist):
            return 'DRAW'

        return 'CONTINUE'


class Player:
    def __init__(self, number):
        self.player_num = number

    def make_move(self, board):
        # Get valid column input
        valid = False
        while not valid:
            print('Please select a column')
            column = input()
            if not column.isnumeric():
                print('Column must be an integer (e.g. 0)')
                continue
            if (board.check_move(int(column))):
                # Valid move
                valid = True
        board.set_item(int(column), str(self.player_num))


class Game:
    def __init__(self):
        self.finished = False

    def start(self):
        board = Board(self.get_size())
        player1 = Player(1)
        player2 = Player(2)
        self.play_game(board, [player1, player2])

    def play_game(self, board, players):
        # Loop through turns and check for win/loss/draw
        while not self.finished:
            for player in players:
                # Show board
                print(str(board))
                # Player to move
                player.make_move(board)
                status = board.check_status()
                if status == 'WIN':
                    print(str(board))
                    print(f"Player {player.player_num} won!")
                    self.finished = True
                    break
                elif status == 'DRAW':
                    print(str(board))
                    print("It's a draw! The board is full")
                    self.finished = True
                    break
                elif status == 'LOSE':
                    print(str(board))
                    print(f"Player {player.player_num} lost!")
                    self.finished = True
                    break

    def get_size(self):
        print('How big would you like the board? (e.g. 4)')
        valid = False
        while not valid:
            board_size = input()
            if not board_size.isnumeric():
                print('Please enter a number')
                continue
            sizeInt = int(board_size)
            if sizeInt < 0 or sizeInt > 10:
                print('Please enter a number between 0 and 10')
                continue
            valid = True
        return sizeInt


if __name__ == '__main__':
    game = Game()
    game.start()
