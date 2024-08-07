import datetime

import pandas as pd
import yfinance as yf
from alpaca.trading.client import TradingClient
from sklearn.linear_model import LinearRegression

import config


class Reversal:
    
    def __init__(self, tickers:list[str]):

        '''
        This bot will first check stocks listed on the NASDAQ for a few characteristics, and order their priority based on these characteristics to decide
        what trades will be made. The characteristics are as follows (and subject to experimentation):

        The coefficient of a lineear regression of closing priceson date should be positive. The coefficient of this regression will determine highest
        priority trades

        The trade will be put on a watchlist when the 20 period moving average crosses below the 60 period moving average

        The trade will be removed from teh watchlist and bought when the 20 period moving average crosses back above the 
        60 period moving average

        The trade will be sold when the 20 period moving average decreases from the previous timestamp, showing that it is starting to reverse
        '''

        self.tickers = tickers
        self.watchlist = []
        self.client = TradingClient(api_key = config.API_KEY, secret_key=config.SECRET_KEY, paper=True)

    def get_ma(self, ticker:object, period:int=20):
        
        # returns a list of the last 2 moving averages, where the last item is the most recent

        # for now, using 5m periods. This is subject to change and would be helpful if it could be variable, that way different periods could be tested

        # we need the last 2 moving averages with a max of 60 periods per average, so 60*5=300 minutes
        # 5 minutes are added because we need the current and previous moving average 

        # NOTE: the calculation is correct and can be verified with real market software
        minutes = '{}m'.format((period+1)*5)
        ma_df = yf.Ticker(ticker).history(period=minutes, interval='5m')

        current_ma = ma_df.tail(period)
        previous_ma = ma_df.iloc[len(ma_df)-2: len(ma_df)-period-1: -1]

        return (previous_ma['Close'].mean(), 
                current_ma['Close'].mean(), 
                ma_df['Close'].iloc[-1]) # return current MA, previous MA, and stock price

    def push_to_watchlist(self):

        # search all tickers, add those that fit the criteria to watchlist

        for ticker in self.tickers:
            if ticker in [i.symbol for i in self.client.get_all_positions()] or ticker in self.watchlist:
                continue
            try:
                ma_20 = self.get_ma(ticker)[1]
                ma_60 = self.get_ma(ticker, period=60)[1]
            except IndexError: # handle error when yfinance cannot find ticker
                self.tickers.remove(ticker)
                continue
            if ma_20 < ma_60:
                self.watchlist.append(ticker)
        
        print('watchlist updated')

    def buy_query(self) -> list:

        # search watchlist, recommend buys if criteria is met

        buys = []
        for ticker in self.watchlist:
            try:
                _, ma_20, current_price = self.get_ma(ticker)
                _, ma_60, _ = self.get_ma(ticker, period=60)
            except IndexError:
                self.tickers.remove(ticker)
                self.watchlist.remove(ticker)
                continue
            if ma_20 > ma_60:
                buys.append((ticker, current_price))
                self.watchlist.remove(ticker)
        return buys
    
    def sell_query(self) -> list:

        # search list of current holdings to see which should be sold
        sells = []

        for ticker in [i.symbol for i in self.client.get_all_positions()]:
            ma = self.get_ma(ticker)
            if ma[1] < ma[0]:
                sells.append(ticker)

        return sells