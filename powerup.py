import numpy as np
from colorama import Fore, Back, Style

from meta import Meta
from velocity import Velocity

class Powerup(Meta):
    def __init__(self, game_height, game_width,  pos, start_time=0):
        self._active = False
        self._ascii = np.array(
            [Back.MAGENTA + '<', 
            Back.MAGENTA + '>'], 
            dtype='object').reshape(1, -1)
        self._start_time = start_time
        self._velocity = Velocity(2)
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)

    def move(self):
        vx = self._velocity.getvx()
        if self._pos[0] + self._size[0] - 1 + vx  <= self._gh - 1:
            self._pos[0] +=  vx
    