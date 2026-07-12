import os
import json
import time
import logging

logger = logging.getLogger(__name__)

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
    import api

    data = {
        'version': 1,
        'saved_at': time.time(),
        'api_games': _serialize_games(api.games, lambda g: g.to_dict()),
        'api_player_games': {str(k): v for k, v in api.player_games.items()},
        'checkers_games': _serialize_games(api.checkers_games, lambda g: g.to_dict()),
        'checkers_player_games': {str(k): v for k, v in api.checkers_player_games.items()},
        'poker_dice_games': _serialize_games(api.pd_games, lambda g: g.to_dict()),
        'poker_dice_player_games': {str(k): v for k, v in api.pd_player_games.items()},
        'backgammon_games': _serialize_games(api.bg_games, lambda g: g.to_dict()),
        'backgammon_player_games': {str(k): v for k, v in api.bg_player_games.items()},
    }
    _write(data)


def load():
    import api
    from game import Game
    from checkers import CheckersGame
    from poker_dice import PokerDiceGame
    from backgammon import BackgammonGame

    data = _read()
    if not data:
        return

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

    api.pd_games.clear()
    api.pd_games.update(_deserialize_games(
        data.get('poker_dice_games', {}),
        PokerDiceGame.from_dict,
    ))
    api.pd_player_games.clear()
    api.pd_player_games.update(data.get('poker_dice_player_games', {}))
    _cleanup_stale_player_games(api.pd_player_games, set(api.pd_games.keys()))

    api.bg_games.clear()
    api.bg_games.update(_deserialize_games(
        data.get('backgammon_games', {}),
        BackgammonGame.from_dict,
    ))
    api.bg_player_games.clear()
    api.bg_player_games.update(data.get('backgammon_player_games', {}))
    _cleanup_stale_player_games(api.bg_player_games, set(api.bg_games.keys()))


