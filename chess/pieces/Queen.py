from chess.pieces.ChessPiece import ChessPiece


class Queen(ChessPiece):

    def __init__(self, color, moves):
        super(Queen, self).__init__(self.__class__.__name__, color, moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(Queen, self).__repr__()})"
