from chess.pieces.ChessPiece import ChessPiece


class Bishop(ChessPiece):

    def __init__(self, color, initial_position, get_valid_moves):
        super(Bishop, self).__init__(self.__class__.__name__, color, initial_position, get_valid_moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(Bishop, self).__repr__()})"
