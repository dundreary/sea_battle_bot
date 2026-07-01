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
    import anagram

    with _lock:
        # Serialize player_games keys as strings (JSON-compatible)
        pg_serialized = {}
        for k, v in api.player_games.items():
            pg_serialized[str(k)] = v

        # Serialize ana_player_sessions
        aps_serialized = {}
        for k, v in api.ana_player_sessions.items():
            aps_serialized[str(k)] = v

        # Serialize checkers_player_games
        ck_pg_serialized = {}
        for k, v in api.checkers_player_games.items():
            ck_pg_serialized[str(k)] = v

        # Serialize stratego_player_games
        st_pg_serialized = {}
        for k, v in api.stratego_player_games.items():
            st_pg_serialized[str(k)] = v

        data = {
            'version': 1,
            'saved_at': time.time(),
            'api_games': {},
            'api_player_games': pg_serialized,
            'api_ana_player_sessions': aps_serialized,
            'anagram_games': anagram.games,
            'anagram_rooms': anagram.rooms,
            'checkers_games': {},
            'checkers_player_games': ck_pg_serialized,
            'stratego_games': {},
            'stratego_player_games': st_pg_serialized,
        }
        for code, game in api.games.items():
            try:
                data['api_games'][code] = game.to_dict()
            except Exception:
                pass  # skip un-serializable games
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
        _write(data)


def load():
    import api
    import anagram
    from game import Game
    from checkers import CheckersGame
    from stratego import StrategoGame

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

        # Remove player_games entries that point to expired/missing games
        valid = set(api.games.keys())
        for uid, code in list(api.player_games.items()):
            if code not in valid:
                del api.player_games[uid]

        # --- Anagram games ---
        anagram.games.clear()
        for sid, gdata in data.get('anagram_games', {}).items():
            try:
                started = gdata.get('started_at', 0)
                if now - started < MAX_AGE:
                    anagram.games[sid] = gdata
            except Exception:
                pass

        anagram.rooms.clear()
        for code, rdata in data.get('anagram_rooms', {}).items():
            try:
                p1 = rdata.get('p1_sid')
                p2 = rdata.get('p2_sid')
                # Keep room if at least one player's session still exists
                if (p1 and p1 in anagram.games) or (p2 and p2 in anagram.games):
                    anagram.rooms[code] = rdata
            except Exception:
                pass

        # Restore ana_player_sessions (after anagram games loaded)
        api.ana_player_sessions.clear()
        for k, v in data.get('api_ana_player_sessions', {}).items():
            try:
                sid = v.get('sid')
                if sid and sid in anagram.games:
                    api.ana_player_sessions[k] = v
            except Exception:
                pass

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
        for k, v in data.get('checkers_player_games', {}).items():
            try:
                uid = int(k)
                code = v
                if code in api.checkers_games:
                    api.checkers_player_games[uid] = code
            except Exception:
                pass

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
        for k, v in data.get('stratego_player_games', {}).items():
            try:
                uid = int(k)
                code = v
                if code in api.stratego_games:
                    api.stratego_player_games[uid] = code
            except Exception:
                pass


