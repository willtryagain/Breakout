import numpy as np
from colorama import Fore, Back, Style

from meta import Meta

class Brick(Meta):

    def __init__(self, game_height, game_width, pos):
        self._ascii = np.array([
            Back.RED + ' ',
            Back.RED + ' ',
            Back.RED + ' ',
            Back.RED + ' ',
            Back.RED + ' ',
        ], dtype='object').reshape(1, -1)
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)