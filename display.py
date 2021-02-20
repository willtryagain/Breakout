import numpy as np
from colorama import Fore, Back, Style

class Display:

    START = '\033[0;0H'
    ERASE = '\033[2J'

    def __init__(self, height, width):
        self._height = height
        self._width = width
        self._back = np.array([
            [Back.BLACK for j in range(self._width)] 
            for i in range(self._height)
            ], dtype='object'
        )
        self._canvas = np.array([
            [' ' for j in range(self._width)] 
            for i in range(self._height)
            ], dtype='object'
        )
       
    def put(self, item):
        pos = item.get_pos()
        tail = item.get_tail()
        ascii = item.get_ascii()
        try:
            self._canvas[ pos[0]: tail[0] + 1, pos[1]: tail[1] + 1] = ascii
        except (IndexError, ValueError) as e:
            print(e)

    def clrscr(self):
        for i in range(self._height):
            for j in range(self._width):
                self._canvas[i][j] = ' '

    def show(self):
        """
        Show the canvas on the terminal
        """
        # ANSI escape for resetting screen point to top  
        print('\033[0;0H')

        for i in range(self._height):
            for j in range(self._width):
                print(self._back[i][j] + self._canvas[i][j], end='')
            print() #next line
    
    def end_game(self, player):
        print(Style.RESET_ALL + self.ERASE + self.START + '\n'*3)
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
        return self._canvas[x][y] != ' '

            