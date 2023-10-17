import numpy as np
from colorama import Back, Fore, Style

import settings
from powerup import Powerup


class Pgrab(Powerup):
    """
    Grab the paddle.
    """

    def __init__(self, pos, start_time):
        super().__init__(pos, start_time)
        self._ascii = np.array(
            [Back.BLUE + "P", Back.BLUE + "G"], dtype="object"
        ).reshape(1, -1)
        self._kind = "pgrab"

    def magic(self, paddle, ball):
        """
        grab the paddle
        """
        paddle._grab = True
        paddle._rel = ball.y - paddle.y
        return paddle

    def reverse(self, paddle):
        """
        deactivate the powerup
        """
        self._state = "DELETE"
        paddle._grab = False
        paddle._rel = 0
        return paddle
