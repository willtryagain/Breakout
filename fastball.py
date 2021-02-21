from powerup import Powerup
import numpy as np
from colorama import Fore, Back, Style


class Fastball(Powerup):
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)
        self._ascii = np.array(
            [Back.BLUE + 'F', 
            Back.BLUE + 'B'], 
            dtype='object').reshape(1, -1)
        self._kind = 'fastball'

    def magic(self, balls):
        balls[0]._fast = True
        return balls

    def reverse(self, balls):
        balls[0]._fast = False
        return balls