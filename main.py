#!/usr/bin/env python3
import os
import json
import logging
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import BotCommand, MenuButtonWebApp, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import config
from bot import start, web_app_data
from api import handle_api
from persist import load as load_state

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.getenv("PORT", 8080))
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._json({"status": "ok"})
        elif self.path == "/" or self.path == "/index.html":
            self._serve_file("index.html", "text/html; charset=utf-8")
        elif self.path.startswith("/static/"):
            self._serve_file(self.path[1:], None)
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        result = handle_api(self.path, body)
        self._json(result)

    def _serve_file(self, name, mime):
        path = os.path.join(STATIC_DIR, os.path.basename(name))
        if not os.path.isfile(path):
            self._json({"error": "not found"}, 404)
            return
        with open(path, "rb") as f:
            data = f.read()
        if mime is None:
            mime = self._guess_mime(path)
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(data)

    @staticmethod
    def _guess_mime(path):
        ext = os.path.splitext(path)[1].lower()
        return {
            ".svg": "image/svg+xml",
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".ico": "image/x-icon",
            ".json": "application/json",
        }.get(ext, "application/octet-stream")

    def _json(self, data, code=200):
        text = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(text)))
        self.end_headers()
        self.wfile.write(text)

    def log_message(self, fmt, *args):
        logger.info("HTTP %s", args[-1] if args else "")

def run_http():
    server = HTTPServer(("0.0.0.0", PORT), MainHandler)
    logger.info("HTTP server on port %s", PORT)
    server.serve_forever()

def run_bot():
    async def setup(app):
        base = config.WEBAPP_URL or os.getenv("RENDER_EXTERNAL_URL", "")
        try:
            me = await app.bot.get_me()
            config.BOT_USERNAME = me.username
            config.BOT_ID = me.id
            logger.info("✅ Bot username: @%s", me.username)
        except Exception as e:
            logger.warning("Could not get bot info: %s", e)
        cmds = [
            BotCommand("start", "🏠 Открыть меню"),
        ]
        try:
            await app.bot.set_my_commands(cmds)
            if base:
                btn = MenuButtonWebApp(text="🎮 Games", web_app=WebAppInfo(url=base))
                await app.bot.set_chat_menu_button(menu_button=btn)
            logger.info("✅ Menu + commands set")
        except Exception as e:
            logger.warning("Menu setup skipped: %s", e)

    app = Application.builder().token(config.BOT_TOKEN).post_init(setup).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    logger.info("Bot started!")
    app.run_polling()

def main():
    load_state()
    # Persist any in-memory state on exit so the last mutations are not lost
    # (the background persistence worker otherwise flushes on its own cadence).
    import atexit
    import persist
    atexit.register(persist.flush)

    # HTTP server in background (can run any thread)
    t = threading.Thread(target=run_http, daemon=True)
    t.start()

    # Bot MUST be on main thread (asyncio limitation)
    try:
        run_bot()
    except Exception as e:
        logger.error("Bot crashed: %s", e)
        # Keep HTTP alive even if bot dies
        while True:
            time.sleep(60)

if __name__ == "__main__":
    main()
