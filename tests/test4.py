#!/usr/bin/env python3
import sys
import csv
import time

sys.path.append('/Users/lliang/Deloitte/options/')

from BlackScholes import black_scholes
from FiniteDiff import OptionPricer as FDPricer

# Constants and configurations
STOCK_PRICE = 50
STRIKE_PRICE = 50
MAX_STOCK_PRICE = 200
INTEREST_RATE = 0.1
VOLATILITY = 0.4
PERIOD = 0.4167
OPTION_TYPE = 'EP'
NUM_TIME_STEPS = 100
NUM_ITERATIONS = 130
PDE_METHOD = 'explicit'
OUTPUT_FILE = f'../outputs/FD_EP_Nt{NUM_TIME_STEPS}_{PDE_METHOD}.csv'

def main():
    option_analytic = black_scholes(OPTION_TYPE, STOCK_PRICE, STRIKE_PRICE, PERIOD, VOLATILITY, INTEREST_RATE)
    option_prices = []
    used_time = []

    for i in range(NUM_ITERATIONS):
        print(i)
        start_time = time.time()
        option_price = FDPricer(STOCK_PRICE, STRIKE_PRICE, NUM_TIME_STEPS, PERIOD, VOLATILITY, INTEREST_RATE).calculate_option_price(OPTION_TYPE, MAX_STOCK_PRICE, i + 10, PDE_METHOD)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1e6
        used_time.append(elapsed_time)
        option_prices.append(option_price)

    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        fieldnames = ['Ns', 'FD', 'Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Ns': f'Stock Price: {STOCK_PRICE}, Strike Price: {STRIKE_PRICE}, Interest Rate: {INTEREST_RATE}, Volatility: {VOLATILITY}, Period: {PERIOD}, BlackScholes Value: {option_analytic}',
                         'FD': '',
                         'Time': ''
                         })

        for i in range(NUM_ITERATIONS):
            writer.writerow({'Ns': 10 + i, 'FD': option_prices[i], 'Time': used_time[i]})

if __name__ == '__main__':

    main()
