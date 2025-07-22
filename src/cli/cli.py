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
         python run_analysis.py --metric                        # Show trading metrics encyclopedia
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

    # --- Metrics Encyclopedia Option ---
    parser.add_argument(
        '--metric',
        nargs='*',
        metavar=('TYPE', 'FILTER'),
        help='Show trading metrics encyclopedia and strategy tips. Usage: --metric [metrics|tips|notes] [filter_text]'
    )

    # --- Interactive Mode Option ---
    parser.add_argument(
        '--interactive',
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
        'BB': 'Bollinger_Bands'
    }
    rule_names = list(TradingRule.__members__.keys())
    all_rule_choices = rule_names + list(rule_aliases_map.keys()) + ['OHLCV', 'AUTO']  # Added 'OHLCV' and 'AUTO' as valid rules
    default_rule_name = 'OHLCV'
    indicator_group.add_argument(
        '--rule',
        default=default_rule_name,
        help=f"Trading rule to apply. Default: {default_rule_name}. Aliases: PHLD=Predict_High_Low_Direction, PV=Pressure_Vector, SR=Support_Resistants, BB=Bollinger_Bands."
    )
    
    # Strategy parameters
    indicator_group.add_argument(
        '--strategy',
        metavar='LOT,RISK_REWARD,FEE',
        help="Strategy parameters: lot_size,risk_reward_ratio,fee_per_trade. Example: --strategy 1,2,0.07 means lot=1.0, risk:reward=2:1, fee=0.07%%. Default: 1.0,2.0,0.07"
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
        '-d', '--draw',
        dest='draw',
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
    other_group.add_argument('-h', action='help', default=argparse.SUPPRESS,
                             help='Show this help message and exit')
    other_group.add_argument('--version', action='version',
                             version=f'{"Shcherbyna Pressure Vector Indicator v"+__version__}',
                             help="Show program version and exit")

    # --- Parse Arguments ---
    try:
        # If --indicators is present, always handle it first and exit
        if '--indicators' in sys.argv:
            idx = sys.argv.index('--indicators')
            args_list = sys.argv[idx+1:]
            searcher = IndicatorSearcher()
            if not args_list:
                searcher.display_categories()
            elif len(args_list) == 1:
                query = args_list[0]
                if query in searcher.indicators:
                    searcher.display_category(query, detailed=True)
                else:
                    results = searcher.search_indicators(query)
                    if results:
                        print(f"\n{Fore.YELLOW}Search results for '{query}' across all categories:{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
                        for ind in results:
                            print(ind.display(detailed=True))
                    else:
                        print(f"{Fore.RED}No indicators found matching: {query}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}Available categories: {', '.join(searcher.list_categories())}{Style.RESET_ALL}")
            elif len(args_list) >= 2:
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

        # If no arguments provided, show help
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(0)

        # Handle --help flag before parsing to avoid mode requirement
        if '--help' in sys.argv or '-h' in sys.argv:
            parser.print_help()
            sys.exit(0)

        # Handle special flags that don't require mode argument BEFORE parsing
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
        
        # Handle --metric encyclopedia
        if '--metric' in sys.argv:
            idx = sys.argv.index('--metric')
            args_list = sys.argv[idx+1:]
            from src.cli.quant_encyclopedia import QuantEncyclopedia
            encyclopedia = QuantEncyclopedia()
            
            if not args_list:
                # Show all metrics and tips
                encyclopedia.show_all_metrics()
                encyclopedia.show_all_tips()
            elif len(args_list) == 1:
                # Single argument - could be type or filter
                arg = args_list[0].lower()
                if arg in ['metrics', 'tips', 'notes']:
                    if arg == 'metrics':
                        encyclopedia.show_all_metrics()
                    elif arg == 'tips':
                        encyclopedia.show_all_tips()
                    elif arg == 'notes':
                        encyclopedia.show_all_tips()  # Notes are part of tips
                else:
                    # Treat as filter text
                    encyclopedia.show_filtered_content(arg)
            elif len(args_list) >= 2:
                # Two or more arguments: type and filter
                metric_type = args_list[0].lower()
                filter_text = ' '.join(args_list[1:])
                
                if metric_type == 'metrics':
                    encyclopedia.show_all_metrics(filter_text)
                elif metric_type == 'tips':
                    encyclopedia.show_all_tips(filter_text)
                elif metric_type == 'notes':
                    encyclopedia.show_all_tips(filter_text)  # Notes are part of tips
                else:
                    # Invalid type, treat first as filter
                    encyclopedia.show_filtered_content(' '.join(args_list))
            
            sys.exit(0)
        
        # Handle --interactive flag
        if '--interactive' in sys.argv:
            from src.cli.interactive_mode import start_interactive_mode
            start_interactive_mode()
            sys.exit(0)
            
        # Now parse arguments for normal operation
        args = parser.parse_args()
    except SystemExit as e:
        if e.code != 0:
            print(f"Argument parsing error (Code: {e.code}). Exiting.", file=sys.stderr)
        sys.exit(e.code)

    # --- Post-parsing validation ---
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    # Normalize stoch aliases to 'stoch:'
    if args.rule:
        if args.rule.lower().startswith('stochastic:'):
            args.rule = 'stoch:' + args.rule.split(':', 1)[1]
        elif args.rule.lower().startswith('stochoscillator:'):
            args.rule = 'stoch:' + args.rule.split(':', 1)[1]
        # Monte Carlo aliases
        elif args.rule.lower().startswith('montecarlo:'):
            args.rule = 'monte:' + args.rule.split(':', 1)[1]
        elif args.rule.lower().startswith('mc:'):
            args.rule = 'monte:' + args.rule.split(':', 1)[1]
        # Fear & Greed aliases
        elif args.rule.lower().startswith('fg:'):
            args.rule = 'feargreed:' + args.rule.split(':', 1)[1]
        # Time Series Forecast aliases
        elif args.rule.lower().startswith('tsforecast:'):
            args.rule = 'tsf:' + args.rule.split(':', 1)[1]

    # Validate rule argument
    if args.rule:
        # Check if it's a parameterized rule
        if ':' in args.rule:
            # Parameterized rule - validate the indicator name part
            indicator_name = args.rule.split(':', 1)[0].lower()
            valid_indicators = ['rsi', 'rsi_mom', 'rsi_div', 'macd', 'stoch', 'stochastic', 'stochoscillator', 'ema', 'bb', 'atr', 'cci', 'vwap', 'pivot', 'hma', 'tsf', 'monte', 'montecarlo', 'kelly', 'putcallratio', 'cot', 'feargreed', 'fg', 'donchain', 'fibo', 'obv', 'stdev', 'adx', 'sar', 'supertrend']
            if indicator_name not in valid_indicators:
                # Provide detailed help for parameterized indicators
                help_info = {
                    'hma': 'HMA (Hull Moving Average): hma:period,price_type (e.g., hma:20,close)',
                    'tsf': 'TSF (Time Series Forecast): tsf:period,price_type (e.g., tsf:20,close)',
                    'monte': 'Monte Carlo: monte:simulations,period (e.g., monte:1000,252)',
                    'kelly': 'Kelly Criterion: kelly:period (e.g., kelly:20)',
                    'putcallratio': 'Put/Call Ratio: putcallratio:period,price_type (e.g., putcallratio:20,close)',
                    'cot': 'COT: cot:period,price_type (e.g., cot:20,close)',
                    'feargreed': 'Fear & Greed: feargreed:period,price_type (e.g., feargreed:20,close)',
                    'donchain': 'Donchian Channel: donchain:period (e.g., donchain:20)',
                    'fibo': 'Fibonacci: fibo:levels or fibo:all (e.g., fibo:0.236,0.382,0.618)',
                    'obv': 'OBV: obv (no parameters needed)',
                    'stdev': 'Standard Deviation: stdev:period,price_type (e.g., stdev:20,close)',
                    'adx': 'ADX: adx:period (e.g., adx:14)',
                    'sar': 'SAR: sar:acceleration,maximum (e.g., sar:0.02,0.2)',
                    'supertrend': 'SuperTrend: supertrend:period,multiplier[,price_type] (e.g., supertrend:10,3.0)',
                    'rsi': 'RSI: rsi:period,price_type (e.g., rsi:14,close)',
                    'macd': 'MACD: macd:fast,slow,signal,price_type (e.g., macd:12,26,9,close)',
                    'stoch': 'Stochastic: stoch:k_period,d_period,price_type (e.g., stoch:14,3,close)',
                    'ema': 'EMA: ema:period,price_type (e.g., ema:20,close)',
                    'bb': 'Bollinger Bands: bb:period,std_dev,price_type (e.g., bb:20,2.0,close)',
                    'atr': 'ATR: atr:period (e.g., atr:14)',
                    'cci': 'CCI: cci:period,price_type (e.g., cci:20,close)',
                    'vwap': 'VWAP: vwap:price_type (e.g., vwap:close)',
                    'pivot': 'Pivot Points: pivot:price_type (e.g., pivot:close)'
                }
                
                if indicator_name in help_info:
                    parser.error(f"Invalid indicator name '{indicator_name}' in parameterized rule '{args.rule}'.\n\n{help_info[indicator_name]}\n\nValid indicators: {', '.join(valid_indicators)}")
                else:
                    parser.error(f"Invalid indicator name '{indicator_name}' in parameterized rule '{args.rule}'. Valid indicators: {', '.join(valid_indicators)}")
        else:
            # Regular rule - validate against choices
            if args.rule not in all_rule_choices:
                # Check if it might be a parameterized indicator
                if args.rule.lower() in ['hma', 'tsf', 'monte', 'montecarlo', 'kelly', 'putcallratio', 'cot', 'feargreed', 'fg', 'donchain', 'fibo', 'obv', 'stdev', 'adx', 'sar', 'supertrend', 'rsi', 'macd', 'stoch', 'stochastic', 'stochoscillator', 'ema', 'bb', 'atr', 'cci', 'vwap', 'pivot']:
                    parser.error(f"Invalid rule '{args.rule}'. This is a parameterized indicator. Use format: {args.rule}:parameters\n\nExamples:\n  {args.rule}:20,close\n  {args.rule}:14,3,close (for stochastic)\n  {args.rule}:1000,252 (for monte carlo)\n\nUse --help for more information about parameterized indicators.")
                else:
                    parser.error(f"Invalid rule '{args.rule}'. Use one of {all_rule_choices}")

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

    # Parse strategy parameters
    if args.strategy:
        try:
            strategy_parts = args.strategy.split(',')
            if len(strategy_parts) != 3:
                parser.error("--strategy must have exactly 3 values: lot_size,risk_reward_ratio,fee_per_trade")
            
            lot_size = float(strategy_parts[0])
            risk_reward_ratio = float(strategy_parts[1])
            fee_per_trade = float(strategy_parts[2])
            
            # Validate strategy parameters
            if lot_size <= 0:
                parser.error("lot_size must be positive")
            if risk_reward_ratio <= 0:
                parser.error("risk_reward_ratio must be positive")
            if fee_per_trade < 0:
                parser.error("fee_per_trade must be non-negative")
            
            # Store parsed values
            args.lot_size = lot_size
            args.risk_reward_ratio = risk_reward_ratio
            args.fee_per_trade = fee_per_trade
            
        except ValueError as e:
            parser.error(f"Invalid strategy parameters: {e}. Use format: lot_size,risk_reward_ratio,fee_per_trade")
    else:
        # Default strategy parameters
        args.lot_size = 1.0
        args.risk_reward_ratio = 2.0
        args.fee_per_trade = 0.07

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

def show_indicator_help(indicator_name: str):
    """
    Show help information for a specific indicator.
    
    Args:
        indicator_name (str): Name of the indicator
    """
    # Use the new enhanced error handling system
    from .error_handling import show_enhanced_indicator_help
    show_enhanced_indicator_help(f"Help requested for indicator: {indicator_name}", indicator_name)
    return
    
    # Legacy help info (kept for reference)
    help_info = {
        'rsi': {
            'name': 'RSI (Relative Strength Index)',
            'format': 'rsi:period,oversold,overbought,price_type',
            'parameters': [
                'period (int): RSI calculation period (default: 14)',
                'oversold (float): Oversold threshold (default: 30)',
                'overbought (float): Overbought threshold (default: 70)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'rsi:14,30,70,open',
                'rsi:21,25,75,close',
                'rsi:14,10,90,open'
            ]
        },
        'rsi_mom': {
            'name': 'RSI Momentum',
            'format': 'rsi_mom:period,oversold,overbought,price_type',
            'parameters': [
                'period (int): RSI calculation period (default: 14)',
                'oversold (float): Oversold threshold (default: 30)',
                'overbought (float): Overbought threshold (default: 70)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'rsi_mom:14,30,70,open',
                'rsi_mom:21,25,75,close',
                'rsi_mom:14,10,90,open'
            ]
        },
        'rsi_div': {
            'name': 'RSI Divergence',
            'format': 'rsi_div:period,oversold,overbought,price_type',
            'parameters': [
                'period (int): RSI calculation period (default: 14)',
                'oversold (float): Oversold threshold (default: 30)',
                'overbought (float): Overbought threshold (default: 70)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'rsi_div:14,30,70,open',
                'rsi_div:21,25,75,close',
                'rsi_div:14,10,90,open'
            ]
        },
        'macd': {
            'name': 'MACD (Moving Average Convergence Divergence)',
            'format': 'macd:fast_period,slow_period,signal_period,price_type',
            'parameters': [
                'fast_period (int): Fast EMA period (default: 12)',
                'slow_period (int): Slow EMA period (default: 26)',
                'signal_period (int): Signal line period (default: 9)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'macd:12,26,9,close',
                'macd:8,21,5,open'
            ]
        },
        'stoch': {
            'name': 'Stochastic',
            'format': 'stoch:k_period,d_period,price_type',
            'parameters': [
                'k_period (int): %K period (default: 14)',
                'd_period (int): %D period (default: 3)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'stoch:14,3,close',
                'stoch:21,5,open'
            ]
        },
        'stochoscillator': 'stoch',  # Алиас, чтобы не было отдельного help
        'ema': {
            'name': 'EMA (Exponential Moving Average)',
            'format': 'ema:period,price_type',
            'parameters': [
                'period (int): EMA period (default: 20)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'ema:20,close',
                'ema:50,open'
            ]
        },
        'bb': {
            'name': 'Bollinger Bands',
            'format': 'bb:period,std_dev,price_type',
            'parameters': [
                'period (int): Moving average period (default: 20)',
                'std_dev (float): Standard deviation multiplier (default: 2.0)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'bb:20,2.0,close',
                'bb:20,2.5,open'
            ]
        },
        'atr': {
            'name': 'ATR (Average True Range)',
            'format': 'atr:period',
            'parameters': [
                'period (int): ATR period (default: 14)'
            ],
            'examples': [
                'atr:14',
                'atr:21'
            ]
        },
        'cci': {
            'name': 'CCI (Commodity Channel Index)',
            'format': 'cci:period,price_type',
            'parameters': [
                'period (int): CCI period (default: 20)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'cci:20,close',
                'cci:14,open'
            ]
        },
        'vwap': {
            'name': 'VWAP (Volume Weighted Average Price)',
            'format': 'vwap:price_type',
            'parameters': [
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'vwap:close',
                'vwap:open'
            ]
        },
        'pivot': {
            'name': 'Pivot Points',
            'format': 'pivot:price_type',
            'parameters': [
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'pivot:close',
                'pivot:open'
            ]
        },
        'hma': {
            'name': 'HMA (Hull Moving Average)',
            'format': 'hma:period,price_type',
            'parameters': [
                'period (int): HMA period (default: 20)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'hma:20,close',
                'hma:50,open'
            ]
        },
        'tsf': {
            'name': 'TSF (Time Series Forecast)',
            'format': 'tsf:period,price_type',
            'parameters': [
                'period (int): TSF period (default: 14)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'tsf:14,close',
                'tsf:20,open'
            ]
        },
        'monte': {
            'name': 'Monte Carlo Simulation',
            'format': 'monte:simulations,period',
            'parameters': [
                'simulations (int): Number of simulations (default: 1000)',
                'period (int): Simulation period (default: 252)'
            ],
            'examples': [
                'monte:1000,252',
                'monte:500,126'
            ]
        },
        'kelly': {
            'name': 'Kelly Criterion',
            'format': 'kelly:period',
            'parameters': [
                'period (int): Kelly period (default: 20)'
            ],
            'examples': [
                'kelly:20',
                'kelly:14'
            ]
        },
        'donchain': {
            'name': 'Donchian Channels',
            'format': 'donchain:period',
            'parameters': [
                'period (int): Donchian period (default: 20)'
            ],
            'examples': [
                'donchain:20',
                'donchain:14'
            ]
        },
        'fibo': {
            'name': 'Fibonacci Retracements',
            'format': 'fibo:level1,level2,level3,...',
            'parameters': [
                'level1,level2,level3,... (float): Fibonacci retracement levels (default: 0.236,0.382,0.5,0.618,0.786)'
            ],
            'examples': [
                'fibo:0.236,0.382,0.5,0.618,0.786',
                'fibo:0.236,0.5,0.786'
            ]
        },
        'obv': {
            'name': 'OBV (On-Balance Volume)',
            'format': 'obv',
            'parameters': [
                'None required'
            ],
            'examples': [
                'obv'
            ]
        },
        'stdev': {
            'name': 'Standard Deviation',
            'format': 'stdev:period,price_type',
            'parameters': [
                'period (int): Standard deviation period (default: 20)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'stdev:20,close',
                'stdev:14,open'
            ]
        },
        'adx': {
            'name': 'ADX (Average Directional Index)',
            'format': 'adx:period',
            'parameters': [
                'period (int): ADX period (default: 14)'
            ],
            'examples': [
                'adx:14',
                'adx:21'
            ]
        },
        'sar': {
            'name': 'SAR (Parabolic SAR)',
            'format': 'sar:acceleration,maximum',
            'parameters': [
                'acceleration (float): Acceleration factor (default: 0.02)',
                'maximum (float): Maximum acceleration (default: 0.2)'
            ],
            'examples': [
                'sar:0.02,0.2',
                'sar:0.01,0.1'
            ]
        },
        'supertrend': {
            'name': 'SuperTrend',
            'format': 'supertrend:period,multiplier[,price_type]',
            'parameters': [
                'period (int): ATR period for SuperTrend calculation (required)',
                'multiplier (float): ATR multiplier (required)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'supertrend:10,3.0',
                'supertrend:14,2.5,close',
                'supertrend:10,3.0,open',
                'supertrend:50,2.5,close'
            ]
        },
        'putcallratio': {
            'name': 'Put/Call Ratio',
            'format': 'putcallratio:period,price_type[,bullish_threshold,bearish_threshold]',
            'parameters': [
                'period (int): Put/Call Ratio period (default: 20)',
                'price_type (string): Price type for calculation - open or close (default: close)',
                'bullish_threshold (float): Bullish threshold (default: 60.0)',
                'bearish_threshold (float): Bearish threshold (default: 40.0)'
            ],
            'examples': [
                'putcallratio:20,close,60.0,40.0',
                'putcallratio:14,open,60.0,40.0'
            ]
        },
        'cot': {
            'name': 'COT (Commitment of Traders)',
            'format': 'cot:period,price_type',
            'parameters': [
                'period (int): COT period (default: 20)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'cot:20,close',
                'cot:14,open'
            ]
        },
        'feargreed': {
            'name': 'Fear & Greed Index',
            'format': 'feargreed:period,price_type',
            'parameters': [
                'period (int): Fear & Greed calculation period (default: 14)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'feargreed:14,close',
                'feargreed:21,open',
                'feargreed:10,close'
            ]
        },
        'fg': {
            'name': 'Fear & Greed Index (alias)',
            'format': 'fg:period,price_type',
            'parameters': [
                'period (int): Fear & Greed calculation period (default: 14)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'fg:14,close',
                'fg:21,open',
                'fg:10,close'
            ]
        }
    }
    
    if indicator_name.lower() not in help_info:
        print(f"Unknown indicator: {indicator_name}")
        print(f"Available indicators: {', '.join(help_info.keys())}")
        return
    
    info = help_info[indicator_name.lower()]
    
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{info['name']} Help{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Format:{Style.RESET_ALL} {info['format']}")
    print(f"{Fore.CYAN}Parameters:{Style.RESET_ALL}")
    for param in info['parameters']:
        print(f"  • {param}")
    print(f"{Fore.CYAN}Examples:{Style.RESET_ALL}")
    for example in info['examples']:
        print(f"  • {example}")
    print()


def parse_rsi_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI parameters: period,oversold,overbought,price_type"""
    params = params_str.split(',')
    if len(params) != 4:
        raise ValueError(f"RSI requires exactly 4 parameters: period,oversold,overbought,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values like 14.0
        oversold = float(params[1].strip())
        overbought = float(params[2].strip())
        price_type = params[3].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid RSI parameters: {params_str}. Error: {e}")
    
    # Validate period
    if period <= 0:
        raise ValueError(f"RSI period must be a positive integer, got: {period}")
    
    # Validate thresholds
    if oversold < 0 or oversold > 100:
        raise ValueError(f"RSI oversold must be between 0 and 100, got: {oversold}")
    
    if overbought < 0 or overbought > 100:
        raise ValueError(f"RSI overbought must be between 0 and 100, got: {overbought}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"RSI price_type must be 'open' or 'close', got: {price_type}")
    
    return 'rsi', {
        'rsi_period': period,
        'oversold': oversold,
        'overbought': overbought,
        'price_type': price_type
    }


def parse_rsi_momentum_parameters(params_str: str) -> tuple[str, dict]:
    # Exactly the same parameters as RSI, but different name
    name, params = parse_rsi_parameters(params_str)
    return 'rsi_mom', params


def parse_rsi_divergence_parameters(params_str: str) -> tuple[str, dict]:
    # Exactly the same parameters as RSI, but different name
    name, params = parse_rsi_parameters(params_str)
    return 'rsi_div', params


def parse_macd_parameters(params_str: str) -> tuple[str, dict]:
    """Parse MACD parameters: fast_period,slow_period,signal_period,price_type"""
    params = params_str.split(',')
    if len(params) != 4:
        raise ValueError(f"MACD requires exactly 4 parameters: fast_period,slow_period,signal_period,price_type. Got: {params_str}")
    
    try:
        fast_period = int(float(params[0].strip()))  # Handle float values
        slow_period = int(float(params[1].strip()))
        signal_period = int(float(params[2].strip()))
        price_type = params[3].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid MACD parameters: {params_str}. Error: {e}")
    
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
    
    try:
        k_period = int(float(params[0].strip()))  # Handle float values
        d_period = int(float(params[1].strip()))
        price_type = params[2].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Stochastic parameters: {params_str}. Error: {e}")
    
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
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid EMA parameters: {params_str}. Error: {e}")
    
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
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        std_dev = float(params[1].strip())
        price_type = params[2].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Bollinger Bands parameters: {params_str}. Error: {e}")
    
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
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid ATR parameters: {params_str}. Error: {e}")
    
    return 'atr', {
        'atr_period': period
    }


def parse_cci_parameters(params_str: str) -> tuple[str, dict]:
    """Parse CCI parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"CCI requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid CCI parameters: {params_str}. Error: {e}")
    
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
    
    try:
        price_type = params[0].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid VWAP parameters: {params_str}. Error: {e}")
    
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
    
    try:
        price_type = params[0].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Pivot Points parameters: {params_str}. Error: {e}")
    
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
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid HMA parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"HMA price_type must be 'open' or 'close', got: {price_type}")
    
    return 'hma', {
        'hma_period': period,
        'price_type': price_type
    }


def parse_tsf_parameters(params_str: str) -> tuple[str, dict]:
    """Parse TSF parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"TSF requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid TSF parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"TSF price_type must be 'open' or 'close', got: {price_type}")
    
    return 'tsf', {
        'tsforecast_period': period,
        'price_type': price_type
    }


def parse_monte_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Monte Carlo parameters: simulations,period"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"Monte Carlo requires exactly 2 parameters: simulations,period. Got: {params_str}")
    
    try:
        simulations = int(float(params[0].strip()))  # Handle float values
        period = int(float(params[1].strip()))
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Monte Carlo parameters: {params_str}. Error: {e}")
    
    return 'monte', {
        'simulations': simulations,
        'period': period
    }


def parse_kelly_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Kelly Criterion parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"Kelly Criterion requires exactly 1 parameter: period. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Kelly Criterion parameters: {params_str}. Error: {e}")
    
    return 'kelly', {
        'kelly_period': period
    }


def parse_donchain_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Donchian Channels parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"Donchian Channels requires exactly 1 parameter: period. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Donchian Channels parameters: {params_str}. Error: {e}")
    
    return 'donchain', {
        'donchain_period': period
    }


def parse_fibo_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Fibonacci Retracements parameters: levels or 'all'"""
    params = params_str.split(',')
    if len(params) < 1:
        raise ValueError(f"Fibonacci Retracements requires at least 1 parameter: levels or 'all'. Got: {params_str}")
    
    # Check if first parameter is 'all'
    if params[0].strip().lower() == 'all':
        # Use all standard Fibonacci levels
        levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    else:
        # Parse custom Fibonacci levels
        try:
            levels = [float(p.strip()) for p in params]
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid Fibonacci Retracements parameters: {params_str}. Error: {e}")
    
    return 'fibo', {
        'fib_levels': levels
    }


def parse_obv_parameters(params_str: str) -> tuple[str, dict]:
    """Parse OBV parameters: none required"""
    # Allow empty parameters after colon (e.g., "obv:")
    if params_str.strip():
        # If there are actual parameters, show help
        raise ValueError(f"OBV does not require parameters. Got: {params_str}")
    
    return 'obv', {}


def parse_stdev_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Standard Deviation parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"Standard Deviation requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Standard Deviation parameters: {params_str}. Error: {e}")
    
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
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid ADX parameters: {params_str}. Error: {e}")
    
    return 'adx', {
        'adx_period': period
    }


def parse_sar_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SAR parameters: acceleration,maximum"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"SAR requires exactly 2 parameters: acceleration,maximum. Got: {params_str}")
    
    try:
        acceleration = float(params[0].strip())
        maximum = float(params[1].strip())
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid SAR parameters: {params_str}. Error: {e}")
    
    return 'sar', {
        'sar_acceleration': acceleration,
        'sar_maximum': maximum
    }


def parse_supertrend_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SuperTrend parameters: period,multiplier[,price_type]"""
    # Handle empty string case
    if not params_str.strip():
        raise ValueError(f"SuperTrend requires exactly 2-3 parameters: period,multiplier[,price_type]. Got: {params_str}")
    
    params = params_str.split(',')
    if len(params) < 2 or len(params) > 3:
        raise ValueError(f"SuperTrend requires exactly 2-3 parameters: period,multiplier[,price_type]. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        multiplier = float(params[1].strip())
        price_type = params[2].strip().lower() if len(params) > 2 else 'close'
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid SuperTrend parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"SuperTrend price_type must be 'open' or 'close', got: {price_type}")
    
    return 'supertrend', {
        'supertrend_period': period,
        'multiplier': multiplier,
        'price_type': price_type
    }


def parse_putcallratio_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Put/Call Ratio parameters: period,price_type[,bullish_threshold,bearish_threshold]"""
    params = params_str.split(',')
    if len(params) < 2 or len(params) > 4:
        raise ValueError(f"Put/Call Ratio requires 2-4 parameters: period,price_type[,bullish_threshold,bearish_threshold]. Got: {params_str}")
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
        bullish_threshold = float(params[2].strip()) if len(params) > 2 else 60.0
        bearish_threshold = float(params[3].strip()) if len(params) > 3 else 40.0
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Put/Call Ratio parameters: {params_str}. Error: {e}")
    if price_type not in ['open', 'close']:
        raise ValueError(f"Put/Call Ratio price_type must be 'open' or 'close', got: {price_type}")
    return 'putcallratio', {
        'putcall_period': period,
        'price_type': price_type,
        'bullish_threshold': bullish_threshold,
        'bearish_threshold': bearish_threshold
    }


def parse_cot_parameters(params_str: str) -> tuple[str, dict]:
    """Parse COT parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"COT requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid COT parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"COT price_type must be 'open' or 'close', got: {price_type}")
    
    return 'cot', {
        'cot_period': period,
        'price_type': price_type
    }


def parse_feargreed_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Fear & Greed parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"Fear & Greed requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Fear & Greed parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Fear & Greed price_type must be 'open' or 'close', got: {price_type}")
    
    return 'feargreed', {
        'feargreed_period': period,
        'price_type': price_type
    }


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
        if indicator_name in ['stoch', 'stochastic', 'stochoscillator']:
            # Always parse as stoch and return 'stoch' as indicator name
            _, params = parse_stoch_parameters(params_str)
            return 'stoch', params
        elif indicator_name in ['monte', 'montecarlo', 'mc']:
            # Always parse as monte and return 'monte' as indicator name
            _, params = parse_monte_parameters(params_str)
            return 'monte', params
        elif indicator_name in ['feargreed', 'fg']:
            # Always parse as feargreed and return 'feargreed' as indicator name
            _, params = parse_feargreed_parameters(params_str)
            return 'feargreed', params
        elif indicator_name in ['tsf', 'tsforecast']:
            # Always parse as tsf and return 'tsf' as indicator name
            _, params = parse_tsf_parameters(params_str)
            return 'tsf', params
        elif indicator_name == 'rsi':
            return parse_rsi_parameters(params_str)
        elif indicator_name == 'rsi_mom':
            return parse_rsi_momentum_parameters(params_str)
        elif indicator_name == 'rsi_div':
            return parse_rsi_divergence_parameters(params_str)
        elif indicator_name == 'macd':
            return parse_macd_parameters(params_str)
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
        elif indicator_name == 'supertrend':
            return parse_supertrend_parameters(params_str)
        elif indicator_name == 'putcallratio':
            return parse_putcallratio_parameters(params_str)
        elif indicator_name == 'cot':
            return parse_cot_parameters(params_str)
        else:
            # Unknown indicator, show help and raise error
            raise ValueError(f"Unknown indicator: {indicator_name}")
            
    except Exception as e:
        # Показываем cool help для параметризованных индикаторов при любой ошибке разбора
        from .cli import show_indicator_help
        indicator_name = rule_str.split(':', 1)[0].lower().strip()
        show_indicator_help(indicator_name)
        # После показа help завершаем выполнение с ошибкой
        import sys
        sys.exit(1)
