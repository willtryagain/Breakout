import os

import settings
from game import Game
from display import Display
from player import Player
from keyboard import KBHit
from paddle import Paddle
from ball import Ball


r, c = os.popen("stty size", "r").read().split()
screen_height = int(r) - settings.TOP_MARGIN
screen_width = int(c) - settings.LEFT_MARGIN
height = int(r) - settings.BOTTOM_MARGIN

IO = {
    "display": Display(screen_height, screen_width),
    "keyboard": KBHit(),
}


# sprites
StopAsynprites = {
    "paddle": Paddle(self.height, self.width),
    "ball": Ball(self.height, self._paddle.y, self._paddle.width),
    "bricks": self.get_brick_pattern(),
    "powerups": [],
}

player = Player()
game = Game(IO, player)
game.mainloop()
