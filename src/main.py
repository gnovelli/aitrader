from monitors.BinanceMonitor import BinanceMonitor
from managers.DatabaseManager import DatabaseManager

if __name__ == "__main__":
    path='../'
    filename='binance.db'
    pathname=path+filename
    crypto_list = ["ethbtc", "btcusdt", "xrpbtc"]
    db = DatabaseManager(pathname)
    monitor = BinanceMonitor(crypto_list, db)
    monitor.run()

