import numpy as np
from scipy.stats import norm

def black_scholes(option_type, current_stock, strike, period, volatility, interest_rate):
    """
    Calculate the price of European or Asian call or put options using the Black-Scholes formula.

    Parameters:
        option_type (str): Type of option ('EC' for European call, 'EP' for European put, 'AEC-A' for Asian call arithmetic average,
                           'AEP-A' for Asian put arithmetic average, 'AEC-G' for Asian call geometric average,
                           'AEP-G' for Asian put geometric average).
        current_stock (float): Current stock price.
        strike (float): Strike price.
        period (float): Time to maturity of the option.
        volatility (float): Volatility of the stock.
        interest_rate (float): Risk-free interest rate.

    Returns:
        float: Option price based on the Black-Scholes formula.
    """
    # Validate option type
    valid_option_types = ('EC', 'EP', 'AEC-A', 'AEP-A', 'AEC-G', 'AEP-G')
    if option_type not in valid_option_types:
        raise ValueError("Invalid option type")

    # Common calculations
    d1 = (np.log(current_stock / strike) + (interest_rate + volatility**2 / 2.) * period) / (volatility * np.sqrt(period))
    d2 = d1 - volatility * np.sqrt(period)
    discount_factor = np.exp(-interest_rate * period)

    # Calculate call and put prices for European options
    call_price = current_stock * norm.cdf(d1) - strike * discount_factor * norm.cdf(d2)
    put_price = strike * discount_factor * norm.cdf(-d2) - current_stock * norm.cdf(-d1)

    # Return the appropriate option price based on the option type
    if option_type == 'EC':
        return call_price
    elif option_type == 'EP':
        return put_price
    else:
        # Calculate prices for Asian options
        if '-G' in option_type:
            rho = (interest_rate - volatility ** 2 / 6.) / 2.
            sigma = volatility * np.sqrt(1. / 3.)
            asian_price = np.exp((rho - interest_rate) * period) * black_scholes('EC' if option_type == 'AEC-G' else 'EP', current_stock, strike, period, sigma, rho)
        else:
            M1 = (np.exp(interest_rate * period) - 1.) / (interest_rate * period) * current_stock
            M2 = 2. * np.exp((2 * interest_rate + volatility ** 2) * period) * current_stock ** 2 / ((interest_rate + volatility ** 2) * (2 * interest_rate + volatility ** 2) * period ** 2) \
                + 2 * current_stock ** 2 / (interest_rate * period ** 2) * (1. / (2. * interest_rate + volatility ** 2) - np.exp(interest_rate * period) / (interest_rate + volatility ** 2))
            F0 = M1
            sigma = np.sqrt(1. / period * np.log(M2 / M1**2))

            d1 = (np.log(F0 / strike + 1.e-20) + sigma ** 2 / 2. * period) / (sigma * np.sqrt(period))
            d2 = d1 - sigma * np.sqrt(period)

            asian_price = np.exp(-interest_rate * period) * (F0 * norm.cdf(d1) - strike * norm.cdf(d2)) if option_type == 'AEC-A' else np.exp(-interest_rate * period) * (strike * norm.cdf(-d2) - F0 * norm.cdf(-d1))

        return asian_price
