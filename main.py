import os
import numpy as np
from colorama import init 

from game import Game
import settings

init()
print('\033[2J') # clear screen
Game.start()