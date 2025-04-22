# src/calculation/__init__.py

"""
Exposes the main indicator calculation function.
"""

# Import from the module that contains the primary calculation entry point
from .indicator_calculation import calculate_indicator

__all__ = [
    'calculate_indicator'
]
