import random
import string
from typing import Dict, List, Optional, Any, Set


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

    rank = 7
    score = sum(dice)
    name = f"Nothing ({score})"

    if sorted_counts[0] == 5:
        rank, score, name = 0, 50, 'Five of a Kind'
    elif sorted_counts[0] == 4:
        rank, score, name = 1, 40, 'Four of a Kind'
    elif sorted_counts[0] == 3 and len(sorted_counts) > 1 and sorted_counts[1] >= 2:
        rank, score, name = 2, 30, 'Full House'
    elif len(counts) == 5 and unique[-1] - unique[0] == 4:
        rank, score, name = 3, 25, 'Straight'
    elif sorted_counts[0] == 3:
        rank, score, name = 4, 20, 'Three of a Kind'
    elif sorted_counts[0] == 2 and len(sorted_counts) > 1 and sorted_counts[1] == 2:
        rank, score, name = 5, 15, 'Two Pair'
    elif sorted_counts[0] == 2:
        rank, score, name = 6, 10, 'One Pair'

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


class PokerDiceGame:
    def __init__(self, code: str, player1_id: int, player2_id: Optional[int] = None, solo: bool = False):
        self.code = code
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.solo = solo
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
            'scorecard': {c: None for c in CATEGORY_IDS},
            'dice_history': [],
        }

    def _reset_player(self, pnum: int):
        p = self.players[pnum]
        p['dice'] = []
        p['rolls'] = 3
        p['scored'] = False
        p['hand'] = None
        p['dice_history'] = []

    def player_num(self, uid: int) -> Optional[int]:
        if uid == self.player1_id:
            return 1
        if uid == self.player2_id:
            return 2
        return None

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

        p['scorecard'][category] = score_for_category(p['dice'], category)
        p['hand'] = evaluate(p['dice'])
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

        p['dice'] = [random.randint(1, 6) for _ in range(5)]
        p['rolls'] = 0
        p['dice_history'] = [list(p['dice'])]

        remaining = _remaining_categories(p['scorecard'])
        best_cat = remaining[0]
        best_score = -1
        for cat in remaining:
            s = score_for_category(p['dice'], cat)
            if s > best_score:
                best_score = s
                best_cat = cat

        p['scorecard'][best_cat] = best_score
        p['hand'] = evaluate(p['dice'])
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
            'hand_rank': p['hand']['rank'] if p['hand'] else None,
            'hand_score': p['hand']['score'] if p['hand'] else None,
            'hand_name': p['hand']['name'] if p['hand'] else None,
            'opponent_scored': opp['scored'],
            'opponent_hand_rank': opp['hand']['rank'] if opp['hand'] else None,
            'opponent_hand_score': opp['hand']['score'] if opp['hand'] else None,
            'opponent_hand_name': opp['hand']['name'] if opp['hand'] else None,
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

    @staticmethod
    def generate_code() -> str:
        return ''.join(random.choices(string.ascii_uppercase, k=6))


games: Dict[str, PokerDiceGame] = {}
player_games: Dict[str, str] = {}
