import logging
import os

import settings
from ball import Ball
from brick_container import BrickList
from collisions import BoundaryCollisionHandler, PaddleCollisionHandler
from display import Display
from game import Game
from kbhit import KBHit
from paddle import Paddle
from player import Player

logging.basicConfig(filename="bb.log", level=logging.DEBUG, filemode="w")
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
paddle_handler = PaddleCollisionHandler()
boundary_handler = BoundaryCollisionHandler()
paddle_handler.set_next(boundary_handler)
game = Game(display, kbhit, ball, paddle, brick_container, paddle_handler, player)
game.mainloop()
