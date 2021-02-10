import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock
import random
import math

import settings
import elements

def intersect(a, b):
    '''
    determine the intersection between the rectangles a and b
    '''

    if type(a) != list or type(b) != list or len(a) != 4 or len(b) != 4:
        raise ValueError

    x0 = max(a[0], b[0])
    x1 = min(a[1], b[1])
    y0 = max(a[2], b[2])
    y1 = min(a[3], b[3])

    if x0 > x1 or y0 > y1:
        return False, [0, 0, 0, 0]
    
    return True, [x0, x1, y0, y1]

def get_design(path):
    '''
    read the template and return np array
    '''
    
    path = os.path.join(settings.DESIGN_BASE_PATH, path)
    arr = []
    try:
        with open(path, 'r') as f:
            for line in f:
                arr.append([line.strip('\n')])
    except FileNotFoundError:
        return None

    return np.array(arr, dtype='object')

def make_brick_group(window_height, window_width, x=0, y=0, h=1, w=1):
    bricks = []
    for i in range(h):
        draw = False
        for j in range(w):
            if not draw:
                if random.random() < 0.65:
                    draw = True
            if draw:
                bricks.append(elements.Brick(window_height, window_width, x+i, y+i))
                if random.random() < 0.3:
                    draw = False
                    break
    return bricks

def get_components(magnitude, start, end):
    '''
    get 2D components of a vector
    '''

    if type(start) != np.ndarray or type(end) != np.ndarray:
        raise ValueError
    
    x = abs(start[0] - end[0])
    y = abs(start[1] - end[1])
            
    theta = math.atan2(x, y)
    x_c = abs(magnitude * math.sin(theta))
    y_c = abs(magnitude * math.cos(theta))

    if end[0] < start[0]:
        x_c = -x_c

    if end[1] < start[1]:
        y_c = -y_c

    return [x_c, y_c]

def get_loading_bar(length, left, total):
    '''
    '''
    if left >= total:
        return Style.BRIGHT + Back.RED + (' ' * length) 
    if left <= 0:
        return Style.BRIGHT + Back.GREEN + (' ' * length) 
    p = int(round(left / total) * length)
    s = Style.BRIGHT + Back.RED + (' ' * p) 
    s += Back.GREEN + (' ' * (length - p)) 
    return s