#!/usr/bin/env python3
import sys
import csv
sys.path.append('/Users/lliang/Deloitte/options/')

from BlackScholes import *
from BinomialTree import OptionPricer as BTPricer
from MonteCarlo import OptionPricer as MCPricer
from FiniteDiff import OptionPricer as FDPricer

def write_output(option_type, stock_prices, option_analytic, option_BT, option_MC, option_FD):
    """
    Function to write the output to a CSV file.
    """
    with open(f'../outputs/{option_type}_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Stock Price', 'Analytic', 'BT', 'MC', 'FD']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Stock Price': '',
                         'Analytic': f'Strike Price: {strike_price}, Interest Rate: {interest_rate}, Volatility: {volatility}, Period: {period}',
                         'BT': '',
                         'MC': '',
                         'FD': ''})
        for i in range(len(stock_prices)):
            writer.writerow({'Stock Price': stock_prices[i], 'Analytic': option_analytic[i], 'BT': option_BT[i], 'MC': option_MC[i], 'FD': option_FD[i]})


########## main function ###############
if __name__=='__main__':

    strike_price, interest_rate, volatility, period, = 50, 0.1, 0.4, 0.4167
    option_type = 'EP'#, 'AP'
    stock_prices = [i for i in range(1,100)]
    Nt = 10

    option_analytic = [black_scholes('EP', stock_price, strike_price, period, volatility, interest_rate) for stock_price in stock_prices]
    option_BT = [BTPricer(stock_price, strike_price, Nt, period, volatility, interest_rate).calculate_option_price(option_type) for stock_price in stock_prices]
    option_MC = [MCPricer(stock_price, strike_price, Nt, period, volatility, interest_rate).calculate_option_price(option_type, 10000) for stock_price in stock_prices]
    option_FD = [FDPricer(stock_price, strike_price, Nt, period, volatility, interest_rate).calculate_option_price(option_type, 200, 100, 'implicit') for stock_price in stock_prices]

    write_output(option_type, stock_prices, option_analytic, option_BT, option_MC, option_FD)
