import datetime

import holidays
import pandas as pd
import yfinance as yf
from sklearn.neighbors import KNeighborsClassifier
from alpaca.trading.client import TradingClient
from datetime import datetime, timedelta

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

        # model vars (to be tested during backtesting)
        self.lookahead = 5 # number of periods ahead to predict return
        self.buy_threshold = 0.05
        self.sell_threshold = 0.025
        self.num_datapoints = 300

        self.backtest_vars = [self.lookahead, self.buy_threshold, self.sell_threshold, 
                              self.returns_interval, self.returns_period, self.highest_returns,
                              self.num_datapoints]

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
                period_return = (history['Close'].iloc[len(history)-1] /
                                history['Open'].iloc[0]) - 1
                returns[ticker] = period_return
            except:
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

    def _build_one_df(self, ticker:str, datapoints:int=1000, returns_period:int=5) -> pd.DataFrame:
        
        '''
        dependent variable: T-period cumulative return
        features:
        current price
        stock return during preceding period
        5 period MA value at preceding period
        10 period MA at preceding period
        total return over last 10 periods
        '''

        data = pd.DataFrame(columns=['return', 'price', 'yesterday_price', 'ma5', 'ma10', 'return10'])
        i = datetime.now() - timedelta(days=returns_period)
        while len(data) < datapoints:
            if i.weekday() < 5 or i in holidays.US(): # check if trading day
                continue
            start_date = i - timedelta(days=15)
            end_date = i + timedelta(days=returns_period)
            df = yf.Ticker(ticker, start=start_date, end=end_date, interval='1d')
            history = df.history()
            print(history.head())
            
        

    def buy_query(self, watchlist:dict[str], buy_threshold:int) -> list[str]:
        
        buy_list = []
        for i in watchlist:
            if None: #TODO
                buy_list.append(i)
        return buy_list
        
    
    def sell_query(self, watchlist:dict[str], sell_threshold:int) -> list[str]:

        sell_list = []
        for i in watchlist:
            if None: #TODO
                sell_list.append(i)
        return sell_list
        