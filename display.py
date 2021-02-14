import numpy as np
from colorama import Fore, Back, Style

class Display:

    BEGIN = '\033[0;0H'

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
       

    def put(self, ball):
        pos = ball.get_pos()
        tail = ball.get_tail()
        ascii = ball.get_ascii()
       
        try:
            self._canvas[ pos[0]: tail[0] + 1, pos[1]: tail[1] + 1] = ascii
            # for i in range(pos[0], tail[0] + 1):
            #     for j in range(pos[1], tail[1] + 1):
            #         self._canvas[i][j] = ascii[i - pos[0]][j - pos[1]]
        except (IndexError, ValueError) as e:
            print(e)


    def clrscr(self):
        for i in range(self._height):
            for j in range(self._width):
                self._canvas[i][j] = ' '


    def show(self):
        print(self.BEGIN)

        for i in range(self._height):
            for j in range(self._width):
                print(self._back[i][j] + self._canvas[i][j], end='')
            print() #next line
        pass    

            