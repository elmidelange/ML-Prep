from collections import Counter
import urllib.request as request
import numpy as np
import string
import random

target_url = "http://www.norvig.com/ngrams/sowpods.txt"
data = request.urlopen(target_url)
words = list()
for word in data:
    words.append(word.decode("utf-8").strip())



class Board:
    def __init__(self):
        self.words_available = list(string.ascii_uppercase)
        self.strikes = []
        self.chosen_letters = []
        self.word_to_guess = list(random.choice(words))

    def __str__(self):
        board_str = 'Available: ' + ','.join(self.words_available) + '\n'
        board_str += f"Strikes ({len(self.strikes)}): {','.join(self.strikes)} \n"
        man_str = [" O\n", "\\", "|", "/ \n", "/", "\\"]
        man_str = ''.join(man_str[:len(self.strikes)])
        word_str = [x if x in self.chosen_letters else '_' for x in self.word_to_guess ]
        word_str = ','.join(word_str)
        return board_str + word_str + '\n' + man_str  + '\n'

    def is_finished(self):
        if len(self.strikes) == 6 or self.check_win():
            return True
        else:
            return False

    def validate_letter(self, letter):
        if letter not in self.words_available:
            return False
        if letter not in self.word_to_guess:
            self.strikes.append(letter)
            print('Not found in word!')
            print(f'You have {6-len(self.strikes)} guesses remaining')
            return True
        print('Found in word!')
        return True

    def choose_letter(self, letter):
        self.words_available.remove(letter)
        self.chosen_letters.append(letter)

    def check_win(self):
        if all(elem in self.chosen_letters for elem in self.word_to_guess):
            return True
        return False


class Player:
    def choose_letter(self):
        letter = input('\nPlease select a letter [A-Z]: ')
        if len(letter) == 1 and letter.isalpha():
            return letter
        return self.choose_letter()


class Game(Board, Player):
    def __init__(self):
        self.board = Board()
        self.player = Player()


    def play(self):
        print('Welcome to Hangman!\n')
        while not self.board.is_finished():
            print(self.board)
            self.make_move()

        print(self.board)
        if self.board.check_win():
            print('You won!')
        else:
            print('You lost!')

        play_again = input('\nWould you like to play again? [y/n]: ')
        if play_again[0].upper() == 'Y':
            print('Starting new game\n')
            self.reset_board()
            self.play()
        else:
            print('Thank you for playing')

    def make_move(self):
        letter = self.player.choose_letter()
        if self.board.validate_letter(letter):
            self.board.choose_letter(letter)
        else:
            print('Invalid selection! Choose another letter\n')
            self.make_move()

    def reset_board(self):
        self.board = Board()
        self.player = Player()


if __name__ == "__main__":
    g = Game()
    g.play()
