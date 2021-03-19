import numpy as np
from colorama import Fore, Back, Style
from time import monotonic as clock, sleep

from velocity import Velocity 
from meta import Meta
import settings
from bomb import Bomb
from brick import Brick

class Boss(Meta):
    def __init__(self, game_height, game_width, paddle):
        self._ascii = np.array([
            [' ', ' ', ' ', ' ', Fore.BLUE + '.', Fore.BLUE + '-', Fore.BLUE + '-', Fore.BLUE + '-', Fore.BLUE + '.', ' ', ' ', ' '],
            [' ', ' ', Fore.BLUE + '_', Fore.BLUE + '/', Fore.BLUE + '_', Fore.BLUE + '_',Style.BRIGHT + Fore.GREEN + '~', Style.BRIGHT + Fore.GREEN + '0', Fore.BLUE + '_', Fore.BLUE + '\\', Fore.BLUE + '_', ' '], 
            [' ',  Fore.BLUE + '(', Fore.BLUE +  '_',  Fore.BLUE + '_', Fore.BLUE + '_', Fore.BLUE + '_', Fore.BLUE + '_', Fore.BLUE + '_', Fore.BLUE + '_', Fore.BLUE + '_', Fore.BLUE + '_', Fore.BLUE + ')' + Style.RESET_ALL]], dtype='object'
        )

        self._velocity = Velocity(0, 0)
        self.awake = False
        self._ltime = None
        self._shield_count = 2
        self._bombs = []
        self._health = settings.BOSS_HEALTH
        pos = [0, (2*paddle._pos[0] + paddle._size[0])//2]
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)

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
        if (not self._ltime) or (clock() - self._ltime >= 5):
            pos = [self._pos[0] + self._size[0], (2*self._pos[1] + self._size[1])//2]
            bomb = Bomb(self._gh, self._gw, pos)
            self._bombs.append(bomb)
            self._ltime = clock() 

    def remove_bombs(self):
        indices = []
        for index, bomb in enumerate(self._bombs):
            if bomb.lost():
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            del self._bombs[index]

    def get_brick_layer(self):
        bricks = []
        x = self._pos[0] + self._size[0] + 2
        y = 0
        while y + 5 <= self._gw - settings.RIGHT_MARGIN:
            brick = Brick(self._gh, self._gw, [x, y], 1)
            brick.repaint()
            brick._shield = True
            y += brick._size[1]
            bricks.append(brick)
        return bricks

    def add_shield(self, bricks):
        if self._health <= 0.25 * settings.BOSS_HEALTH:
            if self._shield_count:
                for brick in bricks:
                    if brick._shield:
                        return
                self._shield_count -= 1
                bricks.extend(self.get_brick_layer()) 