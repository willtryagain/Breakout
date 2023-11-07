from time import sleep

import numpy as np
from colorama import Back, Fore, Style


class Display:
    START = "\033[0;0H"
    ERASE = "\033[2J"

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self._back = np.array(
            [[Back.BLACK for j in range(self.width)] for i in range(self.height)],
            dtype="object",
        )
        self._canvas = np.array(
            [[" " for j in range(self.width)] for i in range(self.height)],
            dtype="object",
        )

    def __repr__(self) -> str:
        return f"Display({self.height}, {self.width})"

    def get_text(self, path="rip.txt"):
        text = []
        try:
            with open(path, "r") as f:
                for line in f:
                    text.append([line.strip("\n")])
        except FileNotFoundError as e:
            print(e)
        return np.array(text, dtype="object")

    def put(self, item):
        x = max(item.x, 0)
        x = min(x, self.height - item.height)
        y = max(item.y, 0)
        y = min(y, self.width - item.width)
        item.draw(self._canvas)

    def clrscr(self):
        for i in range(self.height):
            for j in range(self.width):
                self._canvas[i][j] = " "

    def alert(self, color=Fore.RED):
        rip = self.get_text()
        if rip is None:
            return
        print(self.START)
        print(color, end="")
        for i in range(rip.shape[0]):
            for j in range(rip.shape[1]):
                print(rip[i][j], end="")
            print("")
        sleep(2)
        print(Style.RESET_ALL + self.ERASE + self.START + "\n")

    def show(self):
        """
        Show the canvas on the terminal
        """
        # ANSI escape for resetting screen point to top
        print("\033[0;0H")

        for i in range(self.height):
            for j in range(self.width):
                print(self._back[i][j] + self._canvas[i][j], end="")
            print()  # next line

    def end_game(self, player):
        print(Style.RESET_ALL + self.ERASE + self.START + "\n" * 3)
        # arr = []
        # try:
        #     with open(path, 'r') as f:
        #         for line in f:
        #             arr.append(list(line.strip('\n')))
        # except FileNotFoundError as e:
        #     return None

        # return np.array(arr, dtype='object')
        # ascii =

    def colored(self, x, y):
        return self._canvas[x][y] != " "
