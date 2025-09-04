# -*- coding: utf-8 -*-
# src/cli/core/argument_groups/config.py

"""
Configuration for argument parser setup.
"""

import textwrap
from colorama import Fore, Style

from src.common.constants import TradingRule


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
    AVAILABLE_MODES = ['demo', 'yfinance', 'yf', 'csv', 'polygon', 'binance', 'show']
    
    # Data source choices
    DATA_SOURCE_CHOICES = ['yfinance', 'yf', 'csv', 'polygon', 'binance', 'ind']
    
    # Drawing method choices
    DRAW_CHOICES = ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term']
    
    # Price type choices
    PRICE_TYPE_CHOICES = ['open', 'close']
    
    @classmethod
    def get_main_description(cls) -> str:
        """Get the main description for the argument parser."""
        return textwrap.dedent(f"""
           {Fore.CYAN}{Style.BRIGHT}Shcherbyna Pressure Vector Indicator Analysis Tool{Style.RESET_ALL}
           
           Calculate and plot pressure vector indicators from multiple data sources: demo data, Yahoo Finance, CSV files, Polygon.io, and Binance. Export calculated indicators in parquet, CSV, or JSON formats.
           
           {Fore.YELLOW}Quick Start:{Style.RESET_ALL}
             python run_analysis.py --indicators                    # List all available indicators
             python run_analysis.py --metric                        # Show trading metrics encyclopedia
             python run_analysis.py demo --rule RSI                 # Run with demo data and RSI indicator
           """).strip()
    
    @classmethod
    def get_all_rule_choices(cls) -> list:
        """Get all available rule choices including aliases."""
        rule_names = list(TradingRule.__members__.keys())
        return rule_names + list(cls.RULE_ALIASES_MAP.keys()) + ['OHLCV', 'AUTO']
