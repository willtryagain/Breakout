from typing import Any

import numpy as np
import numpy.typing as npt
from colorama import Back, Fore, Style

import settings
from sprite import Sprite
from velocity import Velocity


class Paddle(Sprite):
    def __init__(self, game_height, game_width):
        self.reset_ascii()
        super().__init__(
            game_height - 1,
            game_width // 2 - self._ascii.shape[1],
        )
        self._velocity = Velocity(0, 0)
        self._grab = False
        self._rel = 0

    def at_left_end(self):
        return self.y <= 0

    def at_right_end(self, game_width):
        return self.y + self.width >= game_width

    def move(self, key, game_width):
        if key == "a":
            # move left
            self.y -= settings.PADDLE_SPEED
            if self.at_left_end():
                # lower bound
                self.y = 0
        elif key == "d":
            # move right
            self.y += settings.PADDLE_SPEED
            if self.at_right_end(game_width):
                # upper bound
                self.y = game_width - self.width

    def update(self, value=0):
        self.reset_ascii(length=max(self.width - 2 + value, 1))

    def reset_ascii(self, **kwargs) -> npt.NDArray[Any]:
        """
        Resets the ASCII representation of the sprite.
        Additional keyword arguments can be provided.
        """
        length = kwargs.get("length", 20)
        color = kwargs.get("color", Back.YELLOW)

        self._ascii = np.array(
            [Fore.WHITE + "("] + [color + " "] * length + [Fore.WHITE + ")"],
            dtype="object",
        ).reshape(1, -1)
