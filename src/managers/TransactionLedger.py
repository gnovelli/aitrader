from models.Transaction import Transaction


class TransactionLedger:
    def __init__(self, initial_cash_balance=0):
        self.transactions = []
        self.cash_balance = initial_cash_balance  # Imposta il bilancio cash iniziale
        self.crypto_balance = {}  # Un dizionario per tenere traccia delle diverse crypto

    def add_transaction(self, transaction):
        if isinstance(transaction, Transaction):
            self.transactions.append(transaction)

            # Aggiorna il bilancio cash
            if transaction.order_type in ["BUY", "LIMIT_BUY"]:
                self.cash_balance -= (transaction.price * transaction.quantity + transaction.fee)
                self.crypto_balance[transaction.symbol] = self.crypto_balance.get(transaction.symbol,
                                                                                  0) + transaction.quantity
            elif transaction.order_type in ["SELL", "LIMIT_SELL"]:
                self.cash_balance += (transaction.price * transaction.quantity - transaction.fee)
                self.crypto_balance[transaction.symbol] = self.crypto_balance.get(transaction.symbol,
                                                                                  0) - transaction.quantity

        else:
            raise ValueError("The provided object is not an instance of the Transaction class.")

    def get_all_transactions(self):
        return self.transactions

    def get_transaction_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                return transaction
        return None

    def __str__(self):
        return "\n".join([str(transaction) for transaction in self.transactions])

    def get_cash_balance(self):
        return self.cash_balance

    def get_crypto_balance(self, symbol=None):
        if symbol:
            return self.crypto_balance.get(symbol, 0)
        return self.crypto_balance

if __name__ == "__main__":
    # Inizializzazione del ledger con un bilancio cash di 10.000
    ledger = TransactionLedger(initial_cash_balance=1000000)

    # Transazione 1: Acquisto di 0.5 BTC a 50000 ciascuno
    transaction1 = Transaction(transaction_id="T001", symbol="BTCUSDT", order_type="BUY", price=50000, quantity=0.5,
                               timestamp="2023-08-26 10:00:00", status="FILLED", fee=10, platform="Binance")
    ledger.add_transaction(transaction1)
    print("Dopo la transazione 1:")
    print(f"Cash Balance: {ledger.get_cash_balance()}")
    print(f"Crypto Balance (BTC): {ledger.get_crypto_balance('BTCUSDT')}\n")

    # Transazione 2: Acquisto di 2 ETH a 3000 ciascuno
    transaction2 = Transaction(transaction_id="T002", symbol="ETHUSDT", order_type="BUY", price=3000, quantity=2,
                               timestamp="2023-08-26 11:00:00", status="FILLED", fee=5, platform="Binance")
    ledger.add_transaction(transaction2)
    print("Dopo la transazione 2:")
    print(f"Cash Balance: {ledger.get_cash_balance()}")
    print(f"Crypto Balance (ETH): {ledger.get_crypto_balance('ETHUSDT')}\n")

    # Transazione 3: Vendita di 0.2 BTC a 52000 ciascuno
    transaction3 = Transaction(transaction_id="T003", symbol="BTCUSDT", order_type="SELL", price=52000, quantity=0.2,
                               timestamp="2023-08-26 12:00:00", status="FILLED", fee=8, platform="Binance")
    ledger.add_transaction(transaction3)
    print("Dopo la transazione 3:")
    print(f"Cash Balance: {ledger.get_cash_balance()}")
    print(f"Crypto Balance (BTC): {ledger.get_crypto_balance('BTCUSDT')}\n")

