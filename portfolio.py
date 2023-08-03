import pandas as pd
import numpy as np

import requests
import datetime

import yfinance as yf

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest, StopLossRequest
from alpaca.trading.stream import TradingStream

import config
from reversal_bot import Reversal

class Portfolio():

    def __init__(self, tickers:list[str]):

        '''
        this class will be the portfolio manager for the bot class

        it will contain tickers to be scanned, positions, and account information

        when a buy order is given from the bot, it will take the amount of buying power and allocate it to
        the stocks to be bought and place the buy order

        when a sell order is given, it will place the order on the given ticker(s)
        '''

        self.tickers = tickers
        
        self.client = TradingClient(api_key = config.API_KEY, secret_key=config.SECRET_KEY, paper=True)
        self.account = dict(client.get_account())

    def buy(self, buys:list[tuple]):

        buying_power = self.account['buying_power']
        buys_per_ticker = buying_power/len(buys) # will not work with small account sizes
        for buy in buys:

            market_order_data = MarketOrderRequest(
                symbol = buy[0],
                qty = buying_power // buy[1],
                side = OrderSide.BUY,
                time_in_force = TimeInForce.DAY
            )

            market_order = self.client.submit_order(
                order_data = market_order_data
            )

    def sell(self, sells:list):
        
        for sell in sells:

            self.client.close_position(sell)
