# PaperTrading

This repository tracks my efforts to build various stock/option trading strategies and deploy them for live paper trading using the Alpaca API.

## Overview

I wanted to implement strategies which traded a large "universe" of tickers rather than training a model/developing a strategy for one specific instrument. This way I could trade at a higher frequency and experiment with portfolio management and risk analysis. In general, there are multiple bot classes which each are responsible for screening a universe of stocks and recommending buys/sells to a portfolio class. The portfolio class is responsible for performing the buys/sells of all of the bots and performing any kind of risk management.

## To Do List
* Add trailing stop losses for some preliminary risk management
* Add logging of trades so that portfolios can be evaluated when multiple are deployed (current dev implementation with pickle, but it's clunky. Switch to using Alpaca TradingStream)
* Add bot trading on a linear regression strategy
* Implement risk management strategy, right now the portfolio just divides all capital between the buys sent by the bots