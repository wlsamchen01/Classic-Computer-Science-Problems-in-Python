from __future__ import annotations
from board import Piece, Board, Move

# find the best possible outcome for original player
def minimax(
    board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8
) -> float:
    # Base case - terminal position or maximum depth reached
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # recursive case - maximise your gains or minimise the opponet's gains
    if maximizing:
        best_eval: float = float(
            "-inf"
        )  # arbitarily low starting point, negative infinity
        # Recursion step. Each move is also a board
        # maximising changed to False because of switching turn
        for move in board.legal_moves:
            result: float = minimax(
                board.move(move), False, original_player, max_depth - 1
            )
            # compare if the result is better than the current
            # value of best_eval, if so update best_eval
            best_eval = max(result, best_eval)
        return best_eval
    else:  # minimising
        worst_eval: float = float("inf")  # arbitarily high starting point, infinity
        for move in board.legal_moves:
            result = minimax(board.move(move), True, original_player, max_depth - 1)
            # compare if the result is lower than the current
            # value of worst_eval, if so update worst_eval
            worst_eval = min(result, worst_eval)
        return worst_eval


# Find the best possible move in the current position
# Looking up to max_depth ahead
def find_best_move(board: Board, max_depth: int = 8) -> Move:
    # initialise values to negative numbers
    best_eval: float = float("-inf")
    best_move: Move = Move(-1)
    # go through the possible moves and update not only the best_eval
    # but also the best_move
    for move in board.legal_moves:
        # result: float = minimax(board.move(move), False, board.turn, max_depth)
        result: float = alphabeta(board.move(move), False, board.turn, max_depth)
        if result > best_eval:
            best_eval = result
            best_move = move
    return best_move


def alphabeta(
    board: Board,
    maximizing: bool,
    original_player: Piece,
    max_depth: int = 8,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> float:
    # Base case - terminal position or maximum depth reached
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # Recursive case - maximising your gains or minimising the opponent's gains
    if maximizing:
        for move in board.legal_moves:
            result: float = alphabeta(
                board.move(move), False, original_player, max_depth - 1, alpha, beta
            )
            # update alpha if result is larger
            alpha = max(result, alpha)
            # break out of recursion of beta is found to be smaller or equal
            # to alpha - ie. kill this branch
            if beta <= alpha:
                break
        return alpha
    else:  # minimising
        for move in board.legal_moves:
            result = alphabeta(
                board.move(move), True, original_player, max_depth - 1, beta
            )
            beta = min(result, beta)
            if beta <= alpha:
                break
        return beta
