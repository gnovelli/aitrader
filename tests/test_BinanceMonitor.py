import unittest
from unittest.mock import MagicMock
from src.monitors.BinanceMonitor import BinanceMonitor
import json

class TestBinanceMonitor(unittest.TestCase):

    def setUp(self):
        # Creiamo un mock per DatabaseManager per evitare interazioni reali con il database
        self.mock_db_manager = MagicMock()
        self.crypto_list = ["ethbtc", "btcusdt", "xrpbtc"]
        self.monitor = BinanceMonitor(self.crypto_list, self.mock_db_manager)

    def test_generate_streams(self):
        expected_streams = ["ethbtc@ticker", "btcusdt@ticker", "xrpbtc@ticker"]
        self.assertEqual(self.monitor.generate_streams(self.crypto_list), expected_streams)

    def test_record_data_with_event(self):
        mock_ws = MagicMock()
        message = json.dumps({'e': 'event', 'other_key': 'value'})
        self.monitor.record_data(mock_ws, message)
        self.mock_db_manager.insert_data.assert_called_once_with(json.loads(message))

    def test_record_data_without_event(self):
        mock_ws = MagicMock()
        message = json.dumps({'other_key': 'value'})
        self.monitor.record_data(mock_ws, message)
        self.mock_db_manager.insert_data.assert_not_called()

    # Altri test possono essere aggiunti per on_message, on_error, on_close, on_open, ecc.
    # Tuttavia, questi metodi potrebbero richiedere l'uso di mock per simulare il comportamento di WebSocket e altre interazioni esterne.

if __name__ == "__main__":
    unittest.main()
