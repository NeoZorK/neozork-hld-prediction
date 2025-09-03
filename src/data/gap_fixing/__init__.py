# -*- coding: utf-8 -*-
# src/data/gap_fixing/__init__.py

"""
Gap Fixing Module for Time Series Data

This package provides advanced algorithms for fixing time series gaps
using modern interpolation and forecasting techniques.
"""

from .core import GapFixer
from .explanation import (
    explain_why_fix_gaps, 
    get_gap_fixing_benefits, 
    get_gap_fixing_methods, 
    get_gap_detection_metrics
)
from .algorithms import GapFixingStrategy
from .interpolation import apply_interpolation_method
from .utils import GapFixingUtils

__all__ = [
    'GapFixer',
    'explain_why_fix_gaps',
    'get_gap_fixing_benefits', 
    'get_gap_fixing_methods',
    'get_gap_detection_metrics',
    'GapFixingStrategy',
    'apply_interpolation_method',
    'GapFixingUtils'
]
