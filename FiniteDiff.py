#!/usr/bin/env python3
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve
import scipy.interpolate as spi

class OptionPricer:
    """Class to calculate option prices using finite difference methods."""

    def __init__(self, current_stock, strike, num_steps, period, volatility, interest_rate):
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

        self.num_steps = num_steps
        self.current_stock = current_stock
        self.strike = strike
        self.sigma = volatility
        self.period = period
        self.deltaT = period / num_steps
        self.interest_rate = interest_rate
        self.discount_factor = np.exp(- interest_rate * (period / num_steps))

    def calculate_option_price(self, option_type, max_stock_price, num_stock_steps, PDE_method):
        """
        Calculate the option price using finite difference methods.

        Parameters:
        option_type (str): Type of option ('EC' for European call, 'EP' for European put,
                           'AC' for American call, 'AP' for American put).
        max_stock_price (float): Maximum stock price.
        num_stock_steps (int): Number of steps in the stock price grid.
        PDE_method (str): Method for solving the partial differential equation ('implicit' or 'explicit').

        Returnum_stock_steps:
        float: Option price.
        """

        if option_type not in ('EC', 'EP', 'AC', 'AP'):
            raise ValueError("Invalid option type")

        if PDE_method not in ('implicit', 'explicit'):
            raise ValueError("Invalid PDE method")

        self._set_grid(num_stock_steps)
        self._set_terminal_condition(option_type, max_stock_price, num_stock_steps)
        self._set_boundary_condition(option_type, max_stock_price)
        self._set_coefficient(PDE_method)
        self._set_matrix(PDE_method)
        self._solve(option_type, PDE_method)
        return self._interpolate(max_stock_price)

    def _set_grid(self, num_stock_steps):
        """Set up the grid for the finite difference method."""

        self.num_stock_steps = num_stock_steps
        self.grid = np.zeros(shape = (num_stock_steps + 1, self.num_steps + 1))

    def _set_terminal_condition(self, option_type, max_stock_price, num_stock_steps):
        """Set the terminal condition for the option."""

        stock_values = np.linspace(0, max_stock_price, num_stock_steps + 1)

        if 'P' in option_type:
            self.grid[:, -1] = np.maximum(self.strike - stock_values, 0)
        else:
            self.grid[:, -1] = np.maximum(stock_values - self.strike, 0)

    def _set_boundary_condition(self, option_type, max_stock_price):
        """Set the boundary conditionum_stock_steps for the option."""

        if 'P' in option_type:
            self.grid[0, :] = self.strike * np.exp(-self.interest_rate * self.deltaT * np.arange(self.num_steps + 1))
            self.grid[-1, :] = np.zeros(self.num_steps + 1)
        else:
            self.grid[0, :] = np.zeros(self.num_steps + 1)
            self.grid[-1, :] = max_stock_price - self.strike * np.exp(-self.interest_rate * self.deltaT * np.arange(self.num_steps + 1))

    def _set_coefficient(self, PDE_method):
        """Set the coefficients for the finite difference method."""

        drift = self.interest_rate * np.arange(1, self.num_stock_steps) * self.deltaT
        diffusion_square = (self.sigma * np.arange(1, self.num_stock_steps))**2 * self.deltaT

        self.a = 0.5 * (diffusion_square - drift)
        self.b = - diffusion_square if PDE_method == 'explicit' else - (diffusion_square + self.interest_rate * self.deltaT)
        self.c = 0.5 * (diffusion_square + drift)

    def _set_matrix(self, PDE_method):
        """Set up the matrix for solving the partial differential equation."""

        A = sp.diags([self.a[1:], self.b, self.c[:-1]], [-1, 0, 1],  format='csc')
        I = sp.eye(self.num_stock_steps - 1, format='csc')
        if PDE_method == 'explicit':
            self.M = (I + A) / (1 + self.interest_rate * self.deltaT)
        else:
            self.M = spsolve(I - A, np.eye(self.num_stock_steps - 1))

    def _solve(self, option_type, PDE_method):
        """Solve the partial differential equation."""

        for i in range(self.num_steps, 0, -1):
            U = self.M.dot(self.grid[1 : -1, i])
            if PDE_method == 'explicit':
                U[0] += self.grid[0, i] * self.a[0] / (1 + self.interest_rate * self.deltaT)
                U[-1] += self.grid[-1, i] * self.c[-1] / (1 + self.interest_rate * self.deltaT)
            else:
                U[0] -=  self.M[0, 0] * self.grid[0, i] * self.a[0] + self.M[0, -1] * self.grid[-1, i] * self.c[-1]
                U[-1] -= self.M[-1, 0] * self.grid[0, i] * self.a[0] + self.M[-1, -1] * self.grid[-1, i] * self.c[-1]
            self.grid[1:-1, i - 1] = [max(U[j - 1], self.grid[j, -1]) for j in range(1, self.num_stock_steps)] if 'A' in option_type else U

    def _interpolate(self, max_stock_price):
        stock_values = np.linspace(0, max_stock_price, self.num_stock_steps + 1)
        return np.interp(self.current_stock, stock_values, self.grid[:,0])
