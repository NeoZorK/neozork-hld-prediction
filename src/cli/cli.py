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


# Custom help formatter to use colors and improve alignment
class ColoredHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """Custom help formatter that adds color to the help output and improves text alignment."""

    def __init__(self, prog):
        # Set consistent width and max_help_position for better alignment with larger indent
        super().__init__(prog, width=200, max_help_position=50, indent_increment=4)

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
        """Format help string with colors and better text wrapping."""
        help_text = super()._get_help_string(action)
        if action.default != argparse.SUPPRESS and action.default is not None:
            defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
            if action.option_strings or action.nargs in defaulting_nargs:
                help_text = help_text.replace(f"(default: {action.default})",
                                           f"({Fore.MAGENTA}default: {action.default}{Style.RESET_ALL})")
        return help_text

    def _split_lines(self, text, width):
        """Override to improve text wrapping with consistent indentation."""
        if len(text) <= width:
            return [text]
        
        # Split long lines more intelligently with larger indent
        import textwrap
        lines = []
        for line in text.splitlines():
            if len(line) <= width:
                lines.append(line)
            else:
                wrapped = textwrap.fill(line, width, 
                                      break_long_words=False, 
                                      break_on_hyphens=False,
                                      subsequent_indent='                            ')
                lines.extend(wrapped.splitlines())
        return lines

    def _format_action(self, action):
        """Override to add larger consistent indentation for all help items."""
        # Get the original formatted action
        help_text = super()._format_action(action)
        
        # Add extra indentation to all lines (4 more spaces)
        lines = help_text.split('\n')
        indented_lines = []
        for i, line in enumerate(lines):
            if line.strip():  # Only indent non-empty lines
                if i == 0 or line.startswith('  '):  # First line or already indented
                    indented_lines.append('    ' + line)
                else:
                    indented_lines.append(line)
            else:
                indented_lines.append(line)
        
        return '\n'.join(indented_lines)

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
       
       Calculate and plot pressure vector indicators from multiple data sources: demo data, Yahoo Finance, CSV files, Polygon.io, Binance, and Exchange Rate API. Export calculated indicators in parquet, CSV, or JSON formats.
       """).strip()


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
    data_source_group.add_argument('--csv-file', metavar='PATH',
                                   help="Path to input CSV file (required for 'csv' mode)")
    # API options (Yahoo Finance / Polygon.io / Binance)
    data_source_group.add_argument('-t', '--ticker', metavar='SYMBOL',
                                   help="Ticker symbol. Examples: 'EURUSD=X' (yfinance), 'AAPL' (polygon), 'BTCUSDT' (binance)")
    data_source_group.add_argument('-i', '--interval', metavar='TIME', default='D1',
                                   help="Timeframe: 'M1', 'H1', 'D1', 'W1', 'MN1'. Default: D1")
    # Point size argument
    data_source_group.add_argument('--point', metavar='SIZE', type=float,
                                   help="Point size. Examples: 0.00001 (EURUSD), 0.01 (stocks/crypto)")
    # History selection (period or start/end dates)
    history_group = data_source_group.add_mutually_exclusive_group()
    history_group.add_argument('--period', metavar='TIME',
                               help="History period for yfinance. Examples: '1mo', '1y', '5d'")
    history_group.add_argument('--start', metavar='DATE',
                               help="Start date for data range (yfinance, polygon, binance)")
    # Make --end related only to --start (not period)
    data_source_group.add_argument('--end', metavar='DATE',
                                   help="End date for data range (required with --start)")

    # --- Indicator Options Group ---
    indicator_group = parser.add_argument_group('Indicator Options')
    rule_aliases_map = {
        'PHLD': 'Predict_High_Low_Direction', 
        'PV': 'Pressure_Vector', 
        'SR': 'Support_Resistants',
        'RSI': 'RSI',
        'RSI_MOM': 'RSI_Momentum',
        'RSI_DIV': 'RSI_Divergence'
    }
    rule_names = list(TradingRule.__members__.keys())
    all_rule_choices = rule_names + list(rule_aliases_map.keys()) + ['OHLCV', 'AUTO']  # Added 'OHLCV' and 'AUTO' as valid rules
    default_rule_name = 'OHLCV'  # Changed from TradingRule.Predict_High_Low_Direction.name
    indicator_group.add_argument(
        '--rule', metavar='RULE',
        default=default_rule_name,
        choices=all_rule_choices,
        help="Trading rule: OHLCV, PV, SR, PHLD, RSI, RSI_MOM, RSI_DIV, AUTO. Aliases: PV=Pressure_Vector, SR=Support_Resistants, RSI_MOM=RSI_Momentum, RSI_DIV=RSI_Divergence"
    )
    
    # Add price type selection for RSI indicators
    indicator_group.add_argument(
        '--price-type', metavar='TYPE',
        choices=['open', 'close'],
        default='close',
        help="Price type for RSI calculation: 'open' or 'close' (default: close)"
    )

    # --- Show Mode Options Group ---
    show_group = parser.add_argument_group('Show Mode Options')
    show_group.add_argument(
        '--source', metavar='SRC', default='yfinance',
        choices=['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'ind'],
        help="Data source filter: yfinance, csv, polygon, binance, exrate, ind (indicators)"
    )
    show_group.add_argument(
        '--keywords', metavar='WORD', nargs='+', default=[],
        help="Filter keywords (e.g., ticker symbol, date patterns)"
    )
    show_group.add_argument(
        '--show-start', metavar='DATE', type=str, default=None,
        help="Start date/datetime to filter data before calculation"
    )
    show_group.add_argument(
        '--show-end', metavar='DATE', type=str, default=None,
        help="End date/datetime to filter data before calculation"
    )
    show_group.add_argument(
        '--show-rule', metavar='RULE', type=str, choices=all_rule_choices, default=None,
        help="Trading rule for indicator calculation (single file mode)"
    )

    # --- Plotting Options Group ---
    plotting_group = parser.add_argument_group('Plotting Options')
    plotting_group.add_argument(
        '-d', '--draw', metavar='METHOD',
        choices=['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
        default='fastest',
        help="Plot method: fastest, fast, plotly, mplfinance, seaborn, term"
    )

    # --- Output Options Group ---
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('--export-parquet',
                              action='store_true',
                              help="Export indicators to parquet format (data/indicators/parquet/)")
    output_group.add_argument('--export-csv',
                              action='store_true',
                              help="Export indicators to CSV format (data/indicators/csv/)")
    output_group.add_argument('--export-json',
                              action='store_true',
                              help="Export indicators to JSON format (data/indicators/json/)")

    # --- Other Options Group ---
    other_group = parser.add_argument_group('Other Options')
    other_group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                             help='Show this help message and exit')
    other_group.add_argument('--version', action='version',
                             version=f'{"Shcherbyna Pressure Vector Indicator v"+__version__}',
                             help="Show program version and exit")

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

    # Check requirements for Polygon and Binance (but not Exchange Rate API)
    polygon_binance_modes = ['polygon', 'binance']
    if effective_mode in polygon_binance_modes:
        if not args.start or not args.end:
            parser.error(f"arguments --start and --end are required when mode is '{effective_mode}'")
        if args.point is None:
            parser.error(f"argument --point is required when mode is '{effective_mode}'")

    # Check requirements for Exchange Rate API (only point and ticker)
    if effective_mode == 'exrate':
        if args.point is None:
            parser.error(f"argument --point is required when mode is 'exrate'")
        # Note: exrate uses --interval for both free (current) and paid (historical) plans

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
            valid_sources = ['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'ind']
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

    # --- Restrict export flags for forbidden modes ---
    # Разрешаем экспорт-флаги только для demo и show (кроме show ind)
    forbidden_export_modes = ['yfinance', 'csv', 'polygon', 'binance', 'exrate']
    if effective_mode in forbidden_export_modes:
        if getattr(args, 'export_parquet', False) or getattr(args, 'export_csv', False) or getattr(args, 'export_json', False):
            parser.error("Export flags (--export-parquet, --export-csv, --export-json) are only allowed in 'demo' and 'show' modes (except 'show ind'). Use 'show' mode to export indicators from downloaded data.")
    # Disallow export flags for 'show ind' (indicator viewing)
    if effective_mode == 'show' and hasattr(args, 'source') and args.source == 'ind':
        if getattr(args, 'export_parquet', False) or getattr(args, 'export_csv', False) or getattr(args, 'export_json', False):
            parser.error("Export flags (--export-parquet, --export-csv, --export-json) are not allowed in 'show ind' mode. Use 'demo' or other show modes to export indicators.")
    # Update help for export flags
    for action in parser._actions:
        if action.dest in ['export_parquet', 'export_csv', 'export_json']:
            action.help += ' (Allowed only in demo and show (except show ind); forbidden in show ind, yfinance, csv, polygon, binance, exrate)'

    return args
