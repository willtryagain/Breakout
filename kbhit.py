import os
import sys
import termios
import atexit
from select import select

class KBHit:

        def __init__(self):
            self._fd = sys.stdin.fileno()
            self._prev_term = termios.tcgetattr(self._fd)
            self._next_term = termios.tcgetattr(self._fd)

            self._next_term[3] = (self._next_term[3] & ~termios.ICANON 
                                  & termios.ECHO)

            termios.tcsetattr(self._fd, termios.TCSAFLUSH, self._next_term)

            atexit.register(self.set_normal_term)

        def set_normal_term(self):
            '''
            reset to normal terminal
            '''
            termios.tcsetattr(self._fd, termios.TCSAFLUSH, self._prev_term)

        def getch(self):
            '''

            '''
            return sys.stdin.read(1)

        def kbhit(self):
            '''
            Determine whether character was keyboard 
            on keyboard
            '''
            dr, dw, de = select([sys.stdin], [], [], 0)
            return dr != []

        def flush(self):
            '''
            clear input buffer
            '''
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)


    