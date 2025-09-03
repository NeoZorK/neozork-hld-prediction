# -*- coding: utf-8 -*-
"""
Quantitative Trading Encyclopedia Module

This module provides comprehensive explanations of trading metrics and valuable tips
organized by indicator groups.
"""

from .oscillators import OscillatorMetrics, OscillatorTips
from .trend import TrendMetrics, TrendTips
from .momentum import MomentumMetrics, MomentumTips
from .volume import VolumeMetrics, VolumeTips
from .volatility import VolatilityMetrics, VolatilityTips
from .support_resistance import SupportResistanceMetrics, SupportResistanceTips
from .predictive import PredictiveMetrics, PredictiveTips
from .probability import ProbabilityMetrics, ProbabilityTips
from .sentiment import SentimentMetrics, SentimentTips

__all__ = [
    # Oscillators
    'OscillatorMetrics',
    'OscillatorTips',
    # Trend
    'TrendMetrics',
    'TrendTips',
    # Momentum
    'MomentumMetrics',
    'MomentumTips',
    # Volume
    'VolumeMetrics',
    'VolumeTips',
    # Volatility
    'VolatilityMetrics',
    'VolatilityTips',
    # Support/Resistance
    'SupportResistanceMetrics',
    'SupportResistanceTips',
    # Predictive
    'PredictiveMetrics',
    'PredictiveTips',
    # Probability
    'ProbabilityMetrics',
    'ProbabilityTips',
    # Sentiment
    'SentimentMetrics',
    'SentimentTips'
]
