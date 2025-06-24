# -*- coding: utf-8 -*-
# src/cli/cli.py

"""
Command Line Interface setup using argparse and RichHelpFormatter for colored help.
All comments are in English.
"""
import argparse
import textwrap
import sys  # Import sys for exit
import src.cli.cli_examples as cli_examples
from colorama import init, Fore, Style
from src.cli.indicators_search import IndicatorSearcher

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
       
       {Fore.YELLOW}Quick Start:{Style.RESET_ALL}
         python run_analysis.py --indicators                    # List all available indicators
         python run_analysis.py demo --rule RSI                 # Run with demo data and RSI indicator
         python run_analysis.py interactive                     # Start interactive mode
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

    # --- Indicators Search Option ---
    parser.add_argument(
        '--indicators',
        nargs='*',
        metavar=('CATEGORY', 'NAME'),
        help='Show available indicators by category and name. Usage: --indicators [category] [name]'
    )

    # --- Interactive Mode Option ---
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Start interactive mode for guided indicator selection and analysis.'
    )

    # --- Required Arguments Group ---
    required_group = parser.add_argument_group('Required Arguments')
    required_group.add_argument('mode', choices=['demo', 'yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'show', 'interactive'],
                                help="Operating mode: 'demo', 'yfinance'/'yf', 'csv', 'polygon', 'binance', 'exrate', 'show', 'interactive'.")

    # --- Show Mode Positional Arguments ---
    parser.add_argument('show_args', nargs='*', default=[],
                        help=argparse.SUPPRESS)  # Hide from help but collect positional args after 'mode'

    # --- Data Source Specific Options Group ---
    data_source_group = parser.add_argument_group('Data Source Options')
    # CSV options
    data_source_group.add_argument('--csv-file', metavar='PATH',
                                   help="Path to input CSV file (required for 'csv' mode)")
    # API options (Yahoo Finance / Polygon.io / Binance)
    data_source_group.add_argument('--ticker', metavar='SYMBOL',
                                   help="Ticker symbol. Examples: 'EURUSD=X' (yfinance), 'AAPL' (polygon), 'BTCUSDT' (binance)")
    data_source_group.add_argument('--interval', metavar='TIME', default='D1',
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
        'RSI_DIV': 'RSI_Divergence',
        'CCI': 'CCI',
        'STOCH': 'Stochastic',
        'EMA': 'EMA',
        'BB': 'Bollinger_Bands',
        'ATR': 'ATR',
        'VWAP': 'VWAP',
        'PIVOT': 'Pivot_Points',
        # Momentum indicators
        'MACD': 'MACD',
        'STOCHOSC': 'StochOscillator',
        # Predictive indicators
        'HMA': 'HMA',
        'TSF': 'TSForecast',
        # Probability indicators
        'MC': 'MonteCarlo',
        'KELLY': 'Kelly',
        # Sentiment indicators
        'FG': 'FearGreed',
        'COT': 'COT',
        'PCR': 'PutCallRatio',
        # Support/Resistance indicators
        'DONCHAIN': 'Donchain',
        'FIBO': 'FiboRetr',
        # Volume indicators
        'OBV': 'OBV',
        # Volatility indicators
        'STDEV': 'StDev',
        # Trend indicators
        'ADX': 'ADX',
        'SAR': 'SAR',
        'SUPERTREND': 'SuperTrend'
    }
    rule_names = list(TradingRule.__members__.keys())
    all_rule_choices = rule_names + list(rule_aliases_map.keys()) + ['OHLCV', 'AUTO']  # Added 'OHLCV' and 'AUTO' as valid rules
    default_rule_name = 'OHLCV'  # Changed from TradingRule.Predict_High_Low_Direction.name
    indicator_group.add_argument(
        '--rule', metavar='RULE',
        default=default_rule_name,
        choices=all_rule_choices,
        help="Trading rule: OHLCV, PV, SR, PHLD, RSI, RSI_MOM, RSI_DIV, CCI, STOCH, EMA, BB, ATR, VWAP, PIVOT, MACD, STOCHOSC, HMA, TSF, MC, KELLY, FG, COT, PCR, DONCHAIN, FIBO, OBV, STDEV, ADX, SAR, SUPERTREND, AUTO. Aliases: PV=Pressure_Vector, SR=Support_Resistants, RSI_MOM=RSI_Momentum, RSI_DIV=RSI_Divergence, STOCH=Stochastic, BB=Bollinger_Bands, PIVOT=Pivot_Points, STOCHOSC=StochOscillator, TSF=TSForecast, MC=MonteCarlo, FG=FearGreed, PCR=PutCallRatio, FIBO=FiboRetr, STDEV=StDev, SUPERTREND=SuperTrend. Parameterized format: rsi:14,30,70,open (period,oversold,overbought,price_type)"
    )
    
    # Add price type selection for indicators that support it
    indicator_group.add_argument(
        '--price-type', metavar='TYPE',
        choices=['open', 'close'],
        default='close',
        help="Price type for indicator calculation: 'open' or 'close' (default: close). Supported by all indicators with price_type parameter"
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
    output_group.add_argument('--export-indicators-info',
                              action='store_true',
                              help="Export indicator metadata to JSON format (data/indicators/metadata/)")

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
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}Indicator Usage Examples:{Style.RESET_ALL}")
            print("  Show all indicators:   --indicators")
            print("  Show oscillators:      --indicators oscillators")
            print("  Show RSI info:         --indicators oscillators rsi")
            print("  Show trend indicators: --indicators trend")
            print("  Show MACD info:        --indicators momentum macd")
            print("  Interactive mode:      python run_analysis.py interactive")
            cli_examples.show_cli_examples_colored()
            sys.exit(0)
        
        # Handle --indicators
        if '--indicators' in sys.argv:
            idx = sys.argv.index('--indicators')
            args_list = sys.argv[idx+1:]
            searcher = IndicatorSearcher()
            if not args_list:
                searcher.display_categories()
            elif len(args_list) == 1:
                searcher.display_category(args_list[0], detailed=True)
            elif len(args_list) >= 2:
                # Search by category and name
                category = args_list[0]
                name = ' '.join(args_list[1:])
                print(f"\n{Fore.YELLOW}Search in category '{category}' for '{name}':{Style.RESET_ALL}")
                results = searcher.search_indicators(name)
                filtered = [ind for ind in results if ind.category == category]
                if filtered:
                    for ind in filtered:
                        print(ind.display(detailed=True))
                else:
                    print(f"No indicators found in category '{category}' matching '{name}'")
            sys.exit(0)
        
        # Handle --interactive flag
        if '--interactive' in sys.argv:
            from src.cli.interactive_mode import start_interactive_mode
            start_interactive_mode()
            sys.exit(0)
            
        args = parser.parse_args()
    except SystemExit as e:
        if e.code != 0:
            print(f"Argument parsing error (Code: {e.code}). Exiting.", file=sys.stderr)
        sys.exit(e.code)

    # --- Post-parsing validation ---
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    # Handle interactive mode
    if effective_mode == 'interactive':
        from src.cli.interactive_mode import start_interactive_mode
        start_interactive_mode()
        sys.exit(0)

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
    # Allow export flags only for demo and show (except show ind)
    forbidden_export_modes = ['yfinance', 'csv', 'polygon', 'binance', 'exrate']
    if effective_mode in forbidden_export_modes:
        if getattr(args, 'export_parquet', False) or getattr(args, 'export_csv', False) or getattr(args, 'export_json', False) or getattr(args, 'export_indicators_info', False):
            parser.error("Export flags (--export-parquet, --export-csv, --export-json, --export-indicators-info) are only allowed in 'demo' and 'show' modes (except 'show ind'). Use 'show' mode to export indicators from downloaded data.")
    # Disallow export flags for 'show ind' (indicator viewing)
    if effective_mode == 'show' and hasattr(args, 'source') and args.source == 'ind':
        if getattr(args, 'export_parquet', False) or getattr(args, 'export_csv', False) or getattr(args, 'export_json', False) or getattr(args, 'export_indicators_info', False):
            parser.error("Export flags (--export-parquet, --export-csv, --export-json, --export-indicators-info) are not allowed in 'show ind' mode. Use 'demo' or other show modes to export indicators.")
    # Update help for export flags
    for action in parser._actions:
        if action.dest in ['export_parquet', 'export_csv', 'export_json', 'export_indicators_info']:
            action.help += ' (Allowed only in demo and show (except show ind); forbidden in show ind, yfinance, csv, polygon, binance, exrate)'

    return args

def parse_indicator_parameters(rule_str: str) -> tuple[str, dict]:
    """
    Parse indicator rule string in format 'indicator:param1,param2,param3,param4'.
    
    Args:
        rule_str (str): Rule string like 'rsi:14,30,70,open' or 'rsi'
    
    Returns:
        tuple: (indicator_name, parameters_dict)
    """
    if ':' not in rule_str:
        # No parameters provided, return indicator name and empty dict
        return rule_str.lower(), {}
    
    try:
        # Split by ':' to separate indicator name from parameters
        parts = rule_str.split(':', 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid rule format: {rule_str}")
        
        indicator_name = parts[0].lower().strip()
        params_str = parts[1].strip()
        
        # Parse parameters based on indicator type
        if indicator_name == 'rsi':
            return parse_rsi_parameters(params_str)
        elif indicator_name == 'macd':
            return parse_macd_parameters(params_str)
        elif indicator_name == 'stoch':
            return parse_stoch_parameters(params_str)
        elif indicator_name == 'ema':
            return parse_ema_parameters(params_str)
        elif indicator_name == 'bb':
            return parse_bb_parameters(params_str)
        elif indicator_name == 'atr':
            return parse_atr_parameters(params_str)
        elif indicator_name == 'cci':
            return parse_cci_parameters(params_str)
        elif indicator_name == 'vwap':
            return parse_vwap_parameters(params_str)
        elif indicator_name == 'pivot':
            return parse_pivot_parameters(params_str)
        elif indicator_name == 'hma':
            return parse_hma_parameters(params_str)
        elif indicator_name == 'tsf':
            return parse_tsf_parameters(params_str)
        elif indicator_name == 'monte':
            return parse_monte_parameters(params_str)
        elif indicator_name == 'kelly':
            return parse_kelly_parameters(params_str)
        elif indicator_name == 'donchain':
            return parse_donchain_parameters(params_str)
        elif indicator_name == 'fibo':
            return parse_fibo_parameters(params_str)
        elif indicator_name == 'obv':
            return parse_obv_parameters(params_str)
        elif indicator_name == 'stdev':
            return parse_stdev_parameters(params_str)
        elif indicator_name == 'adx':
            return parse_adx_parameters(params_str)
        elif indicator_name == 'sar':
            return parse_sar_parameters(params_str)
        else:
            # Unknown indicator, return as-is
            return indicator_name, {}
            
    except Exception as e:
        # Re-raise the exception instead of using logger
        raise e


def parse_rsi_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI parameters: period,oversold,overbought,price_type"""
    params = params_str.split(',')
    if len(params) != 4:
        raise ValueError(f"RSI requires exactly 4 parameters: period,oversold,overbought,price_type. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values like 14.0
    oversold = float(params[1].strip())
    overbought = float(params[2].strip())
    price_type = params[3].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"RSI price_type must be 'open' or 'close', got: {price_type}")
    
    return 'rsi', {
        'rsi_period': period,
        'oversold': oversold,
        'overbought': overbought,
        'price_type': price_type
    }


def parse_macd_parameters(params_str: str) -> tuple[str, dict]:
    """Parse MACD parameters: fast_period,slow_period,signal_period,price_type"""
    params = params_str.split(',')
    if len(params) != 4:
        raise ValueError(f"MACD requires exactly 4 parameters: fast_period,slow_period,signal_period,price_type. Got: {params_str}")
    
    fast_period = int(float(params[0].strip()))  # Handle float values
    slow_period = int(float(params[1].strip()))
    signal_period = int(float(params[2].strip()))
    price_type = params[3].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"MACD price_type must be 'open' or 'close', got: {price_type}")
    
    return 'macd', {
        'macd_fast': fast_period,
        'macd_slow': slow_period,
        'macd_signal': signal_period,
        'price_type': price_type
    }


def parse_stoch_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Stochastic parameters: k_period,d_period,price_type"""
    params = params_str.split(',')
    if len(params) != 3:
        raise ValueError(f"Stochastic requires exactly 3 parameters: k_period,d_period,price_type. Got: {params_str}")
    
    k_period = int(float(params[0].strip()))  # Handle float values
    d_period = int(float(params[1].strip()))
    price_type = params[2].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Stochastic price_type must be 'open' or 'close', got: {price_type}")
    
    return 'stoch', {
        'stoch_k_period': k_period,
        'stoch_d_period': d_period,
        'price_type': price_type
    }


def parse_ema_parameters(params_str: str) -> tuple[str, dict]:
    """Parse EMA parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"EMA requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    price_type = params[1].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"EMA price_type must be 'open' or 'close', got: {price_type}")
    
    return 'ema', {
        'ema_period': period,
        'price_type': price_type
    }


def parse_bb_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Bollinger Bands parameters: period,std_dev,price_type"""
    params = params_str.split(',')
    if len(params) != 3:
        raise ValueError(f"Bollinger Bands requires exactly 3 parameters: period,std_dev,price_type. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    std_dev = float(params[1].strip())
    price_type = params[2].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Bollinger Bands price_type must be 'open' or 'close', got: {price_type}")
    
    return 'bb', {
        'bb_period': period,
        'bb_std_dev': std_dev,
        'price_type': price_type
    }


def parse_atr_parameters(params_str: str) -> tuple[str, dict]:
    """Parse ATR parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"ATR requires exactly 1 parameter: period. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    
    return 'atr', {
        'atr_period': period
    }


def parse_cci_parameters(params_str: str) -> tuple[str, dict]:
    """Parse CCI parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"CCI requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    price_type = params[1].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"CCI price_type must be 'open' or 'close', got: {price_type}")
    
    return 'cci', {
        'cci_period': period,
        'price_type': price_type
    }


def parse_vwap_parameters(params_str: str) -> tuple[str, dict]:
    """Parse VWAP parameters: price_type"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"VWAP requires exactly 1 parameter: price_type. Got: {params_str}")
    
    price_type = params[0].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"VWAP price_type must be 'open' or 'close', got: {price_type}")
    
    return 'vwap', {
        'price_type': price_type
    }


def parse_pivot_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Pivot Points parameters: price_type"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"Pivot Points requires exactly 1 parameter: price_type. Got: {params_str}")
    
    price_type = params[0].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Pivot Points price_type must be 'open' or 'close', got: {price_type}")
    
    return 'pivot', {
        'price_type': price_type
    }


def parse_hma_parameters(params_str: str) -> tuple[str, dict]:
    """Parse HMA parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"HMA requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    price_type = params[1].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"HMA price_type must be 'open' or 'close', got: {price_type}")
    
    return 'hma', {
        'hma_period': period,
        'price_type': price_type
    }


def parse_tsf_parameters(params_str: str) -> tuple[str, dict]:
    """Parse TSF parameters: period,forecast_period,price_type"""
    params = params_str.split(',')
    if len(params) != 3:
        raise ValueError(f"TSF requires exactly 3 parameters: period,forecast_period,price_type. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    forecast_period = int(float(params[1].strip()))
    price_type = params[2].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"TSF price_type must be 'open' or 'close', got: {price_type}")
    
    return 'tsf', {
        'tsf_period': period,
        'tsf_forecast': forecast_period,
        'price_type': price_type
    }


def parse_monte_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Monte Carlo parameters: simulations,period"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"Monte Carlo requires exactly 2 parameters: simulations,period. Got: {params_str}")
    
    simulations = int(float(params[0].strip()))  # Handle float values
    period = int(float(params[1].strip()))
    
    return 'monte', {
        'monte_simulations': simulations,
        'monte_period': period
    }


def parse_kelly_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Kelly Criterion parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"Kelly Criterion requires exactly 1 parameter: period. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    
    return 'kelly', {
        'kelly_period': period
    }


def parse_donchain_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Donchian Channels parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"Donchian Channels requires exactly 1 parameter: period. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    
    return 'donchain', {
        'donchain_period': period
    }


def parse_fibo_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Fibonacci Retracements parameters: levels"""
    params = params_str.split(',')
    if len(params) < 1:
        raise ValueError(f"Fibonacci Retracements requires at least 1 parameter: levels. Got: {params_str}")
    
    levels = [float(p.strip()) for p in params]
    
    return 'fibo', {
        'fib_levels': levels
    }


def parse_obv_parameters(params_str: str) -> tuple[str, dict]:
    """Parse OBV parameters: none required"""
    if params_str.strip():
        raise ValueError(f"OBV does not require parameters. Got: {params_str}")
    
    return 'obv', {}


def parse_stdev_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Standard Deviation parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"Standard Deviation requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    price_type = params[1].strip().lower()
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Standard Deviation price_type must be 'open' or 'close', got: {price_type}")
    
    return 'stdev', {
        'stdev_period': period,
        'price_type': price_type
    }


def parse_adx_parameters(params_str: str) -> tuple[str, dict]:
    """Parse ADX parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"ADX requires exactly 1 parameter: period. Got: {params_str}")
    
    period = int(float(params[0].strip()))  # Handle float values
    
    return 'adx', {
        'adx_period': period
    }


def parse_sar_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SAR parameters: acceleration,maximum"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"SAR requires exactly 2 parameters: acceleration,maximum. Got: {params_str}")
    
    acceleration = float(params[0].strip())
    maximum = float(params[1].strip())
    
    return 'sar', {
        'sar_acceleration': acceleration,
        'sar_maximum': maximum
    }
