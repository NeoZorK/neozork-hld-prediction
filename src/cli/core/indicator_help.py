# -*- coding: utf-8 -*-
# src/cli/core/indicator_help.py

"""
Help information for technical indicators.
"""

from colorama import Fore, Style


def show_indicator_help(indicator_name: str):
    """
    Show help information for a specific indicator.
    
    Args:
        indicator_name (str): Name of the indicator
    """
    # Use the new enhanced error handling system
    try:
        from .error_handling import show_enhanced_indicator_help
        show_enhanced_indicator_help(f"Help requested for indicator: {indicator_name}", indicator_name, show_error_header=False)
    except Exception:
        pass
    
    # Get help info from modular help files
    help_info = _get_combined_help_info()
    
    if indicator_name.lower() not in help_info:
        print(f"Unknown indicator: {indicator_name}")
        print(f"Available indicators: {', '.join(help_info.keys())}")
        return
    
    info = help_info[indicator_name.lower()]
    
    # Handle aliases
    if isinstance(info, str):
        info = help_info[info]
    
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{info['name']} Help{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Format:{Style.RESET_ALL} {info['format']}")
    print(f"{Fore.CYAN}Parameters:{Style.RESET_ALL}")
    for param in info['parameters']:
        print(f"  • {param}")
    print(f"{Fore.CYAN}Examples:{Style.RESET_ALL}")
    for example in info['examples']:
        print(f"  • {example}")
    print()


def _get_combined_help_info():
    """Combine help information from all modules."""
    try:
        from ..help import (
            get_basic_indicators_help,
            get_moving_averages_help,
            get_volatility_indicators_help,
            get_momentum_indicators_help,
            get_volume_indicators_help,
            get_advanced_indicators_help,
            get_statistical_indicators_help,
            get_sentiment_indicators_help
        )
        
        help_info = {}
        help_info.update(get_basic_indicators_help())
        help_info.update(get_moving_averages_help())
        help_info.update(get_volatility_indicators_help())
        help_info.update(get_momentum_indicators_help())
        help_info.update(get_volume_indicators_help())
        help_info.update(get_advanced_indicators_help())
        help_info.update(get_statistical_indicators_help())
        help_info.update(get_sentiment_indicators_help())
        
        return help_info
    except ImportError:
        # Fallback to basic help if modules are not available
        return _get_fallback_help_info()


def _get_fallback_help_info():
    """Fallback help information if modules are not available."""
    return {
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
                'rsi:21,25,75,close'
            ]
        }
    }
