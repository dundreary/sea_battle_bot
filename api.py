import json
import base64
import logging
import urllib.request
from typing import Dict, Any

from game import Game, SIZE, SHIPS, STRIP_SHIPS, EMPTY, SHIP, auto_place_ships, auto_place_strip_ships
from anagram import new_solo as ana_new, new_multi as ana_new_multi, join as ana_join, guess as ana_guess, hint as ana_hint, get_state as ana_state, rooms as ana_rooms
from checkers import CheckersGame, BLACK, get_legal_moves
from checkers_ai import get_ai_move
from persist import save
import config

logger = logging.getLogger(__name__)


def send_strip_photo_to_winner(winner_id: int, photo_data: str, caption: str) -> bool:
    try:
        mime = 'image/jpeg'
        if ',' in photo_data:
            header, b64_data = photo_data.split(',', 1)
            if 'png' in header:
                mime = 'image/png'
            elif 'gif' in header:
                mime = 'image/gif'
            elif 'webp' in header:
                mime = 'image/webp'
        else:
            b64_data = photo_data
        photo_bytes = base64.b64decode(b64_data)

        boundary = '----StripPhotoBoundary'
        body = b''
        body += f'--{boundary}\r\n'.encode()
        body += f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'.encode()
        body += f'{winner_id}\r\n'.encode()
        body += f'--{boundary}\r\n'.encode()
        body += f'Content-Disposition: form-data; name="caption"\r\n\r\n'.encode()
        body += f'{caption}\r\n'.encode()
        body += f'--{boundary}\r\n'.encode()
        body += f'Content-Disposition: form-data; name="photo"; filename="strip_photo.jpg"\r\n'.encode()
        body += f'Content-Type: {mime}\r\n\r\n'.encode()
        body += photo_bytes + b'\r\n'
        body += f'--{boundary}--\r\n'.encode()

        req = urllib.request.Request(
            f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendPhoto',
            data=body,
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            if result.get('ok'):
                return True
            logger.error("Telegram API error: %s", result)
            return False
    except Exception as e:
        logger.error("Failed to send strip photo: %s", e)
        return False

games: Dict[str, Game] = {}
player_games: Dict[int, str] = {}

# Track uid -> {code, sid} for Anagram multiplayer rejoin + active games listing
ana_player_sessions: Dict[int, Dict[str, Any]] = {}

# Checkers games
checkers_games: Dict[str, CheckersGame] = {}
checkers_player_games: Dict[int, str] = {}

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
        "strip_photo": game.strip_photo if game.both_placed and (opp.all_sunk() or own.all_sunk()) else "",
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
    game.placing[2]["ship_idx"] = len(STRIP_SHIPS if game.strip else SHIPS)
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
        if bresult == "repeat":
            continue
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
    ships_list = STRIP_SHIPS if game.strip else SHIPS
    game.placing[pnum]["ship_idx"] = len(ships_list)
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

def _handle_new_solo(data, uid, code):
    if not uid:
        return {"error": "no uid"}
    strip = data.get("strip", False)
    game = new_solo(uid, strip=strip)
    player_games[str(uid)] = game.code
    save()
    return {"ok": True, "code": game.code, "state": as_dict(game, uid)}


def _handle_new_multi(data, uid, code):
    if not uid:
        return {"error": "no uid"}
    strip = data.get("strip", False)
    game = new_multi(uid, strip=strip)
    player_games[str(uid)] = game.code
    save()
    return {"ok": True, "code": game.code, "state": as_dict(game, uid)}


def _handle_join(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    game, status = join_game(uid, code)
    if not game:
        return {"ok": False, "error": status}
    player_games[str(uid)] = code
    save()
    return {"ok": True, "state": as_dict(game, uid)}


def _handle_state(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    state = get_state(uid, code)
    if not state:
        return {"error": "no game"}
    return {"ok": True, "state": state}


def _handle_shoot(data, uid, code):
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
    save()
    return {"ok": True, "result": result, "state": state}


def _handle_place_auto(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    place_auto(uid, code)
    game = games.get(code)
    state = as_dict(game, uid) if game else None
    save()
    return {"ok": True, "state": state}


def _handle_confirm(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    started = confirm_placement(uid, code)
    if started is None:
        return {"ok": False, "error": "not_all_placed"}
    game = games.get(code)
    state = as_dict(game, uid) if game else None
    save()
    return {"ok": True, "started": started, "state": state}


def _handle_upload_photo(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    photo = data.get("photo")
    if not photo:
        return {"error": "no photo"}
    game = games.get(code)
    if not game:
        return {"error": "game not found"}
    game.strip_photo = photo
    save()
    winner_id = game.opponent_id(uid)
    if game.solo or not winner_id or winner_id == 0:
        return {"ok": True}
    user_lang = data.get("lang", "ru")
    captions = {
        'ru': '👗 Твой друг проиграл в режиме «На раздевание»!',
        'uk': '👗 Твій друг програв у режимі «На роздягання»!',
        'en': '👗 Your friend lost in Strip Mode!',
    }
    caption = captions.get(user_lang, captions['ru'])
    ok = send_strip_photo_to_winner(winner_id, photo, caption)
    if ok:
        return {"ok": True}
    return {"ok": False, "error": "send_failed"}


def _handle_ana_new_solo(data, uid, code):
    sid, g = ana_new()
    save()
    return {"ok": True, "sid": sid, "state": ana_state(sid)}


def _handle_ana_new_multi(data, uid, code):
    sid, new_code, g = ana_new_multi()
    if uid:
        ana_player_sessions[str(uid)] = {'code': new_code, 'sid': sid}
    save()
    return {"ok": True, "sid": sid, "code": new_code, "state": ana_state(sid)}


def _handle_ana_join(data, uid, code):
    c = data.get("code", "")
    if not c:
        return {"error": "no code"}
    result = ana_join(c)
    if not result[0]:
        return {"ok": False, "error": result[1]}
    if uid and result[0]:
        ana_player_sessions[str(uid)] = {'code': c.upper(), 'sid': result[0]}
    save()
    return {"ok": True, "sid": result[0], "state": ana_state(result[0])}


def _handle_ana_guess(data, uid, code):
    sid = data.get("sid", "")
    word = data.get("word", "")
    result = ana_guess(sid, word)
    if result[0] != "ok":
        return {"ok": False, "error": result[0]}
    save()
    return {"ok": True, "result": result[1], "state": ana_state(sid)}


def _handle_ana_hint(data, uid, code):
    sid = data.get("sid", "")
    result = ana_hint(sid)
    if not result:
        return {"ok": False, "error": "no_hint"}
    save()
    return {"ok": True, "result": result, "state": ana_state(sid)}


def _handle_ana_state(data, uid, code):
    sid = data.get("sid", "")
    st = ana_state(sid)
    if not st:
        return {"error": "not_found"}
    save()
    return {"ok": True, "state": st}


def _handle_active_games(data, uid, code):
    if not uid:
        return {"error": "no uid"}
    games_list = []
    sb_code = player_games.get(str(uid))
    if sb_code and sb_code in games:
        g = games[sb_code]
        games_list.append({
            'type': 'sea_battle',
            'code': sb_code,
            'solo': g.solo,
            'phase': g.phase,
            'my_turn': g.current_player() == uid,
        })
    ana_data = ana_player_sessions.get(str(uid))
    if ana_data:
        sid = ana_data['sid']
        c = ana_data['code']
        st = ana_state(sid)
        if st:
            games_list.append({
                'type': 'anagram',
                'code': c,
                'finished': st.get('finished', False),
                'score': st.get('score', 0),
                'remaining': st.get('remaining', 0),
            })
    ck_code = checkers_player_games.get(uid)
    if ck_code and ck_code in checkers_games:
        g = checkers_games[ck_code]
        games_list.append({
            'type': 'checkers',
            'code': ck_code,
            'phase': g.phase,
            'my_turn': g.turn == g.player_color(uid) if g.player_color(uid) else False,
        })
    return {"ok": True, "games": games_list}


def _handle_bot_info(data, uid, code):
    return {"ok": True, "bot_username": config.BOT_USERNAME, "webapp_url": config.WEBAPP_URL}


def _handle_resolve_code(data, uid, code):
    c = data.get("code", "").strip().upper()
    if not c:
        return {"error": "no code"}
    if c in games:
        return {"ok": True, "game": "sea_battle", "code": c}
    if c in ana_rooms:
        return {"ok": True, "game": "anagram", "code": c}
    if c in checkers_games:
        return {"ok": True, "game": "checkers", "code": c}
    return {"ok": False, "error": "not_found"}


# ---- Checkers handlers ----

def _handle_checkers_new_solo(data, uid, code):
    if not uid:
        return {"error": "no uid"}
    c = CheckersGame.generate_code()
    while c in checkers_games:
        c = CheckersGame.generate_code()
    game = CheckersGame(c, uid, solo=True)
    checkers_games[c] = game
    checkers_player_games[uid] = c
    save()
    return {"ok": True, "code": c, "state": game.get_state(uid)}


def _handle_checkers_new_multi(data, uid, code):
    if not uid:
        return {"error": "no uid"}
    c = CheckersGame.generate_code()
    while c in checkers_games:
        c = CheckersGame.generate_code()
    game = CheckersGame(c, uid)
    checkers_games[c] = game
    checkers_player_games[uid] = c
    save()
    return {"ok": True, "code": c, "state": game.get_state(uid)}


def _handle_checkers_join(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    game = checkers_games.get(code)
    if not game:
        return {"ok": False, "error": "not_found"}
    if game.player2_id is not None:
        return {"ok": False, "error": "full"}
    game.player2_id = uid
    checkers_player_games[uid] = code
    save()
    return {"ok": True, "state": game.get_state(uid)}


def _handle_checkers_state(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    game = checkers_games.get(code)
    if not game:
        return {"error": "not_found"}
    return {"ok": True, "state": game.get_state(uid)}


def _handle_checkers_move(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    game = checkers_games.get(code)
    if not game or game.phase != "playing":
        return {"error": "not_playing"}

    color = game.player_color(uid)
    if color is None or game.turn != color:
        return {"error": "not_your_turn"}

    start_r = data.get("start_r")
    start_c = data.get("start_c")
    end_r = data.get("end_r")
    end_c = data.get("end_c")
    if None in (start_r, start_c, end_r, end_c):
        return {"error": "missing_coords"}

    moves = get_legal_moves(game.board, color)
    winning_move = None
    for m in moves:
        if m[0] == (start_r, start_c) and (end_r, end_c) == m[1][-1]:
            winning_move = m
            break

    if not winning_move:
        return {"error": "illegal_move"}

    finished = game.make_move(winning_move)
    bot_result = None

    if game.solo and not finished and game.turn == BLACK:
        ai_mv = get_ai_move(game.board, BLACK, difficulty=3)
        if ai_mv:
            finished = game.make_move(ai_mv)
            bot_result = {"move": {"start": list(ai_mv[0]), "end": list(ai_mv[1][-1])}}

    save()
    return {
        "ok": True,
        "state": game.get_state(uid),
        "finished": finished,
        "bot_move": bot_result,
    }


def _handle_checkers_hint(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    game = checkers_games.get(code)
    if not game or game.phase != "playing":
        return {"error": "not_playing"}
    color = game.player_color(uid)
    if color is None or game.turn != color:
        return {"error": "not_your_turn"}
    move = get_ai_move(game.board, color, difficulty=3)
    if not move:
        return {"error": "no_move"}
    return {"ok": True, "hint": {"start": list(move[0]), "end": list(move[1][-1])}}


_HANDLERS = {
    "/api/new_solo": _handle_new_solo,
    "/api/new_multi": _handle_new_multi,
    "/api/join": _handle_join,
    "/api/state": _handle_state,
    "/api/shoot": _handle_shoot,
    "/api/place_auto": _handle_place_auto,
    "/api/confirm": _handle_confirm,
    "/api/upload_photo": _handle_upload_photo,
    "/api/ana_new_solo": _handle_ana_new_solo,
    "/api/ana_new_multi": _handle_ana_new_multi,
    "/api/ana_join": _handle_ana_join,
    "/api/ana_guess": _handle_ana_guess,
    "/api/ana_hint": _handle_ana_hint,
    "/api/ana_state": _handle_ana_state,
    "/api/active_games": _handle_active_games,
    "/api/bot_info": _handle_bot_info,
    "/api/resolve_code": _handle_resolve_code,
    "/api/checkers_new_solo": _handle_checkers_new_solo,
    "/api/checkers_new_multi": _handle_checkers_new_multi,
    "/api/checkers_join": _handle_checkers_join,
    "/api/checkers_state": _handle_checkers_state,
    "/api/checkers_move": _handle_checkers_move,
    "/api/checkers_hint": _handle_checkers_hint,
}


def handle_api(path, body):
    try:
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        data = {}
    uid = data.get("uid")
    code = data.get("code")

    handler = _HANDLERS.get(path)
    if not handler:
        return {"error": "unknown path"}
    return handler(data, uid, code)
