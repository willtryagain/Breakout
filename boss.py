import numpy as np
from colorama import Fore, Back, Style
from time import monotonic as clock, sleep

from velocity import Velocity 
from meta import Meta
import settings
from bomb import Bomb

class Boss(Meta):
    def __init__(self, game_height, game_width):
        self._ascii = np.array([
            [' ', ' ', ' ', ' ', Fore.WHITE + '.', Fore.WHITE + '-', Fore.WHITE + '-', Fore.WHITE + '-', Fore.WHITE + '.', ' ', ' ', ' '],
            [' ', ' ', Fore.WHITE + '_', Fore.WHITE + '/', Fore.WHITE + '_', Fore.WHITE + '_', Fore.WHITE + '~', Fore.WHITE + '0', Fore.WHITE + '_', Fore.WHITE + '\\', Fore.WHITE + '_', Fore.WHITE + ' '], 
            [' ', Fore.WHITE + '(', Fore.WHITE + '_', Fore.WHITE + '_', Fore.WHITE + '_', Fore.WHITE + '_', Fore.WHITE + '_', Fore.WHITE + '_', Fore.WHITE + '_', Fore.WHITE + '_', Fore.WHITE + '_', Fore.WHITE + ')']], dtype='object'
        )

        self._velocity = Velocity(0, 0)
        self.awake = False
        self._ltime = None
        self._bombs = []
        super().__init__(game_height, game_width, [0,0], self._ascii.shape, self._ascii)

    def at_left_end(self):
        return self._pos[1] <= 0
    
    def at_right_end(self):
        return self._pos[1] + self._size[1] >= self._gw 


    def move(self, key):   
        if key == 'a':
            # move left
            self._pos[1] -= settings.PADDLE_SPEED
            if self.at_left_end():
                # lower bound
                self._pos[1] = 0
        elif key == 'd':
            # move right
            self._pos[1] += settings.PADDLE_SPEED
            if self.at_right_end():
                # upper bound
                self._pos[1] = self._gw - self._size[1]

    def add_bomb(self):
        if self.awake and ((not self._ltime) or \
           (clock() - self._ltime >= settings.POWERUP_TIME)):
            pos = [(2*self._pos[0] + self._size[0] - 1)//2, self._pos[1] + self._size[1]]
            bomb = Bomb(self._gh, self._gw, pos)
            self._bombs.append(bomb)
            self._ltime = clock() 

    def remove_bombs(self):
        indices = []
        for index, bomb in enumerate(self._bombs):
            if bomb._pos[1] == self._gh - 1 - self._size[1]:
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            del self._bombs[index]
