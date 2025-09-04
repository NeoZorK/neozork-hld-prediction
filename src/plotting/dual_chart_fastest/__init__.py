# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fastest/__init__.py

"""
Dual chart fastest plotting module.

This module provides functionality for creating dual charts with
main OHLC chart and secondary indicator chart using Plotly.
"""

from .core.main_plotter import plot_dual_chart_fastest, create_dual_chart_fastest

__all__ = [
    'plot_dual_chart_fastest',
    'create_dual_chart_fastest'
]
