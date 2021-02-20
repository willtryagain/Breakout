import os
from time import monotonic as clock, sleep
from colorama import Fore, Back, Style
from random import random

import settings
from ball import Ball
from paddle import Paddle
from brick import Brick
from player import Player
from powerup import Powerup
from fastball import Fastball
from thruball import Thruball
from ballmulti import Ballmulti
from kbhit import KBHit
from display import Display
from velocity import Velocity


class Game:
    def __init__(self):
        r, c = os.popen('stty size', 'r').read().split()
        self._height = int(r) - settings.BOTTOM_MARGIN
        self._width = int(c) - settings.RIGHT_MARGIN
        self.PAUSED = False
        self._paddle = Paddle(self._height, self._width)
        self._balls = [Ball(self._height, self._width, [
            self._height - 2, 
            (2*self._paddle._pos[1] + self._paddle._size[1]) // 2
        ])]
        self._display = Display(self._height, self._width)
        self._keyboard = KBHit()
        self._bricks = self.get_brick_pattern()
        self._powerups = self.add_powerups()
        self._player = Player()

    def add_powerups(self):
        """
        add powerups to bricks
        """
        powerups = []
        for brick in self._bricks:
            powerup = Ballmulti(self._height, self._width, brick._pos, clock())
            powerups.append(powerup)

        return powerups    

    def get_brick_pattern(self):
        """
        Get the pattern of bricks
        """
        bricks = []
        x0 = settings.BRICK_START_ROW
        y0 = self._width // 2
        h = 1
        w = 5
        level = y0//8

        for i in range(level):
            for j in range(-i, i+1):
                brick = Brick(self._height, self._width, pos=[x0 + i*h, y0 + j*w])
                bricks.append(brick)

        for j in range(-level-settings.BRICK_LENGTH, level+settings.BRICK_LENGTH + 1):
            brick = Brick(self._height, self._width, pos=[x0 + level*h, y0 + j*w])
            bricks.append(brick)

        for i in range(level-1, -1, -1):
            for j in range(-i, i+1):
                brick = Brick(self._height, self._width, pos=[x0 + (level +  level - i)*h, y0 + j*w])
                bricks.append(brick)

        return bricks

    def ball_paddle_collide_handle(self, ball):

        # middle position of paddle
        mid = (2*self._paddle._pos[1] + self._paddle._size[1] - 1) // 2

        # in first half 
        if ball._pos[1] < mid:
            # go left
            sign = -1
        else:
            # go right
            sign = 1
        vx = self._balls[i]._velocity.getvx()
        vx = max(vx, 1)
        # distance from the middle
        factor = abs(mid - self._balls[i]._pos[1]) // 2
        factor = max(factor, 1)
        vy = sign * factor

        ball._velocity.setvx(-vx) 
        ball._velocity.setvy(vy)

        return ball

    def handle_paddle_collisions(self):
        for i in range(len(self._balls)):
            self._balls[i] = self.ball_paddle_collide(self._balls[i])

    def ball_paddle_collide(self, ball):
        """
        check if ball collided with the paddle 
        """
        left_paddle = self._paddle._pos[1]
        right_paddle = self._paddle._pos[1] +  self._paddle._size[1] - 1
        height_paddle = self._paddle._pos[0]

        height_ball = ball._pos[0]
        left_ball = ball._pos[1]
        right_ball = ball._pos[1] + ball._size[1]

        # ball is just above paddle
        if height_ball == height_paddle - 1:
            if left_paddle <= left_ball and right_ball <= right_paddle:
                return True
        
        return False

    def ball_side_walls_collide(self, ball):
        """
        check if ball collided with the side walls 
        """
        left_ball = ball._pos[1]
        right_ball = ball._pos[1] + ball._size[1] - 1

        left_wall = 0
        right_wall = self._width - 1

        # hits the side walls
        if left_ball == left_wall or right_wall == right_ball:
            return True
        
        return False

    def ball_top_collide(self, ball):
        """
        check if ball collided with the top wall
        """
        top_ball = ball._pos[0]
        top_wall = 0

        if top_ball == top_wall:
            return True

        return False

    def ball_brick_horizontal_collide(self, ball):
        """
            Above hori
               V
            [|||||]

            [|||||]
               ^
        """

    def collide(self, ball):

        if ball._dead:
            return

        if self.ball_side_walls_collide(ball):
            ball.reverse_vy()
        
        elif ball_top_collide(ball):
            ball.reverse_vx()
        
        elif ball_paddle_collide(ball):
            ball_paddle_collide_handle(ball)
      
        # bricks    
        if self.handle_brick_collisions():
            # print('brick')
            pass


        # fell down
        if height_ball + ball._size[0] - 1 == self._height - 1:
            self.reset()
                # print('bottom')

         
    def handle_ball_collisions(self):
       
      

    def handle_brick_collisions(self):

        hit = False
        for i in range(len(self._balls)):
            for brick in self._bricks:
            
                y0 = brick._pos[1]
                x0 = brick._pos[0]
                y1 = y0 + brick._size[1] - 1
                x1 = x0 + brick._size[0] - 1


                is_above = (self._balls[i]._pos[0] == x0 - 1)
                is_below = (self._balls[i]._pos[0] == x1 + 1)
                is_left = (self._balls[i]._pos[1] == brick._pos[1] - 1)
                is_right = (self._balls[i]._pos[1] == brick._pos[1] + brick._size[1])
                is_between_y = (y0 <= self._balls[i]._pos[1] and self._balls[i]._pos[1] + self._balls[i]._size[1] - 1 <= y1)
                is_between_x = (x0 <= self._balls[i]._pos[0] and self._balls[i]._pos[0] + self._balls[i]._size[0] - 1 <= x1)
                if (is_above or is_below) \
                    and is_between_y:
                    vx = self._balls[i]._velocity.getvx()
                    self._balls[i]._velocity.setvx(-vx)
                    brick.decrease_strength(self._balls[i])
                    hit = True
                
                elif (is_left or is_right) \
                    and is_between_x:
                    vy = self._balls[i]._velocity.getvy()
                    self._balls[i]._velocity.setvy(-vy)
                    brick.decrease_strength(self._balls[i])
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
                for i in range(len(self._balls)):
                    if self._balls[i]._alive:
                        self._paddle.move(key)
                    else:
                        self._paddle.move(key, self._balls[i])
            
            elif key == 'w' or key == 's':
                for i in range(len(self._balls)):
                    if not self._balls[i]._alive:
                        self._balls[i].move(key)
            elif key == ' ':
                for i in range(len(self._balls)):
                    if self._paddle._pos[1] <= self._balls[i]._pos[1] \
                        and self._balls[i]._pos[1] <= self._paddle._pos[1] + self._paddle._size[1] - 1 \
                        and not self._balls[i]._alive:
                        self.restart()

            self._keyboard.flush()

    def restart(self):
        for i in range(len(self._balls)):
            self._balls[i]._alive = True
        self.handle_paddle_collisions()

    def reset(self):
        for i in range(len(self._balls)):
            self._balls[i]._alive = False
            self._balls[i]._pos = [self._height-2, self._width//2 - 1]
            self._paddle._pos = [self._height-1, self._width//2 - self._paddle._size[1]]
            self._player.lose_life()
            self._balls[i]._velocity.setvx(0)
            self._balls[i]._velocity.setvy(0)

    def move_items(self):
        balls = []
        for ball in self._balls:
            balls.append(ball)
        self._balls = []
        for ball in balls:
            ball.move()
            self._balls.append(ball)
        for powerup in self._powerups:
            if powerup._state == 'ACTIVE':
                powerup.move()
        
    def add_items(self):
        for i in range(len(self._balls)):
            self._display.put(self._balls[i])
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
            print(self._width)
            if self.PAUSED:
                while clock() - time < 0.1:
                    pass
                continue
            self.move_items()
            self.handle_ball_collisions()
            for powerup in self._powerups:
                if powerup._state == 'ACTIVE':
                    balls = powerup.handle_collision(self._paddle, self._balls)
                    if balls is not None:
                        self._balls = balls
                    
                elif powerup._state == 'IN_USE':
                    if clock() - powerup._start_time >= 40:
                        powerup._state == 'DELETE'
                        self._paddle.update(reset=True)

    
            self.remove()

            self._display.clrscr()
            self.add_items()
            self._display.show()
            self._player.display_stats()
            while clock() - time < 0.1:
                pass
            
