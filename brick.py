from typing import Any

import numpy as np
import numpy.typing as npt
from colorama import Back, Fore, Style

from sprite import Sprite


class Brick(Sprite):
    def __init__(self, x, y, strength=3):
        super().__init__(x, y)
        self._strength = strength
        self.repaint_brick()

    def reset_ascii(self, **kwargs) -> npt.NDArray[Any]:
        """
        Resets the ASCII representation of the sprite.
        Additional keyword arguments can be provided.
        """
        length = kwargs.get("length", 5)
        color = kwargs.get("color", Back.RED)
        self._ascii = np.array(
            [color + " "] * length,
            dtype="object",
        ).reshape(1, -1)

    def repaint_brick(self):
        if self._strength == "INFINITY":
            self.reset_ascii(color=Back.CYAN)
        elif self._strength == 3:
            self.reset_ascii(color=Back.RED)
        elif self._strength == 2:
            self.reset_ascii(color=Back.GREEN)
        elif self._strength == 1:
            self.reset_ascii(color=Back.MAGENTA)
        elif self._strength == 0:
            self.reset_ascii(color=Back.BLUE)

    def get_damage_points(self, ball=None):
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

