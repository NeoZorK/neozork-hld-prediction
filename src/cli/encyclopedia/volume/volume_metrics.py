# -*- coding: utf-8 -*-
"""
Volume Indicator Metrics Encyclopedia

This module provides comprehensive metrics information for volume indicators.
"""

from typing import Dict, Any

class VolumeMetrics:
    """Comprehensive metrics for volume indicators."""
    
    @staticmethod
    def get_obv_metrics() -> Dict[str, Any]:
        """Get OBV-specific metrics and explanations."""
        return {
            'name': 'On-Balance Volume (OBV)',
            'icon': '📊',
            'category': 'Volume',
            'description': 'Cumulative volume indicator that measures buying and selling pressure',
            'formula': 'OBV = Previous OBV + Current Volume (if Close > Previous Close) or - Current Volume (if Close < Previous Close)',
            'interpretation': 'OBV rising confirms uptrend, falling confirms downtrend',
            'good_range': 'OBV trend matches price trend',
            'excellent_range': 'OBV trend strongly confirms price trend',
            'warning_range': 'OBV trend diverges from price trend',
            'calculation_note': 'Cumulative sum based on price direction and volume',
            'strategy_impact': 'Essential for confirming price movements and identifying divergences'
        }
    
    @staticmethod
    def get_vwap_metrics() -> Dict[str, Any]:
        """Get VWAP-specific metrics and explanations."""
        return {
            'name': 'Volume Weighted Average Price (VWAP)',
            'icon': '⚖️',
            'category': 'Volume',
            'description': 'Average price weighted by volume, used as dynamic support/resistance',
            'formula': 'VWAP = Sum of (Price × Volume) / Sum of Volume',
            'interpretation': 'Price above VWAP indicates bullish bias, below indicates bearish',
            'good_range': 'Price within 0.5% of VWAP',
            'excellent_range': 'Price within 0.2% of VWAP',
            'warning_range': 'Price >2% away from VWAP',
            'calculation_note': 'Volume-weighted average over specified period',
            'strategy_impact': 'Institutional benchmark for fair value and trade execution'
        }
    
    @staticmethod
    def get_volume_sma_metrics() -> Dict[str, Any]:
        """Get Volume SMA-specific metrics and explanations."""
        return {
            'name': 'Volume Simple Moving Average',
            'icon': '📈',
            'category': 'Volume',
            'description': 'Average volume over specified period for trend analysis',
            'formula': 'Volume SMA = Sum of Volume / Number of periods',
            'interpretation': 'Current volume above SMA indicates high activity, below indicates low activity',
            'good_range': 'Current volume within 50% of SMA',
            'excellent_range': 'Current volume within 25% of SMA',
            'warning_range': 'Current volume >200% or <25% of SMA',
            'calculation_note': 'Simple average of volume over specified period',
            'strategy_impact': 'Useful for identifying unusual volume activity and market interest'
        }
    
    @staticmethod
    def get_volume_ema_metrics() -> Dict[str, Any]:
        """Get Volume EMA-specific metrics and explanations."""
        return {
            'name': 'Volume Exponential Moving Average',
            'icon': '📊',
            'category': 'Volume',
            'description': 'Volume average with more weight on recent periods',
            'formula': 'Volume EMA = (Current Volume × Multiplier) + (Previous EMA × (1 - Multiplier))',
            'interpretation': 'Current volume above EMA indicates increasing activity',
            'good_range': 'Current volume within 40% of EMA',
            'excellent_range': 'Current volume within 20% of EMA',
            'warning_range': 'Current volume >300% or <20% of EMA',
            'calculation_note': 'Exponential weighting gives more importance to recent volume',
            'strategy_impact': 'More responsive to recent volume changes than simple average'
        }
    
    @staticmethod
    def get_all_volume_metrics() -> Dict[str, Dict[str, Any]]:
        """Get all volume metrics."""
        return {
            'OBV': VolumeMetrics.get_obv_metrics(),
            'VWAP': VolumeMetrics.get_vwap_metrics(),
            'Volume_SMA': VolumeMetrics.get_volume_sma_metrics(),
            'Volume_EMA': VolumeMetrics.get_volume_ema_metrics()
        }
