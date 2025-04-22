# src/common/__init__.py

"""
Exposes common constants, logger, and potentially other shared utilities.
"""

# Expose selected constants and the logger instance/functions
from .constants import (
    TradingRule,
    BUY,
    SELL,
    NOTRADE,
    EMPTY_VALUE, # <-- Add EMPTY_VALUE
    VALID_DATA_SOURCES
)
from .logger import print_info, print_error, print_warning, print_success, print_debug

__all__ = [
    # Constants
    'TradingRule',
    'BUY',
    'SELL',
    'NOTRADE',
    'EMPTY_VALUE', # <-- Add EMPTY_VALUE to export list
    'VALID_DATA_SOURCES',
    # Logger functions
    'print_info',
    'print_error',
    'print_warning',
    'print_success',
    'print_debug',
    # Or expose the whole logger module if preferred:
    # 'logger'
]
