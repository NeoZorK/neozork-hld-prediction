# -*- coding: utf-8 -*-
# src/cli/parsers/indicators/rsi_parsers.py

"""
Parameter parsers for RSI-based indicators.
"""


def parse_rsi_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI parameters: period,oversold,overbought,price_type"""
    params = params_str.split(',')
    if len(params) != 4:
        raise ValueError(f"RSI requires exactly 4 parameters: period,oversold,overbought,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values like 14.0
        oversold = float(params[1].strip())
        overbought = float(params[2].strip())
        price_type = params[3].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid RSI parameters: {params_str}. Error: {e}")
    
    # Validate period
    if period <= 0:
        raise ValueError(f"RSI period must be a positive integer, got: {period}")
    
    # Validate thresholds
    if oversold < 0 or oversold > 100:
        raise ValueError(f"RSI oversold must be between 0 and 100, got: {oversold}")
    
    if overbought < 0 or overbought > 100:
        raise ValueError(f"RSI overbought must be between 0 and 100, got: {overbought}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"RSI price_type must be 'open' or 'close', got: {price_type}")
    
    return 'rsi', {
        'rsi_period': period,
        'oversold': oversold,
        'overbought': overbought,
        'price_type': price_type
    }


def parse_rsi_momentum_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI Momentum parameters: period,oversold,overbought,price_type"""
    # Exactly the same parameters as RSI, but different name
    name, params = parse_rsi_parameters(params_str)
    return 'rsi_mom', params


def parse_rsi_divergence_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI Divergence parameters: period,oversold,overbought,price_type"""
    # Exactly the same parameters as RSI, but different name
    name, params = parse_rsi_parameters(params_str)
    return 'rsi_div', params
