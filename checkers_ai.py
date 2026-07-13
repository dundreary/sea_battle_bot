import random
import time
from checkers import (
    BOARD_SIZE, EMPTY, WHITE, BLACK, WHITE_KING, BLACK_KING,
    get_legal_moves, apply_move, has_pieces,
    piece_color, is_king, opponent,
)


def evaluate_board(board, color):
    """Static evaluation from `color`'s point of view.

    Combines material (kings are strong in Russian draughts), advancement
    toward promotion, central control and back-row defence (keeping your
    home-row men denies the opponent promotions). The old evaluator only
    counted material and a tiny advancement bonus, which made the bot easy to
    outplay in closed positions. The function stays a single cheap board scan
    so the deeper alpha-beta search below is not slowed down.
    """
    score = 0
    opp = opponent(color)
    mid = (BOARD_SIZE - 1) / 2.0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = board[r][c]
            if p == EMPTY:
                continue
            pc = piece_color(p)
            pk = is_king(p)
            val = 200 if pk else 100
            if not pk:
                # Advancement toward the promotion row.
                adv = (BOARD_SIZE - 1 - r) if pc == WHITE else r
                val += adv * 4
            # Central control: edge and corner pieces are less valuable.
            val -= int(abs(r - mid) + abs(c - mid))
            if pc == color:
                score += val
                if not pk:
                    # Back-row guard: keeping home-row men blocks the
                    # opponent from promoting and is worth defending.
                    if (pc == WHITE and r == BOARD_SIZE - 1) or (pc == BLACK and r == 0):
                        score += 12
            else:
                score -= val
                if not pk:
                    if (pc == WHITE and r == BOARD_SIZE - 1) or (pc == BLACK and r == 0):
                        score -= 12
    return score


def _move_key(board, move):
    """Ordering key (higher = search first). Prefer captures, promotions and
    advancement so alpha-beta prunes more effectively without simulating."""
    captured = move[2] if len(move) > 2 and move[2] else []
    cap = len(captured)
    end = move[1][-1]
    r, c = end
    piece = board[move[0][0]][move[0][1]]
    promote = 0
    if piece == WHITE and r == 0:
        promote = 50
    elif piece == BLACK and r == BOARD_SIZE - 1:
        promote = 50
    adv = (BOARD_SIZE - 1 - r) if piece_color(piece) == WHITE else r
    return cap * 1000 + promote + adv


def alpha_beta(board, depth, alpha, beta, maximizing, ai_color, deadline):
    if time.time() > deadline:
        # Hard stop: the search has blown the time budget. Raising lets the
        # iterative-deepening loop in get_ai_move fall back to the last fully
        # searched depth instead of blocking the (single-threaded) server.
        raise _Timeout()
    current_color = ai_color if maximizing else opponent(ai_color)
    if depth == 0:
        return evaluate_board(board, ai_color), None
    moves = get_legal_moves(board, current_color)
    # A side with no pieces or no legal moves has lost the game.
    if not has_pieces(board, current_color) or not moves:
        return (float("-inf") if maximizing else float("inf")), None

    moves.sort(key=lambda m: _move_key(board, m), reverse=True)
    if maximizing:
        max_eval = float("-inf")
        best_move = moves[0]
        for move in moves:
            new_board = apply_move(board, move)
            eval_score, _ = alpha_beta(new_board, depth - 1, alpha, beta, False, ai_color, deadline)
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
            eval_score, _ = alpha_beta(new_board, depth - 1, alpha, beta, True, ai_color, deadline)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


class _Timeout(Exception):
    pass


def get_ai_move(board, color, difficulty=3, time_budget=1.5):
    moves = get_legal_moves(board, color)
    if not moves:
        return None
    if len(moves) == 1:
        return moves[0]

    if difficulty <= 1:
        return random.choice(moves)

    max_depth = min(difficulty, 14)
    best = moves[0]
    deadline = time.time() + time_budget
    # Iterative deepening: keep the result of the last fully searched depth.
    # The deadline raises _Timeout mid-search so a single AI move can never
    # block the server noticeably longer than time_budget.
    try:
        for depth in range(1, max_depth + 1):
            _, move = alpha_beta(board, depth, float("-inf"), float("inf"), True, color, deadline)
            if move:
                best = move
    except _Timeout:
        pass
    return best
