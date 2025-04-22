# src/cli/cli.py

"""
Command Line Interface setup using argparse and RichHelpFormatter for colored help.
All comments are in English.
"""
import argparse
import textwrap
import sys # Import sys for exit

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
from ..common.constants import TradingRule, VALID_DATA_SOURCES # Import VALID_DATA_SOURCES
from .. import __version__ # Make sure version is updated in src/__init__.py

# Definition of the argument parsing function
def parse_arguments():
    """Sets up argument parser using RichHelpFormatter and returns the parsed arguments."""

    # --- Main description ---
    main_description = textwrap.dedent("""
       Calculate and plot Shcherbyna Pressure Vector indicator using various data sources
       (demo, yfinance, csv, polygon, binance) or show information about cached data.
       Allows choosing the plotting library.
       """)

    # --- Example epilog ---
    example_lines = [
        "[bold]Examples:[/bold]",
        "",
        "  [dim]# Run analysis with demo data (default plotly plot)[/]",
        "  [bold cyan]python run_analysis.py demo[/]",
        "",
        "  [dim]# Run analysis using data from a specific CSV file[/]",
        "  [bold cyan]python run_analysis.py csv --csv-file path/to/data.csv --point 0.01[/]",
        "",
        "  [dim]# Fetch Polygon.io data and plot using mplfinance[/]",
        "  [bold cyan]python run_analysis.py polygon --ticker EURUSD --interval D1 --start 2024-01-01 --end 2024-04-18 --point 0.00001 -d mpl[/]",
        "",
        "  [dim]# List all cached files from Binance[/]",
        "  [bold cyan]python run_analysis.py show --source binance[/]",
        "",
        "  [dim]# List cached yfinance files containing 'MN1'[/]",
        "  [bold cyan]python run_analysis.py show --source yf --search MN1[/]",
        "",
        "  [dim]# Show info for cached Polygon file matching 'GBPUSD' and 'MN1'[/]",
        "  [bold cyan]python run_analysis.py show --source polygon --search GBPUSD MN1[/]",
        "",
        "  [dim]# Plot specific cached yfinance file (requires --point)[/]",
        "  [bold cyan]python run_analysis.py show --source yf --search AAPL MN1 --rule Pressure_Vector --point 0.01 --draw plt[/]",
        # ... (keep other relevant examples) ...
    ]
    examples_epilog = "\n".join(example_lines)

    #--- Argument Parser Setup ---
    parser = argparse.ArgumentParser(
        description=main_description,
        formatter_class=RichHelpFormatter,
        epilog=examples_epilog,
        add_help=False # Disable default help to add it to a specific group
    )

    # --- Mode Selection ---
    # Combine all modes including 'show'
    all_modes = ['demo', 'yfinance', 'yf', 'csv', 'polygon', 'binance', 'show']
    parser.add_argument('mode', choices=all_modes,
                        help=f"Operating mode: {', '.join(all_modes)}.")

    # --- Analysis Mode Options (demo, yf, csv, polygon, binance) ---
    analysis_group = parser.add_argument_group('Analysis Mode Options (demo, yf, csv, polygon, binance)')
    # CSV options
    analysis_group.add_argument('--csv-file',
                                help="Path to the input CSV file (required for 'csv' mode).")
    # API options (Yahoo Finance / Polygon.io / Binance)
    analysis_group.add_argument('-t', '--ticker',
                                help="Ticker symbol (e.g., 'EURUSD=X' for yfinance; 'EURUSD', 'AAPL' for Polygon; 'BTCUSDT' for Binance). Required for 'yfinance', 'polygon', 'binance' modes.")
    analysis_group.add_argument('-i', '--interval', default='D1',
                                help="Timeframe (e.g., 'M1', 'H1', 'D1', 'W1', 'MN1'). Default: D1.")
    # History selection (period or start/end dates)
    history_group = analysis_group.add_mutually_exclusive_group()
    history_group.add_argument('--period',
                               help="History period for yfinance (e.g., '1mo', '1y'). Not used if --start/--end are provided. Not used by Polygon/Binance.")
    history_group.add_argument('--start', help="Start date (YYYY-MM-DD). Used by yfinance, polygon, binance.")
    # Make --end related only to --start (not period)
    analysis_group.add_argument('--end', help="End date (YYYY-MM-DD). Used by yfinance, polygon, binance. Required if --start is used.")


    # --- Show Mode Options ---
    show_group = parser.add_argument_group('Show Mode Options (show)')
    show_group.add_argument('--source', choices=VALID_DATA_SOURCES + ['csv'], # Allow 'csv' for CSV cache_manager
                            help="Specify the data source cache_manager to search ('yf', 'polygon', 'binance', 'csv'). Required for 'show' mode.")
    show_group.add_argument('--search', nargs='*', # 0 or more arguments
                            help="Search terms (e.g., ticker, interval) to filter cached files. If omitted, lists all files for the source.")

    # --- Common Options (Used by Analysis and Show modes) ---
    common_group = parser.add_argument_group('Common Options')
    # Point size argument (Required for csv, polygon, binance in analysis mode; REQUIRED for plotting in show mode)
    common_group.add_argument('--point', type=float,
                              help="Instrument point size (e.g., 0.00001 for EURUSD, 0.01 for stocks/crypto). Overrides yfinance estimation. Required for 'csv', 'polygon', 'binance' analysis modes. Required for plotting in 'show' mode.")
    # Indicator rule
    rule_aliases_map = {'PHLD': 'Predict_High_Low_Direction', 'PV': 'Pressure_Vector', 'SR': 'Support_Resistants'}
    rule_names = list(TradingRule.__members__.keys())
    all_rule_choices = rule_names + list(rule_aliases_map.keys())
    default_rule_name = TradingRule.Predict_High_Low_Direction.name
    common_group.add_argument(
        '--rule',
        default=default_rule_name,
        choices=all_rule_choices,
        help=f"Trading rule to apply. Default: {default_rule_name}. Used in analysis modes and optionally in 'show' mode for plotting."
             f" Aliases: PHLD=Predict_High_Low_Direction, PV=Pressure_Vector, SR=Support_Resistants."
    )
    # Plotting library choice
    common_group.add_argument(
        '-d', '--draw',
        choices=['plotly', 'plt', 'mplfinance', 'mpl'],
        default='plotly',
        help="Choose plotting library: 'plotly'/'plt' (interactive HTML) or 'mplfinance'/'mpl' (static image). Default: plotly. Used in analysis modes and optionally in 'show' mode."
    )

    # --- Other Options Group ---
    other_group = parser.add_argument_group('Other Options')
    other_group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                              help='Show this help message and exit.')
    other_group.add_argument('--version', action='version',
                             version=f'%(prog)s [yellow]{__version__}[/]',
                             help="Show program's version number and exit.")

    # --- Parse Arguments ---
    try:
        args = parser.parse_args()
    except SystemExit as e:
         if e.code != 0:
              print(f"Argument parsing error (Code: {e.code}). Exiting.", file=sys.stderr)
         sys.exit(e.code)


    # --- Post-parsing validation ---
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    # Validation for Analysis Modes
    if effective_mode in ['demo', 'yfinance', 'csv', 'polygon', 'binance']:
        # Check requirements for CSV mode
        if effective_mode == 'csv':
            if not args.csv_file:
                parser.error("argument --csv-file is required when mode is 'csv'")
            if args.point is None:
                parser.error("argument --point is required when mode is 'csv'")

        # Check requirements for API modes (yfinance, polygon, binance)
        api_modes = ['yfinance', 'polygon', 'binance']
        if effective_mode in api_modes:
            if not args.ticker:
                parser.error(f"argument --ticker is required when mode is '{effective_mode}'")

        # Check date/period requirements for yfinance
        if effective_mode == 'yfinance':
             if not args.period and not (args.start and args.end):
                 parser.error("for yfinance mode, provide either --period OR both --start and --end")
             if args.start and not args.end:
                 parser.error("argument --end is required when --start is provided for yfinance mode")
             if args.end and not args.start:
                 parser.error("argument --start is required when --end is provided for yfinance mode")
             if args.period and (args.start or args.end):
                  parser.error("cannot use --period together with --start or --end for yfinance mode")

        # Check requirements for Polygon & Binance
        polygon_binance_modes = ['polygon', 'binance']
        if effective_mode in polygon_binance_modes:
            if not args.start or not args.end:
                 parser.error(f"arguments --start and --end are required when mode is '{effective_mode}'")
            if args.point is None:
                parser.error(f"argument --point is required when mode is '{effective_mode}'")

    # Validation for Show Mode
    elif effective_mode == 'show':
        if not args.source:
            parser.error("argument --source is required when mode is 'show'")
        # If rule is specified (implying plotting), point must also be specified
        if args.rule != default_rule_name or args.draw != 'plotly': # Check if plotting is likely intended
             # A more robust check might be needed if default rule/draw is used for plotting
             # For now, assume if rule is specified, plotting is intended.
             # OR better: check if search terms are specific enough to identify ONE file?
             # Let's require --point explicitly if plotting is intended from cache_manager for now.
             # We'll refine this logic in run_analysis.py based on whether a single file is found.
             pass # Defer point check to main script logic

    # Check point value if provided
    if args.point is not None and args.point <= 0:
        parser.error("argument --point: value must be positive")

    # Normalize source 'yf' to 'yfinance' if needed for consistency
    if hasattr(args, 'source') and args.source == 'yf':
        args.source = 'yfinance'

    return args

