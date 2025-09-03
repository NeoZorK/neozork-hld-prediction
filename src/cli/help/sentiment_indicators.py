# -*- coding: utf-8 -*-
# src/cli/help/sentiment_indicators.py

"""
Help information for sentiment indicators.
"""


def get_sentiment_indicators_help():
    """Get help information for sentiment indicators."""
    return {
        'putcallratio': {
            'name': 'Put/Call Ratio',
            'format': 'putcallratio:period,price_type[,bullish_threshold,bearish_threshold]',
            'parameters': [
                'period (int): Put/Call Ratio period (default: 20)',
                'price_type (string): Price type for calculation - open or close (default: close)',
                'bullish_threshold (float): Bullish threshold (default: 60.0)',
                'bearish_threshold (float): Bearish threshold (default: 40.0)'
            ],
            'examples': [
                'putcallratio:20,close,60.0,40.0',
                'putcallratio:14,open,60.0,40.0'
            ]
        },
        'cot': {
            'name': 'COT (Commitment of Traders)',
            'format': 'cot:period,price_type',
            'parameters': [
                'period (int): COT period (default: 20)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'cot:20,close',
                'cot:14,open'
            ]
        },
        'feargreed': {
            'name': 'Fear & Greed Index',
            'format': 'feargreed:period,price_type',
            'parameters': [
                'period (int): Fear & Greed calculation period (default: 14)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'feargreed:14,close',
                'feargreed:21,open',
                'feargreed:10,close'
            ]
        },
        'fg': {
            'name': 'Fear & Greed Index (alias)',
            'format': 'fg:period,price_type',
            'parameters': [
                'period (int): Fear & Greed calculation period (default: 14)',
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'fg:14,close',
                'fg:21,open',
                'fg:10,close'
            ]
        }
    }
