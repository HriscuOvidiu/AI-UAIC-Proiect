from chess.board.ChessBoard import ChessBoard
from chess.game.ChessState import ChessState
from chess.players.BlackPlayer import BlackPlayer
from chess.players.WhitePlayer import WhitePlayer
from chess.pieces.Pawn import Pawn


class ChessGame:

    def __init__(self, configuration, game_mode):
        self._configuration = configuration
        self._game_mode = game_mode
        self._white = WhitePlayer()
        self._black = BlackPlayer()
        self._init_state = ChessState(self._white, ChessBoard(self._configuration))
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

    def add_log(self, start_line, start_column, end_line, end_column, player_color):
        from string import ascii_uppercase
        letter_list = ascii_uppercase[:8]

        log = f"{player_color} moved {self.current_state.board[end_line][end_column].chess_piece.name} from " \
              f"{letter_list[start_column]}{8 - start_line} to {letter_list[end_column]}{8 - end_line}"

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
        chess_piece_to_move.has_moved()

        end_cell.chess_piece = chess_piece_to_move
        start_cell.chess_piece = None

    def move(self, start_line, start_column, end_line, end_column, no_log=False):
        if not (start_line == end_line and start_column == end_column):
            self.move_piece(start_line, start_column, end_line, end_column)
            if not no_log:
                self.add_log(start_line, start_column, end_line, end_column, 'White' if self.current_state.is_current_player_white() else 'Black')

    def is_promoting(self, current_line, current_column):
        if isinstance(self.current_state.board[current_line][current_column].chess_piece, Pawn):
            is_white_promoting = self.is_current_player_white() and current_line == 0
            is_black_promoting = not self.is_current_player_white() and current_line == self.configuration.get_board_lines() - 1

            return is_white_promoting or is_black_promoting

        return False

    # TODO: Check
    def promotion(self, pawn_line, pawn_column, chess_piece_color='w', chess_piece_type_str='queen'):
        from chess.pieces.ChessPieceFactory import ChessPieceFactory
        from chess.board.Position import Position
        chess_piece_type = ChessPieceFactory.get_type(chess_piece_type_str)
        new_chess_piece = chess_piece_type(chess_piece_color, Position(pawn_line, pawn_column), self._configuration._valid_moves_dict[chess_piece_type])
        pawn_cell = self.current_state.board[pawn_line][pawn_column]

        pawn_cell.chess_piece = new_chess_piece

    
    def is_castling(self, current_line, current_column, end_line, end_column):
        from chess.pieces.King import King
        if isinstance(self.current_state.board[current_line][current_column].chess_piece, King):
            if self.current_state.board[current_line][current_column].chess_piece.has_been_moved is False and current_line == end_line and ((end_column == current_column - 2) or (end_column == current_column + 2)):
                return True
        return False

    def castle(self, current_line, current_column, end_line, end_column):
        # self.move(current_line, current_column, end_line, end_column)
        # Pt tura din dreapta
        if current_column < end_column:
            self.move(current_line, self.configuration.get_board_columns() - 1, end_line, end_column - 1)
        else:
            self.move(current_line, 0, end_line, end_column + 1)

    def has_finished(self):
        return self.configuration.get_end_condition()(self.current_state.current_player.color, self)

    def render(self):
        return self.current_state.get_rendered_board()

    def get_next_moves(self):
        from chess.main import get_valid_positions_check
        from copy import deepcopy
        next_moves = []
        temp_state = deepcopy(self.current_state)
        for line in temp_state.board:
            for cell in line:
                piece = cell.chess_piece if not cell.is_empty() else ''
                if str(piece).startswith(self.current_state.current_player.color):
                    piece_moves = piece.get_valid_moves(cell, self)

                    # TODO: Check if OK
                    piece_moves = get_valid_positions_check(self, cell.position.line, cell.position.column, piece_moves)

                    for position in piece_moves:
                        self.move(cell.position.line, cell.position.column, position.line, position.column, no_log=True)
                        self.change_current_player()
                        if self.is_promoting(position.line, position.column):
                            promotion_pieces = ['rook', 'bishop', 'knight', 'queen']
                            for i in promotion_pieces:
                                self.promotion(position.line, position.column, self.current_state.current_player.color, i)
                                state = deepcopy(self.current_state)
                                next_moves.append((state, cell, self.current_state.board[position.line][position.column]))
                                self.current_state = deepcopy(temp_state)
                        else:
                            state = deepcopy(self.current_state)
                            next_moves.append((state, cell, self.current_state.board[position.line][position.column]))
                            self.current_state = deepcopy(temp_state)
        return next_moves

    def minimax(self, state, depth, maximizing):
        from copy import deepcopy
        if not depth or self.has_finished() == 2:
            return state, self.current_state.get_eval(maximizing)
        max_eval = -float("inf")
        max_state = None
        aux_state = deepcopy(self.current_state)
        next_moves = self.get_next_moves()
        for possible_move in next_moves:
            self.current_state = deepcopy(possible_move[0])
            move_eval = -self.minimax(possible_move, depth - 1, -maximizing)[1]
            self.current_state = deepcopy(aux_state)
            if move_eval > max_eval:
                max_eval = move_eval
                max_state = possible_move
        return max_state, max_eval

    def minimax_pruning(self, state, depth, alpha, beta, maximizing):
        from copy import deepcopy
        if not depth or self.has_finished() == 2:
            return state, self.current_state.get_eval(maximizing)
        max_eval = -float("inf")
        max_state = None
        aux_state = deepcopy(self.current_state)
        next_moves = self.get_next_moves()
        for possible_move in next_moves:
            self.current_state = deepcopy(possible_move[0])
            move_eval = -self.minimax_pruning(possible_move, depth - 1, -beta, -alpha, -maximizing)[1]
            self.current_state = deepcopy(aux_state)
            if move_eval > max_eval:
                max_eval = move_eval
                max_state = possible_move
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
        return max_state, max_eval

    def minimax_root(self, depth=1):
        next_move, score = self.minimax((self.current_state, None, None), depth, 1)
        self.current_state = next_move[0]
        self.add_log(next_move[1].position.line, next_move[1].position.column, next_move[2].position.line,
                     next_move[2].position.column, 'Black' if self.current_state.is_current_player_white() else 'White')

    def alpha_beta_pruning_root(self, depth=2):
        next_move, score = self.minimax_pruning((self.current_state, None, None), depth, -float("inf"), float("inf"), 1)
        self.current_state = next_move[0]
        self.add_log(next_move[1].position.line, next_move[1].position.column, next_move[2].position.line,
                     next_move[2].position.column, 'Black' if self.current_state.is_current_player_white() else 'White')
