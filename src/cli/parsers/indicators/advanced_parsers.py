# -*- coding: utf-8 -*-
# src/cli/parsers/indicators/advanced_parsers.py

"""
Parameter parsers for advanced indicators.
"""

from src.calculation.indicators.trend.wave_ind import ENUM_MOM_TR, ENUM_GLOBAL_TR


def parse_sar_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SAR parameters: acceleration,maximum"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"SAR requires exactly 2 parameters: acceleration,maximum. Got: {params_str}")
    
    try:
        acceleration = float(params[0].strip())
        maximum = float(params[1].strip())
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid SAR parameters: {params_str}. Error: {e}")
    
    if acceleration <= 0:
        raise ValueError(f"SAR acceleration must be positive, got: {acceleration}")
    
    if maximum <= 0:
        raise ValueError(f"SAR maximum must be positive, got: {maximum}")
    
    return 'sar', {
        'sar_acceleration': acceleration,
        'sar_maximum': maximum
    }


def parse_supertrend_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SuperTrend parameters: period,multiplier[,price_type]"""
    params = params_str.split(',')
    if len(params) < 2 or len(params) > 3:
        raise ValueError(f"SuperTrend requires 2-3 parameters: period,multiplier[,price_type]. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))
        multiplier = float(params[1].strip())
        price_type = params[2].strip().lower() if len(params) == 3 else 'close'
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid SuperTrend parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"SuperTrend period must be a positive integer, got: {period}")
    
    if multiplier <= 0:
        raise ValueError(f"SuperTrend multiplier must be positive, got: {multiplier}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"SuperTrend price_type must be 'open' or 'close', got: {price_type}")
    
    return 'supertrend', {
        'supertrend_period': period,
        'supertrend_multiplier': multiplier,
        'price_type': price_type
    }


def parse_wave_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Wave parameters: long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type"""
    params = params_str.split(',')
    if len(params) != 11:
        raise ValueError(f"Wave requires exactly 11 parameters. Got: {params_str}")
    
    try:
        long1 = int(float(params[0].strip()))
        fast1 = int(float(params[1].strip()))
        trend1 = int(float(params[2].strip()))
        tr1 = params[3].strip().lower()
        long2 = int(float(params[4].strip()))
        fast2 = int(float(params[5].strip()))
        trend2 = int(float(params[6].strip()))
        tr2 = params[7].strip().lower()
        global_tr = params[8].strip().lower()
        sma_period = int(float(params[9].strip()))
        price_type = params[10].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Wave parameters: {params_str}. Error: {e}")
    
    # Validate trading rules
    valid_tr = ['fast', 'slow', 'trend']
    if tr1 not in valid_tr:
        raise ValueError(f"Wave tr1 must be one of {valid_tr}, got: {tr1}")
    
    if tr2 not in valid_tr:
        raise ValueError(f"Wave tr2 must be one of {valid_tr}, got: {tr2}")
    
    # Validate global trading rules
    valid_global_tr = ['prime', 'reverse']
    if global_tr not in valid_global_tr:
        raise ValueError(f"Wave global_tr must be one of {valid_global_tr}, got: {global_tr}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Wave price_type must be 'open' or 'close', got: {price_type}")
    
    return 'wave', {
        'wave_long1': long1,
        'wave_fast1': fast1,
        'wave_trend1': trend1,
        'wave_tr1': tr1,
        'wave_long2': long2,
        'wave_fast2': fast2,
        'wave_trend2': trend2,
        'wave_tr2': tr2,
        'wave_global_tr': global_tr,
        'wave_sma_period': sma_period,
        'price_type': price_type
    }


def parse_fibo_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Fibonacci parameters: level1,level2,level3,..."""
    params = params_str.split(',')
    if len(params) < 1:
        raise ValueError(f"Fibonacci requires at least 1 parameter: level1,level2,level3,.... Got: {params_str}")
    
    try:
        levels = [float(param.strip()) for param in params]
    except ValueError as e:
        raise ValueError(f"Invalid Fibonacci parameters: {params_str}. Error: {e}")
    
    # Validate levels are between 0 and 1
    for level in levels:
        if level < 0 or level > 1:
            raise ValueError(f"Fibonacci levels must be between 0 and 1, got: {level}")
    
    return 'fibo', {
        'fibo_levels': levels
    }
