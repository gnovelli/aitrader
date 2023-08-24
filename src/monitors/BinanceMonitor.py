import json
import websocket

# Definizione del decoratore
from managers.DatabaseManager import DatabaseManager

class BinanceMonitor:

    def __init__(self, crypto_list, db_manager):
        self.crypto_list = crypto_list
        streams = "/".join(self.generate_streams(crypto_list))
        self.websocket_url = f"wss://stream.binance.com:9443/ws/{streams}"
        self.db_manager = db_manager

    def generate_streams(self, crypto_pairs):
        """Genera una lista degli stream basata sulle coppie di criptovalute"""
        return [f"{pair}@ticker" for pair in crypto_pairs]

    # Definizione del decoratore
    def record_data(func):
        def wrapper(self, ws, message):
            data = json.loads(message)
            # Utilizza l'istanza di DatabaseManager già presente nell'oggetto
            self.db_manager.insert_data(data)
            return func(self, ws, message)
        return wrapper

    @record_data
    def on_message(self, ws, message):
        data = json.loads(message)
        print(data)

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        # Sottoscrivi agli stream di tuo interesse.
        payload = {
            "method": "SUBSCRIBE",
            "params": self.generate_streams(self.crypto_list),
            "id": 1
        }
        ws.send(json.dumps(payload))

    def run(self):
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
