from chess import Cell


def standard_pawn(start_cell: Cell, chess: Chess):
    if start_cell.chess_piece.color() == "black":
        # if start_cell on starting position
        # chess._board.get_cell_by(start_cell.position().line(), start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line() + 2, start_cell.position().column()))
        if chess._board.get_cell_by(start_cell.position().line() + 1, start_cell.position().column())._is_empty():
            chess._board.get_cell_by(start_cell.position().line(), start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line() + 1, start_cell.position().column()))
        if chess._board.get_cell_by(start_cell.position().line() + 1, start_cell.position().column() + 1)._is_empty() == False:
            if chess._board.get_cell_by(start_cell.position().line() + 1, start_cell.position().column() + 1).chess_piece.color() != start_cell.chess_piece.color():
                chess._board.get_cell_by(start_cell.position().line(), start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line() + 1, start_cell.position().column() + 1))
        if chess._board.get_cell_by(start_cell.position().line() + 1, start_cell.position().column() - 1)._is_empty() == False:
            if chess._board.get_cell_by(start_cell.position().line() + 1, start_cell.position().column() - 1).chess_piece.color() != start_cell.chess_piece.color():
                chess._board.get_cell_by(start_cell.position().line(), start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line() + 1, start_cell.position().column() - 1))
    else:
        # if start_cell on starting position
        # chess._board.get_cell_by(start_cell.position().line(), start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line() - 2, start_cell.position().column()))
        if chess._board.get_cell_by(start_cell.position().line() - 1, start_cell.position().column())._is_empty():
            chess._board.get_cell_by(start_cell.position().line(), start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line() - 1, start_cell.position().column()))
        if chess._board.get_cell_by(start_cell.position().line() - 1, start_cell.position().column() + 1)._is_empty() == False:
            if chess._board.get_cell_by(start_cell.position().line() - 1, start_cell.position().column() + 1).chess_piece.color() != start_cell.chess_piece.color():
                chess._board.get_cell_by(start_cell.position().line(), start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line() - 1, start_cell.position().column() + 1))
        if chess._board.get_cell_by(start_cell.position().line() - 1, start_cell.position().column() - 1)._is_empty() == False:
            if chess._board.get_cell_by(start_cell.position().line() - 1, start_cell.position().column() - 1).chess_piece.color() != start_cell.chess_piece.color():
                chess._board.get_cell_by(start_cell.position().line(), start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line() - 1, start_cell.position().column() - 1))


def standard_rook(start_cell: Cell, chess: Chess):
    for i in range(chess._config.get_board_lines()):
        if i == start_cell.position().line():
            continue
        if chess._board.get_cell_by(i, start_cell.position().column())._is_empty() == False:
            if chess._board.get_cell_by(i, start_cell.position().column()).chess_piece.color() == start_cell.chess_piece.color():
                continue
            chess._board.get_cell_by(i, start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(i, start_cell.position().column()))
            continue
        chess._board.get_cell_by(i, start_cell.position().column()).chess_piece._get_valid_moves.append(chess._board.get_cell_by(i, start_cell.position().column()))
    for j in range(chess._config.get_board_columns()):
        if j == start_cell.position().column():
            continue
        if chess._board.get_cell_by(start_cell.position().line(), j)._is_empty() == False:
            if chess._board.get_cell_by(start_cell.position().line(), j).chess_piece.color() == start_cell.chess_piece.color():
                continue
            chess._board.get_cell_by(start_cell.position().line(), j).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line(), j))
            continue
        chess._board.get_cell_by(start_cell.position().line(), j).chess_piece._get_valid_moves.append(chess._board.get_cell_by(start_cell.position().line(), j))
    return chess._board.get_cell_by(start_cell.position().line(), j).chess_piece._get_valid_moves

# Continue...


def standard_capturing():
    pass


def standard_game_over(board):
    pass


# TODO: complete
func_dict = {"pawn": standard_pawn,
             "rook": standard_rook}

