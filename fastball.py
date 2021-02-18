from powerup import Powerup
import numpy as np
from colorama import Fore, Back, Style

def inc_mag(x, bias=5):
    sign = x // abs(x)
    mag = abs(x)
    return sign * (mag + bias)

class Fastball(Powerup):
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)
        self._ascii = np.array(
            [Back.MAGENTA + '(', 
            Back.MAGENTA + ')'], 
            dtype='object').reshape(1, -1)

    def handle_collision(self, paddle, ball):
        l = paddle._pos[1]
        r = paddle._pos[1] + paddle._size[1] - 1
        if self._pos[0] == self._gh - 2:
            if l <= self._pos[1] and self._pos[1] + self._size[1] <= r:
                self._state = 'IN_USE'
                self.apply(ball)

    def apply(self, ball):
        vx = ball._velocity.getvx()
        vy = ball._velocity.getvy()

        vx = inc_mag(vx)
        vy = inc_mag(vy)

        ball._velocity.setvx(vx)
        ball._velocity.setvy(vy)
