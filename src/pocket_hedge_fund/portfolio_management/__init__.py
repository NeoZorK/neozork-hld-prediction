"""
Portfolio Management Module for Pocket Hedge Fund

This module provides comprehensive portfolio management functionality including:
- Core portfolio operations and position management
- Advanced analytics and performance tracking
- Risk management and monitoring
- Automated rebalancing and optimization
- Comprehensive reporting and insights
"""

from .core.portfolio_manager import PortfolioManager
from .core.position_manager import PositionManager
from .core.portfolio_operations import PortfolioOperations
from .analytics.performance_analyzer import PerformanceAnalyzer
from .analytics.attribution_analyzer import AttributionAnalyzer
from .analytics.benchmark_analyzer import BenchmarkAnalyzer
from .risk.risk_manager import RiskManager
from .risk.risk_monitor import RiskMonitor
from .risk.stress_tester import StressTester
from .automation.rebalancer import PortfolioRebalancer
from .automation.optimizer import PortfolioOptimizer
from .automation.auto_trader import AutoTrader
from .reporting.report_generator import PortfolioReportGenerator
from .reporting.data_visualizer import DataVisualizer
from .reporting.export_manager import ExportManager
from .models.portfolio_models import Portfolio, Position, Asset, AssetType, PositionType, PositionStatus
from .models.performance_models import PerformanceMetrics, RiskMetrics, AttributionMetrics
from .models.transaction_models import Transaction, Trade, RebalanceAction

__version__ = "1.0.0"
__author__ = "Pocket Hedge Fund Team"

__all__ = [
    # Core components
    'PortfolioManager',
    'PositionManager',
    'PortfolioOperations',
    
    # Analytics components
    'PerformanceAnalyzer',
    'AttributionAnalyzer',
    'BenchmarkAnalyzer',
    
    # Risk management components
    'RiskManager',
    'RiskMonitor',
    'StressTester',
    
    # Automation components
    'PortfolioRebalancer',
    'PortfolioOptimizer',
    'AutoTrader',
    
    # Reporting components
    'PortfolioReportGenerator',
    'DataVisualizer',
    'ExportManager',
    
    # Data models
    'Portfolio',
    'Position',
    'Asset',
    'AssetType',
    'PositionType',
    'PositionStatus',
    'PerformanceMetrics',
    'RiskMetrics',
    'AttributionMetrics',
    'Transaction',
    'Trade',
    'RebalanceAction'
]