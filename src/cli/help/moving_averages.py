# -*- coding: utf-8 -*-
# src/cli/help/moving_averages.py

"""
Help information for moving average indicators.
"""


def get_moving_averages_help():
    """Get help information for moving average indicators."""
    return {
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
        'sma': {
            'name': 'SMA (Simple Moving Average)',
            'format': 'sma:period,price_type',
            'parameters': [
                'period (int): SMA period (default: 20)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'sma:20,close',
                'sma:50,open'
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
        }
    }
