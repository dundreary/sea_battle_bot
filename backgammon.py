import random
from typing import Dict, List, Optional, Any, Tuple

from base_game import BaseGame

POINTS = 24
WHITE = 1
BLACK = -1
HEAD = 23  # the "голова" (starting point) for long narde; both colors may sit here

# Short narde = standard/western backgammon starting position.
INITIAL_BOARD_SHORT: List[int] = [
    -2, 0, 0, 0, 0, 5,
    0, 3, 0, 0, 0, -5,
    5, 0, 0, 0, -3, 0,
    0, 0, 0, -5, 0, 2,
]


def direction(player: int, variant: str) -> int:
    # Long narde: both players travel the same rotational direction (toward index 0).
    if variant == 'long':
        return -1
    return 1 if player == WHITE else -1


def opponent(player: int) -> int:
    return BLACK if player == WHITE else WHITE


def is_home(point: int, player: int, variant: str) -> bool:
    if variant == 'long':
        return 0 <= point < 6
    if player == WHITE:
        return 18 <= point < 24
    return 0 <= point < 6


def roll_dice() -> List[int]:
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    if d1 == d2:
        return [d1, d1, d1, d1]
    return [d1, d2]


# --- per-point occupancy helpers (variant-aware) ---------------------------
# Long narde is the only variant where a single point (HEAD) can hold both
# colors at once (only at the very start, before checkers leave the head).
# Everywhere else the "no hitting" rule guarantees a point is single-colour,
# so we keep the compact signed board and track black head checkers separately.

def _own_at(board: List[int], head_black: int, i: int, player: int, variant: str) -> bool:
    if variant == 'long' and i == HEAD:
        return board[HEAD] > 0 if player == WHITE else head_black > 0
    if player == WHITE:
        return board[i] > 0
    return board[i] < 0


def _opp_at(board: List[int], head_black: int, i: int, player: int, variant: str) -> bool:
    if variant == 'long' and i == HEAD:
        return head_black > 0 if player == WHITE else board[HEAD] > 0
    if player == WHITE:
        return board[i] < 0
    return board[i] > 0


def _count_at(board: List[int], head_black: int, i: int, player: int, variant: str) -> int:
    if variant == 'long' and i == HEAD:
        return board[HEAD] if player == WHITE else head_black
    if player == WHITE:
        return board[i] if board[i] > 0 else 0
    return -board[i] if board[i] < 0 else 0


def can_bear_off(board: List[int], head_black: int, bar: List[int], player: int, variant: str) -> bool:
    bar_idx = 0 if player == WHITE else 1
    if bar[bar_idx] > 0:
        return False
    for i in range(POINTS):
        if variant == 'long' and i == HEAD and player == BLACK:
            if head_black > 0:
                return False
            continue
        v = board[i]
        if (player == WHITE and v > 0) or (player == BLACK and v < 0):
            if not is_home(i, player, variant):
                return False
    return True


def legal_moves_for_die(board: List[int], head_black: int, bar: List[int], off: List[int],
                        player: int, die: int, variant: str) -> List[Tuple[int, int]]:
    """Return all legal (from, to) moves for a single die value."""
    moves: List[Tuple[int, int]] = []
    dir = direction(player, variant)
    bar_idx = 0 if player == WHITE else 1

    if bar[bar_idx] > 0:
        if player == WHITE:
            enter_to = die - 1
        else:
            enter_to = 24 - die
        if 0 <= enter_to < POINTS:
            if not _opp_at(board, head_black, enter_to, player, variant):
                moves.append((-1, enter_to))
        return moves

    for i in range(POINTS):
        if not _own_at(board, head_black, i, player, variant):
            continue
        to_idx = i + dir * die
        if 0 <= to_idx < POINTS:
            if not _opp_at(board, head_black, to_idx, player, variant):
                moves.append((i, to_idx))
        else:
            if can_bear_off(board, head_black, bar, player, variant) and is_home(i, player, variant):
                dist = _bear_off_distance(i, player, variant)
                if die == dist:
                    moves.append((i, -1))
                elif die > dist and not _has_higher_checker(board, head_black, i, player, variant):
                    moves.append((i, -1))

    return moves


def apply_move(board: List[int], head_black: int, bar: List[int], off: List[int],
              player: int, from_idx: int, to_idx: int, variant: str) -> int:
    """Mutate the board/bar/off in-place for a single die move.

    Returns the (possibly updated) head_black value.
    """
    bar_idx = 0 if player == WHITE else 1
    opp_bar_idx = 1 if player == WHITE else 0
    off_idx = 0 if player == WHITE else 1

    if from_idx == -1:
        bar[bar_idx] -= 1
        if _opp_at(board, head_black, to_idx, player, variant):
            bar[opp_bar_idx] += 1
            board[to_idx] = 0
        board[to_idx] += player
        return head_black

    # remove from source
    if from_idx == HEAD and variant == 'long':
        if player == WHITE:
            board[HEAD] -= 1
        else:
            head_black -= 1
    else:
        board[from_idx] -= player

    if to_idx == -1:
        off[off_idx] += 1
        return head_black

    if to_idx == HEAD and variant == 'long':
        # Black head checkers are always tracked via head_black.
        if player == WHITE:
            board[HEAD] += 1
        else:
            head_black += 1
        return head_black

    if _opp_at(board, head_black, to_idx, player, variant):
        bar[opp_bar_idx] += 1
        board[to_idx] = 0
    board[to_idx] += player
    return head_black


def _bear_off_distance(point: int, player: int, variant: str) -> int:
    if variant == 'long':
        return point + 1
    if player == WHITE:
        return 24 - point
    return point + 1


def _has_higher_checker(board: List[int], head_black: int, point: int, player: int, variant: str) -> bool:
    if variant == 'long':
        # Higher = smaller index (closer to the off at index 0).
        lo, hi = 0, point
    elif player == WHITE:
        lo, hi = point + 1, POINTS
    else:
        lo, hi = 0, point
    for p in range(lo, hi):
        if _own_at(board, head_black, p, player, variant):
            return True
    # Long narde: a black checker still on the head is "higher" than every home point.
    if variant == 'long' and player == BLACK and head_black > 0:
        return True
    return False


def evaluate_move(board: List[int], head_black: int, bar: List[int], off: List[int],
                  player: int, from_idx: int, to_idx: int, variant: str) -> int:
    """Score a single move for AI selection."""
    score = 0
    if from_idx == -1:
        score += 20
        return score
    if variant == 'long' and from_idx == HEAD:
        # Leaving the head early is good.
        score += 6
    v = _count_at(board, head_black, from_idx, player, variant)
    if v == 1:
        score -= 8
    if to_idx == -1:
        score += 40
        return score
    if _opp_at(board, head_black, to_idx, player, variant):
        score += 30
    after = _count_at(board, head_black, to_idx, player, variant) + 1
    if after >= 2:
        score += 10
    if is_home(to_idx, player, variant):
        score += 5
    return score


class BackgammonGame(BaseGame):
    def __init__(self, code: str, player1_id: int, player2_id: Optional[int] = None,
                 solo: bool = False, difficulty: int = 2, variant: str = 'short'):
        super().__init__(code, player1_id, player2_id, solo, difficulty)
        self.variant = variant if variant in ('short', 'long') else 'short'
        if self.variant == 'long':
            self.board: List[int] = [0] * POINTS
            self.board[HEAD] = 15
            self.head_black: int = 15
        else:
            self.board = list(INITIAL_BOARD_SHORT)
            self.head_black = 0
        self.bar: List[int] = [0, 0]
        self.off: List[int] = [0, 0]
        self.dice: List[int] = []
        self.used_dice: int = 0
        self.turn = WHITE
        self.phase = 'playing'
        self.winner: Optional[int] = None
        self.last_move: Optional[List[Tuple[int, int]]] = None
        self.last_roll: List[int] = []
        self.last_roller: Optional[int] = None
        # Long narde: at most one checker may leave the head per turn on the
        # opening roll (two if the opening roll is a double 6/4/3).
        self.head_first_roll: bool = True
        self.head_moves: int = 0

    @property
    def current_player(self):
        return self.player1_id if self.turn == WHITE else self.player2_id

    def player_color(self, uid: int) -> Optional[int]:
        if uid == self.player1_id:
            return WHITE
        if uid == self.player2_id:
            return BLACK
        return None

    def apply_first_roll(self, pnum: int) -> Optional[Dict]:
        """Opening-roll wrapper: the roll winner moves first.

        Mirrors CheckersGame.apply_first_roll -- the roll is respected in all
        modes (as in Sea Battle and Poker Dice): the winner moves first as
        White (player1), the loser is Black (player2).

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
            self.phase = 'playing'
        return res

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
        self.last_roll = list(self.dice)
        self.last_roller = color
        return self.get_state(uid)

    def _skip_blocked_dice(self):
        """Skip dice that have no legal moves, so dice[used_dice] is always a playable die."""
        while self.used_dice < len(self.dice):
            die_val = self.dice[self.used_dice]
            if legal_moves_for_die(self.board, self.head_black, self.bar, self.off,
                                   self.turn, die_val, self.variant):
                break
            self.used_dice += 1

    def _head_limit(self) -> int:
        if self.variant != 'long' or not self.head_first_roll:
            return 999
        is_double = len(set(self.dice)) == 1
        if is_double and self.dice[0] in (6, 4, 3):
            return 2
        return 1

    def _make_single_move(self, from_idx: int, to_idx: int) -> bool:
        """Apply one die move. Returns True if the move was valid and applied."""
        if not self.dice or self.used_dice >= len(self.dice):
            return False
        if self.variant == 'long' and from_idx == HEAD and self.head_moves >= self._head_limit():
            return False
        for i in range(self.used_dice, len(self.dice)):
            die_val = self.dice[i]
            allowed = legal_moves_for_die(self.board, self.head_black, self.bar, self.off,
                                          self.turn, die_val, self.variant)
            if (from_idx, to_idx) in allowed:
                self.head_black = apply_move(self.board, self.head_black, self.bar, self.off,
                                             self.turn, from_idx, to_idx, self.variant)
                if self.variant == 'long' and from_idx == HEAD:
                    self.head_moves += 1
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
            self._finish_turn(run_bot=True)
            return self.get_state(uid)

        ok = self._make_single_move(from_idx, to_idx)
        if not ok:
            return None

        self._auto_pass()

        if self.used_dice >= len(self.dice):
            self._finish_turn(run_bot=True)
        return self.get_state(uid)

    def _finish_turn(self, run_bot: bool = True):
        if self._finalize_if_won():
            return
        if self.solo:
            self._switch_turn()
            if run_bot and self.phase == 'playing' and self.turn == BLACK:
                self._bot_play()
                if self._finalize_if_won():
                    return
                if self.phase == 'playing':
                    self._switch_turn()
        else:
            self._switch_turn()

    def bot_turn(self) -> Optional[Dict]:
        """Run the AI's full turn (roll + all die moves) as its own step.

        Called by the API layer in a follow-up request right after move() or
        pass_turn() returns the human player's result, so the AI's thinking
        never blocks the response that confirms the player's own move.
        """
        if not self.solo or self.phase != 'playing' or self.turn != BLACK:
            return None
        self._bot_play()
        if self._finalize_if_won():
            return self.get_state(self.player1_id)
        if self.phase == 'playing':
            self._switch_turn()
        return self.get_state(self.player1_id)

    def _finalize_if_won(self) -> bool:
        if self.off[0] >= 15 or self.off[1] >= 15:
            self.phase = 'finished'
            self.winner = self.player1_id if self.turn == WHITE else self.player2_id
            return True
        return False

    def _switch_turn(self):
        self.dice = []
        self.used_dice = 0
        self.head_moves = 0
        self.head_first_roll = False
        self.turn = opponent(self.turn)

    def _bot_play(self):
        if self.phase != 'playing' or self.turn != BLACK:
            return
        self.dice = roll_dice()
        self.used_dice = 0
        self.head_moves = 0
        self.last_roll = list(self.dice)
        self.last_roller = BLACK
        self.last_move = []
        while self.used_dice < len(self.dice):
            die_val = self.dice[self.used_dice]
            if self.variant == 'long' and HEAD in (m[0] for m in
                legal_moves_for_die(self.board, self.head_black, self.bar, self.off,
                                    BLACK, die_val, self.variant)) \
                    and self.head_moves >= self._head_limit():
                self.used_dice += 1
                continue
            moves = legal_moves_for_die(self.board, self.head_black, self.bar, self.off,
                                        BLACK, die_val, self.variant)
            if not moves:
                self.used_dice += 1
                continue
            scored = [(f, t, evaluate_move(self.board, self.head_black, self.bar, self.off,
                                          BLACK, f, t, self.variant)) for f, t in moves]
            scored.sort(key=lambda x: x[2], reverse=True)
            best = scored[0]
            self.head_black = apply_move(self.board, self.head_black, self.bar, self.off,
                                         BLACK, best[0], best[1], self.variant)
            if self.variant == 'long' and best[0] == HEAD:
                self.head_moves += 1
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
                if legal_moves_for_die(self.board, self.head_black, self.bar, self.off,
                                       self.turn, die_val, self.variant):
                    return None
        self._finish_turn(run_bot=True)
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
                moves_for_current.extend(legal_moves_for_die(
                    self.board, self.head_black, self.bar, self.off,
                    self.turn, die_val, self.variant))
        return {
            'code': self.code,
            'solo': self.solo,
            'variant': self.variant,
            'difficulty': self.difficulty,
            'phase': self.phase,
            'board': list(self.board),
            'head_black': self.head_black,
            'bar': list(self.bar),
            'off': list(self.off),
            'dice': list(self.dice),
            'used_dice': self.used_dice,
            'turn': self.turn,
            'my_color': color,
            'my_turn': my_turn,
            'you': uid,
            'opponent_joined': self.player2_id is not None,
            'winner': self.winner,
            'last_move': self.last_move,
            'last_roll': list(self.last_roll),
            'last_roller': self.last_roller,
            'legal_moves': [[list(m) for m in [[f, t]]] for f, t in moves_for_current],
            'my_roll': self.first_roll.get(self.player_num(uid)),
            'opp_roll': (self.first_roll.get(3 - self.player_num(uid))
                         if (self.first_roll.get(1) is not None and self.first_roll.get(2) is not None)
                         else None),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': self.code,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'solo': self.solo,
            'variant': self.variant,
            'difficulty': self.difficulty,
            'board': list(self.board),
            'head_black': self.head_black,
            'bar': list(self.bar),
            'off': list(self.off),
            'dice': list(self.dice),
            'used_dice': self.used_dice,
            'turn': self.turn,
            'phase': self.phase,
            'winner': self.winner,
            'last_move': self.last_move,
            'last_roll': list(self.last_roll),
            'last_roller': self.last_roller,
            'first_roll': self.first_roll_dict(),
            'head_first_roll': self.head_first_roll,
            'head_moves': self.head_moves,
            'created_at': self.created_at,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BackgammonGame':
        game = BackgammonGame.__new__(BackgammonGame)
        game._from_dict_common(data)
        game.variant = data.get('variant', 'short')
        if game.variant == 'long':
            game.board = list(data.get('board', [0] * POINTS))
            if not game.board:
                game.board = [0] * POINTS
            game.head_black = data.get('head_black', 0)
        else:
            game.board = list(data.get('board', INITIAL_BOARD_SHORT))
            game.head_black = 0
        game.bar = list(data.get('bar', [0, 0]))
        game.off = list(data.get('off', [0, 0]))
        game.dice = list(data.get('dice', []))
        game.used_dice = data.get('used_dice', 0)
        game.turn = data.get('turn', WHITE)
        game.phase = data.get('phase', 'playing')
        game.winner = data.get('winner')
        game.last_move = data.get('last_move')
        game.last_roll = list(data.get('last_roll', []))
        game.last_roller = data.get('last_roller')
        game.head_first_roll = data.get('head_first_roll', True)
        game.head_moves = data.get('head_moves', 0)
        return game
