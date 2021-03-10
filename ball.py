import numpy as np
from colorama import Fore, Back, Style

import settings
from meta import Meta
from velocity import Velocity
from powerup import Powerup
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
    
    def paddle_collide(self, paddle):
        """
        check if ball collided with the paddle 
        """
        left_paddle = paddle._pos[1]
        right_paddle = paddle._pos[1] + paddle._size[1] - 1
        height_paddle = paddle._pos[0]

        height_ball = self._pos[0]
        left_ball = self._pos[1]
        right_ball = self._pos[1] + self._size[1]

        # ball is just above paddle
        if height_ball == height_paddle - 1:
            if left_paddle <= left_ball and right_ball <= right_paddle:
                return True
    
        return False

    def paddle_collide_handle(self, paddle):
        if self._dead or paddle._grab:
            self._velocity.setvx(-1)
            self._velocity.setvy(1)

         # middle position of paddle
        mid = (2*paddle._pos[1] + paddle._size[1] - 1) // 2

        # in first half 
        if self._pos[1] < mid:
            # go left
            sign = -1
        else:
            # go right
            sign = 1
        vx = self._velocity.getvx()
        if vx > 0:
            raise ValueError('check vx')

        vy = self._velocity.getvy()

        # distance from the middle
        bias = abs(mid - self._pos[1]) // 2
        

        vy = sign * abs(Powerup.inc_mag(vy, bias))
        self._velocity.setvx(vx) 
        self._velocity.setvy(vy)

    def side_walls_collide(self):
        """
        check if ball collided with the side walls 
        """
        left_ball = self._pos[1]
        right_ball = self._pos[1] + self._size[1] - 1

        left_wall = 0
        right_wall = self._gw - 1

        # hits the side walls
        if left_ball == left_wall or right_wall == right_ball:
            return True
        
        return False


    def top_collide(self):
        """
        check if ball collided with the top wall
        """
        top_ball = self._pos[0]
        top_wall = 0

        if top_ball == top_wall:
            return True

        return False

    
    def brick_horizontal_collide(self, bricks):
        """
            handle collision with brick 
            atmost one at a time
            Above brick
               O
               V
            [|||||]

            Below brick
            [|||||]
               ^
               o

        """
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
                if bottom_ball == top_brick:
                    return index
                # below
                elif top_ball == bottom_brick:
                    return index
           
        return -1   

    def brick_vertical_collide(self, bricks):
        """
            handle collision with brick 
            atmost one at a time
            Left of brick
        
            o   [|||||]

            Right of brick
                [|||||]    o
        """

        top_ball = self._pos[0]
        bottom_ball = self._pos[0] + self._size[0]

        left_ball = self._pos[1]
        right_ball = self._pos[1] + self._size[1]

        for index, brick in enumerate(bricks):
            left_brick = brick._pos[1]
            right_brick = left_brick + brick._size[1]

            top_brick = brick._pos[0]
            bottom_brick = top_brick + brick._size[0] 
      
            in_between = (top_brick <= top_ball and bottom_ball <= bottom_brick)

            if in_between:
                # left
                if right_ball == left_brick:
                    return index
                # right
                elif left_ball == right_brick:
                    return index
           
        return -1   

     def brick_corners_collide(self, bricks):
        top_ball = self._pos[0]
        bottom_ball = self._pos[0] + self._size[0]

        left_ball = self._pos[1]
        right_ball = self._pos[1] + self._size[1]

        for index, brick in enumerate(self._bricks):
            left_brick = brick._pos[1]
            right_brick = left_brick + brick._size[1]

            top_brick = brick._pos[0]
            bottom_brick = top_brick + brick._size[0]
      
            if bottom_ball == top_brick:
                if (left_ball <= left_brick and left_brick <= right_ball) \
                    or (left_ball <= right_brick and right_brick <= right_ball):
                    return index
            
            if top_ball == bottom_brick:
                if (left_ball <= left_brick and left_brick <= right_ball) \
                    or (left_ball <= right_brick and right_brick <= right_ball):
                    return index
           
        return -1   
