import unittest
import os
from tgbot import config

class TestConfig(unittest.TestCase):

    def test_telegram_token_exists(self):
        self.assertTrue(config.TELEGRAM_BOT_TOKEN)

    def test_openai_key_exists(self):
        self.assertTrue(config.OPENAI_API_KEY)

if __name__ == '__main__':
    unittest.main()