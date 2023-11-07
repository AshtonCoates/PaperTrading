import datetime

import pandas as pd
import yfinance as yf
from sklearn.neighbors import KNeighborsClassifier
from alpaca.trading.client import TradingClient

import config

class Single_knn:

    def __init__(self, tickers:list[str]) -> None:

        '''
        This bot will trade a strategy inspired by the single stock KNN strategy in "151 Trading 
        Strategies" by Zura Kakushadz and Juan Andres Serur

        One difference from the Reversal class I implemented prior is that rather than the class
        handling any data fetching, I want to allow for data to be passed in. This will allow
        backtesting (which is necessary to tune parameters for this strategy), where before the bot
        was hardcoded to fetch current data, so feeding past data was not possible.

        This bot predicts a cumulative return over a future time period based off of the prices and
        volumes at previous time periods. 

        Storing enough historical data for all companies is not feasible, so I will screen through
        the available tickers at the start of each trading day to get a selection of companies I 
        can tade with this strategy, then load historical data.
        ''' 

        self.tickers=tickers
        self.client = TradingClient(api_key=config.API_KEY, secret_key=config.SECRET_KEY, paper=True)

        # screening vars (can be changed for backtesting)
        self.returns_interval = '1d'
        self.returns_period = '1mo'
        self.highest_returns = True # what should screener look for, highest or lowest returns

        # create a dataset to be used for the trading day
        self.watchlist = self.screen() # look for tickers trending down
        self.data = self.build_data(self.watchlist)


    def screen(self) -> list[str]:
        
        # look up 10 highest or lowest return tickers

        returns = {}

        for ticker in self.tickers:
            try: # handle tickers not found on yfinance
                history = yf.Ticker(ticker).history(period=self.returns_period, 
                                                    interval=self.returns_interval)
                period_return = (history['Close'].iloc[len(history)-1] - 
                                history['Open'].iloc[0]) / history['Open'].iloc[0]
                returns[ticker] = period_return
            except IndexError:
                self.tickers.remove(ticker)
                continue

        if self.highest_returns:
            return sorted(returns, key=lambda item: item[1])[:10]
        else:
            return sorted(returns, key=lambda item: item[1], reverse=True)[:10]

    def build_data(self, tickers:str) -> dict[pd.DataFrame]:
        data = {}
        for ticker in tickers:
            data[ticker] = self._build_one_df(ticker)
        return data

    def _build_one_df(self, ticker:str) -> pd.DataFrame:
        return

    def buy_query(self) -> list[str]:
        
        return
    
    def sell_query(self) -> list[str]:

        return