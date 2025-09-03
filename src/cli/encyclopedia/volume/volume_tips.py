# -*- coding: utf-8 -*-
"""
Volume Trading Tips

This module provides trading tips for volume indicators.
"""


class VolumeTips:
    """Trading tips for volume indicators."""
    
    @staticmethod
    def get_obv_tips():
        """Get OBV trading tips."""
        return [
            "OBV should confirm price movement direction",
            "Divergence between OBV and price signals reversal",
            "Rising OBV confirms uptrend strength",
            "Falling OBV confirms downtrend strength",
            "Use for volume confirmation with price action"
        ]
    
    @staticmethod
    def get_vwap_tips():
        """Get VWAP trading tips."""
        return [
            "Price above VWAP = bullish, below = bearish",
            "Use VWAP as dynamic support/resistance",
            "VWAP resets daily for intraday trading",
            "Combine with volume for confirmation",
            "Use for institutional trading patterns"
        ]
    
    @staticmethod
    def get_volume_sma_tips():
        """Get Volume SMA trading tips."""
        return [
            "Volume above SMA indicates high activity",
            "Volume below SMA indicates low activity",
            "Use for volume trend analysis",
            "Combine with price indicators for confirmation",
            "High volume confirms price movements"
        ]
    
    @staticmethod
    def get_volume_ema_tips():
        """Get Volume EMA trading tips."""
        return [
            "Volume EMA is more responsive than SMA",
            "Use for short-term volume trend analysis",
            "Volume EMA crossovers signal activity changes",
            "Combine with price EMA for confirmation",
            "Use for momentum confirmation"
        ]
