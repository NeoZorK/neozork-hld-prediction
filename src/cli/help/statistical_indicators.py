# -*- coding: utf-8 -*-
# src/cli/help/statistical_indicators.py

"""
Help information for statistical indicators.
"""


def get_statistical_indicators_help():
    """Get help information for statistical indicators."""
    return {
        'monte': {
            'name': 'Monte Carlo Simulation',
            'format': 'monte:simulations,period',
            'parameters': [
                'simulations (int): Number of simulations (default: 1000)',
                'period (int): Simulation period (default: 252)'
            ],
            'examples': [
                'monte:1000,252',
                'monte:500,126'
            ]
        },
        'kelly': {
            'name': 'Kelly Criterion',
            'format': 'kelly:period',
            'parameters': [
                'period (int): Kelly period (default: 20)'
            ],
            'examples': [
                'kelly:20',
                'kelly:14'
            ]
        }
    }
