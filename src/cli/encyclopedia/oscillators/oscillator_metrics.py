# -*- coding: utf-8 -*-
"""
Oscillator Metrics Encyclopedia

This module provides comprehensive metrics information for oscillator indicators.
"""

from typing import Dict, Any

class OscillatorMetrics:
    """Comprehensive metrics for oscillator indicators."""
    
    @staticmethod
    def get_rsi_metrics() -> Dict[str, Any]:
        """Get RSI-specific metrics and explanations."""
        return {
            'name': 'Relative Strength Index (RSI)',
            'icon': '📊',
            'category': 'Oscillator',
            'description': 'Momentum oscillator measuring speed and change of price movements',
            'formula': 'RSI = 100 - (100 / (1 + RS)) where RS = Average Gain / Average Loss',
            'interpretation': 'Values above 70 indicate overbought, below 30 indicate oversold',
            'good_range': '30-70',
            'excellent_range': '20-80',
            'warning_range': '<20 or >80',
            'calculation_note': 'Based on average gains and losses over specified period',
            'strategy_impact': 'Key tool for identifying potential reversal points and momentum shifts'
        }
    
    @staticmethod
    def get_stochastic_metrics() -> Dict[str, Any]:
        """Get Stochastic-specific metrics and explanations."""
        return {
            'name': 'Stochastic Oscillator',
            'icon': '🔄',
            'category': 'Oscillator',
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
    def get_cci_metrics() -> Dict[str, Any]:
        """Get CCI-specific metrics and explanations."""
        return {
            'name': 'Commodity Channel Index (CCI)',
            'icon': '📈',
            'category': 'Oscillator',
            'description': 'Measures current price level relative to average price over time',
            'formula': 'CCI = (Typical Price - SMA) / (0.015 × Mean Deviation)',
            'interpretation': 'Values above +100 indicate overbought, below -100 indicate oversold',
            'good_range': '-100 to +100',
            'excellent_range': '-150 to +150',
            'warning_range': '<-150 or >+150',
            'calculation_note': 'Uses typical price and mean deviation for normalization',
            'strategy_impact': 'Useful for identifying cyclical trends and extreme conditions'
        }
    
    @staticmethod
    def get_williams_r_metrics() -> Dict[str, Any]:
        """Get Williams %R-specific metrics and explanations."""
        return {
            'name': 'Williams %R',
            'icon': '📉',
            'category': 'Oscillator',
            'description': 'Momentum indicator measuring overbought and oversold levels',
            'formula': '%R = ((Highest High - Close) / (Highest High - Lowest Low)) × -100',
            'interpretation': 'Values above -20 indicate overbought, below -80 indicate oversold',
            'good_range': '-80 to -20',
            'excellent_range': '-90 to -10',
            'warning_range': '<-90 or >-10',
            'calculation_note': 'Inverted scale where 0 is highest and -100 is lowest',
            'strategy_impact': 'Effective for timing entries and exits in trending markets'
        }
    
    @staticmethod
    def get_all_oscillator_metrics() -> Dict[str, Dict[str, Any]]:
        """Get all oscillator metrics."""
        return {
            'RSI': OscillatorMetrics.get_rsi_metrics(),
            'Stochastic': OscillatorMetrics.get_stochastic_metrics(),
            'CCI': OscillatorMetrics.get_cci_metrics(),
            'Williams_R': OscillatorMetrics.get_williams_r_metrics()
        }
