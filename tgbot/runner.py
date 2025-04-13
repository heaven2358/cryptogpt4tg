import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from tgbot.config import TELEGRAM_BOT_TOKEN
from tgbot.core import handle_message, handle_input_message

import asyncio

def run_telegram_bot():
    """
    Run the Telegram bot.

    This function creates a Telegram bot using the TELEGRAM_BOT_TOKEN
    and adds a single message handler to respond to messages that
    are not commands. The bot is then started with run_polling().

    :return: None
    """
    logging.info("🤖 Telegram Crypto Bot is running...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

def run_input_loop():
    """
    Run the input loop for console input.

    This function runs an infinite loop that waits for the user to input
    text. The text is then passed to handle_input_message() to be analyzed
    and responded to. If the user hits Ctrl-C, the loop is interrupted and
    the function exits.

    :return: None
    """
    logging.info("💬 Listening for console input...")
    while True:
        try:
            user_input = input("You: ")
            asyncio.run(handle_input_message(user_input))
        except KeyboardInterrupt:
            logging.info("Console input interrupted.")
            break