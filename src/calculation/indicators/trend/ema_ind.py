# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/ema_ind.py

"""
INDICATOR INFO:
Name: EMA
Category: Trend
Description: Exponential Moving Average. A type of moving average that gives more weight to recent prices.
Usage: --rule ema(20) or --rule ema(20,close)
Parameters: period, price_type
Pros: + Responds quickly to price changes, + Reduces lag compared to SMA, + Good for trend identification
Cons: - Can be more volatile, - May give false signals in choppy markets, - Sensitive to parameter choice

EMA (Exponential Moving Average) indicator calculation module.
"""

# Implement EMA calculation
