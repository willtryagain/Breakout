class Player:
    def __init__(self, lives=3, score=0):
        self._lives = lives
        self._score = score

    def lose_life(self):
        self._lives -= 1
        print(self._lives)