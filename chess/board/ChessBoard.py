from chess.board.Cell import Cell
from chess.board.Position import Position


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

    def __getitem__(self, line):
        return self.board[line]

    def reset(self):
        self._init()

    def move(self, start_position, end_position):
        pass

    def get_rendered_board(self):
        lines = self.config.get_board_lines()
        columns = self.config.get_board_columns()
        return [[self.board[i][j].get_symbol() for j in range(columns)] for i in range(lines)]
