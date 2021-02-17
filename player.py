from time import monotonic as clock
from colorama import Fore, Back, Style

class Player:
    def __init__(self, lives=3, score=0):
        self._lives = lives
        self._score = score
        self._start = clock()

    def lose_life(self):
        self._lives -= 1
        print(self._lives)

    def display_stats(self):
        print(Style.RESET_ALL + Style.BRIGHT, end='')
        print('\033[0K', end='') # EOL
        print('SCORE:', str(self._score).rjust(1), end='\t')
        print('LIVES:', str(self._lives).rjust(3), end='\t')
        print('TIME:', str(self._start).rjust(5), end='\t')
