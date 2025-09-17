"""
Performance and Risk Data Models

This module defines data models for performance metrics, risk metrics,
and attribution analysis.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from decimal import Decimal


@dataclass
class PerformanceMetrics:
    """Performance metrics data model."""
    # Return metrics
    total_return: float
    annualized_return: float
    monthly_return: float
    daily_return: float
    
    # Risk-adjusted returns
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    information_ratio: float
    
    # Volatility metrics
    volatility: float
    annualized_volatility: float
    tracking_error: float
    
    # Drawdown metrics
    max_drawdown: float
    current_drawdown: float
    drawdown_duration: int  # days
    
    # Other metrics
    win_rate: float
    profit_factor: float
    alpha: float
    beta: float
    
    # Period information
    period_start: date
    period_end: date
    calculation_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RiskMetrics:
    """Risk metrics data model."""
    # Value at Risk
    var_95: float
    var_99: float
    cvar_95: float
    cvar_99: float
    
    # Risk ratios
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    
    # Volatility metrics
    volatility: float
    beta: float
    correlation_to_market: float
    
    # Concentration risk
    herfindahl_index: float
    max_position_weight: float
    sector_concentration: Dict[str, float]
    
    # Stress test results
    stress_test_results: Dict[str, Any]
    
    # Risk limits
    risk_limits: Dict[str, float]
    limit_breaches: List[Dict[str, Any]]
    
    calculation_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AttributionMetrics:
    """Performance attribution metrics data model."""
    # Attribution effects
    asset_allocation_effect: float
    security_selection_effect: float
    interaction_effect: float
    total_attribution: float
    
    # Top contributors
    top_contributors: List[Dict[str, Any]]
    bottom_contributors: List[Dict[str, Any]]
    
    # Sector attribution
    sector_attribution: Dict[str, float]
    
    # Asset class attribution
    asset_class_attribution: Dict[str, float]
    
    # Time period
    period_start: date
    period_end: date
    calculation_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BenchmarkComparison:
    """Benchmark comparison data model."""
    benchmark_name: str
    benchmark_return: float
    portfolio_return: float
    excess_return: float
    tracking_error: float
    information_ratio: float
    beta: float
    alpha: float
    correlation: float
    
    # Rolling metrics
    rolling_alpha: List[float]
    rolling_beta: List[float]
    rolling_correlation: List[float]
    
    # Period information
    period_start: date
    period_end: date
    calculation_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PerformanceSnapshot:
    """Performance snapshot data model."""
    portfolio_id: str
    date: date
    total_value: Decimal
    total_return: float
    daily_return: float
    positions_count: int
    cash_balance: Decimal
    
    # Risk metrics
    var_95: float
    volatility: float
    max_drawdown: float
    
    # Attribution
    top_contributor: Optional[str]
    top_contribution: float
    bottom_contributor: Optional[str]
    bottom_contribution: float
    
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RiskLimit:
    """Risk limit data model."""
    limit_type: str
    limit_value: float
    current_value: float
    is_breached: bool
    breach_severity: str  # low, medium, high, critical
    breach_date: Optional[datetime] = None
    last_checked: datetime = field(default_factory=datetime.utcnow)


@dataclass
class StressTestResult:
    """Stress test result data model."""
    scenario_name: str
    scenario_description: str
    portfolio_loss: float
    var_impact: float
    max_drawdown_impact: float
    affected_positions: List[str]
    recommendations: List[str]
    
    test_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PerformanceReport:
    """Comprehensive performance report data model."""
    portfolio_id: str
    report_period: str
    performance_metrics: PerformanceMetrics
    risk_metrics: RiskMetrics
    attribution_metrics: AttributionMetrics
    benchmark_comparison: Optional[BenchmarkComparison]
    
    # Summary statistics
    summary: Dict[str, Any]
    key_insights: List[str]
    recommendations: List[str]
    
    # Report metadata
    generated_at: datetime = field(default_factory=datetime.utcnow)
    generated_by: str = "system"
    report_version: str = "1.0"
