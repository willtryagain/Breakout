import os
from time import monotonic as clock, sleep
from random import random

from ball import Ball
from paddle import Paddle
from brick import Brick
from player import Player
from powerup import Powerup
from kbhit import KBHit
from display import Display
from velocity import Velocity


class Game:
    
    def __init__(self):
        r, c = os.popen('stty size', 'r').read().split()
        self._height = int(r) - 10
        self._width = int(c) - 10
        self._ball = Ball(self._height, self._width)
        self._paddle = Paddle(self._height, self._width)
        self._display = Display(self._height, self._width)
        self._keyboard = KBHit()
        self._powerup = Powerup(self._height, self._width, [0, 0])
        self._bricks = self.arrange_bricks(1, 1)
        self._player = Player()

    def arrange_bricks(self, rows, cols):
        bricks = []
        x0 = 2
        y0 = 2
        h = 1
        w = 5
        for i in range(rows):
            for j in range(cols):
                brick = Brick(self._height, self._width, pos=[x0 + i*h, y0 + j*w])
                bricks.append(brick)
                if i == 0 and j == 0:
                    self._powerup = Powerup(self._height, self._width, [x0 + i*h, y0 + j*w])
        
        return bricks

    def handle_paddle_collisions(self):
        mid = (2*self._paddle._pos[1] + self._paddle._size[1] - 1) // 2
        if self._ball._pos[1] < mid:
            sign = -1
        else:
            sign = 1
        vx = self._ball._velocity.getvx()
        vx = max(vx, 1)
        factor = abs(mid - self._ball._pos[1]) // 2
        factor = max(factor, 1)
        vy = sign * factor

        self._ball._velocity.setvx(-vx) 
        self._ball._velocity.setvy(vy)

    def handle_ball_collisions(self):
        '''
        -----> Y
        |
        |
        v 
        X 

        '''
        l = self._paddle._pos[1]
        r = self._paddle._pos[1] +  self._paddle._size[1] - 1
    
        if not self._ball._alive:
            # print('not alive')
            return

        if self.handle_brick_collisions():
            # print('brick')
            pass


        # reflection from paddle
        elif self._ball._pos[0] == self._height-2 \
            and l <= self._ball._pos[1] \
            and self._ball._pos[1] <= r:
            self.handle_paddle_collisions()
            # print('paddle')

        # reaches the bottom
        elif self._ball._pos[0] == self._height - self._ball._size[0]:
            self.reset()
            # print('bottom')

        # hits the side walls
        elif self._ball._pos[1] == 0 or self._ball._pos[1] == self._width - self._ball._size[1]:
            vy = self._ball._velocity.getvy()
            self._ball._velocity.setvy(-vy)
            # print('side')

        # hits the top
        elif self._ball._pos[0] == 0:
            vx = self._ball._velocity.getvx()
            self._ball._velocity.setvx(-vx)
            # print('top')

    def handle_brick_collisions(self):

        hit = False
        for brick in self._bricks:
        
            y0 = brick._pos[1]
            x0 = brick._pos[0]
            y1 = y0 + brick._size[1] - 1
            x1 = x0 + brick._size[0] - 1


            is_above = (self._ball._pos[0] == x0 - 1)
            is_below = (self._ball._pos[0] == x1 + 1)
            is_left = (self._ball._pos[1] == brick._pos[1] - 1)
            is_right = (self._ball._pos[1] == brick._pos[1] + brick._size[1])
            is_between_y = (y0 <= self._ball._pos[1] and self._ball._pos[1] + self._ball._size[1] - 1 <= y1)
            is_between_x = (x0 <= self._ball._pos[0] and self._ball._pos[0] + self._ball._size[0] - 1 <= x1)
            if (is_above or is_below) \
                and is_between_y:
                vx = self._ball._velocity.getvx()
                self._ball._velocity.setvx(-vx)
                brick.decrease_strength()
                hit = True
            
            elif (is_left or is_right) \
                and is_between_x:
                vy = self._ball._velocity.getvy()
                self._ball._velocity.setvy(-vy)
                brick.decrease_strength()
                hit = True
           
        return hit

    def remove_bricks(self):
        indices = []
        for index, brick in enumerate(self._bricks):
            if brick._strength == 0:
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            if self._bricks[index]._pos == self._powerup._pos:
                self._powerup._active = True
            del self._bricks[index]

    def handle_keys(self):
        if self._keyboard.kbhit():
        
            key = self._keyboard.getch()
            if key == 'a' or key == 'd':
                self._paddle.move(key)
            
            elif key == ' ':
                if self._paddle._pos[1] <= self._ball._pos[1] \
                    and self._ball._pos[1] <= self._paddle._pos[1] + self._paddle._size[1] - 1 \
                    and not self._ball._alive:
                    self.restart()

            self._keyboard.flush()

    def restart(self):
        self._ball._alive = True
        self.handle_paddle_collisions()

    def reset(self):
        self._ball._alive = False
        self._ball._pos = [self._height-2, self._width//2 - 1]
        self._paddle._pos = [self._height-1, self._width//2 - self._paddle._size[1]]
        self._player.lose_life()
        self._ball._velocity.setvx(0)
        self._ball._velocity.setvy(0)

    def move_items(self):
        self._ball.move()
        if self._powerup._active:
            self._powerup.move()
        
    def add_items(self):

        self._display.put(self._ball)
        self._display.put(self._paddle)
        for brick in self._bricks:
            self._display.put(brick)
        if self._powerup._active:
            self._display.put(self._powerup)

    def mainloop(self):
        while True:
            time = clock()
            self.handle_keys()
            self.move_items()
            self.handle_ball_collisions()
            self.remove_bricks()
            # print(self._ball._velocity.getvx(), self._ball._velocity.getvy())
            self._display.clrscr()
            self.add_items()
            self._display.show()
            self._player.display_stats()
            while clock() - time < 0.1:
                pass
            
