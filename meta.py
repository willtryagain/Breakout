'''
Defines the Meta class 
'''
from typing import NamedTuple

import numpy.typing as npt


class Position(NamedTuple):
    """
    Represents the position on X-Y axis
    
    The following directions are considered as X and Y.

    -----> Y
    |
    |
    v
    X
    
    """
    x: int
    y: int


class Velocity(NamedTuple):
    """
    Represents the speed on X-Y axis

    """
    x: int
    y: int

class Meta:
    '''
    The Meta class is responsible for storing the coordinates and ascii
    representation of objects (for e.g. ball, paddle etc). It forms a backbone
    of all the object classes visible on the screen.

    '''

    def __init__(
        self,
        game_height : int,
        game_width : int,
        pos : Position,
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

        return Position(
            self._pos.x + self._size[0] - 1,
            self._pos.y + self._size[1] - 1
        )
    
    def get_size(self):
        """Returns the size of object"""
        return self._size


    def get_ascii(self):
        """
        Returns the ascii representation of the object.
        """
        return self._ascii


if __name__ == "__main__":
    p = Position(1, 2)
    print(p.x)