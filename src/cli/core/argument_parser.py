# -*- coding: utf-8 -*-
# src/cli/core/argument_parser.py

"""
Argument parser setup and configuration for CLI.
"""

import argparse
import textwrap
import sys
from colorama import init, Fore, Style

from src.calculation.indicators.trend.wave_ind import ENUM_MOM_TR, ENUM_GLOBAL_TR
from src.cli.indicators.indicators_search import IndicatorSearcher
from .help_formatter import ColoredHelpFormatter

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Use absolute imports for constants and version within the src package
from src.common.constants import TradingRule
from src import __version__


def show_cool_version():
    """Display the most epic, modern techno-style version banner with insane animations and sounds!"""
    import time
    import os
    import threading
    import random
    from datetime import datetime
    
    
    
    def glitch_effect(text, intensity=3):
        """Add cyberpunk glitch effect to text."""
        glitched = ''
        for char in text:
            if random.random() < 0.05 * intensity:
                # Random glitch characters
                glitched += random.choice(['█', '▓', '▒', '░', '▀', '▄', '▌', '▐'])
            else:
                glitched += char
        return glitched
    
    def typewriter_effect(text, delay=0.0025):
        """Ultra fast typewriter effect."""
        for i in range(len(text) + 1):
            print('\r' + text[:i] + ('█' if i < len(text) else ''), end='', flush=True)
            time.sleep(delay)
        print()  # New line after typing
    
    
    
    
    # No sounds - clean and fast
    
    # Clear screen for maximum effect
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Epic loading sequence
    loading_messages = [
        f'{Fore.GREEN}[SYSTEM]{Style.RESET_ALL} Initializing NeoZorK HLD System...',
        f'{Fore.CYAN}[CORE]{Style.RESET_ALL} Loading Advanced ML Algorithms...',
        f'{Fore.YELLOW}[AI]{Style.RESET_ALL} Quantum Financial Analysis Engine Online...',
        f'{Fore.RED}[SECURITY]{Style.RESET_ALL} Cybersecurity Protocols Activated...',
        f'{Fore.MAGENTA}[READY]{Style.RESET_ALL} All Systems Operational!'
    ]
    
    for msg in loading_messages:
        typewriter_effect(msg, 0.02)
        time.sleep(0.3)
    
    # Clean direct transition to logo
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Epic animated logo reveal - all lines must be exactly 60 characters
    ascii_lines = [
        '███╗   ██╗███████╗ ██████╗ ███████╗ ██████╗ ██████╗ ██╗  ██╗',
        '████╗  ██║██╔════╝██╔═══██╗╚══███╔╝██╔═══██╗██╔══██╗██║ ██╔╝',
        '██╔██╗ ██║█████╗  ██║   ██║  ███╔╝ ██║   ██║██████╔╝█████╔╝ ',
        '██║╚██╗██║██╔══╝  ██║   ██║ ███╔╝  ██║   ██║██╔══██╗██╔═██╗ ',
        '██║ ╚████║███████╗╚██████╔╝███████╗╚██████╔╝██║  ██║██║  ██╗',
        '╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝'
    ]
    
    # Top border - ultra fast animation
    border = '╔══════════════════════════════════════════════════════════════╗'
    for i in range(len(border)):
        print('\r' + border[:i+1], end='', flush=True)
        time.sleep(0.0018)  # 12x faster total (3x * 4x)
    print()
    
    # Animate ASCII art line by line with color transitions
    colors = ['\033[38;5;46m', '\033[38;5;82m', '\033[38;5;118m', '\033[38;5;154m', '\033[38;5;190m', '\033[38;5;226m']
    
    for i, ascii_line in enumerate(ascii_lines):
        # Add glitch effect occasionally
        if random.random() > 0.7:
            glitched_line = glitch_effect(ascii_line, 2)
            # Properly aligned glitched line
            full_line = f'{Fore.CYAN}║{Style.RESET_ALL}  {colors[i]}{Style.BRIGHT}{glitched_line}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}'
            print(full_line)
            time.sleep(0.05)
            # Show correct line after glitch
            print('\r' + ' ' * 66 + '\r', end='')
        
        # Character by character reveal with proper alignment
        revealed_chars = ''
        for char in ascii_line:
            revealed_chars += char
            # Build display line maintaining exactly 66 characters total
            # Format: '║  ' + ascii_content + ' ' + '║' = 66 chars total
            display_line = f'{Fore.CYAN}║{Style.RESET_ALL}  {colors[i]}{Style.BRIGHT}{revealed_chars}{Style.RESET_ALL}'
            remaining_spaces = 60 - len(revealed_chars)  # 60 = space for content inside borders
            display_line += ' ' * remaining_spaces + f' {Fore.CYAN}║{Style.RESET_ALL}'
            print('\r' + display_line, end='', flush=True)
            time.sleep(0.0008)  # 12x faster total
        print()
        time.sleep(0.008)  # 12x faster total
    
    # Middle border - fast
    border = '╠══════════════════════════════════════════════════════════════╣'
    for i in range(len(border)):
        print('\r' + border[:i+1], end='', flush=True)
        time.sleep(0.0008)  # 12x faster total
    print()
    
    # Info section with epic effects
    info_lines = [
        f'{Fore.YELLOW}{Style.BRIGHT}Shcherbyna Pressure Vector Indicator{Style.RESET_ALL}',
        f'{Fore.GREEN}{Style.BRIGHT}Advanced Financial Analysis System{Style.RESET_ALL}',
        f'{Fore.RED}{Style.BRIGHT}Version: {__version__}{Style.RESET_ALL}',
        f'{Fore.BLUE}{Style.BRIGHT}Powered by Advanced ML & Technical Analysis{Style.RESET_ALL}'
    ]
    
    for text in info_lines:
        # Calculate clean text length without color codes
        clean_text = text.replace(Style.BRIGHT, '').replace(Style.RESET_ALL, '').replace(Fore.YELLOW, '').replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Fore.BLUE, '')
        clean_text_len = len(clean_text)
        needed_spaces = 60 - clean_text_len  # 60 = space for content inside borders
        if needed_spaces < 0:
            needed_spaces = 0
        line = f'{Fore.CYAN}║{Style.RESET_ALL}  {text}' + ' ' * needed_spaces + f' {Fore.CYAN}║{Style.RESET_ALL}'
        typewriter_effect(line, 0.0018)  # 12x faster total
        time.sleep(0.018)  # 12x faster total
    
    # Second middle border - fast
    border = '╠══════════════════════════════════════════════════════════════╣'
    for i in range(len(border)):
        print('\r' + border[:i+1], end='', flush=True)
        time.sleep(0.0008)  # 12x faster total
    print()
    
    # Status section with pulsing effects
    status_lines = [
        f'⚡ Ready for high-frequency trading analysis ⚡',
        f'🔮 Predicting market movements with precision 🔮', 
        f'🚀 Optimized for performance and accuracy 🚀'
    ]
    
    for text in status_lines:
        # Calculate proper alignment for 66 total chars
        # Remove emojis for length calculation and account for their display width
        clean_text = text.replace('⚡', '').replace('🔮', '').replace('🚀', '').strip()
        emoji_count = text.count('⚡') + text.count('🔮') + text.count('🚀')
        # Each emoji displays as 2 characters visually
        actual_display_len = len(clean_text) + emoji_count * 2
        needed_spaces = 60 - actual_display_len  # 60 = space for content inside borders
        if needed_spaces < 0:
            needed_spaces = 0
        line = f'{Fore.CYAN}║{Style.RESET_ALL}  {Style.BRIGHT}{text}{Style.RESET_ALL}' + ' ' * needed_spaces + f' {Fore.CYAN}║{Style.RESET_ALL}'
        print(line)
        time.sleep(0.018)  # 12x faster total
    
    # Bottom border - fast
    border = '╚══════════════════════════════════════════════════════════════╝'
    for i in range(len(border)):
        print('\r' + border[:i+1], end='', flush=True)
        time.sleep(0.0008)  # 12x faster total
    print()
    
    # Clean ending - no final messages
    print()
    
    print('\n')


def create_argument_parser():
    """Creates and configures the argument parser."""
    
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
    required_group.add_argument('mode', nargs='?', choices=['demo', 'yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'show', 'interactive'],
                                help="Operating mode: 'demo', 'yfinance'/'yf', 'csv', 'polygon', 'binance', 'exrate', 'show', 'interactive'. Not required when using --interactive flag.")

    # --- Show Mode Positional Arguments ---
    parser.add_argument('show_args', nargs='*', default=[],
                        help=argparse.SUPPRESS)  # Hide from help but collect positional args after 'mode'

    # --- Data Source Specific Options Group ---
    data_source_group = parser.add_argument_group('Data Source Options')
    # CSV options
    data_source_group.add_argument('--csv-file', metavar='PATH',
                                   help="Path to input CSV file (required for 'csv' mode when processing single file)")
    data_source_group.add_argument('--csv-folder', metavar='PATH',
                                   help="Path to folder containing CSV files (required for 'csv' mode when processing multiple files)")
    data_source_group.add_argument('--csv-mask', metavar='MASK',
                                   help="Optional mask to filter CSV files by name (case-insensitive, used with --csv-folder)")
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
    all_rule_choices = rule_names + list(rule_aliases_map.keys()) + ['OHLCV', 'AUTO']
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
                              help="Export indicators to parquet format (../data/indicators/parquet/)")
    output_group.add_argument('--export-csv',
                              action='store_true',
                              help="Export indicators to CSV format (../data/indicators/csv/)")
    output_group.add_argument('--export-json',
                              action='store_true',
                              help="Export indicators to JSON format (../data/indicators/json/)")
    output_group.add_argument('--export-indicators-info',
                              action='store_true',
                              help="Export indicator metadata to JSON format (../data/indicators/metadata/)")

    # --- Other Options Group ---
    other_group = parser.add_argument_group('Other Options')
    other_group.add_argument('-h', action='help', default=argparse.SUPPRESS,
                             help='Show this help message and exit')
    other_group.add_argument('--version', action='store_true',
                             help="Show program version and exit")

    return parser


def parse_arguments():
    """Sets up argument parser using ColoredHelpFormatter and returns the parsed arguments."""
    
    parser = create_argument_parser()
    
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
            
        # Handle --version flag before parsing to avoid mode requirement
        if '--version' in sys.argv:
            show_cool_version()
            sys.exit(0)

        # Handle special flags that don't require mode argument BEFORE parsing
        try:
            from .special_flags_handler import handle_special_flags
            if handle_special_flags():
                return  # Special flag was handled, exit
        except ImportError:
            # Fallback if special flags handler is not available
            pass
            
        # Now parse arguments for normal operation
        args = parser.parse_args()
    except SystemExit as e:
        if e.code != 0:
            print(f"Argument parsing error (Code: {e.code}). Exiting.", file=sys.stderr)
        sys.exit(e.code)

    return args
