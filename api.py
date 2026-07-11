import json
import base64
import logging
import threading
import urllib.request
from typing import Dict, Any, Callable

from game import Game, SIZE, SHIPS, STRIP_SHIPS, SUNK, auto_place_ships, auto_place_strip_ships
from poker_dice import PokerDiceGame as PDGame, games as pd_games, player_games as pd_player_games
from checkers import CheckersGame, BLACK, opponent, get_legal_moves, has_pieces
from checkers_ai import get_ai_move
from persist import save
import config

logger = logging.getLogger(__name__)


STRIP_LOSE_CAPTIONS = {
    'ru': '👗 Твой друг проиграл в режиме «На раздевание»!',
    'uk': '👗 Твій друг програв у режимі «На роздягання»!',
    'en': '👗 Your friend lost in Strip Mode!',
}

STRIP_PHOTO_BOUNDARY = '----StripPhotoBoundary'


def _strip_photo_mime(photo_data: str) -> str:
    if ',' in photo_data:
        header = photo_data.split(',', 1)[0].lower()
        if 'png' in header:
            return 'image/png'
        if 'gif' in header:
            return 'image/gif'
        if 'webp' in header:
            return 'image/webp'
    return 'image/jpeg'


def _strip_photo_multipart(winner_id: int, photo_bytes: bytes, caption: str, mime: str) -> bytes:
    boundary = STRIP_PHOTO_BOUNDARY
    body = b''
    body += f'--{boundary}\r\n'.encode()
    body += 'Content-Disposition: form-data; name="chat_id"\r\n\r\n'.encode()
    body += f'{winner_id}\r\n'.encode()
    body += f'--{boundary}\r\n'.encode()
    body += 'Content-Disposition: form-data; name="caption"\r\n\r\n'.encode()
    body += f'{caption}\r\n'.encode()
    body += f'--{boundary}\r\n'.encode()
    body += 'Content-Disposition: form-data; name="photo"; filename="strip_photo.jpg"\r\n'.encode()
    body += f'Content-Type: {mime}\r\n\r\n'.encode()
    body += photo_bytes + b'\r\n'
    body += f'--{boundary}--\r\n'.encode()
    return body


def send_strip_photo_to_winner(winner_id: int, photo_data: str, caption: str) -> bool:
    try:
        mime = _strip_photo_mime(photo_data)
        b64_data = photo_data.split(',', 1)[1] if ',' in photo_data else photo_data
        photo_bytes = base64.b64decode(b64_data)
        body = _strip_photo_multipart(winner_id, photo_bytes, caption, mime)

        req = urllib.request.Request(
            f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendPhoto',
            data=body,
            headers={'Content-Type': f'multipart/form-data; boundary={STRIP_PHOTO_BOUNDARY}'},
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
player_games: Dict[str, str] = {}

# Checkers games
checkers_games: Dict[str, CheckersGame] = {}
checkers_player_games: Dict[str, str] = {}

# Guards all shared in-memory game dictionaries below. The HTTP server thread and
# the bot's asyncio thread both access these, so mutations must be serialized to
# avoid race conditions (see AUDIT.md, Potential Issue #4).
_state_lock = threading.Lock()


def generate_unique_code(gen_fn: Callable[[], str], existing: Dict[str, Any]) -> str:
    """Return a code produced by ``gen_fn`` that is not already a key in ``existing``."""
    code = gen_fn()
    while code in existing:
        code = gen_fn()
    return code


def _get_game(games_dict, code, uid):
    """Look up a game by code, validate uid. Returns (game, None) or (None, error_dict)."""
    if not uid or not code:
        return None, {"error": "no uid/code"}
    game = games_dict.get(code)
    if not game:
        return None, {"error": "not_found"}
    return game, None


def as_dict(game, uid):
    pnum = game.player_num(uid) if not game.solo else 1
    own = game.board_for(uid)
    opp = game.opponent_board(uid)
    ships_data = [{"size": len(s.cells), "cells": [list(c) for c in s.cells]} for s in own.ships]
    ships_list = STRIP_SHIPS if game.strip else SHIPS
    return {
        "pnum": pnum,
        "code": game.code,
        "solo": game.solo,
        "strip": game.strip,
        "difficulty": game.difficulty,
        "strip_photo": game.strip_photo if (opp.all_sunk() or own.all_sunk()) else "",
        "phase": game.phase,
        "turn": game.turn,
        "current_player": game.current_player(),
        "my_turn": game.current_player() == uid,
        "ready": game.ready,
        "you": uid,
        "own": own.to_flat_list(),
        "own_ships": ships_data,
        "opp": opp.to_flat_list(hide_ships=True),
        "all_sunk": opp.all_sunk(),
        "my_all_sunk": own.all_sunk(),
        "ship_len": game.needs_ship_of_length(pnum) if game.phase != "playing" else None,
        "ships_placed": len(own.ships),
        "ships_list": list(ships_list),
        "own_mines": [list(m) for m in own.mines],
        "mine_placed": len(own.mines) > 0,
    }

def new_solo(uid, strip=False, difficulty=2):
    code = generate_unique_code(Game.generate_code, games)
    game = Game(code, uid, solo=True, strip=strip, difficulty=difficulty)
    game.player2_id = 0
    games[code] = game
    game.phase = "placing"
    if strip:
        auto_place_strip_ships(game.board2)
        game.placing[2]["ship_idx"] = len(STRIP_SHIPS) + 1  # ships + mine
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
    bot_board = game.board_for(game.opponent_id(uid))
    shots = []
    while True:
        br, bc = game.bot_ai.choose_shot(own, strip=game.strip)
        if br is None:
            break
        bresult = own.receive_shot(br, bc)
        if bresult == "repeat":
            continue
        if bresult == "mine":
            game.trigger_mine_explosion(game.opponent_id(uid))
        game.bot_ai.register_shot(br, bc, bresult, own)
        shots.append({"r": br, "c": bc, "result": bresult})
        if bresult in ("miss", "mine"):
            game.switch_turn()
            break
        if own.all_sunk() or bot_board.all_sunk():
            break
    return shots

def _check_game_over(game):
    # Finalize the game once a board is completely sunk (a victory or draw).
    if game.board1.all_sunk() or game.board2.all_sunk():
        game.phase = "finished"
        return True
    return False

def shoot(uid, code, r, c):
    game = games.get(code)
    if not game or game.current_player() != uid or game.phase != "playing":
        return None
    opp = game.opponent_board(uid)
    result = opp.receive_shot(r, c)
    if result == "repeat":
        return None
    mine_damage = None
    if result == "mine":
        mine_damage = game.trigger_mine_explosion(uid)
    bot_shots = None
    # A sunk board ends the game immediately (victory or draw).
    if _check_game_over(game):
        return {"result": result, "bot_shots": None, "mine_damage": mine_damage}
    if result in ("miss", "mine"):
        game.switch_turn()
    if game.solo and result in ("miss", "mine"):
        bot_shots = _bot_shoots(game, uid)
        _check_game_over(game)
    return {"result": result, "bot_shots": bot_shots, "mine_damage": mine_damage}

def place_auto(uid, code):
    game = games.get(code)
    pnum = game.player_num(uid)
    board = game.board_for(uid)
    board.grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    board.ships = []
    board.mines = []
    if game.strip:
        auto_place_strip_ships(board)
        game.placing[pnum]["ship_idx"] = len(STRIP_SHIPS) + 1  # ships + mine
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
    if game.strip and len(board.mines) < 1:
        return None
    if game.solo:
        if len(game.board2.ships) < len(ships_list):
            return None
        if game.strip and len(game.board2.mines) < 1:
            return None
    game.ready[pnum] = True
    if game.ready[1] and game.ready[2]:
        game.phase = "playing"
        game.turn = 1
        return True
    return False

def new_multi(uid, strip=False):
    code = generate_unique_code(Game.generate_code, games)
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

def _with_uid(uid, fn):
    if not uid:
        return {"error": "no uid"}
    return fn()


def _handle_new_solo(data, uid, code):
    return _with_uid(uid, lambda: _do_new_solo(data, uid))


def _do_new_solo(data, uid):
    strip = data.get("strip", False)
    difficulty = data.get("difficulty", 2)
    game = new_solo(uid, strip=strip, difficulty=difficulty)
    player_games[str(uid)] = game.code
    save()
    return {"ok": True, "code": game.code, "state": as_dict(game, uid)}


def _handle_new_multi(data, uid, code):
    return _with_uid(uid, lambda: _do_new_multi(data, uid))


def _do_new_multi(data, uid):
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
    if game and game.phase == 'finished':
        _evict_game(code, games, player_games)
    save()
    return {"ok": True, "result": result, "state": state}


def _handle_place_auto(data, uid, code):
    game, err = _get_game(games, code, uid)
    if err: return err
    place_auto(uid, code)
    state = as_dict(game, uid)
    save()
    return {"ok": True, "state": state}


def _handle_confirm(data, uid, code):
    game, err = _get_game(games, code, uid)
    if err: return err
    started = confirm_placement(uid, code)
    if started is None:
        return {"ok": False, "error": "not_all_placed"}
    state = as_dict(game, uid)
    save()
    return {"ok": True, "started": started, "state": state}


def _handle_upload_photo(data, uid, code):
    """Persist the strip photo. Returns ``(result, pending_send)`` where
    ``pending_send`` is ``(winner_id, photo, caption)`` when a photo must still
    be delivered to the opponent (the actual network send happens outside the
    state lock in :func:`handle_api`)."""
    game, err = _get_game(games, code, uid)
    if err: return err, None
    photo = data.get("photo")
    if not photo:
        return {"error": "no photo"}, None
    game.strip_photo = photo
    save()
    winner_id = game.opponent_id(uid)
    if game.solo or not winner_id or winner_id == 0:
        return {"ok": True}, None
    user_lang = data.get("lang", "ru")
    caption = STRIP_LOSE_CAPTIONS.get(user_lang, STRIP_LOSE_CAPTIONS['ru'])
    return {"ok": True}, (winner_id, photo, caption)


# def _handle_ana_new_solo(data, uid, code):
#     sid, g = ana_new()
#     save()
#     return {"ok": True, "sid": sid, "state": ana_state(sid)}
#
#
# def _handle_ana_new_multi(data, uid, code):
#     sid, new_code, g = ana_new_multi()
#     if uid:
#         ana_player_sessions[str(uid)] = {'code': new_code, 'sid': sid}
#     save()
#     return {"ok": True, "sid": sid, "code": new_code, "state": ana_state(sid)}
#
#
# def _handle_ana_join(data, uid, code):
#     c = data.get("code", "")
#     if not c:
#         return {"error": "no code"}
#     result = ana_join(c)
#     if not result[0]:
#         return {"ok": False, "error": result[1]}
#     if uid and result[0]:
#         ana_player_sessions[str(uid)] = {'code': c.upper(), 'sid': result[0]}
#     save()
#     return {"ok": True, "sid": result[0], "state": ana_state(result[0])}
#
#
# def _handle_ana_guess(data, uid, code):
#     sid = data.get("sid", "")
#     word = data.get("word", "")
#     result = ana_guess(sid, word)
#     if result[0] != "ok":
#         return {"ok": False, "error": result[0]}
#     save()
#     return {"ok": True, "result": result[1], "state": ana_state(sid)}
#
#
# def _handle_ana_hint(data, uid, code):
#     sid = data.get("sid", "")
#     result = ana_hint(sid)
#     if not result:
#         return {"ok": False, "error": "no_hint"}
#     save()
#     return {"ok": True, "result": result, "state": ana_state(sid)}
#
#
# def _handle_ana_state(data, uid, code):
#     sid = data.get("sid", "")
#     st = ana_state(sid)
#     if not st:
#         return {"error": "not_found"}
#     save()
#     return {"ok": True, "state": st}


# ---- Poker Dice handlers ----

def _handle_pd_new_solo(data, uid, code):
    return _with_uid(uid, lambda: _do_pd_new_solo(data, uid))


def _do_pd_new_solo(data, uid):
    c = generate_unique_code(PDGame.generate_code, pd_games)
    game = PDGame(c, uid, solo=True)
    game.player2_id = 0
    pd_games[c] = game
    pd_player_games[str(uid)] = c
    save()
    return {"ok": True, "code": c, "state": game.get_state(1)}


def _handle_pd_new_multi(data, uid, code):
    return _with_uid(uid, lambda: _do_pd_new_multi(data, uid))


def _do_pd_new_multi(data, uid):
    c = generate_unique_code(PDGame.generate_code, pd_games)
    game = PDGame(c, uid)
    pd_games[c] = game
    pd_player_games[str(uid)] = c
    save()
    return {"ok": True, "code": c, "state": game.get_state(1)}


def _handle_surrender(data, uid, code):
    game, err = _get_game(games, code, uid)
    if err: return err
    if uid != game.player1_id and uid != game.player2_id:
        return {"error": "not_in_game"}
    if game.phase != "playing":
        _evict_game(code, games, player_games)
        save()
        return {"ok": True}
    own = game.board_for(uid)
    for ship in own.ships:
        for r, c in ship.cells:
            own.grid[r][c] = SUNK
        ship.hits = set(ship.cells)
        own._mark_dead_zone(ship)
    game.phase = "finished"
    state = as_dict(game, uid)
    _evict_game(code, games, player_games)
    save()
    return {"ok": True, "state": state}


def _handle_pd_join(data, uid, code):
    game, err = _get_game(pd_games, code, uid)
    if err: return err
    if game.player1_id == uid:
        return {"ok": False, "error": "cannot_join_own_game"}
    if game.player2_id is not None:
        return {"ok": False, "error": "full"}
    if game.player2_id == uid:
        return {"ok": False, "error": "already_joined"}
    game.player2_id = uid
    pd_player_games[str(uid)] = code
    save()
    return {"ok": True, "state": game.get_state(2)}


def _handle_pd_roll(data, uid, code):
    game, err = _get_game(pd_games, code, uid)
    if err: return err
    keep = data.get("keep", [])
    st = game.roll(uid, keep)
    if st is None:
        return {"error": "invalid_roll"}
    save()
    return {"ok": True, "state": st}


def _handle_pd_score(data, uid, code):
    game, err = _get_game(pd_games, code, uid)
    if err: return err
    category = data.get("category", "")
    st = game.score(uid, category)
    if st is None:
        return {"error": "invalid_score"}
    if game.phase == 'finished':
        _evict_game(code, pd_games, pd_player_games)
    save()
    return {"ok": True, "state": st}


def _handle_pd_surrender(data, uid, code):
    game, err = _get_game(pd_games, code, uid)
    if err: return err
    st = game.surrender(uid)
    if st is None:
        return {"error": "invalid_surrender"}
    _evict_game(code, pd_games, pd_player_games)
    save()
    return {"ok": True, "state": st}


def _handle_pd_state(data, uid, code):
    game, err = _get_game(pd_games, code, uid)
    if err: return err
    pnum = game.player_num(uid)
    if pnum is None:
        return {"error": "not_in_game"}
    return {"ok": True, "state": game.get_state(pnum)}


def _add_active_game(games_list, gtype, code, game, my_turn):
    if game.phase == 'finished':
        return
    games_list.append({
        'type': gtype,
        'code': code,
        'phase': game.phase,
        'my_turn': my_turn,
    })


def _handle_active_games(data, uid, code):
    if not uid:
        return {"error": "no uid"}
    games_list = []

    # Scan all games dicts for games involving this player, instead of relying
    # on the single-code-per-player mapping that gets overwritten on new game.
    for sb_code, g in games.items():
        if uid != g.player1_id and uid != g.player2_id:
            continue
        own = g.board_for(uid)
        opp = g.opponent_board(uid)
        if not own.all_sunk() and not opp.all_sunk():
            _add_active_game(games_list, 'sea_battle', sb_code, g, g.current_player() == uid)

    for pd_code, g in pd_games.items():
        pnum = g.player_num(uid)
        if pnum:
            _add_active_game(games_list, 'poker_dice', pd_code, g, g.turn == pnum)

    for ck_code, g in checkers_games.items():
        color = g.player_color(uid)
        if color is not None:
            _add_active_game(games_list, 'checkers', ck_code, g, g.turn == color)

    return {"ok": True, "games": games_list}


def _handle_bot_info(data, uid, code):
    return {"ok": True, "bot_username": config.BOT_USERNAME, "webapp_url": config.WEBAPP_URL}


def _handle_resolve_code(data, uid, code):
    c = data.get("code", "").strip().upper()
    if not c:
        return {"error": "no code"}
    if c in games:
        return {"ok": True, "game": "sea_battle", "code": c}
    if c in pd_games:
        return {"ok": True, "game": "poker_dice", "code": c}
    if c in checkers_games:
        return {"ok": True, "game": "checkers", "code": c}
    return {"ok": False, "error": "not_found"}


# ---- Checkers handlers ----

def _handle_checkers_new_solo(data, uid, code):
    return _with_uid(uid, lambda: _do_checkers_new_solo(data, uid))


def _do_checkers_new_solo(data, uid):
    difficulty = data.get("difficulty", 2)
    c = generate_unique_code(CheckersGame.generate_code, checkers_games)
    game = CheckersGame(c, uid, solo=True, difficulty=difficulty)
    checkers_games[c] = game
    checkers_player_games[str(uid)] = c
    save()
    return {"ok": True, "code": c, "state": game.get_state(uid)}


def _handle_checkers_new_multi(data, uid, code):
    return _with_uid(uid, lambda: _do_checkers_new_multi(data, uid))


def _do_checkers_new_multi(data, uid):
    c = generate_unique_code(CheckersGame.generate_code, checkers_games)
    game = CheckersGame(c, uid)
    checkers_games[c] = game
    checkers_player_games[str(uid)] = c
    save()
    return {"ok": True, "code": c, "state": game.get_state(uid)}


def _evict_game(code, games_dict, player_games_dict):
    games_dict.pop(code, None)
    for k in [k for k, v in player_games_dict.items() if v == code]:
        del player_games_dict[k]


def _handle_checkers_join(data, uid, code):
    game, err = _get_game(checkers_games, code, uid)
    if err: return err
    if game.player1_id == uid:
        return {"ok": False, "error": "cannot_join_own_game"}
    if game.player2_id is not None:
        return {"ok": False, "error": "full"}
    if game.player2_id == uid:
        return {"ok": False, "error": "already_joined"}
    game.player2_id = uid
    checkers_player_games[str(uid)] = code
    save()
    return {"ok": True, "state": game.get_state(uid)}


def _handle_checkers_state(data, uid, code):
    game, err = _get_game(checkers_games, code, uid)
    if err: return err
    return {"ok": True, "state": game.get_state(uid)}


def _handle_checkers_move(data, uid, code):
    game, err = _get_game(checkers_games, code, uid)
    if err: return err
    if game.phase != "playing":
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
    if not moves:
        opp_color = opponent(color)
        if not has_pieces(game.board, opp_color):
            game.winner = None
            game.draw = True
        else:
            game.winner = opp_color
        game.phase = "finished"
        state = game.get_state(uid)
        _evict_game(code, checkers_games, checkers_player_games)
        save()
        return {"ok": True, "state": state, "finished": True}

    winning_move = None
    start = (start_r, start_c)
    end = (end_r, end_c)
    # If the client supplies the full landing path, prefer an exact match so
    # that with free capture choice the intended sequence is played (two legal
    # captures can share the same start/end but differ in between).
    client_path = data.get("path")
    if client_path:
        client_path = [tuple(p) for p in client_path]
        if client_path and tuple(client_path[0]) == start:
            client_path = client_path[1:]
    for m in moves:
        if m[0] != start or m[1][-1] != end:
            continue
        if client_path is not None:
            if m[1] == client_path:
                winning_move = m
                break
        else:
            winning_move = m
            break

    if not winning_move:
        return {"error": "illegal_move"}

    finished = game.make_move(winning_move)
    bot_result = None

    if game.solo and not finished and game.turn == BLACK:
        ai_diff = 6 if game.difficulty >= 3 else 3
        ai_mv = get_ai_move(game.board, BLACK, difficulty=ai_diff)
        if ai_mv:
            finished = game.make_move(ai_mv)
            ai_captures = ai_mv[2] if len(ai_mv) > 2 else []
            bot_result = {
                "move": {
                    "start": list(ai_mv[0]),
                    "end": list(ai_mv[1][-1]),
                    "path": [list(s) for s in ai_mv[1]],
                    "captures": [list(c) for c in ai_captures],
                }
            }

    if finished:
        _evict_game(code, checkers_games, checkers_player_games)
    save()
    return {
        "ok": True,
        "state": game.get_state(uid),
        "finished": finished,
        "bot_move": bot_result,
    }


def _handle_checkers_surrender(data, uid, code):
    game, err = _get_game(checkers_games, code, uid)
    if err: return err
    st = game.surrender(uid)
    if st is None:
        return {"error": "invalid_surrender"}
    _evict_game(code, checkers_games, checkers_player_games)
    save()
    return {"ok": True, "state": st}


def _handle_checkers_hint(data, uid, code):
    game, err = _get_game(checkers_games, code, uid)
    if err: return err
    if game.phase != "playing":
        return {"error": "not_playing"}
    color = game.player_color(uid)
    if color is None or game.turn != color:
        return {"error": "not_your_turn"}
    ai_diff = 6 if game.difficulty >= 3 else 3
    move = get_ai_move(game.board, color, difficulty=ai_diff)
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
    "/api/surrender": _handle_surrender,
    "/api/active_games": _handle_active_games,
    "/api/pd_new_solo": _handle_pd_new_solo,
    "/api/pd_new_multi": _handle_pd_new_multi,
    "/api/pd_join": _handle_pd_join,
    "/api/pd_roll": _handle_pd_roll,
    "/api/pd_score": _handle_pd_score,
    "/api/pd_state": _handle_pd_state,
    "/api/pd_surrender": _handle_pd_surrender,
    "/api/bot_info": _handle_bot_info,
    "/api/resolve_code": _handle_resolve_code,
    "/api/checkers_new_solo": _handle_checkers_new_solo,
    "/api/checkers_new_multi": _handle_checkers_new_multi,
    "/api/checkers_join": _handle_checkers_join,
    "/api/checkers_state": _handle_checkers_state,
    "/api/checkers_move": _handle_checkers_move,
    "/api/checkers_hint": _handle_checkers_hint,
    "/api/checkers_surrender": _handle_checkers_surrender,
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

    if path == "/api/upload_photo":
        # The state mutation runs under the lock, but the (slow) network send to
        # Telegram must happen outside it so other requests are not blocked.
        with _state_lock:
            result, pending_send = _handle_upload_photo(data, uid, code)
        if pending_send:
            winner_id, photo, caption = pending_send
            if send_strip_photo_to_winner(winner_id, photo, caption):
                return result
            return {"ok": False, "error": "send_failed"}
        return result

    with _state_lock:
        try:
            return handler(data, uid, code)
        except Exception as exc:  # defensive: never let a handler crash the HTTP handler
            logger.exception("Unhandled error in %s: %s", path, exc)
            return {"error": "internal"}
