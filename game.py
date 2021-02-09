import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep

from screen import Screen
import settings
from meta import Meta
from elements import Ball, Brick
from kbhit import KBHit
import utils

class Game:
    def __init__(self):
        rows, cols = os.popen('ssty size', 'r').read().split()
        self._height = int(rows) - settings.BUFFER_HEIGHT
        self._width = int(cols) - settings.BUFFER_WIDTH

        self.screen = Screen(self._height, self._width)
        self._keyboard = KBHit()
        se 