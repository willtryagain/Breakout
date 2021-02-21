import numpy as np
from colorama import Fore, Back, Style

from powerup import Powerup
import settings

class Pgrab(Powerup):
    """
    Grab the paddle.
    """
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)
        self._ascii = np.array(
        [Back.BLUE + 'P', 
        Back.BLUE + 'G'], 
        dtype='object').reshape(1, -1)
        self._kind = 'pgrab'

    def magic(self, paddle, ball):
        """
        grab the paddle
        """
        paddle._grab = True
        paddle._rel = ball._pos[1] - paddle._pos[1] 
        return paddle

    def reverse(self, paddle):
        """
        deactivate the powerup
        """
        paddle._grab = False
        paddle._rel = 0
        return paddle