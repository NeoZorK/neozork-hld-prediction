# -*- coding: utf-8 -*-
"""
Momentum Trading Tips

This module provides trading tips for momentum indicators.
"""


class MomentumTips:
    """Trading tips for momentum indicators."""
    
    @staticmethod
    def get_macd_tips():
        """Get MACD trading tips."""
        return [
            "MACD line crossing above signal line = bullish signal",
            "MACD line crossing below signal line = bearish signal",
            "Histogram shows momentum strength",
            "Divergence between price and MACD signals reversal",
            "Use zero line crossovers for trend confirmation"
        ]
    
    @staticmethod
    def get_stoch_oscillator_tips():
        """Get Stochastic Oscillator trading tips."""
        return [
            "Stochastic above 80 = overbought, below 20 = oversold",
            "Use %K and %D crossovers for entry signals",
            "Divergence signals potential reversal",
            "Combine with trend indicators for confirmation",
            "Avoid trading in sideways markets"
        ]
    
    @staticmethod
    def get_roc_tips():
        """Get ROC trading tips."""
        return [
            "ROC above zero indicates positive momentum",
            "ROC below zero indicates negative momentum",
            "Rising ROC confirms uptrend strength",
            "Falling ROC confirms downtrend strength",
            "Use for momentum confirmation with other indicators"
        ]
    
    @staticmethod
    def get_momentum_tips():
        """Get Momentum indicator tips."""
        return [
            "Momentum above zero line = bullish momentum",
            "Momentum below zero line = bearish momentum",
            "Rising momentum confirms trend strength",
            "Falling momentum may signal trend weakness",
            "Use for momentum confirmation and divergence"
        ]
