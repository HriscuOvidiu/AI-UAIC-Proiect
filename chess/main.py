from chess.game.ChessGame import ChessGame
from chess.game.Config import Config


def get_board():
    chess_config = Config("./static/configs/standard_chess_cfg.json")
    chess = ChessGame(chess_config)
    return chess.render()


if __name__ == '__main__':
    print(get_board())
