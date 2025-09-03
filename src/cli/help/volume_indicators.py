# -*- coding: utf-8 -*-
# src/cli/help/volume_indicators.py

"""
Help information for volume indicators.
"""


def get_volume_indicators_help():
    """Get help information for volume indicators."""
    return {
        'vwap': {
            'name': 'VWAP (Volume Weighted Average Price)',
            'format': 'vwap:price_type',
            'parameters': [
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'vwap:close',
                'vwap:open'
            ]
        },
        'obv': {
            'name': 'OBV (On-Balance Volume)',
            'format': 'obv',
            'parameters': [
                'None required'
            ],
            'examples': [
                'obv'
            ]
        }
    }
