#!/usr/bin/env python3
import numpy as np

class OptionPricer:
    """Class to calculate option prices using a binomial tree approach."""

    def __init__(self, curr_stock, strike, N, period, volatility, interest_rate):
        """
        Initialize the OptionPricer object with parameters.

        Parameters:
        curr_stock (float): Current stock price.
        strike (float): Strike price.
        N (int): Number of steps in the binomial tree.
        period (float): Period to maturity.
        volatility (float): Volatility of the stock.
        interest_rate (float): Risk-free interest rate.
        """

        self.N = N
        self.curr_stock = curr_stock
        self.strike = strike
        self.u = np.exp(volatility * np.sqrt(period / N))
        self.d = 1. / self.u
        self.a = np.exp(interest_rate * (period / N))
        self.p = (self.a - self.d) / (self.u - self.d)
        self.f = np.exp(-interest_rate * (period / N))
        self.stock_prices = [curr_stock * self.u ** (self.N - 2 * i) for i in range(self.N + 1)]

    def calculate_option_price(self, option_type):
        """
        Calculate the option price based on the specified option type.

        Parameters:
        option_type (str): Type of option ('EC', 'EP', 'AC', 'AP').

        Returns:
        float: Option price.
        """
        if option_type == 'EC':
            return self._calculate_option_price(is_call = True, in_advance = False)
        elif option_type == 'EP':
            return self._calculate_option_price(is_call = False, in_advance = False)
        elif option_type == 'AC':
            return self._calculate_option_price(is_call = True, in_advance = True)
        elif option_type == 'AP':
            return self._calculate_option_price(is_call = False, in_advance = True)
        else:
            raise ValueError("Invalid option type")

    def _calculate_option_price(self, is_call, in_advance):
        """
        Helper method to calculate option price.

        Parameters:
        is_call (bool): Whether it's a call option.
        in_advance (bool): Whether the option is exercised in advance.

        Returns:
        float: Option price.
        """
        options_prices = [max(price - self.strike, 0) if is_call else max(self.strike - price, 0) for price in self.stock_prices]

        while len(options_prices) > 1:
            for i in range(len(options_prices) - 1):
                stock_price = self.curr_stock * self.u ** (len(options_prices) - 2 - 2 * i)
                weighted_price = self.p * options_prices[i] + (1. - self.p) * options_prices[i + 1]
                if in_advance:
                    if is_call:
                        options_prices[i] = max(self.f * weighted_price, stock_price - self.strike)
                    else:
                        options_prices[i] = max(self.f * weighted_price, self.strike - stock_price)
                else:
                    options_prices[i] = self.f * weighted_price
            options_prices.pop()

        return options_prices[0]
