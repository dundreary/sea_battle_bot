import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
import config

logger = logging.getLogger(__name__)

L10N = {
    'ru': {'text': '⚓ <b>Морской бой</b>\n\nНажми кнопку ниже, чтобы открыть игру 🎯', 'btn': '🎮 Открыть игру'},
    'uk': {'text': '⚓ <b>Морський бій</b>\n\nНатисни кнопку нижче, щоб відкрити гру 🎯', 'btn': '🎮 Відкрити гру'},
    'en': {'text': '⚓ <b>Sea Battle</b>\n\nTap the button below to open the game 🎯', 'btn': '🎮 Open Game'},
}

def _(user, key):
    try:
        lc = (user.language_code or 'ru')[:2]
        if lc in ('uk', 'ua'):
            lc = 'uk'
        elif lc.startswith('en'):
            lc = 'en'
        else:
            lc = 'ru'
    except Exception:
        lc = 'ru'
    return L10N.get(lc, L10N['ru']).get(key, key)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base = config.WEBAPP_URL or os.getenv("RENDER_EXTERNAL_URL", "")
    user = update.effective_user
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(_(user, 'btn'), web_app=WebAppInfo(url=base or "https://sea-battle-bot.onrender.com"))
    ]])
    await update.message.reply_text(_(user, 'text'), reply_markup=kb, parse_mode="HTML")

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data.strip().upper()
    user = update.effective_user
    lc = (user.language_code or 'ru')[:2]
    if lc in ('uk', 'ua'):
        share = f"🎮 Морський бій\n\nКод гри: <b>{data}</b>\n\nВідкрийте гру та натисніть «🔗 Ввести код»"
    elif lc.startswith('en'):
        share = f"🎮 Sea Battle\n\nGame code: <b>{data}</b>\n\nOpen the game and tap «🔗 Enter Code»"
    else:
        share = f"🎮 Морской бой\n\nКод игры: <b>{data}</b>\n\nОткройте игру и нажмите «🔗 Ввести код»"
    await update.message.reply_text(share, parse_mode="HTML")
