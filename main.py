# imports
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest, StopLossRequest
from alpaca.trading.stream import TradingStream
import pandas as pd
import yfinance as yf
import time
import datetime
import config # file containing API keys
from reversal_bot import Reversal
from portfolio import Portfolio

if __name__ == '__main__':

    table = pd.read_html('https://stockmarketmba.com/stocksinthenasdaq100.php')
    tickers = table[1]['Symbol'].to_list()

    portfolio = Portfolio()
    bot = Reversal(tickers)

    print('READY TO TRADE')

    while True:

        current_time = datetime.datetime.now().minute
        if current_time % 5 == 0:
            
            bot.push_to_watchlist()

            buys = bot.buy_query()
            portfolio.buy(buys)
            
            sells = bot.sell_query()
            portfolio.sell(sells)

            time.sleep(60)

        else:
            time.sleep(5)