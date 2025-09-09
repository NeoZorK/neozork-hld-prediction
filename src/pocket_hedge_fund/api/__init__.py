"""
API module for Pocket Hedge Fund.

This module provides REST API endpoints for the Pocket Hedge Fund system,
including fund management, portfolio operations, and user interactions.
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import API components
from .fund_api import FundAPI
from .portfolio_api import PortfolioAPI
from .auth_api import AuthAPI
from .performance_api import PerformanceAPI

__all__ = [
    "FundAPI",
    "PortfolioAPI", 
    "AuthAPI",
    "PerformanceAPI"
]