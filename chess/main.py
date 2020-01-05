from chess.game.ChessGame import ChessGame
from chess.game.Config import Config
import json


game_dict = {
                0: "./static/configs/standard_chess_cfg.json", 
                1: "./static/configs/weak_chess_cfg.json",
                2: "./static/configs/endgame_chess_cfg.json"
            }

ai_modes =  {
                -1: None,
                0: "minimax",
                1: "alpha_beta_prunning",
                2: "reinforcement_learning"
            }

def setup(setup_json):
    pass

def get_board():
    chess_config = Config("./static/configs/standard_chess_cfg.json")
    chess = ChessGame(chess_config)
    return chess.render()


if __name__ == '__main__':
    print(get_board())
