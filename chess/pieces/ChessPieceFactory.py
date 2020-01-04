from chess.pieces.Bishop import Bishop
from chess.pieces.King import King
from chess.pieces.Knight import Knight
from chess.pieces.Pawn import Pawn
from chess.pieces.Queen import Queen
from chess.pieces.Rook import Rook


# TODO Singleton
class ChessPieceFactory:

    _types = {"pawn": Pawn,
              "rook": Rook,
              "knight": Knight,
              "bishop": Bishop,
              "king": King,
              "queen": Queen}

    @staticmethod
    def get_type(piece_type):
        return ChessPieceFactory._types[piece_type]
