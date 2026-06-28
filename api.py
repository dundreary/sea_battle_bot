import json
import logging
import time
from typing import Dict, Any

import anagram
import yahtzee
from game import Game, SIZE, SHIPS, STRIP_SHIPS, auto_place_ships, auto_place_strip_ships
from anagram import new_solo as ana_new, new_multi as ana_new_multi, join as ana_join, guess as ana_guess, hint as ana_hint, get_state as ana_state, rooms as ana_rooms
import persist
import config

logger = logging.getLogger(__name__)

# ── Helpers ─────────────────────────────────────────────────────────
def _serialize_player_dict(d: Dict) -> Dict[str, Any]:
    return {str(k): v for k, v in d.items()}


games: Dict[str, Game] = {}
player_games: Dict[int, str] = {}

# Track uid -> {code, sid} for Anagram multiplayer rejoin + active games listing
ana_player_sessions: Dict[int, Dict[str, Any]] = {}

# Yahtzee game storage: code -> Yahtzee instance
yz_games: Dict[str, yahtzee.Yahtzee] = {}
# uid -> latest yz code
yz_player_games: Dict[int, str] = {}

EMPTY = 0
SHIP = 1

# ── Route registry ──────────────────────────────────────────────────────
_ROUTES: Dict[str, Any] = {}

def _route(path: str):
    def wrapper(fn):
        _ROUTES[path] = fn
        return fn
    return wrapper

def as_dict(game, uid):
    pnum = game.player_num(uid) if not game.solo else 1
    own = game.board_for(uid)
    opp = game.opponent_board(uid)
    opp_hidden = [EMPTY if v == SHIP else v for v in [opp.grid[r][c] for r in range(SIZE) for c in range(SIZE)]]
    # Build ship info: size + cells for each ship on own board
    ships_data = []
    for ship in own.ships:
        ship_size = len(ship.cells)
        ships_data.append({"size": ship_size, "cells": [list(c) for c in ship.cells]})
    ships_list = STRIP_SHIPS if game.strip else SHIPS
    return {
        "code": game.code,
        "solo": game.solo,
        "strip": game.strip,
        "phase": game.phase,
        "turn": game.turn,
        "current_player": game.current_player(),
        "my_turn": game.current_player() == uid,
        "ready": game.ready,
        "you": uid,
        "own": [own.grid[r][c] for r in range(SIZE) for c in range(SIZE)],
        "own_ships": ships_data,
        "opp": opp_hidden,
        "all_sunk": opp.all_sunk(),
        "my_all_sunk": own.all_sunk(),
        "ship_len": game.needs_ship_of_length(pnum) if game.phase != "playing" else None,
        "ships_placed": len(own.ships),
        "ships_list": list(ships_list),
        "strip_photo": game.strip_photo,
    }

def new_solo(uid, strip=False):
    code = Game.generate_code()
    while code in games:
        code = Game.generate_code()
    game = Game(code, uid, solo=True, strip=strip)
    game.player2_id = 0
    games[code] = game
    game.phase = "placing"
    if strip:
        auto_place_strip_ships(game.board2)
    else:
        auto_place_ships(game.board2)
    game.placing[2]["ship_idx"] = len(SHIPS)
    game.ready[2] = True
    return game

def get_state(uid, code):
    game = games.get(code)
    if not game:
        return None
    if uid != game.player1_id and uid != game.player2_id:
        return None
    return as_dict(game, uid)

def _bot_shoots(game, uid):
    if not game.bot_ai:
        return []
    own = game.board_for(uid)
    shots = []
    while True:
        br, bc = game.bot_ai.choose_shot(own)
        if br is None:
            break
        bresult = own.receive_shot(br, bc)
        game.bot_ai.register_shot(br, bc, bresult, own)
        shots.append({"r": br, "c": bc, "result": bresult})
        if bresult == "miss":
            game.switch_turn()
            break
        if own.all_sunk():
            break
    return shots

def shoot(uid, code, r, c):
    game = games.get(code)
    if not game or game.current_player() != uid or game.phase != "playing":
        return None
    opp = game.opponent_board(uid)
    result = opp.receive_shot(r, c)
    if result == "repeat":
        return None
    bot_shots = None
    if result == "miss":
        game.switch_turn()
    if game.solo and result == "miss":
        bot_shots = _bot_shoots(game, uid)
    return {"result": result, "bot_shots": bot_shots}

def place_auto(uid, code):
    game = games.get(code)
    pnum = game.player_num(uid)
    board = game.board_for(uid)
    board.grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    board.ships = []
    if game.strip:
        auto_place_strip_ships(board)
    else:
        auto_place_ships(board)
    game.placing[pnum]["ship_idx"] = len(SHIPS)
    return True

def confirm_placement(uid, code):
    game = games.get(code)
    pnum = game.player_num(uid)
    board = game.board_for(uid)
    ships_list = STRIP_SHIPS if game.strip else SHIPS
    if len(board.ships) < len(ships_list):
        return None
    if game.solo and len(game.board2.ships) < len(ships_list):
        return None
    game.ready[pnum] = True
    if game.ready[1] and game.ready[2]:
        game.phase = "playing"
        game.turn = 1
        return True
    return False

def new_multi(uid, strip=False):
    code = Game.generate_code()
    while code in games:
        code = Game.generate_code()
    game = Game(code, uid, strip=strip)
    games[code] = game
    return game

def join_game(uid, code):
    game = games.get(code)
    if not game:
        return None, "not_found"
    if game.player2_id is not None:
        return None, "full"
    game.player2_id = uid
    game.phase = "placing"
    return game, "ok"

def save_all():
    data = {
        'version': 1,
        'saved_at': time.time(),
        'api_games': {},
        'api_player_games': _serialize_player_dict(player_games),
        'api_ana_player_sessions': _serialize_player_dict(ana_player_sessions),
        'anagram_games': anagram.games,
        'anagram_rooms': anagram.rooms,
        'yz_games': {},
        'yz_player_games': _serialize_player_dict(yz_player_games),
    }
    for code, game in games.items():
        try:
            data['api_games'][code] = game.to_dict()
        except Exception:
            pass
    for code, g in yz_games.items():
        try:
            data['yz_games'][code] = g.to_dict()
        except Exception:
            pass
    persist.save(data)


def load_all():
    data = persist.load()
    if not data:
        return

    now = time.time()
    MAX_AGE = 86400

    games.clear()
    for code, gdata in data.get('api_games', {}).items():
        try:
            game = Game.from_dict(gdata)
            created = getattr(game, 'created_at', 0)
            if now - created < MAX_AGE:
                games[code] = game
        except Exception:
            pass

    player_games.clear()
    player_games.update({int(k): v for k, v in data.get('api_player_games', {}).items()})

    valid = set(games.keys())
    for uid, code in list(player_games.items()):
        if code not in valid:
            del player_games[uid]

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
            if (p1 and p1 in anagram.games) or (p2 and p2 in anagram.games):
                anagram.rooms[code] = rdata
        except Exception:
            pass

    ana_player_sessions.clear()
    for k, v in data.get('api_ana_player_sessions', {}).items():
        try:
            sid = v.get('sid')
            if sid and sid in anagram.games:
                ana_player_sessions[int(k)] = v
        except Exception:
            pass

    yz_games.clear()
    for code, gdata in data.get('yz_games', {}).items():
        try:
            g = yahtzee.Yahtzee.from_dict(gdata)
            if time.time() - g.ts < 86400:
                yz_games[code] = g
        except Exception:
            pass

    yz_player_games.clear()
    yz_player_games.update({int(k): v for k, v in data.get('yz_player_games', {}).items()})
    for uid, code in list(yz_player_games.items()):
        if code not in yz_games:
            del yz_player_games[uid]


def handle_api(path, body):
    try:
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        data = {}
    uid = data.get("uid")
    if uid is not None:
        try:
            uid = int(uid)
        except (ValueError, TypeError):
            pass

    handler = _ROUTES.get(path)
    if handler is None:
        return {"error": "unknown path"}
    return handler(uid, data)


# ── Route handlers ──────────────────────────────────────────────────────

@_route("/api/new_solo")
def _handle_new_solo(uid, data):
    if not uid:
        return {"error": "no uid"}
    strip = data.get("strip", False)
    game = new_solo(uid, strip=strip)
    player_games[uid] = game.code
    save_all()
    return {"ok": True, "code": game.code, "state": as_dict(game, uid)}


@_route("/api/new_multi")
def _handle_new_multi(uid, data):
    if not uid:
        return {"error": "no uid"}
    strip = data.get("strip", False)
    game = new_multi(uid, strip=strip)
    player_games[uid] = game.code
    save_all()
    return {"ok": True, "code": game.code, "state": as_dict(game, uid)}


@_route("/api/join")
def _handle_join(uid, data):
    code = data.get("code")
    if not uid or not code:
        return {"error": "no uid/code"}
    game, status = join_game(uid, code)
    if not game:
        return {"ok": False, "error": status}
    player_games[uid] = code
    save_all()
    return {"ok": True, "state": as_dict(game, uid)}


@_route("/api/state")
def _handle_state(uid, data):
    code = data.get("code")
    if not uid or not code:
        return {"error": "no uid/code"}
    state = get_state(uid, code)
    if not state:
        return {"error": "no game"}
    return {"ok": True, "state": state}


@_route("/api/shoot")
def _handle_shoot(uid, data):
    code = data.get("code")
    if not uid or not code:
        return {"error": "no uid/code"}
    r, c = data.get("r"), data.get("c")
    if r is None or c is None:
        return {"error": "no r/c"}
    result = shoot(uid, code, r, c)
    if result is None:
        return {"error": "invalid shot"}
    game = games.get(code)
    state = as_dict(game, uid) if game else None
    save_all()
    return {"ok": True, "result": result, "state": state}


@_route("/api/place_auto")
def _handle_place_auto(uid, data):
    code = data.get("code")
    if not uid or not code:
        return {"error": "no uid/code"}
    place_auto(uid, code)
    game = games.get(code)
    state = as_dict(game, uid) if game else None
    save_all()
    return {"ok": True, "state": state}


@_route("/api/confirm")
def _handle_confirm(uid, data):
    code = data.get("code")
    if not uid or not code:
        return {"error": "no uid/code"}
    started = confirm_placement(uid, code)
    if started is None:
        return {"ok": False, "error": "not_all_placed"}
    game = games.get(code)
    state = as_dict(game, uid) if game else None
    save_all()
    return {"ok": True, "started": started, "state": state}


@_route("/api/upload_photo")
def _handle_upload_photo(uid, data):
    code = data.get("code")
    if not uid or not code:
        return {"error": "no uid/code"}
    photo = data.get("photo")
    if not photo:
        return {"error": "no photo"}
    game = games.get(code)
    if not game:
        return {"error": "game not found"}
    game.strip_photo = photo
    save_all()
    return {"ok": True, "photo_saved": True}


@_route("/api/yz_new_solo")
def _handle_yz_new_solo(uid, data):
    if not uid:
        return {"error": "no uid"}
    code = yahtzee.Yahtzee.generate_code()
    while code in yz_games:
        code = yahtzee.Yahtzee.generate_code()
    g = yahtzee.Yahtzee(code, uid, solo=True)
    g.phase = "play"
    yz_games[code] = g
    yz_player_games[uid] = code
    save_all()
    return {"ok": True, "code": code, "state": yahtzee.build_state(g, uid)}


@_route("/api/yz_new_multi")
def _handle_yz_new_multi(uid, data):
    if not uid:
        return {"error": "no uid"}
    code = yahtzee.Yahtzee.generate_code()
    while code in yz_games:
        code = yahtzee.Yahtzee.generate_code()
    g = yahtzee.Yahtzee(code, uid)
    yz_games[code] = g
    yz_player_games[uid] = code
    save_all()
    return {"ok": True, "code": code, "state": yahtzee.build_state(g, uid)}


@_route("/api/yz_join")
def _handle_yz_join(uid, data):
    code = data.get("code", "").strip().upper()
    if not uid or not code:
        return {"error": "no uid/code"}
    g = yz_games.get(code)
    if not g:
        return {"ok": False, "error": "not_found"}
    if g.p2 is not None:
        return {"ok": False, "error": "full"}
    g.p2 = uid
    g.phase = "play"
    g.turn = 1
    yz_player_games[uid] = code
    save_all()
    return {"ok": True, "state": yahtzee.build_state(g, uid)}


@_route("/api/yz_state")
def _handle_yz_state(uid, data):
    code = data.get("code", "")
    if not uid or not code:
        return {"error": "no uid/code"}
    g = yz_games.get(code)
    if not g:
        return {"error": "no game"}
    if uid != g.p1 and uid != g.p2:
        return {"error": "not your game"}
    save_all()
    return {"ok": True, "state": yahtzee.build_state(g, uid)}


@_route("/api/yz_roll")
def _handle_yz_roll(uid, data):
    code = data.get("code", "")
    if not uid or not code:
        return {"error": "no uid/code"}
    g = yz_games.get(code)
    if not g or g.finished:
        return {"error": "no game"}
    if g.turn != g.player_num(uid):
        return {"error": "not your turn"}
    g.roll()
    save_all()
    return {"ok": True, "state": yahtzee.build_state(g, uid)}


@_route("/api/yz_hold")
def _handle_yz_hold(uid, data):
    code = data.get("code", "")
    idx = data.get("idx")
    if not uid or not code or idx is None:
        return {"error": "no uid/code/idx"}
    g = yz_games.get(code)
    if not g or g.finished:
        return {"error": "no game"}
    if g.turn != g.player_num(uid):
        return {"error": "not your turn"}
    g.toggle(idx)
    save_all()
    return {"ok": True, "state": yahtzee.build_state(g, uid)}


@_route("/api/yz_score")
def _handle_yz_score(uid, data):
    code = data.get("code", "")
    cat = data.get("cat")
    if not uid or not code or cat is None:
        return {"error": "no uid/code/cat"}
    g = yz_games.get(code)
    if not g or g.finished:
        return {"error": "no game"}
    if g.turn != g.player_num(uid):
        return {"error": "not your turn"}
    try:
        cat = int(cat)
    except (ValueError, TypeError):
        return {"error": "invalid category"}
    pts = g.score_cat(g.player_num(uid), cat)
    if pts is None:
        return {"error": "cannot score"}
    save_all()
    return {"ok": True, "pts": pts, "state": yahtzee.build_state(g, uid)}


@_route("/api/yz_active")
def _handle_yz_active(uid, data):
    if not uid:
        return {"error": "no uid"}
    code = yz_player_games.get(uid)
    if code and code in yz_games:
        g = yz_games[code]
        return {"ok": True, "active": {
            'code': code,
            'solo': g.solo,
            'finished': g.finished,
            'phase': g.phase,
            'my_turn': g.turn == g.player_num(uid) and not g.finished,
        }}
    return {"ok": True, "active": None}


@_route("/api/ana_new_solo")
def _handle_ana_new_solo(uid, data):
    sid, g = ana_new()
    save_all()
    return {"ok": True, "sid": sid, "state": ana_state(sid)}


@_route("/api/ana_new_multi")
def _handle_ana_new_multi(uid, data):
    sid, code, g = ana_new_multi()
    if uid:
        ana_player_sessions[uid] = {'code': code, 'sid': sid}
    save_all()
    return {"ok": True, "sid": sid, "code": code, "state": ana_state(sid)}


@_route("/api/ana_join")
def _handle_ana_join(uid, data):
    c = data.get("code", "")
    if not c:
        return {"error": "no code"}
    result = ana_join(c)
    if not result[0]:
        return {"ok": False, "error": result[1]}
    if uid and result[0]:
        ana_player_sessions[uid] = {'code': c.upper(), 'sid': result[0]}
    save_all()
    return {"ok": True, "sid": result[0], "state": ana_state(result[0])}


@_route("/api/ana_guess")
def _handle_ana_guess(uid, data):
    sid = data.get("sid", "")
    word = data.get("word", "")
    result = ana_guess(sid, word)
    if result[0] != "ok":
        return {"ok": False, "error": result[0] if result[0] else result[1]}
    save_all()
    return {"ok": True, "result": result[1], "state": ana_state(sid)}


@_route("/api/ana_hint")
def _handle_ana_hint(uid, data):
    sid = data.get("sid", "")
    result = ana_hint(sid)
    if not result:
        return {"ok": False, "error": "no_hint"}
    save_all()
    return {"ok": True, "result": result, "state": ana_state(sid)}


@_route("/api/ana_state")
def _handle_ana_state(uid, data):
    sid = data.get("sid", "")
    st = ana_state(sid)
    if not st:
        return {"error": "not_found"}
    save_all()
    return {"ok": True, "state": st}


@_route("/api/active_games")
def _handle_active_games(uid, data):
    if not uid:
        return {"error": "no uid"}
    games_list = []
    sb_code = player_games.get(uid)
    if sb_code and sb_code in games:
        g = games[sb_code]
        games_list.append({
            'type': 'sea_battle',
            'code': sb_code,
            'solo': g.solo,
            'phase': g.phase,
            'my_turn': g.current_player() == uid,
        })
    ana_data = ana_player_sessions.get(uid)
    if ana_data:
        sid = ana_data['sid']
        code_ = ana_data['code']
        st = ana_state(sid)
        if st:
            games_list.append({
                'type': 'anagram',
                'code': code_,
                'finished': st.get('finished', False),
                'score': st.get('score', 0),
                'remaining': st.get('remaining', 0),
            })
    yz_code = yz_player_games.get(uid)
    if yz_code and yz_code in yz_games:
        g = yz_games[yz_code]
        games_list.append({
            'type': 'yahtzee',
            'code': yz_code,
            'solo': g.solo,
            'finished': g.finished,
            'my_turn': g.turn == g.player_num(uid) and not g.finished,
            'phase': g.phase,
        })
    return {"ok": True, "games": games_list}


@_route("/api/bot_info")
def _handle_bot_info(uid, data):
    return {"ok": True, "bot_username": config.BOT_USERNAME, "webapp_url": config.WEBAPP_URL}


@_route("/api/resolve_code")
def _handle_resolve_code(uid, data):
    code = data.get("code", "").strip().upper()
    if not code:
        return {"error": "no code"}
    if code in games:
        return {"ok": True, "game": "sea_battle", "code": code}
    if code in ana_rooms:
        return {"ok": True, "game": "anagram", "code": code}
    if code in yz_games:
        return {"ok": True, "game": "yahtzee", "code": code}
    return {"ok": False, "error": "not_found"}
