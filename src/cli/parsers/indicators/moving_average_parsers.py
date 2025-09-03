# -*- coding: utf-8 -*-
# src/cli/parsers/indicators/moving_average_parsers.py

"""
Parameter parsers for moving average indicators.
"""


def parse_ema_parameters(params_str: str) -> tuple[str, dict]:
    """Parse EMA parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"EMA requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid EMA parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"EMA period must be a positive integer, got: {period}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"EMA price_type must be 'open' or 'close', got: {price_type}")
    
    return 'ema', {
        'ema_period': period,
        'price_type': price_type
    }


def parse_sma_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SMA parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"SMA requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid SMA parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"SMA period must be a positive integer, got: {period}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"SMA price_type must be 'open' or 'close', got: {price_type}")
    
    return 'sma', {
        'sma_period': period,
        'price_type': price_type
    }


def parse_hma_parameters(params_str: str) -> tuple[str, dict]:
    """Parse HMA parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"HMA requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid HMA parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"HMA period must be a positive integer, got: {period}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"HMA price_type must be 'open' or 'close', got: {price_type}")
    
    return 'hma', {
        'hma_period': period,
        'price_type': price_type
    }


def parse_tsf_parameters(params_str: str) -> tuple[str, dict]:
    """Parse TSF parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"TSF requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid TSF parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"TSF period must be a positive integer, got: {period}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"TSF price_type must be 'open' or 'close', got: {price_type}")
    
    return 'tsf', {
        'tsf_period': period,
        'price_type': price_type
    }
