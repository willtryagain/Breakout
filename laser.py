import numpy as np
from colorama import Fore, Back, Style

from meta import Meta
from velocity import Velocity

class Laser(Meta):
    """
    implementing lasers
    """
    def __init__(self, game_height, game_width, pos, len):
        self._ascii = self.draw(len)
        self._velocity = Velocity(0, 0)
        super().__init__(game_height, game_width, pos, [1, len], self._ascii)

    def draw(self, len):
        return np.array(
            [Fore.WHITE + '*'] 
            + [' ']*len 
            + [Fore.WHITE + '*'],
            dtype='object'
        ).reshape(1, -1)
