"""
CLI Module for SCHR Levels AutoML

Provides command-line interface for flexible control of SCHR Levels analysis.
"""

from .main import SCHRCLI
from .commands import (
    TrainCommand,
    PredictCommand, 
    BacktestCommand,
    ValidateCommand,
    WebCommand
)

__all__ = [
    "SCHRCLI",
    "TrainCommand",
    "PredictCommand",
    "BacktestCommand", 
    "ValidateCommand",
    "WebCommand"
]
