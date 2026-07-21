#!/usr/bin/env python3
import os
import json
import logging
import threading
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
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

# Changes on every process restart (i.e. every deploy) and stays fixed for as
# long as the process runs -- exactly the cache lifetime we want. index.html
# (always served fresh, see _serve_index) embeds this value in the URLs of
# its own JS/CSS, so a new deploy naturally busts old caches while a given
# deploy's assets can be cached hard by the browser instead of being
# re-downloaded on every single game open.
ASSET_VERSION = str(int(time.time()))

# JS/CSS modules whose content changes on every deploy. Requested with a
# ?v=<ASSET_VERSION> query string (see _serve_index), they are safe to cache
# hard -- that exact URL can never point at different content while this
# process is running. Requested without it (a stale cached index.html from
# before this feature existed, or a direct manual hit), they fall back to the
# old no-cache behaviour so nobody gets stuck on outdated game logic.
APP_MODULES = {"style.css", "common.js", "poker_dice.js", "checkers.js", "backgammon.js"}


class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path_only = self.path.split("?", 1)[0]
        if path_only == "/health":
            self._json({"status": "ok"})
        elif path_only == "/" or path_only == "/index.html":
            self._serve_index()
        elif path_only.startswith("/static/"):
            cache_busted = f"v={ASSET_VERSION}" in self.path
            self._serve_file(path_only[1:], None, cache_busted=cache_busted)
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        result = handle_api(self.path, body)
        self._json(result)

    def do_HEAD(self):
        # UptimeRobot (and most uptime monitors) probe with HEAD, not GET.
        # BaseHTTPRequestHandler returns 501 Not Implemented for any method
        # it doesn't know, so without this the monitor always sees "down"
        # even though GET /health works fine. Mirror do_GET routing but send
        # headers only (no body), as the HTTP spec requires for HEAD.
        path_only = self.path.split("?", 1)[0]
        if path_only == "/health":
            code, mime = 200, "application/json; charset=utf-8"
        elif path_only == "/" or path_only == "/index.html":
            code, mime = 200, "text/html; charset=utf-8"
        elif path_only.startswith("/static/"):
            code, mime = 200, "application/octet-stream"
        else:
            code, mime = 404, "application/json; charset=utf-8"
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _serve_index(self):
        # index.html itself must never be cached -- it's what points browsers
        # at the *current* versioned asset URLs below, so a stale copy would
        # keep sending people to a previous deploy's assets forever.
        path = os.path.join(STATIC_DIR, "index.html")
        if not os.path.isfile(path):
            self._json({"error": "not found"}, 404)
            return
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("__ASSET_VERSION__", ASSET_VERSION)
        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(data)

    def _serve_file(self, name, mime, cache_busted=False):
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
        base_name = os.path.basename(name)
        if base_name in APP_MODULES and cache_busted:
            # This exact ?v=<ASSET_VERSION> URL will never point at different
            # content while this process is running, so it's safe to cache
            # hard instead of re-downloading ~150KB of JS/CSS on every single
            # game open, which unconditional no-cache used to cost.
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        elif base_name in APP_MODULES:
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        else:
            self.send_header("Cache-Control", "public, max-age=604800, immutable")
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
    # ThreadingHTTPServer handles each request on its own thread (with
    # daemon_threads=True by default), instead of the old HTTPServer's
    # one-request-at-a-time behaviour where a single slow request (or an AI
    # move computation -- see api.py's UNLOCKED_* paths) froze the entire
    # app -- every game, every player -- for its whole duration.
    server = ThreadingHTTPServer(("0.0.0.0", PORT), MainHandler)
    logger.info("HTTP server on port %s", PORT)
    server.serve_forever()

def run_bot():
    async def setup(app):
        base = config.WEBAPP_URL or os.getenv("RENDER_EXTERNAL_URL", "")
        try:
            me = await app.bot.get_me()
            config.BOT_USERNAME = me.username
            config.BOT_ID = me.id
            logger.info(" Bot username: @%s", me.username)
        except Exception as e:
            logger.warning("Could not get bot info: %s", e)
        cmds = [
            BotCommand("start", " Открыть меню"),
        ]
        try:
            await app.bot.set_my_commands(cmds)
            if base:
                btn = MenuButtonWebApp(text=" Games", web_app=WebAppInfo(url=base))
                await app.bot.set_chat_menu_button(menu_button=btn)
            logger.info(" Menu + commands set")
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
