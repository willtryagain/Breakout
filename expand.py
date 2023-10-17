import settings
from powerup import Powerup


class Expand(Powerup):
    """
    Increases the size of the paddle by a certain amount.
    """

    def __init__(self, pos, start_time):
        super().__init__(pos, start_time)

    def magic(self, paddle):
        """
        expand the paddle
        """
        paddle.update(settings.EXPAND_VAL)
        return paddle

    def reverse(self, paddle):
        """
        deactivate the powerup
        """
        self._state = "DELETE"
        paddle.update(-settings.EXPAND_VAL)
        return paddle
