from typing import Any

import numpy as np
import numpy.typing as npt
from colorama import Back, Fore, Style

import settings
from sprite import Sprite
from velocity import Velocity


class Ball(Sprite):
    def __init__(self, screen_height, paddle_y, paddle_width):
        super().__init__(screen_height - 2, (2 * paddle_y + paddle_width) // 2)
        self.reset_ascii()
        self._dead = True
        self._thru = False
        self._fast = False
        self._velocity = Velocity(0, 0)

    def reset_ascii(self, **kwargs) -> np.ndarray:
        """
        Resets the ASCII representation of the sprite.
        Additional keyword arguments can be provided.
        """
        self._ascii = np.array(
            [Style.BRIGHT + Fore.RED + "(", Style.BRIGHT + Fore.RED + ")"],
            dtype="object",
        ).reshape(1, -1)

    def go_fast(self):
        self._velocity.vx = (
            settings.MAX_SPEED if self._velocity.vx > 0 else -settings.MAX_SPEED
        )
        self._velocity.vy = (
            settings.MAX_SPEED if self._velocity.vy > 0 else -settings.MAX_SPEED
        )

    def move(self, screen_height: int, screen_width: int, key: str = None):
        if key is not None:
            if key == settings.MOVE_RIGHT_KEY:
                self.move_right()
            elif key == settings.MOVE_LEFT_KEY:
                self.move_left()
            return

        super().move(self._velocity.vx, self._velocity.vy)
        self.x = max(0, min(self.x, screen_height - self.height))
        self.y = max(0, min(self.y, screen_width - self.width))

    def reverse_vy(self):
        self._velocity.vy = -self._velocity.vy

    def reverse_vx(self):
        self._velocity.vx = -self._velocity.vx

    def set_vx(self, vx: int):
        self._velocity.vx = vx

    def set_vy(self, vy: int):
        self._velocity.vy = vy

    def intersects(self, bricks) -> bool:
        right_ball = self.y + self.width - 1
        top_ball = self.x

        for brick in bricks:
            left_brick = brick.y
            right_brick = brick.y + brick.width - 1
            top_brick = brick.x

            if top_brick == top_ball and left_brick <= right_ball <= right_brick:
                return True

        return False
