from abc import ABCMeta


class Player(metaclass=ABCMeta):

    def __init__(self, color, pieces):
        self._color = color
        self._pieces = pieces

    @property
    def color(self):
        return self._color

    @property
    def pieces(self):
        return self._pieces

    def __repr__(self):
        return f"color: {self.color}, pieces: {self.pieces}"
