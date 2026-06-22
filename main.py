#!/usr/bin/env python3
import os
import json
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import BotCommand, MenuButtonWebApp, WebAppInfo
from telegram.ext import Application, CommandHandler
import config
from bot import start
from api import handle_api

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.getenv("PORT", 8080))
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._serve_file("index.html", "text/html; charset=utf-8")
        elif self.path.startswith("/static/"):
            self._serve_file(self.path[1:], "text/html; charset=utf-8")
        elif self.path == "/health" or self.path == "/":
            self._json({"status": "ok"})
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
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, data, code=200):
        text = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(text)))
        self.end_headers()
        self.wfile.write(text)

    def log_message(self, fmt, *args):
        logger.info("HTTP %s", args[-1] if args else "")

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), MainHandler)
    logger.info("HTTP server on port %s", PORT)
    server.serve_forever()

def main():
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    async def setup(app):
        base = config.WEBAPP_URL or os.getenv("RENDER_EXTERNAL_URL", "")
        cmds = [BotCommand("start", "🏠 Открыть меню")]
        try:
            await app.bot.set_my_commands(cmds)
            if base:
                btn = MenuButtonWebApp(text="🎮 Морской бой", web_app=WebAppInfo(url=base))
                await app.bot.set_chat_menu_button(menu_button=btn)
            logger.info("✅ Menu + commands set")
        except Exception as e:
            logger.warning("Menu setup skipped: %s", e)

    app = Application.builder().token(config.BOT_TOKEN).post_init(setup).build()

    app.add_handler(CommandHandler("start", start))

    logger.info("Bot + Web App started!")
    app.run_polling()

if __name__ == "__main__":
    main()
