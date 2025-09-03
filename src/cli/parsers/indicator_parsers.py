# -*- coding: utf-8 -*-
# src/cli/parsers/indicator_parsers.py

"""
Parameter parsers for different technical indicators.
"""

from .indicators import (
    # RSI parsers
    parse_rsi_parameters,
    parse_rsi_momentum_parameters,
    parse_rsi_divergence_parameters,
    
    # Moving average parsers
    parse_ema_parameters,
    parse_sma_parameters,
    parse_hma_parameters,
    parse_tsf_parameters,
    
    # Momentum parsers
    parse_macd_parameters,
    parse_stoch_parameters,
    parse_cci_parameters,
    parse_adx_parameters,
    
    # Volatility parsers
    parse_bb_parameters,
    parse_atr_parameters,
    parse_stdev_parameters,
    parse_donchain_parameters,
    
    # Advanced parsers
    parse_sar_parameters,
    parse_supertrend_parameters,
    parse_wave_parameters,
    parse_fibo_parameters,
    
    # Volume and sentiment parsers
    parse_vwap_parameters,
    parse_obv_parameters,
    parse_pivot_parameters,
    parse_putcallratio_parameters,
    parse_cot_parameters,
    parse_feargreed_parameters,
    
    # Statistical parsers
    parse_monte_parameters,
    parse_kelly_parameters
)


def parse_indicator_parameters(rule_str: str) -> tuple[str, dict]:
    """
    Parse indicator rule string in format 'indicator:param1,param2,param3,param4'.
    
    Args:
        rule_str (str): Indicator rule string
        
    Returns:
        tuple[str, dict]: Tuple of (indicator_name, parameters_dict)
        
    Raises:
        ValueError: If rule format is invalid or parameters are invalid
    """
    if ':' not in rule_str:
        raise ValueError(f"Invalid rule format. Expected 'indicator:params', got: {rule_str}")
    
    indicator_name, params_str = rule_str.split(':', 1)
    indicator_name = indicator_name.strip().lower()
    
    # Map indicator names to their parser functions
    parser_map = {
        'rsi': parse_rsi_parameters,
        'rsi_mom': parse_rsi_momentum_parameters,
        'rsi_div': parse_rsi_divergence_parameters,
        'macd': parse_macd_parameters,
        'stoch': parse_stoch_parameters,
        'stochoscillator': parse_stoch_parameters,  # Alias
        'ema': parse_ema_parameters,
        'sma': parse_sma_parameters,
        'bb': parse_bb_parameters,
        'atr': parse_atr_parameters,
        'cci': parse_cci_parameters,
        'vwap': parse_vwap_parameters,
        'pivot': parse_pivot_parameters,
        'hma': parse_hma_parameters,
        'tsf': parse_tsf_parameters,
        'monte': parse_monte_parameters,
        'kelly': parse_kelly_parameters,
        'donchain': parse_donchain_parameters,
        'fibo': parse_fibo_parameters,
        'obv': parse_obv_parameters,
        'stdev': parse_stdev_parameters,
        'adx': parse_adx_parameters,
        'sar': parse_sar_parameters,
        'supertrend': parse_supertrend_parameters,
        'wave': parse_wave_parameters,
        'putcallratio': parse_putcallratio_parameters,
        'cot': parse_cot_parameters,
        'feargreed': parse_feargreed_parameters,
        'fg': parse_feargreed_parameters  # Alias
    }
    
    if indicator_name not in parser_map:
        raise ValueError(f"Unknown indicator: {indicator_name}")
    
    # Call the appropriate parser
    return parser_map[indicator_name](params_str)


# Re-export all parser functions for backward compatibility
__all__ = [
    'parse_indicator_parameters',
    'parse_rsi_parameters',
    'parse_rsi_momentum_parameters',
    'parse_rsi_divergence_parameters',
    'parse_macd_parameters',
    'parse_stoch_parameters',
    'parse_ema_parameters',
    'parse_sma_parameters',
    'parse_bb_parameters',
    'parse_atr_parameters',
    'parse_cci_parameters',
    'parse_vwap_parameters',
    'parse_pivot_parameters',
    'parse_hma_parameters',
    'parse_tsf_parameters',
    'parse_monte_parameters',
    'parse_kelly_parameters',
    'parse_donchain_parameters',
    'parse_fibo_parameters',
    'parse_obv_parameters',
    'parse_stdev_parameters',
    'parse_adx_parameters',
    'parse_sar_parameters',
    'parse_supertrend_parameters',
    'parse_wave_parameters',
    'parse_putcallratio_parameters',
    'parse_cot_parameters',
    'parse_feargreed_parameters'
]
