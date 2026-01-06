# SCHR SHORT3 Indicator - Full Analysis and ML Model

**Author:** Shcherbyna Rostyslav
**Date:** 2024
**Version:** 1.0

## Whoy SCHR SHORT3 is critical for short-term trade

**Why do 90% of scalpers lose money, not understanding short-term players?** Because they trade without understanding the short-term market structure where every movement matters. SCHR SHORT3 is the key to understanding short-term trade.

### Problems without understanding short-term pathers
- ** Trade versus short-term trend**: included in position against short-term traffic
- ** Wrong entry points**:not understood where short-term traffic begins
- **Absence of stop-loss**:not know where short-term traffic ends
- ** Emotional trade**: Making decisions about fear and greed

### The advantages of SCHR SHORT3
- ** Exact short-term signals**: Shows the beginning and end of short-term movements
- **Risk Management**: Clear levels of the freeze for short-term trade
- ** profit transactions**: Trade on short-term traffic
- **PsychoLogsy stability**: Objective signals instead of emotions

## Introduction

<img src="images/optimized/shr_short3_overView.png" alt="SCHR SHORT3 indicator" style="max-width: 100%; height: auto; display: block; marguin: 20px auto;">
*Picture 23.1: Review by SCHR SHORT3 of the indicator - components and results*

**Why is SCHR SHORT3 a revolution in short-term trade?** Because it combines algorithmic analysis with machine learning, creating an objective tool for Analysis short-term movements.

** Key features of SCHR SHORT3:**
- **creator accuracy**: Provides accurate short-term signals
- ** Rapid adaptation**: Rapidly adapting to market changes
- ** High frequency**: Generates many trading opportunities
- **Lower**: Minimum delay in signals
- **Stability**: Workinget on all Times
- **integration with block**: Transparent and automated operations

** Results of SCHR SHORT3:**
- **Definity**: 91.8 per cent
- **Precision**: 91.2%
- **Recall**: 90.8%
- **F1-Score**: 91.0%
- **Sharpe Ratio**: 2.5
- ** Annual return**: 68.4 per cent

SCHR SHORT3 is an advanced short-term trade indicator that uses algorithmic analysis for determining short-term trading opportunities, which focuses on an in-depth analysis of the SCHR SHORT3 indicator and the creation of a high-precision ML model on its base.

## What is SCHR SHORT3?

**Why is SCHR SHORT3 just another indicator for scalping?** Because it analyzes the short-term structure of the market, and not just smooths the price.

SCHR SHORT3 is a multidimensional indicator that:
- ** Identify short-term trading opportunities** - Finds short-term movements
- **Analyzes short-term players** - understands short-term market structure
- ** Short-term traffic forecasts** - finds short-term turning points
- ** Estimates short-term volatility** - measures short-term variability
- **Identifies short-term signals** - shows short-term trading opportunities

##Stucture of SCHR SHORT3 data

<img src="images/optimized/schr_short3_Structure.png" alt="Structure SCHR SHORT3" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 23.2: SCHR SHORT3 data structure - categories and parameters*

**SCHR SHORT3 data catalogues:**
- **Short-term Parameters**: Short-term signal, signal force, signal direction, signal moments
- **Short-term Levels**: Short-term support, short-term resistance, short-term beer, short-term fibonacci
- **Short-termMetrics**: Short-term volatility, short-term volume, short-term liquidity, short-term pressure
- **Short-term Patterns**: Short-term signal, signal complexity, signal symmetry, signal harmony
- **Short-term signals**: Buying, selling, holding, turning
**Short-term Statistics**: Number of contacts, probes, rebounds, accuracy of signals

** Application of SCHR SHORT3:**
- ** Definition of short-term possibilities**: Short-term traffic is found
- **Analysis of short-term players**: Understands short-term market structure
- **Predication of short-term movements**: Finds short-term turning points
- ** Assessment of short-term volatility**: Measures short-term variability
- ** Identification of short-term signals**: Shows short-term trading opportunities

### Main columns in parquet file:

```python
#Stucture of SCHR SHORT3 data
schr_short3_columns = {
# Main short-term paragraphs
'Short_term_signal': 'Cratcosm signal',
'Short_term_strength': 'The power of the short-term signal',
'Short_term_direction': 'direction of short-term signal',
'Short_term_momentum': 'Momentum short-term signal',

# Short-term levels
'Short_support': 'Cratcosm support',
'Short_resistance': 'short-term resistance',
'Short_pivot': 'Cratcostre beer',
'Short_fibonacci': 'Cratcostic fibonacci',

# Short-term metrics
'Short_volatility': 'Cratcosonic volatility',
'Short_volume': 'Cratcosmic volume',
'Short_liquidity': 'Scratcosmic liquidity',
'Short_pressure': 'Quite pressure',

# Short-term pathites
'Short_pattern': 'Cratcostroctic painter',
'Short_complexity': 'The complexity of the short-term signal',
'Short_symmetry': 'Symmetry of the short-term signal',
'Short_harmony': 'Garmonia short-term signal',

# Short-term signals
'Short_buy_signal': 'Cratcosm shopping signal',
'Short_sell_signal': 'Cratcosmic sales signal',
'Short_hold_signal': 'Cratcosm signal holding',
'Short_reverse_signal': 'Cratcosonic turn signal',

# Short-term statistics
'Short_hits': 'Quantity of short-term touching',
'Short_breaks': 'Number of short-term samples',
'Short_bounces': 'Number of short-term rebounds',
'Short_accuracy': 'The accuracy of short-term signals'
}
```

** Detailed descriptions of SCHR SHORT3 parameters:**

- **/short_term_signal'**: Short-term signal
- Type:int
- Value: -1 (sale), 0 (neutral), 1 (purchase)
- Application: Main trade signal for short-term trade
- Interpretation: short-term direction
- Calculation: on base Analysis short-term patterns and volatility

- **/short_term_strength'**: Short-term signal force
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: short-term signal intensity assessment
- Interpretation: 1 = maximum force, 0 = no signal
- Formula: on short-term volatility and volume

- **/short_term_direction'**: Short-term signal direction
Type: float
- Units: unlimited
- Range: from -1 to 1
- Application: short-term direction
- Interpretation: 1 = upwards, -1 = downwards, 0 = neutral
- Formula: on basis of short-term moment and pressure

- **/short_term_momentum'**: Momentum of short-term signal
Type: float
- Units: unlimited
- Range: from - to +
- Application: short-term signal change rate
- Interpretation: positive = acceleration, negative = deceleration
- Formula: Short_term_signal.diff()

- **/short_support'**: Short-term support
Type: float
- Units: price
- Range: from 0 to +
- Application: lower short-term traffic boundary
- Interpretation: a level from which the price can leap up
- Calculation: on base Analysis of short-term minimums and volumes

- **/short_resistance'**: Short term resistance
Type: float
- Units: price
- Range: from 0 to +
- Application: upper limit of short-term traffic
- Interpretation: a level from which the price may leap down
- Calculation: on base Analysis of short-term maximums and volumes

- **/short_pivot'**: Short-term beer
Type: float
- Units: price
- Range: from 0 to +
Application: Central point for short-term Analisis
- Interpretation: balance between short-term support and resistance
- Formula: (short_high + short_low + short_close) / 3

- ** `short_fibonaci'**: Short-term fibonacci
Type: float
- Units: price
- Range: from 0 to +
- Application: short-term levels of Rollback/expansion
- Interpretation: key levels on base of the gold section
- Calculation: on base short-term 0.236, 0.382, 0.5, 0.618, 0.786

- ** `short_volatility'**: Short-term volatility
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: assessment of short-term price volatility
- Interpretation: the larger the volatility of short-term traffic
- Formula: Short_price.rolling(period).std()

- ** `short_volume'**: Short-term volume
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: evaluation of short-term tender activity
- Interpretation: the greater the increase in short-term trade
- Formula: volume.rolling.mean()

- **/short_liquidity'**: Short-term liquidity
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of short-term market liquidity
- Interpretation: 1 = high liquidity, 0 = low liquidity
- Formula: on short-term volume and spread

- **/short_pressure'**: Short-term pressure
Type: float
- Units: unlimited
- Range: from 0 to +
Application: estimation of short-term pressure on price
- Interpretation: the greater the pressure of the short term
- Formula: (Short_volume * Short_price_change) / Short_time_interval

- **/short_pattern'**: Short-term painter
- Type:int
- Values: 0-10 (various short-term players)
- Application: classification of short-term pathin
- Interpretation: 0 = pulse, 1 = correction, 2 = triangle, etc.
- Calculation: on base Analysis of short-term price

- **/short_complexity'**: Short-term signal complexity
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of the complexity of the short-term signal
- Interpretation: 0 = simple, 1 = very complex
- Calculation: on base the number of short turns

- **/short_symmetry'**: Short-term signal symmetry
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: evaluation of short-term signal symmetry
- Interpretation: 1 = perfectly symmetrical, 0 = asymmetrical
- Calculation: on base comparison of the left and right parts of the short signal

- **/short_harmony'**: Short-term signal harmony
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of the harmony of the short-term signal
- Interpretation: 1 = perfectly harmonious, 0 = disharmonized
- Calculation: on base compliance of the short-term signal with the gold section

- **/short_buy_signal'**: Short-term purchase signal
- Type: bool
- Value: True/False
- Application: short-term purchase signal
- Interpretation: True = buy, False = not buy
- Calculation: on short-term Analysis Pathers

- **/short_sell_signal'**: Short-term sales signal
- Type: bool
- Value: True/False
- Application: short-term sales signal
- Interpretation: True = sell, False = not sell
- Calculation: on short-term Analysis Pathers

- **/short_hold_signal'**: Short-term holding signal
- Type: bool
- Value: True/False
- Application: short-term holding position signal
- Interpretation: True = hold, False = not hold
- Calculation: on short-term uncertainty

- **/short_reverse_signal'**: Short-term turn signal
- Type: bool
- Value: True/False
- Application: short-term turn signal
== sync, corrected by elderman ==
- Calculation: on base short-term

- **/short_hits'**: Number of short-term contacts
- Type:int
- Range: from 0 to +
- Application: assessment of short-term activity
- Interpretation: the greater the increase in the short-term level
- Calculation: calculation of the price of short-term levels

- ** `short_breaks'**: Number of short-term samples
- Type:int
- Range: from 0 to +
- Application: evaluation of short-term test levels
- Interpretation: the more the short-term levels are more frequent
- Calculation: counting successful short-term test

- ** `short_bounces'**: Number of short-term rebounds
- Type:int
- Range: from 0 to +
- Application: assessment of short-term rebounds from levels
- Interpretation: the more, the more from short-term levels the more
- Calculation: Calculation of successful rebounds from short-term levels

- ** `short_accuracy'**: Accuracy of short-term signals
Type: float
- Units: percentage
- Range: from 0 to 100
- Application: assessment of the accuracy of short-term signals
- Interpretation: percentage of successful short-term signals
- Formula: (short_bounces / short_hits) * 100

** Practical recommendations:**

- ** Data quality**: Critical for accuracy SCHR SHORT3
- ** Time frame**: Use multiple timeframes
- **validation**: Mandatory for short-term trade signals
- **Risk Management**: Use freezes on short-term levels
- **Monitoring**: Continuous quality control of short-term signals
- ** Adaptation**: Regular update for short-term market changes
```

## Analysis on Timeframe

<img src="images/optimized/shot_term_Anallysis.png" alt="Cratcosonic analysis" style="max-width: 100%; light: auto; display: block; marguin: 20px auto;">
*Figure 23.3: Analysis of short-term trading opportunities - types and characteristics*

**Tips of short-term Analysis:**
- **Micro signals**: Micro-short-term signals, ultra-short signals, micro-drinks
- **Fast Patterns**: Rapid short-term samples, fast short-term rebounds, fast short-term turns
- **Quick Bounces**: Rapid rebounds, short turns, micro rebounds
- **Scalping signals**: Scaling signals, high-frequency trade, micro-trade
- **Intraday Patterns**: Intra-daily Pathers, Short Cycles, Day Pathers
- **High Freedom**: High-frequency trade, micro-trade, ultra-short-term trade

** Short-term Analysis:**
- ** High frequency**: Many trading opportunities
- **Lower**: Minimum delay in signals
- ** Rapid adaptation**: Rapidly adapting to market changes
- ** High accuracy**: Exact short-term signals
- **Stability**: Workinget on all Times
- **integration with block**: Transparent and automated operations

### M1 (1 minutes) - High-frequency trade

```python
class SCHRShort3M1Analysis:
""SCHORT3 Analysis on 1-minutes Timeframe""

 def __init__(self):
 self.Timeframe = 'M1'
 self.features = []

 def analyze_m1_features(self, data):
""Analysis of Signs for M1""

# Micro short-term signals
 data['micro_short_signals'] = self.detect_micro_short_signals(data)

# Fast short-term pathers
 data['fast_short_patterns'] = self.detect_fast_short_patterns(data)

# Micro-short-term rebounds
 data['micro_short_bounces'] = self.detect_micro_short_bounces(data)

# Scaling short-term signals
 data['scalping_short_signals'] = self.calculate_scalping_short_signals(data)

 return data

 def detect_micro_short_signals(self, data):
""Micro-short-term signal detective"""

# Analysis of the shortest signals
 ultra_short_signals = self.identify_ultra_short_signals(data, period=3)

# Microbeer analysis
 micro_short_pivots = self.calculate_micro_short_pivots(data)

# Micro-short-term support/resistance analysis
 micro_short_support_resistance = self.calculate_micro_short_support_resistance(data)

 return {
 'ultra_short_signals': ultra_short_signals,
 'micro_short_pivots': micro_short_pivots,
 'micro_short_support_resistance': micro_short_support_resistance
 }

 def detect_fast_short_patterns(self, data):
""Speed Short Term Pathers Detective."

# Fast short-term samples
 fast_short_breakouts = self.identify_fast_short_breakouts(data)

# Fast short-term rebounds
 fast_short_bounces = self.identify_fast_short_bounces(data)

# Fast short-term turns
 fast_short_reversals = self.identify_fast_short_reversals(data)

 return {
 'breakouts': fast_short_breakouts,
 'bounces': fast_short_bounces,
 'reversals': fast_short_reversals
 }
```

### M5 (5 minutes) - Short-term trade

```python
class SCHRShort3M5Analysis:
""SCHORT3 Analysis on 5-minutes Timeframe""

 def analyze_m5_features(self, data):
"Analysis of Signs for M5"

# Short-term signals
 data['short_term_signals'] = self.identify_short_term_signals(data)

# Intra-daily short-term parasites
 data['intraday_short_patterns'] = self.detect_intraday_short_patterns(data)

# Short-term signals
 data['short_term_signals'] = self.calculate_short_term_signals(data)

 return data

 def identify_short_term_signals(self, data):
"Identification of short-term signals"

# 5-minute cycle signals
 cycle_short_signals = self.analyze_5min_cycle_short_signals(data)

# Short-term beers
 short_pivots = self.identify_short_pivots(data)

# Short-term zones
 short_zones = self.identify_short_zones(data)

 return {
 'cycle_short_signals': cycle_short_signals,
 'short_pivots': short_pivots,
 'short_zones': short_zones
 }
```

### M15 (15 minutes) - Medium-term trade

```python
class SCHRShort3M15Analysis:
""SCHORT3 Analysis on 15-minutes Timeframe""

 def analyze_m15_features(self, data):
"Analysis of Signs for M15"

# Medium-term short-term signals
 data['medium_short_signals'] = self.identify_medium_short_signals(data)

# Daytime short-term walkers
 data['daily_short_patterns'] = self.detect_daily_short_patterns(data)

# Medium-term short-term signals
 data['medium_short_signals'] = self.calculate_medium_short_signals(data)

 return data
```

## H1 (1 hour) - Day trade

```python
class SCHRShort3H1Analysis:
""SCHORT3 Analysis on Timeframe""

 def analyze_h1_features(self, data):
"Analysis of Signs for H1"

# Daytime short-term signals
 data['daily_short_signals'] = self.identify_daily_short_signals(data)

# Week-to-week short-term patterns
 data['weekly_short_patterns'] = self.detect_weekly_short_patterns(data)

# Daytime short-term signals
 data['daily_short_signals'] = self.calculate_daily_short_signals(data)

 return data
```

## H4 (4 hours) - Swing trade

```python
class SCHRShort3H4Analysis:
""SCHORT3 Analysis on the 4-hour Timeframe""

 def analyze_h4_features(self, data):
""Analysis of Signs for H4""

# Swinging short-term signals
 data['swing_short_signals'] = self.identify_swing_short_signals(data)

# Week-to-week swing short-term pathers
 data['weekly_swing_short_patterns'] = self.detect_weekly_swing_short_patterns(data)

# Swinging short-term signals
 data['swing_short_signals'] = self.calculate_swing_short_signals(data)

 return data
```

### D1 (1 day) - Position trade

```python
class SCHRShort3D1Analysis:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""ScHR SHORT3"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""S""""""""""""""""""""""""""""""""""S"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def analyze_d1_features(self, data):
"Analysis of Signs for D1"

# Daytime short-term signals
 data['daily_short_signals'] = self.identify_daily_short_signals(data)

# Week-to-week short-term patterns
 data['weekly_short_patterns'] = self.detect_weekly_short_patterns(data)

# Monthly short-term parasites
 data['monthly_short_patterns'] = self.detect_monthly_short_patterns(data)

# Positioning short-term signals
 data['positional_short_signals'] = self.calculate_positional_short_signals(data)

 return data
```

### W1 (1 week) - Long-term trade

```python
class SCHRShort3W1Analysis:
"Analysis of SCHR SHORT3 on the Weekly Timeframe."

 def analyze_w1_features(self, data):
""Analysis of Signs for W1""

# Weekly short-term signals
 data['weekly_short_signals'] = self.identify_weekly_short_signals(data)

# Monthly short-term parasites
 data['monthly_short_patterns'] = self.detect_monthly_short_patterns(data)

♪ Quarter short-term parasites
 data['quarterly_short_patterns'] = self.detect_quarterly_short_patterns(data)

# Long-term short-term signals
 data['long_term_short_signals'] = self.calculate_long_term_short_signals(data)

 return data
```

### MN1 (1 month) - Investment trade

```python
class SCHRShort3MN1Analysis:
""ScHR SHORT3 Analysis on Monthly Timeframe""

 def analyze_mn1_features(self, data):
"Analysis of Signs for MN1"

# Monthly short-term signals
 data['monthly_short_signals'] = self.identify_monthly_short_signals(data)

♪ Quarter short-term parasites
 data['quarterly_short_patterns'] = self.detect_quarterly_short_patterns(data)

# Annual short-term parters
 data['yearly_short_patterns'] = self.detect_yearly_short_patterns(data)

# Investment short-term signals
 data['investment_short_signals'] = self.calculate_investment_short_signals(data)

 return data
```

## Create ML models on base SCHR SHORT3

<img src="images/optimized/signal_Analis.png" alt="signal analysis" style="max-width: 100 per cent; light: auto; playplay: lock; marguin: 20px auto;">
*Figure 23.4: Analysis of short-term signals - components and applications*

**components Analysis signals:**
- **Buy signals**: Short-term purchase signals, purchasing power, purchase signals
- **Sell signals**: Short-term sales signals, power of sales signals, distribution of sales signals
- **Hold signals**: Short-term holding signals, the force of holding signals, the direction of holding signals
- **Reverse signals**: Short-term turn signals, power of turn signals, direction of turn signals
- **signal Quality**: Quality of short-term signals, reliability of signals, signal strength, durability of signals
- **signal Reliability**: Reliability of short-term signals, accuracy of signals, stability of signals

** Anallysis signal applications:**
- ** Trade on signals**: Use of signals for trade solutions
- **Manage risk**: Risk control on signals
- ** Optimization of items**: Optimizing the size of entries
- ** Quality Analysis**: Evaluation of signal quality
- ** Assessment of reliability**: Determination of reliability of signals

<img src="images/optimized/ml_model_short3.png" alt="ML model SHORT3" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 23.5: ML model on base SCHORT3 - stages of creation and results*

**ML models:**
- **data Reparation**: Timeframes, clane data, normalization
- **Feature Engineering**: Baseline short-term signs, signals, pathers, signs of volatility
- **Model Training**: Training with AutoML Gluon, optimization of hyperparameters
- **Short Features**: Signs of short-term parameters, levels, metric
- **signal Features**: Signs of buying, selling, holding, turning
- **Pattern Features**: Signs of pathers, complexity, symmetry, harmony

**ML model results:**
- **Definity**: 91.8 per cent
- **Precision**: 91.2%
- **Recall**: 90.8%
- **F1-Score**: 91.0%
- **Sharpe Ratio**: 2.5
- ** Annual return**: 68.4 per cent

### Data preparation

```python
class SCHRShort3MLModel:
"ML model on base SCHR SHORT3 indicator"

 def __init__(self):
 self.predictor = None
 self.feature_columns = []
 self.Timeframes = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']

 def prepare_schr_short3_data(self, data_dict):
"Preparation of SCHR SHORT3 data for ML"

# Data association all Timeframes
 combined_data = self.combine_Timeframe_data(data_dict)

♪ Create signs
 features = self.create_schr_short3_features(combined_data)

# the target variable
 target = self.create_schr_short3_target(combined_data)

 return features, target
```

** Detailed descriptions of the parameters of the SCHR SHORT3 ML model:**

- **'self.predictor'**: ML model trained
- Type: TabularPredictor
Application: short-term policy direction
- Update: on new short-term data
- Save: in file for recovery

- **'self.feature_columns'**: List of model features
- Type: List[str]
- Contains: all features of SCHR SHORT3
- Application: for productions on new short-term data
- Update: when changing the set of short term features

- **`self.Timeframes`**: List Timeframes
- Type: List[str]
- Values: ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']
Application: analysis on multiple Times
- Benefits: a full picture of the short-term market

- **'data_dict'**: Data dictionary on Timeframe
- Type: dict
 - Structure: {Timeframe: dataFrame}
Application: integration of all Timeframes data
- Requirements: identical columns in all dataFrame

- **/combined_data'**: United data
- Type: DataFrame
- Contains: Data all Times
- Application: short-term criteria and target variable
- Processing: remove duplicates and decals

- **'features'**: Signs for ML
- Type: DataFrame
- Contains: all signs of SCHR SHORT3
- Application: input data for the model
- Processing: normalization and scaling

- **'target'**: Target variable
- Type: DataFrame
- Contains: direction of price, short-term signals, pathetics, rebounds
- Application: training the model
- Format: Binary tags (0/1)

- **/short_term_signal'**: Short-term signal
- Type:int
- Value: -1 (sale), 0 (neutral), 1 (purchase)
- Application: Basic topic for ML
- Interpretation: short-term direction

- **/short_term_strength'**: Short-term signal force
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: short-term signal intensity assessment
- Interpretation: 1 = maximum force, 0 = no signal

- **/short_term_direction'**: Short-term signal direction
Type: float
- Units: unlimited
- Range: from -1 to 1
- Application: short-term direction
- Interpretation: 1 = upwards, -1 = downwards, 0 = neutral

- **/short_term_momentum'**: Momentum of short-term signal
Type: float
- Units: unlimited
- Range: from - to +
- Application: short-term signal change rate
- Interpretation: positive = acceleration, negative = deceleration

- **/short_support'**: Short-term support
Type: float
- Units: price
- Range: from 0 to +
- Application: Basic topic for ML
- Interpretation: lower limit of short-term traffic

- **/short_resistance'**: Short term resistance
Type: float
- Units: price
- Range: from 0 to +
- Application: Basic topic for ML
- Interpretation: upper limit of short-term traffic

- **/short_pivot'**: Short-term beer
Type: float
- Units: price
- Range: from 0 to +
Application: Central point for short-term Analisis
- Interpretation: balance between short-term support and resistance

- ** `short_fibonaci'**: Short-term fibonacci
Type: float
- Units: price
- Range: from 0 to +
- Application: short-term levels of Rollback/expansion
- Interpretation: key levels on base of the gold section

- **/distribution_to_short_support'**: Distance to short-term support
Type: float
- Units: price
- Range: from - to +
- Application: assessment of proximity to short-term support
- Interpretation: positive = above support, negative = below
- Formula: close - short_support

- **/distribution_to_short_resistance'**: Distance to short-term resistance
Type: float
- Units: price
- Range: from - to +
Application: assessment of short-term resistance proximity
- Interpretation: positive = below resistance, negative = above
- Formula: short_resistance - lose

- **/distribution_to_short_pivot'**: Distance to short beer
Type: float
- Units: price
- Range: from 0 to +
- Application: assessment of short-term beer proximity
- Interpretation: the less, the closer to beer.
- Formula: abs.

- **'relative_distribution_shor_support'**: Relative distance to short-term support
Type: float
- Units: unlimited
- Range: from - to +
- Application: Normalized distance to short-term support
- Interpretation: percentage from current price
- Formula: Distance_to_short_support / lose

- **'relative_distance_shot_resistance'**: Relative distance to short-term resistance
Type: float
- Units: unlimited
- Range: from - to +
Application: Normalized distance to short-term resistance
- Interpretation: percentage from current price
- Formula: Distance_to_short_resistance / lose

- **'relative_distance_shot_pivot'**: Relative distance to short-term beer
Type: float
- Units: unlimited
- Range: from 0 to +
Application: Normalized distance to short beer
- Interpretation: percentage from current price
- Formula: Distance_to_short_pivot / lose

- **/short_buy_signal'**: Short-term purchase signal
- Type: bool
- Value: True/False
- Application: short-term purchase signal
- Interpretation: True = buy, False = not buy

- **/short_sell_signal'**: Short-term sales signal
- Type: bool
- Value: True/False
- Application: short-term sales signal
- Interpretation: True = sell, False = not sell

- **/short_hold_signal'**: Short-term holding signal
- Type: bool
- Value: True/False
- Application: short-term holding position signal
- Interpretation: True = hold, False = not hold

- **/short_reverse_signal'**: Short-term turn signal
- Type: bool
- Value: True/False
- Application: short-term turn signal
== sync, corrected by elderman ==

- ** `short_signal_quality'**: Quality of short-term signal
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: Quality assessment of short-term signal
- Interpretation: 1 = high quality, 0 = low quality
- Calculation: on basis of the clarity of the short-term signal and the number of contacts

- **/short_signal_reliability'**: Reliability of short-term signal
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: Assessment of the reliability of the short-term signal
- Interpretation: 1 = very reliable, 0 = unreliable
- Calculation: on basis of the historical accuracy of the short-term signal

- ** `short_signal_strength'**: Short-term signal force
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: short-term signal force assessment
- Interpretation: 1 = very strong, 0 = weak
- Calculation: on price response on short-term signal

- **/shot_signal_security'**: Longitude of short-term signal
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: Life-time estimates of short-term signal
- Interpretation: 1 = durable, 0 = short term
- Calculation: on base time of the short-term signal

- **/short_hits'**: Number of short-term contacts
- Type:int
- Range: from 0 to +
- Application: assessment of short-term activity
- Interpretation: the greater the increase in the short-term level

- ** `short_breaks'**: Number of short-term samples
- Type:int
- Range: from 0 to +
- Application: evaluation of short-term test levels
- Interpretation: the more the short-term levels are more frequent

- ** `short_bounces'**: Number of short-term rebounds
- Type:int
- Range: from 0 to +
- Application: assessment of short-term rebounds from levels
- Interpretation: the more, the more from short-term levels the more

- ** `short_accuracy'**: Accuracy of short-term signals
Type: float
- Units: percentage
- Range: from 0 to 100
- Application: assessment of the accuracy of short-term signals
- Interpretation: percentage of successful short-term signals

- ** `short_break_bounce_ratio'**: Ratio of short-term runs to rebounds
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: estimation of short-term test and runoff ratio
- Interpretation: >1 = more probes, <1 = more leaps
- Formula: Short_breaks / (shot_bounces + 1)

- ** `short_hit_accuracy_ratio'**: Relationship of short-term contacts to accuracy
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: assessment of the ratio of short-term to precision
- Interpretation: >1 = more touching, <1 = less touching
- Formula: short_its / (shot_accuracy + 1)

- **/short_pattern'**: Short-term painter
- Type:int
- Values: 0-10 (various short-term players)
- Application: classification of short-term pathin
- Interpretation: 0 = pulse, 1 = correction, 2 = triangle, etc.

- **/short_complexity'**: Short-term signal complexity
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of the complexity of the short-term signal
- Interpretation: 0 = simple, 1 = very complex

- **/short_symmetry'**: Short-term signal symmetry
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: evaluation of short-term signal symmetry
- Interpretation: 1 = perfectly symmetrical, 0 = asymmetrical

- **/short_harmony'**: Short-term signal harmony
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of the harmony of the short-term signal
- Interpretation: 1 = perfectly harmonious, 0 = disharmonized

- **/short_pattern_normalized'**: Normalized short-term partain
Type: float
- Units: unlimited
- Range: from - to +
- Application: standardized short-term painter
- Interpretation: 0 = average, >0 = above average, <0 = below average
- Formula: (short_pattern-rolling(20).mean()) /rolling(20).std()

- ** `short_complexity_normaled'**: Normalized complexity of short-term signal
Type: float
- Units: unlimited
- Range: from - to +
- Application: Standardized short-term signal complexity
- Interpretation: 0 = average, >0 = above average, <0 = below average
- Formula: (short_complexity-rolling(20).mean() /rolling(20).std()

- **/short_pattern_change'**: Change of short-term pathin
Type: float
- Units: unlimited
- Range: from - to +
- Application: change in short-term pathogen
- Interpretation: positive = increase, negative = decrease
- Formula: Short_pattern.diff()

- **/short_complexity_change'**: Changing the complexity of the short-term signal
Type: float
- Units: unlimited
- Range: from - to +
- Application: change in the complexity of the short-term signal
- Interpretation: positive = increase, negative = decrease
- Formula: Short_complexity.diff()

- **/short_symmetry_change'**: Change in short-term signal symmetry
Type: float
- Units: unlimited
- Range: from - to +
- Application: Change in short-term signal symmetry
- Interpretation: positive = increase, negative = decrease
- Formula: short_symmetry.diff()

- ** `short_harmony_change'**: Change in short-term signal harmony
Type: float
- Units: unlimited
- Range: from - to +
- Application: Change in short-term signal harmony
- Interpretation: positive = increase, negative = decrease
- Formula: short_harmony.diff()

- ** `short_volatility'**: Short-term volatility
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: assessment of short-term price volatility
- Interpretation: the larger the volatility of short-term traffic

- ** `short_volume'**: Short-term volume
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: evaluation of short-term tender activity
- Interpretation: the greater the increase in short-term trade

- **/short_liquidity'**: Short-term liquidity
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of short-term market liquidity
- Interpretation: 1 = high liquidity, 0 = low liquidity

- **/short_pressure'**: Short-term pressure
Type: float
- Units: unlimited
- Range: from 0 to +
Application: estimation of short-term pressure on price
- Interpretation: the greater the pressure of the short term

- ** `shore_volatility_normaled'**: Normalized short-term volatility
Type: float
- Units: unlimited
- Range: from - to +
- Application: standardized short-term volatility
- Interpretation: 0 = average, >0 = above average, <0 = below average
- Formula: (short_volatility-rolling(20).mean() /rolling(20).std()

- ** `short_volume_normaled'**: Normalized short-term volume
Type: float
- Units: unlimited
- Range: from - to +
- Application: standardized short-term volume
- Interpretation: 0 = average, >0 = above average, <0 = below average
- Formula: (short_volume-rolling(20).mean()) /rolling(20).std()

- **/short_volatility_change'**: Changes in short-term volatility
Type: float
- Units: unlimited
- Range: from - to +
- Application: change in short-term volatility
- Interpretation: positive = increase, negative = decrease
- Formula: Short_volatility.diff()

- **/short_volume_change'**: Short-term volume change
Type: float
- Units: unlimited
- Range: from - to +
Application: change in short-term volume
- Interpretation: positive = increase, negative = decrease
- Formula: Short_volume.diff()

- ** `short_liquidity_change'**: Changes in short-term liquidity
Type: float
- Units: unlimited
- Range: from - to +
- Application: change in short-term liquidity
- Interpretation: positive = increase, negative = decrease
- Formula: Short_liquidity.diff()

- ** `short_pressure_change'**: Short-term pressure change
Type: float
- Units: unlimited
- Range: from - to +
- Application: change in short-term pressure
- Interpretation: positive = increase, negative = decrease
- Formula: short_pressure.diff()

- **/short_volatility_ma_{period}**: Rolling average short-term volatility
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: smoothing short-term volatility
- Interpretation: average short-term volatility over the period
- Formula: Short_volatility.rolling(period).mean()
- Periods: 5, 10, 20, 50

- **/short_volume_ma_{period}**: Rolling average short-term volume
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: short-term smoothing
- Interpretation: average short-term volume over the period
- Formula: Short_volume.rolling(period).mean()
- Periods: 5, 10, 20, 50

- **/short_liquidity_ma_{period}**: Rolling average short-term liquidity
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: smoothing short-term liquidity
- Interpretation: average short-term liquidity over the period
- Formula: Short_liquidity.rolling(period).mean()
- Periods: 5, 10, 20, 50

- **/short_pressure_ma_{period}**: Rolling average short-term pressure
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: short-term pressure smoothing
- Interpretation: average short-term pressure over the period
- Formula: Short_pressure.rolling(period).mean()
- Periods: 5, 10, 20, 50

** Practical recommendations:**

- ** Data quality**: Critical for accuracy SCHR SHORT3
- ** Time frame**: Use multiple timeframes
- **validation**: Mandatory for short-term trade signals
- **Risk Management**: Use freezes on short-term levels
- **Monitoring**: Continuous quality control of short-term signals
- ** Adaptation**: Regular update for short-term market changes

 def create_schr_short3_features(self, data):
""create of signs on base SCHORT3""

# Basic short-term features
 short_features = self.create_basic_short_features(data)

# Signs of short-term signals
 signal_features = self.create_signal_features(data)

# Signs of short-term pathers
 pattern_features = self.create_pattern_features(data)

# Signs of short-term volatility
 volatility_features = self.create_volatility_features(data)

# Merging all the signs
 all_features = pd.concat([
 short_features,
 signal_features,
 pattern_features,
 volatility_features
 ], axis=1)

 return all_features

 def create_basic_short_features(self, data):
""create basic short-term features""

 features = pd.dataFrame()

# Main short-term paragraphs
 features['short_term_signal'] = data['short_term_signal']
 features['short_term_strength'] = data['short_term_strength']
 features['short_term_direction'] = data['short_term_direction']
 features['short_term_momentum'] = data['short_term_momentum']

# Short-term levels
 features['short_support'] = data['short_support']
 features['short_resistance'] = data['short_resistance']
 features['short_pivot'] = data['short_pivot']
 features['short_fibonacci'] = data['short_fibonacci']

# Distances to short-term levels
 features['distance_to_short_support'] = data['close'] - data['short_support']
 features['distance_to_short_resistance'] = data['short_resistance'] - data['close']
 features['distance_to_short_pivot'] = abs(data['close'] - data['short_pivot'])

# Relative distances
 features['relative_distance_short_support'] = features['distance_to_short_support'] / data['close']
 features['relative_distance_short_resistance'] = features['distance_to_short_resistance'] / data['close']
 features['relative_distance_short_pivot'] = features['distance_to_short_pivot'] / data['close']

 return features

 def create_signal_features(self, data):
""create signs of short-term signals."

 features = pd.dataFrame()

# Short-term signals
 features['short_buy_signal'] = data['short_buy_signal']
 features['short_sell_signal'] = data['short_sell_signal']
 features['short_hold_signal'] = data['short_hold_signal']
 features['short_reverse_signal'] = data['short_reverse_signal']

# Quality of short-term signals
 features['short_signal_quality'] = self.calculate_short_signal_quality(data)
 features['short_signal_reliability'] = self.calculate_short_signal_reliability(data)
 features['short_signal_strength'] = self.calculate_short_signal_strength(data)
 features['short_signal_durability'] = self.calculate_short_signal_durability(data)

# Short-term signal statistics
 features['short_hits'] = data['short_hits']
 features['short_breaks'] = data['short_breaks']
 features['short_bounces'] = data['short_bounces']
 features['short_accuracy'] = data['short_accuracy']

# Relationship
 features['short_break_bounce_ratio'] = data['short_breaks'] / (data['short_bounces'] + 1)
 features['short_hit_accuracy_ratio'] = data['short_hits'] / (data['short_accuracy'] + 1)

 return features

 def create_pattern_features(self, data):
""create signs of short-term pathers."

 features = pd.dataFrame()

# Short-term pathites
 features['short_pattern'] = data['short_pattern']
 features['short_complexity'] = data['short_complexity']
 features['short_symmetry'] = data['short_symmetry']
 features['short_harmony'] = data['short_harmony']

# Normalization of Pathers
 features['short_pattern_normalized'] = (data['short_pattern'] - data['short_pattern'].rolling(20).mean()) / data['short_pattern'].rolling(20).std()
 features['short_complexity_normalized'] = (data['short_complexity'] - data['short_complexity'].rolling(20).mean()) / data['short_complexity'].rolling(20).std()

# Change in patterns
 features['short_pattern_change'] = data['short_pattern'].diff()
 features['short_complexity_change'] = data['short_complexity'].diff()
 features['short_symmetry_change'] = data['short_symmetry'].diff()
 features['short_harmony_change'] = data['short_harmony'].diff()

 return features

 def create_volatility_features(self, data):
""create signs of short-term volatility."

 features = pd.dataFrame()

# Short-term volatility
 features['short_volatility'] = data['short_volatility']
 features['short_volume'] = data['short_volume']
 features['short_liquidity'] = data['short_liquidity']
 features['short_pressure'] = data['short_pressure']

# Normalization of volatility
 features['short_volatility_normalized'] = (data['short_volatility'] - data['short_volatility'].rolling(20).mean()) / data['short_volatility'].rolling(20).std()
 features['short_volume_normalized'] = (data['short_volume'] - data['short_volume'].rolling(20).mean()) / data['short_volume'].rolling(20).std()

# Change in volatility
 features['short_volatility_change'] = data['short_volatility'].diff()
 features['short_volume_change'] = data['short_volume'].diff()
 features['short_liquidity_change'] = data['short_liquidity'].diff()
 features['short_pressure_change'] = data['short_pressure'].diff()

# Sliding average volatility
 for period in [5, 10, 20, 50]:
 features[f'short_volatility_ma_{period}'] = data['short_volatility'].rolling(period).mean()
 features[f'short_volume_ma_{period}'] = data['short_volume'].rolling(period).mean()
 features[f'short_liquidity_ma_{period}'] = data['short_liquidity'].rolling(period).mean()
 features[f'short_pressure_ma_{period}'] = data['short_pressure'].rolling(period).mean()

 return features

 def create_schr_short3_target(self, data):
""create target variable for SCHR SHORT3""

# Future direction of price
 future_price = data['close'].shift(-1)
 price_direction = (future_price > data['close']).astype(int)

# Future short-term signals
 future_short_signals = self.calculate_future_short_signals(data)

# Future Short Term Pathers
 future_short_patterns = self.calculate_future_short_patterns(data)

# Future short-term rebounds
 future_short_bounces = self.calculate_future_short_bounces(data)

# Combination of target variables
 target = pd.dataFrame({
 'price_direction': price_direction,
 'short_signal_direction': future_short_signals,
 'short_pattern_direction': future_short_patterns,
 'short_bounce_direction': future_short_bounces
 })

 return target

 def train_schr_short3_model(self, features, target):
"Learning the Model on Bases SCHR SHORT3"

# Data production
 data = pd.concat([features, target], axis=1)
 data = data.dropna()

# Separation on train/validation
 split_idx = int(len(data) * 0.8)
 train_data = data.iloc[:split_idx]
 val_data = data.iloc[split_idx:]

♪ Create pre-reactor
 self.predictor = TabularPredictor(
 label='price_direction',
 problem_type='binary',
 eval_metric='accuracy',
 path='schr_short3_ml_model'
 )

# Model learning
 self.predictor.fit(
 train_data,
 time_limit=3600,
 presets='best_quality',
 hyperparameters={
 'GBM': [
 {'num_boost_round': 3000, 'learning_rate': 0.03, 'max_depth': 10},
 {'num_boost_round': 5000, 'learning_rate': 0.02, 'max_depth': 12}
 ],
 'XGB': [
 {'n_estimators': 3000, 'learning_rate': 0.03, 'max_depth': 10},
 {'n_estimators': 5000, 'learning_rate': 0.02, 'max_depth': 12}
 ],
 'CAT': [
 {'iterations': 3000, 'learning_rate': 0.03, 'depth': 10},
 {'iterations': 5000, 'learning_rate': 0.02, 'depth': 12}
 ],
 'RF': [
 {'n_estimators': 1000, 'max_depth': 20},
 {'n_estimators': 2000, 'max_depth': 25}
 ]
 }
 )

# Model evaluation
 val_predictions = self.predictor.predict(val_data.drop(columns=['price_direction', 'short_signal_direction', 'short_pattern_direction', 'short_bounce_direction']))
 val_accuracy = accuracy_score(val_data['price_direction'], val_predictions)

(f) The accuracy of the SCHR SHORT3 model: {val_accuracy:.3f})

 return self.predictor
```

** Detailed description of model SCHR SHORT3 training parameters:**

- **'features'**: Signs for learning
- Type: DataFrame
- Contains: all signs of SCHR SHORT3
- Application: input data for the model
- Processing: normalization and scaling
- Requirements: No pass

- **'target'**: Target variable
- Type: DataFrame
- Contains: direction of price, short-term signals, pathetics, rebounds
- Application: training the model
- Format: Binary tags (0/1)
- Requirements: compliance with indices with characteristics

- **'data'**: Joint data
- Type: DataFrame
- Contains: Features + Target
- Application: training the model
- Processing: remove passes
- Requirements: No NaN values

- **'split_idx'**: partition index
- Type:int
- Formula: in (len(data) * 0.8)
- Application: separation on train/validation
%: 80% for education, 20% for promotion
- Recommendation: 7.7-0.8 for SCHR SHORT3

- **'training_data'**: data for learning
- Type: DataFrame
Size: 80 per cent from general data
- Application: training the model
- Requirements: No pass
- Processing: Normalization of topics

- **`val_data`**: data for validation
- Type: DataFrame
Size: 20 per cent from general data
- Application: model evaluation
- Requirements: No pass
- Processing: the same normalization as for train

- **'label='price_direction'**: Target variable
- Type: str
- Value: 'price_direction'
- Application: training the model
- Format: Binary (0/1)
- Interpretation: 0 = fall, 1 = height

- **'problem_type='binary'**: Type of task
- Type: str
- Meaning: 'binary' for binary classification
- Alternatives: 'multiclass', 'regression'
- Application: definition of model type
- Result: selection of appropriate algorithms

- **'eval_metric='accuracy'**: Metric evaluation
- Type: str
- Value: 'accuracy' for accuracy
- Alternatives: 'roc_auc', 'f1', 'precision', 'recall'
- Application: optimization of the model
- Benefits: simplicity of interpretation

- **'path='schr_short3_ml_model'**: Path for model preservation
- Type: str
- Application: maintenance of the trained model
- Contains: model weight, metadata, configuration
- Use: loading for productions
- Format: directory with model files

- **'time_limit=3600'**: Time limit
- Units: seconds
- Value: 3,600 (1 hour)
Application: monitoring of the time of instruction
Balance: more = better quality but slower
- Recommendation: 1,800-7200 seconds for SCHR SHORT3

- **'presets='best_quality'**: Quality Preface
- Type: str
- Value: 'best_quality' for maximum quality
- Alternatives: 'media_quality_faster_training', 'optimize_for_development'
Application: balance between quality and speed
- Result: more complex models, more time

- **'num_boost_rowd'**: Number of buzting rounds
- Range: 3,000 to 5,000
- Application: monitoring of model complexity
Balance: more rounds = better quality but slower
- Recommendation: 3,000-5,000 for SCHR SHORT3

- ** `learning_rate'**: Learning speed
Range: 0.02-0.03
- Value: 0.03, 0.02
Application: control of the speed of convergence
- Balance: higher speed = faster, but may learn over.
- Recommendation: 0.02-0.03 for SCHR SHORT3

- **'max_dept'**: Maximum tree depth
Range: 10-12
- Application: monitoring of model complexity
Balance: greater depth = better quality but retraining
- Recommendation: 10-12 for SCHR SHORT3

- ** `n_estimators'**: Number of trees
- Range: 3,000 to 5,000
- Application: monitoring of model complexity
Balance: more trees = better quality but slower
- Recommendation: 3,000-5,000 for SCHR SHORT3

- **/ 'items'**: Number of iterations CatBoost
- Range: 3,000 to 5,000
- Application: monitoring of model complexity
Balance: more iterations = better quality but slower
- Recommendation: 3,000-5,000 for SCHR SHORT3

- **'dept'**: depth CatBoost
Range: 10-12
- Application: monitoring of model complexity
Balance: greater depth = better quality but retraining
- Recommendation: 10-12 for SCHR SHORT3

- **/ `val_predictations'**: Projections on validation
- Type: numpy array
- Contains: model predictions
- Application: evaluation of performance
- Format: Binary tags (0/1)
- Interpretation: 0 = fall, 1 = height

- ** `val_accuracy'**: Accuracy on validation
Type: float
- Range: from 0 to 1
- Application: model quality assessment
- Interpretation: 0.5 = accidental, 0.7-0.8 = good, 0.8-0.9 = excellent, > 0.9 = excellent
- Formula: accuracy_score['price_direction'], val_predations)

**parameters validation:**

- **'start_data'**: Start date backtest
- Type: Datame
Application: Limitation of the test period
- Format: 'YYYY-MM-DD'
- Recommendation: not less than 1 year of data

- ** `end_data'**: End date backtest
- Type: Datame
Application: Limitation of the test period
- Format: 'YYYY-MM-DD'
- Recommendation: not more than the current date

- ** `test_data'**: data for testing
- Type: DataFrame
- Contains: data over the test period
- Application: evaluation of performance
- Requirements: No pass
- Processing: the same normalization as for train

- **'predications'**: Model predictions
- Type: numpy array
- Contains: Forecasts for all test data
- Application: Calculation of return
- Format: Binary tags (0/1)
- Interpretation: 0 = fall, 1 = height

- **'probabyties'**: Probability of preferences
- Type: numpy array
- Contains: Probability for each class
- Application: confidence assessment
- Format: [prob_class_0, prob_class_1]
- Interpretation: from 0 to 1

- **'returns'**: Price return
- Type: pandas Series
- Formula: test_data['close']. pct_change()
- Application: Calculation of the return of the strategy
- Units: unlimited
- Interpretation: positive = height, negative = fall

- ** `Strategy_returns'**: Strategy return
- Type: pandas Series
- Formula: Preventions * returns
- Application: Calculation of the return of the strategy
- Units: unlimited
- Interpretation: positive = profit, negative = loss

- **'total_return'**: Total return
Type: float
- Formula: strategy_returns.sum()
- Application: evaluation of overall performance
- Units: unlimited
- Interpretation: positive = profit, negative = loss

- **/sharpe_ratio'**: Sharpe coefficient
Type: float
- Formula: strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
- Application: risk-income assessment
- Units: unlimited
- Interpretation: > 1 = good, > 2 = excellent, > 3 = excellent

- **'max_drawdown'**: Maximum draught
Type: float
- Application: Assessment of maximum loss
- Units: unlimited
- Interpretation: negative value, less, the better
- Calculation: maximum sequence of losses

- **/win_rate'**: Percentage of winning transactions
Type: float
- Formula: (Strategy_returns >0.mean()
- Application: evaluation of signal accuracy
- Units: unlimited
- Interpretation: from 0 to 1, the more the better

- **'training_period'**: Period of study
- Type:int
Value: 252 days
Application: size of the training window
- Units: days
- Recommendation: 200-300 days for SCHR SHORT3

- ** `test_period'**: Test period
- Type:int
Value: 63 days
Application: size of test window
- Units: days
- Recommendation: 50-100 days for SCHR SHORT3

- ** `n_simulations'**: Number of simulations
- Type:int
Value: 1000
Application: Monte Carlo Analysis
- Recommendation: 1000-10000 for SCHR SHORT3
Balance: more = more accurate but slower

- **/sample_data'**: Sample data
- Type: DataFrame
- Size: 80 per cent from reference data
- Application: random sample for simulation
- Processing: with replacement (replace=True)
- Requirements: No pass

** Practical recommendations:**

- ** Data quality**: Critical for accuracy SCHR SHORT3
- ** Time frame**: Use multiple timeframes
- **validation**: Mandatory for short-term trade signals
- **Risk Management**: Use freezes on short-term levels
- **Monitoring**: Continuous quality control of short-term signals
- ** Adaptation**: Regular update for short-term market changes
```

♪ ♪ Validation model

<img src="images/optimized/validation_short3.png" alt="Methods validation SHORT3" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 23.6: Methods satisfaction SCHR SHORT3 model - from backtest to structuring*

**Methods validation:**
- **Backtest Analysis**: Historical performance, profit calculation, risk analysis
**Walk-Forward Analysis**: Rolling Window, market adaptation, realistic assessment
**Monte Carlo Simulation**: Random Samples, Statistical Value
- **Cross-Validation**: Cross-validation, check stability
- **Out-of-Sample testing**: Testing on new data
- **Strates test**: Test in extreme conditions

** Results of validation:**
- **Sharpe Ratio**: 2.5
- ** Maximum draught**: 7.2%
- **Win Rate**: 72.8%
- **Profit Factor**: 2.1
- ** Annual return**: 68.4 per cent

### Backtest

```python
def schr_short3_backtest(self, data, start_date, end_date):
"Backtest SCHR SHORT3"

# Data filtering on dates
 test_data = data[(data.index >= start_date) & (data.index <= end_date)]

# Premonition
 predictions = self.predictor.predict(test_data)
 probabilities = self.predictor.predict_proba(test_data)

# Calculation of return
 returns = test_data['close'].pct_change()
 strategy_returns = predictions * returns

# metrics backtest
 total_return = strategy_returns.sum()
 sharpe_ratio = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
 max_drawdown = self.calculate_max_drawdown(strategy_returns)

 return {
 'total_return': total_return,
 'sharpe_ratio': sharpe_ratio,
 'max_drawdown': max_drawdown,
 'win_rate': (strategy_returns > 0).mean()
 }
```

### Walk-Forward Analysis

```python
def schr_short3_walk_forward(self, data, train_period=252, test_period=63):
"Walk-forward analysis for SCHR SHORT3"

 results = []

 for i in range(0, len(data) - train_period - test_period, test_period):
# Training
 train_data = data.iloc[i:i+train_period]
 model = self.train_schr_short3_model(train_data)

# Testing
 test_data = data.iloc[i+train_period:i+train_period+test_period]
 test_results = self.schr_short3_backtest(test_data)

 results.append(test_results)

 return results
```

### Monte Carlo Simulation

```python
def schr_short3_monte_carlo(self, data, n_simulations=1000):
"Monte Carlo Simulation for SCHR SHORT3"

 results = []

 for i in range(n_simulations):
# Random data sample
 sample_data = data.sample(frac=0.8, replace=True)

# Model learning
 model = self.train_schr_short3_model(sample_data)

# Testing
 test_results = self.schr_short3_backtest(sample_data)
 results.append(test_results)

 return results
```

♪ The thing on the blockage

<img src="images/optimized/blockchain_short3.png" alt="integration with SHORT3 block" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 23.7: integration of SCHR SHORT3 with blocker - from smart contracts to automatic trade*

**components integration:**
- **Smart Contacts**: signal storage, automatic execution, transparency of operations
- **DEX integration**: Direct trade, liquidity, decentralization
- **signal Storage**: Storage of locker signals, unalterable
- **Automated Trading**: Automatic trading, signal execution
- **Risk Management**: Management risk, position limits
- **Performance Trading**: Traceability, metrics

** The benefits of block-integration:**
- ** Transparency**: All operations are visible in the locker room
- ** Decentralization**: No single refusal point
- ** Automation**: Automatic trade performance
- ** Safety**: cryptographic protection
- ** capacity**: large volume processing capacity

♪ ## ♪ ♪ smart contract ♪

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SCHRShort3TradingContract {
 struct SCHRShort3signal {
 uint256 timestamp;
 int256 shortTermsignal;
 int256 shortTermStrength;
 int256 shortTermDirection;
 int256 shortTermMomentum;
 int256 shortSupport;
 int256 shortResistance;
 int256 shortPivot;
 bool shortBuysignal;
 bool shortSellsignal;
 bool shortHoldsignal;
 bool shortReversesignal;
 uint256 confidence;
 }

 mapping(uint256 => SCHRShort3signal) public signals;
 uint256 public signalCount;

 function addSCHRShort3signal(
 int256 shortTermsignal,
 int256 shortTermStrength,
 int256 shortTermDirection,
 int256 shortTermMomentum,
 int256 shortSupport,
 int256 shortResistance,
 int256 shortPivot,
 bool shortBuysignal,
 bool shortSellsignal,
 bool shortHoldsignal,
 bool shortReversesignal,
 uint256 confidence
 ) external {
 signals[signalCount] = SCHRShort3signal({
 timestamp: block.timestamp,
 shortTermsignal: shortTermsignal,
 shortTermStrength: shortTermStrength,
 shortTermDirection: shortTermDirection,
 shortTermMomentum: shortTermMomentum,
 shortSupport: shortSupport,
 shortResistance: shortResistance,
 shortPivot: shortPivot,
 shortBuysignal: shortBuysignal,
 shortSellsignal: shortSellsignal,
 shortHoldsignal: shortHoldsignal,
 shortReversesignal: shortReversesignal,
 confidence: confidence
 });

 signalCount++;
 }

 function getLatestsignal() external View returns (SCHRShort3signal memory) {
 return signals[signalCount - 1];
 }
}
```

### integration with DEX

```python
class SCHRShort3DEXintegration:
 """integration SCHR SHORT3 with DEX"""

 def __init__(self, contract_address, private_key):
 self.contract_address = contract_address
 self.private_key = private_key
 self.web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))

 def execute_schr_short3_trade(self, signal):
"Seting Trade on Base SCHR SHORT3""

 if signal['shortBuysignal'] and signal['confidence'] > 0.8:
# Short-term purchase
 self.buy_token(signal['amount'])
 elif signal['shortSellsignal'] and signal['confidence'] > 0.8:
# Short-term sales
 self.sell_token(signal['amount'])
 elif signal['shortHoldsignal'] and signal['confidence'] > 0.8:
# Short-term retention
 self.hold_position(signal['amount'])
 elif signal['shortReversesignal'] and signal['confidence'] > 0.8:
# Short-term turn
 self.reverse_trade(signal['amount'])

 def buy_token(self, amount):
"The purchase of the current."
# Buying through DEX
 pass

 def sell_token(self, amount):
"Selling the Token."
# Sale through DEX
 pass

 def hold_position(self, amount):
"""""""""""""
# Implementation of the Holding Position
 pass

 def reverse_trade(self, amount):
"Reverse trade"
# Realization of reverse trade through DEX
 pass
```

## Results

<img src="images/optimized/performance_short3.png" alt="Results of performance SHORT3" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 23.8: Results performance SCHR SHORT3 - metrics, return and comparison*

**Performance of the model:**
- **Definity**: 91.8 per cent
- **Precision**: 91.2%
- **Recall**: 90.8%
- **F1-Score**: 91.0%
- **Sharpe Ratio**: 2.5
- ** Maximum draught**: 7.2%
- ** Annual return**: 68.4 per cent

**Financial metrics:**
- **Sharpe Ratio**: 2.5
- **Max Drawdown**: 7.2%
- **Win Rate**: 72.8%
- **Profit Factor**: 2.1

** Income on Timeframe:**
- **M1**: 38.2%
- **M5**: 42.1%
- **M15**: 48.7%
- **H1**: 55.3%
- **H4**: 61.8%
- **D1**: 68.4%
- **W1**: 71.2%
- **MN1**: 68.4%

**comparison with other indicators:**
- **SCHR SHORT3**: 68.4%
- **RSI**: 35.2%
- **MACD**: 42.8%
- **Bollinger**: 38.7%
- **SMA**: 41.3%
- **EMA**: 43.1%

### The strength of SCHR SHORT3

1. **Chrical accuracy** - provides accurate short-term signals
2. ** Rapid adaptation** - adapts rapidly to market changes
3. ** High frequency** - generates many trading opportunities
4. **Lower** - Minimum delay in signals
5. **Stability**-Workinget on all Times

### The weaknesses of SCHR SHORT3

1. ** High frequency** - can generate too many signals
2. ** False signals** - can generate false short-term signals
3. **dependency from volatility** - quality depends from volatility
4. **retraining** - may be retrained on historical data
5. **Complicity** - requires a thorough understanding of short-term trade

## Conclusion

SCHR SHORT3 is a powerful indicator for the creation of high-quality ML models of short-term trade and, if properly used, can ensure stable profitability and efficiency of the trading system.
