import json
import logging
import time
from typing import Dict, Any, Callable

from game import (
    Game, SIZE, SHIPS, STRIP_SHIPS, SUNK, EMPTY,
    auto_place_ships, auto_place_strip_ships,
    auto_place_ships_adversarial, auto_place_strip_ships_adversarial,
)
from poker_dice import PokerDiceGame as PDGame
from checkers import CheckersGame, BLACK, opponent, get_legal_moves, has_pieces
from backgammon import BackgammonGame as BGGame
from checkers_ai import get_ai_move
from persist import save, flush
from auth import validate_init_data
import config

from registry import REGISTRIES, STATE_LOCK as _state_lock

from notifications import (
    _enqueue_notifications,
    mark_active as _mark_active,
    notify_recipient as _notify_recipient,
    notify_opponent as _notify_opponent,
)
from strip import send_strip_photo_to_winner, STRIP_LOSE_CAPTIONS
import stats as _stats

logger = logging.getLogger(__name__)

# All game sets live in a single registry (see registry.py). These aliases keep
# the existing handler code unchanged while making the registry the sole owner
# of the underlying dicts.
sb = REGISTRIES["sea_battle"]
pd = REGISTRIES["poker_dice"]
ck = REGISTRIES["checkers"]
bg = REGISTRIES["backgammon"]

games = sb.games
player_games = sb.player_games
checkers_games = ck.games
checkers_player_games = ck.player_games
pd_games = pd.games
pd_player_games = pd.player_games
bg_games = bg.games
bg_player_games = bg.player_games

# Guards all shared in-memory game dictionaries. The HTTP server thread and
# the bot's asyncio thread both access these, so mutations must be serialized to
# avoid race conditions. Provided by the registry as a re-entrant lock so a
# handler that already holds it can trigger a synchronous flush() safely.


def generate_unique_code(gen_fn: Callable[[], str], existing: Dict[str, Any]) -> str:
    """Return a code produced by ``gen_fn`` that is not already a key in ``existing``."""
    code = gen_fn()
    while code in existing:
        code = gen_fn()
    return code


def _record_match_stats(game_type, game):
    """Work out each side's outcome for a game that has just finished (this
    call site's transition into 'finished', not a re-read of an
    already-finished game) and record it via stats.record_match().

    Each game type exposes the finished result differently (Sea Battle has
    no explicit winner field; Checkers stores a colour + draw flag; Poker
    Dice and Backgammon resolve directly to a uid), so this maps each one to
    a single player1-relative outcome and lets record_match() mirror it for
    player2. A game type/state that isn't actually resolved is a no-op.
    """
    if game_type == "sea_battle":
        b1_dead = game.board1.all_sunk()
        b2_dead = game.board2.all_sunk()
        if b1_dead and b2_dead:
            p1_result = "draw"
        elif b2_dead:
            p1_result = "win"
        elif b1_dead:
            p1_result = "loss"
        else:
            return
    elif game_type == "checkers":
        if game.draw:
            p1_result = "draw"
        elif game.winner == 1:  # WHITE == player1's colour
            p1_result = "win"
        elif game.winner == 2:  # BLACK
            p1_result = "loss"
        else:
            return
    elif game_type == "poker_dice":
        winner = game._get_winner()
        if winner is None:
            return
        p1_result = "draw" if winner == -1 else ("win" if winner == game.player1_id else "loss")
    elif game_type == "backgammon":
        if game.winner is None:
            return
        p1_result = "win" if game.winner == game.player1_id else "loss"
    else:
        return
    _stats.record_match(game_type, game.code, game.player1_id, game.player2_id, game.solo, p1_result)


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


def _join_game(games_dict, player_games_dict, code, uid, text, event, state_fn, start_roll=False):
    """Shared join logic for the method-based games (checkers/poker/backgammon).

    ``state_fn(game, uid)`` produces the state object returned to the joiner,
    because each game exposes its state under a different key (uid vs pnum).
    When ``start_roll`` is set, the game enters the opening dice-roll phase as
    the second player joins (used by checkers/poker to decide who goes first).
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
    if start_roll:
        game.phase = "roll"
        game.reset_first_roll()
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


def _surrender_game(games_dict, player_games_dict, code, uid, text, event, game_type):
    """Shared surrender logic that notifies the opponent and evicts the game."""
    game, err = _get_game(games_dict, code, uid)
    if err:
        return err
    st = game.surrender(uid)
    if st is None:
        return {"error": "invalid_surrender"}
    _record_match_stats(game_type, game)
    _mark_active(game, uid)
    pending = _notify_opponent(game, uid, text, event, force=True)
    _evict_game(code, games_dict, player_games_dict)
    flush()
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
        "rematch": game.rematch,
        # Opening dice roll (multiplayer): each player's die, opponent's shown
        # only once both have rolled.
        "my_roll": game.first_roll.get(pnum),
        "opp_roll": (game.first_roll.get(3 - pnum)
                     if (game.first_roll.get(1) is not None and game.first_roll.get(2) is not None)
                     else None),
        "you": uid,
        "own": own.to_flat_list(),
        "own_ships": ships_data,
        # Once the game is finished, reveal the opponent's full board
        # (ships and mines) so the winner can see the complete result
        # instead of a hidden board that looks incomplete.
        "opp": opp.to_flat_list(hide_ships=(game.phase != "finished")),
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
        auto_place_strip_ships_adversarial(game.board2, difficulty)
    else:
        auto_place_ships_adversarial(game.board2, difficulty)
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
        # Both fleets are ready. Roll a die to decide who shoots first;
        # in solo the bot's die is thrown server-side immediately (the bot
        # has no uid to click the button).
        game.phase = "roll"
        game.reset_first_roll()
        if game.solo:
            game.roll_for_first(2)
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
    difficulty = data.get("difficulty", 4)
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
            _record_match_stats("sea_battle", game)
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
        if game.solo:
            pending = _notify_recipient(game, game.current_player(), "⚓ Ваш ход в Морском бое.", "started")
        else:
            pending = _notify_opponent(
                game, uid, "🎲 Оба флота готовы! Бросьте кубик — кто больше, тот ходит первым.",
                "roll", force=True)
    return {"ok": True, "started": started, "state": state}, pending


def _handle_roll_first(data, uid, code):
    game, err = _get_game(games, code, uid)
    if err:
        return err
    if game.phase != "roll":
        return {"ok": False, "error": "not_rolling"}
    res = game.apply_first_roll(game.player_num(uid))
    if res is None:
        return {"ok": False, "error": "invalid_roll"}
    bot_shots = None
    pending = []
    if res.get("winner"):
        # IMPORTANT: keep the dice result visible on the client exactly like
        # multiplayer. The client keeps drawing the roll screen (both dice +
        # who won) as long as my_roll/opp_roll are both present, so we must NOT
        # pre-empt it by taking the bot's opening shot here. The human first
        # sees the result screen (phase is "playing", turn=winner, both dice
        # set), and in solo the bot's first shot is taken only once the client
        # acknowledges the roll via _handle_bot_opening_shot.
        if game.solo and game.turn == 2:
            # Mark that the bot still owes its opening shot; it is performed
            # lazily when the client calls /api/bot_opening_shot after showing
            # the dice result. _bot_shoots is intentionally deferred.
            game.bot_pending_first = True
        pending = _notify_recipient(game, game.current_player(), "⚓ Ваш ход в Морском бое.", "started")
    _mark_active(game, uid)
    save()
    return {"ok": True, "state": as_dict(game, uid), "roll": res,
            "roll_resolved": bool(res.get("winner")), "bot_shots": bot_shots}, pending


def _handle_reroll_first(data, uid, code):
    game, err = _get_game(games, code, uid)
    if err:
        return err
    if game.phase != "roll":
        return {"ok": False, "error": "not_rolling"}
    game.reroll_first(game.player_num(uid))
    if game.solo:
        # The bot can't click the reroll button, so re-throw its die here.
        game.roll_for_first(2)
    _mark_active(game, uid)
    save()
    return {"ok": True, "state": as_dict(game, uid)}


def _handle_bot_opening_shot(data, uid, code):
    """Solo only: take the bot's opening shot after it won the dice roll.

    The opening-roll screen (both dice + who won) is shown to the human first;
    only once the client acknowledges it do we let the bot fire its first shot.
    Idempotent: once the shot is taken the pending flag is cleared.
    """
    game, err = _get_game(games, code, uid)
    if err:
        return err
    if not game.solo:
        return {"ok": False, "error": "not_solo"}
    if game.phase != "playing" or game.turn != 2 or not getattr(game, "bot_pending_first", False):
        return {"ok": True, "state": as_dict(game, uid), "bot_shots": None}
    bot_shots = _bot_shoots(game, uid)
    game.bot_pending_first = False
    _check_game_over(game)
    _mark_active(game, uid)
    save()
    return {"ok": True, "state": as_dict(game, uid), "bot_shots": bot_shots}


def _handle_rematch(data, uid, code):
    """Record a player's wish to replay on the same code.

    When both participants (or a solo player) have opted in, the same game
    object is reset for another round so nobody has to re-enter the code.
    """
    game, err = _get_game(games, code, uid)
    if err:
        return err
    if uid != game.player1_id and uid != game.player2_id:
        return {"error": "not_in_game"}
    if game.phase != "finished":
        return {"ok": False, "error": "not_finished"}
    restarted = game.request_rematch(uid)
    if restarted is None:
        return {"error": "invalid_rematch"}
    _mark_active(game, uid)
    state = as_dict(game, uid)
    if game.solo:
        pending = []
    elif restarted:
        pending = _notify_opponent(
            game, uid, "⚓ Реванш начался! Расставьте корабли.", "rematch_start", force=True)
    else:
        pending = _notify_opponent(
            game, uid, "⚓ Соперник хочет реванш! Расставьте корабли.", "rematch", force=True)
    save()
    return {"ok": True, "restarted": bool(restarted), "state": state}, pending


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
    difficulty = int(data.get('difficulty', 4))
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
    # Record the surrendering player as the loser directly, rather than via
    # _record_match_stats' board-state check: all_sunk() intentionally
    # reports False for a fleet that was never placed (e.g. surrendering
    # during the placement phase, before any ships exist), which would
    # otherwise silently skip recording anything for this match.
    p1_result = "loss" if uid == game.player1_id else "win"
    _stats.record_match("sea_battle", game.code, game.player1_id, game.player2_id, game.solo, p1_result)
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
        "🎲 Друг подключился! Бросьте кубик — кто больше, тот ходит первым.", "roll",
        lambda g, u: g.get_state(g.player_num(u)),
        start_roll=True,
    )


def _handle_pd_roll_first(data, uid, code):
    game, err = _get_game(pd_games, code, uid)
    if err:
        return err
    if game.phase != "roll":
        return {"ok": False, "error": "not_rolling"}
    # In solo the bot can't click the roll button, so make sure its die is
    # already on the table before we resolve the winner (otherwise the roll
    # never resolves and the client hangs).
    if game.solo and game.first_roll.get(2) is None:
        game.roll_for_first(2)
    res = game.apply_first_roll(game.player_num(uid))
    if res is None:
        return {"ok": False, "error": "invalid_roll"}
    # In Poker Dice the opening-roll winner takes the first turn. If the bot
    # won, run its opening turn now (reusing the same logic as
    # _handle_pd_bot_turn -- game.bot_turn()) so control returns to the human.
    if game.solo and game.phase == "playing" and game.turn == 2:
        game.bot_turn()
    _mark_active(game, uid)
    save()
    pending = []
    if res.get("winner"):
        first_uid = game.player1_id if game.turn == 1 else game.player2_id
        pending = _notify_recipient(
            game, first_uid, "🎲 Ваш ход в Покерных костях.", "started")
    return ({"ok": True, "state": game.get_state(game.player_num(uid)), "roll": res,
             "roll_resolved": bool(res.get("winner"))}, pending)


def _handle_pd_reroll_first(data, uid, code):
    game, err = _get_game(pd_games, code, uid)
    if err:
        return err
    if game.phase != "roll":
        return {"ok": False, "error": "not_rolling"}
    game.reroll_first(game.player_num(uid))
    if game.solo:
        # The bot can't click the reroll button, so re-throw its die here.
        game.roll_for_first(2)
    _mark_active(game, uid)
    save()
    return {"ok": True, "state": game.get_state(game.player_num(uid))}


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
        _record_match_stats("poker_dice", game)
        pending = _notify_opponent(game, uid, "🎲 Игра в Покерные кости окончена.", "finished", force=True)
    elif game.player_num(uid) != game.turn:
        # In solo, turn==2 here means the bot is up next but hasn't played
        # yet (bot_turn() runs as a separate follow-up request), so there is
        # no opponent to notify yet.
        if not game.solo:
            pending = _notify_opponent(game, uid, "🎲 Ваш ход в Покерных костях.", f"score:{uid}:{category}")
        else:
            pending = []
    else:
        pending = []
    if game.phase == 'finished':
        _evict_game(code, pd_games, pd_player_games)
    save()
    return {"ok": True, "state": st}, pending


def _handle_pd_bot_turn(data, uid, code):
    """Run the AI's poker-dice turn as its own step, separate from the
    request that confirmed the human player's score. Lets the client show
    the player's own result immediately, then fetch the (possibly slow,
    especially at Expert difficulty) AI turn right after.

    The AI computation runs on a private working copy of the bot's turn
    state (see PokerDiceGame.compute_bot_play) WITHOUT holding the global
    state lock, for the same reason as the checkers bot turn above.
    """
    with _state_lock:
        game, err = _get_game(pd_games, code, uid)
        if err:
            return err
        if game.player_num(uid) != 1:
            return {"error": "not_in_game"}
        can_play = game.solo and game.phase == 'playing' and game.turn == 2
        plan = game.prepare_bot_play() if can_play else None

    if plan is not None:
        plan = game.compute_bot_play(plan)

    with _state_lock:
        game = pd_games.get(code)
        if game is None:
            return {"ok": True, "state": None}
        # Re-validate: nothing else can touch a solo game's bot turn, but the
        # game could have been surrendered/evicted while we were computing.
        if can_play and game.solo and game.phase == 'playing' and game.turn == 2:
            if plan is not None:
                game.commit_bot_play(plan)
            else:
                game._advance_turn(2)
        st = game.get_state(1)
        _mark_active(game, uid)
        if game.phase == 'finished':
            _record_match_stats("poker_dice", game)
            _evict_game(code, pd_games, pd_player_games)
        save()
        return {"ok": True, "state": st}


def _handle_pd_surrender(data, uid, code):
    return _surrender_game(
        pd_games, pd_player_games, code, uid,
        "🎲 Друг сдался в Покерных костях.", "surrender", "poker_dice",
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


def _handle_stats(data, uid, code):
    if not uid:
        return {"error": "no uid"}
    return {"ok": True, "stats": _stats.get_stats(uid)}


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
    difficulty = data.get("difficulty", 4)
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
        "♟ Друг подключился! Бросьте кубик — кто больше, тот ходит первым.", "roll",
        lambda g, u: g.get_state(u),
        start_roll=True,
    )


def _handle_checkers_roll_first(data, uid, code):
    game, err = _get_game(checkers_games, code, uid)
    if err:
        return err
    if game.phase != "roll":
        return {"ok": False, "error": "not_rolling"}
    # In solo the bot can't click the roll button, so make sure its die is
    # already on the table before we resolve the winner. Without it
    # roll_for_first() never sees both dice, the winner stays None, and the
    # client hangs on "waiting for opponent to roll".
    if game.solo and game.first_roll.get(2) is None:
        game.roll_for_first(2)
    res = game.apply_first_roll(game.player_num(uid))
    if res is None:
        return {"ok": False, "error": "invalid_roll"}
    # In solo, apply_first_roll keeps the human in the White (player1) slot
    # and moves first (the bot never opens), so after the roll it is always
    # the human's turn -- no bot move is triggered here.
    _mark_active(game, uid)
    save()
    pending = []
    if res.get("winner"):
        pending = _notify_recipient(
            game, game.current_player, "♟ Ваш ход в Шашках.", "started")
    return ({"ok": True, "state": game.get_state(uid), "roll": res,
             "roll_resolved": bool(res.get("winner"))}, pending)


def _handle_checkers_reroll_first(data, uid, code):
    game, err = _get_game(checkers_games, code, uid)
    if err:
        return err
    if game.phase != "roll":
        return {"ok": False, "error": "not_rolling"}
    game.reroll_first(game.player_num(uid))
    if game.solo:
        # The bot can't click the reroll button, so re-throw its die here.
        game.roll_for_first(2)
    _mark_active(game, uid)
    save()
    return {"ok": True, "state": game.get_state(uid)}


def _handle_checkers_state(data, uid, code):
    return _state_game(checkers_games, code, uid, lambda g, u: g.get_state(u))


def _checkers_ai_difficulty(game):
    """Map the player's chosen difficulty to the AI search depth.

    Easy plays random (very beatable), Medium searches shallow, Hard searches
    deep with iterative deepening bounded by the time budget. Expert (4) goes
    deeper still; the effective depth is also capped by the time budget.
    """
    return {1: 1, 2: 4, 3: 9, 4: 12}.get(game.difficulty, 4)


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
        _record_match_stats("checkers", game)
        state = game.get_state(uid)
        _mark_active(game, uid)
        pending = _notify_opponent(game, uid, "♟ Игра в Шашки окончена.", "finished", force=True)
        _evict_game(code, checkers_games, checkers_player_games)
        flush()
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
    # Capture the position right after the player's move so the client can show
    # the checker sliding into place *immediately*, before the (slower) AI move
    # is computed. The AI's move is now a separate step (see
    # _handle_checkers_bot_turn), triggered by the client right after it
    # renders this response, instead of being computed synchronously here.
    player_state = game.get_state(uid)

    if finished:
        _evict_game(code, checkers_games, checkers_player_games)
        _record_match_stats("checkers", game)
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
        "player_state": player_state,
        "finished": finished,
        # bot_move is no longer computed synchronously here; kept as None for
        # API-shape compatibility with older clients. New clients see
        # needs_bot_turn and call /api/checkers_bot_turn right after this.
        "bot_move": None,
        "needs_bot_turn": bool(game.solo and not finished and game.turn == BLACK),
    }, pending)


def _handle_checkers_bot_turn(data, uid, code):
    """Run the AI's checkers move as its own step, separate from the request
    that confirmed the human player's move. Lets the client render the
    player's own move immediately, then fetch the AI's move right after.

    The AI search itself (up to a few seconds at Hard/Expert) runs WITHOUT
    holding the global state lock: get_ai_move() only reads the plain board
    list it's given and never touches any shared game dict, so it's safe to
    run unlocked. The lock is only held for the cheap read-validate step
    (where a defensive copy of the board is taken) and the cheap commit step
    afterwards, so a slow bot move here no longer freezes every other game on
    the server for its whole duration -- see UNLOCKED_NOTIFY_PATHS below.
    """
    with _state_lock:
        game, err = _get_game(checkers_games, code, uid)
        if err:
            return err
        if game.phase != "playing":
            return {"ok": True, "state": game.get_state(uid), "finished": game.phase == "finished", "bot_move": None}
        color = game.player_color(uid)
        if color is None or not game.solo or game.turn != BLACK:
            return {"ok": True, "state": game.get_state(uid), "finished": False, "bot_move": None}
        # Defensive copy: cheap for an 8x8 board, and guarantees the search
        # below never sees a board mutated by a concurrent request on this
        # same game while it's running unlocked.
        board_snapshot = [row[:] for row in game.board]
        ai_diff = _checkers_ai_difficulty(game)
        tb = 3.0 if game.difficulty >= 4 else 1.5

    # The expensive part: no lock held, and get_ai_move() touches nothing but
    # the board_snapshot passed in.
    ai_mv = get_ai_move(board_snapshot, BLACK, difficulty=ai_diff, time_budget=tb)

    with _state_lock:
        # Re-fetch: the game may have been surrendered/evicted by the other
        # side while the AI was thinking.
        game = checkers_games.get(code)
        if not game or game.phase != "playing" or game.player_color(uid) is None or game.turn != BLACK:
            state = game.get_state(uid) if game else None
            return {"ok": True, "state": state, "finished": bool(game and game.phase == "finished"), "bot_move": None}

        finished = False
        bot_result = None
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
            _record_match_stats("checkers", game)
        _mark_active(game, uid)
        if finished:
            pending = _notify_opponent(game, uid, "♟ Игра в Шашки окончена.", "finished", force=True)
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
        "♟ Друг сдался в Шашках.", "surrender", "checkers",
    )


def _handle_checkers_hint(data, uid, code):
    """Compute a hint move for the current player. The AI search runs
    without holding the global state lock -- see _handle_checkers_bot_turn
    for why this is safe. Read-only, so there's no commit/re-validation step.
    """
    with _state_lock:
        game, err = _get_game(checkers_games, code, uid)
        if err:
            return err
        if game.phase != "playing":
            return {"error": "not_playing"}
        color = game.player_color(uid)
        if color is None or game.turn != color:
            return {"error": "not_your_turn"}
        board_snapshot = [row[:] for row in game.board]
        ai_diff = _checkers_ai_difficulty(game)
        tb = 3.0 if game.difficulty >= 4 else 1.5

    move = get_ai_move(board_snapshot, color, difficulty=ai_diff, time_budget=tb)
    if not move:
        return {"error": "no_move"}
    return {"ok": True, "hint": {"start": list(move[0]), "end": list(move[1][-1])}}


# ---- Backgammon handlers ----

def _handle_bg_new_solo(data, uid, code):
    return _with_uid(uid, lambda: _do_bg_new_solo(data, uid))

def _do_bg_new_solo(data, uid):
    difficulty = data.get("difficulty", 2)
    variant = data.get("variant", "short")
    c = generate_unique_code(BGGame.generate_code, bg_games)
    game = BGGame(c, uid, solo=True, difficulty=difficulty, variant=variant)
    game.player2_id = 0
    return _register_new_game(bg_games, bg_player_games, game, game.get_state(uid))

def _handle_bg_new_multi(data, uid, code):
    return _with_uid(uid, lambda: _do_bg_new_multi(data, uid))

def _do_bg_new_multi(data, uid):
    variant = data.get("variant", "short")
    c = generate_unique_code(BGGame.generate_code, bg_games)
    game = BGGame(c, uid, variant=variant)
    return _register_new_game(bg_games, bg_player_games, game, game.get_state(uid))

def _handle_bg_join(data, uid, code):
    return _join_game(
        bg_games, bg_player_games, code, uid,
        "🎲 Друг подключился! Бросьте кубик — кто больше, тот ходит первым.", "roll",
        lambda g, u: g.get_state(u),
        start_roll=True,
    )

def _handle_bg_roll_first(data, uid, code):
    game, err = _get_game(bg_games, code, uid)
    if err:
        return err
    if game.phase != "roll":
        return {"ok": False, "error": "not_rolling"}
    # In solo the bot can't click the roll button, so make sure its die is
    # already on the table before we resolve the winner (otherwise the roll
    # never resolves and the client hangs on "waiting for opponent to roll").
    if game.solo and game.first_roll.get(2) is None:
        game.roll_for_first(2)
    res = game.apply_first_roll(game.player_num(uid))
    if res is None:
        return {"ok": False, "error": "invalid_roll"}
    # In solo, apply_first_roll keeps the human in the White (player1) slot
    # and moves first (the bot never opens), so after the roll it is always
    # the human's turn -- no bot move is triggered here.
    _mark_active(game, uid)
    save()
    pending = []
    if res.get("winner"):
        pending = _notify_recipient(
            game, game.current_player, "🎲 Ваш ход в Нардах.", "started")
    return ({"ok": True, "state": game.get_state(uid), "roll": res,
             "roll_resolved": bool(res.get("winner"))}, pending)


def _handle_bg_reroll_first(data, uid, code):
    game, err = _get_game(bg_games, code, uid)
    if err:
        return err
    if game.phase != "roll":
        return {"ok": False, "error": "not_rolling"}
    game.reroll_first(game.player_num(uid))
    if game.solo:
        # The bot can't click the reroll button, so re-throw its die here.
        game.roll_for_first(2)
    _mark_active(game, uid)
    save()
    return {"ok": True, "state": game.get_state(uid)}

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
    # In solo, the bot's turn (turn == -1 / BLACK) is now a separate
    # follow-up step (see _handle_bg_bot_turn) rather than something computed
    # synchronously here. needs_bot_turn tells the client explicitly whether
    # to call it, instead of the client guessing from the dice array.
    needs_bot_turn = bool(game.solo and game.phase == 'playing' and game.turn == -1)
    if game.phase == 'finished':
        _record_match_stats("backgammon", game)
        pending = _notify_opponent(game, uid, "🎲 Игра в Нарды окончена.", "finished", force=True)
    elif not game.solo and game.turn != (1 if uid == game.player1_id else -1):
        pending = _notify_opponent(game, uid, "🎲 Ваш ход в Нардах.", f"move:{uid}")
    else:
        pending = []
    if game.phase == 'finished':
        _evict_game(code, bg_games, bg_player_games)
    save()
    return {"ok": True, "state": st, "needs_bot_turn": needs_bot_turn}, pending

def _handle_bg_bot_turn(data, uid, code):
    """Run the AI's backgammon turn as its own step, separate from the
    request that confirmed the human player's move. Lets the client render
    the player's own move immediately, then fetch the AI's turn right after."""
    game, err = _get_game(bg_games, code, uid)
    if err:
        return err
    if game.player_color(uid) != 1:
        return {"error": "not_in_game"}
    st = game.bot_turn()
    if st is None:
        st = game.get_state(uid)
    _mark_active(game, uid)
    if game.phase == 'finished':
        _record_match_stats("backgammon", game)
        _evict_game(code, bg_games, bg_player_games)
    save()
    return {"ok": True, "state": st}

def _handle_bg_surrender(data, uid, code):
    return _surrender_game(
        bg_games, bg_player_games, code, uid,
        "🎲 Друг сдался в Нардах.", "surrender", "backgammon",
    )


_HANDLERS = {
    "/api/new_solo": _handle_new_solo,
    "/api/new_multi": _handle_new_multi,
    "/api/join": _handle_join,
    "/api/state": _handle_state,
    "/api/shoot": _handle_shoot,
    "/api/place_auto": _handle_place_auto,
    "/api/confirm": _handle_confirm,
    "/api/roll_first": _handle_roll_first,
    "/api/reroll_first": _handle_reroll_first,
    "/api/bot_opening_shot": _handle_bot_opening_shot,
    "/api/upload_stake": _handle_upload_stake,
    "/api/rematch": _handle_rematch,
    "/api/surrender": _handle_surrender,
    "/api/message_opponent": _handle_message_opponent,
    "/api/active_games": _handle_active_games,
    "/api/pd_new_solo": _handle_pd_new_solo,
    "/api/pd_new_multi": _handle_pd_new_multi,
    "/api/pd_join": _handle_pd_join,
    "/api/pd_roll_first": _handle_pd_roll_first,
    "/api/pd_reroll_first": _handle_pd_reroll_first,
    "/api/pd_roll": _handle_pd_roll,
    "/api/pd_score": _handle_pd_score,
    "/api/pd_bot_turn": _handle_pd_bot_turn,
    "/api/pd_state": _handle_pd_state,
    "/api/pd_surrender": _handle_pd_surrender,
    "/api/bot_info": _handle_bot_info,
    "/api/stats": _handle_stats,
    "/api/resolve_code": _handle_resolve_code,
    "/api/checkers_new_solo": _handle_checkers_new_solo,
    "/api/checkers_new_multi": _handle_checkers_new_multi,
    "/api/checkers_join": _handle_checkers_join,
    "/api/checkers_roll_first": _handle_checkers_roll_first,
    "/api/checkers_reroll_first": _handle_checkers_reroll_first,
    "/api/checkers_state": _handle_checkers_state,
    "/api/checkers_move": _handle_checkers_move,
    "/api/checkers_bot_turn": _handle_checkers_bot_turn,
    "/api/checkers_hint": _handle_checkers_hint,
    "/api/checkers_surrender": _handle_checkers_surrender,
    "/api/bg_new_solo": _handle_bg_new_solo,
    "/api/bg_new_multi": _handle_bg_new_multi,
    "/api/bg_join": _handle_bg_join,
    "/api/bg_roll_first": _handle_bg_roll_first,
    "/api/bg_reroll_first": _handle_bg_reroll_first,
    "/api/bg_state": _handle_bg_state,
    "/api/bg_roll": _handle_bg_roll,
    "/api/bg_move": _handle_bg_move,
    "/api/bg_bot_turn": _handle_bg_bot_turn,
    "/api/bg_surrender": _handle_bg_surrender,
}

NOTIFY_PATHS = {
    "/api/join", "/api/confirm", "/api/roll_first", "/api/message_opponent", "/api/rematch",
    "/api/pd_join", "/api/pd_roll_first", "/api/pd_score", "/api/pd_surrender",
    "/api/checkers_join", "/api/checkers_roll_first", "/api/checkers_move", "/api/checkers_surrender",
    "/api/bg_join", "/api/bg_roll_first", "/api/bg_move", "/api/bg_surrender",
}

# Endpoints whose expensive part is a CPU-bound AI search that can take up to
# a few seconds (Hard/Expert difficulty). Wrapping the whole handler call in
# the global STATE_LOCK -- as every other endpoint above is -- would freeze
# every other game on the server for that whole duration; this used to be
# exactly what happened here. These handlers manage their own, much narrower
# locking internally instead: the lock is only held to read/validate/commit
# game state, never while the AI is actually thinking. See their docstrings
# in the Checkers/Poker Dice sections above for the exact mechanism.
#
# checkers_bot_turn still needs the notification envelope (it can end the
# game), so it's split out from the plain default-locked set below rather
# than reusing NOTIFY_PATHS, which always wraps the whole call in the lock.
UNLOCKED_NOTIFY_PATHS = {"/api/checkers_bot_turn"}
UNLOCKED_PATHS = {"/api/checkers_hint", "/api/pd_bot_turn"}

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

    if path in UNLOCKED_NOTIFY_PATHS:
        try:
            result, pending_notifications = _split_notification_result(handler(data, uid, code))
        except Exception as exc:
            logger.exception("Unhandled error in %s: %s", path, exc)
            return {"error": "internal"}
        _enqueue_notifications(pending_notifications)
        return result

    if path in UNLOCKED_PATHS:
        try:
            return handler(data, uid, code)
        except Exception as exc:
            logger.exception("Unhandled error in %s: %s", path, exc)
            return {"error": "internal"}

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
            # Keep the finished game in memory so both players can opt into a
            # rematch on the same code (the game is still persisted and pruned
            # after 24h like every other finished game).
            flush()
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
