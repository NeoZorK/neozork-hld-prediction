# -*- coding: utf-8 -*-
# src/calculation/indicators/oscillators/rsi_mom_ind.py

"""
INDICATOR INFO:
Name: RSI_MOM
Category: Oscillators
Description: RSI Momentum indicator. Focuses on RSI direction changes and momentum to identify trend reversals.
Usage: --rule rsi_mom:14,30,70,close
Parameters: period, oversold_level, overbought_level, price_type
Pros: + Identifies momentum shifts, + Early reversal signals, + Reduces false signals
Cons: - More complex than basic RSI, - Can be noisy in sideways markets

RSI Momentum indicator module.
Implements RSI momentum calculation with focus on direction changes and trend reversals.
All comments and texts in English.
"""

# Import the function from the main RSI calculation file
from .rsi_ind_calc import apply_rule_rsi_momentum as apply_rule_rsi_mom 