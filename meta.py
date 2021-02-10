import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock

import settings

class Meta:
    def __init__(self, window_height, window_width, position=np.array([0, 0], dtype='float32'), size=np.array([1, 1])):

        if type(window_height) != int or type(window_width) != int\
            or type(position) != np.ndarray or type(size) != np.ndarray:
            raise ValueError('Invalid arguments')

        self._window_h = window_height
        self._window_w = window_width

        