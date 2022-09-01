import pytz
import decimal as dc
import datetime as dt

def get_order(self, id: int) -> dict:
    """
    Returns:
        -> dict, including keys for 'id', 'filledSize', 'remainingSize', 
           'market' and 'status'.
    """
    return self._get(f"trade/{self.version}/orders/{id}")

def get_orders(self, market: str = None) -> list:
    """
    Gets a list of (live) orders that I have entered to a market. The most 
    recent order is listed first.
    """
    return self._get(f"trade/{self.version}/orders", {
        'accountId': self.account, 'symbolId': market,})
    
def get_orders_active(self, market: str = None) -> list:
    """
    Gets a list of (live) orders that I have entered to a market. The most 
    recent order is listed first.
    """
    return self._get(f"trade/{self.version}/orders/active", {
        'accountId': self.account, 'symbolId': market,})
    
def get_account(self) -> dict:
    """
    Retrives summary information about your account including all your open
    positions.
    """
    return self._get(f"md/{self.version}/summary/{self.account}/EUR")

def get_book(self, market: str, level: str):
    """
    Inputs:
        -> market: str, symbol of the market you want to query.
        -> level: str, can be either 'best_price' or 'market_depth'.
    """
    return self._get(f"md/{self.version}/feed/{market}/last", {'level': level})
    
def get_symbol(self, market: str):
    """
    Exante equiviant of ftx's 'get_market' funciton, collects some basic
    information about the market.

    Inputs:
        -> market: str, symbol that we are collecting information on.
    """
    return self._get(f"md/{self.version}/symbols/{market}")
    
def get_hours(self, market: str):
    """
    Return the hours when the market is open for trading.
    """
    return self._get(f"md/{self.version}/symbols/{market}/schedule")

def get_specifications(self, market: str):
    """
    Collects some additional details about the market, including the price step 
    (priceUnit) and the size step (lotSize).

    Inputs:
        -> market: str, symbol that we are collecting information on.
    """
    return self._get(f"md/{self.version}/symbols/{market}/specification")
    
def get_ticks(self, market: str, type: str, time_start, time_end) -> list:
    """
    Inputs:
        -> type: str, either 'quotes' or 'trades'.
        -> time_start: dt.datetime, earliest tick that will be recorded.
        -> time_end: str, last tick that will be recorded.
    
    Notes:
        -> Will collect only collect 1000 trades at a time. If there are more 
           than 1000 ticks betwen the start time and the end time the first 100 
           will be collected.
        -> The most recent tick is listed first with.
        -> Exante has quite restrictive ratelimits. Once this function has been 
           called it cannot be called again for a minute.
        -> The start and end time are rounded down to the nearest millisecond.
    """
    return self._get(f"md/{self.version}/ticks/{market}", {
        'from': str(int(time_start.timestamp() * 1000)), 
        'to': str(int(time_end.timestamp() * 1000)), 
        'type': type,
        })

def get_candles(self, market, resolution, start = None):
    """
    Inputs:
        -> resolution: int, duration of each candle in seconds. Acceptable 
           numbers are: 60, 300, 600, 900, 1800, 3600, 14400, 21600, and 86400.

    Notes:
        -> Exante has quite restrictive ratelimits. Once this function has been 
           called it cannot be called again for a minute.
    """
    if start == None:
        candles = self._get(f"md/3.0/ohlc/{market}/{resolution}", {'size': 50})
    else:
        candles = self._get(f"md/3.0/ohlc/{market}/{resolution}", {'from': start, 'size': 1000})
    for candle in candles:
        candle['time'] = dt.datetime.fromtimestamp(candle['timestamp'] // 1000).astimezone(pytz.timezone("Europe/Paris"))
    return candles

def get_history(self, market: str) -> list:
    """
    Gets a list of our past trades in a product.

    Returns:
        -> list: will include buys, sells and transaction fees as seperate items 
           in the list.
    """
    return self._get(f"md/{self.version}/transactions",
        {'accountId': self.account, 'symbolId': market,})