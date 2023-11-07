# PaperTrading

This repository tracks my efforts to build various stock/option trading strategies and deploy them for live paper trading using the Alpaca API.

## Overview

I wanted to implement strategies which traded a large "universe" of tickers rather than training a model/developing a strategy for one specific instrument. This way I could trade at a higher frequency and experiment with portfolio management and risk analysis. In general, there are multiple bot classes which each are responsible for screening a universe of stocks and recommending buys/sells to a portfolio class. The portfolio class is responsible for performing the buys/sells of all of the bots and performing any kind of risk management.

The strategies run on a Raspberry Pi 4 automatically each day. This allows the entire process to be automated with a cron job. It would have been easier to deploy the code over the cloud, but I wanted the experience setting up my own machine and using command line Linux.

## To Do List
* Add trailing stop losses for some preliminary risk management
* Add logging of trades so that portfolios can be evaluated when multiple are deployed (current dev implementation with pickle, but it's clunky. Switch to using Alpaca TradingStream)
* Implement risk management strategy, right now the portfolio just divides all capital between the buys sent by the bots
* Implement more strategies, perhaps more technical analysis strategies but I want to move more toward more statistically motivated strategies such as mean reversion and pairs trading