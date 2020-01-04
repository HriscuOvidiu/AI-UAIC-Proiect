import json

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

    # TODO: moves !!!
    def get_white_pieces(self):
        pieces = self.config_dict["pieces"]
        pieces_dict = {}

        for piece_type in pieces:
            chess_piece = ChessPieceFactory.get_type(piece_type)

            piece_valid_moves = pieces[piece_type]["valid_moves"]
            for position in pieces[piece_type]["white"]:
                pieces_dict[tuple(position)] = chess_piece("w", piece_valid_moves)

        return pieces_dict

    # TODO: moves !!!
    def get_black_pieces(self):
        pieces = self.config_dict["pieces"]
        pieces_dict = {}

        for piece_type in pieces:
            chess_piece = ChessPieceFactory.get_type(piece_type)

            piece_valid_moves = pieces[piece_type]["valid_moves"]
            for position in pieces[piece_type]["black"]:
                pieces_dict[tuple(position)] = chess_piece("b", piece_valid_moves)

        return pieces_dict

    def get_capturing_condition(self):
        pass

    def get_end_condition(self):
        pass
