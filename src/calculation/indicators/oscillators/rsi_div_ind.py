# -*- coding: utf-8 -*-
# src/calculation/indicators/oscillators/rsi_div_ind.py

"""
INDICATOR INFO:
Name: RSI_DIV
Category: Oscillators
Description: RSI Divergence indicator. Detects price/RSI divergences to identify potential trend reversals.
Usage: --rule rsi_div:14,30,70,close
Parameters: period, oversold_level, overbought_level, price_type
Pros: + Identifies potential reversals, + Advanced signal quality, + Divergence detection
Cons: - Complex interpretation, - Can miss signals, - Requires experience

RSI Divergence indicator module.
Implements RSI divergence detection to identify potential trend reversals.
All comments and texts in English.
"""

# Import the function from the main RSI calculation file
from .rsi_ind_calc import apply_rule_rsi_divergence as apply_rule_rsi_div 