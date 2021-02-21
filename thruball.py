from powerup import Powerup
import numpy as np
from colorama import Fore, Back, Style

class Thruball(Powerup):
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)
        self._ascii = np.array(
            [Back.BLUE + 'T', 
            Back.BLUE + 'B'], 
            dtype='object').reshape(1, -1) 
        self._kind = 'thruball'

    def magic(self, balls):
        """
        expand the paddle
        """
        new_balls = []
        for ball in balls:
            ball._thru = True
            new_balls.append(ball)
        return new_balls

    def reverse(self, balls):
        """
        deactivate the powerup
        """
        self._state = 'DELETE'
        new_balls = []
        for ball in balls:
            ball._thru = False
            new_balls.append(ball)
        return new_balls