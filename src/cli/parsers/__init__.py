# -*- coding: utf-8 -*-
# src/cli/parsers/__init__.py

"""
Parameter parsers for CLI indicators.
"""

from .indicator_parsers import (
    parse_indicator_parameters,
    parse_rsi_parameters,
    parse_macd_parameters,
    parse_stoch_parameters,
    parse_ema_parameters,
    parse_sma_parameters,
    parse_wave_parameters,
    parse_bb_parameters,
    parse_atr_parameters,
    parse_cci_parameters,
    parse_vwap_parameters,
    parse_pivot_parameters,
    parse_hma_parameters,
    parse_tsf_parameters,
    parse_monte_parameters,
    parse_kelly_parameters,
    parse_donchain_parameters,
    parse_fibo_parameters,
    parse_obv_parameters,
    parse_stdev_parameters,
    parse_adx_parameters,
    parse_sar_parameters,
    parse_supertrend_parameters,
    parse_putcallratio_parameters,
    parse_cot_parameters,
    parse_feargreed_parameters
)

__all__ = [
    'parse_indicator_parameters',
    'parse_rsi_parameters',
    'parse_macd_parameters',
    'parse_stoch_parameters',
    'parse_ema_parameters',
    'parse_sma_parameters',
    'parse_wave_parameters',
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
    'parse_putcallratio_parameters',
    'parse_cot_parameters',
    'parse_feargreed_parameters'
]
