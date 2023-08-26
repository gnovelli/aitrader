import unittest
from models.Ticker import Ticker

class TestTicker(unittest.TestCase):

    def setUp(self):
        self.data = {
            'e': '24hrTicker',
            'E': 1692863706598,
            's': 'BTCUSDT',
            'p': '419.44000000',
            'P': '1.610',
            'w': '26343.27048841',
            'x': '26050.01000000',
            'c': '26469.45000000',
            'Q': '0.00878000',
            'b': '26469.45000000',
            'B': '12.90727000',
            'a': '26469.46000000',
            'A': '1.83432000',
            'o': '26050.01000000',
            'h': '26819.27000000',
            'l': '25812.82000000',
            'v': '41796.56431000',
            'q': '1101058199.10452790',
            'O': 1692777306598,
            'C': 1692863706598,
            'F': 3197587545,
            'L': 3198235645,
            'n': 648101
        }
        self.ticker = Ticker(self.data)

    def test_initialization(self):
        self.assertEqual(self.ticker.event_type, '24hrTicker')
        self.assertEqual(self.ticker.event_time, 1692863706598)
        self.assertEqual(self.ticker.symbol, 'BTCUSDT')
        # ... (test other attributes similarly)

    # You can add more test methods to test other functionalities of the Ticker class.

if __name__ == '__main__':
    unittest.main()
