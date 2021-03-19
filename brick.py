import numpy as np
from colorama import Fore, Back, Style
import random

from meta import Meta
from velocity import Velocity

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
        self._rainbow = False
        self._velocity = Velocity()
        self._shield = False
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)

    def repaint(self):
        if self._rainbow:
            self._strength = random.choice([1, 2, 3])

        if self._strength == 'INFINITY':
           self.draw(Back.CYAN) 
        elif self._strength == 3:
           self.draw(Back.RED) 
        elif self._strength == 2:
           self.draw(Back.GREEN)    
        elif self._strength == 1:
            self.draw(Back.MAGENTA)
        elif self._strength == 0:
            self.draw(Back.BLUE)

    def get_damage_points(self, ball=None):
        """

        """
        if self._strength == 'INFINITY':
            if ball._thru:
                self._strength = 3
                return 10
            else:
                return 0
        
        self._strength -= 1

        if self._strength == 2:
            return 3

        elif self._strength == 1:
            return 2

        elif self._strength == 0:
            return 1
        return 0

    def draw(self, color, len=5):
        self._ascii = [color + ' '] * len

    def move(self):
        self._pos[0] += 1
        self._pos[0] = min(self._pos[0], self._gh - self._size[0])