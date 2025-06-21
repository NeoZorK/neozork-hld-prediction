# -*- coding: utf-8 -*-
# src/calculation/indicators/volatility/atr_ind.py

"""
INDICATOR INFO:
Name: ATR
Category: Volatility
Description: Average True Range. Measures market volatility by decomposing the entire range of an asset price.
Usage: --rule atr(14) or --rule atr(14,close)
Parameters: period, price_type
Pros: + Measures true volatility, + Good for stop-loss placement, + Works in any market condition
Cons: - Lagging indicator, - Doesn't predict direction, - Sensitive to period choice
File: src/calculation/indicators/volatility/atr_ind.py

ATR (Average True Range) indicator calculation module.
"""

# Implement ATR calculation
