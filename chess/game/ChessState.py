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

    def is_valid(self):
        pass

    def get_rendered_board(self):
        return self.board.get_rendered_board()

    def get_next_moves(self):
        next_moves = []
        for line in self.board:
            for cell in line:
                piece = cell.chess_piece if not cell.is_empty() else ''
                if str(piece).startswith(self.current_player.color):
                    # TODO: All the valid moves to the list
                    pass
        return next_moves

    def is_current_player_white(self):
        from chess.players.WhitePlayer import WhitePlayer
        return isinstance(self.current_player, WhitePlayer)

    def get_eval(self):
        # TODO SQUARE SPECIFIC VALUE TABLES
        # https://www.chessprogramming.org/Simplified_Evaluation_Function

        score = 0
        board = self.board.board
        to_move = 1 if not self.is_current_player_white() else -1

        with open('./static/configs/chess_piece_evals.json') as f:
            symbols = json.load(f)

        for line in board:
            for i in line:
                score += symbols[i]
        return score * to_move
