import numpy as np
from colorama import Fore, Back, Style

from meta import Meta, Velocity, Position
import settings

class Paddle(Meta):
    def __init__(self, game_height, game_width, len=20):
        self._ascii = self.draw()
        self._velocity = Velocity(0, 0)
        self._grab = False
        self._rel = 0
        super().__init__(game_height, game_width, Position(game_height-1,\
            game_width//2 - self._ascii.shape[1]), [1, 22], self._ascii)

    def at_left_end(self):
        return self._pos.y <= 0
    
    def at_right_end(self):
        return self._pos.y + self._size[1] >= self._gw 


    def move(self, key):   
        if key == 'a':
            # move left
            self._pos = Velocity(
                self._pos.x, 
                self._pos.y - settings.PADDLE_SPEED
            )
            if self.at_left_end():
                # lower bound
                self._pos = Velocity(
                    self._pos.x, 
                    0
                )
        elif key == 'd':
            # move right
            self._pos = Velocity(
                self._pos.x, 
                self._pos.y + settings.PADDLE_SPEED
            )
            if self.at_right_end():
                # upper bound
                 self._pos = Velocity(
                    self._pos.x, 
                    self._gw - self._size[1]
                )

    def draw(self, len=20, color=Back.YELLOW):

        return np.array(
            [Fore.WHITE + '('] 
            + [color + ' ']*len 
            + [Fore.WHITE + ')'],
            dtype='object'
        ).reshape(1, -1)

    def update(self, value=0):
        len = max(self._size[1] - 2 + value, 1)
        self._ascii = self.draw(len)
        self._size[1] = len + 2

    def reset(self):
        self._ascii = self.draw()
        self._size[0], self._size[1] = self._ascii.shape
        self._pos = [self._gh-1, self._gw//2 - self._size[1]]
