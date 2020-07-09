#Objective: Coding Tic Tac Toe from scratch

class TicTacToe:
    def __init__(self):
        self.finished = False

    def play_game(self):
        # initialise players
        human = Human()
        agent = Agent()
        # play until player leaves
        while not self.finished:
            # initialise game
            board = Board()
            print(str(board))
            # play game until finished
            while not board.finished:
                # Player 1 to move
                human.make_move(board)
                print(str(board))
                if board.check_win():
                    print(board.winner)
                # Agent to make a move
                agent.make_move(board)
                print(str(board))
                if board.check_win():
                    print(board.winner)
            # Ask to play again
            if self.play_again() == 'N':
                self.finished = True

    def play_again(self):
        print('Would you like to play again? (Y/N)')
        answer = input()
        while answer not in ('Y', 'N'):
            print('Please select Y or N')
            answer = input()
        return answer



class Board:
    def __init__(self):
        self.board = self.blank_board()
        self.finished = False

    def __str__(self):
        template = """
                |00|01|02|
                _______
                |01|11|12|
                _______
                |20|21|22|
        """
        board_str = template[:]
        for i in range(3):
            for j in range(3):
                board_str = board_str.replace(str(i)+str(j), self.board[i][j])
        return board_str

    def blank_board(self):
        return [[' ' for i in range(3)] for j in range(3)]

    def valid_move(self, x, y):
        if self.board[x][y] != ' ':
            return False
        else:
            return True

    def update(self, x, y, letter):
        self.board[x][y] = letter

    def check_win(self):
        pass
        # Check for full board

        # Check for verical win
        # Check for horizontal win
        # Check for diagonal win

class Player:
    def __init__(self):
        self.score = 0

class Agent(Player):
    def __init__(self):
        self.letter = 'O'

    def make_move(self, board):
        for i in range(3):
            for j in range(3):
                if board.valid_move(i,j):
                    board.update(i,j,'O')
                    return


class Human(Player):
    def __init__(self):
        self.letter = 'X'

    def make_move(self, board):
        valid_move = False
        while not valid_move:
            # Take input
            print('Please enter your coordinates (e.g. top left is 00)')
            pos = input()
            while not self.validate_input(pos):
                print('Please enter coordinates between 00 and 22')
                pos = input()
            x, y = int(pos[0]), int(pos[1])
            # Update board
            if board.valid_move(x, y):
                board.update(x,y,self.letter)
                valid_move = True
            else:
                print('Invalid move, please try again.')


    def validate_input(self, pos):
        # Check for binary value between '00' and '22'
        if len(pos) != 2:
            print('Input too long')
            return False
        if not pos.isnumeric():
            perint('Input is not numeric')
            return False
        for p in pos:
            if int(p) > 2 or int(p) < 0:
                print('Value is too small/large', p)
                return False
        return True



if __name__ == "__main__":

        game = TicTacToe()
        # game.print_board()
        game.play_game()
