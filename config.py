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

# Browser mode is OFF by default (secure). A request with no signed
# init_data must NOT be trusted for any uid -- leaving the default on lets any
# caller act as any uid on every mutating route (full identity spoofing).
# Set to "1" ONLY as an explicit opt-in to enable the browser-share path;
# unset/"0" in production. See api._authenticate().
ALLOW_BROWSER_AUTH = os.getenv("ALLOW_BROWSER_AUTH", "0") == "1"
