from abc import ABCMeta
import json


class ChessPiece(metaclass=ABCMeta):

    symbols = {"wPawn":     "♙",
               "bPawn":     "♟",
               "wRook":     "♖",
               "bRook":     "♜",
               "wKnight":   "♘",
               "bKnight":   "♞",
               "wBishop":   "♗",
               "bBishop":   "♝",
               "wKing":     "♕",
               "bKing":     "♚",
               "wQueen":    "♕",
               "bQueen":    "♛"}

    def __init__(self, name, color, get_valid_moves=None):
        self._name = name
        self._symbol = ChessPiece.symbols[color + name]
        self._color = color
        self._get_valid_moves = get_valid_moves

    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol

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
        return f"name: {self.name}, symbol: {self.symbol}, color: {self.color}"


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

    def __init__(self, name, color, pieces):
        self._name = name
        self._color = color
        self._pieces = pieces

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def pieces(self):
        return self._pieces

    def __repr__(self):
        return f"name: {self.name}, color: {self.color}, pieces: {self.pieces}"


class WhitePlayer(Player):

    def __init__(self, name, white_pieces):
        super(WhitePlayer, self).__init__(name, "w", white_pieces)

    def __repr__(self):
        return f"{self.__class__.__name__}({super(WhitePlayer, self).__repr__()})"


class BlackPlayer(Player):

    def __init__(self, name, black_pieces):
        super(BlackPlayer, self).__init__(name, "b", black_pieces)

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

    def __repr__(self):
        return self.chess_piece.symbol if self.chess_piece else " "


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

        blacks = self.config.get_black_pieces()
        whites = self.config.get_white_pieces()

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

    def get_cell_by(self, line, col):
        return board[line][col] ###try!!

    def reset(self):
        pass

    def move(self, start_position, end_position):
        pass

    def __repr__(self):
        board_str = ""

        for i in range(self._config.get_board_lines()):
            substr = ""
            for j in range(self._config.get_board_columns()):
                substr += self.board[i][j].chess_piece.symbol if self.board[i][j].chess_piece else " "
            board_str += substr + "\n"

        return board_str


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

    # TODO: moves !!!
    def get_white_pieces(self):
        whites = self.config["pieces"]["white"]
        pieces = {}

        for type_str in whites:
            chess_piece = ChessPieceFactory.get_type(type_str)
            for position in whites[type_str]["positions"]:
                pieces[tuple(position)] = chess_piece("w", moves=None)

        return pieces

    # TODO: moves !!!
    def get_black_pieces(self):
        blacks = self.config["pieces"]["black"]

        pieces = {}

        for type_str in blacks:
            chess_piece = ChessPieceFactory.get_type(type_str)
            for position in blacks[type_str]["positions"]:
                pieces[tuple(position)] = chess_piece("b", moves=None)

        return pieces

    def get_capturing_condition(self):
        pass

    def get_end_condition(self):
        pass


# TODO: ChessGame + ChessState !!!

class Chess:

    def __init__(self, white_player_name, black_player_name, configuration_path):
        self._config = Config(configuration_path)
        self._white = WhitePlayer(white_player_name, None)
        self._black = BlackPlayer(black_player_name, None)
        self._current_player = self._white
        self._board = ChessBoard(self._config)

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
    def current_player(self):
        return self._current_player

    @property
    def board(self):
        return self._board

    def reset_game(self):
        self._current_player = self._white
        self._board.reset()

    @staticmethod
    def get_valid_cells(start_cell: Cell):
        pass

    # TODO: RETURN REWARD
    def move(self, start_cell, end_cell):
        pass

    def has_finished(self):
        pass

    def render(self):
        print(self._board)


if __name__ == '__main__':
    chess = Chess("Andrei", "AI", "standard_chess_cfg.json")
    chess.render()
