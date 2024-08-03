import datetime
import pickle
import sys

import numpy as np
import pandas as pd
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import (MarketOrderRequest,
                                     TrailingStopOrderRequest)
from alpaca.trading.stream import TradingStream

import config
from bots.reversal_bot import Reversal


class Portfolio():

    def __init__(self, order_log):

        '''
        this class will be the portfolio manager for the bot class

        it will contain tickers to be scanned, positions, and account information

        when a buy order is given from the bot, it will take the amount of buying power and allocate it to
        the stocks to be bought and place the buy order

        when a sell order is given, it will place the order on the given ticker(s)
        '''
        
        self.client = TradingClient(api_key = config.API_KEY, secret_key=config.SECRET_KEY, paper=True)
        self.order_log = order_log

    def buy(self, buys:list[tuple]):

        account = dict(self.client.get_account())
        buying_power = float(account['cash'])
        if len(buys) != 0:

            buys_per_ticker = buying_power/len(buys) # will not work with small account sizes
            for buy in buys:

                qty = (0.8 * buys_per_ticker) // buy[1]
                if qty == 0:
                    continue
                
                market_order_data = TrailingStopOrderRequest(
                    symbol = buy[0],
                    qty = qty,
                    side = OrderSide.BUY,
                    time_in_force = TimeInForce.DAY,
                    trail_percent=1,
                )

                market_order = self.client.submit_order(
                    order_data = market_order_data
                )

                pickle_order_data = {
                    'Datetime'   : datetime.datetime.now(),
                    'Order type' : 'buy',
                    'Ticker'     : buy[0],
                    'Shares'     : qty,
                    'Price'      : buy[1]
                }

                self.log_trade(pickle_order_data)

    def sell(self, sells:list):

        if len(sells) != 0:
        
            for sell in sells:
                self.client.close_position(sell)
                print('sell order submitted')

    def log_trade(self, data, log_file_path=config.PICKLE_PATH):
        '''
        data should be a dictionary with these keys:
        Order type
        Ticker symbol
        Shares
        Price
        (Datetime will be added automatically)
        '''
        data['Datetime'] = datetime.datetime.now() # add datetime
        record = pd.DataFrame(data) # create dataframe to concat to log file
        log = pd.read_pickle(log_file_path)
        log = pd.concat([log, record], axis=1)
        pd.to_pickle(log, log_file_path)
