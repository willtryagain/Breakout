from powerup import Powerup
import numpy as np
from colorama import Fore, Back, Style


class Fastball(Powerup):
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)
        self._ascii = np.array(
            [Back.BLUE + 'F', 
            Back.BLUE + 'B'], 
            dtype='object').reshape(1, -1)

    def magic(self, ball):
        vx = ball._velocity.getvx()
        vy = ball._velocity.getvy()

        vx = self.inc_mag(vx, 5)
        vy = self.inc_mag(vy, 5)

        ball._velocity.setvx(vx)
        ball._velocity.setvy(vy)
        return ball

    def reverse(self, ball):
        vx = ball._velocity.getvx()
        vy = ball._velocity.getvy()

        vx = self.inc_mag(vx, -2)
        vy = self.inc_mag(vy, -2)

        ball._velocity.setvx(vx)
        ball._velocity.setvy(vy)
        return ball