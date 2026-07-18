from base_game import BaseGame

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


def get_directions(piece, capture=False):
    if capture or piece in (WHITE_KING, BLACK_KING):
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if piece == WHITE:
        return [(-1, -1), (-1, 1)]
    if piece == BLACK:
        return [(1, -1), (1, 1)]
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
    for dr, dc in get_directions(piece, capture=True):
        mr, mc = r + dr, c + dc
        nr, nc = r + 2 * dr, c + 2 * dc
        if in_bounds(nr, nc) and board[nr][nc] == EMPTY and in_bounds(mr, mc):
            mid = board[mr][mc]
            # Russian draughts (§6.1.5.9): you may pass through the same square
            # more than once; only re-jumping the same opponent piece is
            # forbidden. Captured pieces are also removed from the board as we
            # recurse, so the capture sequence stays finite either way.
            if mid != EMPTY and piece_color(mid) != color and (mr, mc) not in captured:
                new_board = [row[:] for row in board]
                new_board[mr][mc] = EMPTY
                new_board[r][c] = EMPTY
                new_piece = piece
                if piece == WHITE and nr == 0:
                    new_piece = WHITE_KING
                elif piece == BLACK and nr == BOARD_SIZE - 1:
                    new_piece = BLACK_KING
                new_board[nr][nc] = new_piece
                # Russian draughts (§6.1.5.15): if a man reaches the back rank
                # during a capture and a further capture is available, it MUST
                # continue the same move as a king. So we never stop on
                # promotion — we simply recurse with the promoted piece. Kings
                # (already kings) recurse as well. The sequence ends only when
                # no further capture is possible (the leaf case below).
                sub = find_multi_captures(
                    new_board, nr, nc, new_piece,
                    path + [(nr, nc)], captured + [(mr, mc)],
                    start_pos,
                )
                if sub:
                    moves.extend(sub)
                else:
                    moves.append((start_pos, path[1:] + [(nr, nc)], list(captured + [(mr, mc)])))
    return moves


def get_all_captures(board, color):
    # Russian draughts (§6.1.5.14): capturing is mandatory, but the player may
    # choose ANY capture sequence — there is no forced maximum number of pieces
    # and no forced "capture a king" rule. So we return every legal capture
    # sequence; the mover (human or AI) chooses freely among them.
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
    fr, fc = steps[-1]
    new_board[fr][fc] = current_piece
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


class CheckersGame(BaseGame):
    def __init__(self, code, player1_id, player2_id=None, solo=False, difficulty=2):
        super().__init__(code, player1_id, player2_id, solo, difficulty)
        self.board = initial_board()
        self.turn = WHITE
        self.phase = "playing"
        self.winner = None
        self.draw = False
        self.no_progress_plies = 0
        self.last_move = None
        # Draw detection. `_seen` counts how many times each position (board +
        # side to move) has occurred, used for the threefold-repetition rule.
        self._seen = {}
        self._record_position()

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

    def apply_first_roll(self, pnum):
        """Opening-roll wrapper: the roll winner moves first.

        Colour was previously fixed by join order (player1 always White), so
        the roll only decided move order, not colour. Now the roll is
        respected in all modes: the winner moves first as White (player1),
        the loser is Black (player2) -- exactly like Sea Battle and Poker
        Dice.

        In multiplayer a winning player 2 is swapped into the player1 slot
        (which player_color() already maps to White), so after the swap the
        winner is always White. In SOLO mode the human is player1 and the bot
        is player2, so no swap is needed: the winner simply gets the
        corresponding turn (WHITE if the human won, BLACK if the bot won).
        Because the existing bot-turn handler only acts when the bot is BLACK,
        setting turn=BLACK when the bot wins means the bot opens first, as
        intended -- no handler changes required.
        """
        res = self.roll_for_first(pnum)
        if res and res.get("winner"):
            winner = res["winner"]
            if winner == 2 and not self.solo:
                self.player1_id, self.player2_id = self.player2_id, self.player1_id
            if (winner == 1) or (winner == 2 and not self.solo):
                self.turn = WHITE
            else:
                self.turn = BLACK
            self.phase = "playing"
        return res

    def _position_key(self):
        # A position is the board configuration together with the side to move.
        return (tuple(board_to_dict(self.board)), self.turn)

    def _record_position(self):
        key = self._position_key()
        self._seen[key] = self._seen.get(key, 0) + 1
        return self._seen[key]

    def get_moves_for_color(self, color):
        return get_legal_moves(self.board, color)

    def make_move(self, move):
        sr, sc = move[0]
        moved_piece = self.board[sr][sc]
        captures = move[2] if len(move) > 2 else []
        self.board = apply_move(self.board, move)
        self.last_move = move
        # No-progress draw rule (Russian draughts): a capture or a man's forward
        # advance resets the counter; otherwise it increments. 30 plies (~15
        # full moves) without progress ends the game as a draw.
        if captures:
            self.no_progress_plies = 0
        else:
            advanced = False
            if moved_piece in (WHITE, BLACK):
                fr, _ = move[1][-1]
                if (moved_piece == WHITE and fr < sr) or (moved_piece == BLACK and fr > sr):
                    advanced = True
            self.no_progress_plies = 0 if advanced else self.no_progress_plies + 1
        self.switch_turn()
        occurrences = self._record_position()
        if not has_pieces(self.board, self.turn):
            self.winner = opponent(self.turn)
            self.phase = "finished"
            return True
        if not self.get_moves_for_color(self.turn):
            self.winner = opponent(self.turn)
            self.phase = "finished"
            return True
        # Draw: same position (board + side to move) occurred three times.
        if occurrences >= 3:
            self.winner = None
            self.draw = True
            self.phase = "finished"
            return True
        # Draw: 30 plies of non-capturing king-only moves (~15 each).
        if self.no_progress_plies >= 30:
            self.winner = None
            self.draw = True
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
            "my_color": color,
            "my_turn": my_turn,
            "you": uid,
            "solo": self.solo,
            "opponent_joined": self.player2_id is not None,
            "my_roll": self.first_roll.get(self.player_num(uid)),
            "opp_roll": (self.first_roll.get(3 - self.player_num(uid))
                         if (self.first_roll.get(1) is not None and self.first_roll.get(2) is not None)
                         else None),
            "winner": self.winner,
            "draw": self.draw,
            "last_move": self.last_move,
            "piece_counts": {
                "white": count_pieces(self.board, WHITE),
                "black": count_pieces(self.board, BLACK),
            },
            "highlighted_cells": list(highlighted),
            "valid_dests": {str(k): list(v) for k, v in valid_dests.items()},
        }

    def surrender(self, uid):
        color = self.player_color(uid)
        if color is None:
            return None
        self.winner = opponent(color)
        self.phase = "finished"
        return self.get_state(uid)

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
            "draw": self.draw,
            "no_progress_plies": self.no_progress_plies,
            "last_move": self.last_move,
            "created_at": self.created_at,
            "first_roll": self.first_roll_dict(),
            # Repetition history, so threefold-draw detection survives a
            # restart. Position key is (flattened_board, side_to_move).
            "seen": [[list(k[0]), k[1], v] for k, v in self._seen.items()],
        }

    @staticmethod
    def from_dict(data):
        game = CheckersGame.__new__(CheckersGame)
        game._from_dict_common(data)
        game.board = dict_to_board(data["board"])
        game.turn = data["turn"]
        game.phase = data.get("phase", "playing")
        game.winner = data.get("winner")
        game.draw = data.get("draw", False)
        game.no_progress_plies = data.get("no_progress_plies", 0)
        game.last_move = data.get("last_move")
        # Restore repetition history so threefold-draw detection survives a
        # restart. Stored as [[flattened_board, side_to_move, count], ...].
        seen_raw = data.get("seen")
        if seen_raw:
            game._seen = {(tuple(item[0]), item[1]): item[2] for item in seen_raw}
        else:
            game._seen = {}
            game._record_position()
        return game
