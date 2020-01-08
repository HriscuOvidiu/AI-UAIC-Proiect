from abc import ABCMeta


class Player(metaclass=ABCMeta):

    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    def __repr__(self):
        return f"color: {self.color}"
