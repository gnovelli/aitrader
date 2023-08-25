import json
import websocket
from managers.DatabaseManager import DatabaseManager

class BinanceMonitor:
    """
    Classe BinanceMonitor per gestire la connessione e l'interazione con l'API di Binance attraverso WebSockets.
    """
    def __init__(self, crypto_list, db_manager):
        """
        Inizializza la lista delle criptovalute da monitorare, genera gli stream e inizializza l'URL del WebSocket.

        :param crypto_list: Lista delle coppie di criptovalute da monitorare.
        :param db_manager: Istanza di DatabaseManager per gestire le operazioni del database.
        """
        self.crypto_list = crypto_list
        streams = "/".join(self.generate_streams(crypto_list))
        self.websocket_url = f"wss://stream.binance.com:9443/ws/{streams}"
        self.db_manager = db_manager

    def generate_streams(self, crypto_pairs):
        """
        Genera una lista degli stream basata sulle coppie di criptovalute.

        :param crypto_pairs: Lista delle coppie di criptovalute.
        :return: Lista degli stream.
        """
        return [f"{pair}@ticker" for pair in crypto_pairs]

    def record_data(self, ws, message):
        """
        Funzione che registra i dati ricevuti nel database.

        :param ws: Istanza WebSocket.
        :param message: Messaggio ricevuto.
        """
        data = json.loads(message)
        if 'e' in data:
            self.db_manager.insert_data(data)

    def on_message(self, ws, message):
        """
        Gestisce i messaggi ricevuti dal WebSocket.

        :param ws: Istanza WebSocket.
        :param message: Messaggio ricevuto.
        """
        self.record_data(ws, message)  # Chiamata alla funzione di registrazione dei dati
        data = json.loads(message)
        if 'e' in data:
            print(data)

    def on_error(self, ws, error):
        """
        Gestisce gli errori del WebSocket.

        :param ws: Istanza WebSocket.
        :param error: Errore ricevuto.
        """
        print(type(error))
        print(f"Error: {error}")
        print(f"Error args: {error.args}")
        import traceback
        traceback.print_exc()

    def on_close(self, ws, close_status_code, close_msg):
        """
        Gestisce la chiusura del WebSocket.

        :param ws: Istanza WebSocket.
        :param close_status_code: Codice di stato della chiusura.
        :param close_msg: Messaggio di chiusura.
        """
        print("### closed ###")

    def on_open(self, ws):
        """
        Sottoscrive agli stream di interesse quando il WebSocket viene aperto.

        :param ws: Istanza WebSocket.
        """
        # Sottoscrivi agli stream di tuo interesse.
        payload = {
            "method": "SUBSCRIBE",
            "params": self.generate_streams(self.crypto_list),
            "id": 1
        }
        ws.send(json.dumps(payload))

    def run(self):
        """
        Avvia il monitoraggio.
        """
        ws = websocket.WebSocketApp(self.websocket_url, on_message=self.on_message, on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()


if __name__ == "__main__":
    # Lista delle coppie di criptovalute da monitorare
    crypto_list = ["ethbtc", "btcusdt", "xrpbtc"]
    db = DatabaseManager('binance.db')
    monitor = BinanceMonitor(crypto_list, db)
    monitor.run()
