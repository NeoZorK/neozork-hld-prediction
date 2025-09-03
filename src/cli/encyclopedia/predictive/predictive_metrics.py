# -*- coding: utf-8 -*-
"""
Predictive Indicator Metrics Encyclopedia

This module provides comprehensive metrics information for predictive indicators.
"""

from typing import Dict, Any

class PredictiveMetrics:
    """Comprehensive metrics for predictive indicators."""
    
    @staticmethod
    def get_hma_metrics() -> Dict[str, Any]:
        """Get HMA-specific metrics and explanations."""
        return {
            'name': 'Hull Moving Average (HMA)',
            'icon': '🚀',
            'category': 'Predictive',
            'description': 'Fast and smooth moving average that reduces lag and noise',
            'formula': 'HMA = WMA(2 × WMA(n/2) - WMA(n)) where WMA = Weighted Moving Average',
            'interpretation': 'HMA above price indicates uptrend, below indicates downtrend',
            'good_range': 'Price within 1% of HMA',
            'excellent_range': 'Price within 0.5% of HMA',
            'warning_range': 'Price >3% away from HMA',
            'calculation_note': 'Uses weighted moving averages to reduce lag',
            'strategy_impact': 'Excellent for early trend identification with minimal lag'
        }
    
    @staticmethod
    def get_tsforecast_metrics() -> Dict[str, Any]:
        """Get Time Series Forecast-specific metrics and explanations."""
        return {
            'name': 'Time Series Forecast (TSF)',
            'icon': '🔮',
            'category': 'Predictive',
            'description': 'Linear regression-based indicator that projects future price levels',
            'formula': 'TSF = a + bx where a = intercept, b = slope, x = time period',
            'interpretation': 'TSF above price indicates bullish projection, below indicates bearish',
            'good_range': 'Price within 2% of TSF projection',
            'excellent_range': 'Price within 1% of TSF projection',
            'warning_range': 'Price >5% away from TSF projection',
            'calculation_note': 'Based on linear regression of price over time',
            'strategy_impact': 'Useful for identifying potential future price targets and trend direction'
        }
    
    @staticmethod
    def get_linear_regression_metrics() -> Dict[str, Any]:
        """Get Linear Regression-specific metrics and explanations."""
        return {
            'name': 'Linear Regression',
            'icon': '📊',
            'category': 'Predictive',
            'description': 'Statistical method to identify trend direction and strength',
            'formula': 'y = mx + b where m = slope, b = y-intercept, x = time, y = price',
            'interpretation': 'Positive slope indicates uptrend, negative indicates downtrend',
            'good_range': 'R² > 0.7 (strong correlation)',
            'excellent_range': 'R² > 0.85 (very strong correlation)',
            'warning_range': 'R² < 0.5 (weak correlation)',
            'calculation_note': 'Uses least squares method to fit line to price data',
            'strategy_impact': 'Statistical foundation for trend analysis and forecasting'
        }
    
    @staticmethod
    def get_polynomial_regression_metrics() -> Dict[str, Any]:
        """Get Polynomial Regression-specific metrics and explanations."""
        return {
            'name': 'Polynomial Regression',
            'icon': '📈',
            'category': 'Predictive',
            'description': 'Non-linear regression method for complex price patterns',
            'formula': 'y = ax³ + bx² + cx + d (3rd degree polynomial example)',
            'interpretation': 'Higher degree polynomials can capture more complex patterns',
            'good_range': 'R² > 0.8 (strong fit)',
            'excellent_range': 'R² > 0.9 (very strong fit)',
            'warning_range': 'R² < 0.6 (weak fit)',
            'calculation_note': 'Uses polynomial functions to fit non-linear price patterns',
            'strategy_impact': 'Advanced tool for identifying complex market patterns and cycles'
        }
    
    @staticmethod
    def get_all_predictive_metrics() -> Dict[str, Dict[str, Any]]:
        """Get all predictive metrics."""
        return {
            'HMA': PredictiveMetrics.get_hma_metrics(),
            'TSForecast': PredictiveMetrics.get_tsforecast_metrics(),
            'Linear_Regression': PredictiveMetrics.get_linear_regression_metrics(),
            'Polynomial_Regression': PredictiveMetrics.get_polynomial_regression_metrics()
        }
