from random import choice, randint, random

from icecream import ic

import settings
from brick import Brick
from sprite_container import SpriteList


class BrickList(SpriteList):
    def __init__(self, width):
        super().__init__()
        x0 = settings.BRICK_START_ROW
        y0 = width // 2
        h = 1
        w = 5
        level = y0 // 8

        for i in range(level):
            for j in range(-i, i + 1):
                brick = self.create_sprite(x0 + i * h, y0 + j * w)
                self.add(brick)

        for j in range(
            -level - settings.BRICK_LENGTH, level + settings.BRICK_LENGTH + 1
        ):
            if y0 + j * w >= width or y0 + j * w < 0:
                continue
            brick = self.create_sprite(x0 + level * h, y0 + j * w)
            self.add(brick)

        for i in range(level - 1, -1, -1):
            for j in range(-i, i + 1):
                brick = self.create_sprite(x0 + (level + level - i) * h, y0 + j * w)
                self.add(brick)

    def create_sprite(self, x, y, color=None):
        if color is None:
            # todo: add inf
            color = choice([1, 2, 3])
        return Brick(x, y, color)

    def update(self):
        return super().update()
