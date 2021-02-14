import numpy as np
from colorama import Fore, Back, Style

from velocity import Velocity

class Ball(Velocity):
    def __init__(self, game_height, game_width):

        super().__init__(0, 0)
        self._ascii = np.array([
            Back.BLUE + Style.BRIGHT + '(', 
            Back.BLUE + Style.BRIGHT + ')'],
            dtype='object'
        ).reshape(1, 2)
        self._pos = [game_height-2, game_width//2 - 1]

    def get_pos(self):
        return self._pos

    def get_tail(self):
        x0 = self._pos[0]
        y0 = self._pos[1]
        size = self._ascii.shape
        return [x0 + size[0] - 1, y0 + size[1] - 1]

    def get_ascii(self):
        return self._ascii