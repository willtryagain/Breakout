import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep

from screen import Screen
import config as conf
from thing import Thing
from obstacle import FireBeam, MandalorianBullet, Boost, Magnet
from kbhit import KBHit
from mandalorian import Mandalorian
import utils
from boss import Boss
from dragon import Dragon

class Game:
    PLAY_KEYS = ('w', 'a', 'd')
    CONTROL_KEYS = ('q',)

    def __init__(self):
        rows, cols = os.open('stty size', 'r').read().split()
        self._height = int(rows) - conf.BUFFER_DOWN
        self._width = int(cols) - conf.BUFFER_RIGHT
        