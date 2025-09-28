"""
Web Dashboard Module for SCHR Levels AutoML

Provides interactive web visualizations for all analysis components.
"""

from .dashboard import SCHRWebDashboard
from .components import (
    BacktestVisualizer,
    ForecastVisualizer, 
    WalkForwardVisualizer,
    MonteCarloVisualizer,
    AccuracyStabilityVisualizer,
    ProbabilitiesVisualizer
)

__all__ = [
    "SCHRWebDashboard",
    "BacktestVisualizer",
    "ForecastVisualizer",
    "WalkForwardVisualizer", 
    "MonteCarloVisualizer",
    "AccuracyStabilityVisualizer",
    "ProbabilitiesVisualizer"
]
