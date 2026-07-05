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


def save():
    import api

    with _lock:
        pg_serialized = {}
        for k, v in api.player_games.items():
            pg_serialized[str(k)] = v

        ck_pg_serialized = {}
        for k, v in api.checkers_player_games.items():
            ck_pg_serialized[str(k)] = v

        st_pg_serialized = {}
        for k, v in api.stratego_player_games.items():
            st_pg_serialized[str(k)] = v

        pd_pg_serialized = {}
        for k, v in api.pd_player_games.items():
            pd_pg_serialized[str(k)] = v

        data = {
            'version': 1,
            'saved_at': time.time(),
            'api_games': {},
            'api_player_games': pg_serialized,
            'checkers_games': {},
            'checkers_player_games': ck_pg_serialized,
            'stratego_games': {},
            'stratego_player_games': st_pg_serialized,
            'poker_dice_games': {},
            'poker_dice_player_games': pd_pg_serialized,
        }
        for code, game in api.games.items():
            try:
                data['api_games'][code] = game.to_dict()
            except Exception:
                pass
        for code, game in api.checkers_games.items():
            try:
                data['checkers_games'][code] = game.to_dict()
            except Exception:
                pass
        for code, game in api.stratego_games.items():
            try:
                data['stratego_games'][code] = game.to_dict()
            except Exception:
                pass
        for code, game in api.pd_games.items():
            try:
                data['poker_dice_games'][code] = {'code': game.code, 'player1_id': game.player1_id, 'player2_id': game.player2_id, 'solo': game.solo}
            except Exception:
                pass
        _write(data)


def load():
    import api
    from game import Game
    from checkers import CheckersGame
    from stratego import StrategoGame
    from poker_dice import PokerDiceGame

    data = _read()
    if not data:
        return

    now = time.time()
    MAX_AGE = 86400  # 24 hours

    with _lock:
        # --- Sea Battle games ---
        api.games.clear()
        for code, gdata in data.get('api_games', {}).items():
            try:
                game = Game.from_dict(gdata)
                created = getattr(game, 'created_at', 0)
                if now - created < MAX_AGE:
                    api.games[code] = game
            except Exception:
                pass

        api.player_games.clear()
        api.player_games.update(data.get('api_player_games', {}))

        valid = set(api.games.keys())
        for uid, code in list(api.player_games.items()):
            if code not in valid:
                del api.player_games[uid]

        # --- Checkers games ---
        api.checkers_games.clear()
        for code, gdata in data.get('checkers_games', {}).items():
            try:
                game = CheckersGame.from_dict(gdata)
                created = getattr(game, 'created_at', 0)
                if now - created < MAX_AGE:
                    api.checkers_games[code] = game
            except Exception:
                pass

        api.checkers_player_games.clear()
        api.checkers_player_games.update(data.get('checkers_player_games', {}))
        valid_ck = set(api.checkers_games.keys())
        for uid, code in list(api.checkers_player_games.items()):
            if code not in valid_ck:
                del api.checkers_player_games[uid]

        # --- Stratego games ---
        api.stratego_games.clear()
        for code, gdata in data.get('stratego_games', {}).items():
            try:
                game = StrategoGame.from_dict(gdata)
                created = getattr(game, 'created_at', 0)
                if now - created < MAX_AGE:
                    api.stratego_games[code] = game
            except Exception:
                pass

        api.stratego_player_games.clear()
        api.stratego_player_games.update(data.get('stratego_player_games', {}))
        valid_st = set(api.stratego_games.keys())
        for uid, code in list(api.stratego_player_games.items()):
            if code not in valid_st:
                del api.stratego_player_games[uid]

        # --- Poker Dice games ---
        api.pd_games.clear()
        for code, gdata in data.get('poker_dice_games', {}).items():
            try:
                game = PokerDiceGame(code, gdata['player1_id'], gdata.get('player2_id'), gdata.get('solo', False))
                api.pd_games[code] = game
            except Exception:
                pass

        api.pd_player_games.clear()
        api.pd_player_games.update(data.get('poker_dice_player_games', {}))
        valid_pd = set(api.pd_games.keys())
        for uid, code in list(api.pd_player_games.items()):
            if code not in valid_pd:
                del api.pd_player_games[uid]


