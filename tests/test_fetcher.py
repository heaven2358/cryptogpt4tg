import unittest
from tgbot.fetcher import fetch_price

class TestFetcher(unittest.TestCase):

    def test_fetch_price_en(self):
        result = fetch_price("btc", is_chinese=False)
        self.assertIn("The median price of", result)
        self.assertIn("USD", result)

    def test_fetch_price_cn(self):
        result = fetch_price("eth", is_chinese=True)
        self.assertIn("的中位价格是", result)
        self.assertIn("美元", result)

if __name__ == '__main__':
    unittest.main()