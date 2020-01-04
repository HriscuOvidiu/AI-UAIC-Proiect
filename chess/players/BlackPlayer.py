from chess.players.Player import Player


class BlackPlayer(Player):

    def __init__(self, black_pieces):
        super(BlackPlayer, self).__init__("b", black_pieces)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(BlackPlayer, self).__repr__()})"
