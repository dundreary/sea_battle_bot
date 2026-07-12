import os
import json
import time
import logging
import threading

from registry import REGISTRIES, STATE_LOCK

logger = logging.getLogger(__name__)

# The registry is the single owner of every game set; reach the same dict
# objects here so persistence never depends on the API layer.
sb = REGISTRIES["sea_battle"]
pd = REGISTRIES["poker_dice"]
ck = REGISTRIES["checkers"]
bg = REGISTRIES["backgammon"]

PERSIST_PATH = os.path.join(os.path.dirname(__file__), 'data', 'persist.json')


def _write(data):
    os.makedirs(os.path.dirname(PERSIST_PATH), exist_ok=True)
    tmp = PERSIST_PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, default=str)
    os.replace(tmp, PERSIST_PATH)


def _read():
    try:
        with open(PERSIST_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


MAX_AGE = 86400  # 24 hours


def _serialize_games(games_dict, to_dict_fn):
    result = {}
    for code, game in games_dict.items():
        try:
            result[code] = to_dict_fn(game)
        except Exception:
            logger.exception("Failed to serialize game %s", code)
    return result


def _deserialize_games(data_dict, from_dict_fn, check_age=True):
    now = time.time()
    games = {}
    for code, gdata in data_dict.items():
        try:
            game = from_dict_fn(gdata)
            if not check_age:
                games[code] = game
            else:
                created = getattr(game, 'created_at', 0)
                if now - created < MAX_AGE or gdata.get('phase') != 'finished':
                    games[code] = game
        except Exception:
            logger.exception("Failed to deserialize game %s", code)
    return games


def _cleanup_stale_player_games(player_games, valid_codes):
    for uid, code in list(player_games.items()):
        if code not in valid_codes:
            del player_games[uid]


def save():
    """Mark state dirty; a background thread persists it shortly.

    Keeping the serialization + disk write off the request path means a single
    HTTP handler never blocks on dumping every active game.
    """
    global _dirty
    with _dirty_lock:
        _dirty = True
    _flush_event.set()


def flush():
    """Synchronously persist current state.

    Use before evicting a game or shutting down, where the on-disk state must
    be up to date immediately (e.g. so a surrendered game does not reappear).
    """
    global _dirty
    with _dirty_lock:
        _dirty = False
    _dump()


def _dump():
    with STATE_LOCK:
        data = {
            'version': 1,
            'saved_at': time.time(),
            'api_games': _serialize_games(sb.games, lambda g: g.to_dict()),
            'api_player_games': {str(k): v for k, v in sb.player_games.items()},
            'checkers_games': _serialize_games(ck.games, lambda g: g.to_dict()),
            'checkers_player_games': {str(k): v for k, v in ck.player_games.items()},
            'poker_dice_games': _serialize_games(pd.games, lambda g: g.to_dict()),
            'poker_dice_player_games': {str(k): v for k, v in pd.player_games.items()},
            'backgammon_games': _serialize_games(bg.games, lambda g: g.to_dict()),
            'backgammon_player_games': {str(k): v for k, v in bg.player_games.items()},
        }
    _write(data)


_dirty = False
_dirty_lock = threading.Lock()
_flush_event = threading.Event()
PERSIST_INTERVAL = 1.5


def _persistence_worker():
    while True:
        _flush_event.wait(PERSIST_INTERVAL)
        with _dirty_lock:
            if not _dirty:
                continue
        flush()


threading.Thread(target=_persistence_worker, name="persistence", daemon=True).start()


def load():
    from game import Game
    from checkers import CheckersGame
    from poker_dice import PokerDiceGame
    from backgammon import BackgammonGame

    data = _read()
    if not data:
        return

    sb.games.clear()
    sb.games.update(_deserialize_games(data.get('api_games', {}), Game.from_dict))
    sb.player_games.clear()
    sb.player_games.update(data.get('api_player_games', {}))
    _cleanup_stale_player_games(sb.player_games, set(sb.games.keys()))

    ck.games.clear()
    ck.games.update(_deserialize_games(data.get('checkers_games', {}), CheckersGame.from_dict))
    ck.player_games.clear()
    ck.player_games.update(data.get('checkers_player_games', {}))
    _cleanup_stale_player_games(ck.player_games, set(ck.games.keys()))

    pd.games.clear()
    pd.games.update(_deserialize_games(
        data.get('poker_dice_games', {}),
        PokerDiceGame.from_dict,
    ))
    pd.player_games.clear()
    pd.player_games.update(data.get('poker_dice_player_games', {}))
    _cleanup_stale_player_games(pd.player_games, set(pd.games.keys()))

    bg.games.clear()
    bg.games.update(_deserialize_games(
        data.get('backgammon_games', {}),
        BackgammonGame.from_dict,
    ))
    bg.player_games.clear()
    bg.player_games.update(data.get('backgammon_player_games', {}))
    _cleanup_stale_player_games(bg.player_games, set(bg.games.keys()))


