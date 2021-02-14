import os
from time import monotonic as clock, sleep

from ball import Ball
from kbhit import KBHit
from display import Display

class Game:
    
    def __init__(self):
        r, c = os.popen('stty size', 'r').read().split()
        self._height = int(r) - 10
        self._width = int(c) - 10

        self._display = Display(self._height, self._width)

    def mainloop(self):
        ball = Ball(self._height, self._width)
        
        while True:
            time = clock()
            self._display.clrscr()
            self._display.put(ball)
            self._display.show()

            while clock() - time < 0.1:
                pass

