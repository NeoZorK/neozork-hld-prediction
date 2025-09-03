# -*- coding: utf-8 -*-
"""
Support/Resistance Indicator Metrics Encyclopedia

This module provides comprehensive metrics information for support/resistance indicators.
"""

from typing import Dict, Any

class SupportResistanceMetrics:
    """Comprehensive metrics for support/resistance indicators."""
    
    @staticmethod
    def get_pivot_points_metrics() -> Dict[str, Any]:
        """Get Pivot Points-specific metrics and explanations."""
        return {
            'name': 'Pivot Points',
            'icon': '📍',
            'category': 'Support/Resistance',
            'description': 'Key levels calculated from previous period high, low, and close',
            'formula': 'PP = (High + Low + Close) / 3, R1 = (2 × PP) - Low, S1 = (2 × PP) - High',
            'interpretation': 'Price above pivot indicates bullish bias, below indicates bearish',
            'good_range': 'Price within 0.5% of pivot level',
            'excellent_range': 'Price within 0.2% of pivot level',
            'warning_range': 'Price >2% away from pivot level',
            'calculation_note': 'Based on previous period OHLC data',
            'strategy_impact': 'Essential for day trading and short-term support/resistance identification'
        }
    
    @staticmethod
    def get_fibonacci_retracement_metrics() -> Dict[str, Any]:
        """Get Fibonacci Retracement-specific metrics and explanations."""
        return {
            'name': 'Fibonacci Retracement',
            'icon': '📐',
            'category': 'Support/Resistance',
            'description': 'Retracement levels based on Fibonacci ratios for trend analysis',
            'formula': 'Retracement = High - (High - Low) × Fibonacci Ratio (23.6%, 38.2%, 50%, 61.8%)',
            'interpretation': 'Retracement levels act as potential support/resistance during pullbacks',
            'good_range': 'Price within 0.3% of retracement level',
            'excellent_range': 'Price within 0.1% of retracement level',
            'warning_range': 'Price >1% away from retracement level',
            'calculation_note': 'Uses Fibonacci ratios applied to swing high/low',
            'strategy_impact': 'Popular tool for identifying entry points during trend corrections'
        }
    
    @staticmethod
    def get_donchian_channels_metrics() -> Dict[str, Any]:
        """Get Donchian Channels-specific metrics and explanations."""
        return {
            'name': 'Donchian Channels',
            'icon': '📊',
            'category': 'Support/Resistance',
            'description': 'Channel indicator using highest high and lowest low over period',
            'formula': 'Upper Channel = Highest High, Lower Channel = Lowest Low, Middle = (Upper + Lower) / 2',
            'interpretation': 'Channels provide dynamic support/resistance levels',
            'good_range': 'Price within 1% of channel boundary',
            'excellent_range': 'Price within 0.5% of channel boundary',
            'warning_range': 'Price >3% away from channel boundary',
            'calculation_note': 'Based on highest high and lowest low over specified period',
            'strategy_breakout': 'Effective for breakout trading and trend identification'
        }
    
    @staticmethod
    def get_support_resistance_metrics() -> Dict[str, Any]:
        """Get Support/Resistance-specific metrics and explanations."""
        return {
            'name': 'Support/Resistance Levels',
            'icon': '🛡️',
            'category': 'Support/Resistance',
            'description': 'Key price levels where buying/selling pressure is concentrated',
            'formula': 'Identified through historical price action, volume analysis, and technical levels',
            'interpretation': 'Support prevents price from falling, resistance prevents price from rising',
            'good_range': 'Price within 0.5% of level',
            'excellent_range': 'Price within 0.2% of level',
            'warning_range': 'Price >2% away from level',
            'calculation_note': 'Combines multiple analysis methods for level identification',
            'strategy_impact': 'Foundation for entry/exit points and risk management'
        }
    
    @staticmethod
    def get_all_support_resistance_metrics() -> Dict[str, Dict[str, Any]]:
        """Get all support/resistance metrics."""
        return {
            'Pivot_Points': SupportResistanceMetrics.get_pivot_points_metrics(),
            'Fibonacci_Retracement': SupportResistanceMetrics.get_fibonacci_retracement_metrics(),
            'Donchian_Channels': SupportResistanceMetrics.get_donchian_channels_metrics(),
            'Support_Resistance': SupportResistanceMetrics.get_support_resistance_metrics()
        }
