import datetime
import time
from managers.TransactionLedger import TransactionLedger
from managers.PortfolioManager import PortfolioManager
from models.Transaction import Transaction

class PaperTrading:
    def __init__(self, platform="binance.com", buy_commission_rate=0.001, sell_commission_rate=0.001,
                 initial_cash_balance=10000):
        self.ledger = TransactionLedger(initial_cash_balance=initial_cash_balance)
        self.platform = platform
        self.buy_commission_rate = buy_commission_rate
        self.sell_commission_rate = sell_commission_rate

    def _create_transaction(self, symbol, order_type, price, quantity, additional_info=None):
        # Generiamo un ID univoco per la transazione
        transaction_id = f"{symbol}_{order_type}_{self.platform}_{int(time.time())}"
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = "FILLED"  # Per semplificare, supponiamo che ogni ordine venga eseguito immediatamente

        # Applichiamo le commissioni in base al tipo di ordine
        if order_type in ["BUY", "LIMIT_BUY"]:
            fee = price * quantity * self.buy_commission_rate
        elif order_type in ["SELL", "LIMIT_SELL"]:
            fee = price * quantity * self.sell_commission_rate

        # Creiamo una nuova transazione
        transaction = Transaction(transaction_id, symbol, order_type, price, quantity, timestamp, status, fee,
                                  self.platform, additional_info)

        # Aggiungiamo la transazione al registro
        self.ledger.add_transaction(transaction)

    def buy(self, symbol, price, quantity, additional_info=None):
        self._create_transaction(symbol, "BUY", price, quantity, additional_info)

    def sell(self, symbol, price, quantity, additional_info=None):
        self._create_transaction(symbol, "SELL", price, quantity, additional_info)

    def limit_buy(self, symbol, price, quantity, additional_info=None):
        self._create_transaction(symbol, "LIMIT_BUY", price, quantity, additional_info)

    def limit_sell(self, symbol, price, quantity, additional_info=None):
        self._create_transaction(symbol, "LIMIT_SELL", price, quantity, additional_info)

    def print_portfolio(self):
        self.ledger.translate_ledger_to_portfolio().print_portfolio()

    def get_transaction_history(self):
        return self.ledger.get_all_transactions()

    def get_cash_balance(self):
        return self.ledger.get_cash_balance()

    def get_crypto_balance(self, symbol=None):
        return self.ledger.get_crypto_balance(symbol)

if __name__ == "__main__":
    # Istanza di PaperTrading con un bilancio iniziale di 10000
    paper_trading = PaperTrading(initial_cash_balance=1000000)

    # Eseguiamo alcune operazioni di trading
    paper_trading.buy(symbol="BTCUSDT", price=50000, quantity=0.1)  # Acquisto di 0.1 BTC a 50000 ciascuno
    paper_trading.sell(symbol="BTCUSDT", price=55000, quantity=0.05)  # Vendita di 0.05 BTC a 55000 ciascuno
    paper_trading.limit_buy(symbol="ETHUSDT", price=2500, quantity=2)  # Acquisto limite di 2 ETH a 2500 ciascuno
    paper_trading.limit_sell(symbol="ETHUSDT", price=2700, quantity=1)  # Vendita limite di 1 ETH a 2700 ciascuno

    # Visualizziamo l'andamento del trading
    print("Storico delle transazioni:")
    for transaction in paper_trading.get_transaction_history():
        print(transaction)

    print("\nDettagli del portafoglio:")
    paper_trading.print_portfolio()

    print("\nBilancio in contanti:")
    print(paper_trading.get_cash_balance())

    print("\nBilancio in cripto:")
    print(paper_trading.get_crypto_balance())
