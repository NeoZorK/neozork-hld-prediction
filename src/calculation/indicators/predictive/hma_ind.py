# -*- coding: utf-8 -*-
# src/calculation/indicators/predictive/hma_ind.py

"""
INDICATOR INFO:
Name: HMA
Category: Predictive
Description: Hull Moving Average. A fast and smooth moving average that reduces lag while maintaining smoothness.
Usage: --rule hma(20) or --rule hma(20,close)
Parameters: period, price_type
Pros: + Reduces lag compared to SMA, + Smooth output, + Good for trend identification
Cons: - More complex calculation, - May be more volatile, - Sensitive to period choice
File: src/calculation/indicators/predictive/hma_ind.py

HMA (Hull Moving Average) indicator calculation module.
"""

# Implement HMA calculation
