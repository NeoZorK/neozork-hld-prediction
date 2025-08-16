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
        'rsi_mom': {
            'name': 'RSI Momentum',
            'description': 'Advanced RSI variant that calculates the momentum (rate of change) of RSI values to identify trend strength and potential reversal points.',
            'format': 'rsi_mom:period,oversold,overbought,price_type',
            'parameters': [
                ('period', 'int', 'RSI calculation period', '14'),
                ('oversold', 'float', 'Oversold threshold (0-100)', '30'),
                ('overbought', 'float', 'Overbought threshold (0-100)', '70'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('rsi_mom:14,30,70,open', 'Standard RSI Momentum with open prices'),
                ('rsi_mom:21,25,75,close', 'Custom RSI Momentum with close prices'),
                ('rsi_mom:14,10,90,open', 'Wide range RSI Momentum with open prices')
            ],
            'tips': [
                'RSI Momentum measures the rate of change of RSI values',
                'Positive momentum indicates strengthening trend',
                'Negative momentum indicates weakening trend',
                'Use with standard RSI for confirmation signals',
                'Momentum signals can precede price reversals'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid period: Must be a positive integer',
                'Invalid thresholds: Must be between 0 and 100'
            ]
        },
        'rsi_div': {
            'name': 'RSI Divergence',
            'description': 'Advanced RSI variant that detects divergence between price movement and RSI movement to identify potential trend reversals.',
            'format': 'rsi_div:period,oversold,overbought,price_type',
            'parameters': [
                ('period', 'int', 'RSI calculation period', '14'),
                ('oversold', 'float', 'Oversold threshold (0-100)', '30'),
                ('overbought', 'float', 'Overbought threshold (0-100)', '70'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('rsi_div:14,30,70,open', 'Standard RSI Divergence with open prices'),
                ('rsi_div:21,25,75,close', 'Custom RSI Divergence with close prices'),
                ('rsi_div:14,10,90,open', 'Wide range RSI Divergence with open prices')
            ],
            'tips': [
                'RSI Divergence compares price movement with RSI movement',
                'Bullish divergence: Price makes lower lows, RSI makes higher lows',
                'Bearish divergence: Price makes higher highs, RSI makes lower highs',
                'Divergence signals can be powerful reversal indicators',
                'Use with other indicators for confirmation'
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
            'description': 'Momentum oscillator that compares a closing price to its price range over a specific period to identify overbought/oversold conditions.',
            'format': 'stoch:k_period,d_period,price_type',
            'parameters': [
                ('k_period', 'int', '%K period for stochastic calculation', '14'),
                ('d_period', 'int', '%D period for smoothing', '3'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('stoch:14,3,close', 'Standard stochastic with close prices'),
                ('stoch:21,5,open', 'Custom stochastic with open prices'),
                ('stoch:10,2,close', 'Fast stochastic with close prices')
            ],
            'tips': [
                'Standard settings: 14,3 for balanced analysis',
                'Lower k_period = more responsive, more signals',
                'Higher d_period = smoother %D line',
                'Values above 80 indicate overbought conditions',
                'Values below 20 indicate oversold conditions'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid periods: Must be positive integers',
                'k_period too large for dataset size'
            ]
        },
        'stochoscillator': 'stoch',  # Alias to avoid separate help
        'stochastic': 'stoch',      # Alias to avoid separate help
        'monte': {
            'name': 'Monte Carlo Simulation',
            'description': 'Uses statistical simulation to forecast potential price movements and identify trading opportunities.',
            'format': 'monte:simulations,period',
            'parameters': [
                ('simulations', 'int', 'Number of Monte Carlo simulations to run', '1000'),
                ('period', 'int', 'Forecast period (number of days to predict)', '252')
            ],
            'examples': [
                ('monte:1000,252', 'Standard Monte Carlo with 1000 simulations for 1 year'),
                ('monte:500,126', 'Monte Carlo with 500 simulations for 6 months'),
                ('monte:2000,30', 'High-precision Monte Carlo for 1 month')
            ],
            'tips': [
                'More simulations = more accurate results but slower calculation',
                'Longer period = more uncertainty in predictions',
                'Use 252 for annual forecasts, 126 for semi-annual'
            ],
            'common_errors': [
                'Invalid simulations: Must be a positive integer',
                'Invalid period: Must be a positive integer',
                'Too many simulations may cause memory issues'
            ]
        },
        'montecarlo': 'monte',      # Alias for Monte Carlo
        'mc': 'monte',              # Alias for Monte Carlo
        'fg': 'feargreed',          # Alias for Fear & Greed
        'tsforecast': 'tsf',        # Alias for Time Series Forecast
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
        },
        'hma': {
            'name': 'HMA (Hull Moving Average)',
            'description': 'Smooths price data to reduce lag and improve trend detection compared to classic moving averages.',
            'format': 'hma:period,price_type',
            'parameters': [
                ('period', 'int', 'HMA period (window size)', '20'),
                ('price_type', 'string', 'Price type for calculation ("open" or "close")', 'close')
            ],
            'examples': [
                ('hma:20,close', 'Standard HMA with close prices'),
                ('hma:14,open', 'HMA with period 14 and open prices'),
                ('hma:50,close', 'Long-term HMA')
            ],
            'tips': [
                'Lower period = more sensitive, more signals',
                'Higher period = smoother, fewer signals',
                'Use with price_type=open for aggressive entries'
            ],
            'common_errors': [
                'Invalid price_type: Use only "open" or "close"',
                'Invalid period: Must be a positive integer'
            ]
        },
        'tsf': {
            'name': 'TSF (Time Series Forecast)',
            'description': 'Linear regression-based indicator that projects future price levels based on historical data.',
            'format': 'tsf:period,price_type',
            'parameters': [
                ('period', 'int', 'TSF calculation period (window size)', '14'),
                ('price_type', 'string', 'Price type for calculation ("open" or "close")', 'close')
            ],
            'examples': [
                ('tsf:14,close', 'Standard TSF with close prices'),
                ('tsf:20,open', 'TSF with period 20 and open prices'),
                ('tsf:10,close', 'Short-term TSF')
            ],
            'tips': [
                'Shorter period = more responsive to recent trends',
                'Longer period = more stable but less responsive',
                'Use with price_type=open for early trend detection'
            ],
            'common_errors': [
                'Invalid price_type: Use only "open" or "close"',
                'Invalid period: Must be a positive integer'
            ]
        },
        'kelly': {
            'name': 'Kelly Criterion',
            'description': 'Mathematical formula to determine optimal position size based on win probability and risk/reward ratio.',
            'format': 'kelly:period',
            'parameters': [
                ('period', 'int', 'Calculation period for win/loss analysis', '20')
            ],
            'examples': [
                ('kelly:20', 'Standard Kelly Criterion with 20-period analysis'),
                ('kelly:50', 'Long-term Kelly Criterion with 50-period analysis'),
                ('kelly:10', 'Short-term Kelly Criterion with 10-period analysis')
            ],
            'tips': [
                'Longer period = more stable but less responsive to recent changes',
                'Shorter period = more responsive but potentially more volatile',
                'Use as a guide for position sizing, not absolute rule'
            ],
            'common_errors': [
                'Invalid period: Must be a positive integer',
                'Period too short may give unreliable results'
            ]
        },
        'putcallratio': {
            'name': 'Put/Call Ratio',
            'description': 'Measures the ratio of put option volume to call option volume to gauge market sentiment (fear/greed). High values may indicate fear, low values may indicate greed.',
            'format': 'putcallratio:period,price_type[,bullish_threshold,bearish_threshold]',
            'parameters': [
                ('period', 'int', 'Put/Call Ratio period', '20'),
                ('price_type', 'string', 'Price type for calculation - open or close', 'close'),
                ('bullish_threshold', 'float', 'Bullish threshold', '60.0'),
                ('bearish_threshold', 'float', 'Bearish threshold', '40.0')
            ],
            'examples': [
                ('putcallratio:20,close,60.0,40.0', 'Standard Put/Call Ratio with close prices'),
                ('putcallratio:14,open,65.0,35.0', 'Custom thresholds with open prices')
            ],
            'tips': [
                'Use higher bullish_threshold for more conservative buy signals.',
                'Put/Call Ratio above bullish_threshold may indicate excessive fear (potential buy).',
                'Put/Call Ratio below bearish_threshold may indicate excessive greed (potential sell).',
                'Typical values: bullish_threshold=60.0, bearish_threshold=40.0.'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only.',
                'Invalid period: Must be a positive integer.',
                'Thresholds must be floats.'
            ]
        },
        'fibo': {
            'name': 'Fibonacci Retracements',
            'description': 'Plots Fibonacci retracement levels for trend analysis and support/resistance identification.',
            'format': 'fibo:level1,level2,... OR fibo:all',
            'parameters': [
                ('levels', 'float list', 'Comma-separated list of retracement levels (e.g., 0.236,0.382,0.5,0.618,0.786) or "all" for standard levels', 'all'),
            ],
            'examples': [
                ('fibo:all', 'Standard Fibonacci levels: 0.236, 0.382, 0.5, 0.618, 0.786'),
                ('fibo:0.236,0.382,0.5,0.618,0.786', 'Custom Fibonacci levels'),
                ('fibo:0.382,0.618', 'Minimal set of levels'),
            ],
            'tips': [
                'Use "fibo:all" for standard analysis.',
                'You can specify any subset of levels, e.g., "fibo:0.382,0.618".',
                'Fibonacci retracements are best used in trending markets.',
                'Combine with other indicators for confirmation.'
            ],
            'common_errors': [
                'Invalid level: Levels must be floats between 0 and 1.',
                'At least one level must be specified if not using "all".'
            ]
        },
        'donchain': {
            'name': 'Donchian Channel',
            'description': 'Volatility indicator that shows the highest high and lowest low over a specified period, with a middle line representing the average.',
            'format': 'donchain:period',
            'parameters': [
                ('period', 'int', 'Donchian Channel period (window size)', '20')
            ],
            'examples': [
                ('donchain:20', 'Standard Donchian Channel with 20-period window'),
                ('donchain:14', 'Short-term Donchian Channel with 14-period window'),
                ('donchain:50', 'Long-term Donchian Channel with 50-period window')
            ],
            'tips': [
                'Standard period: 20 for balanced analysis',
                'Shorter period = more responsive, more signals',
                'Longer period = smoother, fewer signals',
                'Upper channel = resistance, lower channel = support',
                'Middle line can act as dynamic support/resistance'
            ],
            'common_errors': [
                'Invalid period: Must be a positive integer',
                'Period too short may give unreliable results'
            ]
        },
        'sar': {
            'name': 'SAR (Parabolic Stop and Reverse)',
            'description': 'Trend-following indicator that highlights potential reversal points by placing dots above or below price. Useful for trailing stops and trend detection.',
            'format': 'sar:acceleration,maximum',
            'parameters': [
                ('acceleration', 'float', 'Acceleration factor (step), controls sensitivity. Typical: 0.02', '0.02'),
                ('maximum', 'float', 'Maximum acceleration factor. Typical: 0.2', '0.2')
            ],
            'examples': [
                ('sar:0.02,0.2', 'Standard Parabolic SAR (default settings)'),
                ('sar:0.01,0.1', 'Less sensitive SAR (fewer signals)'),
                ('sar:0.03,0.25', 'More sensitive SAR (more signals)')
            ],
            'tips': [
                'Lower acceleration = fewer signals, smoother trend',
                'Higher acceleration = more signals, more whipsaws',
                'Use for trailing stop-loss or trend confirmation',
                'Combine with other indicators for better entries/exits'
            ],
            'common_errors': [
                'Invalid acceleration/maximum: Must be positive floats',
                'Acceleration should be less than or equal to maximum',
                'Omitting parameters: Use format sar:0.02,0.2'
            ]
        },
        'atr': {
            'name': 'ATR (Average True Range)',
            'description': 'Volatility indicator that measures market volatility by calculating the average of true ranges over a specified period. Higher values indicate higher volatility.',
            'format': 'atr:period',
            'parameters': [
                ('period', 'int', 'ATR calculation period (window size)', '14')
            ],
            'examples': [
                ('atr:14', 'Standard ATR with 14-period window'),
                ('atr:21', 'ATR with 21-period window'),
                ('atr:10', 'Short-term ATR with 10-period window')
            ],
            'tips': [
                'Standard period: 14 for balanced analysis',
                'Shorter period = more responsive to recent volatility',
                'Longer period = smoother, less sensitive to short-term spikes',
                'Use ATR for position sizing and stop-loss placement',
                'Higher ATR values suggest avoiding tight stops'
            ],
            'common_errors': [
                'Invalid period: Must be a positive integer',
                'Period too short may give unreliable results',
                'ATR requires only one parameter: period'
            ]
        },
        'stdev': {
            'name': 'Standard Deviation',
            'description': 'Volatility indicator that measures the degree of variation or dispersion of price data from its average. Higher values indicate higher price volatility.',
            'format': 'stdev:period,price_type',
            'parameters': [
                ('period', 'int', 'Standard deviation calculation period (window size)', '20'),
                ('price_type', 'string', 'Price type for calculation - open or close', 'close')
            ],
            'examples': [
                ('stdev:20,close', 'Standard deviation with 20-period window using close prices'),
                ('stdev:14,close', 'Standard deviation with 14-period window using close prices'),
                ('stdev:10,open', 'Short-term standard deviation with 10-period window using open prices')
            ],
            'tips': [
                'Standard period: 20 for balanced analysis',
                'Shorter period = more responsive to recent volatility',
                'Longer period = smoother, less sensitive to short-term spikes',
                'Use for volatility analysis and risk assessment',
                'Higher values suggest increased market uncertainty'
            ],
            'common_errors': [
                'Invalid period: Must be a positive integer',
                'Invalid price_type: Use only "open" or "close"',
                'Missing parameters: Use format stdev:period,price_type',
                'Period too short may give unreliable results'
            ]
        },
        'obv': {
            'name': 'OBV (On-Balance Volume)',
            'description': 'Volume-based momentum indicator that uses volume flow to predict changes in stock price. Rising OBV suggests accumulation, falling OBV suggests distribution.',
            'format': 'obv',
            'parameters': [
                ('None', 'N/A', 'OBV does not require any parameters', 'N/A')
            ],
            'examples': [
                ('obv', 'Standard OBV calculation using volume and price data'),
                ('obv:', 'Alternative format with colon (same as obv)')
            ],
            'tips': [
                'OBV is a cumulative indicator that adds/subtracts volume based on price direction',
                'Rising OBV with rising prices confirms uptrend strength',
                'Falling OBV with falling prices confirms downtrend strength',
                'Divergence between OBV and price can signal potential reversals',
                'Use OBV to confirm price movements and identify accumulation/distribution'
            ],
            'common_errors': [
                'Adding parameters: OBV does not accept any parameters',
                'Use simple format: obv or obv:',
                'OBV requires volume data in the dataset'
            ]
        },
        'supertrend': {
            'name': 'SuperTrend',
            'description': 'Trend-following indicator that uses ATR to determine trend direction and generate buy/sell signals. Highlights trend reversals and dynamic support/resistance.',
            'format': 'supertrend:period,multiplier[,price_type]',
            'parameters': [
                ('period', 'int', 'ATR period for SuperTrend calculation (required)', '10'),
                ('multiplier', 'float', 'ATR multiplier (required)', '3.0'),
                ('price_type', 'string', 'Price type for calculation - open or close (default: close)', 'close')
            ],
            'examples': [
                ('supertrend:10,3.0', 'Standard SuperTrend with period 10 and multiplier 3.0'),
                ('supertrend:14,2.5,close', 'SuperTrend with period 14, multiplier 2.5, close prices'),
                ('supertrend:10,3.0,open', 'SuperTrend with open prices'),
                ('supertrend:50,2.5,close', 'Long-term SuperTrend with period 50, multiplier 2.5, close prices')
            ],
            'tips': [
                'Lower period = more sensitive, more signals',
                'Higher multiplier = fewer signals, smoother trend',
                'Use price_type=open for more aggressive entries',
                'Combine with other indicators for confirmation',
                'SuperTrend is best used in trending markets'
            ],
            'common_errors': [
                'Invalid period: Must be a positive integer',
                'Invalid multiplier: Must be a positive float',
                'Invalid price_type: Use only "open" or "close"',
                'Omitting parameters: Use format supertrend:10,3.0[,price_type]'
            ]
        },
        'feargreed': {
            'name': 'Fear & Greed Index',
            'description': 'Sentiment indicator that measures market fear and greed levels based on price volatility and momentum. Values below 25 indicate extreme fear (potential buy), values above 75 indicate extreme greed (potential sell).',
            'format': 'feargreed:period,price_type',
            'parameters': [
                ('period', 'int', 'Fear & Greed calculation period', '14'),
                ('price_type', 'string', 'Price type for calculation', 'close')
            ],
            'examples': [
                ('feargreed:14,close', 'Standard Fear & Greed with close prices'),
                ('feargreed:21,open', 'Long-term Fear & Greed with open prices'),
                ('feargreed:10,close', 'Short-term Fear & Greed with close prices')
            ],
            'tips': [
                'Values 0-25: Extreme Fear (potential buy signal)',
                'Values 25-45: Fear (cautious buying)',
                'Values 45-55: Neutral (no clear signal)',
                'Values 55-75: Greed (cautious selling)',
                'Values 75-100: Extreme Greed (potential sell signal)',
                'Use with other indicators for confirmation',
                'Longer periods provide more stable signals'
            ],
            'common_errors': [
                'Invalid price_type: Use "open" or "close" only',
                'Invalid period: Must be a positive integer',
                'Period too short may give unreliable results'
            ]
        },
        'adx': {
            'name': 'ADX (Average Directional Index)',
            'description': 'Trend strength indicator that measures the strength of a trend regardless of its direction. Values above 25 indicate a strong trend, values below 20 indicate a weak trend.',
            'format': 'adx:period',
            'parameters': [
                ('period', 'int', 'ADX calculation period', '14')
            ],
            'examples': [
                ('adx:14', 'Standard ADX with 14-period window'),
                ('adx:21', 'Long-term ADX with 21-period window'),
                ('adx:10', 'Short-term ADX with 10-period window')
            ],
            'tips': [
                'Values 0-20: Weak trend (sideways market)',
                'Values 20-25: Developing trend',
                'Values 25-50: Strong trend',
                'Values 50+: Very strong trend',
                'Use with +DI and -DI for trend direction',
                'ADX alone does not indicate trend direction',
                'Higher ADX values suggest trend-following strategies'
            ],
            'common_errors': [
                'Invalid period: Must be a positive integer',
                'Period too short may give unreliable results',
                'ADX requires only one parameter: period'
            ]
        },
        'schr_dir': {
            'name': 'SCHR Direction (Shcherbyna Direction)',
            'description': 'Premium directional indicator that uses Volume Price Ratio (VPR) to calculate direction lines and generate trading signals. Shows two separate lines (High and Low) for dual chart analysis.',
            'format': 'schr_dir:grow_percent',
            'parameters': [
                ('grow_percent', 'float', 'Growth percentage for line calculation (1-95)', '1.0')
            ],
            'examples': [
                ('schr_dir', 'SCHR Direction with default 1% growth'),
                ('schr_dir:50', 'SCHR Direction with 50% growth (moderate)'),
                ('schr_dir:95', 'SCHR Direction with 95% growth (conservative)'),
            ],
            'tips': [
                'Lower grow_percent (1-25) = more aggressive signals, tighter line separation',
                'Higher grow_percent (50-95) = more conservative signals, wider line separation',
                'Default 1% provides optimal balance for most markets',
                'Use with volume analysis for best results',
                'Dual chart display shows High (blue) and Low (gold) lines',
                'BUY signal: when open price > both lines',
                'SELL signal: when open price < both lines',
                'Premium indicator based on MQL5 SCHR_DIR.mq5'
            ],
            'common_errors': [
                'Invalid grow_percent: Must be between 1.0 and 95.0',
                'Missing parameter: Use schr_dir:value (e.g., schr_dir:50)',
                'Invalid format: Expected number between 1 and 95'
            ]
        },
        'schr_rost': {
            'name': 'SCHR Rost (Shcherbyna Rost) 🚀',
            'description': '🔥 PREMIUM ADX-based trend prediction indicator with 12 speed modes! Advanced directional movement analysis with customizable speed settings and fast reverse signals. Perfect for trend detection and momentum analysis.',
            'format': 'schr_rost:speed_period,faster_reverse',
            'parameters': [
                ('speed_period', 'string', 'Speed mode: Snail,Turtle,Frog,Mouse,Cat,Rabbit,Gepard,Slowest,Slow,Normal,Fast,Future', 'Future'),
                ('faster_reverse', 'boolean', 'Enable faster signal reversal (true/false)', 'false')
            ],
            'examples': [
                ('schr_rost', 'SCHR Rost with default Future speed and no fast reverse'),
                ('schr_rost:Future,true', 'SCHR Rost with Future speed and fast reverse enabled'),
                ('schr_rost:Normal,false', 'SCHR Rost with Normal speed and standard signals'),
                ('schr_rost:Snail,true', 'SCHR Rost with Snail speed (slowest) and fast reverse'),
                ('schr_rost:Fast,false', 'SCHR Rost with Fast speed and standard signals'),
                ('schr_rost:Gepard,true', 'SCHR Rost with Gepard speed (fastest) and fast reverse'),
            ],
            'tips': [
                '🚀 SPEED MODES: Snail(1000) → Turtle(500) → Frog(200) → Mouse(100) → Cat(50) → Rabbit(30) → Gepard(10) → Slowest(5) → Slow(2) → Normal(1.01) → Fast(0.683) → Future(0.501)',
                '⚡ Future speed (0.501) = fastest signals, most responsive to market changes',
                '🐌 Snail speed (1000) = slowest signals, most stable but less responsive',
                '🔄 faster_reverse=true: Enables quick signal reversal for volatile markets',
                '🎯 Best for: Trend detection, momentum analysis, and directional trading',
                '📊 Dual chart display shows main indicator line with signal line and histogram',
                '💎 Premium indicator based on MQL5 SCHR_ROST.mq5 by Shcherbyna Rostyslav',
                '🔥 Use with volume analysis and other indicators for best results',
                '⚡ Fast speeds (Future, Fast) = more signals, higher noise',
                '🐌 Slow speeds (Snail, Turtle) = fewer signals, more stable',
                '🎯 Normal speed (1.01) = balanced approach for most markets'
            ],
            'common_errors': [
                'Invalid speed_period: Use one of: Snail,Turtle,Frog,Mouse,Cat,Rabbit,Gepard,Slowest,Slow,Normal,Fast,Future',
                'Invalid faster_reverse: Use "true" or "false" only',
                'Missing parameters: Use schr_rost:speed,faster_reverse (e.g., schr_rost:Future,true)',
                'Invalid format: Expected schr_rost:speed,boolean'
            ]
        },
        'schr_trend': {
            'name': 'SCHR Trend Helper (Shcherbyna Trend) 📈',
            'description': '🔥 PREMIUM RSI-based trend prediction indicator with 10 trading rule modes! Advanced trend detection with multiple analysis methods including Purchase Power analysis using 10 RSI periods. Perfect for trend identification and signal generation.',
            'format': 'schr_trend:period,tr_mode,extreme_up,extreme_down',
            'parameters': [
                ('period', 'int', 'RSI calculation period', '2'),
                ('tr_mode', 'string', 'Trading rule mode: firstclassic,firsttrend,trend,zone,firstzone,firststrongzone,purchasepower,purchasepower_bycount,purchasepower_extreme,purchasepower_weak', 'zone'),
                ('extreme_up', 'int', 'Extreme up point (0-100)', '95'),
                ('extreme_down', 'int', 'Extreme down point (0-100)', '5')
            ],
            'examples': [
                ('schr_trend', 'SCHR Trend with default settings (period=2, zone mode, extreme_up=95, extreme_down=5)'),
                ('schr_trend:5,zone,90,10', 'SCHR Trend with period 5, zone mode, extreme_up=90, extreme_down=10'),
                ('schr_trend:3,firstclassic,95,5', 'SCHR Trend with period 3, first classic mode, extreme_up=95, extreme_down=5'),
                ('schr_trend:2,purchasepower,95,5', 'SCHR Trend with period 2, purchase power mode, extreme_up=95, extreme_down=5'),
                ('schr_trend:4,trend,85,15', 'SCHR Trend with period 4, trend mode, extreme_up=85, extreme_down=15'),
                ('schr_trend:1,firstzone,98,2', 'SCHR Trend with period 1, first zone mode, extreme_up=98, extreme_down=2'),
            ],
            'tips': [
                '📊 TRADING RULE MODES: 10 different analysis methods for various trading strategies',
                '🎯 Zone mode (default): >50 Buy, <50 Sell with extreme detection',
                '⚡ First Classic: >95 Sell, <5 Buy (classic extreme reversal)',
                '🔄 First Trend: >95 Buy, <5 Sell (trend following with extremes)',
                '📈 Trend mode: Best Up 70| Down 30 with trend continuation',
                '🔥 Purchase Power modes: Analyze 10 RSI periods for consensus signals',
                '💎 Premium indicator based on MQL5 SCHR_Trend.mq5 by Shcherbyna Rostyslav',
                '🎯 Best for: Trend detection, signal generation, and multi-timeframe analysis',
                '📊 Dual chart display shows signal markers and trend direction',
                '⚡ Short periods = more signals, long periods = more stable',
                '🎯 Extreme points: Adjust based on market volatility and trading style'
            ],
            'common_errors': [
                'Invalid tr_mode: Use one of: firstclassic,firsttrend,trend,zone,firstzone,firststrongzone,purchasepower,purchasepower_bycount,purchasepower_extreme,purchasepower_weak',
                'Invalid period: Must be a positive integer',
                'Invalid extreme points: Must be between 0 and 100',
                'Missing parameters: Use schr_trend:period,tr_mode,extreme_up,extreme_down (e.g., schr_trend:2,zone,95,5)',
                'Invalid format: Expected schr_trend:int,string,int,int'
            ]
        }
    }
    
    # Get help data
    data = help_data.get(indicator_name.lower(), None)
    
    # Handle aliases: if data is a string, it's an alias to another indicator
    if isinstance(data, str):
        data = help_data.get(data, None)
    
    return data


def show_enhanced_indicator_help(error_message: str, indicator_name: str = None, show_error_header: bool = True):
    """Show enhanced help for an indicator with colorful formatting and icons."""
    
    # Extract indicator name from error if not provided
    if not indicator_name:
        indicator_name = extract_indicator_name_from_error(error_message)
    
    if not indicator_name:
        # Fallback to basic error display
        if show_error_header:
            CLIErrorHandler.print_error_header(error_message)
        CLIErrorHandler.print_help_section("General Help", "Use --indicators to see all available indicators", 'help')
        CLIErrorHandler.print_footer()
        return
    
    # Get help data for the indicator
    help_data = get_indicator_help_data(indicator_name)
    
    if not help_data:
        # Unknown indicator
        if show_error_header:
            CLIErrorHandler.print_error_header(error_message)
        CLIErrorHandler.print_help_section("Unknown Indicator", f"'{indicator_name}' is not a recognized indicator", 'warning')
        CLIErrorHandler.print_help_section("Available Indicators", "Use --indicators to see all available indicators", 'help')
        CLIErrorHandler.print_footer()
        return
    
    # Print enhanced help
    if show_error_header:
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