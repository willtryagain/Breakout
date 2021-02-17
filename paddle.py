import numpy as np
from colorama import Fore, Back, Style

from velocity import Velocity 
from meta import Meta

class Paddle(Meta):
    def __init__(self, game_height, game_width, len=20):
        ascii = [Fore.WHITE + '('] + [Back.YELLOW + ' ']*len + [Fore.WHITE + ')']
        self._ascii = np.array(
            ascii,
            dtype='object'
        ).reshape(1, -1)
        self._velocity = Velocity(0, 0, 0, 0)
        super().__init__(game_height, game_width, [game_height-1,\
            game_width//2 - self._ascii.shape[1]], self._ascii.shape, self._ascii)


    def at_left_end(self):
        return self._pos[1] <= 0
    
    def at_right_end(self):
        return self._pos[1] + self._size[1] >= self._gw 

    def move(self, key, ball=None):   
        if key == 'a':
            self._pos[1] -= 3
            if self.at_left_end():
                self._pos[1] = 0
        elif key == 'd':
            self._pos[1] += 3
            if self.at_right_end():
                self._pos[1] = self._gw - self._size[1]
        else:
            raise KeyError('paddle')
       
        if ball is not None:
            ball._pos[1] = (2*self._pos[1] + self._size[1]) // 2

