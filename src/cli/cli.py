# src/cli.py # MODIFIED

"""
Command Line Interface setup using argparse and RichHelpFormatter for colored help.
All comments are in English.
"""
import argparse
import textwrap


try:
    # Try importing from rich_argparse first
    from rich_argparse import RichHelpFormatter
except ImportError:
    try:
        # Fallback to rich.argparse if rich_argparse is not installed
        from rich.argparse import RichHelpFormatter
    except ImportError:
        # Fallback to standard argparse formatter if rich is not available
        print("Warning: 'rich' or 'rich-argparse' not installed. Help formatting will be basic.")
        print("Install with: pip install rich")
        RichHelpFormatter = argparse.ArgumentDefaultsHelpFormatter

# Use relative imports for constants and version within the src package
from ..common.constants import TradingRule
from .. import __version__

# Definition of the argument parsing function
def parse_arguments():
    """Sets up argument parser using RichHelpFormatter and returns the parsed arguments."""

    # --- Main description ---
    # Updated description to include all data sources
    main_description = textwrap.dedent("""
       Calculate and plot Shcherbyna Pressure Vector indicator using demo data,
       fetching from Yahoo Finance, reading from a CSV file, or fetching from Polygon.io.
       """) # Updated description

    # --- Example epilog ---
    # Added examples for CSV and Polygon modes
    example_lines = [
        "[bold]Examples:[/bold]",
        "",
        "  [dim]# Run with demo data and default rule[/]",
        "  [bold cyan]python run_analysis.py demo[/]",
        "",
        "  [dim]# Run with demo data and Pressure_Vector rule[/]",
        "  [bold cyan]python run_analysis.py demo --rule PV[/]",
        "",
         "  [dim]# Run using data from a specific CSV file[/]",
         "  [bold cyan]python run_analysis.py csv --csv-file path/to/data.csv --point 0.01[/]",
         "",
         "  [dim]# Fetch Polygon.io data for Forex EUR/USD, D1 interval, specific dates[/]",
         "  [dim]# (Requires POLYGON_API_KEY in .env and --point specified)[/]",
         "  [bold cyan]python run_analysis.py polygon --ticker EURUSD --interval D1 --start 2024-01-01 --end 2024-04-18 --point 0.00001[/]", # Added Polygon example
         "",
        "  [dim]# Fetch Yahoo Finance data for 1 year of Daily EUR/USD, estimate point size, use PV_HighLow rule[/]",
        "  [bold cyan]python run_analysis.py yf --ticker \"EURUSD=X\" --period 1y --interval D1 --rule PV_HighLow[/]",
        "",
        "  [dim]# Fetch Yahoo Finance data for AAPL, H1 interval, specific date range, explicitly set point size[/]",
        "  [bold cyan]python run_analysis.py yfinance --ticker AAPL --interval H1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule PHLD[/]"
    ]
    examples_epilog = "\n".join(example_lines)

    #--- Argument Parser Setup ---
    # Initializes the parser with description, formatter, and epilog.
    parser = argparse.ArgumentParser(
        description=main_description,
        formatter_class=RichHelpFormatter,
        epilog=examples_epilog
    )

    # --- Main Mode Argument ---
    # Updated choices to include 'polygon'
    parser.add_argument('mode', choices=['demo', 'yfinance', 'yf', 'csv', 'polygon'], # ADDED 'polygon'
                        help="Operating mode: 'demo', 'yfinance'/'yf', 'csv', 'polygon'.")

    # --- Data Source Specific Options ---
    # Group for CSV options
    csv_group = parser.add_argument_group('CSV Options (used if mode=csv)')
    csv_group.add_argument('--csv-file',
                         help="Path to the input CSV file (required for csv mode).")

    # Group for Yahoo Finance options
    # Note: Ticker, Interval, Start/End arguments will also be used by Polygon mode
    yf_group = parser.add_argument_group('Yahoo Finance / Polygon.io Options')
    yf_group.add_argument('-t', '--ticker',
                          help="Ticker symbol (e.g., 'EURUSD=X', 'AAPL' for yfinance; 'EURUSD', 'AAPL' for Polygon). Required for yfinance/polygon modes.")
    yf_group.add_argument('-i', '--interval', default='D1',
                          help="Timeframe (e.g., 'M1', 'H1', 'D1', 'W1', 'MN1').")
    # Point size argument is now relevant for csv, yfinance (override), and polygon modes
    yf_group.add_argument('--point', type=float,
                          help="Instrument point size (e.g., 0.00001 for EURUSD, 0.01 for AAPL/XAUUSD). Overrides yfinance estimation. Required for csv/polygon modes.")

    # Group for history selection (period or start/end dates) - Primarily for yfinance
    # Polygon fetch function currently expects start/end dates.
    history_group = yf_group.add_mutually_exclusive_group()
    history_group.add_argument('-p', '--period', default='1y',
                               help="History period for yfinance (e.g., '1mo', '1y'). Not directly used by Polygon fetch.")
    history_group.add_argument('--start', help="Start date (YYYY-MM-DD). Used by yfinance and polygon.")
    yf_group.add_argument('--end', help="End date (YYYY-MM-DD). Used by yfinance and polygon.")


    # --- Indicator Options ---
    indicator_group = parser.add_argument_group('Indicator Options')
    rule_aliases_map = {'PHLD': 'Predict_High_Low_Direction', 'PV': 'Pressure_Vector', 'SR': 'Support_Resistants'}
    rule_names = list(TradingRule.__members__.keys())
    all_rule_choices = rule_names + list(rule_aliases_map.keys())
    default_rule_name = TradingRule.Predict_High_Low_Direction.name
    indicator_group.add_argument(
        '--rule',
        default=default_rule_name,
        choices=all_rule_choices,
        help=f"Trading rule to apply. Default: {default_rule_name}. "
             f"Aliases: PHLD=Predict_High_Low_Direction, PV=Pressure_Vector, SR=Support_Resistants."
    )

    # --- Version ---
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s [yellow]{__version__}[/]',
                        help="Show program's version number and exit.")

    # Parse arguments
    args = parser.parse_args()

    # --- Post-parsing validation ---
    # Check requirements for CSV mode
    if args.mode == 'csv' and not args.csv_file:
        parser.error("argument --csv-file is required when mode is 'csv'")
    # Add checks for other modes if needed (e.g., ticker for yfinance/polygon)
    if args.mode in ['yfinance', 'yf', 'polygon'] and not args.ticker:
         parser.error("argument --ticker is required when mode is 'yfinance' or 'polygon'")
    # Check date requirements for Polygon (and yfinance if using start/end)
    if args.mode == 'polygon' and (not args.start or not args.end):
         parser.error("arguments --start and --end are required when mode is 'polygon'")
    if args.mode in ['yfinance', 'yf'] and args.start and not args.end:
         # Yfinance can work with only start (goes to present), but let's require both if start is given
         # Or modify fetch_yfinance to handle only start better if needed
         parser.error("argument --end is required when --start is provided for yfinance mode")
    if args.mode in ['yfinance', 'yf'] and args.end and not args.start:
         parser.error("argument --start is required when --end is provided for yfinance mode")

    # Point size check for csv/polygon might be better handled in get_point_size function

    return args