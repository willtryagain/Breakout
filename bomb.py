import numpy as np
from colorama import Fore, Back, Style
from time import monotonic as clock, sleep

from meta import Meta
from velocity import Velocity
import settings

class Bomb(Meta):
    """
    """
    def __init__(self, game_height, game_width, pos):
        self._ascii = np.array(
            [Back.MAGENTA + Fore.WHITE +  'X'], 
            dtype='object').reshape(1, -1)
       
        self._velocity = Velocity(vx = settings.POWERUP_SPEED)
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)

    def move(self, paddle=None):

        vx = self._velocity.getvx()
        if self._pos[0] + vx <= self._gh - 1:
            # increment by the velocities
            self._pos[0] += self._velocity.getvx()
            self._pos[1] += self._velocity.getvy()
            
            # non-negative
            self._pos[0] = max(self._pos[0], 0)
            self._pos[1] = max(self._pos[1], 0)
            
            # upper bound
            self._pos[0] = min(self._pos[0], self._gh - self._size[0])
            self._pos[1] = min(self._pos[1], self._gw - self._size[1])

    def paddle_collision(self, paddle):
        """
        return true if collision 
        has taken place with the paddle
        """
        left_paddle = paddle._pos[1]
        right_paddle = paddle._pos[1] + paddle._size[1] - 1
        top_paddle = paddle._pos[0]

        left_powerup = self._pos[1]
        right_powerup = self._pos[1] + self._size[1] - 1
        bottom_powerup = self._pos[0] + self._size[0] - 1
        if bottom_powerup == top_paddle - 1:
            if left_paddle <= left_powerup and right_powerup <= right_paddle:
                return True

        return False

    