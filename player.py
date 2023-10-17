import os
import time
from time import monotonic as clock

import numpy as np
from colorama import Back, Fore, Style


class Player:
    def __init__(
        self,
        name,
        lives=3,
        score=0,
    ):
        self._lives = lives
        self._score = score
        self.name = name
        self._start = clock()

    def lose_life(self):
        self._lives -= 1

    def display_stats(self, length, ball):
        vx = ball._velocity.vx
        vy = ball._velocity.vy

        time_passed = int(clock() - self._start)
        speed = int(np.sqrt(vx**2 + vy**2))
        print(Style.RESET_ALL + Style.BRIGHT, end="")
        print("\033[0K", end="")  # EOL
        print("SCORE:", str(self._score).rjust(1), end="\t")
        print("BALLS:", str(self._lives).rjust(1), end="\t")
        print("TIME:", str(time_passed).rjust(5), end="\t")
        print("PADDLE:", str(length).rjust(3), end="\t")
        print("SPEED", str(speed).rjust(3))

    def log_stats(self):
        time_passed = int(clock() - self._start)
        # create logs folder if it doenst exist and save scores in player.txt
        if not os.path.exists("logs"):
            os.makedirs("logs")
        with open(f"logs/{self.name}.txt", "a") as f:
            # log score , current time
            f.write(f"{self._score} {time_passed}\n")
