import random
import time
from typing import Dict, List, Optional, Any

ONES, TWOS, THREES, FOURS, FIVES, SIXES = range(6)
THREE_KIND, FOUR_KIND, FULL_HOUSE, SM_STRAIGHT, LG_STRAIGHT, YAHTZEE, CHANCE = range(6, 13)

CATEGORIES_RU = {
    ONES: "Единицы", TWOS: "Двойки", THREES: "Тройки", FOURS: "Четверки",
    FIVES: "Пятерки", SIXES: "Шестерки", THREE_KIND: "Тройка",
    FOUR_KIND: "Каре", FULL_HOUSE: "Фулл-хаус", SM_STRAIGHT: "Малый стрит",
    LG_STRAIGHT: "Большой стрит", YAHTZEE: "Покер", CHANCE: "Шанс",
}

CATEGORIES_UK = {
    ONES: "Одиниці", TWOS: "Двійки", THREES: "Трійки", FOURS: "Четвірки",
    FIVES: "П'ятірки", SIXES: "Шістки", THREE_KIND: "Трійка",
    FOUR_KIND: "Каре", FULL_HOUSE: "Фул-хаус", SM_STRAIGHT: "Малий стрит",
    LG_STRAIGHT: "Великий стрит", YAHTZEE: "Покер", CHANCE: "Шанс",
}

CATEGORIES_EN = {
    ONES: "Ones", TWOS: "Twos", THREES: "Threes", FOURS: "Fours",
    FIVES: "Fives", SIXES: "Sixes", THREE_KIND: "Three of a Kind",
    FOUR_KIND: "Four of a Kind", FULL_HOUSE: "Full House",
    SM_STRAIGHT: "Small Straight", LG_STRAIGHT: "Large Straight",
    YAHTZEE: "Yahtzee", CHANCE: "Chance",
}

UPPER = {ONES, TWOS, THREES, FOURS, FIVES, SIXES}
ALL_CATS = list(range(13))


def upper_sum(scores: Dict[int, int]) -> int:
    return sum(scores.get(c, 0) for c in UPPER)


def grand_total(scores: Dict[int, int]) -> int:
    total = sum(scores.values())
    if upper_sum(scores) >= 63:
        total += 35
    return total


def _has_n(dice: List[int], n: int) -> bool:
    for d in set(dice):
        if dice.count(d) >= n:
            return True
    return False


def sc_upper(dice: List[int], face: int) -> int:
    return sum(d for d in dice if d == face)


def sc_three_kind(dice: List[int]) -> int:
    return sum(dice) if _has_n(dice, 3) else 0


def sc_four_kind(dice: List[int]) -> int:
    return sum(dice) if _has_n(dice, 4) else 0


def sc_full_house(dice: List[int]) -> int:
    return 25 if sorted([dice.count(d) for d in set(dice)]) == [2, 3] else 0


def sc_sm_straight(dice: List[int]) -> int:
    vals = sorted(set(dice))
    for i in range(len(vals) - 3):
        if vals[i + 3] - vals[i] == 3:
            return 30
    return 0


def sc_lg_straight(dice: List[int]) -> int:
    vals = sorted(set(dice))
    return 40 if vals in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]) else 0


def sc_yahtzee(dice: List[int]) -> int:
    return 50 if len(set(dice)) == 1 else 0


def sc_chance(dice: List[int]) -> int:
    return sum(dice)


SCORE = {
    ONES: lambda d: sc_upper(d, 1),
    TWOS: lambda d: sc_upper(d, 2),
    THREES: lambda d: sc_upper(d, 3),
    FOURS: lambda d: sc_upper(d, 4),
    FIVES: lambda d: sc_upper(d, 5),
    SIXES: lambda d: sc_upper(d, 6),
    THREE_KIND: sc_three_kind,
    FOUR_KIND: sc_four_kind,
    FULL_HOUSE: sc_full_house,
    SM_STRAIGHT: sc_sm_straight,
    LG_STRAIGHT: sc_lg_straight,
    YAHTZEE: sc_yahtzee,
    CHANCE: sc_chance,
}


class Yahtzee:
    @staticmethod
    def generate_code() -> str:
        return "".join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ', k=5))

    def __init__(self, code: str, p1: int, p2: Optional[int] = None, solo: bool = False):
        self.code = code
        self.p1 = p1
        self.p2 = p2
        self.solo = solo
        self.dice = [0] * 5
        self.held = [False] * 5
        self.rolls = 0
        self.turn = 1
        self.scores = {1: {}, 2: {}}
        self.phase = "waiting" if not solo and p2 is None else "play"
        self.finished = False
        self.ts = time.time()
        self.winner = 0

    def player_num(self, uid: int) -> int:
        return 1 if uid == self.p1 else 2

    def current_uid(self) -> Optional[int]:
        return self.p1 if self.turn == 1 else self.p2

    def roll(self) -> List[int]:
        if self.rolls >= 3:
            return self.dice
        for i in range(5):
            if not self.held[i]:
                self.dice[i] = random.randint(1, 6)
        self.rolls += 1
        return self.dice

    def toggle(self, idx: int) -> bool:
        if self.rolls == 0 or self.rolls >= 3:
            return False
        if not (0 <= idx < 5):
            return False
        self.held[idx] = not self.held[idx]
        return True

    def possible(self, pnum: int) -> Dict[int, int]:
        return {c: SCORE[c](self.dice) for c in ALL_CATS if c not in self.scores[pnum]}

    def score_cat(self, pnum: int, cat: int) -> Optional[int]:
        if pnum != self.turn:
            return None
        if cat in self.scores[pnum]:
            return None
        if self.rolls == 0:
            return None
        pts = SCORE[cat](self.dice)
        self.scores[pnum][cat] = pts
        self.dice = [0] * 5
        self.held = [False] * 5
        self.rolls = 0

        if self.solo:
            if len(self.scores[pnum]) >= 13:
                self.finished = True
                self.winner = 1
            return pts

        other = 2 if pnum == 1 else 1
        if len(self.scores[pnum]) >= 13 and len(self.scores[other]) >= 13:
            self.finished = True
            s1 = grand_total(self.scores[1])
            s2 = grand_total(self.scores[2])
            if s1 > s2:
                self.winner = self.p1
            elif s2 > s1:
                self.winner = self.p2
            return pts

        if len(self.scores[pnum]) < 13:
            self.turn = other
        return pts

    def to_dict(self) -> dict:
        return {
            'code': self.code, 'p1': self.p1, 'p2': self.p2,
            'solo': self.solo, 'dice': self.dice, 'held': self.held,
            'rolls': self.rolls, 'turn': self.turn,
            'scores': {str(k): v for k, v in self.scores.items()},
            'phase': self.phase, 'finished': self.finished,
            'ts': self.ts, 'winner': self.winner,
        }

    @staticmethod
    def from_dict(d: dict) -> 'Yahtzee':
        g = Yahtzee.__new__(Yahtzee)
        g.code = d['code']
        g.p1 = d['p1']
        g.p2 = d.get('p2')
        g.solo = d.get('solo', False)
        g.dice = d['dice']
        g.held = d['held']
        g.rolls = d['rolls']
        g.turn = d['turn']
        g.scores = {int(k): v for k, v in d.get('scores', {}).items()}
        g.phase = d.get('phase', 'play')
        g.finished = d.get('finished', False)
        g.ts = d.get('ts', 0)
        g.winner = d.get('winner', 0)
        return g


def build_state(g: Yahtzee, uid: int) -> dict:
    pn = g.player_num(uid)
    my_sc = g.scores.get(pn, {})
    mt = grand_total(my_sc)
    mu = upper_sum(my_sc)
    opn = 2 if pn == 1 else 1
    op_sc = g.scores.get(opn, {})
    ot = grand_total(op_sc)

    possible = {}
    if not g.finished and g.turn == pn:
        possible = {str(c): v for c, v in g.possible(pn).items()}

    return {
        'code': g.code,
        'solo': g.solo,
        'dice': g.dice,
        'held': g.held,
        'rolls': g.rolls,
        'my_turn': g.turn == pn,
        'you': uid,
        'scores': {str(k): v for k, v in my_sc.items()},
        'opp_scores': {str(k): v for k, v in op_sc.items()},
        'total': mt,
        'opp_total': ot,
        'upper_bonus': 35 if mu >= 63 else 0,
        'possible': possible,
        'finished': g.finished,
        'winner': g.winner,
        'phase': g.phase,
        'left': 13 - len(my_sc),
    }
