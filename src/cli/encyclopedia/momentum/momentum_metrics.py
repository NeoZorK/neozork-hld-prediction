# -*- coding: utf-8 -*-
"""
Momentum Indicator Metrics Encyclopedia

This module provides comprehensive metrics information for momentum indicators.
"""

from typing import Dict, Any

class MomentumMetrics:
    """Comprehensive metrics for momentum indicators."""
    
    @staticmethod
    def get_macd_metrics() -> Dict[str, Any]:
        """Get MACD-specific metrics and explanations."""
        return {
            'name': 'Moving Average Convergence Divergence (MACD)',
            'icon': '📊',
            'category': 'Momentum',
            'description': 'Trend-following momentum indicator showing relationship between two moving averages',
            'formula': 'MACD = Fast EMA - Slow EMA, Signal = EMA of MACD, Histogram = MACD - Signal',
            'interpretation': 'MACD above signal line indicates bullish momentum, below indicates bearish',
            'good_range': 'MACD within 0.5% of signal line',
            'excellent_range': 'MACD within 0.2% of signal line',
            'warning_range': 'MACD >2% away from signal line',
            'calculation_note': 'Default: 12-period fast EMA, 26-period slow EMA, 9-period signal',
            'strategy_impact': 'Excellent for identifying momentum shifts and trend changes'
        }
    
    @staticmethod
    def get_stoch_oscillator_metrics() -> Dict[str, Any]:
        """Get Stochastic Oscillator-specific metrics and explanations."""
        return {
            'name': 'Stochastic Oscillator',
            'icon': '🔄',
            'category': 'Momentum',
            'description': 'Momentum indicator comparing closing price to price range over time',
            'formula': '%K = ((Close - Lowest Low) / (Highest High - Lowest Low)) × 100',
            'interpretation': 'Values above 80 indicate overbought, below 20 indicate oversold',
            'good_range': '20-80',
            'excellent_range': '10-90',
            'warning_range': '<10 or >90',
            'calculation_note': 'Based on price position within recent high-low range',
            'strategy_impact': 'Effective for identifying momentum shifts and reversal signals'
        }
    
    @staticmethod
    def get_roc_metrics() -> Dict[str, Any]:
        """Get Rate of Change-specific metrics and explanations."""
        return {
            'name': 'Rate of Change (ROC)',
            'icon': '📈',
            'category': 'Momentum',
            'description': 'Momentum oscillator measuring percentage change in price over time',
            'formula': 'ROC = ((Current Close - Close n periods ago) / Close n periods ago) × 100',
            'interpretation': 'Positive values indicate upward momentum, negative indicate downward',
            'good_range': '-5% to +5%',
            'excellent_range': '-2% to +2%',
            'warning_range': '<-10% or >+10%',
            'calculation_note': 'Measures speed of price change relative to historical levels',
            'strategy_impact': 'Useful for identifying momentum strength and potential reversals'
        }
    
    @staticmethod
    def get_momentum_metrics() -> Dict[str, Any]:
        """Get Momentum-specific metrics and explanations."""
        return {
            'name': 'Momentum',
            'icon': '⚡',
            'category': 'Momentum',
            'description': 'Simple momentum indicator measuring price change over time',
            'formula': 'Momentum = Current Close - Close n periods ago',
            'interpretation': 'Positive values indicate upward momentum, negative indicate downward',
            'good_range': 'Price change within 2% of average',
            'excellent_range': 'Price change within 1% of average',
            'warning_range': 'Price change >5% from average',
            'calculation_note': 'Absolute price difference over specified period',
            'strategy_impact': 'Simple and effective momentum measurement tool'
        }
    
    @staticmethod
    def get_all_momentum_metrics() -> Dict[str, Dict[str, Any]]:
        """Get all momentum metrics."""
        return {
            'MACD': MomentumMetrics.get_macd_metrics(),
            'StochOscillator': MomentumMetrics.get_stoch_oscillator_metrics(),
            'ROC': MomentumMetrics.get_roc_metrics(),
            'Momentum': MomentumMetrics.get_momentum_metrics()
        }
