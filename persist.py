import os
import json
import time
import threading

PERSIST_PATH = os.path.join(os.path.dirname(__file__), 'data', 'persist.json')
_lock = threading.Lock()


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
            pass
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
                # Only finished games are dropped when stale; in-progress games
                # are kept so a long game (or one left paused) is not lost.
                if now - created < MAX_AGE or gdata.get('phase') != 'finished':
                    games[code] = game
        except Exception:
            pass
    return games


def _cleanup_stale_player_games(player_games, valid_codes):
    for uid, code in list(player_games.items()):
        if code not in valid_codes:
            del player_games[uid]


def save():
    import api

    with _lock:
        data = {
            'version': 1,
            'saved_at': time.time(),
            'api_games': _serialize_games(api.games, lambda g: g.to_dict()),
            'api_player_games': {str(k): v for k, v in api.player_games.items()},
            'checkers_games': _serialize_games(api.checkers_games, lambda g: g.to_dict()),
            'checkers_player_games': {str(k): v for k, v in api.checkers_player_games.items()},
            # Stratego disabled — see AUDIT.md. Not persisted while disabled.
            # 'stratego_games': _serialize_games(api.stratego_games, lambda g: g.to_dict()),
            # 'stratego_player_games': {str(k): v for k, v in api.stratego_player_games.items()},
            'poker_dice_games': _serialize_games(api.pd_games, lambda g: g.to_dict()),
            'poker_dice_player_games': {str(k): v for k, v in api.pd_player_games.items()},
        }
        _write(data)


def load():
    import api
    from game import Game
    from checkers import CheckersGame
    # Stratego disabled — see AUDIT.md.
    # from stratego import StrategoGame
    from poker_dice import PokerDiceGame

    data = _read()
    if not data:
        return

    with _lock:
        api.games.clear()
        api.games.update(_deserialize_games(data.get('api_games', {}), Game.from_dict))
        api.player_games.clear()
        api.player_games.update(data.get('api_player_games', {}))
        _cleanup_stale_player_games(api.player_games, set(api.games.keys()))

        api.checkers_games.clear()
        api.checkers_games.update(_deserialize_games(data.get('checkers_games', {}), CheckersGame.from_dict))
        api.checkers_player_games.clear()
        api.checkers_player_games.update(data.get('checkers_player_games', {}))
        _cleanup_stale_player_games(api.checkers_player_games, set(api.checkers_games.keys()))

        # Stratego disabled — see AUDIT.md. Not loaded while disabled.
        # api.stratego_games.clear()
        # api.stratego_games.update(_deserialize_games(data.get('stratego_games', {}), StrategoGame.from_dict))
        # api.stratego_player_games.clear()
        # api.stratego_player_games.update(data.get('stratego_player_games', {}))
        # _cleanup_stale_player_games(api.stratego_player_games, set(api.stratego_games.keys()))

        api.pd_games.clear()
        api.pd_games.update(_deserialize_games(
            data.get('poker_dice_games', {}),
            PokerDiceGame.from_dict,
            check_age=False,
        ))
        api.pd_player_games.clear()
        api.pd_player_games.update(data.get('poker_dice_player_games', {}))
        _cleanup_stale_player_games(api.pd_player_games, set(api.pd_games.keys()))


