import unittest
from models.Transaction import Transaction

class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.data = {
            'transaction_id': '12345',
            'symbol': 'BTCUSDT',
            'order_type': 'LIMIT',
            'price': '50000.00',
            'quantity': '1',
            'timestamp': '1629876543',
            'status': 'FILLED',
            'fee': '0.001',
            'platform': 'Binance',
            'additional_info': 'Test transaction'
        }
        self.transaction = Transaction(
            transaction_id=self.data['transaction_id'],
            symbol=self.data['symbol'],
            order_type=self.data['order_type'],
            price=self.data['price'],
            quantity=self.data['quantity'],
            timestamp=self.data['timestamp'],
            status=self.data['status'],
            fee=self.data['fee'],
            platform=self.data['platform'],
            additional_info=self.data['additional_info']
        )

    def test_initialization(self):
        self.assertEqual(self.transaction.transaction_id, '12345')
        self.assertEqual(self.transaction.symbol, 'BTCUSDT')
        self.assertEqual(self.transaction.order_type, 'LIMIT')
        self.assertEqual(self.transaction.price, '50000.00')
        self.assertEqual(self.transaction.quantity, '1')
        self.assertEqual(self.transaction.timestamp, '1629876543')
        self.assertEqual(self.transaction.status, 'FILLED')
        self.assertEqual(self.transaction.fee, '0.001')
        self.assertEqual(self.transaction.platform, 'Binance')
        self.assertEqual(self.transaction.additional_info, 'Test transaction')

    def test_str_representation(self):
        expected_str = "Transaction 12345 on Binance - BTCUSDT - LIMIT - 50000.00 - 1 - 1629876543 - FILLED - 0.001"
        self.assertEqual(str(self.transaction), expected_str)

    def test_details(self):
        expected_details = """
        Transaction ID: 12345
        Platform: Binance
        Symbol: BTCUSDT
        Order Type: LIMIT
        Price: 50000.00
        Quantity: 1
        Timestamp: 1629876543
        Status: FILLED
        Fee: 0.001
        Notes: Test transaction
        """
        self.assertEqual(self.transaction.details().strip(), expected_details.strip())

if __name__ == '__main__':
    unittest.main()
