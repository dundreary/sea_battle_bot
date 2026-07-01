import random
import time

BOARD_SIZE = 8
EMPTY = 0
WHITE = 1
BLACK = 2
WHITE_KING = 3
BLACK_KING = 4

PIECE_NAMES = {EMPTY: '.', WHITE: 'w', BLACK: 'b', WHITE_KING: 'W', BLACK_KING: 'B'}


def initial_board():
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if (r + c) % 2 == 1:
                if r < 3:
                    board[r][c] = BLACK
                elif r > 4:
                    board[r][c] = WHITE
    return board


def in_bounds(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def piece_color(piece):
    if piece in (WHITE, WHITE_KING):
        return WHITE
    if piece in (BLACK, BLACK_KING):
        return BLACK
    return None


def is_king(piece):
    return piece in (WHITE_KING, BLACK_KING)


def opponent(color):
    return BLACK if color == WHITE else WHITE


def get_directions(piece):
    if piece == WHITE:
        return [(-1, -1), (-1, 1)]
    elif piece == BLACK:
        return [(1, -1), (1, 1)]
    elif piece == WHITE_KING or piece == BLACK_KING:
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return []


def get_simple_moves(board, r, c):
    piece = board[r][c]
    if piece == EMPTY:
        return []
    moves = []
    for dr, dc in get_directions(piece):
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc) and board[nr][nc] == EMPTY:
            moves.append(((r, c), [(nr, nc)]))
    return moves


def get_capture_moves(board, r, c, piece=None):
    if piece is None:
        piece = board[r][c]
    if piece == EMPTY:
        return []
    color = piece_color(piece)
    moves = []
    for dr, dc in get_directions(piece):
        mr, mc = r + dr, c + dc
        nr, nc = r + 2 * dr, c + 2 * dc
        if in_bounds(nr, nc) and board[nr][nc] == EMPTY and in_bounds(mr, mc):
            mid = board[mr][mc]
            if mid != EMPTY and piece_color(mid) != color:
                moves.append(((r, c), [(nr, nc)], (mr, mc)))
    return moves


def find_multi_captures(board, r, c, piece=None, path=None, captured=None, start_pos=None):
    if piece is None:
        piece = board[r][c]
    if path is None:
        path = [(r, c)]
    if start_pos is None:
        start_pos = (r, c)
    if captured is None:
        captured = []
    color = piece_color(piece)
    moves = []
    for dr, dc in get_directions(piece):
        mr, mc = r + dr, c + dc
        nr, nc = r + 2 * dr, c + 2 * dc
        if in_bounds(nr, nc) and board[nr][nc] == EMPTY and in_bounds(mr, mc):
            mid = board[mr][mc]
            if mid != EMPTY and piece_color(mid) != color and (mr, mc) not in captured:
                new_board = [row[:] for row in board]
                new_board[mr][mc] = EMPTY
                new_board[r][c] = EMPTY
                # Check promotion
                new_piece = piece
                if piece == WHITE and nr == 0:
                    new_piece = WHITE_KING
                elif piece == BLACK and nr == BOARD_SIZE - 1:
                    new_piece = BLACK_KING
                new_board[nr][nc] = new_piece
                sub = find_multi_captures(new_board, nr, nc, new_piece, path + [(nr, nc)], captured + [(mr, mc)], start_pos)
                if sub:
                    moves.extend(sub)
                else:
                    moves.append((start_pos, path[1:] + [(nr, nc)], list(captured + [(mr, mc)])))
    return moves


def get_all_captures(board, color):
    all_moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = board[r][c]
            if p != EMPTY and piece_color(p) == color:
                mc = find_multi_captures(board, r, c)
                all_moves.extend(mc)
    return all_moves


def get_all_simple_moves(board, color):
    all_moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = board[r][c]
            if p != EMPTY and piece_color(p) == color:
                all_moves.extend(get_simple_moves(board, r, c))
    return all_moves


def get_legal_moves(board, color):
    captures = get_all_captures(board, color)
    if captures:
        return captures
    return get_all_simple_moves(board, color)


def apply_move(board, move):
    start, steps, *rest = move
    captures = rest[0] if rest else []
    new_board = [row[:] for row in board]
    sr, sc = start
    piece = new_board[sr][sc]
    new_board[sr][sc] = EMPTY
    for cap in captures:
        new_board[cap[0]][cap[1]] = EMPTY
    current_piece = piece
    for r, c in steps:
        if current_piece == WHITE and r == 0:
            current_piece = WHITE_KING
        elif current_piece == BLACK and r == BOARD_SIZE - 1:
            current_piece = BLACK_KING
        new_board[r][c] = current_piece
    return new_board


def has_pieces(board, color):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if piece_color(board[r][c]) == color:
                return True
    return False


def count_pieces(board, color):
    count = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if piece_color(board[r][c]) == color:
                count += 1
    return count


def board_to_dict(board):
    return [board[r][c] for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]


def dict_to_board(d):
    return [[d[r * BOARD_SIZE + c] for c in range(BOARD_SIZE)] for r in range(BOARD_SIZE)]


class CheckersGame:
    def __init__(self, code, player1_id, player2_id=None, solo=False, difficulty=2):
        self.code = code
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.solo = solo
        self.difficulty = difficulty
        self.board = initial_board()
        self.turn = WHITE
        self.phase = "playing"
        self.created_at = time.time()
        self.winner = None
        self.last_move = None

    @property
    def current_player(self):
        return self.player1_id if self.turn == WHITE else self.player2_id

    def player_color(self, uid):
        if uid == self.player1_id:
            return WHITE
        if uid == self.player2_id:
            return BLACK
        return None

    def switch_turn(self):
        self.turn = opponent(self.turn)

    def player_num(self, uid):
        return 1 if uid == self.player1_id else 2

    def opponent_id(self, uid):
        return self.player2_id if uid == self.player1_id else self.player1_id

    def get_moves_for_color(self, color):
        return get_legal_moves(self.board, color)

    def make_move(self, move):
        self.board = apply_move(self.board, move)
        self.last_move = move
        self.switch_turn()
        if not has_pieces(self.board, self.turn):
            self.winner = opponent(self.turn)
            self.phase = "finished"
            return True
        if not self.get_moves_for_color(self.turn):
            self.winner = opponent(self.turn)
            self.phase = "finished"
            return True
        return False

    def get_state(self, uid):
        color = self.player_color(uid)
        my_turn = self.turn == color
        moves = self.get_moves_for_color(color) if my_turn and self.phase == "playing" else []
        highlighted = set()
        valid_dests = {}
        for m in moves:
            sr, sc = m[0]
            highlighted.add((sr, sc))
            src_key = sr * BOARD_SIZE + sc
            dest_key = m[1][-1][0] * BOARD_SIZE + m[1][-1][1]
            valid_dests.setdefault(src_key, set()).add(dest_key)

        return {
            "code": self.code,
            "difficulty": self.difficulty,
            "phase": self.phase,
            "board": board_to_dict(self.board),
            "turn": self.turn,
            "my_turn": my_turn,
            "you": uid,
            "solo": self.solo,
            "winner": self.winner,
            "last_move": self.last_move,
            "piece_counts": {
                "white": count_pieces(self.board, WHITE),
                "black": count_pieces(self.board, BLACK),
            },
            "highlighted_cells": list(highlighted),
            "valid_dests": {str(k): list(v) for k, v in valid_dests.items()},
        }

    @staticmethod
    def generate_code():
        return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=6))

    def to_dict(self):
        return {
            "code": self.code,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "solo": self.solo,
            "difficulty": self.difficulty,
            "board": board_to_dict(self.board),
            "turn": self.turn,
            "phase": self.phase,
            "winner": self.winner,
            "last_move": self.last_move,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        game = CheckersGame.__new__(CheckersGame)
        game.code = data["code"]
        game.player1_id = data["player1_id"]
        game.player2_id = data.get("player2_id")
        game.solo = data.get("solo", False)
        game.difficulty = data.get("difficulty", 2)
        game.board = dict_to_board(data["board"])
        game.turn = data["turn"]
        game.phase = data.get("phase", "playing")
        game.winner = data.get("winner")
        game.last_move = data.get("last_move")
        game.created_at = data.get("created_at", 0)
        return game
