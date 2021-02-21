import numpy as np
from colorama import Fore, Back, Style

import settings
from meta import Meta
from velocity import Velocity

class Ball(Meta):
    def __init__(self, game_height, game_width, pos):
        self._ascii = self.draw()
        self._dead = True
        self._thru = False
        self._fast = False
        self._velocity = Velocity(0, 0) # composition
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)


    def go_fast(self):
        vx = self._velocity.getvx()
        vy = self._velocity.getvy()
        if vx > 0:
            vx = settings.MAX_SPEED
        else:
            vx = -settings.MAX_SPEED
        if vy > 0:
            vy = settings.MAX_SPEED
        else:
            vy = -settings.MAX_SPEED
        self._velocity.setvx(vx)
        self._velocity.setvy(vy)


    def move(self, key=None):
        if key is not None:
            if key == 'w':
                self._pos[1] += 1
            elif key == 's':
                self._pos[1] -= 1
            return



        # increment by the velocities
        self._pos[0] += self._velocity.vx
        self._pos[1] += self._velocity.vy
        
        # non-negative
        self._pos[0] = max(self._pos[0], 0)
        self._pos[1] = max(self._pos[1], 0)
        
        # upper bound
        self._pos[0] = min(self._pos[0], self._gh - self._size[0])
        self._pos[1] = min(self._pos[1], self._gw - self._size[1])

    def draw(self, color=Fore.RED):
        return np.array([
            Style.BRIGHT + Fore.RED + '(', 
            Style.BRIGHT + Fore.RED + ')'],
            dtype='object'
        ).reshape(1, -1)


    def reverse_vy(self):
        vy = self._velocity.getvy()
        self._velocity.setvy(-vy)

    def set_posy(self, pos):
        self._pos[1] = pos

    def reverse_vx(self):
        vx = self._velocity.getvx()
        self._velocity.setvx(-vx)

    def intersects(self, bricks):
        left_ball = self._pos[1]
        right_ball = self._pos[1] + self._size[1] - 1
        top_ball = self._pos[0]

        for brick in bricks:
            left_brick = brick._pos[1]
            right_brick = brick._pos[1] + brick._size[1] - 1
            top_brick = brick._pos[0]

            if top_brick == top_ball:
                if left_brick <= right_ball and right_ball <= right_brick:
                    return True

        return False

    def left(self):
        self._pos[1] -= 1
    
    def right(self):
        self._pos[1] += 1

    def down(self):
        self._pos[0] += 1

    def up(self):
        self._pos[0] -= 1
    