#!/usr/bin/env python3
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import config
from bot import (
    start, newgame, join, leave, cancel,
    handle_callback
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    app = Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newgame", newgame))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("leave", leave))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
