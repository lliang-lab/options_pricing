#!/usr/bin/env python3
import argparse
import numpy as np
import os
from BinomialTree import OptionPricer as BinPricer
from BinomialTree_Asian import AsianOptionPricer as AsianBinPricer
from MonteCarlo import OptionPricer as MCPricer
from MonteCarlo_Asian import AsianOptionPricer as AsianMCPricer
from FiniteDiff import OptionPricer as FDPricer
from BlackScholes import *

########## main function ###############
if __name__=='__main__':

    parser = argparse.ArgumentParser(description='To calculate the options price. @ Liang Lichen 2024')
    parser.add_argument('-s', '--stock', type = float, default = 50, help = 'current stock price (default value: 50 USD)')
    parser.add_argument('-k', '--strike', type = float, default = 50, help = 'strike price (default value: 52 USD)')
    parser.add_argument('-r', '--interest', type = float, default = 0.1, help = 'risk-free interest rate (default value: 10%%)')
    parser.add_argument('-v', '--volatility', type = float, default = 0.4, help = 'volatility (default value: 40%%)')
    parser.add_argument('-P', '--period', type = float, default = 1., help = 'period at maturity (default value: 1.)')
    parser.add_argument('-N', '--layers', type = int, default = 5, help = 'options type [default: AM (American call)]')
    args = parser.parse_args()

    curr_stock = args.stock
    strike = args.strike
    interest_rate = args.interest
    volatility = args.volatility
    period = args.period
    N = args.layers

    t = BinPricer(curr_stock, strike, N, period, volatility, interest_rate)
    print('Binomial EP', t.calculate_option_price('EP'))
    print('Binomial EC', t.calculate_option_price('EC'))
    print('Binomial AP', t.calculate_option_price('AP'))
    print('Binomial AC', t.calculate_option_price('AC'))

    t = AsianBinPricer(curr_stock, strike, N, period, volatility, interest_rate)
    print('Binomial Asian EP arithmetic', t.calculate_asian_option_price('EP', 'arithmetic'))
    print('Binomial Asian EP geometric', t.calculate_asian_option_price('EP', 'geometric'))
    print('Binomial Asian EC arithmetic', t.calculate_asian_option_price('EC', 'arithmetic'))
    print('Binomial Asian EC geometric', t.calculate_asian_option_price('EC', 'geometric'))
    print('Binomial Asian AP arithmetic', t.calculate_asian_option_price('AP', 'arithmetic'))
    print('Binomial Asian AC arithmetic', t.calculate_asian_option_price('AC', 'arithmetic'))

    t = MCPricer(curr_stock, strike, N, period, volatility, interest_rate)
    print('MonteCarlo EP', t.calculate_option_price('EP', 1000000))
    print('MonteCarlo EC', t.calculate_option_price('EC', 1000000))
    print('MonteCarlo AP', t.calculate_option_price('AP', 100000))
    print('MonteCarlo AC', t.calculate_option_price('AC', 100000))

    t = AsianMCPricer(curr_stock, strike, N, period, volatility, interest_rate)
    print('MonteCarlo Asian EP arithmetic', t.calculate_asian_option_price('EP', 100000, 'arithmetic'))
    print('MonteCarlo Asian EP geometric', t.calculate_asian_option_price('EP', 100000, 'geometric'))
    print('MonteCarlo Asian EC arithmetic', t.calculate_asian_option_price('EC', 100000, 'arithmetic'))
    print('MonteCarlo Asian EC geometric', t.calculate_asian_option_price('EC', 100000, 'geometric'))
    print('MonteCarlo Asian AP arithmetic', t.calculate_asian_option_price('AP', 100000, 'arithmetic'))
    print('MonteCarlo Asian AC arithmetic', t.calculate_asian_option_price('AC', 100000, 'arithmetic'))

    t = FDPricer(curr_stock, strike, N, period, volatility, interest_rate)
    print('Finite Difference EP', t.calculate_option_price('EP', 100, 100, 'implicit'))
    print('Finite Difference EC', t.calculate_option_price('EC', 200, 100, 'implicit'))
    print('Finite Difference AP', t.calculate_option_price('AP', 100, 100, 'implicit'))
    print('Finite Difference AC', t.calculate_option_price('AC', 200, 100, 'implicit'))

    print('Black-Scholes EP', black_scholes('EP', curr_stock, strike, period, volatility, interest_rate))
    print('Black-Scholes EC', black_scholes('EC', curr_stock, strike, period, volatility, interest_rate))
    print('Black-Scholes Asian EP geometric', black_scholes('AEP-G', curr_stock, strike, period, volatility, interest_rate))
    print('Black-Scholes Asian EC geometric', black_scholes('AEC-G', curr_stock, strike, period, volatility, interest_rate))
