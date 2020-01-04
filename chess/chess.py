from abc import ABCMeta
import json


class ChessPiece(metaclass=ABCMeta):

    symbols = {"wPawn":     "pawn-white",
               "bPawn":     "pawn-black",
               "wRook":     "rook-white",
               "bRook":     "rook-black",
               "wKnight":   "knight-white",
               "bKnight":   "knight-black",
               "wBishop":   "bishop-white",
               "bBishop":   "bishop-black",
               "wKing":     "king-white",
               "bKing":     "king-black",
               "wQueen":    "queen-white",
               "bQueen":    "queen-black"}

    def __init__(self, name, color, get_valid_moves=None):
        self._name = name
        self._alias = ChessPiece.symbols[color + name]
        self._color = color
        self._get_valid_moves = get_valid_moves

    @property
    def name(self):
        return self._name

    @property
    def alias(self):
        return self._alias

    @property
    def color(self):
        return self._color

    @property
    def get_valid_moves(self):
        return self._get_valid_moves

    @get_valid_moves.setter
    def get_valid_moves(self, func):
        self._get_valid_moves = func

    def __repr__(self):
        return f"name: {self.name}, alias: {self.alias}, color: {self.color}"


class Pawn(ChessPiece):

    def __init__(self, color, moves):
        super(Pawn, self).__init__(self.__class__.__name__, color, moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(Pawn, self).__repr__()})"


class Rook(ChessPiece):

    def __init__(self, color, moves):
        super(Rook, self).__init__(self.__class__.__name__, color, moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(Rook, self).__repr__()})"


class Knight(ChessPiece):

    def __init__(self, color, moves):
        super(Knight, self).__init__(self.__class__.__name__, color, moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(Knight, self).__repr__()})"


class Bishop(ChessPiece):

    def __init__(self, color, moves):
        super(Bishop, self).__init__(self.__class__.__name__, color, moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(Bishop, self).__repr__()})"


class King(ChessPiece):

    def __init__(self, color, moves):
        super(King, self).__init__(self.__class__.__name__, color, moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(King, self).__repr__()})"


class Queen(ChessPiece):

    def __init__(self, color, moves):
        super(Queen, self).__init__(self.__class__.__name__, color, moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(Queen, self).__repr__()})"


class Player(metaclass=ABCMeta):

    def __init__(self, color, pieces):
        self._color = color
        self._pieces = pieces

    @property
    def color(self):
        return self._color

    @property
    def pieces(self):
        return self._pieces

    def __repr__(self):
        return f"color: {self.color}, pieces: {self.pieces}"


class WhitePlayer(Player):

    def __init__(self, white_pieces):
        super(WhitePlayer, self).__init__("w", white_pieces)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(WhitePlayer, self).__repr__()})"


class BlackPlayer(Player):

    def __init__(self, black_pieces):
        super(BlackPlayer, self).__init__("b", black_pieces)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(BlackPlayer, self).__repr__()})"


class Position:

    def __init__(self, line, column):
        self._line = line
        self._column = column

    @property
    def line(self):
        return self._line

    @property
    def column(self):
        return self._column

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.line + other.line, self.column + other.column)
        raise TypeError

    def __repr__(self):
        return f"{self.__class__.__name__}(line: {self.line}, column: {self.column})"


class Cell:

    def __init__(self, position, chess_piece=None):
        self._position = position
        self._chess_piece = chess_piece

    @property
    def position(self):
        return self._position

    @property
    def chess_piece(self):
        return self._chess_piece

    def _is_empty(self):
        return False if self._chess_piece else True

    def get_symbol(self):
        return self.chess_piece.alias if self.chess_piece else ""

    def __repr__(self):
        return f"{self.__class__.__name__}(position: {self.position}, chess_piece: {self.chess_piece})"


class ChessBoard:

    def __init__(self, config):
        self._config = config
        self._board = self._init()

    @property
    def config(self):
        return self._config

    @property
    def board(self):
        return self._board

    def _init(self):
        lines = self._config.get_board_lines()
        columns = self._config.get_board_columns()

        whites = self.config.get_white_pieces()
        blacks = self.config.get_black_pieces()

        board = []
        for i in range(lines):
            line = []
            for j in range(columns):
                piece = None

                if (i, j) in whites:
                    piece = whites[(i, j)]

                if (i, j) in blacks:
                    piece = blacks[(i, j)]

                cell = Cell(Position(i, j), chess_piece=piece)
                line.append(cell)
            board.append(line)

        return board

    def get_cell_by(self, line, column):
        return self.board[line][column]

    def reset(self):
        pass

    def move(self, start_position, end_position):
        pass

    def get_rendered_board(self):
        lines = self.config.get_board_lines()
        columns = self.config.get_board_columns()
        return [[self.board[i][j].get_symbol() for j in range(columns)] for i in range(lines)]


# TODO Singleton
class ChessPieceFactory:

    _types = {"pawn": Pawn,
              "rook": Rook,
              "knight": Knight,
              "bishop": Bishop,
              "king": King,
              "queen": Queen}

    @staticmethod
    def get_type(piece_type):
        return ChessPieceFactory._types[piece_type]


class Config:

    # TODO Configuration: value strings == function names

    def __init__(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                self._config = json.load(config_file)
        except IOError:
            print("[ERROR]: Config file unable to open!")

    @property
    def config(self):
        return self._config

    def get_board_lines(self):
        return self.config["board"]["lines"]

    def get_board_columns(self):
        return self.config["board"]["columns"]

    def get_pawn_valid_moves_func(self):
        pass

    # TODO: moves !!!
    def get_white_pieces(self):
        pieces = self.config["pieces"]
        pieces_dict = {}

        for piece_type in pieces:
            chess_piece = ChessPieceFactory.get_type(piece_type)

            piece_valid_moves = pieces[piece_type]["valid_moves"]
            for position in pieces[piece_type]["white"]:
                pieces_dict[tuple(position)] = chess_piece(
                    "w", piece_valid_moves)

        return pieces_dict

    # TODO: moves !!!
    def get_black_pieces(self):
        pieces = self.config["pieces"]
        pieces_dict = {}

        for piece_type in pieces:
            chess_piece = ChessPieceFactory.get_type(piece_type)

            piece_valid_moves = pieces[piece_type]["valid_moves"]
            for position in pieces[piece_type]["black"]:
                pieces_dict[tuple(position)] = chess_piece(
                    "b", piece_valid_moves)

        return pieces_dict

    def get_capturing_condition(self):
        pass

    def get_end_condition(self):
        pass


class ChessState:

    def __init__(self, starting_player, chess_board):
        self._current_player = starting_player
        self._board = chess_board

    @property
    def current_player(self):
        return self._current_player

    @property
    def board(self):
        return self._board

    def is_valid(self):
        pass

    def is_final_state(self):
        pass


class ChessGame:

    def __init__(self, configuration):
        self._config = configuration
        self._white = WhitePlayer(None)
        self._black = BlackPlayer(None)
        self._init_state = ChessState(self._white, ChessBoard(self._config))
        self._current_state = self._init_state

    @property
    def config(self):
        return self._config

    @property
    def white(self):
        return self._white

    @property
    def black(self):
        return self._black

    @property
    def init_state(self):
        return self._init_state

    @property
    def current_state(self):
        return self._current_state

    def reset_game(self):
        self._current_state = self._init_state

    @staticmethod
    def get_valid_cells(start_cell: Cell):
        pass

    # TODO: RETURN REWARD
    def move(self, start_cell, end_cell):
        pass

    def has_finished(self):
        return self.current_state.is_final_state()

    def render(self):
        return self.current_state.board.get_rendered_board()


def get_board():
    chess_config = Config("./static/configs/standard_chess_cfg.json")
    chess = ChessGame(chess_config)
    return chess.render()


if __name__ == '__main__':
    print(get_board())
