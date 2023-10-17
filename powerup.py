from time import monotonic as clock
from time import sleep

import numpy as np
from colorama import Back, Fore, Style

<<<<<<< HEAD
=======
from meta import Meta, Velocity
>>>>>>> 92b80f26c4c2d56b8544f5f4ef6c990dd93d62ae
import settings
from sprite import Sprite
from velocity import Velocity


class Powerup(Sprite):
    """
    Powerup has four states
    i. HIDE: Hidden inside the brick
    ii. FALL: The brick has been destroyed. Powerup falls down
    iii. ACTIVE: The powerup has been activated
    iv. DESTROY: The powerup has been used/dropped
    """

    def __init__(self, pos, start_time):
        self._state = "HIDE"
        self._ascii = np.array(
            [Back.MAGENTA + "<", Back.MAGENTA + ">"], dtype="object"
        ).reshape(1, -1)
        self._start_time = start_time
        self._kind = ""

        self._velocity = Velocity(vx=settings.POWERUP_SPEED)
        super().__init__(pos, self._ascii.shape, self._ascii)

<<<<<<< HEAD
    def move(
        self,
        game_height,
        paddle=None,
    ):
        vx = self._velocity.vx
        if self.x + vx <= game_height - 1:
            self.x += vx
=======
        vx = self._velocity.x
        if self._pos.x + vx <= self._gh - 1:
            self._pos.x +=  vx
>>>>>>> 92b80f26c4c2d56b8544f5f4ef6c990dd93d62ae
        else:
            # the powerup fell down
            # it can't be used anymore
            self._state = "DELETE"

    def collision(self, paddle):
        """
        return true if collision
        has taken place with the paddle
        """
<<<<<<< HEAD
        left_paddle = paddle.y
        right_paddle = paddle.y + paddle.width - 1
        top_paddle = paddle.x

        left_powerup = self.y
        right_powerup = self.y + self.width - 1
        bottom_powerup = self.x + self.height - 1
=======
        left_paddle = paddle._pos.y
        right_paddle = paddle._pos.y + paddle._size[1] - 1
        top_paddle = paddle._pos.x

        left_powerup = self._pos.y
        right_powerup = self._pos.y + self._size[1] - 1
        bottom_powerup = self._pos.x + self._size[0] - 1
>>>>>>> 92b80f26c4c2d56b8544f5f4ef6c990dd93d62ae
        if bottom_powerup == top_paddle - 1:
            if left_paddle <= left_powerup and right_powerup <= right_paddle:
                self._state = "ACTIVE"
                self._start_time = clock()
                return True

        return False

    def time_up(self):
        if clock() - self._start_time >= settings.POWERUP_TIME:
            self._state == "DELETE"
            return True

        return False

    def inc_mag(self, x, bias=2):
        if x == 0:
            return x
        sign = x // abs(x)
        mag = abs(x) + bias
        mag = min(mag, settings.MAX_SPEED)
        return sign * mag
