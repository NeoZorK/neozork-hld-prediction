# -*- coding: utf-8 -*-
"""
Sentiment Trading Tips

This module provides trading tips for sentiment indicators.
"""


class SentimentTips:
    """Trading tips for sentiment indicators."""
    
    @staticmethod
    def get_fear_greed_tips():
        """Get Fear & Greed Index trading tips."""
        return [
            "Extreme fear often signals buying opportunities",
            "Extreme greed often signals selling opportunities",
            "Use as contrarian indicator",
            "Combine with technical analysis",
            "Monitor for sentiment extremes"
        ]
    
    @staticmethod
    def get_cot_tips():
        """Get COT trading tips."""
        return [
            "Large speculator positions show sentiment",
            "Commercial positions show smart money",
            "Use for contrarian signals",
            "Monitor position changes weekly",
            "Combine with price action analysis"
        ]
    
    @staticmethod
    def get_put_call_ratio_tips():
        """Get Put/Call Ratio trading tips."""
        return [
            "High put/call ratio = bearish sentiment",
            "Low put/call ratio = bullish sentiment",
            "Use as contrarian indicator",
            "Monitor for extreme readings",
            "Combine with technical analysis"
        ]
    
    @staticmethod
    def get_vix_tips():
        """Get VIX trading tips."""
        return [
            "High VIX = high fear, potential buying opportunity",
            "Low VIX = low fear, potential selling opportunity",
            "VIX is mean-reverting",
            "Use for market timing",
            "Combine with other indicators"
        ]
    
    @staticmethod
    def get_market_sentiment_tips():
        """Get Market Sentiment trading tips."""
        return [
            "Use multiple sentiment indicators",
            "Extreme sentiment often signals reversal",
            "Combine with technical analysis",
            "Monitor for sentiment shifts",
            "Use for contrarian strategies"
        ]
