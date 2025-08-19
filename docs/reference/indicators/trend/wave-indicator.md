# Wave Indicator

## Overview

The Wave indicator is a sophisticated trend-following indicator that combines multiple momentum calculations to generate strong trading signals based on open price movements. It utilizes a dual-wave system with configurable trading rules and global signal filtering.

## Features

- **Dual Signal Validation**: Two-wave system for improved reliability
- **Flexible Configuration**: Multiple trading rules and filters
- **Strong Trend Identification**: Excellent for trending markets
- **Zone-Based Filtering**: Helps avoid counter-trend trades
- **Momentum Validation**: Advanced signal filtering algorithms
- **Visual Clarity**: Clear color coding and multiple visual elements
- **Comprehensive Signal Types**: Various signal combinations
- **Professional Grade**: Sophisticated algorithms for advanced strategies

## Usage

```python
from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters, ENUM_GLOBAL_TR

# Create parameters
params = WaveParameters(
    long1=339,
    fast1=10,
    trend1=2,
    tr1=ENUM_MOM_TR.TR_Fast,
    long2=22,
    fast2=11,
    trend2=4,
    tr2=ENUM_MOM_TR.TR_Fast,
    global_tr=ENUM_GLOBAL_TR.G_TR_PRIME,
    sma_period=22
)

# Apply to DataFrame
result_df = apply_rule_wave(df, params)
```

## Parameters

### WaveParameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `long1` | int | 339 | First long period |
| `fast1` | int | 10 | First fast period |
| `trend1` | int | 2 | First trend period |
| `tr1` | ENUM_MOM_TR | TR_Fast | First trading rule |
| `long2` | int | 22 | Second long period |
| `fast2` | int | 11 | Second fast period |
| `trend2` | int | 4 | Second trend period |
| `tr2` | ENUM_MOM_TR | TR_Fast | Second trading rule |
| `global_tr` | ENUM_GLOBAL_TR | G_TR_PRIME | Global trading rule |
| `sma_period` | int | 22 | SMA calculation period |

## Trading Rules

### Individual Trading Rules (ENUM_MOM_TR)

- **TR_Fast**: Basic momentum comparison
- **TR_Zone**: Simple zone-based signals
- **TR_StrongTrend**: Strong trend confirmation
- **TR_WeakTrend**: Weak trend signals
- **TR_FastZoneReverse**: Reverse signals in zones
- **TR_BetterTrend**: Enhanced trend signals avoiding false signals
- **TR_BetterFast**: Improved fast trading
- **TR_Rost**: Reverse momentum signals
- **TR_TrendRost**: Trend-based reverse signals
- **TR_BetterTrendRost**: Enhanced trend reverse signals

### Global Trading Rules (ENUM_GLOBAL_TR)

The Global TR Switch combines signals from both wave indicators using sophisticated algorithms:

#### G_TR_PRIME
- **Description**: Basic signal combination
- **Logic**: If both wave indicators agree, use the signal
- **Use Case**: Standard signal validation

#### G_TR_REVERSE
- **Description**: Reverse combined signals
- **Logic**: If both wave indicators agree, reverse the signal
- **Use Case**: Contrarian trading strategies

#### G_TR_PRIME_ZONE
- **Description**: Zone-filtered signal combination
- **Logic**: 
  - BUY signals only in negative zones (wave < 0)
  - SELL signals only in positive zones (wave > 0)
- **Use Case**: Trend-following with zone confirmation

#### G_TR_REVERSE_ZONE
- **Description**: Reversed zone-filtered signals
- **Logic**:
  - BUY signals in negative zones become SELL
  - SELL signals in positive zones become BUY
- **Use Case**: Counter-trend trading with zone validation

#### G_TR_NEW_ZONE
- **Description**: Signal generation on disagreement
- **Logic**: Generate opposite signal when wave indicators disagree
- **Use Case**: Momentum reversal detection

#### G_TR_LONG_ZONE
- **Description**: Continuous opposite signal generation
- **Logic**: Always generate opposite signal to the last confirmed signal
- **Use Case**: Mean reversion strategies

#### G_TR_LONG_ZONE_REVERSE
- **Description**: Continuous same signal generation
- **Logic**: Always use the last confirmed signal
- **Use Case**: Trend continuation strategies

## Functions

### Core Functions

#### `calculate_ecore(div_long, price)`
Calculates ECORE (Energy Core) values based on price series and divisor.

#### `calc_draw_lines(div_fast, div_dir, ecore)`
Calculates wave and fastline series from ECORE values.

#### `tr_switch(tr_rule, wave, fastline, prev_signal, prev_wave)`
Applies individual trading rules to determine buy/sell signals.

### Global TR Switch Functions

#### `global_tr_switch(global_tr, wave1, wave2, fastline1, fastline2, color1, color2)`
Main function that applies global trading rules to combine signals from two wave indicators.

#### `g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)`
Global Prime TR - Uses mix of both wave indicators and generates signals when both agree.

#### `g_reverse_tr(wave1, wave2, fastline1, fastline2, color1, color2)`
Global Reverse TR - Reverses signals when both wave indicators agree.

#### `g_prime_tr_zone(wave1, wave2, fastline1, fastline2, color1, color2)`
Global Prime TR + Zone - Filters signals by zones (BUY in negative, SELL in positive).

#### `g_reverse_tr_zone(wave1, wave2, fastline1, fastline2, color1, color2)`
Global Reverse TR + Zone - Reverses zone-filtered signals.

#### `g_new_zone_tr(wave1, wave2, fastline1, fastline2, color1, color2)`
Global New Zone TR - Generates signals when wave indicators disagree.

#### `g_long_zone_tr(wave1, wave2, fastline1, fastline2, color1, color2)`
Global Long Zone TR - Always generates opposite signal to last confirmed signal.

#### `g_long_zone_reverse_tr(wave1, wave2, fastline1, fastline2, color1, color2)`
Global Long Zone Reverse TR - Always uses the last confirmed signal.

## Output Columns

The indicator adds the following columns to the DataFrame:

- `Wave`: Main wave indicator values
- `Wave_Signal`: Combined trading signals from Global TR Switch
- `Wave_Price_Type`: Price type used for calculation (Open/Close)
- `PPrice1`: Support levels (0.5% below Wave)
- `PColor1`: Support level color (BUY)
- `PPrice2`: Resistance levels (0.5% above Wave)
- `PColor2`: Resistance level color (SELL)
- `Direction`: Trading direction
- `Diff`: Price difference from Wave

## Signal Values

- `BUY` (1.0): Buy signal
- `SELL` (2.0): Sell signal
- `NOTRADE` (0.0): No trade signal

## Advantages

- **Dual Signal Validation**: Two-wave system for improved reliability
- **Flexible Configuration**: Multiple trading rules and filters
- **Strong Trend Identification**: Excellent for trending markets
- **Zone-Based Filtering**: Helps avoid counter-trend trades
- **Momentum Validation**: Advanced signal filtering algorithms
- **Visual Clarity**: Clear color coding and multiple visual elements
- **Comprehensive Signal Types**: Various signal combinations
- **Professional Grade**: Sophisticated algorithms for advanced strategies

## Disadvantages

- **Complex Setup**: Requires extensive parameter testing
- **Lag in Ranging Markets**: May be slow in sideways markets
- **Parameter Sensitivity**: Performance depends heavily on proper settings
- **Resource Intensive**: Multiple calculations may impact performance
- **Learning Curve**: Complex rules require significant study time
- **Over-Optimization Risk**: Multiple parameters increase curve-fitting risk
- **Signal Frequency**: May generate fewer signals than simpler indicators
- **Market Dependency**: Best in trending markets, weaker in ranging conditions

## Best Practices

1. **Parameter Testing**: Test different parameter combinations on historical data
2. **Market Conditions**: Use appropriate global trading rules for different market conditions
3. **Risk Management**: Combine with proper position sizing and stop-loss strategies
4. **Confirmation**: Use with other technical indicators for signal confirmation
5. **Timeframe Selection**: Choose appropriate periods based on trading timeframe

## Example Usage

```python
import pandas as pd
from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters, ENUM_GLOBAL_TR, ENUM_MOM_TR

# Load data
df = pd.read_csv('price_data.csv')

# Configure parameters for trending market
trend_params = WaveParameters(
    long1=339,
    fast1=10,
    trend1=2,
    tr1=ENUM_MOM_TR.TR_StrongTrend,
    long2=22,
    fast2=11,
    trend2=4,
    tr2=ENUM_MOM_TR.TR_Fast,
    global_tr=ENUM_GLOBAL_TR.G_TR_PRIME_ZONE,
    sma_period=22
)

# Apply indicator
result = apply_rule_wave(df, trend_params)

# Get buy signals
buy_signals = result[result['Wave_Signal'] == 1.0]
sell_signals = result[result['Wave_Signal'] == 2.0]

print(f"Buy signals: {len(buy_signals)}")
print(f"Sell signals: {len(sell_signals)}")
```
