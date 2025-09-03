# -*- coding: utf-8 -*-
# src/cli/parsers/indicators/volatility_parsers.py

"""
Parameter parsers for volatility indicators.
"""


def parse_bb_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Bollinger Bands parameters: period,std_dev,price_type"""
    params = params_str.split(',')
    if len(params) != 3:
        raise ValueError(f"Bollinger Bands requires exactly 3 parameters: period,std_dev,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        std_dev = float(params[1].strip())
        price_type = params[2].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Bollinger Bands parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"Bollinger Bands period must be a positive integer, got: {period}")
    
    if std_dev <= 0:
        raise ValueError(f"Bollinger Bands std_dev must be positive, got: {std_dev}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Bollinger Bands price_type must be 'open' or 'close', got: {price_type}")
    
    return 'bb', {
        'bb_period': period,
        'bb_std': std_dev,
        'price_type': price_type
    }


def parse_atr_parameters(params_str: str) -> tuple[str, dict]:
    """Parse ATR parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"ATR requires exactly 1 parameter: period. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid ATR parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"ATR period must be a positive integer, got: {period}")
    
    return 'atr', {
        'atr_period': period
    }


def parse_stdev_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Standard Deviation parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"Standard Deviation requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Standard Deviation parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"Standard Deviation period must be a positive integer, got: {period}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Standard Deviation price_type must be 'open' or 'close', got: {price_type}")
    
    return 'stdev', {
        'stdev_period': period,
        'price_type': price_type
    }


def parse_donchain_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Donchian Channels parameters: period"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"Donchian Channels requires exactly 1 parameter: period. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Donchian Channels parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"Donchian Channels period must be a positive integer, got: {period}")
    
    return 'donchain', {
        'donchain_period': period
    }
