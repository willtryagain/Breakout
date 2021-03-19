import numpy as np
from time import monotonic as clock
from colorama import Fore, Back, Style

import settings
import res

class Player:
    def __init__(self, lives=settings.MAX_LIVES, score=0):
        self._lives = lives
        self._score = score
        self._start = clock()
        self._score = score
        self._level = 1

    def lose_life(self):
        self._lives -= 1

    def display_stats(self, length, ball, stime, boss):
        vx = ball._velocity.getvx()
        vy = ball._velocity.getvy()
        rtime = None
        health = None
        if boss.awake:
            health = boss._health
        

        time_passed = int(clock() - self._start)
        speed = int(np.sqrt(vx**2 + vy**2))
        print(Style.RESET_ALL + Style.BRIGHT, end='')
        print('\033[0K', end='') # EOL
        print('SCORE:', str(self._score).rjust(1), end='\t')
        print('BALLS:', str(self._lives).rjust(1), end='\t')
        print('TIME:', str(time_passed).rjust(3), end='\t')
        print('PADDLE:', str(length).rjust(2), end='\t')
        # print('BALL SPEED', str(speed).rjust(3), end='\t')
        print('LEVEL', str(self._level).rjust(3), end='\t')
        if stime:
            rtime = int(settings.POWERUP_TIME - (clock() - stime))
        if rtime:
            print('REM TIME:', str(rtime).rjust(3), end='\t')
        if health:
            print('BOSS HEALTH:', res.get_health_bar(10, health, settings.BOSS_HEALTH))