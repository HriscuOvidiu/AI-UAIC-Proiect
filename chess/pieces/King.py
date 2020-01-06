from chess.pieces.ChessPiece import ChessPiece


class King(ChessPiece):

    def __init__(self, color, initial_position, get_valid_moves):
        super(King, self).__init__(self.__class__.__name__, color, initial_position, get_valid_moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(King, self).__repr__()})"
