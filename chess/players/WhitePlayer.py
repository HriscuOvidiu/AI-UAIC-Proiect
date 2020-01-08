from chess.players.Player import Player


class WhitePlayer(Player):

    def __init__(self):
        super(WhitePlayer, self).__init__("w")

    def __repr__(self):
        return f"{self.__class__.__name__}({super(WhitePlayer, self).__repr__()})"
