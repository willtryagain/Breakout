import numpy as np


class Meta:
    '''
    -----> Y
    |
    |
    v 
    X 

    '''
    def __init__(self, game_height, game_width, pos, size, ascii):

        self._gh = game_height
        self._gw = game_width

        self._pos = pos
        self._size = size
        self._ascii = ascii
    
    def get_pos(self):
        return self._pos

    def get_tail(self):
        x0 = self._pos[0]
        y0 = self._pos[1]
        return [x0 + self._size[0] - 1, y0 + self._size[1] - 1]

    def get_ascii(self):
        return self._ascii

    def draw(self):
        """
        """
        pass

    def side_walls_collide(self):
        """
        check if object collided with the side walls 
        """
        left_ball = self._pos[1]
        right_ball = self._pos[1] + self._size[1] - 1

        left_wall = 0
        right_wall = self._gw - 1

        # hits the side walls
        if left_ball == left_wall or right_wall == right_ball:
            return True
        
        return False

    def top_collide(self):
        """
        check if ball collided with the top wall
        """
        top_ball = self._pos[0]
        top_wall = 0

        if top_ball == top_wall:
            return True

        return False
    
    def lost(self):   
        bottom_ball = self._pos[0] + self._size[0]
        bottom_display = self._gh 
        
        return bottom_ball >= bottom_display