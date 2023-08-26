class Transaction:

    def __init__(self, transaction_id, symbol, order_type, price, quantity, timestamp, status, fee, platform, additional_info=None):
        """
        Initialize a new transaction.

        :param transaction_id: Unique ID of the transaction
        :param symbol: Trading pair symbol (e.g., BTCUSDT)
        :param order_type: Type of order (e.g., LIMIT, MARKET)
        :param price: Price at which the transaction was executed
        :param quantity: Amount of assets traded
        :param timestamp: Order timestamp
        :param status: Order status (e.g., FILLED, CANCELED)
        :param fee: Fee paid for the transaction
        :param platform: The trading platform where the transaction took place (e.g., Binance, Coinbase)
        :param additional_info: Additional information or notes about the transaction (optional)
        """
        self.transaction_id = transaction_id
        self.symbol = symbol
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp
        self.status = status
        self.fee = fee
        self.platform = platform
        self.additional_info = additional_info

    def __str__(self):
        return f"Transaction {self.transaction_id} on {self.platform} - {self.symbol} - {self.order_type} - {self.price} - {self.quantity} - {self.timestamp} - {self.status} - {self.fee}"

    def details(self):
        """
        Returns a detailed representation of the transaction.
        """
        return f"""
        Transaction ID: {self.transaction_id}
        Platform: {self.platform}
        Symbol: {self.symbol}
        Order Type: {self.order_type}
        Price: {self.price}
        Quantity: {self.quantity}
        Timestamp: {self.timestamp}
        Status: {self.status}
        Fee: {self.fee}
        Notes: {self.additional_info}
        """
