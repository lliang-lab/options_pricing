#!/usr/bin/env python3
import numpy as np
import copy

# Global constant for polynomial degree
POLYDEGREE = 3

class AsianOptionPricer:
    """Class to calculate option prices using a binomial tree approach."""

    def __init__(self, current_stock, strike, N, period, volatility, interest_rate):
        """
        Initialize the OptionPricer object with parameters.

        Parameters:
        current_stock (float): Current stock price.
        strike (float): Strike price.
        N (int): Number of steps in the binomial tree.
        period (float): Period to maturity.
        volatility (float): Volatility of the stock.
        interest_rate (float): Risk-free interest rate.
        """

        self.N = N
        self.current_stock = current_stock
        self.strike = strike
        self.mu = interest_rate - volatility ** 2 / 2.
        self.sigma = volatility
        self.period = period
        self.deltaT = period / N
        self.interest_rate = interest_rate
        self.discount_factor = np.exp(-interest_rate * (period / N))

    def calculate_asian_option_price(self, option_type, iterations, average_method):
        """
        Calculate the option price based on the specified option type and number of iterations.

        Parameters:
        option_type (str): Type of option ('EC', 'EP', 'AC', 'AP').
        iterations (int): Number of iterations for simulation.

        Returns:
        float: Option price.
        """
        if option_type not in ('EC', 'EP', 'AC', 'AP'):
            raise ValueError("Invalid option type")

        if average_method not in ('arithmetic', 'geometric'):
            raise ValueError("Invalid average method")

        stock_prices_ave = self._generate_random_paths(iterations, average_method)

        if option_type in ('AC', 'AP'):
            return self._backward_induction(stock_prices_ave, is_call=(option_type == 'AC'), iterations = iterations)
        else:
            res = np.mean([max(price - self.strike, 0) if option_type == 'EC' else max(self.strike - price, 0) for price in np.array(stock_prices_ave)[-1]])
            return res * np.exp(-self.interest_rate * self.period)

    def _generate_random_paths(self, iterations, average_method):

        randomwalk = np.random.normal(0, 1, size = iterations)
        stock_prices = [self.current_stock * np.ones(iterations)]
        ave_prices = copy.deepcopy(stock_prices)

        for i in range(self.N):
            randomwalk = np.random.normal(0, 1, size = iterations)
            X = ave_prices[-1]
            Y = list(stock_prices[-1] * np.exp(self.mu * self.deltaT + self.sigma * self.deltaT ** 0.5 * randomwalk))
            if average_method == 'arithmetic':
                Z = [(X[j] * (i + 1) + Y[j]) / (i + 2) for j in range(len(X))]
            else:
                Z = [np.exp((np.log(X[j]) * (i + 1) + np.log(Y[j])) / (i + 2)) for j in range(len(X))]
            stock_prices.append(Y)
            ave_prices.append(Z)
        return ave_prices

    def _backward_induction(self, stock_prices_ave, is_call, iterations):

        stock_prices_ave = np.array(stock_prices_ave)
        payoff = np.array([[max(stock_prices_ave[i][j] - self.strike, 0) if is_call else max(self.strike - stock_prices_ave[i][j], 0)
                            for j in range(iterations)] for i in range(self.N + 1)])
        Y = payoff[self.N]

        for i in range(self.N - 1, 0, -1):
            X = stock_prices_ave[i]
            hold = np.where(payoff[i] > 0)
            Y *= self.discount_factor

            if len(hold[0]) > POLYDEGREE:
                # Apply Least square method
                regression = np.polyfit(X[hold], Y[hold], POLYDEGREE)
                CY = np.polyval(regression, X[hold])

                # Whether to exercise now
                Y[hold] = np.where(payoff[i][hold] > CY, payoff[i][hold], Y[hold])
        return np.mean(Y)
