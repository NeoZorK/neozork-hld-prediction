# -*- coding: utf-8 -*-
"""
Trend Indicator Metrics Encyclopedia

This module provides comprehensive metrics information for trend indicators.
"""

from typing import Dict, Any

class TrendMetrics:
    """Comprehensive metrics for trend indicators."""
    
    @staticmethod
    def get_ema_metrics() -> Dict[str, Any]:
        """Get EMA-specific metrics and explanations."""
        return {
            'name': 'Exponential Moving Average (EMA)',
            'icon': '📈',
            'category': 'Trend',
            'description': 'Moving average that gives more weight to recent prices',
            'formula': 'EMA = (Close × Multiplier) + (Previous EMA × (1 - Multiplier))',
            'interpretation': 'Price above EMA indicates uptrend, below indicates downtrend',
            'good_range': 'Price within 2% of EMA',
            'excellent_range': 'Price within 1% of EMA',
            'warning_range': 'Price >5% away from EMA',
            'calculation_note': 'Multiplier = 2 / (Period + 1)',
            'strategy_impact': 'Primary tool for trend identification and dynamic support/resistance'
        }
    
    @staticmethod
    def get_sma_metrics() -> Dict[str, Any]:
        """Get SMA-specific metrics and explanations."""
        return {
            'name': 'Simple Moving Average (SMA)',
            'icon': '📊',
            'category': 'Trend',
            'description': 'Average of closing prices over specified period',
            'formula': 'SMA = Sum of Close prices / Number of periods',
            'interpretation': 'Price above SMA indicates uptrend, below indicates downtrend',
            'good_range': 'Price within 3% of SMA',
            'excellent_range': 'Price within 1.5% of SMA',
            'warning_range': 'Price >7% away from SMA',
            'calculation_note': 'Equal weight given to all prices in period',
            'strategy_impact': 'Reliable trend indicator with less noise than shorter EMAs'
        }
    
    @staticmethod
    def get_adx_metrics() -> Dict[str, Any]:
        """Get ADX-specific metrics and explanations."""
        return {
            'name': 'Average Directional Index (ADX)',
            'icon': '🎯',
            'category': 'Trend',
            'description': 'Measures trend strength regardless of direction',
            'formula': 'ADX = 100 × (Sum of +DI and -DI) / (Sum of +DI and -DI)',
            'interpretation': 'ADX >25 indicates strong trend, <20 indicates weak trend',
            'good_range': '20-40',
            'excellent_range': '25-50',
            'warning_range': '<15 or >60',
            'calculation_note': 'Based on directional movement and true range',
            'strategy_impact': 'Essential for determining if trend-following strategies are appropriate'
        }
    
    @staticmethod
    def get_sar_metrics() -> Dict[str, Any]:
        """Get SAR-specific metrics and explanations."""
        return {
            'name': 'Parabolic SAR',
            'icon': '📍',
            'category': 'Trend',
            'description': 'Trend-following indicator that provides entry and exit points',
            'formula': 'SAR = Previous SAR + AF × (EP - Previous SAR)',
            'interpretation': 'Dots below price indicate uptrend, above indicate downtrend',
            'good_range': 'SAR within 2% of price',
            'excellent_range': 'SAR within 1% of price',
            'warning_range': 'SAR >5% away from price',
            'calculation_note': 'AF (Acceleration Factor) increases with trend continuation',
            'strategy_impact': 'Excellent for trailing stops and trend following strategies'
        }
    
    @staticmethod
    def get_supertrend_metrics() -> Dict[str, Any]:
        """Get SuperTrend-specific metrics and explanations."""
        return {
            'name': 'SuperTrend',
            'icon': '🚀',
            'category': 'Trend',
            'description': 'Trend-following indicator with dynamic stop-loss levels',
            'formula': 'SuperTrend = (High + Low) / 2 ± (Multiplier × ATR)',
            'interpretation': 'Green line below price indicates uptrend, red above indicates downtrend',
            'good_range': 'SuperTrend within 3% of price',
            'excellent_range': 'SuperTrend within 1.5% of price',
            'warning_range': 'SuperTrend >7% away from price',
            'calculation_note': 'Uses ATR for volatility adjustment',
            'strategy_impact': 'Combines trend identification with risk management'
        }
    
    @staticmethod
    def get_all_trend_metrics() -> Dict[str, Dict[str, Any]]:
        """Get all trend metrics."""
        return {
            'EMA': TrendMetrics.get_ema_metrics(),
            'SMA': TrendMetrics.get_sma_metrics(),
            'ADX': TrendMetrics.get_adx_metrics(),
            'SAR': TrendMetrics.get_sar_metrics(),
            'SuperTrend': TrendMetrics.get_supertrend_metrics()
        }
