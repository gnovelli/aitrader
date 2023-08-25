import unittest
from unittest.mock import patch, MagicMock
from src.monitors.BinanceMonitor import BinanceMonitor

class TestBinanceMonitor(unittest.TestCase):

    @patch('src.monitors.BinanceMonitor.BinanceMonitor.websocket.WebSocketApp')
    @patch('src.managers.DatabaseManager.DatabaseManager.insert_data')
    def test_on_message(self, mock_insert_data, mock_websocket):
        # Creazione di mock data
        mock_message = json.dumps({"e": "some_event", "data": "some_data"})

        crypto_list = ["ethbtc"]
        db = MagicMock()  # Mocking del DatabaseManager
        monitor = BinanceMonitor(crypto_list, db)

        # Chiamata della funzione
        monitor.on_message(None, mock_message)

        # Verifica che insert_data sia stato chiamato
        mock_insert_data.assert_called_once_with({"e": "some_event", "data": "some_data"})

    @patch('src.monitors.BinanceMonitor.BinanceMonitor.websocket.WebSocketApp')
    @patch('src.managers.DatabaseManager.DatabaseManager.insert_data')
    def test_generate_streams(self, mock_insert_data, mock_websocket):
        crypto_list = ["ethbtc", "btcusdt"]
        db = MagicMock()
        monitor = BinanceMonitor(crypto_list, db)

        expected_streams = ["ethbtc@ticker", "btcusdt@ticker"]
        self.assertListEqual(monitor.generate_streams(crypto_list), expected_streams)

    # Altri test possono essere scritti per on_error, on_close, ecc.

if __name__ == "__main__":
    unittest.main()
