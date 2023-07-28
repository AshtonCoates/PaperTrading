# imports
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest, StopLossRequest
from alpaca.trading.stream import TradingStream
import pandas as pd
import config # file containing API keys

client = TradingClient(api_key = config.API_KEY, secret_key=config.SECRET_KEY, paper=True)
account = dict(client.get_account())
for i,j in account.items():
    print(i, j)

order_details = MarketOrderRequest(
    symbol = "SPY",
    qty = 10,
    side = OrderSide.BUY,
    TimeInForce = TimeInForce.DAY
)

order = client.submit_order(order_data = order_details)

trades = TradingStream(config.API_KEY, config.SECRET_KEY, paper=True)


