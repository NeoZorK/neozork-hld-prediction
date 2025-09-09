"""
Services module for Pocket Hedge Fund

This module provides business logic services including
return calculations, risk management, and analytics.
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import services
from .return_calculator import ReturnCalculator, get_return_calculator

__all__ = [
    "ReturnCalculator",
    "get_return_calculator"
]
