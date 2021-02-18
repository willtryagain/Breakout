import os
from time import monotonic as clock, sleep
from random import random

from ball import Ball
from paddle import Paddle
from colorama import Fore, Back, Style
from brick import Brick
from player import Player
from powerup import Powerup
from fastball import Fastball
from thruball import Thruball

from kbhit import KBHit
from display import Display
from velocity import Velocity


class Game:
    def __init__(self):
        r, c = os.popen('stty size', 'r').read().split()
        self._height = int(r) - 10
        self._width = int(c) - 10
        self.PAUSED = False
        self._paddle = Paddle(self._height, self._width)
        self._balls = [Ball(self._height, self._width, [
            self._height - 2, 
            (2*self._paddle._pos[1] + self._paddle._size[1]) // 2
        ])]
        self._display = Display(self._height, self._width)
        self._keyboard = KBHit()
        self._bricks = self.arrange_bricks(3, 3)
        self._powerups = self.get_powerups()
        self._player = Player()

    def get_powerups(self):
        powerups = []
        for brick in self._bricks:
            powerup = Thruball(self._height, self._width, brick._pos, clock())
            powerups.append(powerup)

        return powerups    

    def arrange_bricks(self, rows, cols):
        bricks = []
        x0 = 2
        y0 = 2
        h = 1
        w = 5
        for i in range(rows):
            for j in range(cols):
                if i == j or i + j == cols - 1:
                    brick = Brick(self._height, self._width, pos=[x0 + i*h, y0 + j*w])
                    bricks.append(brick)
        
        brick = Brick(self._height, self._width, pos=[x0 + rows*h, y0 + cols*w])
        brick.draw_brick(Back.CYAN)
        brick._strength = 'INFINITY'
        bricks.append(brick)
        return bricks

    def handle_paddle_collisions(self):
        for ball in self._balls:
            mid = (2*self._paddle._pos[1] + self._paddle._size[1] - 1) // 2
            if ball._pos[1] < mid:
                sign = -1
            else:
                sign = 1
            vx = ball._velocity.getvx()
            vx = max(vx, 1)
            factor = abs(mid - ball._pos[1]) // 2
            factor = max(factor, 1)
            vy = sign * factor

            ball._velocity.setvx(-vx) 
            ball._velocity.setvy(vy)

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

        for ball in self._balls:
        
        
            if not ball._alive:
                # print('not alive')
                continue

            if self.handle_brick_collisions():
                # print('brick')
                pass


            # reflection from paddle
            elif ball._pos[0] == self._height-2 \
                and l <= ball._pos[1] \
                and ball._pos[1] <= r:
                self.handle_paddle_collisions()
                # print('paddle')

            # reaches the bottom
            elif ball._pos[0] == self._height - ball._size[0]:
                self.reset()
                # print('bottom')

            # hits the side walls
            elif ball._pos[1] == 0 or ball._pos[1] == self._width - ball._size[1]:
                vy = ball._velocity.getvy()
                ball._velocity.setvy(-vy)
                # print('side')

            # hits the top
            elif ball._pos[0] == 0:
                vx = ball._velocity.getvx()
                ball._velocity.setvx(-vx)
                # print('top')

    def handle_brick_collisions(self):

        hit = False
        for ball in self._balls:
            for brick in self._bricks:
            
                y0 = brick._pos[1]
                x0 = brick._pos[0]
                y1 = y0 + brick._size[1] - 1
                x1 = x0 + brick._size[0] - 1


                is_above = (ball._pos[0] == x0 - 1)
                is_below = (ball._pos[0] == x1 + 1)
                is_left = (ball._pos[1] == brick._pos[1] - 1)
                is_right = (ball._pos[1] == brick._pos[1] + brick._size[1])
                is_between_y = (y0 <= ball._pos[1] and ball._pos[1] + ball._size[1] - 1 <= y1)
                is_between_x = (x0 <= ball._pos[0] and ball._pos[0] + ball._size[0] - 1 <= x1)
                if (is_above or is_below) \
                    and is_between_y:
                    vx = ball._velocity.getvx()
                    ball._velocity.setvx(-vx)
                    brick.decrease_strength(ball)
                    hit = True
                
                elif (is_left or is_right) \
                    and is_between_x:
                    vy = ball._velocity.getvy()
                    ball._velocity.setvy(-vy)
                    brick.decrease_strength(ball)
                    hit = True
            
        return hit

        

    def remove(self):
        self.remove_bricks()
        self.remove_powerups()

    def remove_bricks(self):
        indices = []
        for index, brick in enumerate(self._bricks):
            if brick._strength == 0:
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            self._powerups[index]._state = 'ACTIVE'
            del self._bricks[index]

    def remove_powerups(self):
        indices = []
        for index, powerup in enumerate(self._powerups):
            if powerup._state == 'DELETE':
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            del self._powerups[index]

    def handle_keys(self):
        if self._keyboard.kbhit():
        
            key = self._keyboard.getch()

            if key == 'p':
                self.PAUSED = not self.PAUSED
            if key == 'a' or key == 'd':
                for ball in self._balls:
                    if ball._alive:
                        self._paddle.move(key)
                    else:
                        self._paddle.move(key, ball)
            
            elif key == 'w' or key == 's':
                for ball in self._balls:
                    if ball._alive:
                        ball.move(key)
            elif key == ' ':
                for ball in self._balls:
                    if self._paddle._pos[1] <= ball._pos[1] \
                        and ball._pos[1] <= self._paddle._pos[1] + self._paddle._size[1] - 1 \
                        and not ball._alive:
                        self.restart()

            self._keyboard.flush()

    def restart(self):
        for ball in self._balls:
            ball._alive = True
            self.handle_paddle_collisions()

    def reset(self):
        for ball in self._balls:
            ball._alive = False
            ball._pos = [self._height-2, self._width//2 - 1]
            self._paddle._pos = [self._height-1, self._width//2 - self._paddle._size[1]]
            self._player.lose_life()
            ball._velocity.setvx(0)
        ball._velocity.setvy(0)

    def move_items(self):
        for ball in self._balls:
            ball.move()
            for powerup in self._powerups:
                if powerup._state == 'ACTIVE':
                    powerup.move()
        
    def add_items(self):
        for ball in self._balls:
            self._display.put(ball)
            self._display.put(self._paddle)
            for brick in self._bricks:
                if brick._strength:
                    self._display.put(brick)
            for powerup in self._powerups:
                if powerup._state == 'ACTIVE':
                    self._display.put(powerup)

    def mainloop(self):
        while True:
            time = clock()
            self.handle_keys()

            if self.PAUSED:
                while clock() - time < 0.1:
                    pass
                continue
            self.move_items()
            self.handle_ball_collisions()
            for powerup in self._powerups:
                if powerup._state == 'ACTIVE':
                    for ball in self._balls:
                        powerup.handle_collision(self._paddle, ball)
                elif powerup._state == 'IN_USE':
                    if clock() - powerup._start_time >= 40:
                        powerup._state == 'DELETE'
                        self._paddle.update(reset=True)
            self.remove()
            # print(self._ball._velocity.getvx(), self._ball._velocity.getvy())
            self._display.clrscr()
            self.add_items()
            self._display.show()
            self._player.display_stats()
            print(self._paddle._size[1])
            while clock() - time < 0.1:
                pass
            
