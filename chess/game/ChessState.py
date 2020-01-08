import json


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

    def get_rendered_board(self):
        return self.board.get_rendered_board()

    def get_next_moves(self):
        pass

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
