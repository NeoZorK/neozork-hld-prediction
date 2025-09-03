# -*- coding: utf-8 -*-
# src/cli/help/momentum_indicators.py

"""
Help information for momentum indicators.
"""


def get_momentum_indicators_help():
    """Get help information for momentum indicators."""
    return {
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
        }
    }
