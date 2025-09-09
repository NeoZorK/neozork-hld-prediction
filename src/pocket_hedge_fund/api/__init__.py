"""
API module for Pocket Hedge Fund.

This module provides REST API endpoints for the Pocket Hedge Fund system,
including fund management, portfolio operations, and user interactions.
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import API components
from .fund_api import router as fund_router

__all__ = [
    "fund_router"
]