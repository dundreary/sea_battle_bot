import json
from game import Game, SIZE, SHIPS, auto_place_ships

games = {}
player_games = {}

def as_dict(game, uid):
    pnum = game.player_num(uid) if not game.solo else 1
    own = game.board_for(uid)
    opp = game.opponent_board(uid)
    return {
        "code": game.code,
        "solo": game.solo,
        "phase": game.phase,
        "turn": game.turn,
        "current_player": game.current_player(),
        "my_turn": game.current_player() == uid,
        "ready": game.ready,
        "you": uid,
        "own": [own.grid[r][c] for r in range(SIZE) for c in range(SIZE)],
        "opp": [opp.grid[r][c] for r in range(SIZE) for c in range(SIZE)],
        "all_sunk": opp.all_sunk(),
        "my_all_sunk": own.all_sunk(),
        "ship_len": game.needs_ship_of_length(pnum) if game.phase != "playing" else None,
        "ships_placed": len(own.ships),
    }

def new_solo(uid):
    code = Game.generate_code()
    while code in games:
        code = Game.generate_code()
    game = Game(code, uid, solo=True)
    game.player2_id = 0
    games[code] = game
    game.phase = "placing"
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

def shoot(uid, code, r, c):
    game = games.get(code)
    if not game or game.current_player() != uid or game.phase != "playing":
        return None
    opp = game.opponent_board(uid)
    result = opp.receive_shot(r, c)
    if result == "repeat":
        return None
    bot_shot = None
    if result == "miss":
        game.switch_turn()
    if game.solo and result == "miss":
        own = game.board_for(uid)
        br, bc = game.bot_ai.choose_shot(own)
        if br is not None:
            bresult = own.receive_shot(br, bc)
            game.bot_ai.register_shot(br, bc, bresult, own)
            bot_shot = {"r": br, "c": bc, "result": bresult}
            if bresult == "miss":
                game.switch_turn()
    return {"result": result, "bot_shot": bot_shot}

def place_auto(uid, code):
    game = games.get(code)
    pnum = game.player_num(uid)
    board = game.board_for(uid)
    auto_place_ships(board)
    game.placing[pnum]["ship_idx"] = len(SHIPS)
    game.ready[pnum] = True
    if game.ready[1] and game.ready[2]:
        game.phase = "playing"
        game.turn = 1
    return game.phase == "playing"

def handle_api(path, body):
    try:
        data = json.loads(body) if body else {}
    except:
        data = {}
    uid = data.get("uid")
    code = data.get("code")

    if path == "/api/new_solo":
        if not uid:
            return {"error": "no uid"}
        game = new_solo(uid)
        player_games[uid] = game.code
        return {"ok": True, "code": game.code, "state": as_dict(game, uid)}

    if path == "/api/state":
        if not uid or not code:
            return {"error": "no uid/code"}
        state = get_state(uid, code)
        if not state:
            return {"error": "no game"}
        return {"ok": True, "state": state}

    if path == "/api/shoot":
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
        return {"ok": True, "result": result, "state": state}

    if path == "/api/place_auto":
        if not uid or not code:
            return {"error": "no uid/code"}
        started = place_auto(uid, code)
        game = games.get(code)
        state = as_dict(game, uid) if game else None
        return {"ok": True, "started": started, "state": state}

    return {"error": "unknown path"}
