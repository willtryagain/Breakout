import numpy as np
from colorama import Fore, Back, Style

from meta import Meta
from velocity import Velocity

class Ball(Meta):
    def __init__(self, game_height, game_width):
        self._ascii = np.array([
            Back.BLUE + Style.BRIGHT + '(', 
            Back.BLUE + Style.BRIGHT + ')'],
            dtype='object'
        ).reshape(1, -1)
        self._velocity = Velocity(-1, -1) # composition
        self._cache = None
        super().__init__(game_height, game_width, [game_height-2,\
             game_width//2 - 3], self._ascii.shape, self._ascii)

    #     return [x0 + self._size[0] - 1, y0 + self._size[1] - 1]

    def move(self):
        self._pos[0] += self._velocity.vx
        self._pos[1] += self._velocity.vy
        

    def lost(self):
        # left, right, top, bottom
        # return ((self._pos[1] < 0),  (self._pos[0] + self._size[0] > self._)self._pos[0] < 0),  (self._pos[0] + self._size)
        pass
