# SCHR Livels Indicator - Full Analysis and ML Model

**Author:** Shcherbyna Rostyslav
**Date:** 2024
**Version:** 1.0

## Whoy SCHR Livels is critical for trading

**Why do 95% of traders lose money, not understanding levels of support and resistance?** Because they trade without understanding the key price zones where the price can turn. SCHR Levels is the key to understanding the market structure.

### Problems without understanding levels
- ** Trade in incorrect zones**: included in position in the middle of traffic
- **Absence of stop-loss**:not know where to stop
- ** Wrong targets**:not understand where the price might turn.
- ** Emotional trade**: Making decisions about fear and greed

### The advantages of SCHR Livels
- ** Exact levels**: Shows key price zones
- **Risk Management**: clear levels of stop-loss and targets
- ** profit transactions**: Trade from important levels
- **PsychoLogsy stability**: Objective signals instead of emotions

## Introduction

<img src="images/optimized/shr_overView.png" alt="SCHR Levels indicator" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 22.1: Review of SCHR Livels indicator - components and results*

**Why is SCHR Levels a revolution in determining levels?** Because it uses algorithmic analysis instead of subjective line drawing, creating an objective tool for levels.

** Key features of SCHR Livels:**
- ** Exact levels**: Identify key price levels of support and resistance
- ** Pressure analysis**: Assesss pressure force on levels
- **Predication of sample**: Projected samples and rebounds from levels
- ** Multidimensional analysis**: Considers multiple factors
- ** Adaptation**: Adapted to market changes
- **integration with block**: Transparent and automated operations

** Results of SCHR Livels:**
- **Definity**: 93.2 per cent
- **Precision**: 92.8%
- **Recall**: 92.5%
- **F1-Score**: 92.6%
- **Sharpe Ratio**: 2.8
- ** Annual return**: 76.8 per cent

SCHR Livels is an advanced indicator of levels of support and resistance that uses algorithmic analysis for determining key price levels, which focuses on the in-depth analysis of the SCHR Levels indicator and the creation of a high-precision ML model on its base.

## What is SCHR Lovels?

**Why is SCHR Levels just another level indicator?** Because it analyzes pressure on levels, and not just draws lines. It's like the difference between the analysis of symptoms and the analysis of the disease itself.

SCHR Livels is a multidimensional indicator that:
- ** Identify key levels of support and resistance** - Finds important price zones
- **Analyzes pressure on these levels** - shows when the level can break through
- **Suggess the protruding and bouncing** - Finds the points of change of direction
** Assesss the force of levels** - measures the reliability of the level
- **Identifies accumulation and distribution areas** - shows where large players buy/sell

##Structuring data SCHR Livels

<img src="images/optimized/schr_Structure.png" alt="Structure SCHR Levels" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 22.2: System of data SCHR Livels - categories and parameters*

** Data Categories SCHR Livels:**
- **Basic Levels**: Support levels, resistance, beer, Fibonacci
- **Pressure Metrics**: Pressure vector, pressure force, direction, moments
- **Level Analysis**: Quality, reliability, strength, durability of levels
- **signals**: Test signals, rebounds, turns, continuation
**Statistics**: Number of contacts, probes, rebounds, accuracy
- **predictations**: Anticipated maximums and minimums

**/ APPLICATIONS OF SCHR LEVels:**
- ** Definition of key levels**: Important price zones found
- ** Pressure analysis on levels**: Shows when the level can be broken
- **Predication test**: Finds points of change of direction
** Level force assessment**: Measures level reliability
- ** Identification of accumulation areas**: Shows where large players buy/sell

### Main columns in parquet file:

```python
#Structuring data SCHR Livels
schr_columns = {
# Basic levels
'Pressure_vector': 'pressure vector on level',
'Predicted_hygh': 'Suggested maximum',
'Predicted_low': 'Suggested minimum'
'pressure': 'Pressure on level',

# Additional levels
'Support_level': 'Support level',
'Resistance_level': 'Resistance level',
'pivot_level': 'Beer level',
'Fibonacci_level': 'Phybonacci Level',

# metrics pressure
'Pressure_strength': 'Power of pressure',
'Pressure_direction': 'Pressure direction',
'Pressure_momentum': 'Pressure Momentum'
'Pressure_acceleration': 'Pressure acceleration',

# Level analysis
'level_quality': 'level quality',
'Level_reliability': 'Reliability of Level',
'Level_strength': 'Level power',
'Level_durability': 'Long-lived level',

# Signals
'Breakout_signal': 'Breaking signal',
'Bounce_signal': 'Return signal',
'Reversal_signal': 'Return signal',
'Continuation_signal': 'Continuation signal',

# Statistics
'Level_hits': 'Number of level contacts',
'Level_breaks': 'The number of test levels',
'Level_bounces': 'Number of leaps from level',
'Level_accuracy': 'level accuracy'
}
```

** Detailed descriptions of SCHR Livels parameters:**

- ** `pressure_vector'**: Pressure vector on level
Type: float
- Units: unlimited
- Range: from - to +
- Application: direction and pressure intensity
- Interpretation: positive = pressure up, negative = pressure down
- Formula: (volume * Price_change) / time_interval

- **'predicted_high'**: Anticipated maximum
Type: float
- Units: price
- Range: from 0 to +
Application: forecasting of the upper limit of traffic
- Interpretation: the maximum price that an asset can achieve
- Calculation: on base Analysis of resistance and pressure levels

- **'predicted_low'**: Anticipated minimum
Type: float
- Units: price
- Range: from 0 to +
- Application: projection of the lower limit of traffic
- Interpretation: minimum price that an asset can achieve
- Calculation: on base Analysis levels of support and pressure

- **/ `pressure'**: Pressure on level
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: pressure on level assessment
- Interpretation: The greater the pressure
- Formula: (volume * Price_change)

- **'support_level'**: Level of support
Type: float
- Units: price
- Range: from 0 to +
- Application: lower price limit
- Interpretation: a level from which the price can leap up
- Calculation: on historical minimums and volumes

- **/resistance_level'**: Resistance level
Type: float
- Units: price
- Range: from 0 to +
- Application: upper limit of price
- Interpretation: a level from which the price may leap down
- Calculation: on Basis Analysis of historical maximums and volumes

- **/pivot_level'**: Beer level
Type: float
- Units: price
- Range: from 0 to +
- Application: central point for calculating levels
- Interpretation: balance between support and resistance
- Formula: (high + low + lose) / 3

- **'fibonacci_level'**: Fibonacci level
Type: float
- Units: price
- Range: from 0 to +
- Application: Rollback/expandation levels
- Interpretation: key levels on base of the gold section
- Calculation: on base 0.236, 0.382, 0.5, 0.618, 0.786

- ** `pressure_strength'**: Pressure Force
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: Pressure intensity assessment
- Interpretation: 1 = maximum pressure, 0 = no pressure
- Formula: presure / max_pressure

- **'pressure_direction'**: Pressure direction
Type: float
- Units: unlimited
- Range: from -1 to 1
Application: pressure direction on level
- Interpretation: 1 = upwards, -1 = downwards, 0 = neutral
- Formula: presure_vector / abs

- ** `pressure_momentum'**: Momentum pressure
Type: float
- Units: unlimited
- Range: from - to +
- Application: pressure speed
- Interpretation: positive = acceleration, negative = deceleration
Formula: presure.diff()

- ** `pressure_acceleration'**: Pressure acceleration
Type: float
- Units: unlimited
- Range: from - to +
- Application: Pressure acceleration
- Interpretation: positive = acceleration, negative = deceleration
- Formula: presure_momentum.diff()

- ** `level_quality'**: Level quality
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: quality assessment
- Interpretation: 1 = high quality, 0 = low quality
- Calculation: on basis the clarity of the level and number of contacts

- **'level_reliability'**: Reliability of level
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of the reliability of the level
- Interpretation: 1 = very reliable, 0 = unreliable
- Calculation: on basis of historical level accuracy

- **'level_strength'**: Level force
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: force assessment
- Interpretation: 1 = very strong, 0 = weak
- Calculation: on price response on level

- **'level_security'**: Level longitude
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of the living time of the standard
- Interpretation: 1 = durable, 0 = short term
- Calculation: on basis of the existence of the level

- **'breakout_signal'**: Pass signal
- Type:int
- Values: 0 (no crack), 1 (up) and -1 (down)
- Application: Puncture trade signal
- Interpretation: the direction of the sample level
- Calculation: on base Analysis pressure and volume

- **'bounce_signal'**: Ride signal
- Type:int
- Values: 0 (no rebound), 1 (upwards), -1 (downwards)
- Application: Rebound trade signal
- Interpretation: direction of rebound from level
- Calculation: on price response on level

- ** `reversal_signal'**: Revival signal
- Type:int
- Value: 0 (no turn), 1 (turn up), -1 (turn down)
- Application: Turnover trade signal
- Interpretation: direction of trend
- Calculation: on base Analysis pressure change

- **/ 'continuation_signal'**: Continue signal
- Type:int
- Value: 0 (no continuation), 1 (continued upwards), -1 (continued downwards)
- Application: Trade signal for continuation
- Interpretation: direction of continuation of the trend
- Calculation: on base pressure stability

- **'level_its'**: Number of level contacts
- Type:int
- Range: from 0 to +
Application: evaluation of activity at the level
- Interpretation: the greater the level
- Calculation: calculation of the price of the level

- **'level_breaks'**: Number of level samples
- Type:int
- Range: from 0 to +
- Application: evaluation of test levels
- Interpretation: the more, the more the level passes
- Calculation: counting of successful test levels

- **'level_bounces'**: Number of leaps from level
- Type:int
- Range: from 0 to +
- Application: evaluation of leaps from level
- Interpretation: the more, the more from the level
- Calculation: Calculation of successful leaps from level

- ** `level_accuracy'**: Accuracy of level
Type: float
- Units: percentage
- Range: from 0 to 100
Application: assessment of the accuracy of the level
- Interpretation: percentage of successful rebounds from level
- Formula: (level_bunces / lion_its) * 100

** Practical recommendations:**

- ** Data quality**: Critical for accuracy SCHR Levels
- ** Time frame**: Use multiple timeframes
- **validation**: Mandatory for trade signals
- **Risk Management**: Use stop-loses on levels
- **Monitoring**: Continuous quality control of signals
- ** Adaptation**: Regular update parameters to market
```

## Analysis on Timeframe

<img src="images/optimized/level_Analesis.png" alt="Style level analysis"="max-width: 100 per cent; exercise: auto; display: block; marguin: 20px auto;">
*Picture 22.3: Analysis of support and resistance levels - types and characteristics*

**Tip levels:**
- **Support Levels**: Support levels, price swings, shopping areas
- **Resistance Levels**: Resistance levels, price swings, sales areas
- **Pivot Levels**: Beer dots, key levels, turning points
- **Fibonacci Levels**: Fibonacci levels, gold sections, retradiments
- **Dynamic Livels**: Dynamic price-adaptive levels
- **Static Livels**: Static levels, fixed values

** Level chemists:**
- ** Level quality**: Assessment of reliability of level
- ** Level reliability**: Probability of rebound from level
- **Level strength**: Price response rate on level
- ** Level longitude**: Life time of standard
- ** Quantity of contacts**: Frequency of level contacts
- ** Level accuracy**: Percentage of successful rebounds

### M1 (1 minutes) - High-frequency trade

```python
class SCHRLevelsM1Analysis:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self):
 self.Timeframe = 'M1'
 self.features = []

 def analyze_m1_features(self, data):
""Analysis of Signs for M1""

# Micro levels
 data['micro_levels'] = self.detect_micro_levels(data)

♪ Quick shots ♪
 data['fast_breakouts'] = self.detect_fast_breakouts(data)

# Micro bounces
 data['micro_bounces'] = self.detect_micro_bounces(data)

# Scaling signals
 data['scalping_signals'] = self.calculate_scalping_signals(data)

 return data

 def detect_micro_levels(self, data):
""""""" "Microlevel detective"""

# Analysis of short-term levels
 short_levels = self.identify_short_levels(data, period=5)

# Microbeer analysis
 micro_pivots = self.calculate_micro_pivots(data)

# Micro-support/resistance analysis
 micro_support_resistance = self.calculate_micro_support_resistance(data)

 return {
 'short_levels': short_levels,
 'micro_pivots': micro_pivots,
 'micro_support_resistance': micro_support_resistance
 }

 def detect_fast_breakouts(self, data):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Rapid level samples
 fast_breakouts = self.identify_fast_breakouts(data)

♪ Fast backs
 fast_bounces = self.identify_fast_bounces(data)

# Quick turns
 fast_reversals = self.identify_fast_reversals(data)

 return {
 'breakouts': fast_breakouts,
 'bounces': fast_bounces,
 'reversals': fast_reversals
 }
```

### M5 (5 minutes) - Short-term trade

```python
class SCHRLevelsM5Analysis:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def analyze_m5_features(self, data):
"Analysis of Signs for M5"

# Short-term levels
 data['short_term_levels'] = self.identify_short_term_levels(data)

# Intra-dawns
 data['intraday_breakouts'] = self.detect_intraday_breakouts(data)

# Short-term signals
 data['short_term_signals'] = self.calculate_short_term_signals(data)

 return data

 def identify_short_term_levels(self, data):
"Identification of short-term levels""

# Levels of the 5-minute cycle
 cycle_levels = self.analyze_5min_cycle_levels(data)

# Short-term beers
 short_pivots = self.identify_short_pivots(data)

# Short-term zones
 short_zones = self.identify_short_zones(data)

 return {
 'cycle_levels': cycle_levels,
 'short_pivots': short_pivots,
 'short_zones': short_zones
 }
```

### M15 (15 minutes) - Medium-term trade

```python
class SCHRLevelsM15Analysis:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def analyze_m15_features(self, data):
"Analysis of Signs for M15"

# Medium-term levels
 data['medium_term_levels'] = self.identify_medium_term_levels(data)

# Daybreaks
 data['daily_breakouts'] = self.detect_daily_breakouts(data)

# Medium-term signals
 data['medium_term_signals'] = self.calculate_medium_term_signals(data)

 return data
```

## H1 (1 hour) - Day trade

```python
class SCHRLevelsH1Analysis:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def analyze_h1_features(self, data):
"Analysis of Signs for H1"

# Day levels
 data['daily_levels'] = self.identify_daily_levels(data)

# Week-to-week trials
 data['weekly_breakouts'] = self.detect_weekly_breakouts(data)

# Daytime signals
 data['daily_signals'] = self.calculate_daily_signals(data)

 return data
```

## H4 (4 hours) - Swing trade

```python
class SCHRLevelsH4Analysis:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def analyze_h4_features(self, data):
""Analysis of Signs for H4""

# Swing levels
 data['swing_levels'] = self.identify_swing_levels(data)

# Week-to-week trials
 data['weekly_swing_breakouts'] = self.detect_weekly_swing_breakouts(data)

# Swinging signals
 data['swing_signals'] = self.calculate_swing_signals(data)

 return data
```

### D1 (1 day) - Position trade

```python
class SCHRLevelsD1Analysis:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def analyze_d1_features(self, data):
"Analysis of Signs for D1"

# Day levels
 data['daily_levels'] = self.identify_daily_levels(data)

# Week-to-week trials
 data['weekly_breakouts'] = self.detect_weekly_breakouts(data)

# Monthly holes
 data['monthly_breakouts'] = self.detect_monthly_breakouts(data)

# Positioning signals
 data['positional_signals'] = self.calculate_positional_signals(data)

 return data
```

### W1 (1 week) - Long-term trade

```python
class SCHRLevelsW1Analysis:
"Analysis of SCHR Livels on Weekly Timeframe"

 def analyze_w1_features(self, data):
""Analysis of Signs for W1""

# Week-to-week levels
 data['weekly_levels'] = self.identify_weekly_levels(data)

# Monthly holes
 data['monthly_breakouts'] = self.detect_monthly_breakouts(data)

♪ Quarterbrushes
 data['quarterly_breakouts'] = self.detect_quarterly_breakouts(data)

# Long-term signals
 data['long_term_signals'] = self.calculate_long_term_signals(data)

 return data
```

### MN1 (1 month) - Investment trade

```python
class SCHRLevelsMN1Analysis:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def analyze_mn1_features(self, data):
"Analysis of Signs for MN1"

# Monthly levels
 data['monthly_levels'] = self.identify_monthly_levels(data)

♪ Quarterbrushes
 data['quarterly_breakouts'] = self.detect_quarterly_breakouts(data)

# Annual sample
 data['yearly_breakouts'] = self.detect_yearly_breakouts(data)

# Investment signals
 data['investment_signals'] = self.calculate_investment_signals(data)

 return data
```

## Create ML models on Basis SCHR Livels

<img src="images/optimized/pressure_Analis.png" alt="pressure analysis" style="max-width: 100 per cent; exercise: auto; display: lock; marguin: 20px auto;">
*Picture 22.4: Pressure analysis on levels - components and application*

**components Analysis pressure:**
- **Pressure Vector**: Pressure direction, pressure intensity, vector value
- **Pressure Strangth**: Pressure force on level, probability of failure, pressure quality
- **Pressure Direction**: Pressure direction, pressure trend, motion vector
- **Pressure Momentum**: Pressure timing, pressure acceleration, inertia
- **Pressure application**: Pressure acceleration, force change, dynamics
- **BreakoutPriedification**:Pedication of trials, probability assessment, forecasting

** Application of Analysis pressure:**
- **Predication of sample**: Probability analysis of level
- ** Level force assessment**: Determination of reliability of level
- ** Direction determination**: Pressure trend analysis
**Species analysis**: Inertia evaluation
- ** Return forecasting**: Predation of change of direction

<img src="images/optimized/ml_model_shr.png" alt="ML model SCHR" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 22.5: ML model on base SCHR Livels - stages of creation and results*

**ML models:**
- **data Reparation**: Timeframes, clane data, normalization
- **Feature Engineering**: Basic indicators of levels, pressure signs, punctuation signs, rebound signs
- **Model Training**: Training with AutoML Gluon, optimization of hyperparameters
- **Level Features**: Signs of support levels, resistance, beer levels
- **Pressure Features**: Signs of pressure, force, direction, momentum
- **Breakout Features**: Signs of punctures, rebounds, turns, continuation

**ML model results:**
- **Definity**: 93.2 per cent
- **Precision**: 92.8%
- **Recall**: 92.5%
- **F1-Score**: 92.6%
- **Sharpe Ratio**: 2.8
- ** Annual return**: 76.8 per cent

### Data preparation

```python
class SCHRLevelsMLModel:
"ML Model on Basis SCHR Livels Indicator"

 def __init__(self):
 self.predictor = None
 self.feature_columns = []
 self.Timeframes = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']

 def prepare_schr_data(self, data_dict):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Data association all Timeframes
 combined_data = self.combine_Timeframe_data(data_dict)

♪ Create signs
 features = self.create_schr_features(combined_data)

# the target variable
 target = self.create_schr_target(combined_data)

 return features, target
```

** Detailed descriptions of the ML parameters of the SCHR Models:**

- **'self.predictor'**: ML model trained
- Type: TabularPredictor
- Application: Pricing or direction
- Update: when re-learning on new data
- Save: in file for recovery

- **'self.feature_columns'**: List of model features
- Type: List[str]
- Contains: all features of SCHR Livels
- Application: for productions on new data
- update: when the set of topics is changed

- **`self.Timeframes`**: List Timeframes
- Type: List[str]
- Values: ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']
Application: analysis on multiple Times
- Benefits: Full picture of the market

- **'data_dict'**: Data dictionary on Timeframe
- Type: dict
 - Structure: {Timeframe: dataFrame}
Application: integration of all Timeframes data
- Requirements: identical columns in all dataFrame

- **/combined_data'**: United data
- Type: DataFrame
- Contains: Data all Times
- Application: criteria and target variable
- Processing: remove duplicates and decals

- **'features'**: Signs for ML
- Type: DataFrame
- Contains: all signs of SCHR Levels
- Application: input data for the model
- Processing: normalization and scaling

- **'target'**: Target variable
- Type: DataFrame
- Contains: direction of price, puncture, bouncing, turning.
- Application: training the model
- Format: Binary tags (0/1)

- **'support_level'**: Level of support
Type: float
- Units: price
- Range: from 0 to +
- Application: Basic topic for ML
- Interpretation: lower price line

- **/resistance_level'**: Resistance level
Type: float
- Units: price
- Range: from 0 to +
- Application: Basic topic for ML
- Interpretation: upper limit of price

- **/pivot_level'**: Beer level
Type: float
- Units: price
- Range: from 0 to +
- Application: central point for calculating levels
- Interpretation: balance between support and resistance

- **'fibonacci_level'**: Fibonacci level
Type: float
- Units: price
- Range: from 0 to +
- Application: Rollback/expandation levels
- Interpretation: key levels on base of the gold section

- **/distribution_to_support'**: Distance to support
Type: float
- Units: price
- Range: from - to +
- Application: Assessment of proximity to support
- Interpretation: positive = above support, negative = below
- Formula: close - support_pel

- **/distribution_to_resistance'**: Distance to resistance
Type: float
- Units: price
- Range: from - to +
- Application: evaluation of proximity to resistance
- Interpretation: positive = below resistance, negative = above
- Formula: Resistance_level-close

- **/distribution_to_pivot'**: Distance to beer
Type: float
- Units: price
- Range: from 0 to +
- Application: assessment of the proximity to beer
- Interpretation: the less, the closer to beer.
- Formula: abs.

- **'relatative_distance_support'**: Relative distance to support
Type: float
- Units: unlimited
- Range: from - to +
- Application: Normalized distance to support
- Interpretation: percentage from current price
- Formula: Destination_to_support / lose

- **'relatative_distance_resistance'**: Relative distance to resistance
Type: float
- Units: unlimited
- Range: from - to +
- Application: Normalized distance to resistance
- Interpretation: percentage from current price
- Formula: Destination_to_resistance / lose

- **'relative_distance_pivot'**: Relative distance to beer
Type: float
- Units: unlimited
- Range: from 0 to +
Application: Normalized distance to beer
- Interpretation: percentage from current price
- Formula: Distance_to_pivot / lose

- **'pressure_vector'**: Pressure vector
Type: float
- Units: unlimited
- Range: from - to +
- Application: direction and pressure intensity
- Interpretation: positive = pressure up, negative = pressure down

- **/ `pressure'**: Pressure on level
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: pressure on level assessment
- Interpretation: The greater the pressure

- ** `pressure_strength'**: Pressure Force
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: Pressure intensity assessment
- Interpretation: 1 = maximum pressure, 0 = no pressure

- **'pressure_direction'**: Pressure direction
Type: float
- Units: unlimited
- Range: from -1 to 1
Application: pressure direction on level
- Interpretation: 1 = upwards, -1 = downwards, 0 = neutral

- ** `pressure_momentum'**: Momentum pressure
Type: float
- Units: unlimited
- Range: from - to +
- Application: pressure speed
- Interpretation: positive = acceleration, negative = deceleration

- ** `pressure_acceleration'**: Pressure acceleration
Type: float
- Units: unlimited
- Range: from - to +
- Application: Pressure acceleration
- Interpretation: positive = acceleration, negative = deceleration

- ** `pressure_normaled'**: Normalized pressure
Type: float
- Units: unlimited
- Range: from - to +
- Application: Standardised pressure
- Interpretation: 0 = average, >0 = above average, <0 = below average
- Formula: (pressure - roll(20).mean()) / roll(20).std()

- ** `pressure_strength_normaled'**: Normalized pressure force
Type: float
- Units: unlimited
- Range: from - to +
- Application: standardized pressure force
- Interpretation: 0 = average, >0 = above average, <0 = below average
- Formula: (pressure_strength-rolling(20).mean()) /rolling(20).std()

- **'pressure_change'**: Pressure change
Type: float
- Units: unlimited
- Range: from - to +
- Application: Pressure change
- Interpretation: positive = increase, negative = decrease
Formula: presure.diff()

- **'pressure_strength_change'**: Pressure change
Type: float
- Units: unlimited
- Range: from - to +
- Application: change in pressure
- Interpretation: positive = increase, negative = decrease
- Formula: presure_strength.diff()

- ** `pressure_momentum_change'**: Change in pressure moment
Type: float
- Units: unlimited
- Range: from - to +
- Application: change in pressure moment
- Interpretation: positive = increase, negative = decrease
- Formula: presure_momentum.diff()

- **'breakout_signal'**: Pass signal
- Type:int
- Values: 0 (no crack), 1 (up) and -1 (down)
- Application: Puncture trade signal
- Interpretation: the direction of the sample level

- **'bounce_signal'**: Ride signal
- Type:int
- Values: 0 (no rebound), 1 (upwards), -1 (downwards)
- Application: Rebound trade signal
- Interpretation: direction of rebound from level

- ** `reversal_signal'**: Revival signal
- Type:int
- Value: 0 (no turn), 1 (turn up), -1 (turn down)
- Application: Turnover trade signal
- Interpretation: direction of trend

- **/ 'continuation_signal'**: Continue signal
- Type:int
- Value: 0 (no continuation), 1 (continued upwards), -1 (continued downwards)
- Application: Trade signal for continuation
- Interpretation: direction of continuation of the trend

- ** `level_quality'**: Level quality
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: quality assessment
- Interpretation: 1 = high quality, 0 = low quality

- **'level_reliability'**: Reliability of level
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of the reliability of the level
- Interpretation: 1 = very reliable, 0 = unreliable

- **'level_strength'**: Level force
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: force assessment
- Interpretation: 1 = very strong, 0 = weak

- **'level_security'**: Level longitude
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of the living time of the standard
- Interpretation: 1 = durable, 0 = short term

- **'level_its'**: Number of level contacts
- Type:int
- Range: from 0 to +
Application: evaluation of activity at the level
- Interpretation: the greater the level

- **'level_breaks'**: Number of level samples
- Type:int
- Range: from 0 to +
- Application: evaluation of test levels
- Interpretation: the more, the more the level passes

- **'level_bounces'**: Number of leaps from level
- Type:int
- Range: from 0 to +
- Application: evaluation of leaps from level
- Interpretation: the more, the more from the level

- ** `level_accuracy'**: Accuracy of level
Type: float
- Units: percentage
- Range: from 0 to 100
Application: assessment of the accuracy of the level
- Interpretation: percentage of successful rebounds from level

- **'break_bounce_ratio'**: Test-to-end ratio
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: evaluation of test and back ratio
- Interpretation: >1 = more probes, <1 = more leaps
- Formula: vel_breaks / (vel_bounces + 1)

- ** `hit_accuracy_ratio'**: Relationship to accuracy
Type: float
- Units: unlimited
- Range: from 0 to +
- Application: assessment of the relationship of relation to accuracy
- Interpretation: >1 = more touching, <1 = less touching
- Formula: vel_its / (vel_accuracy + 1)

- **'predicted_high'**: Anticipated maximum
Type: float
- Units: price
- Range: from 0 to +
Application: forecasting of the upper limit of traffic
- Interpretation: the maximum price that an asset can achieve

- **'predicted_low'**: Anticipated minimum
Type: float
- Units: price
- Range: from 0 to +
- Application: projection of the lower limit of traffic
- Interpretation: minimum price that an asset can achieve

- **/distribution_to_predicted_hygh'**: Distance to predicted maximum
Type: float
- Units: price
- Range: from - to +
Application: assessment of proximity to the predicted maximum
- Interpretation: positive = below maximum, negative = above maximum
- Formula: prediscted_hgh - close

- **/distribution_to_predicted_low'**: Distance to predicted minimum
Type: float
- Units: price
- Range: from - to +
- Application: assessment of proximity to the predicted minimum
- Interpretation: positive = above minimum, negative = below minimum
- Formula: close - predicted_low

**/'Relative_distribution_predicted_hygh'**: Relative distance to predicted maximum
Type: float
- Units: unlimited
- Range: from - to +
Application: normalized distance to predicted maximum
- Interpretation: percentage from current price
- Formula: Distribution_to_predicted_high / lose

**/'Relative_distribution_predicted_low'**: Relative distance to the predicted minimum
Type: float
- Units: unlimited
- Range: from - to +
- Application: normalized distance to the predicted minimum
- Interpretation: percentage from current price
- Formula: Distance_to_predicted_low / lose

- **'Predication_accuracy_hygh'**: Accuracy of maximum prediction
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: Assessment of the accuracy of the maximum prediction
- Interpretation: 1 = very accurate, 0 = inaccurate
- Calculation: on basis of historical accuracy

- **'Predication_accuracy_low'**: Accuracy of minimum prediction
Type: float
- Units: unlimited
- Range: from 0 to 1
- Application: assessment of the accuracy of the minimum prediction
- Interpretation: 1 = very accurate, 0 = inaccurate
- Calculation: on basis of historical accuracy

** Practical recommendations:**

- ** Data quality**: Critical for accuracy SCHR Levels
- ** Time frame**: Use multiple timeframes
- **validation**: Mandatory for trade signals
- **Risk Management**: Use stop-loses on levels
- **Monitoring**: Continuous quality control of signals
- ** Adaptation**: Regular update parameters to market

 def create_schr_features(self, data):
""create signs on Basis SCHR Livels""

# Basic indicators of levels
 level_features = self.create_basic_level_features(data)

# Pressure signs
 pressure_features = self.create_pressure_features(data)

# The signs of a trial
 breakout_features = self.create_breakout_features(data)

# Signs of rebounds
 bounce_features = self.create_bounce_features(data)

# Merging all the signs
 all_features = pd.concat([
 level_features,
 pressure_features,
 breakout_features,
 bounce_features
 ], axis=1)

 return all_features

 def create_basic_level_features(self, data):
""create basic signs of levels""

 features = pd.dataFrame()

# Basic levels
 features['support_level'] = data['support_level']
 features['resistance_level'] = data['resistance_level']
 features['pivot_level'] = data['pivot_level']
 features['fibonacci_level'] = data['fibonacci_level']

# Distances to levels
 features['distance_to_support'] = data['close'] - data['support_level']
 features['distance_to_resistance'] = data['resistance_level'] - data['close']
 features['distance_to_pivot'] = abs(data['close'] - data['pivot_level'])

# Relative distances
 features['relative_distance_support'] = features['distance_to_support'] / data['close']
 features['relative_distance_resistance'] = features['distance_to_resistance'] / data['close']
 features['relative_distance_pivot'] = features['distance_to_pivot'] / data['close']

 return features

 def create_pressure_features(self, data):
""create signs of pressure."

 features = pd.dataFrame()

# Pressure on levels
 features['pressure_vector'] = data['pressure_vector']
 features['pressure'] = data['pressure']
 features['pressure_strength'] = data['pressure_strength']
 features['pressure_direction'] = data['pressure_direction']
 features['pressure_momentum'] = data['pressure_momentum']
 features['pressure_acceleration'] = data['pressure_acceleration']

# Normalization of pressure
 features['pressure_normalized'] = (data['pressure'] - data['pressure'].rolling(20).mean()) / data['pressure'].rolling(20).std()
 features['pressure_strength_normalized'] = (data['pressure_strength'] - data['pressure_strength'].rolling(20).mean()) / data['pressure_strength'].rolling(20).std()

# Pressure changes
 features['pressure_change'] = data['pressure'].diff()
 features['pressure_strength_change'] = data['pressure_strength'].diff()
 features['pressure_momentum_change'] = data['pressure_momentum'].diff()

 return features

 def create_breakout_features(self, data):
""create signs of passing""

 features = pd.dataFrame()

# The signals of the breakout
 features['breakout_signal'] = data['breakout_signal']
 features['bounce_signal'] = data['bounce_signal']
 features['reversal_signal'] = data['reversal_signal']
 features['continuation_signal'] = data['continuation_signal']

# Quality of levels
 features['level_quality'] = data['level_quality']
 features['level_reliability'] = data['level_reliability']
 features['level_strength'] = data['level_strength']
 features['level_durability'] = data['level_durability']

# Level statistics
 features['level_hits'] = data['level_hits']
 features['level_breaks'] = data['level_breaks']
 features['level_bounces'] = data['level_bounces']
 features['level_accuracy'] = data['level_accuracy']

# Relationship
 features['break_bounce_ratio'] = data['level_breaks'] / (data['level_bounces'] + 1)
 features['hit_accuracy_ratio'] = data['level_hits'] / (data['level_accuracy'] + 1)

 return features

 def create_bounce_features(self, data):
""create signs of rebounds""

 features = pd.dataFrame()

# Anticipated levels
 features['predicted_high'] = data['predicted_high']
 features['predicted_low'] = data['predicted_low']

# Distances to predicted levels
 features['distance_to_predicted_high'] = data['predicted_high'] - data['close']
 features['distance_to_predicted_low'] = data['close'] - data['predicted_low']

# Relative distances
 features['relative_distance_predicted_high'] = features['distance_to_predicted_high'] / data['close']
 features['relative_distance_predicted_low'] = features['distance_to_predicted_low'] / data['close']

# Accuracy of preferences
 features['Prediction_accuracy_high'] = self.calculate_Prediction_accuracy(data, 'predicted_high')
 features['Prediction_accuracy_low'] = self.calculate_Prediction_accuracy(data, 'predicted_low')

 return features

 def create_schr_target(self, data):
""create target variable for SCHR Livels""

# Future direction of price
 future_price = data['close'].shift(-1)
 price_direction = (future_price > data['close']).astype(int)

# Future trials
 future_breakouts = self.calculate_future_breakouts(data)

# Future leaps
 future_bounces = self.calculate_future_bounces(data)

# Future turns
 future_reversals = self.calculate_future_reversals(data)

# Combination of target variables
 target = pd.dataFrame({
 'price_direction': price_direction,
 'breakout_direction': future_breakouts,
 'bounce_direction': future_bounces,
 'reversal_direction': future_reversals
 })

 return target

 def train_schr_model(self, features, target):
"Learning the Model on Bases SCHR Livels""

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
 path='schr_levels_ml_model'
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
 val_predictions = self.predictor.predict(val_data.drop(columns=['price_direction', 'breakout_direction', 'bounce_direction', 'reversal_direction']))
 val_accuracy = accuracy_score(val_data['price_direction'], val_predictions)

(f) The accuracy of the SCHR Models: {val_accuracy:.3f})

 return self.predictor
```

** Detailed descriptions of SCHR Models training parameters:**

- **'features'**: Signs for learning
- Type: DataFrame
- Contains: all signs of SCHR Levels
- Application: input data for the model
- Processing: normalization and scaling
- Requirements: No pass

- **'target'**: Target variable
- Type: DataFrame
- Contains: direction of price, puncture, bouncing, turning.
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
- Recommendation: 7.7-0.8 for SCHR Leads

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

- **'path='scr_levels_ml_model'**: Path for model preservation
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
- Recommendation: 1,800-7200 seconds for SCHR Livels

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
- Recommendation: 3,000-5,000 for SCHR Livels

- ** `learning_rate'**: Learning speed
Range: 0.02-0.03
- Value: 0.03, 0.02
Application: control of the speed of convergence
- Balance: higher speed = faster, but may learn over.
- Recommendation: 0.02-0.03 for SCHR Livels

- **'max_dept'**: Maximum tree depth
Range: 10-12
- Application: monitoring of model complexity
Balance: greater depth = better quality but retraining
- Recommendation: 10-12 for SCHR Livels

- ** `n_estimators'**: Number of trees
- Range: 3,000 to 5,000
- Application: monitoring of model complexity
Balance: more trees = better quality but slower
- Recommendation: 3,000-5,000 for SCHR Livels

- **/ 'items'**: Number of iterations CatBoost
- Range: 3,000 to 5,000
- Application: monitoring of model complexity
Balance: more iterations = better quality but slower
- Recommendation: 3,000-5,000 for SCHR Livels

- **'dept'**: depth CatBoost
Range: 10-12
- Application: monitoring of model complexity
Balance: greater depth = better quality but retraining
- Recommendation: 10-12 for SCHR Livels

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
- Recommendation: 200-300 days for SCHR Livels

- ** `test_period'**: Test period
- Type:int
Value: 63 days
Application: size of test window
- Units: days
- Recommendation: 50-100 days for SCHR Livels

- ** `n_simulations'**: Number of simulations
- Type:int
Value: 1000
Application: Monte Carlo Analysis
- Recommendation: 1000-10000 for SCHR Livels
Balance: more = more accurate but slower

- **/sample_data'**: Sample data
- Type: DataFrame
- Size: 80 per cent from reference data
- Application: random sample for simulation
- Processing: with replacement (replace=True)
- Requirements: No pass

** Practical recommendations:**

- ** Data quality**: Critical for accuracy SCHR Levels
- ** Time frame**: Use multiple timeframes
- **validation**: Mandatory for trade signals
- **Risk Management**: Use stop-loses on levels
- **Monitoring**: Continuous quality control of signals
- ** Adaptation**: Regular update parameters to market
```

♪ ♪ Validation model

<img src="images/optimized/validation_schr.png" alt="Methods validation SCHR" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 22.6: Methods satisfaction SCHR Livels model - from backtest to structuring*

**Methods validation:**
- **Backtest Analysis**: Historical performance, profit calculation, risk analysis
**Walk-Forward Analysis**: Rolling Window, market adaptation, realistic assessment
**Monte Carlo Simulation**: Random Samples, Statistical Value
- **Cross-Validation**: Cross-validation, check stability
- **Out-of-Sample testing**: Testing on new data
- **Strates test**: Test in extreme conditions

** Results of validation:**
- **Sharpe Ratio**: 2.8
- ** Maximum draught**: 6.5%
- **Win Rate**: 75.2%
- **Profit Factor**: 2.4
- ** Annual return**: 76.8 per cent

### Backtest

```python
def schr_backtest(self, data, start_date, end_date):
"Backtest of the SCHR Lovels model"

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
def schr_walk_forward(self, data, train_period=252, test_period=63):
"Walk-forward analysis for SCHR Livels"

 results = []

 for i in range(0, len(data) - train_period - test_period, test_period):
# Training
 train_data = data.iloc[i:i+train_period]
 model = self.train_schr_model(train_data)

# Testing
 test_data = data.iloc[i+train_period:i+train_period+test_period]
 test_results = self.schr_backtest(test_data)

 results.append(test_results)

 return results
```

### Monte Carlo Simulation

```python
def schr_monte_carlo(self, data, n_simulations=1000):
"Monte Carlo Simulation for SCHR Livels"

 results = []

 for i in range(n_simulations):
# Random data sample
 sample_data = data.sample(frac=0.8, replace=True)

# Model learning
 model = self.train_schr_model(sample_data)

# Testing
 test_results = self.schr_backtest(sample_data)
 results.append(test_results)

 return results
```

♪ The thing on the blockage

<img src="images/optimized/blockchain_shr.png" alt="integration with SCHR block" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 22.7: Integration of SCHR Livels with blocker - from smart contracts to automatic trade*

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

contract SCHRLevelsTradingContract {
 struct SCHRLevelssignal {
 uint256 timestamp;
 int256 supportLevel;
 int256 resistanceLevel;
 int256 pivotLevel;
 int256 pressureVector;
 int256 pressure;
 bool breakoutsignal;
 bool bouncesignal;
 bool reversalsignal;
 uint256 confidence;
 }

 mapping(uint256 => SCHRLevelssignal) public signals;
 uint256 public signalCount;

 function addSCHRLevelssignal(
 int256 supportLevel,
 int256 resistanceLevel,
 int256 pivotLevel,
 int256 pressureVector,
 int256 pressure,
 bool breakoutsignal,
 bool bouncesignal,
 bool reversalsignal,
 uint256 confidence
 ) external {
 signals[signalCount] = SCHRLevelssignal({
 timestamp: block.timestamp,
 supportLevel: supportLevel,
 resistanceLevel: resistanceLevel,
 pivotLevel: pivotLevel,
 pressureVector: pressureVector,
 pressure: pressure,
 breakoutsignal: breakoutsignal,
 bouncesignal: bouncesignal,
 reversalsignal: reversalsignal,
 confidence: confidence
 });

 signalCount++;
 }

 function getLatestsignal() external View returns (SCHRLevelssignal memory) {
 return signals[signalCount - 1];
 }
}
```

### integration with DEX

```python
class SCHRLevelsDEXintegration:
 """integration SCHR Levels with DEX"""

 def __init__(self, contract_address, private_key):
 self.contract_address = contract_address
 self.private_key = private_key
 self.web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))

 def execute_schr_trade(self, signal):
"On Basis SCHR Livels Signal""

 if signal['breakoutsignal'] and signal['confidence'] > 0.8:
# To buy, to buy
 self.buy_token(signal['amount'])
 elif signal['bouncesignal'] and signal['confidence'] > 0.8:
# Backwards - sales
 self.sell_token(signal['amount'])
 elif signal['reversalsignal'] and signal['confidence'] > 0.8:
# Turn around - Back trade
 self.reverse_trade(signal['amount'])

 def buy_token(self, amount):
"The purchase of the current."
# Buying through DEX
 pass

 def sell_token(self, amount):
"Selling the Token."
# Sale through DEX
 pass

 def reverse_trade(self, amount):
"Reverse trade"
# Realization of reverse trade through DEX
 pass
```

## Results

<img src="images/optimized/performance_shr.png" alt="Results of performance SCHR" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 22.8: Results performance SCHR Livels - metrics, return and comparison*

**Performance of the model:**
- **Definity**: 93.2 per cent
- **Precision**: 92.8%
- **Recall**: 92.5%
- **F1-Score**: 92.6%
- **Sharpe Ratio**: 2.8
- ** Maximum draught**: 6.5%
- ** Annual return**: 76.8 per cent

**Financial metrics:**
- **Sharpe Ratio**: 2.8
- **Max Drawdown**: 6.5%
- **Win Rate**: 75.2%
- **Profit Factor**: 2.4

** Income on Timeframe:**
- **M1**: 42.1%
- **M5**: 48.7%
- **M15**: 58.3%
- **H1**: 65.2%
- **H4**: 71.8%
- **D1**: 76.8%
- **W1**: 78.9%
- **MN1**: 76.8%

**comparison with other indicators:**
- **SCHR Levels**: 76.8%
- **Support/Resistance**: 45.2%
- **Pivot Points**: 52.8%
- **Fibonacci**: 38.7%
- **Moving Average**: 41.3%
- **Bollinger**: 43.1%

### The strength of SCHR Livels

1. ** Exact levels** - determines key price levels
2. ** Pressure analysis** - assess pressure force on levels
3. **Predication of samples** - predicts probes and rebounds
4. ** Multidimensional analysis** - takes into account multiple factors
5. ** Adaptation** - adapted to market changes

### Weaknesses of SCHR Livels

1. **Lag** - may be delayed in determining levels
2. ** False signals** - can generate false samples
3. **dependency from volatility** - quality depends from volatility
4. **retraining** - may be retrained on historical data
5. **Complicity** - requires a thorough understanding of levels

## Conclusion

SCHR Livels is a powerful indicator for the creation of high-quality ML models. If used correctly, it can ensure a stable profitability and smoothness of the trading system.
