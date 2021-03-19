import numpy as np
from colorama import Fore, Back, Style
from time import monotonic as clock, sleep

from meta import Meta
from velocity import Velocity
import settings

class Powerup(Meta):
    """
    Powerup has three states
    i. HIDE: Hidden inside the brick
    ii. FALL: The brick has been destroyed. Powerup falls down
    iii. ACTIVE: The powerup has been activated
    iv. DESTROY: The powerup has been used/dropped
    """
    def __init__(self, game_height, game_width,  pos, start_time):
        self._state = 'HIDE'
        self._ascii = np.array(
            [Back.MAGENTA + Fore.WHITE +  '<', 
            Back.MAGENTA + '>'], 
            dtype='object').reshape(1, -1)
        self._start_time = start_time
        self._kind = ''
       
        self._velocity = Velocity(gravity=settings.GRAVITY)
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)

    def move(self, paddle=None):

        vx = self._velocity.getvx()
       
        self._velocity.setvx(vx + self._velocity.gravity)

        # increment by the velocities
        self._pos[0] += self._velocity.getvx()
        self._pos[1] += self._velocity.getvy()
        
        # non-negative
        self._pos[0] = max(self._pos[0], 0)
        self._pos[1] = max(self._pos[1], 0)
        
        # upper bound
        self._pos[0] = min(self._pos[0], self._gh - self._size[0])
        self._pos[1] = min(self._pos[1], self._gw - self._size[1])
      
        
    def trivial_collision(self):
        if self.side_walls_collide():
            self._velocity.reversevy()
            return True

        if self.top_collide():
            self._velocity.reversevx()
            return True
        return False

    def paddle_collision(self, paddle):
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
        if bottom_powerup == top_paddle or \
            bottom_powerup == top_paddle + 1:
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

    def inc_mag(self, x, bias=2):
        if x == 0:
            return x
        sign = x // abs(x)
        mag = abs(x)+ bias
        mag = min(mag, settings.MAX_SPEED)
        return sign * mag 

        