import os
import json
import logging
import threading
import urllib.request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import config

logger = logging.getLogger(__name__)

user_chat_map = {}
user_chat_map_lock = threading.Lock()

L10N = {
    'ru': {'text': '⚓ <b>Морской бой</b>\n\nНажми кнопку ниже, чтобы открыть игру 🎯', 'btn': '🎮 Открыть игру'},
    'uk': {'text': '⚓ <b>Морський бій</b>\n\nНатисни кнопку нижче, щоб відкрити гру 🎯', 'btn': '🎮 Відкрити гру'},
    'en': {'text': '⚓ <b>Sea Battle</b>\n\nTap the button below to open the game 🎯', 'btn': '🎮 Open Game'},
}

def _(user, key):
    try:
        lc = (user.language_code or 'ru')[:2]
        if lc.startswith('uk'): lc = 'uk'
        elif lc.startswith('en'): lc = 'en'
        else: lc = 'ru'
    except:
        lc = 'ru'
    return L10N.get(lc, L10N['ru']).get(key, key)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base = config.WEBAPP_URL or os.getenv("RENDER_EXTERNAL_URL", "")
    user = update.effective_user
    if user.username:
        with user_chat_map_lock:
            user_chat_map[user.username.lower()] = update.effective_chat.id
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(_(user, 'btn'), web_app=WebAppInfo(url=base or "https://sea-battle-bot.onrender.com"))
    ]])
    await update.message.reply_text(_(user, 'text'), reply_markup=kb, parse_mode="HTML")

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data.strip().upper()
    user = update.effective_user
    if user.username:
        with user_chat_map_lock:
            user_chat_map[user.username.lower()] = update.effective_chat.id
    lc = (user.language_code or 'ru')[:2]
    if lc.startswith('uk'): share = f"🎮 Морський бій\n\nКод гри: <b>{data}</b>\n\nВідкрийте гру та натисніть «🔗 Ввести код»"
    elif lc.startswith('en'): share = f"🎮 Sea Battle\n\nGame code: <b>{data}</b>\n\nOpen the game and tap «🔗 Enter Code»"
    else: share = f"🎮 Морской бой\n\nКод игры: <b>{data}</b>\n\nОткройте игру и нажмите «🔗 Ввести код»"
    await update.message.reply_text(share, parse_mode="HTML")

async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /invite @username GAMECODE")
        return
    username = args[0].lstrip('@').lower()
    code = args[1].upper()
    with user_chat_map_lock:
        chat_id = user_chat_map.get(username)
    if not chat_id:
        await update.message.reply_text(f"User @{username} hasn't started the bot yet. Ask them to /start first.")
        return
    base_url = config.WEBAPP_URL or "https://sea-battle-bot.onrender.com"
    webapp_url = f"https://t.me/{config.BOT_USERNAME}/app?startapp={code}" if config.BOT_USERNAME else f"{base_url}?startapp={code}"
    kb = {"inline_keyboard": [[{"text": "🎮 Play", "web_app": {"url": webapp_url}}]]}
    payload = json.dumps({
        "chat_id": chat_id,
        "text": f"🎮 {update.effective_user.first_name} приглашает тебя сыграть!\n\nКод: <b>{code}</b>\n\nНажми «🎮 Play», чтобы открыть игру с этим кодом.",
        "parse_mode": "HTML",
        "reply_markup": kb,
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        r = urllib.request.urlopen(req, timeout=10)
        if r.status == 200:
            await update.message.reply_text("✅ Приглашение отправлено!")
        else:
            await update.message.reply_text("❌ Не удалось отправить приглашение.")
    except Exception as e:
        logger.error("Invite error: %s", e)
        await update.message.reply_text("❌ Ошибка отправки приглашения.")
