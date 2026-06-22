import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import config
from game import Game, SHIPS, SIZE, validate_ship_placement, auto_place_ships

logger = logging.getLogger(__name__)

games = {}
player_games = {}

def placement_grid_keyboard(game_code, board, ship_len, selected_cells):
    kb = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            v = board.grid[r][c]
            if (r, c) in selected_cells:
                text = "❌"
            elif v == 1:
                text = "🟩"
            elif v == 4:
                text = "✖"
            else:
                text = "⬜"
            cb = f"plc_{r}_{c}_{game_code}"
            row.append(InlineKeyboardButton(text, callback_data=cb))
        kb.append(row)
    ship_len = ship_len if ship_len else 0
    remaining = ship_len - len(selected_cells) if ship_len else 0
    status = f"🚢 Осталось: {remaining} клеток"
    if remaining == 0 and ship_len:
        kb.append([InlineKeyboardButton(f"✅ Подтвердить ({ship_len})", callback_data=f"cfm_{game_code}")])
    kb.append([InlineKeyboardButton("🔀 Расставить автоматически", callback_data=f"auto_{game_code}")])
    kb.append([InlineKeyboardButton("❌ Отменить последнюю", callback_data=f"undo_{game_code}")])
    return InlineKeyboardMarkup(kb), status

def shoot_grid_keyboard(game_code, opp_board):
    kb = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            v = opp_board.grid[r][c]
            if v == 0:
                text = "⬜"
            elif v == 2:
                text = "❌"
            elif v == 3:
                text = "⭕"
            elif v == 4:
                text = "✖"
            elif v == 5:
                text = "·"
            else:
                text = "⬜"
            cb = f"sht_{r}_{c}_{game_code}"
            row.append(InlineKeyboardButton(text, callback_data=cb))
        kb.append(row)
    return InlineKeyboardMarkup(kb)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base = config.WEBAPP_URL or os.getenv("RENDER_EXTERNAL_URL", "")
    text = "⚓ <b>Морской бой</b>\n\nКоманды:\n/solo — игра против бота\n/newgame — с другом\n/join XXX — присоединиться"
    kb = None
    if base and base.startswith("http"):
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("🎮 Открыть игру", web_app=WebAppInfo(url=base))
        ]])
        text += "\n\nИли нажми кнопку ниже, чтобы открыть <b>мини-приложение</b> 🎯"
    await update.message.reply_text(text, reply_markup=kb, parse_mode="HTML")

async def newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in player_games:
        await update.message.reply_text("Вы уже в игре. Используйте /leave чтобы выйти.")
        return
    code = Game.generate_code()
    while code in games:
        code = Game.generate_code()
    game = Game(code, uid)
    games[code] = game
    player_games[uid] = code
    await update.message.reply_text(
        f"🎮 Игра создана!\n\n"
        f"Код для приглашения соперника: <b>{code}</b>\n\n"
        f"Отправьте сопернику: /join {code}\n"
        f"Ожидаем соперника...",
        parse_mode="HTML"
    )

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in player_games:
        await update.message.reply_text("Вы уже в игре. Используйте /leave чтобы выйти.")
        return
    args = context.args
    if not args:
        await update.message.reply_text("Использование: /join <код>")
        return
    code = args[0].upper()
    if code not in games:
        await update.message.reply_text("Игра с таким кодом не найдена.")
        return
    game = games[code]
    if game.player2_id is not None:
        await update.message.reply_text("В этой игре уже два игрока.")
        return
    game.player2_id = uid
    player_games[uid] = code
    game.phase = "placing"
    await update.message.reply_text(
        f"✅ Вы присоединились к игре <b>{code}</b>!\n"
        "Начинаем расстановку кораблей!",
        parse_mode="HTML"
    )
    for pid in (game.player1_id, game.player2_id):
        pnum = game.player_num(pid)
        board = game.board_for(pid)
        await send_placement_prompt(update.get_bot(), pid, game, pnum, board)

async def solo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in player_games:
        await update.message.reply_text("Вы уже в игре. Используйте /leave чтобы выйти.")
        return
    code = Game.generate_code()
    while code in games:
        code = Game.generate_code()
    game = Game(code, uid, solo=True)
    game.player2_id = 0
    games[code] = game
    player_games[uid] = code
    game.phase = "placing"
    auto_place_ships(game.board2)
    game.placing[2]["ship_idx"] = len(SHIPS)
    game.ready[2] = True
    await update.message.reply_text(
        "🤖 <b>Режим игры с ботом</b>\n\n"
        "Расставь свои корабли, и начинаем!",
        parse_mode="HTML"
    )
    await send_placement_prompt(context.bot, uid, game, 1, game.board1)

async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in player_games:
        await update.message.reply_text("Вы не в игре.")
        return
    code = player_games.pop(uid)
    game = games.get(code)
    if game:
        other_id = game.player2_id if uid == game.player1_id else game.player1_id
        if other_id and other_id in player_games:
            player_games.pop(other_id, None)
        games.pop(code, None)
    await update.message.reply_text("Вы вышли из игры.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    game_code = player_games.get(uid)
    if not game_code:
        await update.message.reply_text("Нечего отменять.")
        return
    game = games.get(game_code)
    if not game or game.phase == "playing":
        await update.message.reply_text("Нечего отменять.")
        return
    pnum = game.player_num(uid)
    game.placing[pnum]["cells"] = []
    board = game.board_for(uid)
    await send_placement_prompt(context.bot, uid, game, pnum, board)

async def send_placement_prompt(bot, uid, game, pnum, board):
    ship_len = game.needs_ship_of_length(pnum)
    if ship_len is None:
        return
    selected = game.placing[pnum]["cells"]
    kb, status = placement_grid_keyboard(game.code, board, ship_len, selected)
    placed = len(board.ships)
    total = len(SHIPS)
    text = (
        f"<b>Расстановка кораблей</b>\n"
        f"Размещено: {placed}/{total}\n"
        f"Текущий корабль: <b>{ship_len} палубы</b>\n"
        f"{status}\n\n"
        f"Нажимайте на клетки доски, чтобы разместить корабль."
    )
    await bot.send_message(uid, text, reply_markup=kb, parse_mode="HTML")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = update.effective_user.id

    if data == "newgame":
        await newgame(update, context)
        return
    if data == "join_prompt":
        await query.edit_message_text(
            "Отправьте команду:\n/join <код>\n\n"
            "Например: /join ABCDEF"
        )
        return

    if data.startswith("plc_"):
        parts = data.split("_")
        r, c, game_code = int(parts[1]), int(parts[2]), parts[3]
        await handle_placement_click(query, uid, game_code, r, c)
        return
    if data.startswith("cfm_"):
        game_code = data.split("_", 1)[1]
        await handle_confirm_placement(query, uid, game_code, context.bot)
        return
    if data.startswith("auto_"):
        game_code = data.split("_", 1)[1]
        await handle_auto_place(query, uid, game_code, context.bot)
        return
    if data.startswith("undo_"):
        game_code = data.split("_", 1)[1]
        await handle_undo(query, uid, game_code)
        return
    if data.startswith("sht_"):
        parts = data.split("_")
        r, c, game_code = int(parts[1]), int(parts[2]), parts[3]
        await handle_shot(query, uid, game_code, r, c, context.bot)
        return

async def handle_placement_click(query, uid, game_code, r, c):
    game = games.get(game_code)
    if not game:
        await query.edit_message_text("Игра не найдена.")
        return
    pnum = game.player_num(uid)
    if game.phase != "placing":
        await query.answer("Сейчас не время для расстановки.", show_alert=True)
        return
    if game.ready[pnum]:
        await query.answer("Вы уже расставили все корабли.", show_alert=True)
        return
    board = game.board_for(uid)
    if board.grid[r][c] != 0:
        await query.answer("Эта клетка уже занята.", show_alert=True)
        return
    ship_len = game.needs_ship_of_length(pnum)
    if ship_len is None:
        return
    selected = game.placing[pnum]["cells"]
    if (r, c) in selected:
        await query.answer("Уже выбрано.", show_alert=True)
        return
    if len(selected) >= ship_len:
        await query.answer(f"Корабль уже {ship_len} клеток. Нажмите 'Подтвердить'.", show_alert=True)
        return
    selected.append((r, c))
    if len(selected) == ship_len:
        valid, err = validate_ship_placement(selected)
        if not valid:
            selected.pop()
            await query.answer(err, show_alert=True)
            return
    kb, status = placement_grid_keyboard(game_code, board, ship_len, selected)
    placed = len(board.ships)
    total = len(SHIPS)
    text = (
        f"<b>Расстановка кораблей</b>\n"
        f"Размещено: {placed}/{total}\n"
        f"Текущий корабль: <b>{ship_len} палубы</b>\n"
        f"{status}\n\n"
        f"Нажимайте на клетки доски, чтобы разместить корабль."
    )
    await query.edit_message_text(text, reply_markup=kb, parse_mode="HTML")

async def handle_confirm_placement(query, uid, game_code, bot):
    game = games.get(game_code)
    if not game:
        await query.edit_message_text("Игра не найдена.")
        return
    pnum = game.player_num(uid)
    board = game.board_for(uid)
    ship_len = game.needs_ship_of_length(pnum)
    if ship_len is None:
        await query.answer("Все корабли уже расставлены.", show_alert=True)
        return
    selected = game.placing[pnum]["cells"]
    if len(selected) != ship_len:
        await query.answer(f"Нужно выбрать {ship_len} клеток.", show_alert=True)
        return
    valid, err = validate_ship_placement(selected)
    if not valid:
        await query.answer(err, show_alert=True)
        return
    if not board.can_place(selected):
        await query.answer("Нельзя разместить здесь (рядом другие корабли).", show_alert=True)
        return
    board.place_ship(selected)
    game.placing[pnum]["cells"] = []
    game.placing[pnum]["ship_idx"] += 1
    next_len = game.needs_ship_of_length(pnum)
    if next_len is None:
        game.ready[pnum] = True
        if game.ready[1] and game.ready[2]:
            game.phase = "playing"
            game.turn = 1
            try:
                await query.edit_message_text("✅ Все корабли расставлены! Игра начинается!")
                if game.solo:
                    logger.info("Starting solo game, sending turn prompt to %s", uid)
                    await notify_solo_turn(bot, game_code)
                else:
                    await notify_turn(bot, game_code)
            except Exception as e:
                logger.error("Error starting game: %s", e, exc_info=True)
                await bot.send_message(uid, f"⚠️ Ошибка: {e}")
        else:
            await query.edit_message_text("✅ Ваши корабли расставлены. Ожидайте соперника...")
    else:
        await send_placement_prompt(bot, uid, game, pnum, board)

async def handle_auto_place(query, uid, game_code, bot):
    game = games.get(game_code)
    if not game:
        await query.edit_message_text("Игра не найдена.")
        return
    pnum = game.player_num(uid)
    board = game.board_for(uid)
    auto_place_ships(board)
    game.placing[pnum]["cells"] = []
    game.placing[pnum]["ship_idx"] = len(SHIPS)
    game.ready[pnum] = True
    if game.ready[1] and game.ready[2]:
        game.phase = "playing"
        game.turn = 1
        try:
            await query.edit_message_text("✅ Все корабли расставлены! Игра начинается!")
            if game.solo:
                logger.info("Starting solo game (auto), sending turn prompt to %s", uid)
                await notify_solo_turn(bot, game_code)
            else:
                await notify_turn(bot, game_code)
        except Exception as e:
            logger.error("Error starting game: %s", e, exc_info=True)
            await bot.send_message(uid, f"⚠️ Ошибка: {e}")
    else:
        await query.edit_message_text("✅ Ваши корабли расставлены автоматически. Ожидайте соперника...")

async def handle_undo(query, uid, game_code):
    game = games.get(game_code)
    if not game:
        await query.edit_message_text("Игра не найдена.")
        return
    pnum = game.player_num(uid)
    selected = game.placing[pnum]["cells"]
    if selected:
        selected.pop()
        board = game.board_for(uid)
        ship_len = game.needs_ship_of_length(pnum)
        kb, status = placement_grid_keyboard(game_code, board, ship_len, selected)
        placed = len(board.ships)
        total = len(SHIPS)
        text = (
            f"<b>Расстановка кораблей</b>\n"
            f"Размещено: {placed}/{total}\n"
            f"Текущий корабль: <b>{ship_len} палубы</b>\n"
            f"{status}\n\n"
            f"Нажимайте на клетки доски, чтобы разместить корабль."
        )
        await query.edit_message_text(text, reply_markup=kb, parse_mode="HTML")
    else:
        await query.answer("Нечего отменять.", show_alert=True)

async def handle_shot(query, uid, game_code, r, c, bot):
    game = games.get(game_code)
    if not game:
        await query.edit_message_text("Игра не найдена.")
        return
    if game.current_player() != uid:
        await query.answer("Сейчас не ваш ход!", show_alert=True)
        return
    if not game.both_placed:
        await query.answer("Игра ещё не началась.", show_alert=True)
        return
    opp_board = game.opponent_board(uid)
    result = opp_board.receive_shot(r, c)
    if result == "repeat":
        await query.answer("Вы уже стреляли сюда!", show_alert=True)
        return
    own_board = game.board_for(uid)
    msg_parts = []
    if result == "hit":
        msg_parts.append("🔥 Попадание!")
    elif result == "sunk":
        msg_parts.append("💀 Корабль потоплен!")
    elif result == "miss":
        msg_parts.append("💨 Мимо!")

    action = " ".join(msg_parts)

    if opp_board.all_sunk():
        final = f"🚢 <b>ТВОИ КОРАБЛИ</b>\n<pre>{own_board.render_own()}</pre>\n🏆 <b>ВЫ ПОБЕДИЛИ!</b>"
        await query.edit_message_text(final, parse_mode="HTML")
        other_uid = game.opponent_id(uid)
        if not game.solo:
            await bot.send_message(
                other_uid,
                f"💔 <b>Вы проиграли!</b>\n<pre>{opp_board.render_own()}</pre>",
                parse_mode="HTML"
            )
        for pid in (game.player1_id, game.player2_id):
            player_games.pop(pid, None)
        games.pop(game_code, None)
        return

    if result == "miss":
        game.switch_turn()
        await query.edit_message_text(
            f"{action}\n🚢 <b>ТВОИ КОРАБЛИ</b>\n<pre>{own_board.render_own()}</pre>",
            parse_mode="HTML"
        )
        if game.solo:
            await handle_bot_turn(bot, game_code)
        else:
            await notify_turn(bot, game_code)
    else:
        kb = shoot_grid_keyboard(game_code, opp_board)
        await query.edit_message_text(
            f"{action}\n🚢 <b>ТВОИ КОРАБЛИ</b>\n<pre>{own_board.render_own()}</pre>\n\n🎯 Ещё выстрел!",
            reply_markup=kb,
            parse_mode="HTML"
        )

async def handle_bot_turn(bot, game_code):
    game = games.get(game_code)
    if not game or not game.both_placed:
        return
    uid = game.player1_id
    own = game.board_for(uid)
    opp = game.opponent_board(uid)

    r, c = game.bot_ai.choose_shot(own)
    if r is None:
        return

    result = own.receive_shot(r, c)
    game.bot_ai.register_shot(r, c, result, own)

    cell_name = f"{chr(ord('A') + c)}{r + 1}"
    if result == "hit":
        action = f"🔥 Попадание в {cell_name}!"
    elif result == "sunk":
        action = f"💀 Корабль на {cell_name} потоплен!"
    else:
        action = f"💨 Мимо — {cell_name}"

    if own.all_sunk():
        await bot.send_message(
            uid,
            f"💔 <b>ВЫ ПРОИГРАЛИ!</b> Бот потопил все ваши корабли.\n🚢 <b>ТВОИ КОРАБЛИ</b>\n<pre>{own.render_own()}</pre>",
            parse_mode="HTML"
        )
        player_games.pop(uid, None)
        games.pop(game_code, None)
        return

    if result == "miss":
        game.switch_turn()
        await bot.send_message(
            uid,
            f"🤖 {action}\n🚢 <b>ТВОИ КОРАБЛИ</b>\n<pre>{own.render_own()}</pre>\n⚓ <b>Твой ход!</b>",
            reply_markup=shoot_grid_keyboard(game_code, opp),
            parse_mode="HTML"
        )
    else:
        game.bot_ai.shots.add((r, c))
        await bot.send_message(
            uid,
            f"🤖 {action} 🎯 Бот стреляет ещё...",
            parse_mode="HTML"
        )
        await handle_bot_turn(bot, game_code)

async def notify_solo_turn(bot, game_code):
    game = games.get(game_code)
    if not game or not game.both_placed:
        return
    uid = game.player1_id
    own = game.board_for(uid)
    opp = game.opponent_board(uid)
    kb = shoot_grid_keyboard(game_code, opp)
    await bot.send_message(
        uid,
        f"🚢 <b>ТВОИ КОРАБЛИ</b>\n<pre>{own.render_own()}</pre>\n⚓ <b>Твой ход!</b>",
        reply_markup=kb,
        parse_mode="HTML"
    )

async def notify_turn(bot, game_code):
    game = games.get(game_code)
    if not game or not game.both_placed:
        return
    current_uid = game.current_player()
    other_uid = game.opponent_id(current_uid)
    own_board = game.board_for(current_uid)
    opp_board = game.opponent_board(current_uid)
    kb = shoot_grid_keyboard(game_code, opp_board)
    await bot.send_message(
        other_uid,
        "⏳ Ход соперника... Ожидайте.",
    )
    await bot.send_message(
        current_uid,
        f"🚢 <b>ТВОИ КОРАБЛИ</b>\n<pre>{own_board.render_own()}</pre>\n⚓ <b>Твой ход!</b>",
        reply_markup=kb,
        parse_mode="HTML"
    )
