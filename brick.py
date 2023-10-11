import numpy as np
from colorama import Back, Fore, Style
from sprite import Sprite


class Brick(Sprite):
    def __init__(self, pos, strength=3):
        self._ascii = np.array(
            [
                Back.RED + " ",
                Back.RED + " ",
                Back.RED + " ",
                Back.RED + " ",
                Back.RED + " ",
            ],
            dtype="object",
        ).reshape(1, -1)
        self._strength = strength
        super().__init__(pos, self._ascii.shape, self._ascii)

    def repaint_brick(self):
        if self._strength == "INFINITY":
            self.draw(Back.CYAN)
        elif self._strength == 3:
            self.draw(Back.RED)
        elif self._strength == 2:
            self.draw(Back.GREEN)
        elif self._strength == 1:
            self.draw(Back.MAGENTA)
        elif self._strength == 0:
            self.draw(Back.BLUE)

    def get_damage_points(self, player, ball=None):
        """ """
        if self._strength == "INFINITY":
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
        self._ascii = [color + " "] * len
