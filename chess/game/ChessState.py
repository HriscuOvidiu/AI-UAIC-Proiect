import json
from chess.players.Player import Player


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

    @current_player.setter
    def current_player(self, cp):
        if isinstance(cp, Player) or cp is None:
            self._current_player = cp
        else:
            raise AttributeError("[current_player] Invalid type of <cp>")

    @current_player.getter
    def current_player(self):
        return self._current_player

    def is_valid(self, start_line, start_column, end_line, end_column):
        return not (start_line == end_line and start_column == end_column)

    def make_transition(self, start_line, start_column, end_line, end_column):
        start_cell = self.board[start_line][start_column]
        end_cell = self.board[end_line][end_column]

        chess_piece_to_move = start_cell.chess_piece
        chess_piece_to_move.has_moved()

        end_cell.chess_piece = chess_piece_to_move
        start_cell.chess_piece = None

    def get_rendered_board(self):
        return self.board.get_rendered_board()

    def is_current_player_white(self):
        from chess.players.WhitePlayer import WhitePlayer
        return isinstance(self.current_player, WhitePlayer)

    def get_eval(self, maximizing):
        # https://www.chessprogramming.org/Simplified_Evaluation_Function

        score = 0
        board = self.board.board
        if (self.is_current_player_white() and maximizing == 1) or \
                (not self.is_current_player_white() and maximizing == -1):
            max_player = 'w'
        else:
            max_player = 'b'

        with open('./static/configs/chess_piece_evals.json') as f:
            symbols = json.load(f)
        with open('./static/configs/chess_piece_square_tables.json') as f:
            square_tables = json.load(f)

        for line in board:
            for i in line:
                if not i.is_empty():
                    table = square_tables[str(i.chess_piece)]
                    score += symbols[str(i.chess_piece)[1:]] + table[i.position.line][i.position.column] \
                        if i.chess_piece.color == max_player else -1 * (symbols[str(i.chess_piece)[1:]] +
                                                                        table[i.position.line][i.position.column])

        return score * maximizing

    def __repr__(self):
        return f'{self.__class__.__name__}({self.current_player}, {self.board.get_rendered_board()})'
