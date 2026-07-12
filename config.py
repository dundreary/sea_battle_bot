import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN не задан! Добавь переменную окружения BOT_TOKEN на Render")

WEBAPP_URL = os.getenv("WEBAPP_URL") or os.getenv("RENDER_EXTERNAL_URL", "")

BOT_USERNAME = ""
BOT_ID = 0

# Off by default (secure). Set to "1" only for local testing outside a real
# Telegram client, where there's no signed init_data to verify -- see auth.py
# and api.py:_authenticate(). Must stay unset/"0" in production.
SKIP_TELEGRAM_AUTH = os.getenv("SKIP_TELEGRAM_AUTH", "0") == "1"

# A regular browser has no signed Telegram WebApp payload. Keep that mode
# available for sharing games outside Telegram; set to "0" to require Telegram
# authentication on every request.
ALLOW_BROWSER_AUTH = os.getenv("ALLOW_BROWSER_AUTH", "1") == "1"
