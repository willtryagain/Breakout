import numpy as np
from colorama import Back, Fore, Style

from powerup import Powerup


class Fastball(Powerup):
    def __init__(self, pos, start_time):
        super().__init__(pos, start_time)
        self._ascii = np.array(
            [Back.BLUE + "F", Back.BLUE + "B"], dtype="object"
        ).reshape(1, -1)
        self._kind = "fastball"

    def magic(self, balls):
        balls[0]._fast = True
        return balls

    def reverse(self, balls):
        self._state = "DELETE"
        balls[0]._fast = False
        return balls
