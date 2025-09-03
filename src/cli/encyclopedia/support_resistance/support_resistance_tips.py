# -*- coding: utf-8 -*-
"""
Support/Resistance Trading Tips

This module provides trading tips for support/resistance indicators.
"""


class SupportResistanceTips:
    """Trading tips for support/resistance indicators."""
    
    @staticmethod
    def get_pivot_points_tips():
        """Get Pivot Points trading tips."""
        return [
            "Pivot point acts as central support/resistance",
            "R1, R2, R3 are resistance levels",
            "S1, S2, S3 are support levels",
            "Use for intraday trading levels",
            "Combine with other indicators for confirmation"
        ]
    
    @staticmethod
    def get_fibonacci_retracement_tips():
        """Get Fibonacci Retracement trading tips."""
        return [
            "Use 23.6%, 38.2%, 50%, 61.8% retracement levels",
            "61.8% is often the maximum retracement",
            "Use for entry and exit points",
            "Combine with trend analysis",
            "Fibonacci levels work best in trending markets"
        ]
    
    @staticmethod
    def get_donchian_channels_tips():
        """Get Donchian Channels trading tips."""
        return [
            "Upper channel = highest high of period",
            "Lower channel = lowest low of period",
            "Middle line = average of upper and lower",
            "Use for breakout strategies",
            "Channels show price range and volatility"
        ]
    
    @staticmethod
    def get_support_resistance_levels_tips():
        """Get Support/Resistance Levels trading tips."""
        return [
            "Support = price floor, resistance = price ceiling",
            "Levels become stronger with more touches",
            "Breakout above resistance = bullish signal",
            "Breakdown below support = bearish signal",
            "Use for stop-loss and take-profit placement"
        ]
