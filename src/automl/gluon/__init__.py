"""
SCHR Levels AutoML - Gluon Integration Module

This module provides AutoML capabilities for SCHR Levels financial data analysis
using AutoGluon for machine learning model training and prediction.

Main Components:
- CLI interface for flexible script control
- Web dashboard for visualization
- Analysis tools for backtesting and validation
- Model management and utilities

Author: Neozork Team
Version: 1.0.0
"""

from .cli.main import SCHRCLI
from .analysis.pipeline import SCHRLevelsAutoMLPipeline
from .web.dashboard import SCHRWebDashboard

__version__ = "1.0.0"
__author__ = "Neozork Team"

__all__ = [
    "SCHRCLI",
    "SCHRLevelsAutoMLPipeline", 
    "SCHRWebDashboard"
]