#!/usr/bin/env python3
import numpy as np

class AsianOptionPricer:
    """Class to calculate Asian option prices using a binomial tree approach."""

    def __init__(self, current_stock, strike, N, period, volatility, interest_rate):
        """
        Initialize the AsianOptionPricer object with parameters.

        Parameters:
        current_stock (float): Current stock price.
        strike (float): Strike price.
        N (int): Number of steps in the binomial tree.
        period (float): Period to maturity.
        volatility (float): Volatility of the stock.
        interest_rate (float): Risk-free interest rate.
        """

        self.N = N
        self.curr_stock = current_stock
        self.strike = strike
        self.u = np.exp(volatility * np.sqrt(period / N))
        self.d = 1. / self.u
        self.a = np.exp(interest_rate * (period / N))
        self.p = (self.a - self.d) / (self.u - self.d)
        self.f = np.exp(-interest_rate * (period / N))

    def calculate_asian_option_price(self, option_type, method):
        """
        Calculate the Asian option price based on the specified option type and method.

        Parameters:
        option_type (str): Type of option ('EC', 'EP', 'AC', 'AP').
        method (str): Method for averaging ('arithmetic' or 'geometric').

        Returns:
        float: Option price.
        """
        if method not in ('arithmetic', 'geometric'):
            raise ValueError("Method must be 'arithmetic' or 'geometric'")

        if option_type == 'EC':
            return self._calculate_asian_option_price(is_call = True, in_advance = False, method = method)
        elif option_type == 'EP':
            return self._calculate_asian_option_price(is_call = False, in_advance = False, method = method)
        elif option_type == 'AC':
            return self._calculate_asian_option_price(is_call = True, in_advance = True, method = method)
        elif option_type == 'AP':
            return self._calculate_asian_option_price(is_call = False, in_advance = True, method = method)
        else:
            raise ValueError("Invalid option type")

    def _calculate_asian_option_price(self, is_call, in_advance, method):
        """
        Helper method to calculate Asian option price.

        Parameters:
        is_call (bool): Whether it's a call option.
        in_advance (bool): Whether the option is exercised in advance.
        method (str): Method for averaging ('arithmetic' or 'geometric').

        Returns:
        float: Option price.
        """
        stock_prices = self._initialize_stock_prices()
        ave_stock_prices = self._initialize_ave_stock_prices(stock_prices, method)

        option_price = self._calculate_option_prices(stock_prices, ave_stock_prices, is_call, in_advance)
        return option_price

    def _initialize_stock_prices(self):
        stock_prices = {1:{}}

        for i in range(1, self.N + 1):
            if i == 1:
                stock_prices[1]['u'] = [self.curr_stock, self.curr_stock * self.u]
                stock_prices[1]['d'] = [self.curr_stock, self.curr_stock * self.d]
            else:
                stock_prices[i] = {}
                for path in stock_prices[i - 1]:
                    upper_path = ''.join([path, 'u'])
                    lower_path = ''.join([path, 'd'])
                    stock_prices[i][upper_path] = stock_prices[i - 1][path] + [stock_prices[i - 1][path][-1] * self.u]
                    stock_prices[i][lower_path] = stock_prices[i - 1][path] + [stock_prices[i - 1][path][-1] * self.d]

        return stock_prices

    def _initialize_ave_stock_prices(self, stock_prices, method):
        ave_stock_prices = {}

        for i in stock_prices:
            ave_stock_prices[i] = {}
            for path in stock_prices[i]:
                if method == 'arithmetic':
                    ave_stock_prices[i][path] = np.average(stock_prices[i][path])
                    ave_stock_prices[i][path] = np.average(stock_prices[i][path])
                else:
                    ave_stock_prices[i][path] = np.exp(np.average([np.log(price) for price in stock_prices[i][path]]))
                    ave_stock_prices[i][path] = np.exp(np.average([np.log(price) for price in stock_prices[i][path]]))

        return ave_stock_prices

    def _calculate_option_prices(self, stock_prices, ave_stock_prices, is_call, in_advance):

        options_prices = {self.N: {}}
        for path in stock_prices[self.N]:
            options_prices[self.N][path] = max(ave_stock_prices[self.N][path] - self.strike, 0) if is_call else max(self.strike - ave_stock_prices[self.N][path], 0)

        for i in range(self.N - 1, 0, -1):
            options_prices[i] = {}
            for path in stock_prices[i]:
                weighted_price = self.p * options_prices[i + 1][path + 'u'] + (1. - self.p) * options_prices[i + 1][path + 'd']
                if in_advance:
                    if is_call:
                        options_prices[i][path] = max(self.f * weighted_price, max(ave_stock_prices[i][path] - self.strike, 0))
                    else:
                        options_prices[i][path] = max(self.f * weighted_price, max(self.strike - ave_stock_prices[i][path], 0))
                else:
                    options_prices[i][path] = self.f * weighted_price

        return self.f * (self.p * options_prices[1]['u'] + (1. - self.p) * options_prices[1]['d'])
