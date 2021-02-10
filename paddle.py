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
        super().__init__(window_height, window_width, np.array([window_height - settings.BOTTOM_HEIGHT - 4, y]), np.array([4, 3]))
        self._a = np.array([settings.GRAVITY_X])
        self._ascii = np.array([
            [' ', Fore.CYAN + Style.BRIGHT + '_', ' '],
            [Fore.CYAN + Style.BRIGHT + '|', Fore.GREEN +
                Style.BRIGHT + 'O', Fore.CYAN + Style.BRIGHT + '`'],
            [Fore.CYAN + Style.BRIGHT + '[', Style.BRIGHT + Back.GREEN + ' ', Fore.CYAN + Style.BRIGHT + ']'],
            [' ', Fore.CYAN + Style.BRIGHT + 'J', Fore.CYAN + Style.BRIGHT + 'L']
        ], dtype='object')
      
    def is_out(self):
        return (self._position[0] < 0), (self._position[1] < 0), (self._position[0] + self._size[0] > self._window_h), (self._position[1] + self._size[1] > self._window_w)

    def show(self):
        return np.round(self._position).astype(np.int32), self._size, self._ascii

    def push(self, key):
        if key == 'a':
            self._a[0] -= settings.KEY_FORCE
        elif key == 'd':
            self._a[0] += settings.KEY_FORCE

    def reset_a(self):
        super().reset_a()

        self._a[0] += settings.GRAVITY_X
