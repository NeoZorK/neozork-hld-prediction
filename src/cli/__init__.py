# -*- coding: utf-8 -*-
# src/cli/__init__.py

"""
Command Line Interface Module

This package provides CLI functionality for the application.
"""

from .core.cli import *
from .core.cli_show_mode import *
from .core.interactive_mode import *
from .indicators.indicators_search import *
from .examples import *
from .encyclopedia import *
from .core.error_handling import *

__all__ = [
    # Core CLI functionality
    'CLI',
    'CLIShowMode',
    'InteractiveMode',
    'CLIErrorHandler',
    
    # Examples
    'OscillatorExamples',
    'TrendExamples',
    'MomentumExamples',
    'show_all_cli_examples',
    'show_indicator_group_examples',
    
    # Encyclopedia
    'OscillatorMetrics',
    'OscillatorTips',
    'TrendMetrics',
    'TrendTips',
    'MomentumMetrics',
    'MomentumTips',
    'VolumeMetrics',
    'VolumeTips',
    'VolatilityMetrics',
    'VolatilityTips',
    'SupportResistanceMetrics',
    'SupportResistanceTips',
    'PredictiveMetrics',
    'PredictiveTips',
    'ProbabilityMetrics',
    'ProbabilityTips',
    'SentimentMetrics',
    'SentimentTips'
]