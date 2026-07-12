import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
import config

logger = logging.getLogger(__name__)

L10N = {
    'ru': {'text': '🎮 <b>Добро пожаловать!</b>\n\nДоступны игры:\n⚓ Морской бой\n♟ Шашки\n🎲 Покер в кости\n♜ Нарды\n\nНажми кнопку ниже, чтобы открыть 🎯', 'btn': '🎮 Открыть игры'},
    'uk': {'text': '🎮 <b>Ласкаво просимо!</b>\n\nДоступні ігри:\n⚓ Морський бій\n♟ Шашки\n🎲 Покер у кості\n♜ Нарди\n\nНатисни кнопку нижче, щоб відкрити 🎯', 'btn': '🎮 Відкрити ігри'},
    'en': {'text': '🎮 <b>Welcome!</b>\n\nAvailable games:\n⚓ Sea Battle\n♟ Checkers\n🎲 Poker Dice\n♜ Backgammon\n\nTap the button below to open 🎯', 'btn': '🎮 Open Games'},
}

def _lang_code(user):
    try:
        lc = (user.language_code or 'ru')[:2]
        return 'uk' if lc in ('uk', 'ua') else 'en' if lc.startswith('en') else 'ru'
    except Exception:
        return 'ru'

def _(user, key):
    lc = _lang_code(user)
    return L10N.get(lc, L10N['ru']).get(key, key)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base = config.WEBAPP_URL or os.getenv("RENDER_EXTERNAL_URL", "")
    url = base or "https://sea-battle-bot.onrender.com"
    if "?" in url:
        url += "&v=2"
    else:
        url += "?v=2"
    user = update.effective_user
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(_(user, 'btn'), web_app=WebAppInfo(url=url))
    ]])
    await update.message.reply_text(_(user, 'text'), reply_markup=kb, parse_mode="HTML")

SHARE_L10N = {
    'ru': '- Код игры: <b>{}</b>\n\nОткройте игру и нажмите «🔗 Ввести код»',
    'uk': '- Код гри: <b>{}</b>\n\nВідкрийте гру та натисніть «🔗 Ввести код»',
    'en': '- Game code: <b>{}</b>\n\nOpen the game and tap «🔗 Enter Code»',
}

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data.strip().upper()
    user = update.effective_user
    lc = _lang_code(user)
    share = SHARE_L10N.get(lc, SHARE_L10N['ru']).format(data)
    await update.message.reply_text(share, parse_mode="HTML")
