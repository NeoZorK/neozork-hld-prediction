"""
Database module for Pocket Hedge Fund.

This module provides database connectivity, models, and utilities
for the Pocket Hedge Fund system.
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import database components
from .connection import DatabaseManager, get_db_manager, init_database, close_database
from .models import (
    User, Fund, Investment, PortfolioPosition, TradingStrategy,
    FundStrategy, Transaction, PerformanceSnapshot, RiskMetric,
    APIKey, AuditLog, Base
)

__all__ = [
    "DatabaseManager",
    "get_db_manager",
    "init_database",
    "close_database",
    "User",
    "Fund", 
    "Investment",
    "PortfolioPosition",
    "TradingStrategy",
    "FundStrategy",
    "Transaction",
    "PerformanceSnapshot",
    "RiskMetric",
    "APIKey",
    "AuditLog",
    "Base"
]
