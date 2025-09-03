# -*- coding: utf-8 -*-
"""
Trend Trading Tips

This module provides trading tips for trend indicators.
"""


class TrendTips:
    """Trading tips for trend indicators."""
    
    @staticmethod
    def get_ema_tips():
        """Get EMA trading tips."""
        return [
            "Use EMA crossovers to identify trend changes",
            "Shorter EMAs are more responsive to price changes",
            "Longer EMAs provide better trend confirmation",
            "Price above EMA indicates uptrend, below indicates downtrend",
            "Multiple EMAs can show trend strength and momentum"
        ]
    
    @staticmethod
    def get_sma_tips():
        """Get SMA trading tips."""
        return [
            "SMA provides smoother trend lines than EMA",
            "Use SMA for longer-term trend analysis",
            "Price crossing above/below SMA signals trend change",
            "SMA slope indicates trend strength",
            "Combine with volume for confirmation"
        ]
    
    @staticmethod
    def get_adx_tips():
        """Get ADX trading tips."""
        return [
            "ADX above 25 indicates strong trend",
            "ADX below 20 suggests ranging market",
            "Rising ADX confirms trend strength",
            "Falling ADX may signal trend reversal",
            "Use with directional indicators for entry signals"
        ]
    
    @staticmethod
    def get_sar_tips():
        """Get SAR trading tips."""
        return [
            "SAR dots below price indicate uptrend",
            "SAR dots above price indicate downtrend",
            "SAR reversal signals potential trend change",
            "Use for stop-loss placement",
            "Combine with other indicators for confirmation"
        ]
    
    @staticmethod
    def get_supertrend_tips():
        """Get SuperTrend trading tips."""
        return [
            "SuperTrend line below price = uptrend",
            "SuperTrend line above price = downtrend",
            "Line color change signals trend reversal",
            "Use for dynamic stop-loss management",
            "Combine with volume for entry confirmation"
        ]
    
    @staticmethod
    def get_wave_tips():
        """Get Wave analysis tips."""
        return [
            "Identify Elliott Wave patterns for trend direction",
            "Wave 3 is typically the strongest",
            "Use Fibonacci retracements for wave targets",
            "Wave 5 often shows divergence",
            "Combine with momentum indicators for timing"
        ]
