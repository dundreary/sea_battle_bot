import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN не задан! Добавь переменную окружения BOT_TOKEN на Render")

WEBAPP_URL = os.getenv("WEBAPP_URL", "")
