from powerup import Powerup
import numpy as np
from colorama import Fore, Back, Style

from ball import Ball

class Multi(Powerup):
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)
        self._ascii = np.array(
            [Back.BLUE + '2', 
            Back.BLUE + 'x'], 
            dtype='object').reshape(1, -1)
        self._kind = 'multi'

        
    def magic(self, balls):
        split_balls = []
        for ball in balls:
            vx = 1
            vy = 1
            ball1 = Ball(self._gh, self._gw, ball._pos)
            ball1._velocity.setvx(vx)
            ball1._velocity.setvy(vy)
            ball._multi = False
            ball1._alive = True

            ball2 = Ball(self._gh, self._gw, ball._pos)
            ball2._velocity.setvx(-vx)
            ball2._velocity.setvy(-vy)
            ball2._alive = True
            ball._multi = True
            split_balls.extend((ball1, ball2))
   
        return split_balls

    def reverse(self, balls):
        # for ball in balls:
        pass
