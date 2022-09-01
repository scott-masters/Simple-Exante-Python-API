# This is not much of a testing infrastucture. We just run some funcitons to
# make sure your credientials and connection are good.

import pytz
import time

import datetime as dt

from main import Exante_Client

client = Exante_Client(
    account = "ABC1234.001",
    app_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    client_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    shared_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    end_point = "https://api-demo.exante.eu/"
)

# Collects some summary information about your account.
account = client.get_account()

time.sleep(61)

# Collects any live orders you have in this product.
orders = client.get_orders(market = "BIRG.EURONEXT")

# Going to sleep to accomodate Exante rate limits.
time.sleep(61)

# Collects the open-high-low-close candles for AAVE with hourly resolution.
olhc = client.get_candles(market = "AAVE.USD", resolution = 3600)

# Finds out what hours this product is open for trading.
schedule = client.get_hours(market = "GLB.EURONEXT")

# Collects the current order book of AAVE.
book = client.get_book(market = "AAVE.USD", level = "market_depth")

# Going to sleep to accomodate Exante rate limits.
time.sleep(61)

# Lists the trades that other people made in AAPL. 
trades = client.get_ticks(
    market = "AAPL.NASDAQ", type = "trades", 
    time_start = dt.datetime(2020, 8, 29, tzinfo = pytz.timezone("UTC")), 
    time_end = dt.datetime.now(pytz.timezone("UTC"))
)

# If you don't want to trade you may wish to move the price below the current
# price of AAVE before you uncomment this command.
# order = client.place_order(
#     market = "AAVE.USD", side = "buy", price = "90", size = "1")

# Note: not all functions are included in this file. Read through exante.py to
# see everything I have provided and https://api-live.exante.eu/api-docs/ for
# the full offering of what you can build.

