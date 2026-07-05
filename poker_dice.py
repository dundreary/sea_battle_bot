import random
import string
from typing import Dict, List, Optional, Any, Set


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


class PokerDiceGame:
    def __init__(self, code: str, player1_id: int, player2_id: Optional[int] = None, solo: bool = False, total_rounds: int = 5):
        self.code = code
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.solo = solo
        self.total_rounds = total_rounds
        self.current_round = 1
        self.players = {
            1: {'dice': [], 'rolls': 3, 'scored': False, 'hand': None},
            2: {'dice': [], 'rolls': 3, 'scored': False, 'hand': None},
        }
        self.round_history = []
        self.turn = 1
        self.phase = 'playing'

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
        if p['scored'] or p['rolls'] <= 0:
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

        if p['rolls'] <= 0:
            p['hand'] = evaluate(dice)
            p['scored'] = True
            self._after_score(pnum)

        return self.get_state(pnum)

    def score(self, uid: int) -> Optional[Dict]:
        pnum = self.player_num(uid)
        if pnum is None or pnum != self.turn or self.phase != 'playing':
            return None
        p = self.players[pnum]
        if p['scored'] or not p['dice']:
            return None

        p['hand'] = evaluate(p['dice'])
        p['scored'] = True
        self._after_score(pnum)
        return self.get_state(pnum)

    def _after_score(self, pnum: int):
        other = 3 - pnum
        if self.players[other]['scored']:
            self._end_round()
        else:
            if self.solo and pnum == 1:
                self.turn = 2
                self._bot_play()
            else:
                self.turn = other

    def _end_round(self):
        self.round_history.append({
            'round': self.current_round,
            'p1': dict(self.players[1]['hand']),
            'p2': dict(self.players[2]['hand']),
        })

        if self.current_round >= self.total_rounds:
            self.phase = 'finished'
        else:
            self.current_round += 1
            self.players[1] = {'dice': [], 'rolls': 3, 'scored': False, 'hand': None}
            self.players[2] = {'dice': [], 'rolls': 3, 'scored': False, 'hand': None}
            self.turn = 1

    def _bot_play(self):
        p = self.players[2]
        dice = [random.randint(1, 6) for _ in range(5)]
        for r in range(3):
            counts = {}
            for d in dice:
                counts[d] = counts.get(d, 0) + 1
            if r < 2:
                keep = set()
                for i, d in enumerate(dice):
                    if counts[d] >= 2:
                        keep.add(i)
                if not keep:
                    keep = {i for i, d in enumerate(dice) if d == max(dice)}
                for i in range(5):
                    if i not in keep:
                        dice[i] = random.randint(1, 6)
        p['dice'] = dice
        p['hand'] = evaluate(dice)
        p['scored'] = True
        self._after_score(2)

    def _get_total(self, pnum: int) -> int:
        return sum(r[f'p{pnum}']['score'] for r in self.round_history)

    def _get_winner(self):
        if self.phase != 'finished':
            return None
        total1 = self._get_total(1)
        total2 = self._get_total(2)
        if total1 > total2:
            return self.player1_id
        if total2 > total1:
            return self.player2_id if self.player2_id else 0
        return -1

    def _get_history_for_player(self, pnum: int) -> List[Dict]:
        history = []
        for r in self.round_history:
            my_key = f'p{pnum}'
            opp_key = f'p{3-pnum}'
            my_hand = r[my_key]
            opp_hand = r[opp_key]
            entry = {
                'round': r['round'],
                'my_score': my_hand['score'],
                'my_hand': my_hand['name'],
                'my_rank': my_hand['rank'],
                'opp_score': opp_hand['score'],
                'opp_hand': opp_hand['name'],
                'opp_rank': opp_hand['rank'],
            }
            if my_hand['rank'] < opp_hand['rank']:
                entry['result'] = 'win'
            elif my_hand['rank'] > opp_hand['rank']:
                entry['result'] = 'lose'
            elif my_hand['score'] > opp_hand['score']:
                entry['result'] = 'win'
            elif my_hand['score'] < opp_hand['score']:
                entry['result'] = 'lose'
            else:
                entry['result'] = 'draw'
            history.append(entry)
        return history

    def get_state(self, pnum: int) -> Dict[str, Any]:
        p = self.players[pnum]
        opp = self.players[3 - pnum]

        winner = self._get_winner()
        total_my = self._get_total(pnum)
        total_opp = self._get_total(3 - pnum)

        return {
            'code': self.code,
            'solo': self.solo,
            'phase': self.phase,
            'turn': self.turn,
            'my_turn': self.turn == pnum,
            'you': pnum,
            'dice': p['dice'],
            'rolls_left': p['rolls'],
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
            'current_round': self.current_round,
            'total_rounds': self.total_rounds,
            'round_history': self._get_history_for_player(pnum),
            'total_score': total_my,
            'opponent_total_score': total_opp,
        }

    @staticmethod
    def generate_code() -> str:
        return ''.join(random.choices(string.ascii_uppercase, k=6))


games: Dict[str, PokerDiceGame] = {}
player_games: Dict[str, str] = {}
