from chess.board.Cell import Cell
from chess.board.ChessBoard import ChessBoard
from chess.game.ChessState import ChessState
from chess.players.BlackPlayer import BlackPlayer
from chess.players.WhitePlayer import WhitePlayer


class ChessGame:

    def __init__(self, configuration):
        self._configuration = configuration
        self._white = WhitePlayer(None)
        self._black = BlackPlayer(None)
        self._init_state = ChessState(self._white, ChessBoard(self._configuration))
        self._current_state = self._init_state

    @property
    def configuration(self):
        return self._configuration

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
        return self.current_state.get_rendered_board()
