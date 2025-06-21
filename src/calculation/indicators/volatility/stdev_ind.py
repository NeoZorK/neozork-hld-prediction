# -*- coding: utf-8 -*-
# src/calculation/indicators/volatility/stdev_ind.py

"""
INDICATOR INFO:
Name: Standard Deviation
Category: Volatility
Description: Standard Deviation. Measures the dispersion of price data from its mean over a specified period.
Usage: --rule stdev(20) or --rule stdev(20,close)
Parameters: period, price_type
Pros: + Measures price dispersion, + Good for volatility analysis, + Simple to understand
Cons: - Doesn't predict direction, - Sensitive to outliers, - Requires sufficient data
File: src/calculation/indicators/volatility/stdev_ind.py

Standard Deviation indicator calculation module.
"""

# Implement Standard Deviation calculation
