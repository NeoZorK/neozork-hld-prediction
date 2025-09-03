# -*- coding: utf-8 -*-
# src/cli/parsers/indicators/__init__.py

"""
Indicator parameter parsers module.
"""

from .rsi_parsers import (
    parse_rsi_parameters,
    parse_rsi_momentum_parameters,
    parse_rsi_divergence_parameters
)

from .moving_average_parsers import (
    parse_ema_parameters,
    parse_sma_parameters,
    parse_hma_parameters,
    parse_tsf_parameters
)

from .momentum_parsers import (
    parse_macd_parameters,
    parse_stoch_parameters,
    parse_cci_parameters,
    parse_adx_parameters
)

from .volatility_parsers import (
    parse_bb_parameters,
    parse_atr_parameters,
    parse_stdev_parameters,
    parse_donchain_parameters
)

from .advanced_parsers import (
    parse_sar_parameters,
    parse_supertrend_parameters,
    parse_wave_parameters,
    parse_fibo_parameters
)

from .volume_sentiment_parsers import (
    parse_vwap_parameters,
    parse_obv_parameters,
    parse_pivot_parameters,
    parse_putcallratio_parameters,
    parse_cot_parameters,
    parse_feargreed_parameters
)

from .statistical_parsers import (
    parse_monte_parameters,
    parse_kelly_parameters
)

__all__ = [
    # RSI parsers
    'parse_rsi_parameters',
    'parse_rsi_momentum_parameters',
    'parse_rsi_divergence_parameters',
    
    # Moving average parsers
    'parse_ema_parameters',
    'parse_sma_parameters',
    'parse_hma_parameters',
    'parse_tsf_parameters',
    
    # Momentum parsers
    'parse_macd_parameters',
    'parse_stoch_parameters',
    'parse_cci_parameters',
    'parse_adx_parameters',
    
    # Volatility parsers
    'parse_bb_parameters',
    'parse_atr_parameters',
    'parse_stdev_parameters',
    'parse_donchain_parameters',
    
    # Advanced parsers
    'parse_sar_parameters',
    'parse_supertrend_parameters',
    'parse_wave_parameters',
    'parse_fibo_parameters',
    
    # Volume and sentiment parsers
    'parse_vwap_parameters',
    'parse_obv_parameters',
    'parse_pivot_parameters',
    'parse_putcallratio_parameters',
    'parse_cot_parameters',
    'parse_feargreed_parameters',
    
    # Statistical parsers
    'parse_monte_parameters',
    'parse_kelly_parameters'
]
