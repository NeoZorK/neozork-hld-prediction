"""
API module for Pocket Hedge Fund.

This module provides REST API endpoints for the Pocket Hedge Fund system,
including fund management, portfolio operations, and user interactions.
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import API components
from .fund_api import router as fund_router
from .investment_api import router as investment_router
from .portfolio_api import router as portfolio_router
from .returns_api import router as returns_router
from .web_api import router as web_router
from .mobile_api import router as mobile_router

__all__ = [
    "fund_router",
    "investment_router",
    "portfolio_router",
    "returns_router",
    "web_router",
    "mobile_router"
]