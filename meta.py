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

        self._position = position
        self._size = size
        self._vel = np.array([0, -settings.GAME_SPEED], dtype='float32') 
        self._a = np.array([0, 0], dtype='float32')

        self._ascii = np.array([[' ' for j in range(self._size[1])] for i in range(self._size[0])], dtype='object')

    def show(self):
        return np.round(self._position).astype(np.int32), self._size, self._ascii

    def at_bottom(self):
        '''
        '''
        return int(round(self._position[0] + self._size[0])) >= self._window_h - settings.BOTTOM_HEIGHT

    def at_top(self):
        return int(round(self._position[0])) <= settings.TOP_DEPTH

    def is_out(self):
        '''

        '''
        return (self._position[0] + self._size[0] - 1 < 0), (self._position[1] + self._size[1] - 1 < 0), (self._position[0] >= self._window_h), (self._position[1] >= self._window_w)

    def reset_a(self):
        self._a = np.array([0, 0], dtype='float32')

    def add_a(self, a):
        if type(a) != np.ndarray:
            raise ValueError
    
        self._a += a

    def move(self):
        self._vel += self._a 
        self._position += self._vel

        # if self.at_bottom():
        #     if self._vel[0] > 0:
