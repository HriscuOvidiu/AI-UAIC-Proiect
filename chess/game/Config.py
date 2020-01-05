import json

from chess.rules.chess_rules import rules_func_dict
from chess.pieces.ChessPieceFactory import ChessPieceFactory


class Config:

    def __init__(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                self._config_dict = json.load(config_file)
        except IOError:
            print("[ERROR]: Config file unable to open!")

    @property
    def config_dict(self):
        return self._config_dict

    def get_board_lines(self):
        return self.config_dict["board"]["lines"]

    def get_board_columns(self):
        return self.config_dict["board"]["columns"]

    def get_white_pieces(self):
        pieces = self.config_dict["pieces"]
        pieces_dict = {}

        for piece_type in pieces:
            chess_piece = ChessPieceFactory.get_type(piece_type)

            # TODO: moves !!!
            piece_valid_moves = pieces[piece_type]["valid_moves"]

            try:
                valid_moves_func = rules_func_dict[piece_valid_moves]
            except:
                valid_moves_func = None
                print(f"No available 'valid_move_func' for {piece_type}")

            try:
                for position in pieces[piece_type]["white"]:
                    pieces_dict[tuple(position)] = chess_piece("w", valid_moves_func)
            except:
                print(f"White piece not found for {piece_type}")

        return pieces_dict

    def get_black_pieces(self):
        pieces = self.config_dict["pieces"]
        pieces_dict = {}

        for piece_type in pieces:
            chess_piece = ChessPieceFactory.get_type(piece_type)

            # TODO: moves !!!
            piece_valid_moves = pieces[piece_type]["valid_moves"]

            try:
                valid_moves_func = rules_func_dict[piece_valid_moves]
            except:
                valid_moves_func = None
                print(f"No available 'valid_move_func' for {piece_type}")

            try:
                for position in pieces[piece_type]["black"]:
                    pieces_dict[tuple(position)] = chess_piece("b", valid_moves_func)
            except Exception:
                print(f"Black piece not found for {piece_type}")

        return pieces_dict

    def get_capturing_condition(self):
        func_name = self.config_dict['capturing_condition']
        return rules_func_dict[func_name]

    def get_end_condition(self):
        func_name = self.config_dict['game_over']
        return rules_func_dict[func_name]
