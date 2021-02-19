import numpy as np
from colorama import Fore, Back, Style

from meta import Meta

class Brick(Meta):

    def __init__(self, game_height, game_width, pos, strength=3):

        self._ascii = np.array([
            Back.RED + ' ',
            Back.RED + ' ',
            Back.RED + ' ',
            Back.RED + ' ',
            Back.RED + ' ',
        ], dtype='object').reshape(1, -1)
        self._strength = strength
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)

    def decrease_strength(self, ball=None):
        if self._strength == 'INFINITY':
            if ball._thru:
                self._strength = 0
            return
        
        self._strength -= 1

        if self._strength == 2:
            self.draw(Back.GREEN)

        elif self._strength == 1:
            self.draw(Back.MAGENTA)

        elif self._strength == 0:
            self.draw(Back.BLUE)

    def draw(self, color, len=5):
        self._ascii = [color + ' '] * len