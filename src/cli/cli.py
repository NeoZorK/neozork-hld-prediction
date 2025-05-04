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
    from rich.console import Console
except ImportError:
    try:
        # Fallback to rich.argparse if rich_argparse is not installed
        from rich.argparse import RichHelpFormatter
        from rich.console import Console
    except ImportError:
        # Fallback to standard argparse formatter if rich is not available
        print("Warning: 'rich' or 'rich-argparse' not installed. Help formatting will be basic.")
        print("Install with: pip install rich")
        RichHelpFormatter = argparse.ArgumentDefaultsHelpFormatter
        Console = None

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
    examples_epilog = None  # Убираем epilog

    #--- Argument Parser Setup ---
    parser = argparse.ArgumentParser(
        description=main_description,
        formatter_class=RichHelpFormatter,
        epilog=None,  # epilog убран
        add_help=False # Disable default help to add it to a specific group
    )

    # --- Examples Option ---
    parser.add_argument(
        '--examples',
        action='store_true',
        help='Show usage examples and exit.'
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
        # If no arguments provided, show help
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(0)
        # Если пользователь запросил примеры
        if '--examples' in sys.argv:
            if 'Console' in globals() and Console is not None:
                console = Console()
                console.print("[bold cyan]\nEXAMPLES (run: python run_analysis.py --examples):[/bold cyan]\n")
                console.print("[bold]1. DEMO DATA MODES[/bold]")
                console.print("[dim]# Run with demo data (default rule)[/dim]\n[bold green]python run_analysis.py demo[/bold green]")
                console.print("[dim]# Run with demo data using mplfinance[/dim]\n[bold green]python run_analysis.py demo -d mpl[/bold green]")
                console.print("[dim]# Run with demo data and PV_HighLow rule[/dim]\n[bold green]python run_analysis.py demo --rule PV_HighLow[/bold green]")
                console.print("[dim]# Run with demo data and PHLD rule, plotly backend[/dim]\n[bold green]python run_analysis.py demo --rule PHLD -d plotly[/bold green]\n")

                console.print("[bold]2. CSV FILE MODES[/bold]")
                console.print("[dim]# Basic CSV mode[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01[/bold green]")
                console.print("[dim]# CSV with Support_Resistants rule[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01 --rule SR[/bold green]")
                console.print("[dim]# CSV with mplfinance backend[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01 -d mplfinance[/bold green]")
                console.print("[dim]# CSV with PV rule, fastest backend[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV --draw fastest[/bold green]\n")

                console.print("[bold]3. YAHOO FINANCE (YF) MODES[/bold]")
                console.print("[dim]# EURUSD=X, 1mo, point size[/dim]\n[bold green]python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001[/bold green]")
                console.print("[dim]# AAPL, 6mo, point size[/dim]\n[bold green]python run_analysis.py yfinance -t AAPL --period 6mo --point 0.01[/bold green]")
                console.print("[dim]# BTC-USD, date range, point size[/dim]\n[bold green]python run_analysis.py yf -t BTC-USD --start 2023-01-01 --end 2023-12-31 --point 0.01[/bold green]")
                console.print("[dim]# EURUSD=X, date range, mpl backend[/dim]\n[bold green]python run_analysis.py yf -t EURUSD=X --start 2024-01-01 --end 2024-04-18 --point 0.00001 -d mpl[/bold green]")
                console.print("[dim]# AAPL, 1y, Support_Resistants rule[/dim]\n[bold green]python run_analysis.py yf -t AAPL --period 1y --rule SR[/bold green]\n")

                console.print("[bold]4. POLYGON.IO MODES[/bold]")
                console.print("[dim]# AAPL, D1, date range, point size[/dim]\n[bold green]python run_analysis.py polygon --ticker AAPL --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01[/bold green]")
                console.print("[dim]# EURUSD, H1, date range, PV rule[/dim]\n[bold green]python run_analysis.py polygon --ticker EURUSD --interval H1 --start 2022-01-01 --end 2022-06-01 --point 0.00001 --rule PV[/bold green]\n")

                console.print("[bold]5. BINANCE MODES[/bold]")
                console.print("[dim]# BTCUSDT, H1, date range, point size[/dim]\n[bold green]python run_analysis.py binance --ticker BTCUSDT --interval H1 --start 2024-01-01 --end 2024-04-18 --point 0.01[/bold green]")
                console.print("[dim]# ETHUSDT, D1, date range, Support_Resistants rule[/dim]\n[bold green]python run_analysis.py binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule SR[/bold green]\n")

                console.print("[bold]6. SHOW MODE (CACHE/FILES)[/bold]")
                console.print("[dim]# Show all YFinance files[/dim]\n[bold green]python run_analysis.py show yf[/bold green]")
                console.print("[dim]# Show YFinance files with 'aapl' and 'mn1' in name[/dim]\n[bold green]python run_analysis.py show yf aapl mn1[/bold green]")
                console.print("[dim]# Show Binance files with 'btc' in name[/dim]\n[bold green]python run_analysis.py show binance btc[/bold green]")
                console.print("[dim]# Show CSV files with EURUSD MN1[/dim]\n[bold green]python run_analysis.py show csv EURUSD MN1[/bold green]")
                console.print("[dim]# Show Polygon files with AAPL 2023[/dim]\n[bold green]python run_analysis.py show polygon AAPL 2023[/bold green]")
                console.print("[dim]# Show YF files with PV rule[/dim]\n[bold green]python run_analysis.py show yf --show-rule PV[/bold green]")
                console.print("[dim]# Show YF files for date range[/dim]\n[bold green]python run_analysis.py show yf --show-start 2023-01-01 --show-end 2023-12-31[/bold green]\n")

                console.print("[bold]7. ADVANCED/EDGE CASES[/bold]")
                console.print("[dim]# CSV, PHLD rule, plotly backend[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PHLD --draw plotly[/bold green]")
                console.print("[dim]# YF, PV rule, fastest backend[/dim]\n[bold green]python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 --rule PV --draw fastest[/bold green]")
                console.print("[dim]# Polygon, SR rule, mpl backend[/dim]\n[bold green]python run_analysis.py polygon --ticker EURUSD --interval D1 --start 2022-01-01 --end 2022-12-31 --point 0.00001 --rule SR --draw mpl[/bold green]")
                console.print("[dim]# Binance, M1, PHLD rule[/dim]\n[bold green]python run_analysis.py binance --ticker BTCUSDT --interval M1 --start 2023-01-01 --end 2023-01-31 --point 0.01 --rule PHLD[/bold green]\n")

                console.print("[bold]8. HELP, VERSION, EXAMPLES[/bold]")
                console.print("[dim]# Show help, version, or all examples[/dim]")
                console.print("[bold green]python run_analysis.py -h[/bold green]")
                console.print("[bold green]python run_analysis.py --version[/bold green]")
                console.print("[bold green]python run_analysis.py --examples[/bold green]\n")

                console.print("[bold]9. CACHE/DEBUG[/bold]")
                console.print("[dim]# Remove cache and rerun[/dim]")
                console.print("[bold green]rm data/cache/csv_converted/*.parquet[/bold green]")
                console.print("[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01[/bold green]\n")

                console.print("[bold]10. ERROR CASES (will show error/help)[/bold]")
                console.print("[dim]# Missing required arguments[/dim]")
                console.print("[bold green]python run_analysis.py csv --csv-file data.csv[/bold green]   [dim]# (missing --point)[/dim]")
                console.print("[bold green]python run_analysis.py yf -t EURUSD=X[/bold green]            [dim]# (missing --period or --start/--end)[/dim]\n")

                console.print("[bold yellow]Note:[/bold yellow] For all API modes (yfinance, polygon, binance), the --point parameter is required to specify the instrument's point size (e.g., 0.00001 for EURUSD, 0.01 for stocks/crypto).\n")
                console.print("[yellow]- Use -d/--draw to select plotting backend: fastest, fast, plotly, mplfinance, etc.")
                console.print("- Use --rule to select trading rule: PV_HighLow, Support_Resistants, Pressure_Vector, Predict_High_Low_Direction, PHLD, PV, SR.")
                console.print("- SHOW mode allows filtering cached files by source, keywords, date, and rule.")
                console.print("- For more details, see README.md or run with -h for full help.\n")
            else:
                print("""
EXAMPLES (run: python run_analysis.py --examples):

  # 1. DEMO DATA MODES
  python run_analysis.py demo
  python run_analysis.py demo -d mpl
  python run_analysis.py demo --rule PV_HighLow
  python run_analysis.py demo --rule PHLD -d plotly

  # 2. CSV FILE MODES
  python run_analysis.py csv --csv-file data.csv --point 0.01
  python run_analysis.py csv --csv-file data.csv --point 0.01 --rule SR
  python run_analysis.py csv --csv-file data.csv --point 0.01 -d mplfinance
  python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV --draw fastest

  # 3. YAHOO FINANCE (YF) MODES
  python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001
  python run_analysis.py yfinance -t AAPL --period 6mo --point 0.01
  python run_analysis.py yf -t BTC-USD --start 2023-01-01 --end 2023-12-31 --point 0.01
  python run_analysis.py yf -t EURUSD=X --start 2024-01-01 --end 2024-04-18 --point 0.00001 -d mpl
  python run_analysis.py yf -t AAPL --period 1y --rule SR

  # 4. POLYGON.IO MODES
  python run_analysis.py polygon --ticker AAPL --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01
  python run_analysis.py polygon --ticker EURUSD --interval H1 --start 2022-01-01 --end 2022-06-01 --point 0.00001 --rule PV

  # 5. BINANCE MODES
  python run_analysis.py binance --ticker BTCUSDT --interval H1 --start 2024-01-01 --end 2024-04-18 --point 0.01
  python run_analysis.py binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule SR

  # 6. SHOW MODE (CACHE/FILES)
  python run_analysis.py show yf
  python run_analysis.py show yf aapl mn1
  python run_analysis.py show binance btc
  python run_analysis.py show csv EURUSD MN1
  python run_analysis.py show polygon AAPL 2023
  python run_analysis.py show yf --show-rule PV
  python run_analysis.py show yf --show-start 2023-01-01 --show-end 2023-12-31

  # 7. ADVANCED/EDGE CASES
  python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PHLD --draw plotly
  python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 --rule PV --draw fastest
  python run_analysis.py polygon --ticker EURUSD --interval D1 --start 2022-01-01 --end 2022-12-31 --point 0.00001 --rule SR --draw mpl
  python run_analysis.py binance --ticker BTCUSDT --interval M1 --start 2023-01-01 --end 2023-01-31 --point 0.01 --rule PHLD

  # 8. HELP, VERSION, EXAMPLES
  python run_analysis.py -h
  python run_analysis.py --version
  python run_analysis.py --examples

  # 9. CACHE/DEBUG
  # Remove cache and rerun
  rm data/cache/csv_converted/*.parquet
  python run_analysis.py csv --csv-file data.csv --point 0.01

  # 10. ERROR CASES (will show error/help)
  python run_analysis.py csv --csv-file data.csv   # (missing --point)
  python run_analysis.py yf -t EURUSD=X            # (missing --period or --start/--end)

Note:
- For all API modes (yfinance, polygon, binance), the --point parameter is required to specify the instrument's point size (e.g., 0.00001 for EURUSD, 0.01 for stocks/crypto).
- Use -d/--draw to select plotting backend: fastest, fast, plotly, mplfinance, etc.
- Use --rule to select trading rule: PV_HighLow, Support_Resistants, Pressure_Vector, Predict_High_Low_Direction, PHLD, PV, SR.
- SHOW mode allows filtering cached files by source, keywords, date, and rule.
- For more details, see README.md or run with -h for full help.\n""")
            sys.exit(0)
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
