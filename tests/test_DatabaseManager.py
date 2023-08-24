import unittest
import sqlite3
import pandas as pd
from src.managers.DatabaseManager import DatabaseManager  # Assuming the given code is saved in a file named "your_module.py"


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager()

        # Sample data for testing
        self.sample_data = {
            'e': '24hrTicker', 'E': 1692863706598, 's': 'BTCUSDT', 'p': '419.44000000', 'P': '1.610',
            'w': '26343.27048841', 'x': '26050.01000000', 'c': '26469.45000000', 'Q': '0.00878000',
            'b': '26469.45000000', 'B': '12.90727000', 'a': '26469.46000000', 'A': '1.83432000',
            'o': '26050.01000000', 'h': '26819.27000000', 'l': '25812.82000000', 'v': '41796.56431000',
            'q': '1101058199.10452790', 'O': 1692777306598, 'C': 1692863706598, 'F': 3197587545,
            'L': 3198235645, 'n': 648101
        }

    def test_insert_data(self):
        # Insert sample data
        self.db.insert_data(self.sample_data)

        # Fetch data
        fetched_data = self.db.fetch_data(symbol="BTCUSDT")
        self.assertEqual(len(fetched_data), 1)  # Only one record should be present

    def test_fetch_data(self):
        self.db.insert_data(self.sample_data)
        records = self.db.fetch_data(symbol="BTCUSDT")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][3], 'BTCUSDT')  # Checking symbol

    def test_records_to_dataframe(self):
        self.db.insert_data(self.sample_data)
        records = self.db.fetch_data(symbol="BTCUSDT")
        df = self.db.records_to_dataframe(records)

        # Check if it returns a pandas DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Checking if the dataframe contains our inserted record
        self.assertEqual(df.iloc[0]["symbol"], "BTCUSDT")

    def test_fetch_dataframe(self):
        self.db.insert_data(self.sample_data)
        df = self.db.fetch_dataframe(symbol="BTCUSDT")

        # Check if it returns a pandas DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Checking if the dataframe contains our inserted record
        self.assertEqual(df.iloc[0]["symbol"], "BTCUSDT")

    def tearDown(self):
        self.db.close()


if __name__ == "__main__":
    unittest.main()
