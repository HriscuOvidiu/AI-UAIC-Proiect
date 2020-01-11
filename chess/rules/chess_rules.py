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

def pawn_can_move(cell, chess, color, double = False):
    if 0 <= cell.position.line + color <= chess._configuration.get_board_lines() - 1:
        if double == True and chess.current_state.board[cell.position.line + color][cell.position.column].is_empty():
            color *= 2     
        if chess.current_state.board[cell.position.line + color][cell.position.column].is_empty():
            return True
    return False

def pawn_capture_empty(cell, chess, color, direction):
    if 0 <= cell.position.line + color <= chess._configuration.get_board_lines() - 1 and 0 <= cell.position.column + direction <= chess._configuration.get_board_columns() - 1:
        return chess.current_state.board[cell.position.line + color][cell.position.column + direction].is_empty()
    return True

def pawn_can_capture(cell, chess, color):
    capture_list = []
    if pawn_capture_empty(cell, chess, color, 1) is False:
        if different_color(cell, chess.current_state.board[cell.position.line + color][cell.position.column + 1]):
            capture_list.append(chess.current_state.board[cell.position.line + color][cell.position.column + 1].position)
            
    if pawn_capture_empty(cell, chess, color, -1) is False:
        if different_color(cell, chess.current_state.board[cell.position.line + color][cell.position.column - 1]):
            capture_list.append(chess.current_state.board[cell.position.line + color][cell.position.column - 1].position)
    return capture_list


def standard_pawn(start_cell: Cell, chess: ChessGame):
    valid_moves = []
    color = 1 if start_cell.chess_piece.color == "b" else -1
    if on_starting_position(start_cell) and pawn_can_move(start_cell, chess, color, True):
        add_move_by_location(valid_moves, chess, start_cell.position.line + (2 * color), start_cell.position.column)
    if pawn_can_move(start_cell, chess, color):
        add_move_by_location(valid_moves, chess, start_cell.position.line + color, start_cell.position.column)
    valid_moves += pawn_can_capture(start_cell, chess, color)

    return valid_moves


def standard_rook(start_cell: Cell, chess: ChessGame):
    valid_moves = []
    directions = [[1,0],[-1,0],[0,-1],[0,1]]
    for direction in directions:
        i = start_cell.position.line
        j = start_cell.position.column
        blocked = 0
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
    return valid_moves
    

def standard_king(start_cell: Cell, chess: ChessGame, checkmate = False):
    valid_moves = []
    directions = [[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]]
    for direction in directions:
        i = start_cell.position.line
        j = start_cell.position.column
        i += direction[0]
        j += direction[1]
        if 0 <= i <= 7 and 0 <= j <= 7:
            if chess.current_state.board[i][j].is_empty():
                add_move_by_location(valid_moves, chess, i, j)
            elif different_color(start_cell, chess.current_state.board[i][j]) and not checkmate:
                add_move_by_location(valid_moves, chess, i, j)
            

    return valid_moves

def standard_bishop(start_cell: Cell, chess: ChessGame):
    valid_moves = []
    directions = [[1,1],[-1,1],[-1,-1],[1,-1]]
    for direction in directions:
        i = start_cell.position.line
        j = start_cell.position.column
        blocked = 0
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

    return valid_moves

def standard_queen(start_cell: Cell, chess: ChessGame):
    valid_moves = []
    valid_moves.extend(standard_bishop(start_cell, chess))
    valid_moves.extend(standard_rook(start_cell, chess))
    return valid_moves

def standard_knight(start_cell: Cell, chess: ChessGame):
    valid_moves = []
    directions = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]
    for direction in directions:
        i = start_cell.position.line
        j = start_cell.position.column
        i += direction[0]
        j += direction[1]
        if 0 <= i <= 7 and 0 <= j <= 7:
            if chess.current_state.board[i][j].is_empty():
                add_move_by_location(valid_moves, chess, i, j)
            elif different_color(start_cell, chess.current_state.board[i][j]):
                add_move_by_location(valid_moves, chess, i, j)
            

    return valid_moves


def get_king_pos(game, player):
    for line in game.current_state.board:
        for cell in line:
            piece = str(cell.chess_piece) if not cell.is_empty() else ''
            # print(piece, player + 'King')
            if piece == player + 'King':
                return cell


def standard_game_over(player, game):
    # TODO: check mate refinement - eg. move a white piece to save the king
    king_cell = get_king_pos(game, player)
    check_pos = []
    for line in game.current_state.board:
        for cell in line:
            piece = cell.chess_piece if not cell.is_empty() else ''
            if piece and not str(piece).startswith(player):
                check_pos += piece.get_valid_moves(cell, game)
    if king_cell.position in check_pos and \
            all(elem in check_pos for elem in king_cell.chess_piece.get_valid_moves(king_cell, game)):
        return 2
    if king_cell.position in check_pos:
        return 1
    return 0


# TODO: complete
rules_func_dict = { "standard_pawn": standard_pawn,
                    "standard_rook": standard_rook,
                    "standard_king": standard_king,
                    "standard_bishop": standard_bishop,
                    "standard_queen": standard_queen,
                    "standard_knight": standard_knight,
                    "standard_game_over": standard_game_over}

