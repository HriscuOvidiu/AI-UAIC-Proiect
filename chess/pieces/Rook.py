from chess.pieces.ChessPiece import ChessPiece


class Rook(ChessPiece):

    def __init__(self, color, moves):
        super(Rook, self).__init__(self.__class__.__name__, color, moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(Rook, self).__repr__()})"
