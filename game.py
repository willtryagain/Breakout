import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep

import settings
from screen import Screen
from kbhit import KBHit
from player import Player

class Game:
    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        self._height = int(rows) - settings.BUFFER_DOWN
        self._width = int(cols) - settings.BUFFER_RIGHT

        self._screen = Screen(self._height, self._width)
        self._keyboard = KBHit()
        self._player = Player(self._height, self._width, settings.PLAYER_START_Y)

    def handle_input(self):
        if self._keyboard.kbhit():
            key = self._keyboard.getch()

            if key == 'a':
                print('left')
            elif key == 'd':
                print('right')

            elif key == 'q':
                self.end_game(lost=True)

            self._keyboard.flush()

    def end_game(self, lost=True):
        self._screen.end_game(lost)
        while True:
            if self._keyboard.kbhit():
                if self._keyboard.getch() == 'e':
                    break
        self._keyboard.set_normal_term()
        raise SystemExit

    def play(self):
        while True:
            self.handle_input()

            self._screen.reset_fg()

# print(Back.GREEN + ' ' * 5)
# print(Back.RED + ' ' * 5)
