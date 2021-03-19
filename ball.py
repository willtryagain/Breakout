import numpy as np
from colorama import Fore, Back, Style

import settings
from meta import Meta
from velocity import Velocity
from powerup import Powerup


class Ball(Meta):
    def __init__(self, game_height, game_width, pos):
        self._ascii = np.array([
            Style.BRIGHT + Fore.RED + '(', 
            Style.BRIGHT + Fore.RED + ')'],
            dtype='object'
        ).reshape(1, -1)

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
        # if vy > 0:
        #     vy = settings.MAX_SPEED
        # else:
        #     vy = -settings.MAX_SPEED
        self._velocity.setvx(vx)
        self._velocity.setvy(vy)


    def move(self, key=None):
        if key is not None:
            if key == 'w':
                self._pos[1] += 1
            elif key == 's':
                self._pos[1] -= 1
            return

        # increment the pos
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



    def set_posy(self, pos):
        self._pos[1] = pos


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
        if height_ball == height_paddle - 1 or \
            height_ball == height_paddle:
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

        for index, brick in enumerate(bricks):
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

   

    def brick_intersection(self, bricks):
        vx = self._velocity.getvx()
        vy = self._velocity.getvy()
        while self.intersects(bricks):
            if vx < 0: 
                self.down() 
            else:
                self.up()

            if vy < 0:
                self.right()
            else:
                self.left()
        # debug += str(self.ball_brick_horizontal_collide(ball)) + ':' + \
        #     str(self.ball_brick_vertical_collide(ball)) + '\n'
        # ball.reverse_vx()

    def trivial_collision(self, paddle):
        if self._dead:
            return True

        if self._velocity.getvx() == 0:
            self._velocity.setvx(-1)

        if self.side_walls_collide():
            self._velocity.reversevy()
            return True

        if self.top_collide():
            self._velocity.reversevx()
            return True

        if self.paddle_collide(paddle):
            if paddle._grab:
                self._velocity.setvx(0)
                self._velocity.setvy(0)

            else:
                if self._velocity.getvx() > 0:
                    self._velocity.reversevx()
                self.paddle_collide_handle(paddle)


            return True

        return False

    def paddle_centre(self, paddle, rel=None):
        left_paddle = paddle._pos[1]
        right_paddle = paddle._pos[1] +  paddle._size[1] - 1
        mid = (left_paddle + right_paddle) // 2
        # debug += str(rel) + '\n'
        if rel:
            y = left_paddle + rel
            self.set_posy(y)
        self.set_posy(mid)
     
    def boss_intersect(self, boss):
        top_boss = boss._pos[0]
        bottom_boss = boss._pos[0] + boss._size[0]

        left_boss = boss._pos[1]
        right_boss = boss._pos[1] + boss._size[1]

        left_ball = self._pos[1]
        top_ball = self._pos[0]

        if left_boss <= left_ball and left_ball + 1 <= right_boss:
            if top_boss <= top_ball and top_ball + 1 <= bottom_boss:
                return True

        return False

    def boss_intersection(self, boss):
        vx = self._velocity.getvx()
        vy = self._velocity.getvy()
        if self.boss_intersect(boss):
            self._pos[0] = boss._pos[0] + boss._size[0]
            self._pos[1] = (2*boss._pos[1] + boss._size[1])//2

    def boss_collide(self, boss):
        left_boss = boss._pos[1]
        right_boss = boss._pos[1] + boss._size[1]
        flag = ''
        bottom_boss = boss._pos[0] +  boss._size[0]

        if self._pos[0] < bottom_boss:
            if self._pos[1] == left_boss - 1:
                self._velocity.reversevy()
                return True
            elif self._pos[1] == right_boss:
                self._velocity.reversevy()
                return True
        elif self._pos[0] == bottom_boss:
            if left_boss <= self._pos[1] and self._pos[1] + self._size[1] <= right_boss:
                self._velocity.reversevx()
                return True
        return False
