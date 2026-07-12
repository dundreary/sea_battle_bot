import json
import logging
import threading
import time
from typing import Dict, Any, Callable

from game import Game, SIZE, SHIPS, STRIP_SHIPS, SUNK, EMPTY, auto_place_ships, auto_place_strip_ships
from poker_dice import PokerDiceGame as PDGame, games as pd_games, player_games as pd_player_games
from checkers import CheckersGame, BLACK, opponent, get_legal_moves, has_pieces
from backgammon import BackgammonGame as BGGame, games as bg_games, player_games as bg_player_games
from checkers_ai import get_ai_move
from persist import save
from auth import validate_init_data
import config

from notifications import (
    _enqueue_notifications,
    mark_active as _mark_active,
    notify_recipient as _notify_recipient,
    notify_opponent as _notify_opponent,
)
from strip import send_strip_photo_to_winner, STRIP_LOSE_CAPTIONS

logger = logging.getLogger(__name__)

# Notification delivery (see notifications.py) and strip-mode stake-photo
# delivery (see strip.py) are extracted into their own modules. The helpers
# below are re-exported under their historical names so call sites in this
# file are unchanged.

games: Dict[str, Game] = {}
player_games: Dict[str, str] = {}

# Checkers games
checkers_games: Dict[str, CheckersGame] = {}
checkers_player_games: Dict[str, str] = {}

# Guards all shared in-memory game dictionaries below. The HTTP server thread and
# the bot's asyncio thread both access these, so mutations must be serialized to
# avoid race conditions.
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


def _register_new_game(games_dict, player_games_dict, game, state):
    """Store a freshly created game, map its creator, persist, and return it."""
    games_dict[game.code] = game
    player_games_dict[str(game.player1_id)] = game.code
    save()
    return {"ok": True, "code": game.code, "state": state}


def _join_game(games_dict, player_games_dict, code, uid, text, event, state_fn):
    """Shared join logic for the method-based games (checkers/poker/backgammon).

    ``state_fn(game, uid)`` produces the state object returned to the joiner,
    because each game exposes its state under a different key (uid vs pnum).
    """
    game, err = _get_game(games_dict, code, uid)
    if err:
        return err
    if game.player1_id == uid:
        return {"ok": False, "error": "cannot_join_own_game"}
    if game.player2_id is not None:
        return {"ok": False, "error": "full"}
    if game.player2_id == uid:
        return {"ok": False, "error": "already_joined"}
    game.player2_id = uid
    player_games_dict[str(uid)] = code
    _mark_active(game, uid)
    save()
    return (
        {"ok": True, "state": state_fn(game, uid)},
        _notify_opponent(game, uid, text, event, force=True),
    )


def _state_game(games_dict, code, uid, state_fn):
    """Shared state lookup that also delivers queued in-game messages."""
    game, err = _get_game(games_dict, code, uid)
    if err:
        return err
    _mark_active(game, uid)
    state = state_fn(game, uid)
    if state is None:
        return {"error": "not_in_game"}
    state["messages"] = _pop_in_game_messages(game, uid)
    return {"ok": True, "state": state}


def _surrender_game(games_dict, player_games_dict, code, uid, text, event):
    """Shared surrender logic that notifies the opponent and evicts the game."""
    game, err = _get_game(games_dict, code, uid)
    if err:
        return err
    st = game.surrender(uid)
    if st is None:
        return {"error": "invalid_surrender"}
    _mark_active(game, uid)
    pending = _notify_opponent(game, uid, text, event, force=True)
    _evict_game(code, games_dict, player_games_dict)
    save()
    return {"ok": True, "state": st}, pending


def _authenticate(data):
    """Return a verified Telegram user id for this request, or None if it
    can't be authenticated.

    The client-supplied ``uid`` field is NEVER trusted by itself -- it must
    match the user embedded in a Telegram-signed ``init_data`` string (see
    auth.py). Without this, knowing someone's game code and their uid was
    enough to act as them.

    A regular browser has no signed Telegram payload. When browser access is
    enabled, it falls back to the locally generated uid only if ``init_data``
    is entirely absent; malformed Telegram payloads are still rejected.
    """
    if getattr(config, "SKIP_TELEGRAM_AUTH", False):
        uid = data.get("uid")
        try:
            return int(uid) if uid else None
        except (TypeError, ValueError):
            return None
    init_data = data.get("init_data", "")
    if init_data:
        return validate_init_data(init_data, config.BOT_TOKEN)
    if getattr(config, "ALLOW_BROWSER_AUTH", True):
        try:
            uid = data.get("uid")
            return int(uid) if uid else None
        except (TypeError, ValueError):
            return None
    return None


def _pop_in_game_messages(game, uid):
    """Return and consume messages addressed to a player in a game client."""
    pending = getattr(game, "in_game_messages", [])
    received = [item["text"] for item in pending if item["recipient"] == uid]
    game.in_game_messages = [item for item in pending if item["recipient"] != uid]
    return received


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
        # The strip stake photos are committed before the game starts.
        # Each player sees their own stake (strip_stake); the winner also
        # sees the loser's stake (opp_stake) once the loser is sunk.
        "strip_stake": game.strip_stakes.get(pnum, "") if game.strip else "",
        "opp_stake": (game.strip_stakes.get(3 - pnum, "") if (game.strip and opp.all_sunk()) else ""),
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
        "ships_placed": len(own.ships),
        "ships_list": list(ships_list),
        "own_mines": [list(m) for m in own.mines],
        "mine_placed": len(own.mines) > 0,
        "messages": _pop_in_game_messages(game, uid),
    }

def new_solo(uid, strip=False, difficulty=2):
    code = generate_unique_code(Game.generate_code, games)
    game = Game(code, uid, solo=True, strip=strip, difficulty=difficulty)
    game.player2_id = 0
    game.phase = "placing"
    if strip:
        auto_place_strip_ships(game.board2)
    else:
        auto_place_ships(game.board2)
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
    board = game.board_for(uid)
    board.grid = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
    board.ships = []
    board.mines = []
    if game.strip:
        auto_place_strip_ships(board)
    else:
        auto_place_ships(board)
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
    # In strip mode every human participant must commit a stake photo
    # before they can confirm placement.
    if game.strip and not game.strip_stakes.get(pnum):
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
    return game

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
    return _register_new_game(games, player_games, game, as_dict(game, uid))


def _handle_new_multi(data, uid, code):
    return _with_uid(uid, lambda: _do_new_multi(data, uid))


def _do_new_multi(data, uid):
    strip = data.get("strip", False)
    game = new_multi(uid, strip=strip)
    return _register_new_game(games, player_games, game, as_dict(game, uid))


def _handle_join(data, uid, code):
    if not uid or not code:
        return {"error": "no uid/code"}
    game = games.get(code)
    if not game:
        return {"ok": False, "error": "not_found"}
    if game.player1_id == uid:
        return {"ok": False, "error": "cannot_join_own_game"}
    if game.player2_id is not None:
        return {"ok": False, "error": "full"}
    game.player2_id = uid
    game.phase = "placing"
    player_games[str(uid)] = code
    _mark_active(game, uid)
    save()
    return (
        {"ok": True, "state": as_dict(game, uid)},
        _notify_opponent(game, uid, "⚓ Друг подключился к игре. Расставьте корабли, чтобы начать.", "join", force=True),
    )


def _handle_state(data, uid, code):
    state = get_state(uid, code)
    if not state:
        return {"error": "no game"}
    _mark_active(games[code], uid)
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
    pending_notifications = []
    if game:
        _mark_active(game, uid)
        if game.phase == 'finished':
            pending_notifications = _notify_opponent(
                game, uid, "⚓ Игра в Морской бой окончена.", "finished", force=True)
        elif game.current_player() != uid:
            pending_notifications = _notify_opponent(
                game, uid, "⚓ Ваш ход в Морском бое.", f"shoot:{uid}:{r}:{c}")
    pending_stake = None
    # When a strip game finishes, deliver the loser's pre-committed stake
    # photo to the winner. Regular finished games are retained for up to a
    # day so both players can retrieve the final board and see the result.
    if game and game.phase == 'finished':
        if game.strip:
            loser_id = game.opponent_id(uid)
            loser_stake = game.strip_stakes.get(game.player_num(loser_id), "")
            if loser_stake:
                caption = STRIP_LOSE_CAPTIONS['ru']
                pending_stake = (uid, loser_stake, caption)
    save()
    return {"ok": True, "result": result, "state": state}, pending_stake, pending_notifications


def _handle_place_auto(data, uid, code):
    game, err = _get_game(games, code, uid)
    if err:
        return err
    place_auto(uid, code)
    state = as_dict(game, uid)
    _mark_active(game, uid)
    save()
    return {"ok": True, "state": state}


def _handle_confirm(data, uid, code):
    game, err = _get_game(games, code, uid)
    if err:
        return err
    started = confirm_placement(uid, code)
    if started is None:
        game = games.get(code)
        if game and game.strip and not game.strip_stakes.get(game.player_num(uid)):
            return {"ok": False, "error": "need_stake"}
        return {"ok": False, "error": "not_all_placed"}
    state = as_dict(game, uid)
    _mark_active(game, uid)
    save()
    pending = []
    if started:
        pending = _notify_recipient(game, game.current_player(), "⚓ Ваш ход в Морском бое.", "started")
    return {"ok": True, "started": started, "state": state}, pending


def _handle_upload_stake(data, uid, code):
    """Persist a player's strip "stake" photo. Stakes are committed
    before the game starts (during placement) so a participant cannot
    join a strip game and then refuse the forfeit."""
    game, err = _get_game(games, code, uid)
    if err:
        return err
    if uid != game.player1_id and uid != game.player2_id:
        return {"error": "not_in_game"}
    photo = data.get("photo")
    if not photo:
        return {"error": "no photo"}
    pnum = game.player_num(uid)
    game.strip_stakes[pnum] = photo
    save()
    return {"ok": True}


# ---- Poker Dice handlers ----

def _handle_pd_new_solo(data, uid, code):
    return _with_uid(uid, lambda: _do_pd_new_solo(data, uid))


def _do_pd_new_solo(data, uid):
    c = generate_unique_code(PDGame.generate_code, pd_games)
    difficulty = int(data.get('difficulty', 3))
    game = PDGame(c, uid, solo=True, difficulty=difficulty)
    game.player2_id = 0
    return _register_new_game(pd_games, pd_player_games, game, game.get_state(1))


def _handle_pd_new_multi(data, uid, code):
    return _with_uid(uid, lambda: _do_pd_new_multi(data, uid))


def _do_pd_new_multi(data, uid):
    c = generate_unique_code(PDGame.generate_code, pd_games)
    game = PDGame(c, uid)
    return _register_new_game(pd_games, pd_player_games, game, game.get_state(1))


def _handle_surrender(data, uid, code):
    game, err = _get_game(games, code, uid)
    if err:
        return err, None, []
    if uid != game.player1_id and uid != game.player2_id:
        return {"error": "not_in_game"}, None, []
    # Sink the surrendering player's ships so the opponent sees a clean result,
    # whether this is an in-progress surrender, a surrender during placement, or
    # a repeat call on an already-finished game. We return a state snapshot
    # (instead of an empty ok) so the client can show the result overlay.
    own = game.board_for(uid)
    for ship in own.ships:
        for r, c in ship.cells:
            own.grid[r][c] = SUNK
        ship.hits = set(ship.cells)
        own._mark_dead_zone(ship)
    game.phase = "finished"
    state = as_dict(game, uid)
    _mark_active(game, uid)
    pending = _notify_opponent(game, uid, "⚓ Друг сдался в Морском бое.", "surrender", force=True)
    pending_stake = None
    if game.strip:
        # The surrendering player (uid) is the loser; deliver their
        # pre-committed stake photo to the winner, same as a normal finish
        # via /api/shoot. The game is evicted by the caller once that
        # delivery attempt (best-effort) completes.
        winner_id = game.opponent_id(uid)
        loser_stake = game.strip_stakes.get(game.player_num(uid), "")
        if loser_stake and winner_id:
            user_lang = data.get("lang", "ru")
            caption = STRIP_LOSE_CAPTIONS.get(user_lang, STRIP_LOSE_CAPTIONS['ru'])
            pending_stake = (winner_id, loser_stake, caption)
    save()
    return {"ok": True, "state": state}, pending_stake, pending


def _handle_message_opponent(data, uid, code):
    """Send a short Telegram notification to the opponent in a live game."""
    game_type = data.get("game", "sea_battle")
    game_sets = {
        "sea_battle": games,
        "poker_dice": pd_games,
        "checkers": checkers_games,
        "backgammon": bg_games,
    }
    games_dict = game_sets.get(game_type)
    if games_dict is None:
        return {"error": "unknown_game"}
    game, err = _get_game(games_dict, code, uid)
    if err:
        return err
    if uid not in (game.player1_id, game.player2_id):
        return {"error": "not_in_game"}
    if game.solo or game.phase != "playing":
        return {"error": "message_unavailable"}

    message = data.get("message", "")
    if not isinstance(message, str):
        return {"error": "invalid_message"}
    message = " ".join(message.split())[:280]
    if not message:
        return {"error": "empty_message"}

    last_sent = getattr(game, "last_message_sent", {})
    now = time.time()
    if now - last_sent.get(str(uid), 0) < 3:
        return {"error": "message_rate_limited"}
    last_sent[str(uid)] = now
    game.last_message_sent = last_sent

    recipient = game.opponent_id(uid) if hasattr(game, "opponent_id") else (
        game.player2_id if uid == game.player1_id else game.player1_id
    )
    game.in_game_messages = getattr(game, "in_game_messages", [])
    game.in_game_messages.append({
        "recipient": recipient,
        "text": message,
    })
    return {"ok": True}, []


def _handle_pd_join(data, uid, code):
    return _join_game(
        pd_games, pd_player_games, code, uid,
        "🎲 Друг подключился к игре. Ваш ход в Покерных костях.", "join",
        lambda g, u: g.get_state(g.player_num(u)),
    )


def _handle_pd_roll(data, uid, code):
    game, err = _get_game(pd_games, code, uid)
    if err:
        return err
    keep = data.get("keep", [])
    st = game.roll(uid, keep)
    if st is None:
        return {"error": "invalid_roll"}
    _mark_active(game, uid)
    save()
    return {"ok": True, "state": st}


def _handle_pd_score(data, uid, code):
    game, err = _get_game(pd_games, code, uid)
    if err:
        return err
    category = data.get("category", "")
    st = game.score(uid, category)
    if st is None:
        return {"error": "invalid_score"}
    _mark_active(game, uid)
    if game.phase == 'finished':
        pending = _notify_opponent(game, uid, "🎲 Игра в Покерные кости окончена.", "finished", force=True)
    elif game.player_num(uid) != game.turn:
        pending = _notify_opponent(game, uid, "🎲 Ваш ход в Покерных костях.", f"score:{uid}:{category}")
    else:
        pending = []
    if game.phase == 'finished':
        _evict_game(code, pd_games, pd_player_games)
    save()
    return {"ok": True, "state": st}, pending


def _handle_pd_surrender(data, uid, code):
    return _surrender_game(
        pd_games, pd_player_games, code, uid,
        "🎲 Друг сдался в Покерных костях.", "surrender",
    )


def _handle_pd_state(data, uid, code):
    return _state_game(
        pd_games, code, uid,
        lambda g, u: g.get_state(g.player_num(u)) if g.player_num(u) is not None else None,
    )


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

    for bg_code, g in bg_games.items():
        color = g.player_color(uid)
        if color is not None:
            _add_active_game(games_list, 'backgammon', bg_code, g, g.turn == color)

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
    if c in bg_games:
        return {"ok": True, "game": "backgammon", "code": c}
    return {"ok": False, "error": "not_found"}


# ---- Checkers handlers ----

def _handle_checkers_new_solo(data, uid, code):
    return _with_uid(uid, lambda: _do_checkers_new_solo(data, uid))


def _do_checkers_new_solo(data, uid):
    difficulty = data.get("difficulty", 2)
    c = generate_unique_code(CheckersGame.generate_code, checkers_games)
    game = CheckersGame(c, uid, solo=True, difficulty=difficulty)
    return _register_new_game(checkers_games, checkers_player_games, game, game.get_state(uid))


def _handle_checkers_new_multi(data, uid, code):
    return _with_uid(uid, lambda: _do_checkers_new_multi(data, uid))


def _do_checkers_new_multi(data, uid):
    c = generate_unique_code(CheckersGame.generate_code, checkers_games)
    game = CheckersGame(c, uid)
    return _register_new_game(checkers_games, checkers_player_games, game, game.get_state(uid))


def _evict_game(code, games_dict, player_games_dict):
    games_dict.pop(code, None)
    for k in [k for k, v in player_games_dict.items() if v == code]:
        del player_games_dict[k]


def _handle_checkers_join(data, uid, code):
    return _join_game(
        checkers_games, checkers_player_games, code, uid,
        "♟ Друг подключился к игре. Ваш ход в Шашках.", "join",
        lambda g, u: g.get_state(u),
    )


def _handle_checkers_state(data, uid, code):
    return _state_game(checkers_games, code, uid, lambda g, u: g.get_state(u))


def _checkers_ai_difficulty(game):
    """Map the player's chosen difficulty to the AI search depth."""
    return 6 if game.difficulty >= 3 else 3


def _handle_checkers_move(data, uid, code):
    game, err = _get_game(checkers_games, code, uid)
    if err:
        return err
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
        _mark_active(game, uid)
        pending = _notify_opponent(game, uid, "♟ Игра в Шашки окончена.", "finished", force=True)
        _evict_game(code, checkers_games, checkers_player_games)
        save()
        return {"ok": True, "state": state, "finished": True}, pending

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
        ai_diff = _checkers_ai_difficulty(game)
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
    _mark_active(game, uid)
    if finished:
        pending = _notify_opponent(game, uid, "♟ Игра в Шашки окончена.", "finished", force=True)
    elif not game.solo and game.current_player != uid:
        pending = _notify_opponent(game, uid, "♟ Ваш ход в Шашках.", f"move:{game.last_move}")
    else:
        pending = []
    save()
    return ({
        "ok": True,
        "state": game.get_state(uid),
        "finished": finished,
        "bot_move": bot_result,
    }, pending)


def _handle_checkers_surrender(data, uid, code):
    return _surrender_game(
        checkers_games, checkers_player_games, code, uid,
        "♟ Друг сдался в Шашках.", "surrender",
    )


def _handle_checkers_hint(data, uid, code):
    game, err = _get_game(checkers_games, code, uid)
    if err:
        return err
    if game.phase != "playing":
        return {"error": "not_playing"}
    color = game.player_color(uid)
    if color is None or game.turn != color:
        return {"error": "not_your_turn"}
    ai_diff = _checkers_ai_difficulty(game)
    move = get_ai_move(game.board, color, difficulty=ai_diff)
    if not move:
        return {"error": "no_move"}
    return {"ok": True, "hint": {"start": list(move[0]), "end": list(move[1][-1])}}


# ---- Backgammon handlers ----

def _handle_bg_new_solo(data, uid, code):
    return _with_uid(uid, lambda: _do_bg_new_solo(data, uid))

def _do_bg_new_solo(data, uid):
    difficulty = data.get("difficulty", 2)
    c = generate_unique_code(BGGame.generate_code, bg_games)
    game = BGGame(c, uid, solo=True, difficulty=difficulty)
    game.player2_id = 0
    return _register_new_game(bg_games, bg_player_games, game, game.get_state(uid))

def _handle_bg_new_multi(data, uid, code):
    return _with_uid(uid, lambda: _do_bg_new_multi(data, uid))

def _do_bg_new_multi(data, uid):
    c = generate_unique_code(BGGame.generate_code, bg_games)
    game = BGGame(c, uid)
    return _register_new_game(bg_games, bg_player_games, game, game.get_state(uid))

def _handle_bg_join(data, uid, code):
    return _join_game(
        bg_games, bg_player_games, code, uid,
        "🎲 Друг подключился к игре. Ваш ход в Нардах.", "join",
        lambda g, u: g.get_state(u),
    )

def _handle_bg_state(data, uid, code):
    return _state_game(bg_games, code, uid, lambda g, u: g.get_state(u))

def _handle_bg_roll(data, uid, code):
    game, err = _get_game(bg_games, code, uid)
    if err:
        return err
    st = game.roll(uid)
    if st is None:
        return {"error": "invalid_roll"}
    _mark_active(game, uid)
    save()
    return {"ok": True, "state": st}

def _handle_bg_move(data, uid, code):
    game, err = _get_game(bg_games, code, uid)
    if err:
        return err
    from_idx = data.get("from")
    to_idx = data.get("to")
    if from_idx is None and to_idx is None:
        st = game.get_state(uid) if game else None
        if st:
            _mark_active(game, uid)
        return {"ok": True, "state": st}
    if from_idx == -1 and to_idx == -1:
        st = game.pass_turn(uid)
        if st is None:
            return {"error": "invalid_pass"}
    else:
        st = game.move(uid, from_idx, to_idx if to_idx is not None else -1)
        if st is None:
            return {"error": "invalid_move"}
    _mark_active(game, uid)
    if game.phase == 'finished':
        pending = _notify_opponent(game, uid, "🎲 Игра в Нарды окончена.", "finished", force=True)
    elif game.turn != (1 if uid == game.player1_id else -1):
        pending = _notify_opponent(game, uid, "🎲 Ваш ход в Нардах.", f"move:{uid}")
    else:
        pending = []
    if game.phase == 'finished':
        _evict_game(code, bg_games, bg_player_games)
    save()
    return {"ok": True, "state": st}, pending

def _handle_bg_surrender(data, uid, code):
    return _surrender_game(
        bg_games, bg_player_games, code, uid,
        "🎲 Друг сдался в Нардах.", "surrender",
    )


_HANDLERS = {
    "/api/new_solo": _handle_new_solo,
    "/api/new_multi": _handle_new_multi,
    "/api/join": _handle_join,
    "/api/state": _handle_state,
    "/api/shoot": _handle_shoot,
    "/api/place_auto": _handle_place_auto,
    "/api/confirm": _handle_confirm,
    "/api/upload_stake": _handle_upload_stake,
    "/api/surrender": _handle_surrender,
    "/api/message_opponent": _handle_message_opponent,
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
    "/api/bg_new_solo": _handle_bg_new_solo,
    "/api/bg_new_multi": _handle_bg_new_multi,
    "/api/bg_join": _handle_bg_join,
    "/api/bg_state": _handle_bg_state,
    "/api/bg_roll": _handle_bg_roll,
    "/api/bg_move": _handle_bg_move,
    "/api/bg_surrender": _handle_bg_surrender,
}

NOTIFY_PATHS = {
    "/api/join", "/api/confirm", "/api/message_opponent",
    "/api/pd_join", "/api/pd_score", "/api/pd_surrender",
    "/api/checkers_join", "/api/checkers_move", "/api/checkers_surrender",
    "/api/bg_join", "/api/bg_move", "/api/bg_surrender",
}

# Handlers on these paths can end a strip game and must deliver the loser's
# pre-committed stake photo to the winner before the game is evicted. They
# return a 3-tuple: (response, pending_stake_or_None, pending_notifications).
STAKE_PATHS = {"/api/shoot", "/api/surrender"}

# Endpoints that don't act on behalf of a specific authenticated player and
# so don't need init_data verification.
_NO_AUTH_PATHS = {"/api/bot_info", "/api/resolve_code"}


def _split_notification_result(out):
    """Handlers with notifications return ``(response, pending_messages)``."""
    if isinstance(out, tuple) and len(out) == 2 and isinstance(out[1], list):
        return out
    return out, []


def handle_api(path, body):
    try:
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        data = {}
    code = data.get("code")

    handler = _HANDLERS.get(path)
    if not handler:
        return {"error": "unknown path"}

    if path in _NO_AUTH_PATHS:
        uid = data.get("uid")
    else:
        uid = _authenticate(data)
        if uid is None:
            return {"error": "auth_failed"}

    if path in STAKE_PATHS:
        # The state mutation runs under the lock; the (slow) network send to
        # Telegram happens outside it so other requests are not blocked. The
        # game is evicted right after that delivery attempt (success or not)
        # instead of being left in memory/persist.json indefinitely.
        try:
            with _state_lock:
                response, pending_stake, pending_notifications = handler(data, uid, code)
        except Exception as exc:
            logger.exception("Unhandled error in %s: %s", path, exc)
            return {"error": "internal"}
        _enqueue_notifications(pending_notifications)
        if pending_stake:
            winner_id, photo, caption = pending_stake
            send_strip_photo_to_winner(winner_id, photo, caption)
            with _state_lock:
                _evict_game(code, games, player_games)
                save()
        return response

    if path in NOTIFY_PATHS:
        try:
            with _state_lock:
                result, pending_notifications = _split_notification_result(handler(data, uid, code))
        except Exception as exc:
            logger.exception("Unhandled error in %s: %s", path, exc)
            return {"error": "internal"}
        _enqueue_notifications(pending_notifications)
        return result

    with _state_lock:
        try:
            return handler(data, uid, code)
        except Exception as exc:  # defensive: never let a handler crash the HTTP handler
            logger.exception("Unhandled error in %s: %s", path, exc)
            return {"error": "internal"}
