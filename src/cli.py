# src/cli.py

"""
Command Line Interface setup using argparse.
All comments are in English.
"""

import argparse
# Use relative imports for constants and version within the src package
from .constants import TradingRule
from . import __version__

def parse_arguments():
    """Sets up argument parser and returns the parsed arguments."""
    parser = argparse.ArgumentParser(
        description="Calculate and plot Shcherbyna Pressure Vector indicator using demo data or fetching from Yahoo Finance.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # --- Arguments ---
    parser.add_argument('mode', choices=['demo', 'yfinance', 'yf'],
                        help="Operating mode: 'demo' uses built-in data, 'yfinance' or 'yf' fetches data.")

    # --- Yahoo Finance Options ---
    yf_group = parser.add_argument_group('Yahoo Finance Options (used if mode=yfinance/yf)')
    yf_group.add_argument('-t', '--ticker',
                          help="Ticker symbol for yfinance (e.g., 'EURUSD=X', 'BTC-USD', 'AAPL'). Required for yfinance/yf mode.")
    yf_group.add_argument('-i', '--interval', default='D1',
                          help="Timeframe (e.g., 'M1', 'H1', 'D1', 'W1', 'MN1'). Will be mapped to yfinance interval.")
    yf_group.add_argument('--point', type=float,
                          help="Instrument point size (e.g., 0.00001). Overrides automatic estimation. Crucial for accuracy.")

    # --- History Selection ---
    history_group = yf_group.add_mutually_exclusive_group()
    history_group.add_argument('-p', '--period', default='1y',
                               help="History period for yfinance (e.g., '1mo', '6mo', '1y', '5y', 'max').")
    history_group.add_argument('--start', help="Start date for yfinance data (YYYY-MM-DD). Use with --end.")
    yf_group.add_argument('--end', help="End date for yfinance data (YYYY-MM-DD). Use with --start.")

    # --- Indicator Options ---
    indicator_group = parser.add_argument_group('Indicator Options')
    # Dynamically create choices from TradingRule enum members
    rule_choices = list(TradingRule.__members__.keys())
    indicator_group.add_argument('--rule', default=TradingRule.PV_HighLow.name, choices=rule_choices,
                                 help="Trading rule to apply.")
    indicator_group.add_argument('--core_back', type=int, default=5,
                                 help="Period for CORE1 calculation.")
    indicator_group.add_argument('--strength_back', type=int, default=3,
                                 help="Period for LWMA calculation.")
    indicator_group.add_argument('--limit', type=int, default=1000,
                                 help="Limit for Tick_Volume_Limit rule.")
    indicator_group.add_argument('--pv_tp_multy', type=int, default=10,
                                 help="Multiplier for PV TakeProfit rules.")
    indicator_group.add_argument('--reverse', action='store_true', default=False,
                                 help="Reverse the final signals.")

    # --- Version ---
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    # Parse and return arguments
    args = parser.parse_args()
    return args