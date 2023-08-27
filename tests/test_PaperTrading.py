import unittest
from trading.PaperTrading import PaperTrading

class TestPaperTrading(unittest.TestCase):

    def setUp(self):
        self.paper_trading = PaperTrading(initial_cash_balance=10000)

    def test_buy(self):
        self.paper_trading.buy(symbol="BTCUSDT", price=50000, quantity=0.1)
        transactions = self.paper_trading.get_transaction_history()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].symbol, "BTCUSDT")
        self.assertEqual(transactions[0].order_type, "BUY")
        self.assertEqual(transactions[0].price, 50000)
        self.assertEqual(transactions[0].quantity, 0.1)

    def test_sell(self):
        self.paper_trading.sell(symbol="BTCUSDT", price=55000, quantity=0.05)
        transactions = self.paper_trading.get_transaction_history()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].symbol, "BTCUSDT")
        self.assertEqual(transactions[0].order_type, "SELL")
        self.assertEqual(transactions[0].price, 55000)
        self.assertEqual(transactions[0].quantity, 0.05)

    def test_limit_buy(self):
        self.paper_trading.limit_buy(symbol="ETHUSDT", price=2500, quantity=2)
        transactions = self.paper_trading.get_transaction_history()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].symbol, "ETHUSDT")
        self.assertEqual(transactions[0].order_type, "LIMIT_BUY")
        self.assertEqual(transactions[0].price, 2500)
        self.assertEqual(transactions[0].quantity, 2)

    def test_limit_sell(self):
        self.paper_trading.limit_sell(symbol="ETHUSDT", price=2700, quantity=1)
        transactions = self.paper_trading.get_transaction_history()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].symbol, "ETHUSDT")
        self.assertEqual(transactions[0].order_type, "LIMIT_SELL")
        self.assertEqual(transactions[0].price, 2700)
        self.assertEqual(transactions[0].quantity, 1)

    def test_cash_balance(self):
        self.paper_trading.buy(symbol="BTCUSDT", price=50000, quantity=0.1)
        self.assertEqual(self.paper_trading.get_cash_balance(), 10000 - (50000 * 0.1 + 5))  # 5 is the fee

    def test_crypto_balance(self):
        self.paper_trading.buy(symbol="BTCUSDT", price=50000, quantity=0.1)
        self.assertEqual(self.paper_trading.get_crypto_balance("BTCUSDT"), 0.1)

if __name__ == '__main__':
    unittest.main()
