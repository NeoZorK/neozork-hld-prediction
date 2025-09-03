# -*- coding: utf-8 -*-
"""
Calculation Module for NeoZorK HLD Prediction

This module provides calculation capabilities including:
- Indicator calculations
- Trading metrics
- Error handling and validation
"""

from .indicator_calculation import calculate_indicator
from .trading_metrics import TradingMetricsCalculator
from .universal_trading_metrics import UniversalTradingMetrics
from .rules import apply_trading_rule
from .core_calculations import calculate_hl, calculate_pressure, calculate_pv
from .indicator import calculate_pressure_vector

# Error handling imports
from .error_handling import (
    OscillatorErrorHandler,
    TrendErrorHandler,
    MomentumErrorHandler,
    VolumeErrorHandler,
    VolatilityErrorHandler,
    SupportResistanceErrorHandler,
    PredictiveErrorHandler,
    ProbabilityErrorHandler,
    SentimentErrorHandler
)

__all__ = [
    'calculate_indicator',
    'TradingMetricsCalculator',
    'UniversalTradingMetrics',
    'apply_trading_rule',
    'calculate_hl',
    'calculate_pressure', 
    'calculate_pv',
    'calculate_pressure_vector',
    # Error handlers
    'OscillatorErrorHandler',
    'TrendErrorHandler',
    'MomentumErrorHandler',
    'VolumeErrorHandler',
    'VolatilityErrorHandler',
    'SupportResistanceErrorHandler',
    'PredictiveErrorHandler',
    'ProbabilityErrorHandler',
    'SentimentErrorHandler'
]
