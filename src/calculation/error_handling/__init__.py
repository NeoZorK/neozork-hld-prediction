# -*- coding: utf-8 -*-
# src/calculation/error_handling/__init__.py
"""
Error Handling Module for Indicator Calculations

This module provides error handling and validation for different indicator groups.
"""

from .oscillators import OscillatorErrorHandler
from .trend import TrendErrorHandler
from .momentum import MomentumErrorHandler
from .volume import VolumeErrorHandler
from .volatility import VolatilityErrorHandler
from .support_resistance import SupportResistanceErrorHandler
from .predictive import PredictiveErrorHandler
from .probability import ProbabilityErrorHandler
from .sentiment import SentimentErrorHandler

__all__ = [
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
