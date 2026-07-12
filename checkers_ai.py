import random
import time
from checkers import (
    BOARD_SIZE, EMPTY, WHITE,
    get_legal_moves, apply_move, has_pieces,
    piece_color, is_king, opponent,
)


def evaluate_board(board, color):
    score = 0
    opp = opponent(color)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = board[r][c]
            if p == EMPTY:
                continue
            pc = piece_color(p)
            pk = is_king(p)
            if pc == color:
                if pk:
                    score += 150
                else:
                    score += 100
                    if color == WHITE:
                        score += (7 - r) * 5
                    else:
                        score += r * 5
            elif pc == opp:
                if pk:
                    score -= 150
                else:
                    score -= 100
                    if opp == WHITE:
                        score -= (7 - r) * 5
                    else:
                        score -= r * 5
    return score


def alpha_beta(board, depth, alpha, beta, maximizing, ai_color):
    current_color = ai_color if maximizing else opponent(ai_color)
    if depth == 0:
        return evaluate_board(board, ai_color), None
    moves = get_legal_moves(board, current_color)
    # A side with no pieces or no legal moves has lost the game.
    if not has_pieces(board, current_color) or not moves:
        return (float("-inf") if maximizing else float("inf")), None

    if maximizing:
        max_eval = float("-inf")
        best_move = moves[0]
        for move in moves:
            new_board = apply_move(board, move)
            eval_score, _ = alpha_beta(new_board, depth - 1, alpha, beta, False, ai_color)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = moves[0]
        for move in moves:
            new_board = apply_move(board, move)
            eval_score, _ = alpha_beta(new_board, depth - 1, alpha, beta, True, ai_color)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


def get_ai_move(board, color, difficulty=3, time_budget=1.5):
    moves = get_legal_moves(board, color)
    if not moves:
        return None
    if len(moves) == 1:
        return moves[0]

    if difficulty <= 1:
        return random.choice(moves)

    max_depth = min(difficulty, 9)
    best = moves[0]
    start = time.time()
    # Iterative deepening: keep the result of the last fully searched depth and
    # stop early if the search runs past the time budget, so a single AI move
    # can never block the (single-threaded) server for long.
    for depth in range(1, max_depth + 1):
        _, move = alpha_beta(board, depth, float("-inf"), float("inf"), True, color)
        if move:
            best = move
        if time.time() - start > time_budget:
            break
    return best
