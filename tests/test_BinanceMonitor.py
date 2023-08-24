from src.monitors.BinanceMonitor import BinanceMonitor
import json
import unittest
from time import sleep


# Assumendo che BinanceMonitor sia definita nello stesso file
# Altrimenti, importala da dove è stata definita

class TestBinanceMonitor(unittest.TestCase):

    def test_websocket_connection(self):
        # Definisci una callback personalizzata per on_message per verificare la ricezione dei dati
        def custom_on_message(ws, message):
            data = json.loads(message)
            # Ignora il messaggio di risposta alla sottoscrizione
            if 'result' in data and data['id'] == 1:
                return
            self.assertTrue('e' in data)  # Verifica che il messaggio abbia un campo 'e'
            ws.close()  # Chiudi la connessione dopo aver ricevuto un messaggio

        crypto_list = ["ethbtc"]
        monitor = BinanceMonitor(crypto_list)
        monitor.on_message = custom_on_message  # Sostituisci il metodo on_message con la nostra callback personalizzata
        monitor.run()
        sleep(5)  # Attendi un po' per dare al WebSocket il tempo di ricevere un messaggio


if __name__ == "__main__":
    unittest.main()
