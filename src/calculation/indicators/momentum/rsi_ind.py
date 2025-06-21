# -*- coding: utf-8 -*-
# src/calculation/indicators/momentum/rsi_ind.py

"""
INDICATOR INFO:
Name: RSI
Category: Momentum
Description: Relative Strength Index. Measures the speed and magnitude of price changes to identify overbought/oversold conditions.
Usage: --rule rsi(14,70,30,open) or --rule rsi(14,70,30,close)
Parameters: period, overbought_level, oversold_level, price_type
Pros: + Identifies overbought/oversold conditions, + Simple to interpret, + Widely used
Cons: - Can give false signals in trending markets, - Lagging indicator
File: src/calculation/indicators/momentum/rsi_ind.py

RSI (Relative Strength Index) indicator calculation module for momentum analysis.
"""

# Implement RSI calculation for momentum
