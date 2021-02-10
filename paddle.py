import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock

import settings
from meta import Meta

class Paddle(Meta):

    def __init__(self, window_height, window_width, y=0):
        self._a = np.array([settings.GRAVITY_X])
        self._ascii = np.array([
            [' ', Fore.CYAN + Style.BRIGHT + '_', ' '],
            [Fore.CYAN + Style.BRIGHT + '|', Fore.GREEN +
                Style.BRIGHT + 'O', Fore.CYAN + Style.BRIGHT + '`'],
            [Fore.CYAN + Style.BRIGHT + '[', Style.BRIGHT + Back.GREEN + ' ', Fore.CYAN + Style.BRIGHT + ']'],
            [' ', Fore.CYAN + Style.BRIGHT + 'J', Fore.CYAN + Style.BRIGHT + 'L']
        ], dtype='object')
      
    def is_out(self):
        return (self._pos[0] < 0), (self._pos[1] < 0), (self._pos[0] + self._size[0] > self._window_h), (self._pos[1] + self._size[1] > self._game_w)

    def show(self):
        return np.round(self._pos).astype(np.int32), self._size, self._ascii

    def push(self, key):
        if key == 'a':
            self.a[1] -= settings.KEY_FORCE
        elif key == 'd':
            self.a[1] += settings.KEY_FORCE

    def reset_a()