import sqlite3
import pandas as pd
import threading

class DatabaseManager:
    """
    Classe DatabaseManager per gestire la connessione e le operazioni con un database SQLite.
    """

    # Mappa che traduce le chiavi dei dati ricevuti in nomi di campo più descrittivi per il database.
    FIELD_MAPPING = {
        'e': 'event_type',
        'E': 'event_time',
        's': 'symbol',
        'p': 'price_change',
        'P': 'price_change_percent',
        'w': 'weighted_avg_price',
        'x': 'prev_close_price',
        'c': 'curr_close_price',
        'Q': 'last_trade_qty',
        'b': 'best_bid_price',
        'B': 'best_bid_qty',
        'a': 'best_ask_price',
        'A': 'best_ask_qty',
        'o': 'open_price',
        'h': 'high_price',
        'l': 'low_price',
        'v': 'traded_base_vol',
        'q': 'traded_quote_vol',
        'O': 'stats_open_time',
        'C': 'stats_close_time',
        'F': 'first_trade_id',
        'L': 'last_trade_id',
        'n': 'total_trades'
    }

    def __init__(self, db_path=':memory:'):
        """
        Inizializza la connessione al database e crea la tabella se non esiste.

        :param db_path: Percorso del database. Di default, utilizza la memoria.
        """
        # Connessione al database
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()

        # Creazione della tabella se non esiste
        self.create_table()

    def create_table(self):
        """
        Crea una tabella nel database se non esiste già.
        """
        columns = ', '.join([f"{v} TEXT" for v in self.FIELD_MAPPING.values()])
        with self.lock:
            self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS binance_data (
                id INTEGER PRIMARY KEY,
                {columns}
            )
            ''')

    def insert_data(self, data):
        """
        Inserisce i dati nella tabella.

        :param data: Dizionario contenente i dati da inserire.
        """
        keys = ', '.join(self.FIELD_MAPPING.values())
        placeholders = ', '.join(['?'] * len(self.FIELD_MAPPING))
        values = [data[k] for k in self.FIELD_MAPPING.keys()]
        with self.lock:
            self.cursor.execute(f'''
            INSERT INTO binance_data ({keys})
            VALUES ({placeholders})
            ''', values)
            self.conn.commit()

    def fetch_data(self, symbol=None):
        """
        Recupera i dati dalla tabella. Se viene fornito un simbolo, filtra per quella coppia di valute.

        :param symbol: (Opzionale) Simbolo della coppia di valute da filtrare.
        :return: Lista di tuple contenente i dati recuperati.
        """
        query = "SELECT * FROM binance_data"
        params = ()

        if symbol:
            query += " WHERE symbol = ?"
            params = (symbol,)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def records_to_dataframe(self,
                             records):
        """
        Converte una lista di record in un DataFrame di pandas.

        :param records: Lista di tuple contenente i dati.
        :return: DataFrame di pandas.
        """
        # Lista dei nomi dei campi (colonne) in base all'ordine in cui sono inseriti nel database
        columns = [
            'id','event_type', 'event_time', 'symbol', 'price_change', 'price_change_percent',
            'weighted_avg_price', 'prev_close_price', 'current_close_price', 'last_trade_quantity',
            'best_bid_price', 'best_bid_quantity', 'best_ask_price', 'best_ask_quantity',
            'open_price', 'high_price', 'low_price', 'total_traded_base_asset_volume',
            'total_traded_quote_asset_volume', 'stats_open_time', 'stats_close_time',
            'first_trade_id', 'last_trade_id', 'total_num_trades'
        ]

        # Conversione dei record in un DataFrame
        df = pd.DataFrame(records, columns=columns)

        return df

    def fetch_dataframe(self, symbol=None):
        """
        Recupera i dati dalla tabella e li restituisce come DataFrame.

        :param symbol: (Opzionale) Simbolo della coppia di valute da filtrare.
        :return: DataFrame di pandas.
        """
        records = self.fetch_data(symbol=symbol)
        df = self.records_to_dataframe(records)
        return df

    def close(self):
        """
        Chiude la connessione al database.
        """
        with self.lock:
            self.conn.close()

if __name__ == "__main__":
    # Test della classe DatabaseManager
    db = DatabaseManager('C:\\Users\\shema\\Documents\\dev\\aitrader\\binance.db')
    sample_data = {
        'e': '24hrTicker', 'E': 1692863706598, 's': 'BTCUSDT', 'p': '419.44000000', 'P': '1.610',
        'w': '26343.27048841', 'x': '26050.01000000', 'c': '26469.45000000', 'Q': '0.00878000',
        'b': '26469.45000000', 'B': '12.90727000', 'a': '26469.46000000', 'A': '1.83432000',
        'o': '26050.01000000', 'h': '26819.27000000', 'l': '25812.82000000', 'v': '41796.56431000',
        'q': '1101058199.10452790', 'O': 1692777306598, 'C': 1692863706598, 'F': 3197587545,
        'L': 3198235645, 'n': 648101
    }
    db.insert_data(sample_data)

    df = db.fetch_dataframe(symbol="BTCUSDT")
    print(df.describe())
    print(df.tail(100))

    db.close()
