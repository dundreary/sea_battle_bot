import random
from typing import Dict, List, Optional, Any, Set

from base_game import BaseGame


CATEGORY_IDS = [
    'ones', 'twos', 'threes', 'fours', 'fives', 'sixes',
    'pair', 'two_pairs', 'three_of_kind', 'four_of_kind',
    'full_house', 'small_straight', 'large_straight', 'five_of_kind', 'chance',
]

CATEGORY_NAMES = {
    'ru': ['Единицы', 'Двойки', 'Тройки', 'Четверки', 'Пятерки', 'Шестерки',
           'Пара', 'Две пары', 'Тройка', 'Каре',
           'Фулл-хаус', 'Малый стрит', 'Большой стрит', 'Покер', 'Шанс'],
    'en': ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes',
           'One Pair', 'Two Pairs', 'Three of a Kind', 'Four of a Kind',
           'Full House', 'Small Straight', 'Large Straight', 'Five of a Kind', 'Chance'],
    'uk': ['Очки', 'Двійки', 'Трійки', 'Четвірки', "П'ятірки", 'Шістки',
           'Пара', 'Дві пари', 'Трійка', 'Каре',
           'Фулл-хаус', 'Малий стрит', 'Великий стрит', 'Покер', 'Шанс'],
}

BONUS_THRESHOLD = 63
BONUS_SCORE = 35


def score_for_category(dice: List[int], category: str) -> int:
    counts = {}
    for d in dice:
        counts[d] = counts.get(d, 0) + 1
    sorted_counts = sorted(counts.values(), reverse=True)

    if category == 'ones':
        return sum(d for d in dice if d == 1)
    if category == 'twos':
        return sum(d for d in dice if d == 2)
    if category == 'threes':
        return sum(d for d in dice if d == 3)
    if category == 'fours':
        return sum(d for d in dice if d == 4)
    if category == 'fives':
        return sum(d for d in dice if d == 5)
    if category == 'sixes':
        return sum(d for d in dice if d == 6)
    if category == 'chance':
        return sum(dice)
    if category == 'pair':
        return sum(dice) if sorted_counts and sorted_counts[0] >= 2 else 0
    if category == 'two_pairs':
        return sum(dice) if len(sorted_counts) >= 2 and sorted_counts[0] >= 2 and sorted_counts[1] >= 2 else 0
    if category == 'three_of_kind':
        return sum(dice) if sorted_counts and sorted_counts[0] >= 3 else 0
    if category == 'four_of_kind':
        return sum(dice) if sorted_counts and sorted_counts[0] >= 4 else 0
    if category == 'full_house':
        return 25 if sorted_counts[0] == 3 and len(sorted_counts) > 1 and sorted_counts[1] >= 2 else 0
    if category == 'small_straight':
        unique = sorted(set(dice))
        for i in range(len(unique) - 3):
            if unique[i + 3] - unique[i] == 3:
                return 30
        return 0
    if category == 'large_straight':
        unique = sorted(set(dice))
        if len(unique) == 5 and unique[-1] - unique[0] == 4:
            return 40
        return 0
    if category == 'five_of_kind':
        return 50 if sorted_counts and sorted_counts[0] == 5 else 0
    return 0


def evaluate(dice: List[int]) -> Dict[str, Any]:
    counts = {}
    for d in dice:
        counts[d] = counts.get(d, 0) + 1
    sorted_counts = sorted(counts.values(), reverse=True)
    unique = sorted(counts.keys())

    rank = 8
    score = sum(dice)
    name = f"Nothing ({score})"

    if sorted_counts[0] == 5:
        rank, score, name = 0, 50, 'Five of a Kind'
    elif sorted_counts[0] == 4:
        rank, score, name = 1, sum(dice), 'Four of a Kind'
    elif sorted_counts[0] == 3 and len(sorted_counts) > 1 and sorted_counts[1] >= 2:
        rank, score, name = 2, 25, 'Full House'
    elif len(counts) == 5 and unique[-1] - unique[0] == 4:
        rank, score, name = 3, 40, 'Large Straight'
    elif any(unique[i + 3] - unique[i] == 3 for i in range(len(unique) - 3)):
        rank, score, name = 4, 30, 'Small Straight'
    elif sorted_counts[0] == 3:
        rank, score, name = 5, sum(dice), 'Three of a Kind'
    elif sorted_counts[0] == 2 and len(sorted_counts) > 1 and sorted_counts[1] == 2:
        rank, score, name = 6, sum(dice), 'Two Pair'
    elif sorted_counts[0] == 2:
        rank, score, name = 7, sum(dice), 'One Pair'

    return {'rank': rank, 'score': score, 'name': name}


def _upper_sum(scorecard: Dict[str, Optional[int]]) -> int:
    return sum(scorecard.get(c, 0) or 0 for c in ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes'])


def _total_score(scorecard: Dict[str, Optional[int]]) -> int:
    total = sum(v for v in scorecard.values() if v is not None)
    if _upper_sum(scorecard) >= BONUS_THRESHOLD:
        total += BONUS_SCORE
    return total


def _remaining_categories(scorecard: Dict[str, Optional[int]]) -> List[str]:
    return [c for c in CATEGORY_IDS if scorecard.get(c) is None]


# ---------------------------------------------------------------------------
# Bot AI (difficulty-aware)
#
# Difficulty levels (mirrors the Checkers picker: 1=Easy, 2=Normal, 3=Hard):
#   1 Easy   - single roll, scores the highest raw category (legacy behaviour)
#   2 Normal - up to 3 rolls with a simple keep heuristic, best raw category
#   3 Hard   - up to 3 rolls with 2-ply Monte-Carlo expectimax keep decisions
#             and marginal-value category choice with upper-bonus awareness
# ---------------------------------------------------------------------------

_KEEP_ALL = 0b11111


def _keep_candidates(dice: List[int]) -> List[int]:
    """Small set of realistic keep-masks (avoids the full 32-mask search).

    Covers: keep everything, keep the modal group, keep all non-singles
    (pursues two pairs / full house), and keep the longest consecutive run.
    This is both far faster and almost always contains the optimal keep.
    """
    counts: Dict[int, int] = {}
    for d in dice:
        counts[d] = counts.get(d, 0) + 1
    masks = {_KEEP_ALL}
    maxc = max(counts.values())
    if maxc >= 2:
        mode = [d for d, c in counts.items() if c == maxc][0]
        masks.add(sum(1 << i for i, d in enumerate(dice) if d == mode))
        masks.add(sum(1 << i for i, d in enumerate(dice) if counts[d] >= 2))
    uniq = sorted(set(dice))
    best: List[int] = []
    cur = [uniq[0]]
    for x in uniq[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            cur = [x]
        if len(cur) > len(best):
            best = list(cur)
    if len(best) >= 2:
        masks.add(sum(1 << i for i, d in enumerate(dice) if d in best))
    return list(masks)


def _compute_expected_values(samples: int = 20000) -> Dict[str, float]:
    ev: Dict[str, float] = {}
    for c in CATEGORY_IDS:
        total = 0
        for _ in range(samples):
            dice = [random.randint(1, 6) for _ in range(5)]
            total += score_for_category(dice, c)
        ev[c] = total / samples
    return ev


# Lazily computed on first use (Hard difficulty only) and cached, instead of
# blocking module import with 300k rolls. See _expected_value().
_EXPECTED_VALUE_CACHE: Dict[str, float] = {}


def _expected_value() -> Dict[str, float]:
    global _EXPECTED_VALUE_CACHE
    if not _EXPECTED_VALUE_CACHE:
        _EXPECTED_VALUE_CACHE = _compute_expected_values()
    return _EXPECTED_VALUE_CACHE


def _bot_keep_simple(dice: List[int]) -> int:
    """Greedy keep heuristic for Normal difficulty.

    Keeps the largest matching group (pair/triple/...), or the longest
    consecutive run when there is no group.
    """
    counts: Dict[int, int] = {}
    for d in dice:
        counts[d] = counts.get(d, 0) + 1
    max_count = max(counts.values())
    if max_count >= 2:
        mode = [d for d, c in counts.items() if c == max_count][0]
        return sum(1 << i for i, d in enumerate(dice) if d == mode)
    uniq = sorted(set(dice))
    best_run: List[int] = []
    cur: List[int] = [uniq[0]]
    for x in uniq[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            cur = [x]
        if len(cur) > len(best_run):
            best_run = list(cur)
    return sum(1 << i for i, d in enumerate(dice) if d in best_run)


def _bot_ev(dice: List[int], rolls_left: int, remaining: List[str], r_samples: int = 16) -> float:
    """Expected marginal value of the best play from this dice state.

    Leaf (rolls_left <= 0): best category value minus its baseline expected
    value, so the bot does not waste a high-value category on a weak roll.
    """
    if rolls_left <= 0:
        return max(score_for_category(dice, c) - _expected_value()[c] for c in remaining)
    best = -1e18
    for mask in _keep_candidates(dice):
        s = 0.0
        for _ in range(r_samples):
            nd = [dice[i] if (mask >> i) & 1 else random.randint(1, 6) for i in range(5)]
            s += _bot_ev(nd, rolls_left - 1, remaining, r_samples)
        val = s / r_samples
        if val > best:
            best = val
    return best


def _bot_best_keep(dice: List[int], rolls_left: int, remaining: List[str], r_samples: int = 16) -> int:
    """Pick the keep-mask that maximises expected marginal value."""
    best_mask = _KEEP_ALL
    best_val = -1e18
    for mask in _keep_candidates(dice):
        s = 0.0
        for _ in range(r_samples):
            nd = [dice[i] if (mask >> i) & 1 else random.randint(1, 6) for i in range(5)]
            s += _bot_ev(nd, rolls_left - 1, remaining, r_samples)
        val = s / r_samples
        if val > best_val:
            best_val = val
            best_mask = mask
    return best_mask


def _bot_choose_category(dice: List[int], remaining: List[str], scorecard: Dict[str, Optional[int]]) -> str:
    """Choose the category maximising marginal value, nudged toward the
    upper-section bonus (>=63 gives +35) when still reachable."""
    upper = ('ones', 'twos', 'threes', 'fours', 'fives', 'sixes')
    upper_sum = _upper_sum(scorecard)
    best_cat = remaining[0]
    best_val = -1e18
    for c in remaining:
        val = score_for_category(dice, c) - _expected_value()[c]
        if c in upper and upper_sum < 63:
            gap = 63 - upper_sum
            contrib = score_for_category(dice, c)
            val += 35.0 * min(contrib, gap) / 63.0 * 0.5
        if val > best_val:
            best_val = val
            best_cat = c
    return best_cat


class PokerDiceGame(BaseGame):
    def __init__(self, code: str, player1_id: int, player2_id: Optional[int] = None, solo: bool = False, difficulty: int = 3):
        super().__init__(code, player1_id, player2_id, solo, difficulty)
        self.phase = 'playing'
        self.turn = 1
        self.surrendered = None
        self.players = {
            1: self._fresh_player(),
            2: self._fresh_player(),
        }

    def _fresh_player(self):
        return {
            'dice': [],
            'rolls': 3,
            'scored': False,
            'hand': None,
            'last_scored_category': None,
            'last_scored_score': None,
            'scorecard': {c: None for c in CATEGORY_IDS},
            'dice_history': [],
        }

    def _reset_player(self, pnum: int):
        p = self.players[pnum]
        p['dice'] = []
        p['rolls'] = 3
        p['scored'] = False
        p['hand'] = None
        p['last_scored_category'] = None
        p['last_scored_score'] = None
        p['dice_history'] = []

    def roll(self, uid: int, keep_indices: Optional[List[int]] = None) -> Optional[Dict]:
        pnum = self.player_num(uid)
        if pnum is None or pnum != self.turn or self.phase != 'playing':
            return None
        p = self.players[pnum]

        if not _remaining_categories(p['scorecard']):
            return None

        if p['scored']:
            self._reset_player(pnum)
        elif p['rolls'] <= 0:
            return None

        keep: Set[int] = set(keep_indices or [])
        prev = p['dice'] or [0] * 5
        dice = []
        for i in range(5):
            if i in keep and prev:
                dice.append(prev[i])
            else:
                dice.append(random.randint(1, 6))

        p['dice'] = dice
        p['rolls'] -= 1
        p['dice_history'].append(list(dice))

        return self.get_state(pnum)

    def score(self, uid: int, category: str) -> Optional[Dict]:
        pnum = self.player_num(uid)
        if pnum is None or pnum != self.turn or self.phase != 'playing':
            return None
        p = self.players[pnum]
        if p['scored'] or not p['dice']:
            return None
        if category not in CATEGORY_IDS:
            return None
        if p['scorecard'].get(category) is not None:
            return None
        if not _remaining_categories(p['scorecard']):
            return None

        scored_points = score_for_category(p['dice'], category)
        p['scorecard'][category] = scored_points
        p['hand'] = evaluate(p['dice'])
        p['last_scored_category'] = category
        p['last_scored_score'] = scored_points
        p['scored'] = True

        self._advance_turn(pnum)

        return self.get_state(pnum)

    def _advance_turn(self, pnum: int):
        p1_remaining = _remaining_categories(self.players[1]['scorecard'])
        p2_remaining = _remaining_categories(self.players[2]['scorecard'])

        if not p1_remaining and not p2_remaining:
            self.phase = 'finished'
            return

        if self.solo:
            if pnum == 1:
                if p2_remaining:
                    self.turn = 2
                    self._bot_play()
                else:
                    self.turn = 1
                    if self.players[1]['scored']:
                        self._reset_player(1)
            else:
                if p1_remaining:
                    self.turn = 1
                    self._reset_player(1)
                else:
                    self.phase = 'finished'
        else:
            next_pnum = 3 - pnum
            next_rem = p1_remaining if next_pnum == 1 else p2_remaining
            if next_rem:
                self.turn = next_pnum
                if self.players[next_pnum]['scored']:
                    self._reset_player(next_pnum)
            else:
                curr_rem = p1_remaining if pnum == 1 else p2_remaining
                if curr_rem:
                    self.turn = pnum
                    if self.players[pnum]['scored']:
                        self._reset_player(pnum)
                else:
                    self.phase = 'finished'

    def _bot_play(self):
        p = self.players[2]
        if not _remaining_categories(p['scorecard']):
            self._advance_turn(2)
            return

        # Player 2 is never reset by _advance_turn, so reset it each bot turn.
        self._reset_player(2)
        remaining = _remaining_categories(p['scorecard'])
        diff = self.difficulty

        def _bot_roll(keep_mask: int):
            fresh = []
            for i in range(5):
                if (keep_mask >> i) & 1 and len(p['dice']) == 5:
                    fresh.append(p['dice'][i])
                else:
                    fresh.append(random.randint(1, 6))
            p['dice'] = fresh
            if p['rolls'] > 0:
                p['rolls'] -= 1
            p['dice_history'].append(list(fresh))

        if diff <= 1:
            # Easy: one roll, score the highest raw category (legacy behaviour).
            _bot_roll(0)
            best_cat = max(remaining, key=lambda c: score_for_category(p['dice'], c))
        else:
            # Normal / Hard: up to 3 rolls, choosing which dice to keep.
            _bot_roll(0)
            while p['rolls'] > 0:
                if diff == 2:
                    mask = _bot_keep_simple(p['dice'])
                else:
                    mask = _bot_best_keep(p['dice'], p['rolls'], remaining)
                if mask == _KEEP_ALL:
                    break
                _bot_roll(mask)
            best_cat = _bot_choose_category(p['dice'], remaining, p['scorecard'])

        scored_points = score_for_category(p['dice'], best_cat)
        p['scorecard'][best_cat] = scored_points
        p['hand'] = evaluate(p['dice'])
        p['last_scored_category'] = best_cat
        p['last_scored_score'] = scored_points
        p['scored'] = True

        self._advance_turn(2)

    def _get_winner(self):
        if self.phase != 'finished':
            return None
        if self.surrendered:
            if self.surrendered == 1:
                return self.player2_id if self.player2_id else 0
            return self.player1_id
        total1 = _total_score(self.players[1]['scorecard'])
        total2 = _total_score(self.players[2]['scorecard'])
        if total1 > total2:
            return self.player1_id
        if total2 > total1:
            return self.player2_id if self.player2_id else 0
        return -1

    def get_state(self, pnum: int) -> Dict[str, Any]:
        p = self.players[pnum]
        opp = self.players[3 - pnum]

        winner = self._get_winner()
        my_total = _total_score(p['scorecard'])
        opp_total = _total_score(opp['scorecard'])
        my_upper = _upper_sum(p['scorecard'])

        my_sc = {}
        for c in CATEGORY_IDS:
            val = p['scorecard'].get(c)
            if val is not None:
                my_sc[c] = val
        opp_sc = {}
        for c in CATEGORY_IDS:
            val = opp['scorecard'].get(c)
            if val is not None:
                opp_sc[c] = val

        my_turn = self.turn == pnum
        # A saved hand describes the previous scored turn.  The UI needs the
        # combination formed by the dice currently visible on the table.
        my_hand = evaluate(p['dice']) if p['dice'] else None
        opponent_hand = evaluate(opp['dice']) if opp['dice'] else None

        return {
            'code': self.code,
            'solo': self.solo,
            'phase': self.phase,
            'turn': self.turn,
            'my_turn': my_turn,
            'opponent_joined': self.player2_id is not None,
            'you': pnum,
            'dice': p['dice'] if my_turn else opp['dice'],
            'my_dice': p['dice'],
            'rolls_left': p['rolls'] if my_turn else opp['rolls'],
            'scored': p['scored'],
            'hand_rank': my_hand['rank'] if my_hand else None,
            'hand_score': my_hand['score'] if my_hand else None,
            'hand_name': my_hand['name'] if my_hand else None,
            'opponent_scored': opp['scored'],
            'opponent_hand_rank': opponent_hand['rank'] if opponent_hand else None,
            'opponent_hand_score': opponent_hand['score'] if opponent_hand else None,
            'opponent_hand_name': opponent_hand['name'] if opponent_hand else None,
            'opponent_scored_category': opp['last_scored_category'] if opp['scored'] else None,
            'opponent_scored_points': opp['last_scored_score'] if opp['scored'] else None,
            'winner': winner,
            'you_id': self.player1_id if pnum == 1 else self.player2_id,
            'scorecard': my_sc,
            'opponent_scorecard': opp_sc,
            'scorecard_all': {c: p['scorecard'][c] for c in CATEGORY_IDS},
            'opponent_scorecard_all': {c: opp['scorecard'][c] for c in CATEGORY_IDS},
            'total_score': my_total,
            'opponent_total_score': opp_total,
            'upper_sum': my_upper,
            'bonus': my_upper >= BONUS_THRESHOLD,
            'opponent_upper_sum': _upper_sum(opp['scorecard']),
            'opponent_bonus': _upper_sum(opp['scorecard']) >= BONUS_THRESHOLD,
            'opponent_dice': opp['dice'],
            'categories_left': _remaining_categories(p['scorecard']),
            'opponent_categories_left': _remaining_categories(opp['scorecard']),
            'max_categories': len(CATEGORY_IDS),
            'dice_history': p['dice_history'] if my_turn else opp['dice_history'],
        }

    def surrender(self, uid: int) -> Optional[Dict]:
        pnum = self.player_num(uid)
        if pnum is None or self.phase != 'playing':
            return None
        p = self.players[pnum]
        for cat in _remaining_categories(p['scorecard']):
            p['scorecard'][cat] = 0
        self.surrendered = pnum
        self.phase = 'finished'
        return self.get_state(pnum)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': self.code,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'solo': self.solo,
            'difficulty': self.difficulty,
            'phase': self.phase,
            'turn': self.turn,
            'surrendered': self.surrendered,
            'players': {
                str(k): {
                    'dice': list(v['dice']),
                    'rolls': v['rolls'],
                    'scored': v['scored'],
                    'hand': v['hand'],
                    'last_scored_category': v['last_scored_category'],
                    'last_scored_score': v['last_scored_score'],
                    'scorecard': dict(v['scorecard']),
                    'dice_history': [list(h) for h in v['dice_history']],
                }
                for k, v in self.players.items()
            },
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PokerDiceGame':
        game = PokerDiceGame.__new__(PokerDiceGame)
        game._from_dict_common(data)
        game.phase = data.get('phase', 'playing')
        game.turn = data.get('turn', 1)
        game.surrendered = data.get('surrendered')
        game.players = {}
        for k, v in data.get('players', {}).items():
            pnum = int(k)
            game.players[pnum] = {
                'dice': list(v.get('dice', [])),
                'rolls': v.get('rolls', 3),
                'scored': v.get('scored', False),
                'hand': v.get('hand'),
                'last_scored_category': v.get('last_scored_category'),
                'last_scored_score': v.get('last_scored_score'),
                'scorecard': {c: v.get('scorecard', {}).get(c) for c in CATEGORY_IDS},
                'dice_history': [list(h) for h in v.get('dice_history', [])],
            }
        if game.solo and game.player2_id is None:
            game.player2_id = 0
        return game
