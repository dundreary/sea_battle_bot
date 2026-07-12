import time

from utils import make_game_code


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
        # Ephemeral delivery state: intentionally excluded from persistence.
        self.last_activity = {}
        self.notification_events = set()

    def player_num(self, uid):
        return 1 if uid == self.player1_id else 2

    def opponent_id(self, uid):
        return self.player2_id if uid == self.player1_id else self.player1_id

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
        }

    def _from_dict_common(self, data):
        self.code = data['code']
        self.player1_id = data['player1_id']
        self.player2_id = data.get('player2_id')
        self.solo = data.get('solo', False)
        self.difficulty = data.get('difficulty', 2)
        self.created_at = data.get('created_at', 0)
        # Ephemeral delivery state is reset after a restart.
        self.last_activity = {}
        self.notification_events = set()
