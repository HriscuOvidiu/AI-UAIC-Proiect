from chess.game.ChessGame import ChessGame
from chess.game.Config import Config
import json


rules_dict = {
                0: "./static/configs/standard_chess_cfg.json", 
                1: "./static/configs/weak_chess_cfg.json",
                2: "./static/configs/endgame_chess_cfg.json"
            }

game_type_dict = {
                    0: "pvc",
                    1: "cvc"
                }

ai_modes_dict = {
                    -1:     None,
                    0:      "minimax",
                    1:      "alpha_beta_prunning",
                    2:      "reinforcement_learning"
                }

def get_setup(setup_dict):
    rule = rules_dict[setup_dict['rule']]
    game_type = game_type_dict[setup_dict['game-type']]
    white_player = ai_modes_dict[setup_dict['ai-type2']]
    black_player = ai_modes_dict[setup_dict['ai-type']]

    return rule, game_type, white_player, black_player

def get_board(setup_dict):
    setup = get_setup(setup_dict)
    chess_config = Config(setup[0])
    chess = ChessGame(chess_config)
    return chess.render()


if __name__ == '__main__':
    print(get_board())
