from typing import Any, Dict


class GameRegistry:
    """Owns the in-memory games and per-player lookups for one game type."""

    def __init__(self):
        self.games: Dict[str, Any] = {}
        self.player_games: Dict[str, str] = {}

    def add(self, game) -> None:
        self.games[game.code] = game
        self.player_games[str(game.player1_id)] = game.code

    def get(self, code):
        return self.games.get(code)

    def remove(self, code) -> None:
        self.games.pop(code, None)
        for k in [k for k, v in self.player_games.items() if v == code]:
            del self.player_games[k]

    def player_code(self, uid):
        return self.player_games.get(str(uid))

    def set_player_code(self, uid, code) -> None:
        self.player_games[str(uid)] = code

    def clear(self) -> None:
        self.games.clear()
        self.player_games.clear()

    def items(self):
        return self.games.items()

    def cleanup(self, valid_codes) -> None:
        for uid, code in list(self.player_games.items()):
            if code not in valid_codes:
                del self.player_games[uid]


# Single owner of every game set. Handlers and the persistence layer both
# reach the same dict objects through these registries.
REGISTRIES: Dict[str, GameRegistry] = {
    "sea_battle": GameRegistry(),
    "poker_dice": GameRegistry(),
    "checkers": GameRegistry(),
    "backgammon": GameRegistry(),
}
