# imports
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest, StopLossRequest
from alpaca.trading.stream import TradingStream
import pandas as pd
import time
import datetime
import config # file containing API keys
from reversal_bot import Reversal
from portfolio import Portfolio

def read_tickers(filename):
    tickers_list = []
    with open(filename, 'r') as file:
        for line in file:
            ticker = line.strip()
            tickers_list.append(ticker)
        return tickers_list

if __name__ == '__main__':

    # (deprecated) list of tickers on the NASDAQ 100
    tickers = read_tickers('nasdaq_100.txt')

    portfolio = Portfolio()
    bot = Reversal(tickers)

    while True:

        current_time = datetime.datetime.now().minute
        if current_time % 5 == 0:
            
            bot.push_to_watchlist()

            buys = bot.buy_query()
            portfolio.buy(buys)
            
            sells = bot.sell_query(bot.holdings)
            portfolio.sell(sells)

        else:
            time.sleep(60)