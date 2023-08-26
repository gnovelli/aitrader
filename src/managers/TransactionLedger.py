from models.Transaction import Transaction
from managers.PortfolioManager import PortfolioManager

class TransactionLedger:
    def __init__(self, initial_cash_balance=0):
        self.transactions = []
        self.cash_balance = initial_cash_balance
        self.total_fees = 0
        self.total_spent_on_crypto = 0
        self.crypto_balance = {}

    def add_transaction(self, transaction):
        if isinstance(transaction, Transaction):
            self.transactions.append(transaction)

            # Aggiorna il bilancio cash, le commissioni e l'importo speso in crypto
            if transaction.order_type in ["BUY", "LIMIT_BUY"]:
                self.cash_balance -= (transaction.price * transaction.quantity + transaction.fee)
                self.total_fees += transaction.fee
                self.total_spent_on_crypto += (transaction.price * transaction.quantity)
                self.crypto_balance[transaction.symbol] = self.crypto_balance.get(transaction.symbol,
                                                                                  0) + transaction.quantity
            elif transaction.order_type in ["SELL", "LIMIT_SELL"]:
                self.cash_balance += (transaction.price * transaction.quantity - transaction.fee)
                self.total_fees += transaction.fee
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

    def get_cash_details(self):
        return {
            "current_cash_balance": self.cash_balance,
            "total_fees_spent": self.total_fees,
            "total_spent_on_crypto": self.total_spent_on_crypto,
            "crypto_balances": self.crypto_balance
        }

    def translate_ledger_to_portfolio(self, portfolio_manager):
        for transaction in self.get_all_transactions():
            if transaction.order_type in ["BUY", "LIMIT_BUY"]:
                portfolio_manager.remove_cash(transaction.price * transaction.quantity + transaction.fee)
                portfolio_manager.add_crypto(transaction.symbol, transaction.quantity)
                portfolio_manager.add_fee(transaction.fee)
                portfolio_manager.add_spent_on_crypto(transaction.price * transaction.quantity)
            elif transaction.order_type in ["SELL", "LIMIT_SELL"]:
                portfolio_manager.add_cash(transaction.price * transaction.quantity - transaction.fee)
                portfolio_manager.remove_crypto(transaction.symbol, transaction.quantity)
                portfolio_manager.add_fee(transaction.fee)
        return portfolio_manager

if __name__ == "__main__":
    # Inizializzazione del ledger con un bilancio cash di 10.000
    ledger = TransactionLedger(initial_cash_balance=1000000)

    # Transazione 1: Acquisto di 0.5 BTC a 50000 ciascuno
    transaction1 = Transaction(transaction_id="T001", symbol="BTCUSDT", order_type="BUY", price=50000, quantity=0.5,
                               timestamp="2023-08-26 10:00:00", status="FILLED", fee=10, platform="Binance")
    ledger.add_transaction(transaction1)
    print(f"Dopo la transazione 1: {transaction1}")
    details = ledger.get_cash_details()
    print(f"Current Cash Balance: {details['current_cash_balance']}")
    print(f"Total Fees Spent: {details['total_fees_spent']}")
    print(f"Total Spent on Crypto: {details['total_spent_on_crypto']}")
    for symbol, quantity in details['crypto_balances'].items():
        print(f"Quantity of {symbol}: {quantity}")
    portfolio_manager = PortfolioManager(initial_cash=1000000)
    portfolio_manager=ledger.translate_ledger_to_portfolio(portfolio_manager)
    portfolio_manager.print_portfolio()

    # Transazione 2: Acquisto di 2 ETH a 3000 ciascuno
    transaction2 = Transaction(transaction_id="T002", symbol="ETHUSDT", order_type="BUY", price=3000, quantity=2,
                               timestamp="2023-08-26 11:00:00", status="FILLED", fee=5, platform="Binance")
    ledger.add_transaction(transaction2)
    print(f"Dopo la transazione 2: {transaction2}")
    details = ledger.get_cash_details()
    print(f"Current Cash Balance: {details['current_cash_balance']}")
    print(f"Total Fees Spent: {details['total_fees_spent']}")
    print(f"Total Spent on Crypto: {details['total_spent_on_crypto']}")
    for symbol, quantity in details['crypto_balances'].items():
        print(f"Quantity of {symbol}: {quantity}")
    portfolio_manager = PortfolioManager(initial_cash=1000000)
    portfolio_manager=ledger.translate_ledger_to_portfolio(portfolio_manager)
    portfolio_manager.print_portfolio()

    # Transazione 3: Vendita di 0.2 BTC a 52000 ciascuno
    transaction3 = Transaction(transaction_id="T003", symbol="BTCUSDT", order_type="SELL", price=52000, quantity=0.2,
                               timestamp="2023-08-26 12:00:00", status="FILLED", fee=8, platform="Binance")
    ledger.add_transaction(transaction3)
    print(f"Dopo la transazione 3: {transaction3}")
    details = ledger.get_cash_details()
    print(f"Current Cash Balance: {details['current_cash_balance']}")
    print(f"Total Fees Spent: {details['total_fees_spent']}")
    print(f"Total Spent on Crypto: {details['total_spent_on_crypto']}")
    for symbol, quantity in details['crypto_balances'].items():
        print(f"Quantity of {symbol}: {quantity}")
    portfolio_manager = PortfolioManager(initial_cash=1000000)
    portfolio_manager=ledger.translate_ledger_to_portfolio(portfolio_manager)
    portfolio_manager.print_portfolio()


