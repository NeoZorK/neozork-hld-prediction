# -*- coding: utf-8 -*-
# src/cli/cli.py

"""
Command Line Interface setup using argparse and RichHelpFormatter for     data_source_group.add_argument('--start', help="Start date (YYYY-MM-DD). Used by yfinance, polygon, binance, exrate.")
    # Make --end related only to --start (not period)
    data_source_group.add_argument('--end',
                                   help="End date (YYYY-MM-DD). Used by yfinance, polygon, binance, exrate. Required if --start is used.")red help.
All comments are in English.
"""
import argparse
import textwrap
import sys  # Import sys for exit
import src.cli.cli_examples as cli_examples
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Use relative imports for constants and version within the src package
from ..common.constants import TradingRule
from .. import __version__  # Make sure version is updated in src/__init__.py


# Custom help formatter to use colors
class ColoredHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """Custom help formatter that adds color to the help output."""

    def _format_action_invocation(self, action):
        """Format the action invocation (e.g. -h, --help) with color."""
        if action.option_strings:
            parts = []
            for option_string in action.option_strings:
                parts.append(f"{Fore.GREEN}{option_string}{Style.RESET_ALL}")
            return ', '.join(parts)
        else:
            return super()._format_action_invocation(action)

    def _format_usage(self, usage, actions, groups, prefix):
        """Format usage with colors."""
        if prefix is None:
            prefix = f"{Fore.YELLOW}usage: {Style.RESET_ALL}"
        return super()._format_usage(usage, actions, groups, prefix)

    def _format_args(self, action, default_metavar):
        """Format args with colors."""
        result = super()._format_args(action, default_metavar)
        return f"{Fore.CYAN}{result}{Style.RESET_ALL}"

    def _get_help_string(self, action):
        """Format help string with colors."""
        help_text = super()._get_help_string(action)
        if action.default != argparse.SUPPRESS and action.default is not None:
            defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
            if action.option_strings or action.nargs in defaulting_nargs:
                help_text = help_text.replace(f"(default: {action.default})",
                                           f"({Fore.MAGENTA}default: {action.default}{Style.RESET_ALL})")
        return help_text

    def start_section(self, heading):
        """Format section headings with colors."""
        heading = f"{Fore.YELLOW}{Style.BRIGHT}{heading}{Style.RESET_ALL}"
        super().start_section(heading)

# Definition of the argument parsing function
def parse_arguments():
    """Sets up argument parser using ColoredHelpFormatter and returns the parsed arguments."""

    # --- Main description ---
    main_description = textwrap.dedent(f"""
       {Fore.CYAN}{Style.BRIGHT}Shcherbyna Pressure Vector Indicator Analysis Tool{Style.RESET_ALL}
       
       Calculate and plot Shcherbyna Pressure Vector indicator using demo data,
       fetching from Yahoo Finance, reading from a CSV file, fetching from Polygon.io,
       or fetching from Binance. Allows choosing the plotting library.
       """)


    # --- Argument Parser Setup ---
    parser = argparse.ArgumentParser(
        description=main_description,
        formatter_class=ColoredHelpFormatter,
        epilog=None,  # no epilog
        add_help=False  # Disable default help to add it to a specific group
    )

    # --- Examples Option ---
    parser.add_argument(
        '--examples',
        action='store_true',
        help='Show usage examples and exit.'
    )

    # --- Required Arguments Group ---
    required_group = parser.add_argument_group('Required Arguments')
    required_group.add_argument('mode', choices=['demo', 'yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'show'],
                                help="Operating mode: 'demo', 'yfinance'/'yf', 'csv', 'polygon', 'binance', 'exrate', 'show'.")

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
                                   help="Ticker symbol (e.g., 'EURUSD=X' for yfinance; 'EURUSD', 'AAPL' for Polygon; 'BTCUSDT' for Binance; 'EURUSD', 'GBPJPY' for Exchange Rate API). Required for 'yfinance', 'polygon', 'binance', 'exrate' modes.")
    data_source_group.add_argument('-i', '--interval', default='D1',
                                   help="Timeframe (e.g., 'M1', 'H1', 'D1', 'W1', 'MN1'). Default: D1.")
    # Point size argument
    data_source_group.add_argument('--point', type=float,
                                   help="Instrument point size (e.g., 0.00001 for EURUSD, 0.01 for stocks/crypto). Overrides yfinance estimation. Required for 'csv', 'polygon', 'binance', 'exrate' modes.")
    # History selection (period or start/end dates)
    history_group = data_source_group.add_mutually_exclusive_group()
    history_group.add_argument('--period',
                               help="History period for yfinance (e.g., '1mo', '1y'). Not used if --start/--end are provided. Not used by Polygon/Binance.")
    history_group.add_argument('--start', help="Start date (YYYY-MM-DD). Used by yfinance, polygon, binance.")
    # Make --end related only to --start (not period)
    data_source_group.add_argument('--end',
                                   help="End date (YYYY-MM-DD). Used by yfinance, polygon, binance. Required if --start is used.")

    # --- Indicator Options Group ---
    indicator_group = parser.add_argument_group('Indicator Options')
    rule_aliases_map = {'PHLD': 'Predict_High_Low_Direction', 'PV': 'Pressure_Vector', 'SR': 'Support_Resistants'}
    rule_names = list(TradingRule.__members__.keys())
    all_rule_choices = rule_names + list(rule_aliases_map.keys()) + ['OHLCV', 'AUTO']  # Added 'OHLCV' and 'AUTO' as valid rules
    default_rule_name = 'OHLCV'  # Changed from TradingRule.Predict_High_Low_Direction.name
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
        choices=['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate'],
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
        choices=['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
        default='fastest',
        help="Choose plotting library: 'fastest' (Plotly+Dask+Datashader for extremely large datasets, default), 'fast' (Dask+Datashader+Bokeh), 'plotly'/'plt' (interactive HTML), 'mplfinance'/'mpl' (static image), 'seaborn'/'sb' (statistical plots), or 'term' (terminal charts with plotext)."
    )

    # --- Output Options Group ---
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('--export-parquet',
                              action='store_true',
                              help="Export indicator data to parquet file. The file will be named as the original with the rule name as a postfix (e.g., CSVExport_AAPL.NAS_PERIOD_D1_PHLD.parquet)."
                             )

    # --- Other Options Group ---
    other_group = parser.add_argument_group('Other Options')
    other_group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                             help='Show this help message and exit.')
    other_group.add_argument('--version', action='version',
                             version=f'{"Shcherbyna Pressure Vector Indicator v"+__version__}',
                             help="Show program's version number and exit.")

    # --- Parse Arguments ---
    try:
        # If no arguments provided, show help
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(0)

        if '--examples' in sys.argv:
            cli_examples.show_cli_examples_colored()
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

    # Check requirements for API modes (yfinance, polygon, binance, exrate)
    api_modes = ['yfinance', 'polygon', 'binance', 'exrate']
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

    # Check requirements for Polygon, Binance & Exchange Rate API
    polygon_binance_exrate_modes = ['polygon', 'binance', 'exrate']
    if effective_mode in polygon_binance_exrate_modes:
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

    # --- Fix: Merge positional show_args into source/keywords for show mode ---
    if effective_mode == 'show':
        # If user provided positional arguments after 'show', use them as source/keywords
        if args.show_args:
            # If the first positional arg is a valid source, treat as source
            valid_sources = ['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate']
            # Remove any flags from show_args (e.g. --raw, --cleaned, --draw, etc.)
            filtered_args = [a for a in args.show_args if not a.startswith('--')]
            if filtered_args:
                if filtered_args[0] in valid_sources:
                    args.source = filtered_args[0]
                    args.keywords = filtered_args[1:]
                    if args.source == 'yf':
                        args.source = 'yfinance'
                else:
                    args.keywords = filtered_args

    # --- Fix: Map --show-rule to args.rule for show mode compatibility ---
    if effective_mode == 'show' and hasattr(args, 'show_rule') and args.show_rule:
        args.rule = args.show_rule

    return args
