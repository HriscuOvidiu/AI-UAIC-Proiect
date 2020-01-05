from chess.board.Cell import Cell
from chess.game.ChessGame import ChessGame


def on_starting_position():
    pass


def add_move_by_location(move_list, line, column):
    move_list.append(chess.current_state.board[line][column].position)


def different_color(cell1, cell2):
    return cell1.chess_piece.color != cell2.chess_piece.color


def pawn_can_move(cell, chess, color, double = False):
    if double:
        color *= 2     
    if chess.current_state.board[start_cell.position.line + color][start_cell.position.column]._is_empty():
            return True
    return False


def pawn_capture_empty(cell, chess, color, direction):
    return chess.current_state.board[start_cell.position.line + color][start_cell.position.column + direction]._is_empty()


def pawn_can_capture(cell, chess, color):
    capture_list = []
    if pawn_capture_empty(cell, chess, color, 1) is False and different_color(cell, chess.current_state.board[start_cell.position.line + color][start_cell.position.column + 1]):
        capture_list.append(chess.current_state.board[start_cell.position.line + color][start_cell.position.column + 1].position)
    if pawn_capture_empty(cell, chess, color, -1) is False and different_color(cell, chess.current_state.board[start_cell.position.line + color][start_cell.position.column - 1]):
        capture_list.append(chess.current_state.board[start_cell.position.line + color][start_cell.position.column - 1].position)
    return capture_list


def standard_pawn(start_cell: Cell, chess: Chess):
    valid_moves = []
    color = 1 if start_cell.chess_piece.color == "black" else -1
    if on_starting_position() and pawn_can_move(start_cell, chess, color, True):
        add_move_by_location(valid_moves, start_cell.position.line + (2 * color), start_cell.position.column)
    if pawn_can_move(start_cell, chess, color):
        add_move_by_location(valid_moves, start_cell.position.line + color, start_cell.position.column)
    valid_moves.extend(pawn_can_capture(start_cell, chess, color))
    return valid_moves


def standard_rook(start_cell: Cell, chess: ChessGame):
    valid_moves = []
    for i in range(chess._config.get_board_lines()):
        if i == start_cell.position.line:
            continue
        if chess.current_state.board[i][start_cell.position.column]._is_empty() == False and different_color(start_cell, chess.current_state.board[i][start_cell.position.column]):
            add_move_by_location(valid_moves, i, start_cell.position.column)
            continue
        add_move_by_location(valid_moves, i, start_cell.position.column)
    for j in range(chess._config.get_board_columns()):
        if j == start_cell.position.column:
            continue
        if chess.current_state.board[start_cell.position.line][j]._is_empty() == False and different_color(start_cell, chess.current_state.board[start_cell.position.line][j]):
            add_move_by_location(valid_moves, start_cell.position.line, j)
            continue
        add_move_by_location(valid_moves, start_cell.position.line, j)
    return valid_moves

def can_move_column(cell, chess, direction):  
    if chess.current_state.board[start_cell.position.line][start_cell.position.column + direction]._is_empty():
            return True
    return False

def get_king_moves(start_cell, chess):
    king_moves = []

    if pawn_can_move(start_cell, chess, 1):
        add_move_by_location(king_moves, start_cell.position.line + 1, start_cell.position.column)
    if pawn_can_move(start_cell, chess, -1):
        add_move_by_location(king_moves, start_cell.position.line - 1, start_cell.position.column)
    if can_move_column(start_cell, chess, 1):
        add_move_by_location(king_moves, start_cell.position.line, start_cell.position.column + 1)
    if can_move_column(start_cell, chess, -1):
        add_move_by_location(king_moves, start_cell.position.line, start_cell.position.column - 1)

    return king_moves

def get_king_captures(start_cell, chess):
    king_captures = []
    king_captures.extend(pawn_can_capture(cell, chess, 1))
    king_captures.extend(pawn_can_capture(cell, chess, -1))
    return king_captures
    

def standard_king(start_cell: Cell, chess: ChessGame):
    valid_moves = []

    valid_moves.extend(get_king_moves(start_cell, chess))
    valid_moves.extend(get_king_captures(start_chell, chess))

    return valid_moves

def standard_bishop(start_cell: Cell, chess: ChessGame):
    valid_moves = []
    directions = [[1,1],[-1,1],[-1,-1],[1,-1]]
    for direction in directions:
        i = start_cell.position.line
        j = start_cell.position.column
        for counter in range(0,8):
            i += direction[0]
            j += direction[1]
            if chess.current_state.board[i][j]._is_empty() or different_color(start_cell, chess.current_state.board[i][j]):
                add_move_by_location(valid_moves, i, j)

    return valid_moves

def standard_capturing():
    pass


def standard_game_over(board):
    pass


# TODO: complete
func_dict = {"pawn": standard_pawn,
             "rook": standard_rook,
             "king": standard_king,
             "bishop": standard_bishop}

