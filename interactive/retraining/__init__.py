# -*- coding: utf-8 -*-
"""
Retraining module for NeoZork Interactive ML Trading Strategy Development.

This module provides automated retraining and model management capabilities.
"""

from .automated_retraining import AutomatedRetraining
from .regime_detection import RegimeDetection
from .data_drift_detection import DataDriftDetection

class RetrainingSystem:
    """Main retraining system class."""
    def __init__(self):
        self.automated_retraining = AutomatedRetraining()
        self.regime_detection = RegimeDetection()
        self.data_drift_detection = DataDriftDetection()

__all__ = [
    'RetrainingSystem',
    'AutomatedRetraining',
    'RegimeDetection',
    'DataDriftDetection'
]
