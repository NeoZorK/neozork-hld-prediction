"""
Database module for Pocket Hedge Fund.

This module provides database connectivity, models, and utilities
for the Pocket Hedge Fund system.
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import database components
from .connection import DatabaseManager, get_db_connection
from .models import (
    FundModel,
    PortfolioModel,
    PerformanceModel,
    RiskModel,
    UserModel,
    TransactionModel,
    StrategyModel
)
from .migrations import MigrationManager
from .utils import DatabaseUtils

__all__ = [
    "DatabaseManager",
    "get_db_connection",
    "FundModel",
    "PortfolioModel", 
    "PerformanceModel",
    "RiskModel",
    "UserModel",
    "TransactionModel",
    "StrategyModel",
    "MigrationManager",
    "DatabaseUtils"
]
