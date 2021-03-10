import os
import sys
from time import monotonic as clock, sleep
from colorama import Fore, Back, Style
from random import random, choice, randint

import settings
from ball import Ball
from paddle import Paddle
from brick import Brick
from player import Player

from powerup import Powerup
from expand import Expand
from shrink import Shrink
from fastball import Fastball
from thruball import Thruball
from multi import Multi
from pgrab import Pgrab

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
        self._powerups = [] # self.add_powerups()
        self._player = Player()

    def get_brick_pattern(self):
        """
        Get the pattern of bricks
        """
        bricks = []
        x0 = settings.BRICK_START_ROW
        y0 = self._width // 2
        h = 1
        w = 5
        level = y0//25

        # for i in range(level):
        #     for j in range(-i, i+1):
        #         brick = Brick(self._height, self._width, pos=[x0 + i*h, y0 + j*w])
        #         brick._strength = choice([1, 2, 3, 'INFINITY'])
        #         brick.repaint_brick()
        #         bricks.append(brick)

        for j in range(-level-settings.BRICK_LENGTH, level+settings.BRICK_LENGTH + 1):
            if y0 + j*w >= self._width \
                or y0 + j*w < 0:
                continue
            brick = Brick(self._height, self._width, pos=[x0 + level*h, y0 + j*w])
            brick._strength = choice([1, 2, 3])# , 'INFINITY'])
            brick.repaint_brick()
            bricks.append(brick)

        # for i in range(level-1, -1, -1):
        #     for j in range(-i, i+1):
        #         brick = Brick(self._height, self._width, pos=[x0 + (level +  level - i)*h, y0 + j*w])
        #         brick._strength = choice([1, 2, 3, 'INFINITY'])
        #         brick.repaint_brick()
        #         bricks.append(brick)

        return bricks

    def non_trivial_collision(self, ball):
        if ball.intersects(self._bricks):
            ball.brick_intersection(self._bricks)
        
        index = ball.brick_corners_collide(self._bricks)
        if index != -1:
            # debug += 'corners\n'
            ball.reverse_vx()
            self._player._score += \
                self._bricks[index].get_damage_points(ball)
            self._bricks[index].repaint_brick()
            return ball

        index = ball.brick_horizontal_collide(self._bricks)
        if index != -1:
            # debug += 'horizontal\n'
            ball.reverse_vx()
            self._player._score += \
                self._bricks[index].get_damage_points(ball)
            self._bricks[index].repaint_brick()
            return ball

        index = ball.brick_vertical_collide(self._bricks)
        if index != -1:
            ball.reverse_vy()
            self._player._score += \
                self._bricks[index].get_damage_points(ball)
            self._bricks[index].repaint_brick()
            return ball

        return ball
        
    def ball_collisions_handle(self):
        new_balls = []
        for ball in self._balls:
            if not ball.trivial_collision(self._paddle):
                ball = self.non_trivial_collision(ball)
            if ball.lost():
                ball =  self.reset_game(ball)
                new_balls = [ball]
                break
            new_balls.append(ball)
        return new_balls

    def get_powerup(self, pos):
        type = choice(['expand', 'shrink', 'pgrab', 'thruball']) # 'fastball'
        # type = choice(['multi'])

        if type == 'expand':
            powerup = Expand(self._height, self._width, pos, clock())
        elif type == 'shrink':  
            powerup = Shrink(self._height, self._width, pos, clock())
        elif type == 'fastball':
            powerup = Fastball(self._height, self._width, pos, clock())
        elif type == 'multi':
            powerup = Multi(self._height, self._width, pos, clock())
        elif type == 'pgrab':
            powerup = Pgrab(self._height, self._width, pos, clock())   
        elif type == 'thruball':
            powerup = Thruball(self._height, self._width, pos, clock())      
        powerup._state = 'FALL'
        return powerup

    def remove_bricks(self):
        global debug 
        indices = []
        for index, brick in enumerate(self._bricks):
            if brick._strength == 0:
                indices.append(index)
                pos = [brick._pos[0], brick._pos[1]]
                powerup = self.get_powerup(pos)
                self._powerups.append(powerup)

        indices.sort(reverse=True)
        for index in indices:
            del self._bricks[index]

    def remove_powerups(self):
        global debug 
        indices = []
        for index, powerup in enumerate(self._powerups):
            if powerup._state == 'DELETE':
                # debug += str(index) + '\n'
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            del self._powerups[index]

    def remove_items(self):
        self.remove_bricks()
        self.remove_powerups()

    def ball_paddle_centre(self, ball, rel=None):
        left_paddle = self._paddle._pos[1]
        right_paddle = self._paddle._pos[1] +  self._paddle._size[1] - 1
        mid = (left_paddle + right_paddle) // 2
        
        if rel:
            y = left_paddle + rel
            ball.set_posy(y)
            return ball
       
        ball.set_posy(mid)
        return ball

    def handle_keys(self):
        global debug
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
                    self._paddle.move(key)
                    if  ball._dead or (self._paddle._grab and ball._velocity.getvx() == 0):
                        self.ball_paddle_centre(ball, rel=None)
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
                    if  ball.paddle_collide(self._paddle):
                        ball.paddle_collide_handle(self._paddle)
                        ball._dead = False
                    new_balls.append(ball)    
                self._balls = new_balls
            self._keyboard.flush()
       
    def reset_game(self, ball):
        global debug 
        self.remove_items()
        self._display.clrscr()
        self.add_items()
        self._display.show()

        ball._dead = True
        self._display.alert()
        self._powerups = self.deactivate()
        self._paddle.reset()
        ball._pos[0] = self._height-2
        ball._pos[1] = randint(self._paddle._pos[1], self._paddle._pos[1] + self._paddle._size[1] - 2)
        self._player.lose_life()
        if self._player._lives == 0:
            self.end_game()
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
                powerup.move()
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

    def powerup_magic(self, powerup):
        if powerup._kind == 'multi':
            self._balls = powerup.magic(self._balls)
        elif powerup._kind == 'pgrab':
            self._paddle = powerup.magic(self._paddle, self._balls[0])
        elif powerup._kind == 'fastball':
            self._balls = powerup.magic(self._balls)
        elif powerup._kind == 'thruball':
            self._balls = powerup.magic(self._balls)
        else:
            self._paddle = powerup.magic(self._paddle)

    def powerup_reverse(self, powerup):
        if powerup._kind == 'multi':
            self._balls = powerup.reverse(self._balls)
        elif powerup._kind == 'pgrab':
            self._paddle = powerup.reverse(self._paddle)
        elif powerup._kind == 'fastball':
            self._balls = powerup.reverse(self._balls)
        elif powerup._kind == 'thruball':
            self._balls = powerup.reverse(self._balls)
        else:
            self._paddle = powerup.reverse(self._paddle)

    def powerup_handle(self):
        global debug
        powerups = []
        for powerup in self._powerups:
            if powerup._state == 'FALL':
                if powerup.collision(self._paddle):
                    self.powerup_magic(powerup)
                    if self._balls[0]._fast:
                        self._balls[0].go_fast()
                    debug += 'magic\n'
                
            elif powerup._state == 'ACTIVE':
                if powerup.time_up():
                    self.powerup_reverse(powerup)
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

    def deactivate(self):
        powerups = []
        for powerup in self._powerups:
            if powerup._state == 'ACTIVE':
                self.powerup_reverse(powerup)
                powerup._state = 'DELETE'

            powerups.append(powerup)
        return powerups

    def level_up(self):
        if not self._bricks: 
            self._bricks = self.get_brick_pattern()
            self._player._level += 1
        if self._player._level == 3:
            raise SystemExit

    def mainloop(self):
        global debug
        while True:
            time = clock()
            self.handle_keys()
            if self.PAUSED:
                self.wait(time)
                continue
            self.level_up()
            self.move_items()
            
            self._balls = self.ball_collisions_handle()
            self.powerup_handle()
            self.remove_items()
            self._display.clrscr()
            self.add_items()
            self._display.show()
            self._player.display_stats(self._paddle._size[1], self._balls[0])
            self.wait(time) 
            debug += str(self._balls[0]._thru) + '\n'