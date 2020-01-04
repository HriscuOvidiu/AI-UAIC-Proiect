from abc import ABCMeta


class ChessPiece(metaclass=ABCMeta):

    symbols = {"wPawn":     "pawn-white",
               "bPawn":     "pawn-black",
               "wRook":     "rook-white",
               "bRook":     "rook-black",
               "wKnight":   "knight-white",
               "bKnight":   "knight-black",
               "wBishop":   "bishop-white",
               "bBishop":   "bishop-black",
               "wKing":     "king-white",
               "bKing":     "king-black",
               "wQueen":    "queen-white",
               "bQueen":    "queen-black"}

    def __init__(self, name, color, get_valid_moves=None):
        self._name = name
        self._alias = ChessPiece.symbols[color + name]
        self._color = color
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
    def get_valid_moves(self):
        return self._get_valid_moves

    @get_valid_moves.setter
    def get_valid_moves(self, func):
        self._get_valid_moves = func

    def __repr__(self):
        return f"name: {self.name}, alias: {self.alias}, color: {self.color}"
