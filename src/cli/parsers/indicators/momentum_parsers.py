# -*- coding: utf-8 -*-
# src/cli/parsers/indicators/momentum_parsers.py

"""
Parameter parsers for momentum indicators.
"""


def parse_macd_parameters(params_str: str) -> tuple[str, dict]:
    """Parse MACD parameters: fast_period,slow_period,signal_period,price_type"""
    params = params_str.split(',')
    if len(params) != 4:
        raise ValueError(f"MACD requires exactly 4 parameters: fast_period,slow_period,signal_period,price_type. Got: {params_str}")
    
    try:
        fast_period = int(float(params[0].strip()))  # Handle float values
        slow_period = int(float(params[1].strip()))
        signal_period = int(float(params[2].strip()))
        price_type = params[3].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid MACD parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"MACD price_type must be 'open' or 'close', got: {price_type}")
    
    return 'macd', {
        'macd_fast': fast_period,
        'macd_slow': slow_period,
        'macd_signal': signal_period,
        'price_type': price_type
    }


def parse_stoch_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Stochastic parameters: k_period,d_period,price_type"""
    params = params_str.split(',')
    if len(params) != 3:
        raise ValueError(f"Stochastic requires exactly 3 parameters: k_period,d_period,price_type. Got: {params_str}")
    
    try:
        k_period = int(float(params[0].strip()))  # Handle float values
        d_period = int(float(params[1].strip()))
        price_type = params[2].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Stochastic parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Stochastic price_type must be 'open' or 'close', got: {price_type}")
    
    return 'stoch', {
        'stoch_k': k_period,
        'stoch_d': d_period,
        'price_type': price_type
    }


def parse_cci_parameters(params_str: str) -> tuple[str, dict]:
    """Parse CCI parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"CCI requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid CCI parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"CCI period must be a positive integer, got: {period}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"CCI price_type must be 'open' or 'close', got: {price_type}")
    
    return 'cci', {
        'cci_period': period,
        'price_type': price_type
    }


def parse_adx_parameters(params_str: str) -> tuple[str, dict]:
    """Parse ADX parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"ADX requires exactly 1 parameter: period. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid ADX parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"ADX period must be a positive integer, got: {period}")
    
    return 'adx', {
        'adx_period': period
    }
