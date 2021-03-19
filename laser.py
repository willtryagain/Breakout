import numpy as np
from colorama import Fore, Back, Style

from ball import Ball
from velocity import Velocity

class Laser(Ball):
    """
    implementing lasers
    """
    def __init__(self, game_height, game_width, pos, len):
        super().__init__(game_height, game_width, pos)
        self._ascii = self.draw(len)
        self._size = [1, len]
        self._velocity = Velocity(-2, 0)

    def draw(self, len):
        return np.array(
            [Fore.WHITE + '*'] 
            + [' ']*(len - 2)
            + [Fore.WHITE + '*'],
            dtype='object'
        ).reshape(1, -1)

    def move(self):
        # increment by the velocities
        self._pos[0] += self._velocity.vx
        
        # non-negative
        self._pos[0] = max(self._pos[0], 0)

    def brick_collide(self, bricks):

        top_ball = self._pos[0]
        bottom_ball = self._pos[0] + self._size[0]

        left_ball = self._pos[1]
        right_ball = self._pos[1] + self._size[1]

        for index, brick in enumerate(bricks):
            left_brick = brick._pos[1]
            right_brick = left_brick + brick._size[1]

            top_brick = brick._pos[0]
            bottom_brick = top_brick + brick._size[0]

            in_between = (left_brick <= left_ball and right_ball <= right_brick)

            if in_between:
                # above
                if bottom_ball == top_brick or \
                    bottom_ball == top_brick + 1:
                    return index
                # below
                elif top_ball == bottom_brick or \
                    top_ball == bottom_brick - 1:
                    return index
           
        return -1   