import random
from typing import Dict, List, Optional, Any, Tuple

from base_game import BaseGame

POINTS = 24
WHITE = 1
BLACK = -1

INITIAL_BOARD: List[int] = [
    -2, 0, 0, 0, 0, 5,
    0, 3, 0, 0, 0, -5,
    5, 0, 0, 0, -3, 0,
    0, 0, 0, -5, 0, 2,
]


def direction(player: int) -> int:
    return 1 if player == WHITE else -1


def opponent(player: int) -> int:
    return BLACK if player == WHITE else WHITE


def is_home(point: int, player: int) -> bool:
    if player == WHITE:
        return 18 <= point < 24
    return 0 <= point < 6


def roll_dice() -> List[int]:
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    if d1 == d2:
        return [d1, d1, d1, d1]
    return [d1, d2]


def can_bear_off(board: List[int], bar: List[int], player: int) -> bool:
    bar_idx = 0 if player == WHITE else 1
    if bar[bar_idx] > 0:
        return False
    for i in range(POINTS):
        v = board[i]
        if (player == WHITE and v > 0) or (player == BLACK and v < 0):
            if not is_home(i, player):
                return False
    return True


def legal_moves_for_die(board: List[int], bar: List[int], off: List[int], player: int, die: int) -> List[Tuple[int, int]]:
    """Return all legal (from, to) moves for a single die value."""
    moves: List[Tuple[int, int]] = []
    dir = direction(player)
    bar_idx = 0 if player == WHITE else 1

    if bar[bar_idx] > 0:
        if player == WHITE:
            enter_to = die - 1
        else:
            enter_to = 24 - die
        if 0 <= enter_to < POINTS:
            target = board[enter_to]
            if (player == WHITE and target >= -1) or (player == BLACK and target <= 1):
                moves.append((-1, enter_to))
        return moves

    for i in range(POINTS):
        v = board[i]
        if (player == WHITE and v <= 0) or (player == BLACK and v >= 0):
            continue
        to_idx = i + dir * die
        if 0 <= to_idx < POINTS:
            target = board[to_idx]
            if (player == WHITE and target >= -1) or (player == BLACK and target <= 1):
                moves.append((i, to_idx))
        else:
            if can_bear_off(board, bar, player) and is_home(i, player):
                moves.append((i, -1))

    return moves


def apply_move(board: List[int], bar: List[int], off: List[int], player: int, from_idx: int, to_idx: int):
    """Mutate the board/bar/off in-place for a single die move."""
    bar_idx = 0 if player == WHITE else 1
    opp_bar_idx = 1 if player == WHITE else 0

    if from_idx == -1:
        bar[bar_idx] -= 1
        if (player == WHITE and board[to_idx] == -1) or (player == BLACK and board[to_idx] == 1):
            bar[opp_bar_idx] += 1
            board[to_idx] = 0
        board[to_idx] += player
        return

    board[from_idx] -= player
    if to_idx == -1:
        off[0 if player == WHITE else 1] += 1
        return

    if (player == WHITE and board[to_idx] == -1) or (player == BLACK and board[to_idx] == 1):
        bar[opp_bar_idx] += 1
        board[to_idx] = 0
    board[to_idx] += player


def board_copy(board: List[int], bar: List[int], off: List[int]) -> Tuple[List[int], List[int], List[int]]:
    return list(board), list(bar), list(off)


def evaluate_move(board: List[int], bar: List[int], off: List[int], player: int, from_idx: int, to_idx: int) -> int:
    """Score a single move for AI selection."""
    score = 0
    if from_idx == -1:
        score += 20
        return score
    v = board[from_idx]
    if abs(v) == 1:
        score -= 8
    if to_idx == -1:
        score += 40
        return score
    if (player == WHITE and board[to_idx] == -1) or (player == BLACK and board[to_idx] == 1):
        score += 30
    after = board[to_idx] + player
    if abs(after) >= 2:
        score += 10
    if is_home(to_idx, player):
        score += 5
    return score


class BackgammonGame(BaseGame):
    def __init__(self, code: str, player1_id: int, player2_id: Optional[int] = None, solo: bool = False, difficulty: int = 2):
        super().__init__(code, player1_id, player2_id, solo, difficulty)
        self.board: List[int] = list(INITIAL_BOARD)
        self.bar: List[int] = [0, 0]
        self.off: List[int] = [0, 0]
        self.dice: List[int] = []
        self.used_dice: int = 0
        self.turn = WHITE
        self.phase = 'playing'
        self.winner: Optional[int] = None
        self.last_move: Optional[List[Tuple[int, int]]] = None

    @property
    def current_player(self):
        return self.player1_id if self.turn == WHITE else self.player2_id

    def player_color(self, uid: int) -> Optional[int]:
        if uid == self.player1_id:
            return WHITE
        if uid == self.player2_id:
            return BLACK
        return None

    def roll(self, uid: int) -> Optional[Dict]:
        color = self.player_color(uid)
        if color is None or color != self.turn or self.phase != 'playing':
            return None
        if not self.solo and self.player2_id is None:
            return None
        if self.dice:
            return None
        self.dice = roll_dice()
        self.used_dice = 0
        return self.get_state(uid)

    def _skip_blocked_dice(self):
        """Skip dice that have no legal moves, so dice[used_dice] is always a playable die."""
        while self.used_dice < len(self.dice):
            die_val = self.dice[self.used_dice]
            if legal_moves_for_die(self.board, self.bar, self.off, self.turn, die_val):
                break
            self.used_dice += 1

    def _make_single_move(self, from_idx: int, to_idx: int) -> bool:
        """Apply one die move. Returns True if the move was valid and applied."""
        if not self.dice or self.used_dice >= len(self.dice):
            return False
        for i in range(self.used_dice, len(self.dice)):
            die_val = self.dice[i]
            allowed = legal_moves_for_die(self.board, self.bar, self.off, self.turn, die_val)
            if (from_idx, to_idx) in allowed:
                apply_move(self.board, self.bar, self.off, self.turn, from_idx, to_idx)
                self.dice[i], self.dice[self.used_dice] = self.dice[self.used_dice], self.dice[i]
                self.used_dice += 1
                return True
        return False

    def _remaining_dice(self) -> List[int]:
        return self.dice[self.used_dice:]

    def _auto_pass(self):
        """Skip dice that have no legal moves. Returns True if no playable dice remain."""
        self._skip_blocked_dice()
        return self.used_dice >= len(self.dice)

    def move(self, uid: int, from_idx: int, to_idx: int) -> Optional[Dict]:
        color = self.player_color(uid)
        if color is None or color != self.turn or self.phase != 'playing':
            return None
        if not self.solo and self.player2_id is None:
            return None
        if not self.dice:
            return None

        self._skip_blocked_dice()
        if self.used_dice >= len(self.dice):
            self._finish_turn()
            return self.get_state(uid)

        ok = self._make_single_move(from_idx, to_idx)
        if not ok:
            return None

        self._auto_pass()

        if self.used_dice >= len(self.dice):
            self._finish_turn()
        return self.get_state(uid)

    def _finish_turn(self):
        if self._finalize_if_won():
            return
        if self.solo:
            self._switch_turn()
            if self.phase == 'playing' and self.turn == BLACK:
                self._bot_play()
                if self._finalize_if_won():
                    return
                if self.phase == 'playing':
                    self._switch_turn()
        else:
            self._switch_turn()

    def _finalize_if_won(self) -> bool:
        if self.off[0] >= 15 or self.off[1] >= 15:
            self.phase = 'finished'
            self.winner = self.player1_id if self.turn == WHITE else self.player2_id
            return True
        return False

    def _switch_turn(self):
        self.dice = []
        self.used_dice = 0
        self.turn = opponent(self.turn)

    def _bot_play(self):
        if self.phase != 'playing' or self.turn != BLACK:
            return
        self.dice = roll_dice()
        self.used_dice = 0
        self.last_move = []
        while self.used_dice < len(self.dice):
            die_val = self.dice[self.used_dice]
            moves = legal_moves_for_die(self.board, self.bar, self.off, BLACK, die_val)
            if not moves:
                self.used_dice += 1
                continue
            scored = [(f, t, evaluate_move(self.board, self.bar, self.off, BLACK, f, t)) for f, t in moves]
            scored.sort(key=lambda x: x[2], reverse=True)
            best = scored[0]
            apply_move(self.board, self.bar, self.off, BLACK, best[0], best[1])
            self.last_move.append((best[0], best[1]))
            self.used_dice += 1

    def pass_turn(self, uid: int) -> Optional[Dict]:
        color = self.player_color(uid)
        if color is None or color != self.turn or self.phase != 'playing':
            return None
        if not self.solo and self.player2_id is None:
            return None
        if not self.dice:
            return None
        if self.used_dice < len(self.dice):
            remaining = self._remaining_dice()
            for die_val in remaining:
                if legal_moves_for_die(self.board, self.bar, self.off, self.turn, die_val):
                    return None
        self._finish_turn()
        return self.get_state(uid)

    def surrender(self, uid: int) -> Optional[Dict]:
        color = self.player_color(uid)
        if color is None or self.phase != 'playing':
            return None
        self.winner = self.player1_id if color == BLACK else (self.player2_id or 0)
        self.phase = 'finished'
        return self.get_state(uid)

    def get_state(self, uid: int) -> Dict[str, Any]:
        color = self.player_color(uid)
        my_turn = self.turn == color
        remaining = self._remaining_dice()
        moves_for_current: List[Tuple[int, int]] = []
        if my_turn and remaining:
            for die_val in remaining:
                moves_for_current.extend(legal_moves_for_die(self.board, self.bar, self.off, self.turn, die_val))
        return {
            'code': self.code,
            'solo': self.solo,
            'difficulty': self.difficulty,
            'phase': self.phase,
            'board': list(self.board),
            'bar': list(self.bar),
            'off': list(self.off),
            'dice': list(self.dice),
            'turn': self.turn,
            'my_color': color,
            'my_turn': my_turn,
            'you': uid,
            'opponent_joined': self.player2_id is not None,
            'winner': self.winner,
            'last_move': self.last_move,
            'legal_moves': [[list(m) for m in [[f, t]]] for f, t in moves_for_current],
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': self.code,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'solo': self.solo,
            'difficulty': self.difficulty,
            'board': list(self.board),
            'bar': list(self.bar),
            'off': list(self.off),
            'dice': list(self.dice),
            'used_dice': self.used_dice,
            'turn': self.turn,
            'phase': self.phase,
            'winner': self.winner,
            'last_move': self.last_move,
            'created_at': self.created_at,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BackgammonGame':
        game = BackgammonGame.__new__(BackgammonGame)
        game._from_dict_common(data)
        game.board = list(data.get('board', INITIAL_BOARD))
        game.bar = list(data.get('bar', [0, 0]))
        game.off = list(data.get('off', [0, 0]))
        game.dice = list(data.get('dice', []))
        game.used_dice = data.get('used_dice', 0)
        game.turn = data.get('turn', WHITE)
        game.phase = data.get('phase', 'playing')
        game.winner = data.get('winner')
        game.last_move = data.get('last_move')
        return game
