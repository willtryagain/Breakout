from colorama import Fore, Back, Style
import numpy as np

from powerup import Powerup
import settings

class Gunpaddle(Powerup):
    """
    The paddle will now shoot bullets.
    """
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)
        self._ascii = np.array(
        [Back.MAGENTA + 'G', 
        Back.MAGENTA + 'P'], 
        dtype='object').reshape(1, -1)
        self._kind = 'gunpaddle'

    def magic(self, paddle):
        """
        change the paddle
        """
        paddle._ascii = paddle.draw(len=paddle._size[1]-2, start='^', stop='^')
        paddle._gun = True

        return paddle

    def reverse(self, paddle):
        """
        deactivate the powerup
        """
        paddle._ascii = paddle.draw(len=paddle._size[1]-2)
        paddle._gun = False
        self._state = 'DELETE'
        # paddle.update(-settings.EXPAND_VAL)
        return paddle