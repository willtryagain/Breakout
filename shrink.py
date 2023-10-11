import numpy as np
from colorama import Fore, Back, Style

from powerup import Powerup
import settings

class Shrink(Powerup):
    """
    Shrinks the size of the paddle by a certain amount.
    """
    def __init__(self, pos, start_time):
        super().__init__(pos, start_time)
        self._ascii = np.array(
        [Back.MAGENTA + '>', 
        Back.MAGENTA + '<'], 
        dtype='object').reshape(1, -1)

    def magic(self, paddle):
        """
        shrink the paddle
        """
        paddle.update(-settings.EXPAND_VAL)
        return paddle

    def reverse(self, paddle):
        """
        deactivate the powerup
        """
        self._state = 'DELETE'
        paddle.update(settings.EXPAND_VAL)
        return paddle