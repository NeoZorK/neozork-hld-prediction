# src/cli.py

"""
Command Line Interface setup using argparse and RichHelpFormatter for colored help.
Removed arguments related to LWMA, CORE1, etc.
All comments are in English.
"""

import argparse
# Import RichHelpFormatter from rich_argparse
try:
    # Recommended import path
    from rich_argparse import RichHelpFormatter
except ImportError:
    # Fallback for older rich versions or different installation methods
    try:
        from rich.argparse import RichHelpFormatter
    except ImportError:
        # If rich is not installed or rich-argparse is missing, fallback gracefully
        print("Warning: 'rich' or 'rich-argparse' not installed. Help formatting will be basic.")
        print("Install with: pip install rich")
        # Use the standard formatter as a fallback
        RichHelpFormatter = argparse.ArgumentDefaultsHelpFormatter


# Use relative imports for constants and version within the src package
# Import the updated TradingRule enum
from .constants import TradingRule
from . import __version__

def parse_arguments():
    """Sets up argument parser using RichHelpFormatter and returns the parsed arguments."""
    # Use RichHelpFormatter for colored and formatted help output
    parser = argparse.ArgumentParser(
        description="Calculate and plot Shcherbyna Pressure Vector indicator using demo data or fetching from Yahoo Finance.",
        formatter_class=RichHelpFormatter # <--- USE RICH FORMATTER
    )

    # --- Arguments ---
    # The mode argument determines the data source
    parser.add_argument('mode', choices=['demo', 'yfinance', 'yf'],
                        help="Operating mode: 'demo' uses built-in data, 'yfinance' or 'yf' fetches data.")

    # --- Yahoo Finance Options ---
    # Grouping arguments for better organization in help message
    yf_group = parser.add_argument_group('Yahoo Finance Options (used if mode=yfinance/yf)')
    # Added rich markup [cyan]...[/] for examples in help strings
    yf_group.add_argument('-t', '--ticker',
                          help="Ticker symbol for yfinance (e.g., [cyan]'EURUSD=X'[/], [cyan]'BTC-USD'[/], [cyan]'AAPL'[/]). Required for yfinance/yf mode.")
    # Default value 'D1' will be shown by the formatter
    yf_group.add_argument('-i', '--interval', default='D1',
                          help="Timeframe (e.g., [cyan]'M1', 'H1', 'D1', 'W1', 'MN1'[/]). Will be mapped to yfinance interval.")
    yf_group.add_argument('--point', type=float,
                          help="Instrument point size (e.g., [cyan]0.00001[/]). Overrides automatic estimation. Crucial for accuracy.")

    # --- History Selection ---
    # Mutually exclusive group ensures only period or start/end is used
    history_group = yf_group.add_mutually_exclusive_group()
    # Default value '1y' will be shown by the formatter
    history_group.add_argument('-p', '--period', default='1y',
                               help="History period for yfinance (e.g., [cyan]'1mo', '6mo', '1y', '5y', 'max'[/]).")
    history_group.add_argument('--start', help="Start date for yfinance data (YYYY-MM-DD). Use with [bold]--end[/].")
    # --end is defined outside the exclusive group but logically belongs with --start
    yf_group.add_argument('--end', help="End date for yfinance data (YYYY-MM-DD). Use with [bold]--start[/].")

    # --- Indicator Options (Simplified) ---
    # Another group for indicator parameters
    indicator_group = parser.add_argument_group('Indicator Options')
    # Get available rules dynamically AFTER updating TradingRule enum
    # These are the only rules left after the removal step
    rule_choices = list(TradingRule.__members__.keys())
    # Default value PV_HighLow.name will be shown by the formatter
    indicator_group.add_argument('--rule', default=TradingRule.Predict_High_Low_Direction.name, choices=rule_choices,
                                 help="Trading rule to apply.")

    # Arguments for core_back, strength_back, limit, pv_tp_multy, reverse are removed

    # --- Version ---
    # Standard version argument, using rich markup for the version string output
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s [yellow]{__version__}[/]', # Added color markup
                        help="Show program's version number and exit.")

    # Parse and return arguments
    args = parser.parse_args()
    return args