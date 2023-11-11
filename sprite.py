from typing import Any

import numpy as np
import numpy.typing as npt


class Sprite:
    """
    A basic representation of a sprite in a game.
    """

    def __init__(self, x: int, y: int, **kwargs) -> None:
        """
        Initializes a new instance of the Sprite class with the given x and y coordinates.
        Additional keyword arguments can be provided.
        """

        # check if x and y are positive integers
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("x and y must be integers")
        if x < 0 or y < 0:
            raise ValueError("x and y must be positive integers")

        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def height(self) -> int:
        """
        Returns the height of the sprite, which is the number of rows in its ASCII representation.
        """
        return len(self._ascii)

    @property
    def width(self) -> int:
        """
        Returns the width of the sprite, which is the number of columns in its ASCII representation.
        """
        return len(self._ascii[0])

    def reset_ascii(self, **kwargs) -> npt.NDArray[Any]:
        """
        Resets the ASCII representation of the sprite.
        Additional keyword arguments can be provided.
        """
        pass

    def move(self, x: int = 0, y: int = 0) -> None:
        """
        Moves the sprite by the given x and y coordinates.
        """
        self._x += x
        self._y += y

    def move_to(self, x: int, y: int) -> None:
        """
        Moves the sprite to the given x and y coordinates.
        """
        if x < 0 or y < 0:
            raise ValueError("x and y must be positive")
        self._x = x
        self._y = y

    def move_up(self, distance: int = 1) -> None:
        # check if distance is positive
        if distance < 0:
            raise ValueError("distance must be positive")
        self._x -= distance

    def move_down(self, distance: int = 1) -> None:
        if distance < 0:
            raise ValueError("distance must be positive")
        self._x += distance

    def move_left(self, distance: int = 1) -> None:
        if distance < 0:
            raise ValueError("distance must be positive")
        self._y -= distance

    def move_right(self, distance: int = 1) -> None:
        if distance < 0:
            raise ValueError("distance must be positive")
        self._y += distance

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self._x}, y={self._y}, width={self.width}, height={self.height}"

    def draw(self, canvas) -> None:
        """
        Draws the sprite on the canvas.
        """
        try:
            canvas[
                self._x : self._x + self.height, self._y : self._y + self.width
            ] = self._ascii
        except Exception as e:
            print(e)
            print(self)
