# -*- coding: utf-8 -*-
# src/cli/parsers/indicators/statistical_parsers.py

"""
Parameter parsers for statistical indicators.
"""


def parse_monte_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Monte Carlo parameters: simulations,period"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"Monte Carlo requires exactly 2 parameters: simulations,period. Got: {params_str}")
    
    try:
        simulations = int(float(params[0].strip()))
        period = int(float(params[1].strip()))
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Monte Carlo parameters: {params_str}. Error: {e}")
    
    if simulations <= 0:
        raise ValueError(f"Monte Carlo simulations must be a positive integer, got: {simulations}")
    
    if period <= 0:
        raise ValueError(f"Monte Carlo period must be a positive integer, got: {period}")
    
    return 'monte', {
        'monte_simulations': simulations,
        'monte_period': period
    }


def parse_kelly_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Kelly Criterion parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"Kelly Criterion requires exactly 1 parameter: period. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Kelly Criterion parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"Kelly Criterion period must be a positive integer, got: {period}")
    
    return 'kelly', {
        'kelly_period': period
    }
