# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/wave_ind.py

"""
INDICATOR INFO:
Name: WAVE
Category Trend
Description: Wave  is a sophisticated trend-following indicator that combines multiple momentum calculations
to generate strong trading signals based on open price movements. It utilizes a dual-wave system with configurable
trading rules and global signal filtering.
Usage: --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open
Parameters: period_long1, period_short1, period_trend1, tr1,
 period_long2, period_short2, period_trend2, tr2,
 global_tr, sma_period

 Pros+:
+Dual Signal Validation: Two-wave system for improved reliability
+Flexible Configuration: Multiple trading rules and filters
+Strong Trend Identification: Excellent for trending markets
+Zone-Based Filtering: Helps avoid counter-trend trades
+Momentum Validation: Advanced signal filtering algorithms
+Visual Clarity: Clear color coding and multiple visual elements
+Comprehensive Signal Types: Various signal combinations
+Professional Grade: Sophisticated algorithms for advanced strategies

Cons-:
-Complex Setup: Requires extensive parameter testing
-Lag in Ranging Markets: May be slow in sideways markets
-Parameter Sensitivity: Performance depends heavily on proper settings
-Resource Intensive: Multiple calculations may impact performance
-Learning Curve: Complex rules require significant study time
-Over-Optimization Risk: Multiple parameters increase curve-fitting risk
-Signal Frequency: May generate fewer signals than simpler indicators
-Market Dependency: Best in trending markets, weaker in ranging conditions
This analysis provides traders with a balanced view of the indicator's strengths and limitations, helping them make informed decisions about whether Wave2 fits their trading style and market conditions.
"""
import pandas as pd
from ....common import logger
from ....common import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType