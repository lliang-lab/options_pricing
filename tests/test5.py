#!/usr/bin/env python3
import sys
import csv
sys.path.append('/Users/lliang/Deloitte/options/')

from BlackScholes import *
from BinomialTree_Asian import AsianOptionPricer as BTPricer
from MonteCarlo_Asian import AsianOptionPricer as MCPricer

AVE_METHOD = 'arithmetic' #'geometric'

def write_output(option_type, stock_prices, option_analytic, option_BT, option_MC):
    """
    Function to write the output to a CSV file.
    """
    with open(f'../outputs/Asian{option_type}_{AVE_METHOD}_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Stock Price', 'Analytic', 'BT', 'MC']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Stock Price': '',
                         'Analytic': f'Strike Price: {strike_price}, Interest Rate: {interest_rate}, Volatility: {volatility}, Period: {period}',
                         'BT': '',
                         'MC': '',
                         })
        for i in range(len(stock_prices)):
            writer.writerow({'Stock Price': stock_prices[i], 'Analytic': option_analytic[i], 'BT': option_BT[i], 'MC': option_MC[i]})


########## main function ###############
if __name__=='__main__':

    strike_price, interest_rate, volatility, period, = 50, 0.1, 0.4, 0.4167
    option_type = 'EP'#, 'AP'
    stock_prices = [i for i in range(1,100)]
    Nt = 10

    option_analytic = [black_scholes(f'A{option_type}-A', stock_price, strike_price, period, volatility, interest_rate) for stock_price in stock_prices]
    option_BT = [BTPricer(stock_price, strike_price, Nt, period, volatility, interest_rate).calculate_asian_option_price(option_type, AVE_METHOD) for stock_price in stock_prices]
    option_MC = [MCPricer(stock_price, strike_price, Nt, period, volatility, interest_rate).calculate_asian_option_price(option_type, 10000, AVE_METHOD) for stock_price in stock_prices]

    write_output(option_type, stock_prices, option_analytic, option_BT, option_MC)
