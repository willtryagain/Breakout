import numpy as np
from colorama import Fore, Back, Style

from ball import Ball
from velocity import Velocity

class Laser(Ball):
    """
    implementing lasers
    """
    def __init__(self, game_height, game_width, pos, len):
        super().__init__(game_height, game_width, pos)
        self._ascii = self.draw(len)
        self._size = [1, len]
        self._velocity = Velocity(-2, 0)

    def draw(self, len):
        return np.array(
            [Fore.WHITE + '*'] 
            + [' ']*(len - 2)
            + [Fore.WHITE + '*'],
            dtype='object'
        ).reshape(1, -1)

    def move(self):
        # increment by the velocities
        self._pos[0] += self._velocity.vx
        
        # non-negative
        self._pos[0] = max(self._pos[0], 0)