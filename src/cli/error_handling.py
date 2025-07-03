# -*- coding: utf-8 -*-
# src/cli/error_handling.py

"""
Enhanced error handling for CLI with colorful help and icons.
All comments and text are in English.
"""

from colorama import Fore, Style
import re


class CLIErrorHandler:
    """Enhanced error handler for CLI with colorful help and icons."""
    
    # Icons for different types of help
    ICONS = {
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'success': '✅',
        'help': '💡',
        'indicator': '📊',
        'parameter': '⚙️',
        'example': '💻',
        'tip': '💡',
        'fix': '🔧'
    }
    
    # Color schemes for different message types
    COLORS = {
        'error': Fore.RED,
        'warning': Fore.YELLOW,
        'info': Fore.CYAN,
        'success': Fore.GREEN,
        'help': Fore.MAGENTA,
        'indicator': Fore.BLUE,
        'parameter': Fore.WHITE,
        'example': Fore.GREEN,
        'tip': Fore.YELLOW,
        'fix': Fore.CYAN
    }
    
    @classmethod
    def print_error_header(cls, error_message: str):
        """Print a colorful error header with icon."""
        print(f"\n{cls.ICONS['error']} {cls.COLORS['error']}{Style.BRIGHT}ERROR:{Style.RESET_ALL} {error_message}")
        print(f"{cls.COLORS['error']}{'=' * 60}{Style.RESET_ALL}")
    
    @classmethod
    def print_help_section(cls, title: str, content: str, icon_type: str = 'help'):
        """Print a help section with icon and color."""
        print(f"\n{cls.ICONS[icon_type]} {cls.COLORS[icon_type]}{Style.BRIGHT}{title}:{Style.RESET_ALL}")
        print(f"{content}")
    
    @classmethod
    def print_parameter_info(cls, param_name: str, param_desc: str, param_type: str = "string", default_value: str = None):
        """Print parameter information with formatting."""
        param_line = f"  {cls.ICONS['parameter']} {cls.COLORS['parameter']}{Style.BRIGHT}{param_name}{Style.RESET_ALL} ({param_type})"
        if default_value:
            param_line += f" {cls.COLORS['info']}[default: {default_value}]{Style.RESET_ALL}"
        print(param_line)
        print(f"     {param_desc}")
    
    @classmethod
    def print_example(cls, example: str, description: str = None):
        """Print an example with formatting."""
        example_line = f"  {cls.ICONS['example']} {cls.COLORS['example']}{example}{Style.RESET_ALL}"
        if description:
            example_line += f" {cls.COLORS['info']}# {description}{Style.RESET_ALL}"
        print(example_line)
    
    @classmethod
    def print_tip(cls, tip: str):
        """Print a tip with formatting."""
        print(f"  {cls.ICONS['tip']} {cls.COLORS['tip']}{tip}{Style.RESET_ALL}")
    
    @classmethod
    def print_fix(cls, fix: str):
        """Print a fix suggestion with formatting."""
        print(f"  {cls.ICONS['fix']} {cls.COLORS['fix']}{fix}{Style.RESET_ALL}")
    
    @classmethod
    def print_command_usage(cls, command: str, description: str = None):
        """Print command usage with formatting."""
        usage_line = f"  {cls.ICONS['example']} {cls.COLORS['example']}{command}{Style.RESET_ALL}"
        if description:
            usage_line += f" {cls.COLORS['info']}# {description}{Style.RESET_ALL}"
        print(usage_line)
    
    @classmethod
    def print_separator(cls):
        """Print a separator line."""
        print(f"{cls.COLORS['info']}{'─' * 60}{Style.RESET_ALL}")
    
    @classmethod
    def print_footer(cls):
        """Print a footer with additional help information."""
        print(f"\n{cls.ICONS['help']} {cls.COLORS['help']}{Style.BRIGHT}Need more help?{Style.RESET_ALL}")
        print(f"  {cls.ICONS['example']} {cls.COLORS['example']}python run_analysis.py --indicators{Style.RESET_ALL} {cls.COLORS['info']}# List all indicators{Style.RESET_ALL}")
        print(f"  {cls.ICONS['example']} {cls.COLORS['example']}python run_analysis.py --examples{Style.RESET_ALL} {cls.COLORS['info']}# Show usage examples{Style.RESET_ALL}")
        print(f"  {cls.ICONS['example']} {cls.COLORS['example']}python run_analysis.py --help{Style.RESET_ALL} {cls.COLORS['info']}# Show general help{Style.RESET_ALL}")


def extract_indicator_name_from_error(error_message: str) -> str:
    """Extract indicator name from error message."""
    # Common patterns in error messages
    patterns = [
        r"(\w+) price_type must be 'open' or 'close'",
        r"(\w+) requires exactly \d+ parameters",
        r"Invalid (\w+) parameters",
        r"Unknown indicator: (\w+)",
        r"(\w+) period must be",
        r"(\w+) oversold must be",
        r"(\w+) overbought must be"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, error_message, re.IGNORECASE)
        if match:
            return match.group(1).lower()
    
    return None


def get_indicator_help_data(indicator_name: str) -> dict:
    """Get comprehensive help data for an indicator."""
    help_data = {
        'rsi': {
            'name': 'RSI (Relative Strength Index)',
            'description': 'Measures the speed and magnitude of price changes to identify overbought/oversold conditions.',
            'format': 'rsi:period,oversold,overbought,price_type',
            'parameters': [
                ('period', 'int', 'RSI calculation period', '14'),
                ('oversold', 'float', 'Oversold threshold (0-100)', '30'),
                ('overbought', 'float', 'Overbought threshold (0-100)', '70'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('rsi:14,30,70,open', 'Standard RSI with open prices'),
                ('rsi:21,25,75,close', 'Custom RSI with close prices'),
                ('rsi:14,10,90,open', 'Wide range RSI with open prices')
            ],
            'tips': [
                'Use period 14 for standard analysis',
                'Oversold/overbought levels can be adjusted based on market conditions',
                'Open prices are more volatile, close prices are more stable'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid period: Must be a positive integer',
                'Invalid thresholds: Must be between 0 and 100'
            ]
        },
        'macd': {
            'name': 'MACD (Moving Average Convergence Divergence)',
            'description': 'Shows the relationship between two moving averages to identify momentum changes.',
            'format': 'macd:fast_period,slow_period,signal_period,price_type',
            'parameters': [
                ('fast_period', 'int', 'Fast EMA period', '12'),
                ('slow_period', 'int', 'Slow EMA period', '26'),
                ('signal_period', 'int', 'Signal line period', '9'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('macd:12,26,9,close', 'Standard MACD with close prices'),
                ('macd:8,21,5,open', 'Fast MACD with open prices'),
                ('macd:21,55,13,close', 'Slow MACD with close prices')
            ],
            'tips': [
                'Standard settings: 12, 26, 9',
                'Fast MACD: 8, 21, 5 for more signals',
                'Slow MACD: 21, 55, 13 for fewer signals'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid periods: Must be positive integers',
                'Fast period must be less than slow period'
            ]
        },
        'stoch': {
            'name': 'Stochastic Oscillator',
            'description': 'Measures momentum by comparing closing price to price range over time.',
            'format': 'stoch:k_period,d_period,price_type',
            'parameters': [
                ('k_period', 'int', '%K period', '14'),
                ('d_period', 'int', '%D period', '3'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('stoch:14,3,close', 'Standard Stochastic with close prices'),
                ('stoch:21,5,open', 'Slow Stochastic with open prices'),
                ('stoch:9,3,close', 'Fast Stochastic with close prices')
            ],
            'tips': [
                'Standard settings: 14, 3',
                'Fast Stochastic: 9, 3 for more signals',
                'Slow Stochastic: 21, 5 for fewer signals'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid periods: Must be positive integers',
                'D period should be less than K period'
            ]
        },
        'ema': {
            'name': 'EMA (Exponential Moving Average)',
            'description': 'Weighted moving average that gives more importance to recent prices.',
            'format': 'ema:period,price_type',
            'parameters': [
                ('period', 'int', 'EMA period', '20'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('ema:20,close', 'Standard EMA with close prices'),
                ('ema:50,open', 'Long-term EMA with open prices'),
                ('ema:10,close', 'Short-term EMA with close prices')
            ],
            'tips': [
                'Short-term: 10-20 periods for quick signals',
                'Medium-term: 20-50 periods for trend analysis',
                'Long-term: 50+ periods for major trends'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid period: Must be a positive integer'
            ]
        },
        'bb': {
            'name': 'Bollinger Bands',
            'description': 'Volatility indicator with upper and lower bands around a moving average.',
            'format': 'bb:period,std_dev,price_type',
            'parameters': [
                ('period', 'int', 'Moving average period', '20'),
                ('std_dev', 'float', 'Standard deviation multiplier', '2.0'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('bb:20,2.0,close', 'Standard Bollinger Bands with close prices'),
                ('bb:20,2.5,open', 'Wide bands with open prices'),
                ('bb:10,1.5,close', 'Tight bands with close prices')
            ],
            'tips': [
                'Standard settings: 20, 2.0',
                'Tight bands: 1.5-2.0 for volatile markets',
                'Wide bands: 2.5-3.0 for stable markets'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid period: Must be a positive integer',
                'Invalid std_dev: Must be a positive number'
            ]
        },
        'cot': {
            'name': 'COT (Commitment of Traders)',
            'description': 'Analyzes futures market positioning to gauge institutional sentiment.',
            'format': 'cot:period,price_type',
            'parameters': [
                ('period', 'int', 'COT calculation period', '20'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('cot:20,close', 'Standard COT with close prices'),
                ('cot:14,open', 'Short-term COT with open prices'),
                ('cot:30,close', 'Long-term COT with close prices')
            ],
            'tips': [
                'Standard period: 20 for balanced analysis',
                'Short-term: 14 for quick sentiment changes',
                'Long-term: 30 for major sentiment trends'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid period: Must be a positive integer'
            ]
        },
        'cci': {
            'name': 'CCI (Commodity Channel Index)',
            'description': 'Measures price deviations from average price to identify cyclical trends.',
            'format': 'cci:period,price_type',
            'parameters': [
                ('period', 'int', 'CCI calculation period', '20'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('cci:20,close', 'Standard CCI with close prices'),
                ('cci:14,open', 'Short-term CCI with open prices'),
                ('cci:30,close', 'Long-term CCI with close prices')
            ],
            'tips': [
                'Standard period: 20 for balanced analysis',
                'Short-term: 14 for quick signals',
                'Long-term: 30 for major trends'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid period: Must be a positive integer'
            ]
        },
        'vwap': {
            'name': 'VWAP (Volume Weighted Average Price)',
            'description': 'Average price weighted by volume, useful for intraday analysis.',
            'format': 'vwap:price_type',
            'parameters': [
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('vwap:close', 'VWAP with close prices'),
                ('vwap:open', 'VWAP with open prices')
            ],
            'tips': [
                'Most commonly used with close prices',
                'Open prices can be used for specific analysis',
                'VWAP is recalculated daily'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only'
            ]
        },
        'pivot': {
            'name': 'Pivot Points',
            'description': 'Support and resistance levels based on previous day\'s high, low, and close.',
            'format': 'pivot:price_type',
            'parameters': [
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('pivot:close', 'Pivot points with close prices'),
                ('pivot:open', 'Pivot points with open prices')
            ],
            'tips': [
                'Most commonly used with close prices',
                'Open prices can be used for specific analysis',
                'Pivot points are recalculated daily'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only'
            ]
        }
    }
    
    return help_data.get(indicator_name.lower(), None)


def show_enhanced_indicator_help(error_message: str, indicator_name: str = None):
    """Show enhanced help for an indicator with colorful formatting and icons."""
    
    # Extract indicator name from error if not provided
    if not indicator_name:
        indicator_name = extract_indicator_name_from_error(error_message)
    
    if not indicator_name:
        # Fallback to basic error display
        CLIErrorHandler.print_error_header(error_message)
        CLIErrorHandler.print_help_section("General Help", "Use --indicators to see all available indicators", 'help')
        CLIErrorHandler.print_footer()
        return
    
    # Get help data for the indicator
    help_data = get_indicator_help_data(indicator_name)
    
    if not help_data:
        # Unknown indicator
        CLIErrorHandler.print_error_header(error_message)
        CLIErrorHandler.print_help_section("Unknown Indicator", f"'{indicator_name}' is not a recognized indicator", 'warning')
        CLIErrorHandler.print_help_section("Available Indicators", "Use --indicators to see all available indicators", 'help')
        CLIErrorHandler.print_footer()
        return
    
    # Print enhanced help
    CLIErrorHandler.print_error_header(error_message)
    
    # Indicator information
    CLIErrorHandler.print_help_section(
        f"{help_data['name']} Help", 
        help_data['description'], 
        'indicator'
    )
    
    # Format
    CLIErrorHandler.print_help_section("Format", f"{CLIErrorHandler.ICONS['parameter']} {help_data['format']}", 'parameter')
    
    # Parameters
    CLIErrorHandler.print_help_section("Parameters", "", 'parameter')
    for param_name, param_type, param_desc, default_value in help_data['parameters']:
        CLIErrorHandler.print_parameter_info(param_name, param_desc, param_type, default_value)
    
    # Examples
    CLIErrorHandler.print_help_section("Examples", "", 'example')
    for example, description in help_data['examples']:
        CLIErrorHandler.print_example(example, description)
    
    # Tips
    if help_data.get('tips'):
        CLIErrorHandler.print_help_section("Tips", "", 'tip')
        for tip in help_data['tips']:
            CLIErrorHandler.print_tip(tip)
    
    # Common errors
    if help_data.get('common_errors'):
        CLIErrorHandler.print_help_section("Common Errors", "", 'warning')
        for error in help_data['common_errors']:
            CLIErrorHandler.print_fix(error)
    
    # Command usage examples
    CLIErrorHandler.print_help_section("Command Usage", "", 'example')
    CLIErrorHandler.print_command_usage(
        f"python run_analysis.py show csv mn1 -d fastest --rule {help_data['examples'][0][0]}",
        "Basic usage with first example"
    )
    CLIErrorHandler.print_command_usage(
        f"python run_analysis.py show csv mn1 -d fastest --rule {help_data['examples'][1][0]}",
        "Alternative usage with second example"
    )
    
    CLIErrorHandler.print_separator()
    CLIErrorHandler.print_footer()


def handle_indicator_error(error_message: str, show_help: bool = True):
    """Handle indicator calculation errors with enhanced help."""
    if show_help:
        show_enhanced_indicator_help(error_message)
    else:
        CLIErrorHandler.print_error_header(error_message) 