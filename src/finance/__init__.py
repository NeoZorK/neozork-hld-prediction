"""
Financial Analysis Module

This module provides comprehensive financial analysis capabilities for OHLCV data,
including price validation, volatility analysis, returns analysis, and drawdown analysis.

Modules:
- file_operations: Data I/O operations
- cli_interface: CLI argument parsing
- color_utils: Terminal color utilities
- reporting: Report generation
- progress_tracker: Progress tracking
- ohlcv_analysis: OHLCV data analysis
- volatility_analysis: Volatility analysis
- returns_analysis: Returns analysis
- drawdown_analysis: Drawdown analysis
- core: Core financial analysis components
"""

__version__ = "1.0.0"
__author__ = "Neozork Financial Analysis Team"

# Import main classes for easy access
from .file_operations import FinanceFileOperations
from .cli_interface import FinanceCLI
from .reporting import FinanceReporter
from .progress_tracker import FinanceProgressTracker
from .ohlcv_analysis import OHLCVAnalysis
from .volatility_analysis import VolatilityAnalysis
from .returns_analysis import ReturnsAnalysis
from .drawdown_analysis import DrawdownAnalysis

__all__ = [
    'FinanceFileOperations',
    'FinanceCLI', 
    'FinanceReporter',
    'FinanceProgressTracker',
    'OHLCVAnalysis',
    'VolatilityAnalysis',
    'ReturnsAnalysis',
    'DrawdownAnalysis'
]
