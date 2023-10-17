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
        self.x = x
        self.y = y

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
        self.x += x
        self.y += y

    def move_to(self, x: int, y: int) -> None:
        """
        Moves the sprite to the given x and y coordinates.
        """
        self.x = x
        self.y = y

    def move_up(self, value: int = 1) -> None:
        self.x -= value

    def move_down(self, value: int = 1) -> None:
        self.x += value

    def move_left(self, value: int = 1) -> None:
        self.y -= value

    def move_right(self, value: int = 1) -> None:
        self.y += value

    def move_x_to(self, x: int) -> None:
        self.x = x

    def move_y_to(self, y: int) -> None:
        self.y = y

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, width={self.width}, height={self.height}"

    def draw(self, canvas) -> None:
        """
        Draws the sprite on the canvas.
        """
        try:
            canvas[
                self.x : self.x + self.height, self.y : self.y + self.width
            ] = self._ascii
        except Exception as e:
            print(e)
            print(self)
