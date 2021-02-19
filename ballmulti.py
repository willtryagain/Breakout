from powerup import Powerup
import numpy as np
from colorama import Fore, Back, Style

from ball import Ball

class Ballmulti(Powerup):
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)
        self._ascii = np.array(
            [Back.MAGENTA + '2', 
            Back.MAGENTA + 'x'], 
            dtype='object').reshape(1, -1)

    def apply(self, balls):
        split_balls = []
        for ball in balls:
            vx = 1
            vy = 1
            ball1 = Ball(self._gh, self._gw, ball._pos)
            ball1._velocity.setvx(vx)
            ball1._velocity.setvy(vy)
            ball1._alive = True

            ball2 = Ball(self._gh, self._gw, ball._pos)
            ball2._velocity.setvx(-vx)
            ball2._velocity.setvy(-vy)
            ball2._alive = True

            split_balls.extend((ball1, ball2))
   
        return split_balls
    def handle_collision(self, paddle, balls):
        l = paddle._pos[1]
        r = paddle._pos[1] + paddle._size[1] - 1
        if self._pos[0] == self._gh - 2:

            
            if l <= self._pos[1] and self._pos[1] + self._size[1] <= r:
                return self.apply(balls)