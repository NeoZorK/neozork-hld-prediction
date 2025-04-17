# src/cli.py

"""
Command Line Interface setup using argparse and RichHelpFormatter for colored help.
Removed arguments related to LWMA, CORE1, etc.
All comments are in English.
"""
import argparse
import textwrap # Import textwrap for cleaner epilog formatting

try:
    from rich_argparse import RichHelpFormatter
except ImportError:
    try:
        from rich.argparse import RichHelpFormatter
    except ImportError:
        # If rich is not installed or rich-argparse is missing, fallback gracefully
        print("Warning: 'rich' or 'rich-argparse' not installed. Help formatting will be basic.")
        print("Install with: pip install rich")
        # Use the standard formatter as a fallback
        RichHelpFormatter = argparse.ArgumentDefaultsHelpFormatter

# Use relative imports for constants and version within the src package
from ..common.constants import TradingRule
from .. import __version__

def parse_arguments():
    """Sets up argument parser using RichHelpFormatter and returns the parsed arguments."""

    # --- Define examples with explicit newlines ---
    # Используем f-string и textwrap.dedent для чистоты, добавляя \n в конце каждой строки примера
    examples = textwrap.dedent(f"""
        Examples:
          # Run with demo data and default rule
          python run_analysis.py demo\n
          # Run with demo data and Pressure_Vector rule
          python run_analysis.py demo --rule PV\n
          # Fetch 1 year of Daily EUR/USD data, estimate point size, use PV_HighLow rule
          python run_analysis.py yf --ticker "EURUSD=X" --period 1y --interval D1 --rule PV_HighLow\n
          # Fetch AAPL data for a specific date range, H1 interval, explicitly set point size
          python run_analysis.py yfinance --ticker AAPL --interval H1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule PHLD\n
        """)


    # Use RichHelpFormatter for colored and formatted help output
    parser = argparse.ArgumentParser(
        description="Calculate and plot Shcherbyna Pressure Vector indicator using demo data or fetching from Yahoo Finance.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=examples # <--- USE RICH FORMATTER
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
    indicator_group = parser.add_argument_group('Indicator Options')

    # Get available rules dynamically AFTER updating TradingRule enum
    # These are the only rules left after the removal step
    #rule_choices = list(TradingRule.__members__.keys())

    # Map rule choices to their corresponding TradingRule enum values
    rule_aliases = {
        'PHLD': 'Predict_High_Low_Direction',
        'PV': 'Pressure_Vector',
        'SR': 'Support_Resistants'
    }

    # Add aliases to the rule choices
    rule_names = list(TradingRule.__members__.keys())

    # Create a list of all rule choices including aliases
    all_rule_choices = rule_names + list(rule_aliases.keys())

    # Set default rule to Predict_High_Low_Direction
    default_rule_name = TradingRule.Predict_High_Low_Direction.name

    # Add argument for rule selection
    indicator_group.add_argument(
        '--rule',
        default=default_rule_name,
        choices=all_rule_choices,  # use all_rule_choices
        help=f"Trading rule to apply. Default: {default_rule_name}. "
             f"Aliases: PHLD=Predict_High_Low_Direction."  # add alias info
    )

    # --- Version ---
    # Standard version argument, using rich markup for the version string output
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s [yellow]{__version__}[/]', # Added color markup
                        help="Show program's version number and exit.")

    # Parse and return arguments
    args = parser.parse_args()
    return args