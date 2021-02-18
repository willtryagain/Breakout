import numpy as np
from colorama import Fore, Back, Style

from velocity import Velocity 
from meta import Meta

class Paddle(Meta):
    def __init__(self, game_height, game_width, len=20):
        self._ascii = self.draw()
        self._velocity = Velocity(0, 0, 0, 0)
        self
        super().__init__(game_height, game_width, [game_height-1,\
            game_width//2 - self._ascii.shape[1]], [1, 22], self._ascii)


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

    def draw(self, len=20):

        return np.array(
            [Fore.WHITE + '('] 
            + [Back.YELLOW + ' ']*len 
            + [Fore.WHITE + ')'],
            dtype='object'
        ).reshape(1, -1)

    def update(self, value=0, reset=False):
        
        len = self._size[1] - 2 + value
        if reset:
            len = 20
        self._ascii = self.draw(len)
        self._size[1] = len + 2
