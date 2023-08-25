import unittest
from src.managers.PortfolioManager import PortfolioManager

class TestPortfolioManager(unittest.TestCase):

    def setUp(self):
        # Questo metodo viene chiamato prima di ogni metodo di test
        self.portfolio = PortfolioManager()

    def test_add_crypto(self):
        self.portfolio.add_crypto("BTC", 1)
        self.assertEqual(self.portfolio.crypto_portfolio["BTC"], 1)
        self.portfolio.add_crypto("BTC", 1)
        self.assertEqual(self.portfolio.crypto_portfolio["BTC"], 2)

    def test_remove_crypto(self):
        self.portfolio.add_crypto("BTC", 2)
        self.portfolio.remove_crypto("BTC", 1)
        self.assertEqual(self.portfolio.crypto_portfolio["BTC"], 1)

        with self.assertRaises(ValueError):
            self.portfolio.remove_crypto("BTC", 2)

    def test_add_remove_cash(self):
        self.portfolio.add_cash(1000.0)
        self.assertEqual(self.portfolio.cash, 1000.0)

        self.portfolio.remove_cash(500.0)
        self.assertEqual(self.portfolio.cash, 500.0)

        with self.assertRaises(ValueError):
            self.portfolio.remove_cash(600.0)

    def test_get_balance(self):
        self.portfolio.add_crypto("BTC", 1)
        self.portfolio.add_cash(1000.0)
        expected_balance = {'BTC': 1, 'CASH': 1000.0}
        self.assertEqual(self.portfolio.get_balance(), expected_balance)

    def test_get_portfolio_value(self):
        self.portfolio.add_crypto("BTC", 1)
        self.portfolio.add_cash(1000.0)
        prices = {"BTC": 50000.0}
        self.assertEqual(self.portfolio.get_portfolio_value(prices), 51000.0)

        # Se non viene fornito un prezzo per una cripto nel portafoglio, il valore non dovrebbe cambiare
        del prices["BTC"]
        self.assertEqual(self.portfolio.get_portfolio_value(prices), 1000.0)


if __name__ == '__main__':
    unittest.main()
