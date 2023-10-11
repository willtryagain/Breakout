import numpy as np


class Sprite:
    """
    -----> Y
    |
    |
    v
    X

    """

    def __init__(self, pos, size, ascii):
        self._pos = pos
        self._size = size
        self._ascii = ascii

    def get_pos(self):
        return self._pos

    def get_tail(self):
        x0 = self._pos[0]
        y0 = self._pos[1]
        return [x0 + self._size[0] - 1, y0 + self._size[1] - 1]

    def get_ascii(self):
        return self._ascii

    def draw(self):
        """ """
        pass
