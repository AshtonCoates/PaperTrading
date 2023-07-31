'''
This script serves as a module to screen for stocks fitting a specific criteria each day.

For my starting strategy, I want to screen for stocks that have an uptrend over a long time period but show a pullback 
'''

#imports
import pandas as pd
import yfinance as yf
import datetime
from sklearn.linear_model import LinearRegression

# Screener will search NASDAQ tickers, need to convert all possible tickers to a list
nasdaq_tickers = pd.read_csv('nasdaq_tickers.csv')
tickers = nasdaq_tickers['Symbol'].tolist()

class Reversal:
    
    def __init__(self, tickers:list):

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

        self.tickers = yf.tickers(tickers)
        self.watchlist = []

    def get_ma(self, ticker:object, period:int=20):
        
        # returns a list of the last 2 moving averages, where the last item is the most recent

        # for now, using 5m periods. This is subject to change and would be helpful if it could be variable, that way different periods could be tested

        # we need the last 2 moving averages with a max of 60 periods per average, so 60*5=300 minutes
        # 5 minutes are added because we need the current and previous moving average 
        ma_df = self.tickers[ticker].history(period='305m', interval='5m')

        current_ma = ma_df.tail(period)
        previous_ma = ma_df.iloc[len(ma_df)-2: len(ma_df)-period-1: -1]

        return (previous_ma['Close'].mean(), current_ma['Close'].mean())

    def push_to_watchlist(self):

        # search all tickers, add those that fit the criteria to watchlist

        for ticker in self.tickers:
            ma_20 = self.get_ma(ticker)[1]
            ma_60 = self.get_ma(ticker, period=60)[1]
            if ma_20 < ma_60:
                self.watchlist.append(ticker)

    def buy_query(self) -> list[tickers]:

        # search watchlist, recommend buys if criteria is met

        buys = []
        for ticker in self.watchlist:
            ma_20 = self.get_ma(ticker)[1]
            ma_60 = self.get_ma(ticker, period=60)[1]
            if ma_20 > ma_60:
                buys.append(ticker)
        return buys
    
    def sell_query(self, positions) -> list[tickers]:

        # search list of current holdings to see which should be sold
        sells = []

        for ticker in positions:
            ma = self.get_ma(ticker)
            if ma[1] < ma[0]:
                sells.append(ticker)

        return sells