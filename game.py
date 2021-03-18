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
from laser import Laser

from powerup import Powerup
from expand import Expand
from shrink import Shrink
from fastball import Fastball
from thruball import Thruball
from multi import Multi
from pgrab import Pgrab
from gunpaddle import Gunpaddle

from kbhit import KBHit
from display import Display
from velocity import Velocity

debug = ''

class Game:
    def __init__(self):
        r, c = os.popen('stty size', 'r').read().split()
        self._height = int(r) - settings.BOTTOM_MARGIN
        self._last_time = clock()
        self.bricks_fall = False
        self._width = int(c) - settings.RIGHT_MARGIN
        self.PAUSED = False
        self._paddle = Paddle(self._height, self._width)
        self._balls = [Ball(self._height, self._width, [
            self._height - 2, 
            (2*self._paddle._pos[1] + self._paddle._size[1]) // 2
        ])]
        self._lasers = []
        self._display = Display(self._height, self._width)
        self._keyboard = KBHit()
        self._bricks = self.get_brick_pattern(1)
        self._powerups = [] # self.add_powerups()
        self._player = Player()
        global debug

    def get_brick_pattern(self, level):
        """
        Get the pattern of bricks
        """
        bricks = []
        x0 = settings.BRICK_START_ROW
        y0 = self._width // 2
        h = 1
        w = 5
        margin = 2
        breadth = y0//4

        if level == 1:
            for j in range(-margin-settings.BRICK_LENGTH, margin+settings.BRICK_LENGTH + 1):
                if y0 + j*w >= self._width \
                    or y0 + j*w < 0:
                    continue
                brick = Brick(self._height, self._width, pos=[x0 + level*h, y0 + j*w])
                brick._strength = choice([1, 2, 3])
                brick.repaint()
                bricks.append(brick)

        if level == 2:
            for i in range(x0 + 5, x0 + 8):
                brick = Brick(self._height, self._width, pos=[i, y0 - breadth])
                brick._strength = choice([1, 2, 3])
                brick.repaint()
                bricks.append(brick)

                brick = Brick(self._height, self._width, pos=[i, y0 + breadth])
                brick._strength = choice([1, 2, 3])
                brick.repaint()
                bricks.append(brick)

        # unbreakable and possible
        bricks[0]._strength = 'INFINITY'
        bricks[0].repaint()
        brick = Brick(self._height, self._width, pos=[15, self._width//2])
        brick._rainbow = True
        brick.repaint()
        bricks.append(brick)




        # for i in range(level-1, -1, -1):
        #     for j in range(-i, i+1):
        #         brick = Brick(self._height, self._width, pos=[x0 + (level +  level - i)*h, y0 + j*w])
        #         brick._strength = choice([1, 2, 3, 'INFINITY'])
        #         brick.repaint()
        #         bricks.append(brick)

        return bricks

    def non_trivial_collision(self, ball):
        """
        collision which make changes to not only ball
        but bricks, player's score as well
        """
        if ball.intersects(self._bricks):
            ball.brick_intersection(self._bricks)
        
        index = ball.brick_corners_collide(self._bricks)
        if index != -1:
            # debug += 'corners\n'
            self._bricks[index]._velocity = ball._velocity
            self._bricks[index]._rainbow = False
            ball._velocity.reversevx()
            self._player._score += \
                self._bricks[index].get_damage_points(ball)
            self._bricks[index].repaint()
            return ball

        index = ball.brick_horizontal_collide(self._bricks)
        if index != -1:
            self._bricks[index]._velocity = ball._velocity
            self._bricks[index]._rainbow = False
            # debug += 'horizontal\n'
            ball._velocity.reversevx()
            self._player._score += \
                self._bricks[index].get_damage_points(ball)
            self._bricks[index].repaint()
            return ball

        index = ball.brick_vertical_collide(self._bricks)
        if index != -1:
            self._bricks[index]._velocity = ball._velocity
            self._bricks[index]._rainbow = False
            ball._velocity.reversevy()
            self._player._score += \
                self._bricks[index].get_damage_points(ball)
            self._bricks[index].repaint()
            return ball

        return ball
        
    def ball_collisions_handle(self):
        new_balls = []
        for ball in self._balls:
            if ball.paddle_collide(self._paddle):
                if self.bricks_fall and not ball._dead and not self._paddle._grab:
                    for brick in self._bricks:
                        brick.move()
                    self._last_time = clock()
            if not ball.trivial_collision(self._paddle):
                ball = self.non_trivial_collision(ball)
            if ball.lost():
                ball =  self.reset_game(ball)
                new_balls = [ball]
                break
            new_balls.append(ball)
        return new_balls

    def get_powerup(self, pos, type=None):
        if type == None:
        # randomly choose from the various types of powerups
            type = choice(['expand', 'shrink', 'pgrab', 'thruball', 'fastball', 'gunpaddle']) # 
            type = choice(['gunpaddle'])


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
        elif type == 'gunpaddle':
            powerup = Gunpaddle(self._height, self._width, pos, clock())     
        powerup._state = 'FALL'
        return powerup

    def remove_bricks(self):
        global debug 
        indices = []
        # find indices of bricks to be deleted
        # and place a powerup in their place
        for index, brick in enumerate(self._bricks):
            if brick._strength == 0:
                indices.append(index)
                pos = [brick._pos[0], brick._pos[1]]
                debug += 'pos ' + ' '.join(map(str, pos)) + '\n'
                if pos[1] ==  self._width//2:
                    powerup = self.get_powerup(pos, 'thruball')
                else:
                    powerup = self.get_powerup(pos)
                powerup._velocity = Velocity(brick._velocity.getvx(), brick._velocity.getvy())
                self._powerups.append(powerup)

        # delete the bricks
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

    def remove_lasers(self):
        indices = []
        for index, laser in enumerate(self._lasers):
            if laser.top_collide():
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            del self._lasers[index]

    def remove_items(self):
        self.remove_bricks()
        self.remove_powerups()
        self.remove_lasers()
    

    def handle_keys(self):
        global debug
        if self._keyboard.kbhit():
        
            key = self._keyboard.getch()

            # Quit
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
                        ball.paddle_centre(self._paddle)
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
                    if ball._velocity.getvx() == 0:
                        ball._velocity.setvx(1)
                    if  ball.paddle_collide(self._paddle):
                        if self._paddle._grab:
                            self._paddle._rel = ball._pos[1] - self._paddle._pos[1] 
                            debug += "{} {} {}\n".format(ball._pos[1], self._paddle._pos[1], self._paddle._rel)
                        if self.bricks_fall:
                            debug += 'fall\n'
                            for brick in self._bricks:
                                brick.move()
                            self._last_time = clock()

                        ball.paddle_collide_handle(self._paddle)
                        ball._dead = False
                    new_balls.append(ball)    
                self._balls = new_balls
            
            elif key == 'l':
                self._player._level += 1
                self._bricks = self.get_brick_pattern(self._player._level)
                self._powerups = self.deactivate()

            elif key == 'f':
                if self._paddle._gun:
                    pos = self._paddle._pos
                    len = self._paddle._size[1]
                    laser = Laser(self._height, self._width, [pos[0]-1, pos[1]], len)
                    self._lasers.append(laser)
            
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

        for laser in self._lasers:
            laser.move()

        if clock() - self._last_time > settings.FALL_TIME:
            self.bricks_fall = True
        else:
            self.bricks_fall = False
        

    def add_items(self):
        global debug
        # add balls to the screen
        for ball in self._balls:
            self._display.put(ball)

        self._display.put(self._paddle)

        for brick in self._bricks:
            if brick._rainbow:
                brick.repaint()
            if brick._strength:
                self._display.put(brick)

        for powerup in self._powerups:
            if powerup._state == 'FALL':
                self._display.put(powerup)

        for laser in self._lasers:
            debug += 'pos: ' + ' '.join(map(str, laser.get_pos())) + '\n'
            debug += 'tail: ' + ' '.join(map(str, laser.get_tail())) + '\n'
            self._display.put(laser)


    def powerup_magic(self, powerup):
        """
        powerup starts working
        """
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
        elif powerup._kind == 'pgrab' or \
            powerup._kind == 'gunpaddle':
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
                if not powerup.trivial_collision():
                    if powerup.paddle_collision(self._paddle):
                        self.powerup_magic(powerup)
                    # debug += 'magic\n'
                
            elif powerup._state == 'ACTIVE':
                if powerup.time_up():
                    self.powerup_reverse(powerup)
            powerups.append(powerup)
        self._powerups = powerups

    def laser_handle(self):
        for laser in self._lasers:
            index = laser.brick_corners_collide(self._bricks)
            if index != -1:
                # debug += 'corners\n'
                self._bricks[index]._velocity = laser._velocity
                self._bricks[index]._rainbow = False
                self._player._score += \
                    self._bricks[index].get_damage_points(laser)
                self._bricks[index].repaint()
                continue

            index = laser.brick_vertical_collide(self._bricks)
            if index != -1:
                self._bricks[index]._velocity = laser._velocity
                self._bricks[index]._rainbow = False
                self._player._score += \
                    self._bricks[index].get_damage_points(laser)
                self._bricks[index].repaint()

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
            self._bricks = self.get_brick_pattern(self._player._level)
            self._player._level += 1
            self._powerups = self.deactivate()

    def check_end_game(self):
        if self._player._level == 4:
            raise SystemExit
        for brick in self._bricks:
            if brick._pos[0] == self._height - 1:
                self.end_game()

    def mainloop(self):
        global debug
        while True:
            time = clock()
            self.handle_keys()
            if self.PAUSED:
                self.wait(time)
                continue
            self.check_end_game()
            self.level_up()
            self.move_items()
            
            self._balls = self.ball_collisions_handle()
            self.powerup_handle()
            self.laser_handle()
            self.remove_items()
            self._display.clrscr()
            self.add_items()
            self._display.show()
            self._player.display_stats(self._paddle._size[1], self._balls[0])
            self.wait(time) 