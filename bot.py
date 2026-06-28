import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
import config

logger = logging.getLogger(__name__)

L10N = {
    'ru': {'text': '⚓ <b>Морской бой</b>\n\nНажми кнопку ниже, чтобы открыть игру 🎯', 'btn': '🎮 Открыть игру', 'share': '🎮 Морской бой\n\nКод игры: <b>{code}</b>\n\nОткройте игру и нажмите «🔗 Ввести код»'},
    'uk': {'text': '⚓ <b>Морський бій</b>\n\nНатисни кнопку нижче, щоб відкрити гру 🎯', 'btn': '🎮 Відкрити гру', 'share': '🎮 Морський бій\n\nКод гри: <b>{code}</b>\n\nВідкрийте гру та натисніть «🔗 Ввести код»'},
    'en': {'text': '⚓ <b>Sea Battle</b>\n\nTap the button below to open the game 🎯', 'btn': '🎮 Open Game', 'share': '🎮 Sea Battle\n\nGame code: <b>{code}</b>\n\nOpen the game and tap «🔗 Enter Code»'},
}

def _locale_code(user):
    lc = (user.language_code or 'ru')[:2] if user else 'ru'
    return 'uk' if lc.startswith('uk') else 'en' if lc.startswith('en') else 'ru'

def _(user, key):
    return L10N.get(_locale_code(user), L10N['ru']).get(key, '')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(_(user, 'btn'), web_app=WebAppInfo(url=config.WEBAPP_URL or "https://sea-battle-bot.onrender.com"))
    ]])
    await update.message.reply_text(_(user, 'text'), reply_markup=kb, parse_mode="HTML")

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data.strip().upper()
    user = update.effective_user
    share = L10N.get(_locale_code(user), L10N['ru']).get('share', '').format(code=data)
    await update.message.reply_text(share, parse_mode="HTML")
