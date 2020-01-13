import json

from chess.game.ChessGame import ChessGame
from chess.game.Config import Config
from copy import deepcopy


with open('./static/configs/game_modes.json') as f:
    rules_dict = json.load(f)

game_type_dict = {
                    0: "pvc",
                    1: "cvc",
                    2: "pvp"
                }

ai_modes_dict = {
                    -1:     None,
                    0:      "minimax",
                    1:      "reinforcement_learning",
                    2:      "alpha_beta_pruning"
                }

def get_setup(setup_dict):
    rule = rules_dict[setup_dict['rule']]
    game_type = game_type_dict[setup_dict['game-type']]
    white_player = ai_modes_dict[setup_dict['second-ai-type']]
    black_player = ai_modes_dict[setup_dict['ai-type']]

    return rule, game_type, white_player, black_player

def get_chess_game(setup_dict):
    setup = get_setup(setup_dict)
    chess_config = Config(setup[0])
    chess = ChessGame(chess_config, None)

    return chess

def get_valid_positions_check(chess: ChessGame, start_line, start_column, end_position_list):
    positions = []

    aux_state = deepcopy(chess.current_state)
    
    for end_position in end_position_list:
        chess.move_piece(start_line, start_column, end_position.line, end_position.column)
        if chess.has_finished() == 0:
            positions.append(end_position)
        chess.current_state = deepcopy(aux_state)

    return positions

def positions_to_frontend(game, line, column):
    positions = game.get_valid_positions(line, column)
    # print(game.get_next_moves())
    if positions:
        # TODO: Check if OK
        positions = get_valid_positions_check(deepcopy(game), line, column, positions)
        #
        
        if len(positions):
            positions_l = [[position.line, position.column] for position in positions]

            return zip(*positions_l)
    return [], []

