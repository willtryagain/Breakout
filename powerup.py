import numpy as np
from colorama import Fore, Back, Style

from meta import Meta
from velocity import Velocity
import settings

class Powerup(Meta):
    """
    Powerup has four states
    i. HIDE: Hidden inside the brick
    ii. FALL: The brick has been destroyed. Powerup falls down
    iii. ACTIVE: The powerup has been activated
    iv. DESTROY: The powerup has been used/dropped
    """
    def __init__(self, game_height, game_width,  pos, start_time):
        self._state = 'HIDE'
        self._ascii = np.array(
            [Back.MAGENTA + '<', 
            Back.MAGENTA + '>'], 
            dtype='object').reshape(1, -1)
        self._start_time = start_time
       
        self._velocity = Velocity(vx = settings.POWERUP_SPEED)
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)

    def move(self, paddle=None):

        vx = self._velocity.getvx()
        if self._pos[0] + vx <= self._gh - 1:
            self._pos[0] +=  vx
        else:
            # the powerup fell down
            # it can't be used anymore
            self._state = 'DESTROY'
 
    
    def collision(self, paddle):
        """
        return true if collision 
        has taken place with the paddle
        """
        l = paddle._pos[1]
        r = paddle._pos[1] + paddle._size[1] - 1
        if self._pos[0] == self._gh - 2:
            if l <= self._pos[1] and self._pos[1] + self._size[1] <= r:
                self._state = 'ACTIVE'
                return True

        return False