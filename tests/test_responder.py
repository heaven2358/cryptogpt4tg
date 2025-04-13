import unittest
import asyncio
from tgbot.responder import generate_reply

class TestResponder(unittest.TestCase):

    def test_generate_buy_reply_en(self):
        reply = asyncio.run(generate_reply("buy_intent", "btc", "fiat", "Sure", is_chinese=False))
        self.assertIn("Buy with fiat on Binance", reply)

    def test_generate_buy_reply_cn(self):
        reply = asyncio.run(generate_reply("buy_intent", "eth", "web3", "好的", is_chinese=True))
        self.assertIn("使用 Web3 钱包在 PancakeSwap", reply)

if __name__ == '__main__':
    unittest.main()