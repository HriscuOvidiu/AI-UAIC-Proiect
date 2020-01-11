from chess.board.Cell import Cell
from chess.board.ChessBoard import ChessBoard
from chess.game.ChessState import ChessState
from chess.players.BlackPlayer import BlackPlayer
from chess.players.WhitePlayer import WhitePlayer


class ChessGame:

    def __init__(self, configuration, game_mode):
        self._configuration = configuration
        self._game_mode = game_mode
        self._white = WhitePlayer()
        self._black = BlackPlayer()
        self._init_state = ChessState(
            self._white, ChessBoard(self._configuration))
        self._current_state = self._init_state
        self._logs = []

    @property
    def configuration(self):
        return self._configuration

    @property
    def game_mode(self):
        return self._game_mode

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

    @current_state.setter
    def current_state(self, cs):
        if isinstance(cs, ChessState) or cs is None:
            self._current_state = cs
        else:
            raise AttributeError("[current_state] Invalid type of <cs>")

    @current_state.getter
    def current_state(self):
        return self._current_state

    @property
    def logs(self):
        return self._logs

    def add_log(self, start_line, start_column, end_line, end_column):
        from string import ascii_uppercase
        player_list = ["Black", "White"]
        letter_list = ascii_uppercase[:8]

        log = player_list[int(self.is_current_player_white())]
        log += f" moved piece from {letter_list[start_column]}{8 - start_line} to {letter_list[end_column]}{8 - end_line}"

        self._logs.append(log)

    def is_current_player_white(self):
        return self.current_state.is_current_player_white()

    def change_current_player(self):
        if self.is_current_player_white():
            self._current_state.current_player = self._black
        else:
            self._current_state.current_player = self._white

    def reset_game(self):
        self._current_state = self._init_state

    def get_valid_positions(self, line, column):
        cell = self._current_state.board[line][column]

        try:
            chess_piece = cell.chess_piece
            return chess_piece.get_valid_moves(cell, self)
        except Exception as e:
            print(e)

    def move_piece(self, start_line, start_column, end_line, end_column):
        start_cell = self.current_state.board[start_line][start_column]
        end_cell = self.current_state.board[end_line][end_column]

        chess_piece_to_move = start_cell.chess_piece
        end_cell.chess_piece = chess_piece_to_move
        start_cell.chess_piece = None

    def move(self, start_line, start_column, end_line, end_column, promotion_piece_type='queen'):
        # If PROMOTION
        if self.is_current_player_white():
            if end_line == 0:
                self.move_piece(start_line, start_column, end_line, end_column)
                self.promotion(end_line, end_column, 'w', promotion_piece_type)
                self.change_current_player()
                return
        else:
            if end_line == 7:
                self.move_piece(start_line, start_column, end_line, end_column)
                self.promotion(end_line, end_column, 'b', promotion_piece_type)
                self.change_current_player()
                return

        # If not the same position is selected
        if not (start_line == end_line and start_column == end_column):
            self.move_piece(start_line, start_column, end_line, end_column)
            self.add_log(start_line, start_column, end_line, end_column)
            self.change_current_player()

    # TODO: Check
    def promotion(self, pawn_line, pawn_column, chess_piece_color='w', chess_piece_type_str='queen'):
        from chess.pieces.ChessPieceFactory import ChessPieceFactory
        from chess.board.Position import Position
        chess_piece_type = ChessPieceFactory.get_type(chess_piece_type_str)
        new_chess_piece = chess_piece_type(chess_piece_color, Position(pawn_line, pawn_column), self._configuration._valid_moves_dict[chess_piece_type])
        pawn_cell = self.current_state.board[pawn_line][pawn_column]

        pawn_cell.chess_piece = new_chess_piece

        print(self.current_state.board[pawn_line][pawn_column])

    def has_finished(self):
        return self.configuration.get_end_condition()(self.current_state.current_player.color, self)

    def render(self):
        return self.current_state.get_rendered_board()

    def get_next_moves(self):
        next_moves = []
        for line in self.current_state.board:
            for cell in line:
                piece = cell.chess_piece if not cell.is_empty() else ''
                if str(piece).startswith(self.current_state.current_player.color):
                    piece_moves = piece.get_valid_moves(cell, self)

                    # TODO: Check if OK
                    from chess.main import get_valid_positions_check
                    from copy import deepcopy
                    piece_moves = get_valid_positions_check(deepcopy(self), cell.position.line, cell.position.column, piece_moves)
                    #

                    for position in piece_moves:
                        new_board = deepcopy(self.current_state.board)
                        start_cell = new_board[cell.position.line][cell.position.column]
                        end_cell = new_board[position.line][position.column]
                        end_cell.chess_piece = start_cell.chess_piece
                        start_cell.chess_piece = None
                        state = ChessState(self._black, new_board) if self.is_current_player_white() \
                            else ChessState(self._white, new_board)
                        next_moves.append(state)
        return next_moves

    def minimax(self, state, depth):
        if not depth or self.has_finished() == 2:
            return state
        max_eval = -float("inf")
        max_state = None
        for possible_move in self.get_next_moves():
            next_move = self.minimax(possible_move, depth - 1)
            move_eval = next_move.get_eval()
            if move_eval > max_eval:
                max_eval = move_eval
                max_state = possible_move
        return max_state

    def minimax_pruning(self, state, depth, alpha, beta):
        if not depth or self.has_finished() == 2:
            return state
        max_eval = -float("inf")
        max_state = None
        for possible_move in self.get_next_moves():
            next_move = self.minimax_pruning(
                possible_move, depth - 1, -beta, -alpha)
            move_eval = next_move.get_eval()
            alpha = max(alpha, max_eval)
            if move_eval > max_eval:
                max_eval = move_eval
                max_state = possible_move
            if alpha >= beta:
                break
        return max_state

    def minimax_root(self, depth):
        self.current_state = self.minimax_pruning(
            self.current_state, depth, -float("inf"), float("inf"))
        # self.current_state = self.minimax(self.current_state, depth)
