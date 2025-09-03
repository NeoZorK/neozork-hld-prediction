# -*- coding: utf-8 -*-
"""
Oscillator Trading Tips Encyclopedia

This module provides comprehensive trading tips for oscillator indicators.
"""

from typing import Dict, Any, List

class OscillatorTips:
    """Comprehensive trading tips for oscillator indicators."""
    
    @staticmethod
    def get_rsi_tips() -> List[Dict[str, Any]]:
        """Get RSI-specific trading tips."""
        return [
            {
                'title': 'RSI Divergence Strategy',
                'description': 'Look for price making new highs while RSI makes lower highs (bearish divergence) or price making new lows while RSI makes higher lows (bullish divergence)',
                'difficulty': 'Intermediate',
                'risk_level': 'Medium',
                'best_market': 'Trending',
                'timeframe': '4H-1D'
            },
            {
                'title': 'RSI Overbought/Oversold Bounces',
                'description': 'Trade bounces from extreme levels: buy when RSI crosses above 30, sell when RSI crosses below 70',
                'difficulty': 'Beginner',
                'risk_level': 'Low',
                'best_market': 'Ranging',
                'timeframe': '1H-4H'
            },
            {
                'title': 'RSI Centerline Crossovers',
                'description': 'Use RSI crossing above/below 50 as trend confirmation signals',
                'difficulty': 'Beginner',
                'risk_level': 'Low',
                'best_market': 'Trending',
                'timeframe': '1D-1W'
            }
        ]
    
    @staticmethod
    def get_stochastic_tips() -> List[Dict[str, Any]]:
        """Get Stochastic-specific trading tips."""
        return [
            {
                'title': 'Stochastic Crossover Strategy',
                'description': 'Buy when %K line crosses above %D line in oversold territory, sell when %K crosses below %D in overbought territory',
                'difficulty': 'Beginner',
                'risk_level': 'Low',
                'best_market': 'Ranging',
                'timeframe': '1H-4H'
            },
            {
                'title': 'Stochastic Divergence',
                'description': 'Identify potential reversals when price and stochastic show opposite movements',
                'difficulty': 'Intermediate',
                'risk_level': 'Medium',
                'best_market': 'Trending',
                'timeframe': '4H-1D'
            },
            {
                'title': 'Stochastic Range Trading',
                'description': 'Use extreme levels (20/80) as support and resistance for range-bound markets',
                'difficulty': 'Beginner',
                'risk_level': 'Low',
                'best_market': 'Ranging',
                'timeframe': '1H-4H'
            }
        ]
    
    @staticmethod
    def get_cci_tips() -> List[Dict[str, Any]]:
        """Get CCI-specific trading tips."""
        return [
            {
                'title': 'CCI Zero Line Crossovers',
                'description': 'Use CCI crossing above/below zero as trend direction signals',
                'difficulty': 'Beginner',
                'risk_level': 'Low',
                'best_market': 'Trending',
                'timeframe': '1D-1W'
            },
            {
                'title': 'CCI Extreme Level Trading',
                'description': 'Trade reversals from extreme levels: buy when CCI crosses above -100, sell when CCI crosses below +100',
                'difficulty': 'Intermediate',
                'risk_level': 'Medium',
                'best_market': 'Ranging',
                'timeframe': '4H-1D'
            },
            {
                'title': 'CCI Trend Confirmation',
                'description': 'Use CCI staying above/below zero to confirm trend strength and direction',
                'difficulty': 'Beginner',
                'risk_level': 'Low',
                'best_market': 'Trending',
                'timeframe': '1D-1W'
            }
        ]
    
    @staticmethod
    def get_williams_r_tips() -> List[Dict[str, Any]]:
        """Get Williams %R-specific trading tips."""
        return [
            {
                'title': 'Williams %R Reversal Signals',
                'description': 'Buy when %R crosses above -80, sell when %R crosses below -20',
                'difficulty': 'Beginner',
                'risk_level': 'Low',
                'best_market': 'Ranging',
                'timeframe': '1H-4H'
            },
            {
                'title': 'Williams %R Trend Confirmation',
                'description': 'Use %R staying in extreme territories to confirm trend continuation',
                'difficulty': 'Intermediate',
                'risk_level': 'Medium',
                'best_market': 'Trending',
                'timeframe': '4H-1D'
            },
            {
                'title': 'Williams %R Divergence',
                'description': 'Look for price and %R moving in opposite directions for reversal signals',
                'difficulty': 'Advanced',
                'risk_level': 'High',
                'best_market': 'Trending',
                'timeframe': '1D-1W'
            }
        ]
    
    @staticmethod
    def get_general_oscillator_tips() -> List[Dict[str, Any]]:
        """Get general tips for all oscillators."""
        return [
            {
                'title': 'Multiple Timeframe Analysis',
                'description': 'Use oscillators on multiple timeframes to confirm signals and reduce false positives',
                'difficulty': 'Intermediate',
                'risk_level': 'Low',
                'best_market': 'All',
                'timeframe': 'Multi'
            },
            {
                'title': 'Oscillator Combination',
                'description': 'Combine multiple oscillators (e.g., RSI + Stochastic) for stronger confirmation signals',
                'difficulty': 'Intermediate',
                'risk_level': 'Medium',
                'best_market': 'All',
                'timeframe': 'All'
            },
            {
                'title': 'Volume Confirmation',
                'description': 'Use volume to confirm oscillator signals - higher volume increases signal reliability',
                'difficulty': 'Beginner',
                'risk_level': 'Low',
                'best_market': 'All',
                'timeframe': 'All'
            },
            {
                'title': 'Market Context',
                'description': 'Consider overall market trend and volatility when interpreting oscillator signals',
                'difficulty': 'Advanced',
                'risk_level': 'Low',
                'best_market': 'All',
                'timeframe': 'All'
            }
        ]
    
    @staticmethod
    def get_all_oscillator_tips() -> Dict[str, List[Dict[str, Any]]]:
        """Get all oscillator tips."""
        return {
            'RSI': OscillatorTips.get_rsi_tips(),
            'Stochastic': OscillatorTips.get_stochastic_tips(),
            'CCI': OscillatorTips.get_cci_tips(),
            'Williams_R': OscillatorTips.get_williams_r_tips(),
            'General': OscillatorTips.get_general_oscillator_tips()
        }
