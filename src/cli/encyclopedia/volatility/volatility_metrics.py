# -*- coding: utf-8 -*-
"""
Volatility Indicator Metrics Encyclopedia

This module provides comprehensive metrics information for volatility indicators.
"""

from typing import Dict, Any

class VolatilityMetrics:
    """Comprehensive metrics for volatility indicators."""
    
    @staticmethod
    def get_atr_metrics() -> Dict[str, Any]:
        """Get ATR-specific metrics and explanations."""
        return {
            'name': 'Average True Range (ATR)',
            'icon': '📏',
            'category': 'Volatility',
            'description': 'Measures market volatility by decomposing the entire range of an asset',
            'formula': 'ATR = EMA of True Range, True Range = max(High-Low, |High-Previous Close|, |Low-Previous Close|)',
            'interpretation': 'Higher ATR indicates higher volatility, lower indicates lower volatility',
            'good_range': 'ATR within 20% of historical average',
            'excellent_range': 'ATR within 10% of historical average',
            'warning_range': 'ATR >50% above or <50% below historical average',
            'calculation_note': 'Uses true range to account for gaps and limit moves',
            'strategy_impact': 'Essential for position sizing and stop-loss placement'
        }
    
    @staticmethod
    def get_bollinger_bands_metrics() -> Dict[str, Any]:
        """Get Bollinger Bands-specific metrics and explanations."""
        return {
            'name': 'Bollinger Bands',
            'icon': '📊',
            'category': 'Volatility',
            'description': 'Volatility indicator with upper and lower bands around moving average',
            'formula': 'Upper Band = SMA + (Standard Deviation × Multiplier), Lower Band = SMA - (Standard Deviation × Multiplier)',
            'interpretation': 'Bands widening indicates increasing volatility, narrowing indicates decreasing',
            'good_range': 'Price within 2 standard deviations of mean',
            'excellent_range': 'Price within 1.5 standard deviations of mean',
            'warning_range': 'Price outside 2.5 standard deviations of mean',
            'calculation_note': 'Uses standard deviation to measure price dispersion',
            'strategy_impact': 'Excellent for identifying overbought/oversold conditions and volatility breakouts'
        }
    
    @staticmethod
    def get_stdev_metrics() -> Dict[str, Any]:
        """Get Standard Deviation-specific metrics and explanations."""
        return {
            'name': 'Standard Deviation',
            'icon': '📈',
            'category': 'Volatility',
            'description': 'Statistical measure of price dispersion around the mean',
            'formula': 'StDev = √(Σ(x - μ)² / n) where x = price, μ = mean, n = periods',
            'interpretation': 'Higher values indicate higher volatility, lower values indicate lower volatility',
            'good_range': 'Within 20% of historical average',
            'excellent_range': 'Within 10% of historical average',
            'warning_range': '>50% above or <50% below historical average',
            'calculation_note': 'Square root of variance, measures spread of data',
            'strategy_impact': 'Statistical foundation for volatility analysis and risk management'
        }
    
    @staticmethod
    def get_keltner_channels_metrics() -> Dict[str, Any]:
        """Get Keltner Channels-specific metrics and explanations."""
        return {
            'name': 'Keltner Channels',
            'icon': '📊',
            'category': 'Volatility',
            'description': 'Volatility-based envelope indicator using ATR for channel width',
            'formula': 'Upper Channel = EMA + (ATR × Multiplier), Lower Channel = EMA - (ATR × Multiplier)',
            'interpretation': 'Channels widening indicates increasing volatility, narrowing indicates decreasing',
            'good_range': 'Price within 1.5 ATR of EMA',
            'excellent_range': 'Price within 1 ATR of EMA',
            'warning_range': 'Price outside 2.5 ATR of EMA',
            'calculation_note': 'Uses ATR instead of standard deviation for volatility measurement',
            'strategy_impact': 'Effective for trend following and volatility breakout strategies'
        }
    
    @staticmethod
    def get_all_volatility_metrics() -> Dict[str, Dict[str, Any]]:
        """Get all volatility metrics."""
        return {
            'ATR': VolatilityMetrics.get_atr_metrics(),
            'Bollinger_Bands': VolatilityMetrics.get_bollinger_bands_metrics(),
            'StDev': VolatilityMetrics.get_stdev_metrics(),
            'Keltner_Channels': VolatilityMetrics.get_keltner_channels_metrics()
        }
