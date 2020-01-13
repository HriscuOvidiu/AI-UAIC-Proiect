from abc import ABCMeta
import json


class ChessPiece(metaclass=ABCMeta):

    def __init__(self, name, color, initial_position, get_valid_moves=None):
        with open('./static/configs/chess_piece_symbols.json') as f:
            symbols = json.load(f)
        self._name = name
        self._alias = symbols[color + name]
        self._color = color
        # TODO: Delete attr
        self._initial_position = initial_position
        #
        self._has_been_moved = False
        self._get_valid_moves = get_valid_moves

    @property
    def name(self):
        return self._name

    @property
    def alias(self):
        return self._alias

    @property
    def color(self):
        return self._color

    @property
    def initial_position(self):
        return self._initial_position

    @property
    def has_been_moved(self):
        return self._has_been_moved

    @property
    def get_valid_moves(self):
        return self._get_valid_moves

    @get_valid_moves.setter
    def get_valid_moves(self, func):
        self._get_valid_moves = func

    def has_moved(self):
        self._has_been_moved = True

    def __repr__(self):
        return f"name: {self.name}, alias: {self.alias}, color: {self.color}, initial_position: {self.initial_position}, get_valid_moves: {self.get_valid_moves}"

    def __str__(self):
        return self.color + self.name
