import json

from chess.game.ChessGame import ChessGame
from chess.game.Config import Config


with open('./static/configs/game_modes.json') as f:
    rules_dict = json.load(f)

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

def get_chess_game(setup_dict):
    setup = get_setup(setup_dict)
    chess_config = Config(setup[0])
    chess = ChessGame(chess_config, None)

    return chess

def positions_to_frontend(game, line, column):
    positions = game.get_valid_positions(line, column)
    if len(positions):
        positions_l = [[position.line, position.column] for position in positions]

        return zip(*positions_l)
    return [], []

