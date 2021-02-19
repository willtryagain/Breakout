from powerup import Powerup

class Expand(Powerup):
    """
    Increases the size of the paddle by a certain amount.
    """
    def __init__(self, game_height, game_width, pos, start_time):
        super().__init__(game_height, game_width, pos, start_time)

    def magic(self):
        pass