import os

import settings
from ball import Ball
from brick_container import BrickList
from display import Display
from game import Game
from kbhit import KBHit
from paddle import Paddle
from player import Player

r, c = os.popen("stty size", "r").read().split()
screen_height = int(r) - settings.BOTTOM_MARGIN
screen_width = int(c) - settings.RIGHT_MARGIN
display = Display(screen_height, screen_width)
kbhit = KBHit()
paddle = Paddle(screen_height, screen_width)
ball = Ball(screen_height, paddle.y, paddle.width)
brick_container = BrickList(screen_width)
name = "Aditya"
player = Player(name=name)
game = Game(display, kbhit, ball, paddle, brick_container, player)
game.mainloop()
