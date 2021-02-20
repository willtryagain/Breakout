import os
import sys
from time import monotonic as clock, sleep
from colorama import Fore, Back, Style
from random import random

import settings
from ball import Ball
from paddle import Paddle
from brick import Brick
from player import Player
from expand import Expand
from fastball import Fastball
from thruball import Thruball
from ballmulti import Ballmulti
from kbhit import KBHit
from display import Display
from velocity import Velocity

debug = ''

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
            powerup = Expand(self._height, self._width, brick._pos, clock())
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
        level = 1

        # for i in range(level):
        #     for j in range(-i, i+1):
        #         brick = Brick(self._height, self._width, pos=[x0 + i*h, y0 + j*w])
        #         bricks.append(brick)

        for j in range(-level-settings.BRICK_LENGTH, level+settings.BRICK_LENGTH + 1):
            brick = Brick(self._height, self._width, pos=[x0 + level*h, y0 + j*w])
            bricks.append(brick)

        # for i in range(level-1, -1, -1):
        #     for j in range(-i, i+1):
        #         brick = Brick(self._height, self._width, pos=[x0 + (level +  level - i)*h, y0 + j*w])
        #         bricks.append(brick)

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
        vx = ball._velocity.getvx()
        vx = max(vx, 1)
        # distance from the middle
        factor = abs(mid - ball._pos[1]) // 2
        factor = max(factor, 1)
        vy = sign * factor

        ball._velocity.setvx(-vx) 
        ball._velocity.setvy(vy)

        return ball

   

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
        for index, brick in enumerate(self._bricks):
            left_brick = brick._pos[1]
            right_brick = left_brick + brick._size[1] - 1

            top_brick = brick._pos[0]
            bottom_brick = top_brick + brick._size[0] - 1

            top_ball = ball._pos[0]

            left_ball = ball._pos[1]
            right_ball = ball._pos[1] + ball._size[1] - 1
      
            in_between = (left_brick <= left_ball and right_ball <= right_brick)

            if in_between:
                # above
                if top_ball == top_brick - 1:
                    return index
                # below
                elif top_ball == bottom_brick + 1:
                    return index
           
        return -1   

    def ball_brick_vertical_collide(self, ball):
        """
            handle collision with brick 
            atmost one at a time
            Left of brick
        
            o   [|||||]

            Right of brick
                [|||||]    o
        """
        for index, brick in enumerate(self._bricks):
            left_brick = brick._pos[1]
            right_brick = left_brick + brick._size[1] - 1

            top_brick = brick._pos[0]
            bottom_brick = top_brick + brick._size[0] - 1

            top_ball = ball._pos[0]
            bottom_ball = ball._pos[0] + ball._size[0] - 1

            left_ball = ball._pos[1]
            right_ball = ball._pos[1] + ball._size[1] - 1
      
            in_between = (top_brick <= top_ball and bottom_ball <= bottom_brick)

            if in_between:
                # left
                if right_ball == left_brick - 1:
                    return index
                # right
                elif left_ball == right_brick + 1:
                    return index
           
        return -1   

    def lost_ball(self, ball):   
        bottom_ball = ball._pos[0] + ball._size[0] - 1
        bottom_display = self._height - 1

        return bottom_ball >= bottom_display

    def ball_brick_intersection(self, ball):
        vx = ball._velocity.getvx()
        if vx < 0: 
            while ball.intersects(self._display):
                ball.down()
        else:
            while ball.intersects(self._display):
                ball.up()
        return ball

    def collide(self, ball):

        if ball._dead:
            print('1')
            return ball

        if self.ball_side_walls_collide(ball):
            print('2')
            ball.reverse_vy()
            return ball

        if self.ball_top_collide(ball):
            print('3')
            ball.reverse_vx()
            return ball
        
        if self.ball_paddle_collide(ball):
            print('4')
            ball = self.ball_paddle_collide_handle(ball)
            return ball

        # if ball.intersects(self._display):
        #     return self.ball_brick_intersection(ball)
      
        index = self.ball_brick_horizontal_collide(ball)
        if index != -1:
            ball.reverse_vx()
            self._player._score += \
                self._bricks[index].get_damage_points(ball, self._player)
            self._bricks[index].repaint_brick()
            return ball

        index = self.ball_brick_vertical_collide(ball)
        if index != -1:
            ball.reverse_vy()
            self._player._score += \
                self._bricks[index].get_damage_points(ball, self._player)
            self._bricks[index].repaint_brick()
            return ball

        
        # fell down
        if self.lost_ball(ball):
            return self.reset_ball_paddle(ball)

        return ball
         
    def ball_collisions_handle(self):
        new_balls = []
        for ball in self._balls:
            ball = self.collide(ball)
            new_balls.append(ball)
        return new_balls

  
    def remove_bricks(self):
        indices = []
        for index, brick in enumerate(self._bricks):
            if brick._strength == 0:
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            self._powerups[index]._state = 'FALL'
            del self._bricks[index]


    def remove_powerups(self):
        indices = []
        for index, powerup in enumerate(self._powerups):
            if powerup._state == 'DELETE':
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            del self._powerups[index]

    def remove_items(self):
        self.remove_bricks()
        self.remove_powerups()

    def ball_paddle_centre(self, ball):
        left_paddle = self._paddle._pos[1]
        right_paddle = self._paddle._pos[1] +  self._paddle._size[1] - 1
        mid = (left_paddle + right_paddle) // 2
        ball.set_posy(mid)
        return ball

    def handle_keys(self):
        if self._keyboard.kbhit():
        
            key = self._keyboard.getch()

            # Pause / Unpause
            if key == 'q':
                self.end_game()

            # Pause / Unpause
            if key == 'p':
                self.PAUSED = not self.PAUSED

            # Paddle left / right
            elif key == 'a' or key == 'd':
                new_balls = []
                for ball in self._balls:
                    if not ball._dead:
                        self._paddle.move(key)
                    else:
                        self._paddle.move(key)
                        self.ball_paddle_centre(ball)
                    new_balls.append(ball)
                self._balls = new_balls
            
            # Ball left / right
            elif key == 'w' or key == 's':
                new_balls = []
                for ball in self._balls:
                    if not ball._dead:
                        pass
                    else:
                        ball.move(key)
                    new_balls.append(ball)
                self._balls = new_balls
            
            # Start the game
            elif key == ' ':
                new_balls = []
                for ball in self._balls:
                    ball._dead = False
                    if self.ball_paddle_collide(ball):
                        ball = self.ball_paddle_collide_handle(ball)
                    new_balls.append(ball)    
                self._balls = new_balls

            self._keyboard.flush()
       

    def reset_ball_paddle(self, ball):
        ball._dead = True
        ball._pos = [self._height-2, self._width//2 - 1]
        self._paddle._pos = [self._height-1, self._width//2 - self._paddle._size[1]]
        self._player.lose_life()
        ball._velocity.setvx(0)
        ball._velocity.setvy(0)
        return ball

    def move_items(self):
        new_balls = []
        for ball in self._balls:
            ball.move()
            new_balls.append(ball)
        self._balls = new_balls

        powerups = []
        for powerup in self._powerups:
            if powerup._state == 'FALL':
                # powerup.move()
                pass
            powerups.append(powerup)
        self._powerups = powerups
    def add_items(self):

        # put the balls
        for ball in self._balls:
            self._display.put(ball)

        self._display.put(self._paddle)

        for brick in self._bricks:
            if brick._strength:
                self._display.put(brick)

        for powerup in self._powerups:
            if powerup._state == 'FALL':
                self._display.put(powerup)

    def powerup_handle(self):
        global debug
        powerups = []
        for powerup in self._powerups:
            if powerup._state == 'FALL':
                if powerup.collision(self._paddle):
                    # assuming Expand
                    self._paddle = powerup.magic(self._paddle)
                    # debug += 'magic\n'
                
            elif powerup._state == 'ACTIVE':
                if powerup.time_up():
                    self._paddle = powerup.reverse(self._paddle)
                    # debug += 'reverse\n'
            powerups.append(powerup)
        self._powerups = powerups

    def wait(self, time):
        while clock() - time < 0.1:
            pass

    def end_game(self):
        global debug
        out = open('debug.txt', 'w')
        out.write(debug)
        out.close
        sys.exit(0) 

    def mainloop(self):
        global debug
        while True:
            time = clock()
            self.handle_keys()
            if self.PAUSED:
                self.wait(time)
                continue
            self.move_items()
            
            self._balls = self.ball_collisions_handle()
            self.powerup_handle()
            

    
            self.remove_items()

            self._display.clrscr()
            self.add_items()
            self._display.show()
            self._player.display_stats()
            self.wait(time) 
    
            for brick in self._bricks:
                debug += str(brick._pos[0]) + str(brick._pos[1]) + ','
            debug += '\n'
