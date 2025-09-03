# -*- coding: utf-8 -*-
# src/cli/parsers/indicators/volume_sentiment_parsers.py

"""
Parameter parsers for volume and sentiment indicators.
"""


def parse_vwap_parameters(params_str: str) -> tuple[str, dict]:
    """Parse VWAP parameters: price_type"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"VWAP requires exactly 1 parameter: price_type. Got: {params_str}")
    
    try:
        price_type = params[0].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid VWAP parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"VWAP price_type must be 'open' or 'close', got: {price_type}")
    
    return 'vwap', {
        'price_type': price_type
    }


def parse_obv_parameters(params_str: str) -> tuple[str, dict]:
    """Parse OBV parameters: none required"""
    if params_str.strip():
        raise ValueError(f"OBV requires no parameters. Got: {params_str}")
    
    return 'obv', {}


def parse_pivot_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Pivot Points parameters: price_type"""
    params = params_str.split(',')
    if len(params) != 1:
        raise ValueError(f"Pivot Points requires exactly 1 parameter: price_type. Got: {params_str}")
    
    try:
        price_type = params[0].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Pivot Points parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Pivot Points price_type must be 'open' or 'close', got: {price_type}")
    
    return 'pivot', {
        'price_type': price_type
    }


def parse_putcallratio_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Put/Call Ratio parameters: period,price_type[,bullish_threshold,bearish_threshold]"""
    params = params_str.split(',')
    if len(params) < 2 or len(params) > 4:
        raise ValueError(f"Put/Call Ratio requires 2-4 parameters: period,price_type[,bullish_threshold,bearish_threshold]. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))
        price_type = params[1].strip().lower()
        bullish_threshold = float(params[2].strip()) if len(params) > 2 else 60.0
        bearish_threshold = float(params[3].strip()) if len(params) > 3 else 40.0
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Put/Call Ratio parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"Put/Call Ratio period must be a positive integer, got: {period}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Put/Call Ratio price_type must be 'open' or 'close', got: {price_type}")
    
    return 'putcallratio', {
        'putcallratio_period': period,
        'price_type': price_type,
        'putcallratio_bullish': bullish_threshold,
        'putcallratio_bearish': bearish_threshold
    }


def parse_cot_parameters(params_str: str) -> tuple[str, dict]:
    """Parse COT parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"COT requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid COT parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"COT period must be a positive integer, got: {period}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"COT price_type must be 'open' or 'close', got: {price_type}")
    
    return 'cot', {
        'cot_period': period,
        'price_type': price_type
    }


def parse_feargreed_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Fear & Greed parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"Fear & Greed requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Fear & Greed parameters: {params_str}. Error: {e}")
    
    if period <= 0:
        raise ValueError(f"Fear & Greed period must be a positive integer, got: {period}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"Fear & Greed price_type must be 'open' or 'close', got: {price_type}")
    
    return 'feargreed', {
        'feargreed_period': period,
        'price_type': price_type
    }
