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
from ..common.constants import TradingRule
from .. import __version__ # Make sure version is updated in src/__init__.py

# Definition of the argument parsing function
def parse_arguments():
    """Sets up argument parser using RichHelpFormatter and returns the parsed arguments."""

    # --- Main description ---
    main_description = textwrap.dedent("""
       Calculate and plot Shcherbyna Pressure Vector indicator using demo data,
       fetching from Yahoo Finance, reading from a CSV file, fetching from Polygon.io,
       or fetching from Binance. Allows choosing the plotting library.
       """)

    # --- Example epilog ---
    example_lines = [
        "[bold]EXAMPLES:[/bold]",
        "",
        "[bold cyan]─── Basic Usage ───[/bold cyan]",
        "  [dim]# Run with demo data (using fastest mode by default)[/dim]",
        "  [bold]python run_analysis.py demo[/bold]",
        "",
        "[bold cyan]─── Alternative Visualization ───[/bold cyan]",
        "  [dim]# Run with demo data using mplfinance for plotting[/dim]",
        "  [bold]python run_analysis.py demo -d mpl[/bold]",
        "",
        "[bold cyan]─── CSV Data Source ───[/bold cyan]",
        "  [dim]# Run using data from a specific CSV file (using fastest mode)[/dim]",
        "  [bold]python run_analysis.py csv --csv-file path/to/data.csv --point 0.01[/bold]",
        "",
        "[bold cyan]─── External API Data ───[/bold cyan]",
        "  [dim]# Fetch Polygon.io data and plot using mplfinance[/dim]",
        "  [bold]python run_analysis.py polygon --ticker EURUSD --interval D1 \\[/bold]",
        "  [bold]                         --start 2024-01-01 --end 2024-04-18 \\[/bold]",
        "  [bold]                         --point 0.00001 -d mpl[/bold]",
        "",
        "[bold cyan]─── Show Mode ───[/bold cyan]",
        "  [dim]# Show all cached YFinance files[/dim]",
        "  [bold]python run_analysis.py show yf[/bold]",
        "  [dim]# Search for YFinance files with 'aapl' and 'mn1' in the name[/dim]", 
        "  [bold]python run_analysis.py show yf aapl mn1[/bold]",
        "  [dim]# Search for Binance files with 'btc' in the name[/dim]",
        "  [bold]python run_analysis.py show binance btc[/bold]",
        "",
        # ... (keep other examples) ...
    ]
    examples_epilog = "\n".join(example_lines)

    #--- Argument Parser Setup ---
    parser = argparse.ArgumentParser(
        description=main_description,
        formatter_class=RichHelpFormatter,
        epilog=examples_epilog,
        add_help=False # Disable default help to add it to a specific group
    )

    # --- Required Arguments Group ---
    required_group = parser.add_argument_group('Required Arguments')
    required_group.add_argument('mode', choices=['demo', 'yfinance', 'yf', 'csv', 'polygon', 'binance', 'show'],
                                help="Operating mode: 'demo', 'yfinance'/'yf', 'csv', 'polygon', 'binance', 'show'.")

    # --- Show Mode Positional Arguments ---
    parser.add_argument('show_args', nargs='*', default=[],
                         help=argparse.SUPPRESS)  # Hide from help but collect positional args after 'mode'
    
    # --- Data Source Specific Options Group ---
    data_source_group = parser.add_argument_group('Data Source Options')
    # CSV options
    data_source_group.add_argument('--csv-file',
                                   help="Path to the input CSV file (required for 'csv' mode).")
    # API options (Yahoo Finance / Polygon.io / Binance)
    data_source_group.add_argument('-t', '--ticker',
                                   help="Ticker symbol (e.g., 'EURUSD=X' for yfinance; 'EURUSD', 'AAPL' for Polygon; 'BTCUSDT' for Binance). Required for 'yfinance', 'polygon', 'binance' modes.")
    data_source_group.add_argument('-i', '--interval', default='D1',
                                   help="Timeframe (e.g., 'M1', 'H1', 'D1', 'W1', 'MN1'). Default: D1.")
    # Point size argument
    data_source_group.add_argument('--point', type=float,
                                   help="Instrument point size (e.g., 0.00001 for EURUSD, 0.01 for stocks/crypto). Overrides yfinance estimation. Required for 'csv', 'polygon', 'binance' modes.")
    # History selection (period or start/end dates)
    history_group = data_source_group.add_mutually_exclusive_group()
    history_group.add_argument('--period',
                               help="History period for yfinance (e.g., '1mo', '1y'). Not used if --start/--end are provided. Not used by Polygon/Binance.")
    history_group.add_argument('--start', help="Start date (YYYY-MM-DD). Used by yfinance, polygon, binance.")
    # Make --end related only to --start (not period)
    data_source_group.add_argument('--end', help="End date (YYYY-MM-DD). Used by yfinance, polygon, binance. Required if --start is used.")
    
    
    # --- Indicator Options Group ---
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
    
    # --- Show Mode Options Group ---
    show_group = parser.add_argument_group('Show Mode Options')
    show_group.add_argument(
        '--source', default='yfinance',
        choices=['yfinance', 'yf', 'csv', 'polygon', 'binance'],
        help="Filter files by data source type. Can also use first positional argument after 'show'. Default: 'yfinance'."
    )
    show_group.add_argument(
        '--keywords', nargs='+', default=[],
        help="Additional keywords to filter files by (e.g., ticker symbol or date). Can also use remaining positional arguments after source. Default: show all files from the source."
    )
    show_group.add_argument(
        '--show-start', type=str, default=None,
        help="Start date/datetime (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) to filter data before calculation."
    )
    show_group.add_argument(
        '--show-end', type=str, default=None,
        help="End date/datetime (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) to filter data before calculation."
    )
    show_group.add_argument(
        '--show-rule', type=str, choices=all_rule_choices, default=None,
        help="Trading rule to apply for indicator calculation when showing a single file."
    )
    
    # --- Plotting Options Group ---
    plotting_group = parser.add_argument_group('Plotting Options')
    plotting_group.add_argument(
        '-d', '--draw',
        choices=['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl'],
        default='fastest',
        help="Choose plotting library: 'fastest' (Plotly+Dask+Datashader for extremely large datasets, default), 'fast' (Dask+Datashader+Bokeh), 'plotly'/'plt' (interactive HTML), or 'mplfinance'/'mpl' (static image)."
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

    # Handle positional arguments for 'show' mode
    if effective_mode == 'show':
        # Default to empty source if no args provided (will show help)
        if not args.show_args:
            args.source = ''
        else:
            # First positional argument is the source (if provided)
            args.source = args.show_args[0]
            # Normalize 'yf' to 'yfinance'
            if args.source == 'yf':
                args.source = 'yfinance'
        
            # Remaining arguments are keywords
            if len(args.show_args) > 1:
                args.keywords = args.show_args[1:]
    
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

    # Check point value if provided
    if args.point is not None and args.point <= 0:
        parser.error("argument --point: value must be positive")

    # Normalize source for show mode
    if effective_mode == 'show' and args.source == 'yf':
        args.source = 'yfinance'
    
    return args
