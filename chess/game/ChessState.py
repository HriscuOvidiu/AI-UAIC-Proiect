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
