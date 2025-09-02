#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gap Fixer Module for Time Series Data

This module provides advanced algorithms for fixing time series gaps
using modern interpolation and forecasting techniques.

This module has been refactored into smaller components for better maintainability.
"""

# Import the main class and functions from the refactored modules
from .gap_fixer_core import GapFixer
from .gap_fixer_explanation import explain_why_fix_gaps, get_gap_fixing_benefits, get_gap_fixing_methods, get_gap_detection_metrics

# Re-export for backward compatibility
__all__ = [
    'GapFixer',
    'explain_why_fix_gaps',
    'get_gap_fixing_benefits', 
    'get_gap_fixing_methods',
    'get_gap_detection_metrics'
]
