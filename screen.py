import os
import numpy as np
from colorama import init 
from colorama import Fore, Back, Style
import random
import time

import settings
import utils


class Screen:

    CURSOR_START = '\033[0;0H'
    CLEAR = '\033[2J'

    def __init__(self, height, width):
        self._height = height
        self._width = width

        self._back_board = np.array([[settings.BG_COLOR for j in range(self._width)] for i in range(self._height)], dtype='object')
        for i in range(self._height):
            for j in range(self._width):
                if random.random() < settings.ACCENT_AMT:
                    self._back_board[i][j] = settings.BG_ACCENT_COLOR

        for i in range(settings.FG_DEPTH):
            for j in range(self._width):
                self._back_board[i][j] = settings.FG_COLOR

        self._fore_board = np.array([[' ' for j in range(self._width)] for i in range(self._height)], dtype='object')


    def reset_fg(self):
        '''
        clear the foreground
        '''

        for i in range(settings.FG_DEPTH):
            for j in range(self._width):
                self._back_board[i][j] = ' '

    def add(self, obj):
        '''
        obj is added to screen
        '''

        if True in obj.is_out():
            return

        pos, size, front = obj.show()

        x_start = pos[0]
        x_start_ = 0
        x_end = pos[0] + size[0]
        x_end_ = size[0]
        y_start = pos[1]
        y_start_ = 0
        y_end = pos[1] + size[1]
        y_end_ = size[1]

        if x_start < 0:
            x_start_ = 0 - x_start
            x_start = 0

        if y_start < 0:
            y_start_ = 0 - y_start
            y_start = 0

        if x_end > self._height:
            x_end_ = self._height - pos[0]
            x_end = self._height
        
        if y_end > self._width:
            y_end_ = self._width - pos[1]
            y_end = self._width

        try:
            self._fore_board[x_start:x_end, y_start:y_end] = front[x_start:x_end_, y_start_:y_end_]
        except (IndexError, ValueError):
            return

    def print_board(self, frame_count):
        print(self.CURSOR_START)

        for i in range(self._height):
            for j in range(self._width):
                print(self._back_board[i][(j + frame_count) % self._width] + self._fore_board[i][j], end='')
            print('')

    def flash(self, color, frame_count, times=3):
        
        arr = np.array([[color for j in range(self._width)] for i in range(self._height)], dtype='object')
        for _ in range(times):
            print(self.CURSOR_START) 
            for i in range(self._height):
                for j in range(self._width):
                    print(arr[i][j], end='')
                print('')
            time.sleep(0.1)
            self.print_board(frame_count)
            time.sleep(0.2)

    def end_game(self, lost):
        print(Style.RESET_ALL + self.CLEAR + self.CURSOR_START + '\n\n\n')

        if not lost:
            pass
        game_over_art = utils.get_design('game-over.txt')
        if game_over_art is not None:
            print(Fore.GREEN, end='')
            for i in range(game_over_art.shape[0]):
                for j in range(game_over_art.shape[1]):
                    print(game_over_art[i][j], end='')
                print('')
     
        print('\n\n', end='')

        if not lost:
            print(Style.BRIGHT + Fore.GREEN + 'YOU WON!')
        else:
            print(Style.BRIGHT + Fore.RED + 'YOU LOST!')

        print('\n\n', end='')

        print(Style.DIM + '\nPress E to exit')
        print(Style.RESET_ALL)