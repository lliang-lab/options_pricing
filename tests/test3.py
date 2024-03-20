#!/usr/bin/env python3
import sys
import csv
import time

sys.path.append('/Users/lliang/Deloitte/options/')

from BlackScholes import black_scholes
from MonteCarlo import OptionPricer as MCPricer

# Constants and configurations
OUTPUT_FILE = '../outputs/MC_EP_steps.csv'
STOCK_PRICE = 50
STRIKE_PRICE = 50
INTEREST_RATE = 0.1
N = 10
VOLATILITY = 0.4
PERIOD = 0.4167
OPTION_TYPE = 'EP'
NUM_ITERATIONS = 150

def main():
    option_analytic = black_scholes(OPTION_TYPE, STOCK_PRICE, STRIKE_PRICE, PERIOD, VOLATILITY, INTEREST_RATE)
    option_prices = []
    used_time = []

    for i in range(2, NUM_ITERATIONS + 2):
        print(i)
        iterations = int(10 ** (2 + 0.03 * i))
        start_time = time.time()
        option_price = MCPricer(STOCK_PRICE, STRIKE_PRICE, N, PERIOD, VOLATILITY, INTEREST_RATE).calculate_option_price(OPTION_TYPE, iterations)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1e6
        used_time.append(elapsed_time)
        option_prices.append(option_price)

    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        fieldnames = ['iterations', 'MC', 'Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Nt': f'Stock Price: {STOCK_PRICE}, Strike Price: {STRIKE_PRICE}, Interest Rate: {INTEREST_RATE}, Volatility: {VOLATILITY}, Period: {PERIOD}, BlackScholes Value: {option_analytic}',
                         'BT': '',
                         'Time': ''
                         })

        for i in range(NUM_ITERATIONS):
            writer.writerow({'Nt': int(10 ** (2.06 + 0.03 * i)), 'BT': option_prices[i], 'Time': used_time[i]})

if __name__ == '__main__':

    main()
