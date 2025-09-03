# -*- coding: utf-8 -*-
"""
Predictive Trading Tips

This module provides trading tips for predictive indicators.
"""


class PredictiveTips:
    """Trading tips for predictive indicators."""
    
    @staticmethod
    def get_hma_tips():
        """Get HMA trading tips."""
        return [
            "HMA is more responsive than traditional moving averages",
            "Use for trend identification and momentum",
            "HMA crossovers provide entry signals",
            "Combine with volume for confirmation",
            "Use for dynamic trend following"
        ]
    
    @staticmethod
    def get_tsforecast_tips():
        """Get Time Series Forecast trading tips."""
        return [
            "TSF provides linear trend projection",
            "Use for price target estimation",
            "Combine with other indicators for confirmation",
            "Use for trend continuation strategies",
            "Monitor for trend changes and reversals"
        ]
    
    @staticmethod
    def get_linear_regression_tips():
        """Get Linear Regression trading tips."""
        return [
            "Linear regression shows trend direction and slope",
            "Use for trend strength analysis",
            "Regression channels show price boundaries",
            "Use for mean reversion strategies",
            "Combine with momentum indicators"
        ]
    
    @staticmethod
    def get_polynomial_regression_tips():
        """Get Polynomial Regression trading tips."""
        return [
            "Polynomial regression captures non-linear trends",
            "Use for complex trend analysis",
            "Higher degree polynomials fit data better",
            "Use for advanced trend modeling",
            "Combine with other technical indicators"
        ]
