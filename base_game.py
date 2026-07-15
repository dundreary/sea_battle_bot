import random
import time

from utils import make_game_code

# Shared phase used by every game while the two human players roll a die to
# decide who moves first.  A decisive roll advances the game into its own
# "playing" phase.
ROLL_PHASE = "roll"


class BaseGame:
    """State and helpers shared by every game type.

    Subclasses call ``super().__init__(...)`` for the common fields, then set
    their own. Serialization is split the same way: ``to_dict_common()`` emits
    the shared keys and ``_from_dict_common()`` restores them, so each game
    only deals with its game-specific data.
    """

    def __init__(self, code, player1_id, player2_id=None, solo=False, difficulty=2):
        self.code = code
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.solo = solo
        self.difficulty = difficulty
        self.created_at = time.time()
        # Opening dice roll to decide who moves first (multiplayer only).
        # None = that player has not rolled yet.
        self.first_roll = {1: None, 2: None}
        # Ephemeral delivery state: intentionally excluded from persistence.
        self.last_activity = {}
        self.notification_events = set()

    def player_num(self, uid):
        return 1 if uid == self.player1_id else 2

    def opponent_id(self, uid):
        return self.player2_id if uid == self.player1_id else self.player1_id

    def reset_first_roll(self):
        self.first_roll = {1: None, 2: None}

    def roll_for_first(self, pnum):
        """Record player ``pnum``'s opening die (1-6) and report the outcome.

        On a tie both dice stay visible (the caller shows a "Reroll" button)
        instead of being cleared automatically -- ``reroll_first`` is what
        actually clears them, once the player chooses to try again. Returns:
          {"my": int, "opp": int|None, "both": bool, "tie": bool,
           "winner": 1|2|None}
        ``winner`` is set only once both players have rolled distinct values;
        the caller is responsible for turning that into its own turn/phase.
        """
        if pnum not in (1, 2):
            return None
        if self.first_roll.get(pnum) is None:
            self.first_roll[pnum] = random.randint(1, 6)
        r1, r2 = self.first_roll[1], self.first_roll[2]
        both = r1 is not None and r2 is not None
        winner = None
        tie = False
        if both:
            if r1 == r2:
                tie = True
            else:
                winner = 1 if r1 > r2 else 2
        return {
            "my": self.first_roll.get(pnum),
            "opp": self.first_roll.get(3 - pnum) if both else None,
            "both": both,
            "tie": tie,
            "winner": winner,
        }

    def reroll_first(self, pnum):
        """Clear both dice so the opening roll can happen again after a tie.

        Either player may trigger this once ``roll_for_first`` reports a
        tie; it's a no-op otherwise so a stray call can't wipe a decisive
        or in-progress roll.
        """
        if pnum not in (1, 2):
            return False
        r1, r2 = self.first_roll.get(1), self.first_roll.get(2)
        if r1 is not None and r2 is not None and r1 == r2:
            self.reset_first_roll()
            return True
        return False

    def first_roll_dict(self):
        return {str(k): v for k, v in self.first_roll.items()}

    def restore_first_roll(self, data):
        fr = data.get("first_roll") or {}
        self.first_roll = {1: fr.get("1", fr.get(1)), 2: fr.get("2", fr.get(2))}

    @staticmethod
    def generate_code():
        return make_game_code()

    def to_dict_common(self):
        return {
            'code': self.code,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'solo': self.solo,
            'difficulty': self.difficulty,
            'created_at': self.created_at,
            'first_roll': self.first_roll_dict(),
        }

    def _from_dict_common(self, data):
        self.code = data['code']
        self.player1_id = data['player1_id']
        self.player2_id = data.get('player2_id')
        self.solo = data.get('solo', False)
        self.difficulty = data.get('difficulty', 2)
        self.created_at = data.get('created_at', 0)
        self.restore_first_roll(data)
        # Ephemeral delivery state is reset after a restart.
        self.last_activity = {}
        self.notification_events = set()
