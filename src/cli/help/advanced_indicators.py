# -*- coding: utf-8 -*-
# src/cli/help/advanced_indicators.py

"""
Help information for advanced indicators.
"""


def get_advanced_indicators_help():
    """Get help information for advanced indicators."""
    return {
        'pivot': {
            'name': 'Pivot Points',
            'format': 'pivot:price_type',
            'parameters': [
                'price_type (string): Price type for calculation - open or close (default: close)'
            ],
            'examples': [
                'pivot:close',
                'pivot:open'
            ]
        },
        'fibo': {
            'name': 'Fibonacci Retracements',
            'format': 'fibo:level1,level2,level3,...',
            'parameters': [
                'level1,level2,level3,... (float): Fibonacci retracement levels (default: 0.236,0.382,0.5,0.618,0.786)'
            ],
            'examples': [
                'fibo:0.236,0.382,0.5,0.618,0.786',
                'fibo:0.236,0.5,0.786'
            ]
        },
        'wave': {
            'name': 'Wave',
            'format': 'wave:long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type',
            'parameters': [
                'long1 (int): First long period (default: 339)',
                'fast1 (int): First fast period (default: 10)',
                'trend1 (int): First trend period (default: 2)',
                'tr1 (ENUM_MOM_TR): First trading rule (default: TR_Fast)',
                'long2 (int): Second long period (default: 22)',
                'fast2 (int): Second fast period (default: 11)',
                'trend2 (int): Second trend period (default: 4)',
                'tr2 (ENUM_MOM_TR): Second trading rule (default: TR_Fast)',
                'global_tr (ENUM_GLOBAL_TR): Global trading rule (default: G_TR_PRIME)',
                'sma_period (int): SMA calculation period (default: 22)'
            ],
            'examples': [
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'wave:33,10,2,fast,22,11,4,fast,reverse,22,open'
            ]
        }
    }
