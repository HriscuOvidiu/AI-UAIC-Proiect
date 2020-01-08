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

    def is_current_player_white(self):
        return self.current_state.is_current_player_white()

    def reset_game(self):
        self._current_state = self._init_state

    def get_valid_positions(self, line, column):
        cell = self._current_state.board[line][column]

        try:
            chess_piece = cell.chess_piece
            return chess_piece.get_valid_moves(cell, self)
        except:
           print("No ChessPiece found on current cell!")

    # TODO: RETURN REWARD
    def move(self, start_line, start_column, end_line, end_column):
        reward = 0

        start_cell = self.current_state.board[start_line][start_column]
        end_cell = self.current_state.board[end_line][end_column]

        end_cell.chess_piece = start_cell.chess_piece
        start_cell.chess_piece = None

        return reward

    def has_finished(self):
        return self.current_state.is_final_state()

    def render(self):
        return self.current_state.get_rendered_board()

    @current_state.setter
    def current_state(self, value):
        self._current_state = value

    def minimax(self, state, depth):
        if not depth or state.is_final_state():
            return state
        max_eval = -float("inf")
        max_state = None
        for possible_move in state.get_next_moves():
            next_move = self.minimax(possible_move, depth)
            move_eval = next_move.get_eval()
            if move_eval > max_eval:
                max_eval = move_eval
                max_state = possible_move
        return max_state

    def minimax_pruning(self, state, depth, alpha, beta):
        if not depth or state.is_final_state():
            return state
        max_eval = -float("inf")
        max_state = None
        for possible_move in state.get_next_moves():
            next_move = self.minimax_pruning(possible_move, depth, -beta, -alpha)
            move_eval = next_move.get_eval()
            alpha = max(alpha, max_eval)
            if move_eval > max_eval:
                max_eval = move_eval
                max_state = possible_move
            if alpha >= beta:
                break
        return max_state

    def minimax_root(self, depth):
        self.current_state = self.minimax_pruning(self.current_state, depth, -float("inf"), float("inf"))
