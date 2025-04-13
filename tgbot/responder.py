import json, logging, openai
from tgbot.config import OPENAI_API_KEY, user_contexts
from tgbot.fetcher import fetch_price

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

async def analyze_with_context(user_input: str, username: str, user_id: int) -> dict:
    """
    Analyze the given user input with the context-aware AI model.

    If the user asks for investment advice, add "sensitive": true.
    Reply in Chinese if user uses Chinese, else English.
    Classify message intent:

    - "price_query", "buy_intent", or "none"

    If intent is buy_intent, also give:
    - "buy_method": fiat / web3 / both

    If message includes sensitive info (wallet, seed, card, etc), add "sensitive": true
    If unrelated to crypto and user mentioned bot, give polite reply.
    Recognize if we should answer with chinese or english: is_chinese = true/false
    Don't reply price on you own, we have api to fetch price

    Return JSON:
    {"intent": "...", "coin": "...", "buy_method": "...", "sensitive": true/false, "is_chinese": true/false, "reply": "..."}
    """
    user_context = user_contexts[user_id]
    user_context.append({"role": "user", "content": f"@{username}: {user_input}"})

    prompt = [
        {"role": "system", "content": """
You are a crypto-savvy human who helps people get real-time prices and buying options for cryptocurrencies.
Important rules:
- NEVER say you're an AI, assistant, or bot.
- NEVER say "I can't provide price", because real-time prices are fetched for you.
- If user asks for investment advice, add "sensitive": true.
- Reply in Chinese if user uses Chinese, else English.
- Classify message intent:
    - "price_query", "buy_intent", or "none"
- If intent is buy_intent, also give:
    - "buy_method": fiat / web3 / both
- If message includes sensitive info (wallet, seed, card, etc), add "sensitive": true
- If unrelated to crypto and user mentioned bot, give polite reply.
- Recognize if we should answer with chinese or english: is_chinese = true/false
- Don't reply price on you own, we have api to fetch price

Return JSON:
{"intent": "...", "coin": "...", "buy_method": "...", "sensitive": true/false, "is_chinese": true/false, "reply": "..."}
"""}
    ] + list(user_context)

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=prompt,
        )
        result = response.choices[0].message.content
        parsed = json.loads(result)
        return parsed
    except Exception as e:
        logging.error(f"GPT error: {e}")
        return {"intent": "none", "coin": "", "reply": "", "sensitive": False, "is_chinese": False}

async def generate_reply(intent, coin, buy_method, reply, is_chinese=False, include_footer=False):
    """
    Generate a reply based on the given intent, coin, and buy method.

    - If intent is "price_query", append the current price of the coin to the reply.
    - If intent is "buy_intent", append the available purchase methods to the reply.
    - If include_footer is True, append a footer to the reply with a link to the personal assistant.

    :param intent: The intent of the message, can be "price_query", "buy_intent", or "none"
    :param coin: The name of the cryptocurrency
    :param buy_method: The preferred purchase method, can be "fiat", "web3", or "both"
    :param reply: The original reply to append to
    :param is_chinese: Whether the reply should be in Chinese, defaults to False
    :param include_footer: Whether to include a footer with a link to the personal assistant, defaults to False
    :return: The generated reply
    """
    if intent == "price_query" and coin:
        reply += f"\n\n📊 {fetch_price(coin, is_chinese)}"

    if intent == "buy_intent" and coin:
        reply += "\n\n" + ("以下是可用的购买方式：" if is_chinese else "Here are some ways to buy:")
        symbol = coin.upper()
        lower = coin.lower()

        if buy_method == "fiat":
            reply += f"\n🟢 {'使用法币在 Binance 购买' if is_chinese else 'Buy with fiat on Binance'}: [Binance](https://www.binance.com/en/crypto/buy/USD/{symbol})"
            reply += f"\n💳 {'使用法币在 MoonPay 购买' if is_chinese else 'Buy with fiat on MoonPay'}: [MoonPay](https://www.moonpay.com/buy/{lower})"
        elif buy_method == "web3":
            reply += f"\n🌀 {'使用 Web3 钱包在 PancakeSwap 兑换' if is_chinese else 'Swap on PancakeSwap via Web3'}: [PancakeSwap](https://pancakeswap.finance/swap?inputCurrency=0xdAC17F...&outputCurrency={symbol})"
            reply += f"\n🔗 {'使用 Web3 钱包在 1inch 兑换' if is_chinese else 'Swap on 1inch via Web3'}: [1inch](https://app.1inch.io/#/56/advanced/swap/USDT/{symbol})"
        else:
            reply += (
                f"\n🟢 {'使用法币在 Binance 购买' if is_chinese else 'Buy with fiat on Binance'}: [Binance](https://www.binance.com/en/crypto/buy/USD/{symbol})"
                f"\n🌀 {'使用 Web3 钱包在 PancakeSwap 兑换' if is_chinese else 'Swap on PancakeSwap via Web3'}: [PancakeSwap](https://pancakeswap.finance/swap?inputCurrency=0xdAC17F...&outputCurrency={symbol})"
                f"\n💳 {'使用法币在 MoonPay 购买' if is_chinese else 'Buy with fiat on MoonPay'}: [MoonPay](https://www.moonpay.com/buy/{lower})"
                f"\n🔗 {'使用 Web3 钱包在 1inch 兑换' if is_chinese else 'Swap on 1inch via Web3'}: [1inch](https://app.1inch.io/#/56/advanced/swap/USDT/{symbol})"
            )

    if include_footer:
        footer = (
            "如需更多操作指导，或提问涉及隐私信息，推荐使用 CryptoGPT 私人助理进行一对一解答: https://cryptogpt-test.apro.com/"
            if is_chinese else
            "For more guidance or private questions, please use CryptoGPT personal assistant: https://cryptogpt-test.apro.com/"
        )
        reply += f"\n\n{footer}"

    return reply