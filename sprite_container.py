from abc import ABC, abstractmethod


class SpriteList(ABC):
    """
    A container for sprites.
    """

    def __init__(self):
        self.sprites = []

    def add(self, sprite):
        """
        Add a sprite to the container.
        """
        self.sprites.append(sprite)

    def remove(self, sprite):
        """
        Remove a sprite from the container.
        """
        self.sprites.remove(sprite)

    @abstractmethod
    def create_sprite():
        pass

    @abstractmethod
    def update(self):
        pass
