from telegram import Update
from telegram.ext import ContextTypes
from tgbot.config import user_contexts
from tgbot.responder import generate_reply, analyze_with_context


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for incoming Telegram messages.

    Analyze the message text with the context-aware AI model, and generate a
    reply based on the intent and other extracted information.

    If the message text contains a mention of the bot and is determined to be
    a price query or buy intent, a reply containing the price information and/or
    purchase options will be sent back to the user. If the message contains
    sensitive information (e.g. wallet addresses, seed phrases, card numbers),
    a reply with a warning will be sent.

    The bot's username is required for the mention detection to work correctly.
    """
    user = update.message.from_user
    user_id = user.id
    username = user.username or user.first_name
    user_lang = user.language_code or "en"
    user_text = update.message.text

    mentioned = any(
        e.type == "mention" and context.bot.username.lower() in user_text.lower()
        for e in (update.message.entities or [])
    )
    if not mentioned:
        return

    result = await analyze_with_context(user_text, username, user_id)
    intent = result.get("intent")
    # may cause AttributeError: 'NoneType' object has no attribute 'lower'
    coin = result.get("coin", "")
    if coin:
        coin = coin.lower()
    buy_method = result.get("buy_method", "both")
    sensitive = result.get("sensitive", False)
    is_chinese = result.get("is_chinese", user_lang.startswith("zh"))
    reply = result.get("reply", "")

    user_contexts[user_id].append({"role": "assistant", "content": reply})
    include_footer = intent in ["buy_intent"] or sensitive

    if intent in ["price_query", "buy_intent"]:
        reply = await generate_reply(intent, coin, buy_method, reply, is_chinese, include_footer=include_footer)
    elif mentioned and sensitive:
        reply = await generate_reply("buy_intent", coin, "both", reply or "", is_chinese, include_footer=include_footer)

    await update.message.reply_text(reply, parse_mode="Markdown")

async def handle_input_message(message: str, user_id=1):
    """
    Handle console input messages for testing purposes.

    This function analyzes the provided message using a context-aware AI model
    to determine the intent, coin, buy method, and language preference.
    It then generates a reply based on these parameters and prints it.

    :param message: The input message to be analyzed.
    :param user_id: The ID of the user, defaults to 1.
    """

    result = await analyze_with_context(message, "tester", user_id)
    reply = await generate_reply(result["intent"], result["coin"], result.get("buy_method", "both"),
                                 result["reply"], result.get("is_chinese", False),
                                 include_footer=result["intent"] == "buy_intent" or result.get("sensitive", False))
    print(reply)
