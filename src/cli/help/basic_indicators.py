# -*- coding: utf-8 -*-
# src/cli/help/basic_indicators.py

"""
Help information for basic technical indicators.
"""

from colorama import Fore, Style


def get_basic_indicators_help():
    """Get help information for basic technical indicators."""
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
        'stochoscillator': 'stoch'  # Alias to avoid separate help
    }
