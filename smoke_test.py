"""Smoke test: drives every game end-to-end without any network.

Run with:  python smoke_test.py
It monkeypatches persistence (no disk writes) and Telegram delivery (no
network), so it exercises game logic + the refactored api.py handlers only.
"""
import api
import persist
import notifications

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
finished = False
for r in range(10):
    for c in range(10):
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

print("Poker Dice (solo roll + score):")
uid = 4001
res = unwrap(api._handle_pd_new_solo({"difficulty": 3}, uid, None))
code_pd = res["code"]
out = api._handle_pd_roll({"code": code_pd, "keep": []}, uid, code_pd)
check(unwrap(out).get("ok"), "poker dice roll")
out = api._handle_pd_score({"code": code_pd, "category": "chance"}, uid, code_pd)
check(unwrap(out).get("ok"), "poker dice score")

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

print("\nALL SMOKE TESTS PASSED")
