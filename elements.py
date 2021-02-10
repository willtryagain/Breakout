import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock
import math

import settings 
from meta import Meta

class Brick(Meta):
    '''
    Brick class inherits from Meta class
    '''
    def __init__(self, window_height, window_width, x=0, y=0):
        if type(x) != int or type(y) != int:
            raise ValueError
        super().__init__(window_height, window_width, np.array([x, y], dtype='float32'), np.array([1, 1]))

        self._ascii = np.array([[Fore.YELLOW + Style.BRIGHT + '$']], dtype='object')

class Ball(Meta):
    '''

    '''

    def __init__(self, window_height, window_width, x=0, y=0):
        if type(x) != int or type(y) != int:
            raise ValueError

        super().__init__(window_height, window_width, np.array([x, y], dtype='float32'), np.array([1, 3]))

        self._rprsnttn = np.array([[Back.WHITE + ' ', Back.WHITE + ' ', Style.BRIGHT + Fore.WHITE + 'D']], dtype='object')
        self._velocity = np.array([0, settings.BALL_SPEED], dtype='float32')

    def reset_a(self):
        super().reset_a()

        self._a[0] += settings.GRAVITY_X * 0.1





