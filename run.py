from zipline.api import record, symbol, get_open_orders, order_percent, order, order_target_percent
import operator
import math
from pandas import *
from numpy import *
from zipline.errors import SymbolNotFound


def initialize(context):
    # Get all tickers in america stock
    tickers=read_table('Ticker.txt')
    context.tickers=transpose(array(tickers)).tolist()[0]

    # Configurations for context object
    context.day = 0
    context.DAYS_CUMULATIVE = 90
    context.REFORM_PERIOD = 5
    context.PORTFOLIO_SIZE = 20
    context.STARTING_CASH = 100000.0
    context.my_portfolio_quantity = {}

# This method runs every day. data.history fetches the data from TODAY
def handle_data(context, data):
    # Skip first 90 days to get full windows
    if context.day < context.DAYS_CUMULATIVE:
        context.day += 1
        return
    if context.day % context.REFORM_PERIOD != 0:
        context.day += 1
        return
    context.day += 1

    # For each stock, compute gain in last 90 days
    d = {}
    for ticker in context.tickers:
        # Compute averages
        # data.history() has to be called with the same params
        # from above and returns a pandas dataframe.
        try:
            df = data.history(symbol(ticker), 'close', bar_count=context.DAYS_CUMULATIVE, frequency="1d")
            start_price = df.iloc[:1].tolist()[0]
            end_price = df.iloc[-1:].tolist()[0]

            gain = float(end_price) / start_price
            if not math.isnan(gain):
                d[ticker] = gain
        except SymbolNotFound as e:
            # print "WARN: Unable to get data for %s" % ticker
            print '',
            
        
    # Sort all tickers by there gain in ascending order
    sorted_d = sorted(d.items(), key=operator.itemgetter(1))

    portfolio_with_gain = sorted_d[-context.PORTFOLIO_SIZE:]
    portfolio = [i[0] for i in portfolio_with_gain]
    
    capital_each_share = context.STARTING_CASH / context.PORTFOLIO_SIZE
    
    # Trading logic
    for stock in portfolio:
        if stock not in context.my_portfolio_quantity.keys():
            quantity = int(capital_each_share / data.current(symbol(stock), 'close'))

            # order(symbol(stock) , quantity)

            order_percent(symbol(stock) , 1.0 / context.PORTFOLIO_SIZE)
            
            context.my_portfolio_quantity[stock] = quantity
            
    for stock in context.my_portfolio_quantity.keys():
        if stock not in portfolio:
            quantity = context.my_portfolio_quantity[stock]
            del context.my_portfolio_quantity[stock]
            # order(symbol(stock) ,-quantity)

            order_target_percent(symbol(stock) , 0.0)
            

    # Printing each portfolio
    print "day %d" % context.day        
    print portfolio    
    print '\n\n'