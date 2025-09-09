"""
Advanced Analytics Module for Pocket Hedge Fund

This module provides comprehensive analytics capabilities including:
- Machine Learning models for market prediction
- Advanced statistical analysis
- Real-time market insights
- Predictive analytics
- Risk modeling and forecasting
- Performance attribution analysis
- Market sentiment analysis
- Alternative data integration
"""

from .core.analytics_engine import AnalyticsEngine
from .core.data_processor import DataProcessor
from .core.feature_engineer import FeatureEngineer
from .core.insight_generator import InsightGenerator

from .models.analytics_models import (
    MarketData,
    PredictionResult,
    AnalyticsInsight,
    ModelPerformance,
    FeatureImportance
)

from .ml.prediction_models import (
    PricePredictor,
    VolatilityPredictor,
    SentimentAnalyzer,
    RiskPredictor
)

from .visualization.chart_generator import ChartGenerator
from .visualization.dashboard_builder import DashboardBuilder
from .visualization.report_visualizer import ReportVisualizer

from .insights.market_insights import MarketInsights
from .insights.performance_insights import PerformanceInsights
from .insights.risk_insights import RiskInsights

__version__ = "1.0.0"
__author__ = "Pocket Hedge Fund Team"

__all__ = [
    # Core components
    "AnalyticsEngine",
    "DataProcessor", 
    "FeatureEngineer",
    "InsightGenerator",
    
    # Models
    "MarketData",
    "PredictionResult",
    "AnalyticsInsight",
    "ModelPerformance",
    "FeatureImportance",
    
    # ML components
    "PricePredictor",
    "VolatilityPredictor", 
    "SentimentAnalyzer",
    "RiskPredictor",
    
    # Visualization
    "ChartGenerator",
    "DashboardBuilder",
    "ReportVisualizer",
    
    # Insights
    "MarketInsights",
    "PerformanceInsights",
    "RiskInsights"
]
