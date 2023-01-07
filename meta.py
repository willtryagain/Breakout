'''
Defines the Meta class
'''
from typing import List

import numpy.typing as npt


class Meta:
    '''

    The Meta class is responsible for storing the coordinates and ascii
    representation of objects (for e.g. ball, paddle etc). It forms a backbone
    of all the object classes visible on the screen.

    The following directions are considered as X and Y.

    -----> Y
    |
    |
    v
    X

    '''

    def __init__(
        self,
        game_height : int,
        game_width : int,
        pos : List[int, int],
        size : int,
        ascii_arr : npt.ArrayLike
    ):
        self._gh = game_height
        self._gw = game_width
        self._pos = pos
        self._size = size
        self._ascii = ascii_arr

    def get_pos(self):
        """
        Returns coordinates of current object (x, y)
        """
        return self._pos

    def get_tail(self):
        """
        Returns the bottom-right coordinate of the object.
        """
        x_0 = self._pos[0]
        y_0 = self._pos[1]
        return [x_0 + self._size[0] - 1, y_0 + self._size[1] - 1]

    def get_ascii(self):
        """
        Returns the ascii representation of the object.
        """
        return self._ascii
