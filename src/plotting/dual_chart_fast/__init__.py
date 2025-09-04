# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fast/__init__.py

"""
Dual chart fast plotting module.

This module provides functionality for creating dual charts with
main OHLC chart and secondary indicator chart using Plotly.
"""

from .core.main_plotter import plot_dual_chart_fast, create_dual_chart_fast

__all__ = [
    'plot_dual_chart_fast',
    'create_dual_chart_fast'
]
