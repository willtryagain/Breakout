from typing import Any

import numpy as np
import numpy.typing as npt
from colorama import Back, Fore, Style

from sprite import Sprite


class Brick(Sprite):
    def __init__(self, x, y, type="basic", length=5):
        super().__init__(x, y)
        self.length = length
        self.type = type
        self.type_color_dict = {
            "basic": Back.MAGENTA,
            "mid": Back.BLUE,
            "hard": Back.GREEN,
            "unbreakable": Back.RED,
        }
        self.reset_ascii(self.length)

    def reset_ascii(self, length: int) -> npt.NDArray[Any]:
        """
        Resets the ASCII representation of the sprite.
        Additional keyword arguments can be provided.
        """
        color = self.type_color_dict[self.type]
        self._ascii = np.array(
            [color + " "] * length,
            dtype="object",
        ).reshape(1, -1)

    def get_damage_points(self, ball=None):
        """ """
        if self.type == "unbreakable":
            if ball._thru:
                self.type = "hard"
                return 10
            else:
                return 0

        if self.type == "hard":
            self.type = "mid"
            return 3

        elif self.type == "mid":
            self.type = "basic"
            return 2

        elif self.type == "basic":
            self.type = "broken"
            return 1
        return 0
