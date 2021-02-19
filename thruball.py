from powerup import Powerup
import numpy as np
from colorama import Fore, Back, Style

class Thruball(Powerup):
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)
        self._ascii = np.array(
            [Back.MAGENTA + 'T', 
            Back.MAGENTA + 'B'], 
            dtype='object').reshape(1, -1) 

    def apply(self, ball):
        ball._thru = True
        

    def handle_collision(self, paddle, ball):
        l = paddle._pos[1]
        r = paddle._pos[1] + paddle._size[1] - 1
        if self._pos[0] == self._gh - 2:
            if l <= self._pos[1] and self._pos[1] + self._size[1] <= r:
                self.apply(ball)