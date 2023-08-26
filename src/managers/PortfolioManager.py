class PortfolioManager:
    def __init__(self, initial_cash = 0):
        # Inizializza un dizionario vuoto per le crypto pairs. La chiave è la sigla della criptovaluta, e il valore è la quantità.
        self.crypto_portfolio = {}

        # Inizializza il contante a disposizione.
        self.cash = initial_cash
        # Aggiungi attributi per tracciare le commissioni e l'importo speso in criptovalute
        self.total_fees = 0
        self.total_spent_on_crypto = 0

    def add_crypto(self, symbol, amount):
        """
        Aggiunge o aggiorna la quantità di una specifica criptovaluta al portafoglio.

        :param symbol: Stringa che rappresenta la sigla della criptovaluta (es. "BTC", "ETH", ecc.).
        :param amount: Quantità di criptovaluta da aggiungere.
        """
        if symbol in self.crypto_portfolio:
            self.crypto_portfolio[symbol] += amount
        else:
            self.crypto_portfolio[symbol] = amount

    def remove_crypto(self, symbol, amount):
        """
        Rimuove una quantità specifica di una criptovaluta dal portafoglio.

        :param symbol: Stringa che rappresenta la sigla della criptovaluta.
        :param amount: Quantità di criptovaluta da rimuovere.
        """
        if symbol in self.crypto_portfolio:
            self.crypto_portfolio[symbol] -= amount
            if self.crypto_portfolio[symbol] < 0:
                raise ValueError(f"Quantità insufficiente di {symbol} nel portafoglio.")
        else:
            raise ValueError(f"{symbol} non presente nel portafoglio.")

    def add_fee(self, fee):
        """
        Aggiunge la commissione al totale delle commissioni spese.

        :param fee: Importo della commissione.
        """
        self.total_fees += fee

    def add_spent_on_crypto(self, amount):
        """
        Aggiunge l'importo speso in criptovalute al totale speso.

        :param amount: Importo speso.
        """
        self.total_spent_on_crypto += amount

    def add_cash(self, amount):
        """
        Aggiunge contante al portafoglio.

        :param amount: Quantità di contante da aggiungere.
        """
        self.cash += amount

    def remove_cash(self, amount):
        """
        Rimuove contante dal portafoglio.

        :param amount: Quantità di contante da rimuovere.
        """
        if self.cash >= amount:
            self.cash -= amount
        else:
            raise ValueError("Contante insufficiente nel portafoglio.")

    def get_balance(self):
        """
        Restituisce un riepilogo del saldo del portafoglio, includendo tutte le criptovalute e il contante disponibile.

        :return: Dizionario contenente le quantità di ogni criptovaluta e il contante disponibile.
        """
        balance = self.crypto_portfolio.copy()
        balance['CASH'] = self.cash
        return balance

    def get_portfolio_value(self, current_prices):
        """
        Calcola e restituisce il valore totale del portafoglio sulla base dei prezzi correnti.

        :param current_prices: Dizionario con le sigle delle criptovalute come chiavi e i loro prezzi correnti come valori.
        :return: Valore totale del portafoglio.
        """
        total_value = self.cash  # Inizia con il contante disponibile

        for symbol, amount in self.crypto_portfolio.items():
            if symbol in current_prices:
                total_value += amount * current_prices[symbol]
            else:
                print(f"Attenzione: Prezzo per {symbol} non disponibile.")

        return total_value

    def print_portfolio(self, current_prices=None):
        """
        Stampa un riepilogo del portafoglio, includendo il contante, la quantità di ogni criptovaluta e il loro valore,
        se vengono forniti i prezzi correnti.

        :param current_prices: (Opzionale) Dizionario con le sigle delle criptovalute come chiavi e i loro prezzi correnti come valori.
        """
        print("---- PORTAFOLIO RIEPILOGO ----")
        print(f"CASH: ${self.cash:.2f}")
        print(f"CASH SPENT ON FEEs: ${self.total_fees:.2f}")
        print(f"CASH SPENT ON CRYPTOs: ${self.total_spent_on_crypto:.2f}")

        crypto_total_value = 0.0

        for symbol, amount in self.crypto_portfolio.items():
            if current_prices and symbol in current_prices:
                value = amount * current_prices[symbol]
                crypto_total_value += value
                print(f"{symbol}: {amount} units | Valore: ${value:.2f}")
            else:
                print(f"{symbol}: {amount} units")

        if current_prices:
            print(f"Valore totale delle criptovalute: ${crypto_total_value:.2f}")
            print(f"Valore totale del portafoglio: ${crypto_total_value + self.cash:.2f}")
        print("-----------------------------")

if __name__ == "__main__":
    # Test della classe
    portfolio = PortfolioManager(initial_cash=1000000)
    portfolio.add_crypto("BTC", 1)
    portfolio.add_crypto("ETH", 5)

    # Supponiamo che il prezzo corrente del BTC sia $40,000 e dell'ETH sia $2,000
    current_prices = {"BTC": 40000.0, "ETH": 2000.0}

    portfolio.print_portfolio()
    portfolio.print_portfolio(current_prices)