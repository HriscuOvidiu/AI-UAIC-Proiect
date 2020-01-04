from chess.pieces.ChessPiece import ChessPiece


class Knight(ChessPiece):

    def __init__(self, color, moves):
        super(Knight, self).__init__(self.__class__.__name__, color, moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(Knight, self).__repr__()})"
