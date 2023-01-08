"""
Defines the Ball class
"""

import numpy as np
from colorama import Fore, Style

import settings
from meta import Meta, Velocity, Position

class Ball(Meta):
    """
    Defines the ball. Handles its motion on the screen.
    """
    def __init__(self, game_height, game_width, pos):
        self._ascii = self.draw()
        self._dead = True
        self._thru = False
        self._fast = False
        self._velocity = Velocity(0, 0) # composition
        super().__init__(game_height, game_width, pos, self._ascii.shape, self._ascii)


    def go_fast(self):
        """increases the speed of ball"""
        # TODO: refactor 
        v_x = self._velocity.x
        v_y = self._velocity.y
        if v_x > 0:
            v_x = settings.MAX_SPEED
        else:
            v_x = -settings.MAX_SPEED
        if v_y > 0:
            v_y = settings.MAX_SPEED
        else:
            v_y = -settings.MAX_SPEED
        self._velocity = Velocity(v_x, v_y)


    def move(self, key=None):
        """updates the position of ball based on velocity"""

        pos_x = self._pos.x
        pos_y = self._pos.y

        if key is not None:
            if key == 'w':
                pos_y += 1
            elif key == 's':
                pos_y -= 1
            return

        # increment by the velocities
        
        pos_x += self._velocity.x
        pos_y += self._velocity.y
        
        # non-negative
        pos_x = max(pos_x, 0)
        pos_y = max(pos_y, 0)
        
        # upper bound
        pos_x = min(pos_x, self._gh - self._size[0])
        pos_y = min(pos_y, self._gw - self._size[1])

        self._pos = Position(pos_x, pos_y)

        

    def draw(self):
        """Returns the ascii representation"""
        return np.array([
            Style.BRIGHT + Fore.RED + '(',
            Style.BRIGHT + Fore.RED + ')'],
            dtype='object'
        ).reshape(1, -1)


    def reverse_vy(self):
        """reverses velocity of ball along Y axis"""
        self._velocity.y = -self._velocity.y

    def reverse_vx(self):
        """reverses velocity of ball along X axis"""
        self._velocity.x = -self._velocity.x

    def set_posy(self, pos_y):
        """Set y coordinate of the object"""
        self._pos = Position(self._pos.x, pos_y) 

    def intersects(self, bricks):
        """
        returns true if the ball's representation is intersecting with
        the bricks
        """
        right_ball = self._pos.y + self._size[1] - 1
        top_ball = self._pos.x

        for brick in bricks:
            brick_pos = brick.get_pos()
            brick_size = brick.get_size()

            left_brick,  = brick_pos.y
            right_brick = brick_pos.y + brick_size[1] - 1
            top_brick = brick_pos.x

            if top_brick == top_ball:
                if left_brick <= right_ball and right_ball <= right_brick:
                    return True

        return False


    # ? move this to meta?

    def left(self):
        """ball moves left"""
        self._pos = Position(self._pos.x, self._pos.y - 1)

    def right(self):
        """ball moves right"""
        self._pos = Position(self._pos.x, self._pos.y + 1)

    def down(self):
        """ball moves down"""
        self._pos = Position(self._pos.x + 1, self._pos.y)

    def up(self):
        """ball moves up"""
        self._pos = Position(self._pos.x - 1, self._pos.y)

    