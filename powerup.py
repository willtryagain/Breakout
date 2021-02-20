import numpy as np
from colorama import Fore, Back, Style
from time import monotonic as clock, sleep

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
        left_paddle = paddle._pos[1]
        right_paddle = paddle._pos[1] + paddle._size[1] - 1
        top_paddle = paddle._pos[0]

        left_powerup = self._pos[1]
        right_powerup = self._pos[1] + self._size[1] - 1
        bottom_powerup = self._pos[0] + self._size[0] - 1
        if bottom_powerup == top_paddle - 1:
            if left_paddle <= left_powerup and right_powerup <= right_paddle:
                self._state = 'ACTIVE'
                self._start_time = clock()
                return True

        return False

    def time_up(self):
        if clock() - self._start_time >= settings.POWERUP_TIME:
            self._state == 'DELETE' 
            return True
        
        return False