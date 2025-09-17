"""
Analytics Insights

This module generates actionable insights from analytics data:
- Market insights and trends
- Performance insights and attribution
- Risk insights and warnings
- Trading signals and recommendations
- Market regime analysis
"""

from .market_insights import MarketInsights
from .performance_insights import PerformanceInsights
from .risk_insights import RiskInsights
from .trading_insights import TradingInsights
from .regime_insights import RegimeInsights

__all__ = [
    "MarketInsights",
    "PerformanceInsights",
    "RiskInsights",
    "TradingInsights",
    "RegimeInsights"
]
