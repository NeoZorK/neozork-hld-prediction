# -*- coding: utf-8 -*-
"""
Volatility Trading Tips

This module provides trading tips for volatility indicators.
"""


class VolatilityTips:
    """Trading tips for volatility indicators."""
    
    @staticmethod
    def get_atr_tips():
        """Get ATR trading tips."""
        return [
            "High ATR indicates high volatility",
            "Low ATR indicates low volatility",
            "Use ATR for stop-loss placement",
            "ATR expansion signals trend continuation",
            "ATR contraction may signal reversal"
        ]
    
    @staticmethod
    def get_bollinger_bands_tips():
        """Get Bollinger Bands trading tips."""
        return [
            "Price touching upper band = overbought",
            "Price touching lower band = oversold",
            "Bands narrowing = low volatility",
            "Bands widening = high volatility",
            "Use for mean reversion strategies"
        ]
    
    @staticmethod
    def get_stdev_tips():
        """Get Standard Deviation trading tips."""
        return [
            "High standard deviation = high volatility",
            "Low standard deviation = low volatility",
            "Use for risk assessment",
            "Combine with mean for statistical analysis",
            "Use for volatility-based position sizing"
        ]
    
    @staticmethod
    def get_keltner_channels_tips():
        """Get Keltner Channels trading tips."""
        return [
            "Price above upper channel = overbought",
            "Price below lower channel = oversold",
            "Channels based on ATR for volatility",
            "Use for trend following strategies",
            "Combine with volume for confirmation"
        ]
