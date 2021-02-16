import os
from time import monotonic as clock, sleep

from ball import Ball
from paddle import Paddle
from brick import Brick
from player import Player
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
        self._brick = Brick(self._height, self._width, pos=[2, self._width // 2])
        self._player = Player()

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


        # self.handle_brick_collisions()
        # reflection from paddle
        if self._ball._pos[0] == self._height-2 \
            and l <= self._ball._pos[1] \
            and self._ball._pos[1] <= r:
            vx = self._ball._velocity.getvx()
            self._ball._velocity.setvx(-vx)

        # hits the surface
        elif self._ball._pos[0] == self._height-1:
            self.handle_death()

        elif self._ball._pos[1] == 0 or self._ball._pos[1] == self._width-2:
            vy = self._ball._velocity.getvy()
            self._ball._velocity.setvy(-vy)

        elif self._ball._pos[0] == 0:
            vx = self._ball._velocity.getvx()
            self._ball._velocity.setvx(-vx)

    def handle_brick_collisions(self):
        y0 = self._brick._pos[1]
        x0 = self._brick._pos[0]
        y1 = y0 + self._brick._pos[1] - 1
        x1 = x0 + self._brick._pos[0] - 1


        is_above = (self._brick._pos[0] == x0 - 1)
        is_below = (self._brick._pos[0] == x1 + 1)
        is_left = (self._brick._pos[1] - 1)
        is_right = (self._brick._pos[1] + self._brick._size[1])
        is_between_y = (y0 <= self._brick._pos[1] and self._brick._pos[1] <= y1)
        is_between_x = (y0 <= self._brick._pos[1] and self._brick._pos[1] <= y1)
        if (is_above or is_below) \
            and is_between_y:
            vx = self._ball._velocity.getvx()
            self._ball._velocity.setvx(-vx)


    def handle_keys(self):
        if self._keyboard.kbhit():
        
            key = self._keyboard.getch()
            if key == 'a' or key == 'd':
                self._paddle.move(key)
            
            elif key == ''
            self._keyboard.flush()

    def handle_death(self):
        self._ball._pos = [self._height-2, self._width//2 - 1]
        self._ball._velocity.setvx(0)
        self._ball._velocity.setvy(0)
        self._paddle._pos = [self._height-1, self._width//2 - self._paddle._size[1]]
        self._player.lose_life()

    def move_items(self):
        self._ball.move()
        
    def add_items(self):
        self._display.put(self._ball)
        self._display.put(self._paddle)
        self._display.put(self._brick)

    def mainloop(self):
        
        while True:
            time = clock()
            self.handle_keys()
            self.move_items()
            self.handle_ball_collisions()

            self._display.clrscr()
            self.add_items()
            self._display.show()

            while clock() - time < 0.1:
                pass

