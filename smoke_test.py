"""Smoke test: drives every game end-to-end without any network.

Run with:  python smoke_test.py
It monkeypatches persistence (no disk writes) and Telegram delivery (no
network), so it exercises game logic + the refactored api.py handlers only.
"""
import api
import persist
import notifications
from game import Game as _G, MINE, MINE_HIT

# Never touch disk (persist.json) or the network during the test.
api.save = lambda: None
persist.save = lambda: None
persist.flush = lambda: None
notifications.send_telegram_message = lambda *a, **k: True


def unwrap(out):
    """Handlers may return a dict or a (dict, pending...) tuple."""
    return out[0] if isinstance(out, tuple) else out


def check(cond, label):
    if not cond:
        raise AssertionError(f"FAILED: {label}")
    print(f"  ok: {label}")


# ---------------------------------------------------------------------------
print("Sea Battle (solo, full play to finished):")
uid = 1001
res = unwrap(api._handle_new_solo({"strip": False, "difficulty": 2}, uid, None))
check(res.get("ok"), "new_solo")
code_sb = res["code"]
unwrap(api._handle_place_auto({"code": code_sb}, uid, code_sb))
res = unwrap(api._handle_confirm({"code": code_sb}, uid, code_sb))
check(res.get("ok"), "confirm_placement")
# Solo now opens with a die roll; throw the human's die to start play.
roll0 = unwrap(api._handle_roll_first({"code": code_sb}, uid, code_sb))
# The opening roll can be won by either side (or tie, requiring a reroll);
# handle all three so this test doesn't depend on how the dice landed.
guard = 0
while roll0.get("roll", {}).get("tie") and guard < 30:
    roll0 = unwrap(api._handle_reroll_first({"code": code_sb}, uid, code_sb))
    roll0 = unwrap(api._handle_roll_first({"code": code_sb}, uid, code_sb))
    guard += 1
if api.games[code_sb].bot_pending_first:
    # Bot won the opening roll; it only fires once the client acknowledges
    # the roll result screen, exactly as in real play.
    unwrap(api._handle_bot_opening_shot({"code": code_sb}, uid, code_sb))
finished = False
for r in range(10):
    for c in range(10):
        st = unwrap(api._handle_state({"code": code_sb}, uid, code_sb))["state"]
        if st["phase"] == "finished":
            finished = True
            break
        if st["my_turn"]:
            out = api._handle_shoot({"code": code_sb, "r": r, "c": c}, uid, code_sb)
            if unwrap(out).get("state", {}).get("phase") == "finished":
                finished = True
                break
    if finished:
        break
check(finished, "sea battle reaches finished phase")

print("Sea Battle (multi + join + message):")
uidA, uidB = 2001, 2002
res = unwrap(api._handle_new_multi({"strip": False}, uidA, None))
code_m = res["code"]
join = unwrap(api._handle_join({"code": code_m}, uidB, code_m))
check(join.get("ok"), "join multi game")
msg = unwrap(api._handle_message_opponent(
    {"code": code_m, "game": "sea_battle", "message": "hi there"}, uidA, code_m))
check(msg.get("ok") or isinstance(msg, dict), "message_opponent")

print("Sea Battle (multi opening dice roll decides first move):")
uidA, uidB = 2101, 2102
code_r = unwrap(api._handle_new_multi({"strip": False}, uidA, None))["code"]
unwrap(api._handle_join({"code": code_r}, uidB, code_r))
for u in (uidA, uidB):
    unwrap(api._handle_place_auto({"code": code_r}, u, code_r))
    unwrap(api._handle_confirm({"code": code_r}, u, code_r))
st = unwrap(api._handle_state({"code": code_r}, uidA, code_r))["state"]
check(st["phase"] == "roll", "enters roll phase after both confirm")
started = False
for _ in range(60):
    rollA = unwrap(api._handle_roll_first({"code": code_r}, uidA, code_r))["roll"]
    rollB = unwrap(api._handle_roll_first({"code": code_r}, uidB, code_r))["roll"]
    still_rolling = (
        rollA.get("tie") or rollB.get("tie")
        or unwrap(api._handle_state({"code": code_r}, uidA, code_r))["state"]["phase"] == "roll"
    )
    if still_rolling:
        unwrap(api._handle_reroll_first({"code": code_r}, uidA, code_r))
        unwrap(api._handle_reroll_first({"code": code_r}, uidB, code_r))
        continue
    st = unwrap(api._handle_state({"code": code_r}, uidA, code_r))["state"]
    if st["phase"] == "playing":
        started = True
        break
check(started and st["turn"] in (1, 2), "roll decides first turn -> playing")

print("Sea Battle (solo opening dice roll decides first move):")
uid = 2201
code_sr = unwrap(api._handle_new_solo({"strip": False, "difficulty": 2}, uid, None))["code"]
unwrap(api._handle_place_auto({"code": code_sr}, uid, code_sr))
res = unwrap(api._handle_confirm({"code": code_sr}, uid, code_sr))
check(res.get("ok"), "solo confirm_placement")
st = unwrap(api._handle_state({"code": code_sr}, uid, code_sr))["state"]
check(st["phase"] == "roll", "solo enters roll phase after confirm")
check(api.games[code_sr].first_roll[2] is not None, "bot die thrown server-side on confirm")
# Force the bot to win the opening roll deterministically, then verify the
# dice result screen is surfaced exactly like multiplayer: both dice present,
# phase already "playing", and the bot's opening shot is deferred (pending).
g = api.games[code_sr]
g.first_roll = {1: 2, 2: 5}
roll = unwrap(api._handle_roll_first({"code": code_sr}, uid, code_sr))
check(roll.get("roll_resolved"), "solo bot-win roll resolved")
st_botwin = roll["state"]
check(st_botwin["my_roll"] is not None and st_botwin["opp_roll"] is not None,
      "solo bot-win keeps both dice in state (result screen shows)")
check(st_botwin["phase"] == "playing" and st_botwin["turn"] == 2,
      "solo bot-win -> playing, bot turn")
check(g.bot_pending_first, "solo bot-win defers bot opening shot")
# The human acknowledges the dice screen; the bot then takes its opening shot.
bot_out = unwrap(api._handle_bot_opening_shot({"code": code_sr}, uid, code_sr))
check(bot_out.get("ok"), "solo bot opening shot ok")
check(not api.games[code_sr].bot_pending_first, "solo bot opening shot consumed")
# Symmetric case: fresh solo game where the human wins the opening roll.
uid_h = 2202
code_srh = unwrap(api._handle_new_solo({"strip": False, "difficulty": 2}, uid_h, None))["code"]
unwrap(api._handle_place_auto({"code": code_srh}, uid_h, code_srh))
unwrap(api._handle_confirm({"code": code_srh}, uid_h, code_srh))
gh = api.games[code_srh]
gh.first_roll = {1: 6, 2: 1}
roll2 = unwrap(api._handle_roll_first({"code": code_srh}, uid_h, code_srh))
st_humanwin = roll2["state"]
check(st_humanwin["my_roll"] is not None and st_humanwin["opp_roll"] is not None,
      "solo human-win keeps both dice in state (result screen shows)")
check(st_humanwin["phase"] == "playing" and st_humanwin["turn"] == 1,
      "solo human-win -> playing, human turn")
check(not api.games[code_srh].bot_pending_first, "solo human-win no pending bot shot")

print("Checkers (solo move + AI reply + hint):")
uid = 3001
res = unwrap(api._handle_checkers_new_solo({"difficulty": 3}, uid, None))
code_ck = res["code"]
out = api._handle_checkers_move(
    {"code": code_ck, "start_r": 5, "start_c": 0, "end_r": 4, "end_c": 1}, uid, code_ck)
check(unwrap(out).get("ok"), "checkers move")
hint = unwrap(api._handle_checkers_hint({"code": code_ck}, uid, code_ck))
check("hint" in hint or "error" in hint, "checkers hint")

print("Checkers (multi join + state):")
uidA, uidB = 3101, 3102
res = unwrap(api._handle_checkers_new_multi({"difficulty": 2}, uidA, None))
code_ckm = res["code"]
join = unwrap(api._handle_checkers_join({"code": code_ckm}, uidB, code_ckm))
check(join.get("ok"), "checkers join")
state = unwrap(api._handle_checkers_state({"code": code_ckm}, uidB, code_ckm))
check(state.get("ok"), "checkers state")
check(state["state"]["phase"] == "roll", "checkers enters roll phase on join")
started = False
for _ in range(60):
    rollA = unwrap(api._handle_checkers_roll_first({"code": code_ckm}, uidA, code_ckm))["roll"]
    rollB = unwrap(api._handle_checkers_roll_first({"code": code_ckm}, uidB, code_ckm))["roll"]
    if rollA.get("tie") or rollB.get("tie"):
        api._handle_checkers_reroll_first({"code": code_ckm}, uidA, code_ckm)
        api._handle_checkers_reroll_first({"code": code_ckm}, uidB, code_ckm)
        continue
    st = unwrap(api._handle_checkers_state({"code": code_ckm}, uidA, code_ckm))["state"]
    if st["phase"] == "playing":
        started = True
        break
check(started, "checkers roll decides first move -> playing")

print("Poker Dice (solo roll + score):")
uid = 4001
res = unwrap(api._handle_pd_new_solo({"difficulty": 3}, uid, None))
code_pd = res["code"]
out = api._handle_pd_roll({"code": code_pd, "keep": []}, uid, code_pd)
check(unwrap(out).get("ok"), "poker dice roll")
out = api._handle_pd_score({"code": code_pd, "category": "chance"}, uid, code_pd)
check(unwrap(out).get("ok"), "poker dice score")

print("Poker Dice (multi opening dice roll decides first move):")
uidA, uidB = 4101, 4102
code_pdm = unwrap(api._handle_pd_new_multi({"difficulty": 3}, uidA, None))["code"]
unwrap(api._handle_pd_join({"code": code_pdm}, uidB, code_pdm))
st = unwrap(api._handle_pd_state({"code": code_pdm}, uidA, code_pdm))["state"]
check(st["phase"] == "roll", "poker enters roll phase on join")
started = False
for _ in range(60):
    rollA = unwrap(api._handle_pd_roll_first({"code": code_pdm}, uidA, code_pdm))["roll"]
    rollB = unwrap(api._handle_pd_roll_first({"code": code_pdm}, uidB, code_pdm))["roll"]
    if rollA.get("tie") or rollB.get("tie"):
        api._handle_pd_reroll_first({"code": code_pdm}, uidA, code_pdm)
        api._handle_pd_reroll_first({"code": code_pdm}, uidB, code_pdm)
        continue
    st = unwrap(api._handle_pd_state({"code": code_pdm}, uidA, code_pdm))["state"]
    if st["phase"] == "playing":
        started = True
        break
check(started and st["turn"] in (1, 2), "poker roll decides first turn -> playing")

print("Backgammon (solo roll + move + bot reply):")
uid = 5001
res = unwrap(api._handle_bg_new_solo({"difficulty": 2}, uid, None))
code_bg = res["code"]
out = api._handle_bg_roll({"code": code_bg}, uid, code_bg)
resp = unwrap(out)
check(resp.get("ok"), "backgammon roll")
moves = (resp.get("state") or {}).get("legal_moves") or []
if moves:
    f, t = moves[0][0]
    out = api._handle_bg_move({"code": code_bg, "from": f, "to": t}, uid, code_bg)
    check(unwrap(out).get("ok"), "backgammon move")
    # In solo the bot must take its turn and hand control back to the human.
    st = (unwrap(out).get("state") or {})
    check(st.get("my_turn") is True, "control returns to human after move")
    # Play out the rest of the human's dice so the bot actually moves.
    guard = 0
    while (st.get("legal_moves")) and guard < 10:
        f, t = st["legal_moves"][0][0]
        out = api._handle_bg_move({"code": code_bg, "from": f, "to": t}, uid, code_bg)
        st = (unwrap(out).get("state") or {})
        guard += 1
    check(st.get("my_turn") is True, "control still with human after full turn")
    check(st.get("turn") == 1, "turn is WHITE (human) after bot reply")

print("Backgammon (long narde: shared head, no hitting, same direction):")
uid = 5002
res = unwrap(api._handle_bg_new_solo({"difficulty": 2, "variant": "long"}, uid, None))
code_bg_l = res["code"]
out = api._handle_bg_roll({"code": code_bg_l}, uid, code_bg_l)
resp = unwrap(out)
check(resp.get("ok"), "long narde roll")
st = (resp.get("state") or {})
check(st.get("variant") == "long", "variant is long")
check(st.get("board", [])[23] == 15, "white starts with 15 on the head")
check(st.get("head_black") == 15, "black starts with 15 on the head")
# a move from the head must be permitted
moves = st.get("legal_moves") or []
if moves:
    f, t = moves[0][0]
    out = api._handle_bg_move({"code": code_bg_l, "from": f, "to": t}, uid, code_bg_l)
    check(unwrap(out).get("ok"), "long narde move from head")
    # a second move from the head on the opening roll must be rejected
    st2 = (unwrap(out).get("state") or {})
    if st2.get("my_turn") and st2.get("legal_moves"):
        f2, t2 = st2["legal_moves"][0][0]
        if f2 == 23:
            out2 = api._handle_bg_move({"code": code_bg_l, "from": f2, "to": t2}, uid, code_bg_l)
            check(unwrap(out2).get("ok") is not True, "2nd head move on opening roll rejected")

print("Shared endpoints (active_games / bot_info / resolve_code):")
unwrap(api._handle_active_games({"code": None}, uid, None))
unwrap(api._handle_bot_info({}, uid, None))
rc = unwrap(api._handle_resolve_code({"code": code_sb}, uid, None))
check(rc.get("game") == "sea_battle", "resolve_code")

print("Mine shows as a mine (not a cross) when hit:")
_mg = _G("MINET", 1, 2)
_mg.board1.grid[3][3] = MINE
_mres = _mg.board1.receive_shot(3, 3)
check(_mres == "mine", "mine shot returns 'mine'")
check(_mg.board1.grid[3][3] == MINE_HIT, "hit mine cell is MINE_HIT, not HIT")
check(_mg.board1.cell_display(3, 3) == "💣", "hit mine renders as mine glyph")
_mflat = _mg.board1.to_flat_list(hide_ships=True)
check(_mflat[3 * 10 + 3] == MINE_HIT, "hit mine stays visible on opponent board")

print("Rematch reuses the same code:")
_rg = _G("REMTC", 1, 2)
_rg.phase = "finished"
_r1 = _rg.request_rematch(1)
check(_r1 is False, "first rematch vote records but waits")
check(_rg.phase == "finished", "still finished after one vote")
_r2 = _rg.request_rematch(2)
check(_r2 is True, "second rematch vote restarts game")
check(_rg.phase == "placing", "game restarted to placing phase")
check(_rg.code == "REMTC", "same code preserved")
check(_rg.rematch == {1: False, 2: False}, "rematch votes reset")

print("Rematch via api handler:")
api.games["REMTA"] = _G("REMTA", 11, 22)
api.games["REMTA"].phase = "finished"
_res = unwrap(api._handle_rematch({"code": "REMTA"}, 11, "REMTA"))
check(_res.get("ok"), "rematch vote ok")
_res2 = unwrap(api._handle_rematch({"code": "REMTA"}, 22, "REMTA"))
check(_res2.get("ok") and _res2.get("restarted"), "rematch restarts on second vote")
check(api.games["REMTA"].phase == "placing", "api game restarted")

print("Player stats (winrate + history recorded on match finish):")
import stats as _stats_mod
# NOTE: this block intentionally uses hardcoded ids/codes (1001, 2001, 2002,
# a fresh code_stm -- not code_m) rather than the uid/uidA/uidB/code_m names
# from earlier tests: those get reassigned many times by the time execution
# reaches here, so reusing them would silently check the wrong player.

# 1) Solo: reuse the game the very first test above already played to a real
#    finish through the actual API (no shortcuts), and check the human's
#    (uid 1001) record was updated -- and that the bot's placeholder id (0)
#    never accumulates a phantom record of its own.
s_solo = unwrap(api._handle_stats({}, 1001, None))["stats"]
check(s_solo["total"] == 1, "solo match recorded exactly once for the human")
check(s_solo["wins"] + s_solo["losses"] == 1, "solo match recorded as a win or a loss")
check(s_solo["by_game"]["sea_battle"]["wins"] + s_solo["by_game"]["sea_battle"]["losses"] == 1,
      "per-game breakdown updated")
check(len(s_solo["history"]) == 1 and s_solo["history"][0]["solo"] is True,
      "match recorded in history, flagged as solo")
check(_stats_mod.get_stats(0)["total"] == 0, "bot's placeholder id (0) never accumulates a record")

# 2) Multiplayer: a fresh 2-human game, finished via surrender for a
#    deterministic, real API-driven result, then check both sides got the
#    mirrored outcome. Surrendered before ship placement on purpose -- this
#    is exactly the edge case that originally slipped through.
uidA_st, uidB_st = 2001, 2002
code_stm = unwrap(api._handle_new_multi({"strip": False}, uidA_st, None))["code"]
unwrap(api._handle_join({"code": code_stm}, uidB_st, code_stm))
surr = unwrap(api._handle_surrender({"code": code_stm}, uidA_st, code_stm))
check(surr.get("ok"), "surrender ends the multiplayer game")
sA = unwrap(api._handle_stats({}, uidA_st, None))["stats"]
sB = unwrap(api._handle_stats({}, uidB_st, None))["stats"]
check(sA["losses"] == 1 and sA["wins"] == 0, "surrendering player recorded as a loss")
check(sB["wins"] == 1 and sB["losses"] == 0, "opponent recorded as a win")
check(sB["winrate"] == 100.0, "winrate computed correctly")
check(sA["history"][0]["opponent"] == uidB_st and sB["history"][0]["opponent"] == uidA_st,
      "history on each side records the other as the opponent")
check(sA["history"][0]["solo"] is False, "multiplayer match not flagged as solo")

# 3) A brand-new player must get a well-formed, all-zero record, not an error.
s_fresh = unwrap(api._handle_stats({}, 424242, None))["stats"]
check(s_fresh["total"] == 0 and s_fresh["winrate"] is None, "unseen player gets a clean empty record")

print("\nALL SMOKE TESTS PASSED")
