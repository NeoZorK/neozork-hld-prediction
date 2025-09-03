# -*- coding: utf-8 -*-
# src/cli/help/volatility_indicators.py

"""
Help information for volatility indicators.
"""


def get_volatility_indicators_help():
    """Get help information for volatility indicators."""
    return {
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
        }
    }
