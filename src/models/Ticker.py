class Ticker:
    def __init__(self, data):
        """
        Initialize a new Ticker instance.

        :param data: Dictionary containing ticker data.
        """
        self.event_type = data['e']
        self.event_time = data['E']
        self.symbol = data['s']
        self.price_change = data['p']
        self.price_change_percent = data['P']
        self.weighted_avg_price = data['w']
        self.first_trade_price = data['x']
        self.last_price = data['c']
        self.last_qty = data['Q']
        self.best_bid_price = data['b']
        self.best_bid_qty = data['B']
        self.best_ask_price = data['a']
        self.best_ask_qty = data['A']
        self.open_price = data['o']
        self.high_price = data['h']
        self.low_price = data['l']
        self.total_traded_base_asset_volume = data['v']
        self.total_traded_quote_asset_volume = data['q']
        self.statistics_open_time = data['O']
        self.statistics_close_time = data['C']
        self.first_trade_id = data['F']
        self.last_trade_id = data['L']
        self.total_number_of_trades = data['n']

    def __str__(self):
        return f"Ticker for {self.symbol} - Last Price: {self.last_price}"

    # You can add more methods or attributes if needed.
