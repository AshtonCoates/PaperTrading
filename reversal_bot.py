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

class reversal:
    
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

    def get_ma(self, ticker:str, period:int=20):
        
        # for now, using 5m periods. This is subject to change and would be helpful if it could be variable, that way different periods could be tested

        self.tickers[ticker].history(period='5m')

    def search(self):
        for ticker in self.tickers: