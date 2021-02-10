import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep

import settings
from screen import Screen
from kbhit import KBHit
from paddle import Paddle

class Game:
    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        self._height = int(rows) - settings.BUFFER_DOWN
        self._width = int(cols) - settings.BUFFER_RIGHT

        self._screen = Screen(self._height, self._width)
        self._keyboard = KBHit()
        self._frame_count = 0

        self._lives = settings.MAX_LIVES
        self._score = 0
        self._start_time = clock()

        self._paddle = Paddle(self._height, self._width, settings.PADDLE_START_Y)

    def handle_input(self):
        if self._keyboard.kbhit():
            key = self._keyboard.getch()

            if key in ['a', 'd']:
                self._paddle.push(key)
            elif key == 'q':
                self.end_game(lost=True)

            self._keyboard.flush()

    def paint_objs(self):
        self._screen.add(self._paddle)

    def move_objs(self):
        self._paddle.move()
    
    def reset_a_objs(self):
        self._paddle.reset_a()

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
            loop_start_time = clock()

            self.handle_input()

            self._screen.reset_fg()
            self.paint_objs()

            self._screen.print_board(self._frame_count)
            self._frame_count += 1
            while clock() - loop_start_time < 0.1:
                pass
# print(Back.GREEN + ' ' * 5)
# print(Back.RED + ' ' * 5)
