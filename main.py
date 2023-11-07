# imports
import logging
import time
from datetime import date, datetime
import os

import holidays
import pandas as pd
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest, StopLossRequest
from alpaca.trading.stream import TradingStream

import config  # file containing API keys
from portfolio import Portfolio
from bots.reversal_bot import Reversal

logging.basicConfig(filename='error_log.txt',
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():

    us_holidays = holidays.US()
    today=date.today()
    if today in us_holidays:
        print('HOLIDAY: MARKET CLOSED')
        quit()

    table = pd.read_html('https://stockmarketmba.com/stocksinthenasdaq100.php')
    tickers = table[1]['Symbol'].to_list()

    # Create dataframe for logging if there isn't one, otherwise load it into memory
    log_cols = ['Datetime','Order type', 'Ticker', 'Shares', 'Price']
    log = pd.read_pickle(config.PICKLE_PATH) if os.path.exists(config.PICKLE_PATH) else pd.DataFrame(columns=log_cols)

    portfolio = Portfolio(log)
    bot = Reversal(tickers)

    print('READY TO TRADE')

    while True:

        current_time = datetime.now()
        print(current_time)

        if current_time.hour >= 13:
            print('MARKET CLOSED')
            quit()

        elif current_time.minute % 5 == 0:
            
            bot.push_to_watchlist()

            buys = bot.buy_query()
            portfolio.buy(buys)
            
            sells = bot.sell_query()
            portfolio.sell(sells)

            time.sleep(60)

        else:
            time.sleep(5)

if __name__ == '__main__':
        main()