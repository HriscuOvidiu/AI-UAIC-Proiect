from chess.pieces.ChessPiece import ChessPiece


class Cell:

    def __init__(self, position, chess_piece=None):
        self._position = position
        self._chess_piece = chess_piece

    @property
    def position(self):
        return self._position

    @property
    def chess_piece(self):
        return self._chess_piece

    @chess_piece.setter
    def chess_piece(self, cp):
        if isinstance(cp, ChessPiece) or cp is None:
            self._chess_piece = cp
        else:
            raise AttributeError("[chess_piece] Invalid type for <cp>")

    @chess_piece.getter
    def chess_piece(self):
        return self._chess_piece

    def is_empty(self):
        return True if self._chess_piece is None else False

    def get_symbol(self):
        return self.chess_piece.alias if self.chess_piece else ""

    def __repr__(self):
        return f"{self.__class__.__name__}(position: {self.position}, chess_piece: {self.chess_piece})"
