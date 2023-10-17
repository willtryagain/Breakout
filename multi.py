import numpy as np
from colorama import Back, Fore, Style

from ball import Ball
from powerup import Powerup


class Multi(Powerup):
    def __init__(self, pos, start_time):
        super().__init__(pos, start_time)
        self._ascii = np.array(
            [Back.BLUE + "2", Back.BLUE + "x"], dtype="object"
        ).reshape(1, -1)
        self._kind = "multi"

    def magic(self, balls):
        split_balls = []
        for ball in balls:
            vx = -1
            vy = 1
            ball1 = Ball(ball.x, ball.y)
            ball1._velocity.vx = vx
            ball1._velocity.vy = vy
            ball._multi = False
            ball1._dead = False

            ball2 = Ball(ball.x, ball.y)
            ball2._velocity.vx = vx
            ball2._velocity.vy = -vy
            ball._dead = False
            split_balls.extend((ball1, ball2))

        return split_balls

    def reverse(self, balls):
        self._state = "DELETE"
        # for ball in balls:
        pass
