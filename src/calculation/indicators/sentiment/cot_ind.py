# -*- coding: utf-8 -*-
# src/calculation/indicators/sentiment/cot_ind.py

"""
INDICATOR INFO:
Name: COT
Category: Sentiment
Description: Commitment of Traders. Shows the net positions of commercial and non-commercial traders.
Usage: --rule cot() or --rule cot(close)
Parameters: price_type
Pros: + Shows institutional sentiment, + Good for commodities, + Contrarian signals
Cons: - Lagging data, - May not work for all assets, - Complex interpretation
File: src/calculation/indicators/sentiment/cot_ind.py

COT (Commitment of Traders) indicator calculation module.
"""

# Implement COT calculation
