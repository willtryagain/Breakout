from meta import Meta

class Powerup(Meta):
    def __init__(self, pos, ascii, start_time):
        self._pos = pos
        self._ascii = ascii
        self._start_time = start_time

    