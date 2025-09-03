# -*- coding: utf-8 -*-
"""
Sentiment Indicator Metrics Encyclopedia

This module provides comprehensive metrics information for sentiment indicators.
"""

from typing import Dict, Any

class SentimentMetrics:
    """Comprehensive metrics for sentiment indicators."""
    
    @staticmethod
    def get_fear_greed_metrics() -> Dict[str, Any]:
        """Get Fear & Greed-specific metrics and explanations."""
        return {
            'name': 'Fear & Greed Index',
            'icon': '😨',
            'category': 'Sentiment',
            'description': 'Market sentiment indicator measuring fear vs. greed in the market',
            'formula': 'Combines multiple factors: volatility, momentum, market volume, put/call ratio, etc.',
            'interpretation': '0-25: Extreme Fear, 26-45: Fear, 46-55: Neutral, 56-75: Greed, 76-100: Extreme Greed',
            'good_range': '30-70 (balanced sentiment)',
            'excellent_range': '40-60 (neutral sentiment)',
            'warning_range': '<20 or >80 (extreme sentiment)',
            'calculation_note': 'Multi-factor composite index updated daily',
            'strategy_impact': 'Contrarian indicator: extreme fear often signals buying opportunity, extreme greed signals selling'
        }
    
    @staticmethod
    def get_cot_metrics() -> Dict[str, Any]:
        """Get COT-specific metrics and explanations."""
        return {
            'name': 'Commitments of Traders (COT)',
            'icon': '📊',
            'category': 'Sentiment',
            'description': 'Weekly report showing positions of different trader categories',
            'formula': 'Net Position = Long Positions - Short Positions',
            'interpretation': 'Large net long positions indicate bullish sentiment, large net short indicate bearish',
            'good_range': 'Net position within 20% of historical average',
            'excellent_range': 'Net position within 10% of historical average',
            'warning_range': 'Net position >50% above or below historical average',
            'calculation_note': 'Published weekly by CFTC for futures markets',
            'strategy_impact': 'Institutional sentiment indicator for major market participants'
        }
    
    @staticmethod
    def get_put_call_ratio_metrics() -> Dict[str, Any]:
        """Get Put/Call Ratio-specific metrics and explanations."""
        return {
            'name': 'Put/Call Ratio',
            'icon': '📈',
            'category': 'Sentiment',
            'description': 'Ratio of put option volume to call option volume',
            'formula': 'Put/Call Ratio = Put Option Volume / Call Option Volume',
            'interpretation': 'Ratio >1 indicates bearish sentiment, <1 indicates bullish sentiment',
            'good_range': '0.5-1.5 (balanced sentiment)',
            'excellent_range': '0.7-1.3 (neutral sentiment)',
            'warning_range': '<0.3 or >2.0 (extreme sentiment)',
            'calculation_note': 'Based on options trading volume and open interest',
            'strategy_impact': 'Contrarian indicator: extreme values often signal market reversals'
        }
    
    @staticmethod
    def get_vix_metrics() -> Dict[str, Any]:
        """Get VIX-specific metrics and explanations."""
        return {
            'name': 'Volatility Index (VIX)',
            'icon': '📊',
            'category': 'Sentiment',
            'description': 'Market volatility index measuring expected market volatility',
            'formula': 'Based on S&P 500 options implied volatility',
            'interpretation': 'High VIX indicates fear and uncertainty, low VIX indicates complacency',
            'good_range': '15-25 (normal volatility)',
            'excellent_range': '18-22 (low volatility)',
            'warning_range': '<12 or >35 (extreme volatility)',
            'calculation_note': 'Forward-looking volatility expectation based on options pricing',
            'strategy_impact': 'Fear gauge: high VIX often signals market bottoms, low VIX signals potential tops'
        }
    
    @staticmethod
    def get_market_sentiment_metrics() -> Dict[str, Any]:
        """Get Market Sentiment-specific metrics and explanations."""
        return {
            'name': 'Market Sentiment',
            'icon': '🎭',
            'category': 'Sentiment',
            'description': 'Composite sentiment indicator combining multiple sentiment measures',
            'formula': 'Weighted average of various sentiment indicators',
            'interpretation': 'Positive values indicate bullish sentiment, negative indicate bearish',
            'good_range': '-0.3 to +0.3 (balanced sentiment)',
            'excellent_range': '-0.2 to +0.2 (neutral sentiment)',
            'warning_range': '<-0.5 or >+0.5 (extreme sentiment)',
            'calculation_note': 'Combines multiple sentiment sources for comprehensive view',
            'strategy_impact': 'Overall market mood indicator for strategic positioning'
        }
    
    @staticmethod
    def get_all_sentiment_metrics() -> Dict[str, Dict[str, Any]]:
        """Get all sentiment metrics."""
        return {
            'FearGreed': SentimentMetrics.get_fear_greed_metrics(),
            'COT': SentimentMetrics.get_cot_metrics(),
            'PutCallRatio': SentimentMetrics.get_put_call_ratio_metrics(),
            'VIX': SentimentMetrics.get_vix_metrics(),
            'Market_Sentiment': SentimentMetrics.get_market_sentiment_metrics()
        }
