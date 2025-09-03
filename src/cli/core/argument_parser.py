# -*- coding: utf-8 -*-
# src/cli/core/argument_parser.py

"""
Argument parser setup and configuration for CLI.

This module provides argument parsing functionality for the NeoZorK HLD Prediction tool,
including a sophisticated version banner display system and comprehensive CLI argument handling.
"""

import argparse
import os
import random
import sys
import textwrap
import time
from datetime import datetime

from colorama import Fore, Style, init

from src import __version__
from src.calculation.indicators.trend.wave_ind import ENUM_GLOBAL_TR, ENUM_MOM_TR
from src.cli.indicators.indicators_search import IndicatorSearcher
from src.common.constants import TradingRule

from .help_formatter import ColoredHelpFormatter

# Initialize colorama for cross-platform colored output
init(autoreset=True)


# ============================================================================
# VERSION BANNER DISPLAY SYSTEM
# ============================================================================

class VersionBannerDisplay:
    """Handles the display of the version banner with animations and effects."""
    
    # Animation timing constants (100x faster than original)
    BORDER_ANIMATION_DELAY = 0.00018
    ASCII_ANIMATION_DELAY = 0.0000008
    ASCII_LINE_DELAY = 0.000008
    TYPEWRITER_DELAY = 0.0000018
    INFO_LINE_DELAY = 0.000018
    STATUS_LINE_DELAY = 0.000018
    LOADING_MESSAGE_DELAY = 0.02
    LOADING_PAUSE_DELAY = 0.02
    
    # ASCII art for NEOZORK logo (60 characters each line)
    ASCII_LOGO_LINES = [
        '███╗   ██╗███████╗ ██████╗ ███████╗ ██████╗ ██████╗ ██╗  ██╗',
        '████╗  ██║██╔════╝██╔═══██╗╚══███╔╝██╔═══██╗██╔══██╗██║ ██╔╝',
        '██╔██╗ ██║█████╗  ██║   ██║  ███╔╝ ██║   ██║██████╔╝█████╔╝ ',
        '██║╚██╗██║██╔══╝  ██║   ██║ ███╔╝  ██║   ██║██╔══██╗██╔═██╗ ',
        '██║ ╚████║███████╗╚██████╔╝███████╗╚██████╔╝██║  ██║██║  ██╗',
        '╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝'
    ]
    
    # Color palette for ASCII art animation
    ASCII_COLORS = [
        '\033[38;5;46m', '\033[38;5;82m', '\033[38;5;118m',
        '\033[38;5;154m', '\033[38;5;190m', '\033[38;5;226m'
    ]
    
    # Loading messages for system initialization
    LOADING_MESSAGES = [
        f'{Fore.GREEN}[SYSTEM]{Style.RESET_ALL} Initializing NeoZorK HLD System...',
        f'{Fore.CYAN}[CORE]{Style.RESET_ALL} Loading Advanced ML Algorithms...',
        f'{Fore.YELLOW}[AI]{Style.RESET_ALL} Quantum Financial Analysis Engine Online...',
        f'{Fore.RED}[SECURITY]{Style.RESET_ALL} Cybersecurity Protocols Activated...',
        f'{Fore.MAGENTA}[READY]{Style.RESET_ALL} All Systems Operational!'
    ]
    
    # Information lines for the banner
    INFO_LINES = [
        f'{Fore.YELLOW}{Style.BRIGHT}Shcherbyna Pressure Vector Indicator{Style.RESET_ALL}',
        f'{Fore.GREEN}{Style.BRIGHT}Advanced Financial Analysis System{Style.RESET_ALL}',
        f'{Fore.RED}{Style.BRIGHT}Version: {__version__}{Style.RESET_ALL}',
        f'{Fore.BLUE}{Style.BRIGHT}Powered by Advanced ML & Technical Analysis{Style.RESET_ALL}'
    ]
    
    # Status lines with emojis
    STATUS_LINES = [
        f'⚡ Ready for high-frequency trading analysis ⚡',
        f'🔮 Predicting market movements with precision 🔮',
        f'🚀 Optimized for performance and accuracy 🚀'
    ]
    
    @staticmethod
    def create_aligned_line(text: str, clean_text_len: int, total_width: int = 66, 
                           move_border_left: int = 0, move_border_right: int = 0) -> str:
        """Create perfectly aligned line with exact width."""
        content_width = 60 - move_border_left + move_border_right
        needed_spaces = max(0, content_width - clean_text_len)
        return f'{Fore.CYAN}║{Style.RESET_ALL}  {text}' + ' ' * needed_spaces + f' {Fore.CYAN}║{Style.RESET_ALL}'
    
    @staticmethod
    def glitch_effect(text: str, intensity: int = 3) -> str:
        """Add cyberpunk glitch effect to text."""
        glitch_chars = ['█', '▓', '▒', '░', '▀', '▄', '▌', '▐']
        return ''.join(
            random.choice(glitch_chars) if random.random() < 0.05 * intensity else char
            for char in text
        )
    
    @staticmethod
    def typewriter_effect(text: str, delay: float = 0.00025) -> None:
        """Ultra fast typewriter effect with border symbols."""
        for i in range(len(text) + 1):
            print('\r' + text[:i] + ('█' if i < len(text) else ''), end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def typewriter_effect_clean(text: str, delay: float = 0.0025) -> None:
        """Ultra fast typewriter effect without border symbols."""
        for i in range(len(text) + 1):
            print('\r' + text[:i], end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def animate_border(border: str, delay: float) -> None:
        """Animate border drawing."""
        for i in range(len(border)):
            print('\r' + border[:i+1], end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def animate_ascii_art() -> None:
        """Animate ASCII art with color transitions."""
        for i, ascii_line in enumerate(VersionBannerDisplay.ASCII_LOGO_LINES):
            # Character by character reveal with perfect alignment
            revealed_chars = ''
            for char in ascii_line:
                revealed_chars += char
                colored_text = f'{VersionBannerDisplay.ASCII_COLORS[i]}{Style.BRIGHT}{revealed_chars}{Style.RESET_ALL}'
                display_line = VersionBannerDisplay.create_aligned_line(colored_text, len(revealed_chars))
                print('\r' + display_line, end='', flush=True)
                time.sleep(VersionBannerDisplay.ASCII_ANIMATION_DELAY)
            print()
            time.sleep(VersionBannerDisplay.ASCII_LINE_DELAY)
    
    @staticmethod
    def display_info_section() -> None:
        """Display information section with typewriter effect."""
        for text in VersionBannerDisplay.INFO_LINES:
            # Calculate clean text length without color codes
            clean_text = text.replace(Style.BRIGHT, '').replace(Style.RESET_ALL, '')
            for color in [Fore.YELLOW, Fore.GREEN, Fore.RED, Fore.BLUE]:
                clean_text = clean_text.replace(color, '')
            clean_text_len = len(clean_text)
            
            line = VersionBannerDisplay.create_aligned_line(text, clean_text_len, move_border_right=0)
            VersionBannerDisplay.typewriter_effect_clean(line, VersionBannerDisplay.TYPEWRITER_DELAY)
            time.sleep(VersionBannerDisplay.INFO_LINE_DELAY)
    
    @staticmethod
    def display_status_section() -> None:
        """Display status section with emoji handling."""
        for text in VersionBannerDisplay.STATUS_LINES:
            # Calculate proper alignment accounting for emoji display width
            clean_text = text.replace('⚡', '').replace('🔮', '').replace('🚀', '').strip()
            emoji_count = text.count('⚡') + text.count('🔮') + text.count('🚀')
            actual_display_len = len(clean_text) + emoji_count * 2  # Each emoji displays as 2 chars
            
            line = VersionBannerDisplay.create_aligned_line(
                f'{Style.BRIGHT}{text}{Style.RESET_ALL}', 
                actual_display_len, 
                move_border_left=2
            )
            print(line)
            time.sleep(VersionBannerDisplay.STATUS_LINE_DELAY)
    
    @classmethod
    def display_banner(cls) -> None:
        """Display the complete version banner with all animations."""
        # Clear screen for maximum effect
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Display loading sequence
        for msg in cls.LOADING_MESSAGES:
            cls.typewriter_effect(msg, cls.LOADING_MESSAGE_DELAY)
            time.sleep(cls.LOADING_PAUSE_DELAY)
        
        # Clean transition to logo
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Top border
        cls.animate_border('╔═══════════════════════════════════════════════════════════════╗', 
                          cls.BORDER_ANIMATION_DELAY)
        
        # ASCII art animation
        cls.animate_ascii_art()
        
        # Middle border
        cls.animate_border('╠═══════════════════════════════════════════════════════════════╣', 
                          cls.ASCII_ANIMATION_DELAY)
        
        # Information section
        cls.display_info_section()
        
        # Second middle border
        cls.animate_border('╠═══════════════════════════════════════════════════════════════╣', 
                          cls.ASCII_ANIMATION_DELAY)
        
        # Status section
        cls.display_status_section()
        
        # Bottom border
        cls.animate_border('╚═══════════════════════════════════════════════════════════════╝', 
                          cls.ASCII_ANIMATION_DELAY)
        
        # Clean ending
        print('\n')


# ============================================================================
# ARGUMENT PARSER CONFIGURATION
# ============================================================================

class ArgumentParserConfig:
    """Configuration class for argument parser setup."""
    
    # Trading rule aliases mapping
    RULE_ALIASES_MAP = {
        'PHLD': 'Predict_High_Low_Direction',
        'PV': 'Pressure_Vector',
        'SR': 'Support_Resistants',
        'BB': 'Bollinger_Bands'
    }
    
    # Available modes
    AVAILABLE_MODES = ['demo', 'yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'show', 'interactive']
    
    # Data source choices
    DATA_SOURCE_CHOICES = ['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'ind']
    
    # Drawing method choices
    DRAW_CHOICES = ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term']
    
    # Price type choices
    PRICE_TYPE_CHOICES = ['open', 'close']
    
    @classmethod
    def get_main_description(cls) -> str:
        """Get the main description for the argument parser."""
        return textwrap.dedent(f"""
           {Fore.CYAN}{Style.BRIGHT}Shcherbyna Pressure Vector Indicator Analysis Tool{Style.RESET_ALL}
           
           Calculate and plot pressure vector indicators from multiple data sources: demo data, Yahoo Finance, CSV files, Polygon.io, Binance, and Exchange Rate API. Export calculated indicators in parquet, CSV, or JSON formats.
           
           {Fore.YELLOW}Quick Start:{Style.RESET_ALL}
             python run_analysis.py --indicators                    # List all available indicators
             python run_analysis.py --metric                        # Show trading metrics encyclopedia
             python run_analysis.py demo --rule RSI                 # Run with demo data and RSI indicator
             python run_analysis.py interactive                     # Start interactive mode
           """).strip()
    
    @classmethod
    def get_all_rule_choices(cls) -> list:
        """Get all available rule choices including aliases."""
        rule_names = list(TradingRule.__members__.keys())
        return rule_names + list(cls.RULE_ALIASES_MAP.keys()) + ['OHLCV', 'AUTO']


class ArgumentGroupBuilder:
    """Builder class for creating argument groups."""
    
    @staticmethod
    def add_examples_option(parser: argparse.ArgumentParser) -> None:
        """Add examples option to parser."""
        parser.add_argument(
            '--examples',
            action='store_true',
            help='Show usage examples and exit.'
        )
    
    @staticmethod
    def add_indicators_option(parser: argparse.ArgumentParser) -> None:
        """Add indicators search option to parser."""
        parser.add_argument(
            '--indicators',
            nargs='*',
            metavar=('CATEGORY', 'NAME'),
            help='Show available indicators by category and name. Usage: --indicators [category] [name]'
        )
    
    @staticmethod
    def add_metrics_option(parser: argparse.ArgumentParser) -> None:
        """Add metrics encyclopedia option to parser."""
        parser.add_argument(
            '--metric',
            nargs='*',
            metavar=('TYPE', 'FILTER'),
            help='Show trading metrics encyclopedia and strategy tips. Usage: --metric [metrics|tips|notes] [filter_text]'
        )
    
    @staticmethod
    def add_interactive_option(parser: argparse.ArgumentParser) -> None:
        """Add interactive mode option to parser."""
        parser.add_argument(
            '--interactive',
            action='store_true',
            help='Start interactive mode for guided indicator selection and analysis.'
        )
    
    @staticmethod
    def add_required_arguments(parser: argparse.ArgumentParser) -> None:
        """Add required arguments group."""
        required_group = parser.add_argument_group('Required Arguments')
        required_group.add_argument(
            'mode', 
            nargs='?', 
            choices=ArgumentParserConfig.AVAILABLE_MODES,
            help="Operating mode: 'demo', 'yfinance'/'yf', 'csv', 'polygon', 'binance', 'exrate', 'show', 'interactive'. Not required when using --interactive flag."
        )
        
        # Show mode positional arguments
        parser.add_argument(
            'show_args', 
            nargs='*', 
            default=[],
            help=argparse.SUPPRESS  # Hide from help but collect positional args after 'mode'
        )
    
    @staticmethod
    def add_data_source_options(parser: argparse.ArgumentParser) -> None:
        """Add data source specific options group."""
        data_source_group = parser.add_argument_group('Data Source Options')
        
        # CSV options
        data_source_group.add_argument(
            '--csv-file', 
            metavar='PATH',
            help="Path to input CSV file (required for 'csv' mode when processing single file)"
        )
        data_source_group.add_argument(
            '--csv-folder', 
            metavar='PATH',
            help="Path to folder containing CSV files (required for 'csv' mode when processing multiple files)"
        )
        data_source_group.add_argument(
            '--csv-mask', 
            metavar='MASK',
            help="Optional mask to filter CSV files by name (case-insensitive, used with --csv-folder)"
        )
        
        # API options
        data_source_group.add_argument(
            '--ticker', 
            metavar='SYMBOL',
            help="Ticker symbol. Examples: 'EURUSD=X' (yfinance), 'AAPL' (polygon), 'BTCUSDT' (binance)"
        )
        data_source_group.add_argument(
            '--interval', 
            metavar='TIME', 
            default='D1',
            help="Timeframe: 'M1', 'H1', 'D1', 'W1', 'MN1'. Default: D1"
        )
        data_source_group.add_argument(
            '--point', 
            metavar='SIZE', 
            type=float,
            help="Point size. Examples: 0.00001 (EURUSD), 0.01 (stocks/crypto)"
        )
        
        # History selection
        history_group = data_source_group.add_mutually_exclusive_group()
        history_group.add_argument(
            '--period', 
            metavar='TIME',
            help="History period for yfinance. Examples: '1mo', '1y', '5d'"
        )
        history_group.add_argument(
            '--start', 
            metavar='DATE',
            help="Start date for data range (yfinance, polygon, binance)"
        )
        data_source_group.add_argument(
            '--end', 
            metavar='DATE',
            help="End date for data range (required with --start)"
        )
    
    @staticmethod
    def add_indicator_options(parser: argparse.ArgumentParser) -> None:
        """Add indicator options group."""
        indicator_group = parser.add_argument_group('Indicator Options')
        
        all_rule_choices = ArgumentParserConfig.get_all_rule_choices()
        default_rule_name = 'OHLCV'
        
        indicator_group.add_argument(
            '--rule',
            default=default_rule_name,
            help=f"Trading rule to apply. Default: {default_rule_name}. Aliases: PHLD=Predict_High_Low_Direction, PV=Pressure_Vector, SR=Support_Resistants, BB=Bollinger_Bands."
        )
        
        indicator_group.add_argument(
            '--strategy',
            metavar='LOT,RISK_REWARD,FEE',
            help="Strategy parameters: lot_size,risk_reward_ratio,fee_per_trade. Example: --strategy 1,2,0.07 means lot=1.0, risk:reward=2:1, fee=0.07%%. Default: 1.0,2.0,0.07"
        )
        
        indicator_group.add_argument(
            '--price-type', 
            metavar='TYPE',
            choices=ArgumentParserConfig.PRICE_TYPE_CHOICES,
            default='close',
            help="Price type for indicator calculation: 'open' or 'close' (default: close). Supported by all indicators with price_type parameter"
        )
    
    @staticmethod
    def add_show_mode_options(parser: argparse.ArgumentParser) -> None:
        """Add show mode options group."""
        show_group = parser.add_argument_group('Show Mode Options')
        all_rule_choices = ArgumentParserConfig.get_all_rule_choices()
        
        show_group.add_argument(
            '--source', 
            metavar='SRC', 
            default='yfinance',
            choices=ArgumentParserConfig.DATA_SOURCE_CHOICES,
            help="Data source filter: yfinance, csv, polygon, binance, exrate, ind (indicators)"
        )
        show_group.add_argument(
            '--keywords', 
            metavar='WORD', 
            nargs='+', 
            default=[],
            help="Filter keywords (e.g., ticker symbol, date patterns)"
        )
        show_group.add_argument(
            '--show-start', 
            metavar='DATE', 
            type=str, 
            default=None,
            help="Start date/datetime to filter data before calculation"
        )
        show_group.add_argument(
            '--show-end', 
            metavar='DATE', 
            type=str, 
            default=None,
            help="End date/datetime to filter data before calculation"
        )
        show_group.add_argument(
            '--show-rule', 
            metavar='RULE', 
            type=str, 
            choices=all_rule_choices, 
            default=None,
            help="Trading rule for indicator calculation (single file mode)"
        )
    
    @staticmethod
    def add_plotting_options(parser: argparse.ArgumentParser) -> None:
        """Add plotting options group."""
        plotting_group = parser.add_argument_group('Plotting Options')
        plotting_group.add_argument(
            '-d', '--draw',
            dest='draw',
            choices=ArgumentParserConfig.DRAW_CHOICES,
            default='fastest',
            help="Plot method: fastest, fast, plotly, mplfinance, seaborn, term"
        )
    
    @staticmethod
    def add_output_options(parser: argparse.ArgumentParser) -> None:
        """Add output options group."""
        output_group = parser.add_argument_group('Output Options')
        output_group.add_argument(
            '--export-parquet',
            action='store_true',
            help="Export indicators to parquet format (../data/indicators/parquet/)"
        )
        output_group.add_argument(
            '--export-csv',
            action='store_true',
            help="Export indicators to CSV format (../data/indicators/csv/)"
        )
        output_group.add_argument(
            '--export-json',
            action='store_true',
            help="Export indicators to JSON format (../data/indicators/json/)"
        )
        output_group.add_argument(
            '--export-indicators-info',
            action='store_true',
            help="Export indicator metadata to JSON format (../data/indicators/metadata/)"
        )
    
    @staticmethod
    def add_other_options(parser: argparse.ArgumentParser) -> None:
        """Add other options group."""
        other_group = parser.add_argument_group('Other Options')
        other_group.add_argument(
            '-h', 
            action='help', 
            default=argparse.SUPPRESS,
            help='Show this help message and exit'
        )
        other_group.add_argument(
            '--version', 
            action='store_true',
            help="Show program version and exit"
        )


# ============================================================================
# ARGUMENT PARSER CREATION
# ============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """Creates and configures the argument parser."""
    parser = argparse.ArgumentParser(
        description=ArgumentParserConfig.get_main_description(),
        formatter_class=ColoredHelpFormatter,
        epilog=None,
        add_help=False  # Disable default help to add it to a specific group
    )
    
    # Add all argument groups
    ArgumentGroupBuilder.add_examples_option(parser)
    ArgumentGroupBuilder.add_indicators_option(parser)
    ArgumentGroupBuilder.add_metrics_option(parser)
    ArgumentGroupBuilder.add_interactive_option(parser)
    ArgumentGroupBuilder.add_required_arguments(parser)
    ArgumentGroupBuilder.add_data_source_options(parser)
    ArgumentGroupBuilder.add_indicator_options(parser)
    ArgumentGroupBuilder.add_show_mode_options(parser)
    ArgumentGroupBuilder.add_plotting_options(parser)
    ArgumentGroupBuilder.add_output_options(parser)
    ArgumentGroupBuilder.add_other_options(parser)
    
    return parser


# ============================================================================
# INDICATORS SEARCH HANDLER
# ============================================================================

class IndicatorsSearchHandler:
    """Handles indicators search functionality."""
    
    @staticmethod
    def handle_indicators_search(args_list: list) -> None:
        """Handle indicators search with different argument patterns."""
        searcher = IndicatorSearcher()
        
        if not args_list:
            searcher.display_categories()
        elif len(args_list) == 1:
            IndicatorsSearchHandler._handle_single_query(args_list[0], searcher)
        else:
            IndicatorsSearchHandler._handle_category_query(args_list, searcher)
    
    @staticmethod
    def _handle_single_query(query: str, searcher: IndicatorSearcher) -> None:
        """Handle single query search."""
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
    
    @staticmethod
    def _handle_category_query(args_list: list, searcher: IndicatorSearcher) -> None:
        """Handle category-specific query search."""
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


# ============================================================================
# MAIN ARGUMENT PARSING FUNCTION
# ============================================================================

def parse_arguments():
    """Sets up argument parser using ColoredHelpFormatter and returns the parsed arguments."""
    parser = create_argument_parser()
    
    try:
        # Handle --indicators flag first
        if '--indicators' in sys.argv:
            idx = sys.argv.index('--indicators')
            args_list = sys.argv[idx+1:]
            IndicatorsSearchHandler.handle_indicators_search(args_list)
            sys.exit(0)
        
        # Handle no arguments case
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(0)
        
        # Handle help flags
        if '--help' in sys.argv or '-h' in sys.argv:
            parser.print_help()
            sys.exit(0)
        
        # Handle version flag
        if '--version' in sys.argv:
            VersionBannerDisplay.display_banner()
            sys.exit(0)
        
        # Handle special flags
        try:
            from .special_flags_handler import handle_special_flags
            if handle_special_flags():
                return  # Special flag was handled, exit
        except ImportError:
            # Fallback if special flags handler is not available
            pass
        
        # Parse arguments for normal operation
        args = parser.parse_args()
        
    except SystemExit as e:
        if e.code != 0:
            print(f"Argument parsing error (Code: {e.code}). Exiting.", file=sys.stderr)
        sys.exit(e.code)
    
    return args


# ============================================================================
# LEGACY FUNCTION COMPATIBILITY
# ============================================================================

def show_cool_version():
    """Legacy function for backward compatibility."""
    VersionBannerDisplay.display_banner()