import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
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
        if lc.startswith('uk'): lc = 'uk'
        elif lc.startswith('en'): lc = 'en'
        else: lc = 'ru'
    except:
        lc = 'ru'
    return L10N.get(lc, L10N['ru']).get(key, key)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base = config.WEBAPP_URL or os.getenv("RENDER_EXTERNAL_URL", "")
    user = update.effective_user
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(_(user, 'btn'), web_app=WebAppInfo(url=base or "https://sea-battle-bot.onrender.com"))
    ]])
    await update.message.reply_text(_(user, 'text'), reply_markup=kb, parse_mode="HTML")
