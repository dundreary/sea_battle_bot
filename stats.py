"""Per-player win/loss/draw statistics and recent match history.

A player's record is keyed by their Telegram user id (the same id used
everywhere else in the app), so it persists across every game type and every
game code. Like every other piece of shared game state, callers are expected
to hold STATE_LOCK while calling record_match() / get_stats() -- this module
itself does no locking, matching the pattern the rest of the codebase uses
(registry.py's STATE_LOCK is acquired by the API layer, not by individual
state modules).
"""
from typing import Any, Dict, Optional
import time

GAME_TYPES = ("sea_battle", "poker_dice", "checkers", "backgammon")

# Keep enough history to be genuinely useful without letting a very active
# player's record grow without bound.
MAX_HISTORY_PER_PLAYER = 50

# uid (str) -> {
#   "wins": int, "losses": int, "draws": int,
#   "by_game": {game_type: {"wins": int, "losses": int, "draws": int}},
#   "history": [{"game", "code", "result", "opponent", "solo", "finished_at"}, ...]
# }  -- history is most-recent-first and capped at MAX_HISTORY_PER_PLAYER.
_stats: Dict[str, Dict[str, Any]] = {}

_RESULT_FIELD = {"win": "wins", "loss": "losses", "draw": "draws"}
_MIRROR = {"win": "loss", "loss": "win", "draw": "draw"}


def _fresh_record() -> Dict[str, Any]:
    return {
        "wins": 0,
        "losses": 0,
        "draws": 0,
        "by_game": {g: {"wins": 0, "losses": 0, "draws": 0} for g in GAME_TYPES},
        "history": [],
    }


def _record_one(game_type: str, code: str, uid, result: str, opponent, solo: bool) -> None:
    if not uid or result not in _RESULT_FIELD:
        return
    key = str(uid)
    rec = _stats.setdefault(key, _fresh_record())
    by_game = rec["by_game"].setdefault(game_type, {"wins": 0, "losses": 0, "draws": 0})
    field = _RESULT_FIELD[result]
    rec[field] += 1
    by_game[field] += 1
    rec["history"].insert(0, {
        "game": game_type,
        "code": code,
        "result": result,
        "opponent": opponent,
        "solo": solo,
        "finished_at": time.time(),
    })
    del rec["history"][MAX_HISTORY_PER_PLAYER:]


def record_match(game_type: str, code: str, player1_id, player2_id, solo: bool, p1_result: Optional[str]) -> None:
    """Record a finished match's outcome for both real participants.

    ``p1_result`` is player1's own outcome ("win"/"loss"/"draw"); player2's is
    inferred as the mirror image. A falsy id (0/None, used for the bot slot in
    solo games) is skipped -- only human players accumulate a stats record.
    Call this once per finished game, while holding STATE_LOCK like every
    other mutation of shared state. A None/invalid ``p1_result`` is a no-op,
    so call sites don't need to special-case "not actually finished yet".
    """
    if p1_result not in _RESULT_FIELD:
        return
    if player1_id:
        _record_one(game_type, code, player1_id, p1_result, player2_id if not solo else None, solo)
    if player2_id and not solo:
        _record_one(game_type, code, player2_id, _MIRROR[p1_result], player1_id, solo)


def get_stats(uid) -> Dict[str, Any]:
    """Return uid's aggregate record and recent history. Always returns a
    well-formed (possibly all-zero) structure, even for a player with no
    recorded matches yet."""
    rec = _stats.get(str(uid)) or _fresh_record()
    total = rec["wins"] + rec["losses"] + rec["draws"]
    winrate = round(100.0 * rec["wins"] / total, 1) if total else None
    return {
        "wins": rec["wins"],
        "losses": rec["losses"],
        "draws": rec["draws"],
        "total": total,
        "winrate": winrate,
        "by_game": rec["by_game"],
        "history": rec["history"],
    }


def reset_stats(uid) -> None:
    """Reset a player's statistics and history to a clean all-zero state.

    Unlike ``_fresh_record`` (which omits the computed ``total``/``winrate``
    fields), this mirrors the exact shape ``get_stats`` returns so a freshly
    reset record is byte-for-byte compatible with the cached structure.
    """
    uid = str(uid)
    _stats[uid] = {
        "wins": 0, "losses": 0, "draws": 0, "total": 0,
        "winrate": 0.0,
        "by_game": {"sea_battle": {"wins": 0, "losses": 0, "draws": 0},
                    "poker_dice": {"wins": 0, "losses": 0, "draws": 0},
                    "checkers": {"wins": 0, "losses": 0, "draws": 0},
                    "backgammon": {"wins": 0, "losses": 0, "draws": 0}},
        "history": [],
    }


def to_dict() -> Dict[str, Any]:
    return _stats


def load_from_dict(data: Optional[Dict[str, Any]]) -> None:
    global _stats
    _stats = data or {}
