from chess.players.Player import Player


class WhitePlayer(Player):

    def __init__(self, white_pieces):
        super(WhitePlayer, self).__init__("w", white_pieces)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(WhitePlayer, self).__repr__()})"
