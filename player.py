import numpy as np

from time import monotonic as clock
from colorama import Fore, Back, Style

class Player:
    def __init__(self, lives=3, score=0):
        self._lives = lives
        self._score = score
        self._start = clock()
        self._score = score

    def lose_life(self):
        self._lives -= 1
        

    def display_stats(self, length, ball):
        vx = ball._velocity.x
        vy = ball._velocity.y
        
        time_passed = int(clock() - self._start)
        speed = int(np.sqrt(vx**2 + vy**2))
        print(Style.RESET_ALL + Style.BRIGHT, end='')
        print('\033[0K', end='') # EOL
        print('SCORE:', str(self._score).rjust(1), end='\t')
        print('BALLS:', str(self._lives).rjust(1), end='\t')
        print('TIME:', str(time_passed).rjust(5), end='\t')
        print('PADDLE:', str(length).rjust(3), end='\t')
        print('SPEED', str(speed).rjust(3))