from chess.board.Cell import Cell
from chess.game.ChessGame import ChessGame

#TODO: Chess board + config instead of ChessGame

def on_starting_position(cell):
    return cell.position == cell.chess_piece.initial_position


def add_move_by_location(move_list, chess, line, column):
    move_list.append(chess.current_state.board[line][column].position)


def different_color(cell1, cell2):
    if cell1.chess_piece == None or cell2.chess_piece == None:
        return True
    return cell1.chess_piece.color != cell2.chess_piece.color

def get_move_by(start_cell, chess, directions, iterative=False, can_capture=True, can_move=True):
    valid_moves = []
    for direction in directions:
        i = start_cell.position.line
        j = start_cell.position.column
        blocked = 0
        if iterative:
            for counter in range(0, chess._configuration.get_board_lines() + 1):
                i += direction[0]
                j += direction[1]
                if 0 <= i <= 7 and 0 <= j <= 7 and blocked == 0:
                    if chess.current_state.board[i][j].is_empty():
                        add_move_by_location(valid_moves, chess, i, j)
                    elif different_color(start_cell, chess.current_state.board[i][j]):
                        add_move_by_location(valid_moves, chess, i, j)
                        blocked = 1
                    else:
                        blocked = 1
        else:
            i += direction[0]
            j += direction[1]
            if 0 <= i <= 7 and 0 <= j <= 7:
                if chess.current_state.board[i][j].is_empty() and can_move is True:
                    add_move_by_location(valid_moves, chess, i, j)
                elif different_color(start_cell, chess.current_state.board[i][j]) and can_capture is True and chess.current_state.board[i][j].chess_piece is not None:
                    add_move_by_location(valid_moves, chess, i, j)

    return valid_moves

def standard_pawn(start_cell: Cell, chess: ChessGame):
    valid_moves = []   
    color = 1 if start_cell.chess_piece.color == "b" else -1
    directions_move = [[color,0]]
    directions_capture = [[color,-1],[color,1]]
    if on_starting_position(start_cell):
        directions_move.append([color*2,0])
    valid_moves.extend(get_move_by(start_cell, chess, directions_move, False, False, True))
    valid_moves.extend(get_move_by(start_cell, chess, directions_capture, False, True, False))
    return valid_moves


def standard_rook(start_cell: Cell, chess: ChessGame):
    directions = [[1,0],[-1,0],[0,-1],[0,1]]
    return get_move_by(start_cell, chess, directions, True)
    

def standard_king(start_cell: Cell, chess: ChessGame, checkmate = False):
    directions = [[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]]
    return get_move_by(start_cell, chess, directions)

def standard_bishop(start_cell: Cell, chess: ChessGame):
    directions = [[1,1],[-1,1],[-1,-1],[1,-1]]
    return get_move_by(start_cell, chess, directions, True)

def standard_queen(start_cell: Cell, chess: ChessGame):
    valid_moves = []
    valid_moves.extend(standard_bishop(start_cell, chess))
    valid_moves.extend(standard_rook(start_cell, chess))
    return valid_moves

def standard_knight(start_cell: Cell, chess: ChessGame):
    directions = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]
    return get_move_by(start_cell, chess, directions)

def get_king_pos(game: ChessGame, player: str):
    for line in game.current_state.board:
        for cell in line:
            piece = str(cell.chess_piece) if not cell.is_empty() else ''
            # print(piece, player + 'King')
            if piece == player + 'King':
                return cell


def is_in_check(game: ChessGame, player: str):
    king_cell = get_king_pos(game, player)
    check_pos = []
    for line in game.current_state.board:
        for cell in line:
            piece = cell.chess_piece if not cell.is_empty() else ''
            if piece and not str(piece).startswith(player):
                check_pos += piece.get_valid_moves(cell, game)
    if king_cell.position in check_pos:
        return True
    return False


def standard_game_over(player: str, game: ChessGame):
    if is_in_check(game, player):
        from copy import deepcopy
        aux_state = deepcopy(game.current_state)
        for line in game.current_state.board:
            for cell in line:
                piece = cell.chess_piece if not cell.is_empty() else ''
                if piece and str(piece).startswith(player):
                    move_list = piece.get_valid_moves(cell, game)
                    for i in move_list:
                        game.move_piece(cell.position.line, cell.position.column, i.line, i.column)
                        if not is_in_check(game, player):
                            game.current_state = deepcopy(aux_state)
                            return 1
                        game.current_state = deepcopy(aux_state)
        return 2
    return 0


# TODO: complete
rules_func_dict = { "standard_pawn": standard_pawn,
                    "standard_rook": standard_rook,
                    "standard_king": standard_king,
                    "standard_bishop": standard_bishop,
                    "standard_queen": standard_queen,
                    "standard_knight": standard_knight,
                    "standard_game_over": standard_game_over}
