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

### CLI Usage

```bash
# Basic Wave with default parameters
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fastest

# Wave with custom trading rules
uv run run_analysis.py demo --rule wave:33,10,2,strongtrend,22,11,4,fast,reverse,22,open -d plotly

# Wave with zone-based filtering
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,primezone,22,open -d fastest

# Wave with fast display mode (Bokeh-based)
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fast

# Wave with real data in fast mode
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fastzonereverse,22,11,4,fast,prime,10,close -d fast

# Get help for wave indicator
uv run run_analysis.py demo --rule wave --help
```

### Programmatic Usage

```python
from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters, ENUM_GLOBAL_TR, ENUM_MOM_TR

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

## CLI Integration

The Wave indicator is fully integrated into the CLI system with comprehensive parameter validation and help support.

### Parameter Format
```
wave:long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type
```

### Trading Rule Values

#### Individual Trading Rules (tr1, tr2)
- `fast` - Basic momentum comparison
- `zone` - Simple zone-based signals
- `strongtrend` - Strong trend confirmation
- `weaktrend` - Weak trend signals
- `fastzonereverse` - Reverse signals in zones
- `bettertrend` - Enhanced trend signals
- `betterfast` - Improved fast trading
- `rost` - Reverse momentum signals
- `trendrost` - Trend-based reverse signals
- `bettertrendrost` - Enhanced trend reverse signals

#### Global Trading Rules (global_tr)
- `prime` - Basic signal combination
- `reverse` - Reverse combined signals
- `primezone` - Zone-filtered signal combination
- `reversezone` - Reversed zone-filtered signals
- `newzone` - Signal generation on disagreement
- `longzone` - Continuous opposite signal generation
- `longzonereverse` - Continuous same signal generation

### Help System
```bash
# Get detailed help for wave indicator
uv run run_analysis.py demo --rule wave --help

# Get help for specific parameter
uv run run_analysis.py demo --rule wave:invalid --help
```

## Display Modes

The Wave indicator supports all display modes with specialized visualization features:

### Fastest Mode (`-d fastest`)
- **Technology**: Plotly-based dual chart
- **Features**: Interactive charts with zoom, pan, and hover
- **Wave Visualization**: Continuous line with dynamic colors
- **Signal Display**: Buy/sell signals on main chart
- **Best For**: Detailed analysis and exploration

### Fast Mode (`-d fast`) ⭐ **NEW**
- **Technology**: Bokeh-based dual chart
- **Features**: Real-time updates and responsive interface
- **Wave Visualization**: Discontinuous lines (only where signals exist)
- **Signal Display**: Color-coded signals (red=BUY, blue=SELL)
- **Hover Tooltips**: Detailed information on hover
- **Best For**: Real-time monitoring and fast analysis

### Other Modes
- **Plotly Mode (`-d plotly`)**: Single chart visualization
- **Matplotlib Mode (`-d mpl`)**: Static charts for reports
- **Seaborn Mode (`-d seaborn`)**: Statistical visualization
- **Terminal Mode (`-d term`)**: Text-based output

### Fast Mode Features
```bash
# Test fast mode with wave indicator
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fastzonereverse,22,11,4,fast,prime,10,close -d fast
```

**Key Fast Mode Advantages:**
- **Discontinuous Wave Lines**: Only displays where signals exist
- **Color-Coded Signals**: Red for BUY, blue for SELL signals
- **Real-Time Updates**: Responsive Bokeh interface
- **Signal Markers**: Clear buy/sell indicators on main chart
- **Hover Information**: Detailed tooltips for analysis

## Best Practices

1. **Parameter Testing**: Test different parameter combinations on historical data
2. **Market Conditions**: Use appropriate global trading rules for different market conditions
3. **Risk Management**: Combine with proper position sizing and stop-loss strategies
4. **Confirmation**: Use with other technical indicators for signal confirmation
5. **Timeframe Selection**: Choose appropriate periods based on trading timeframe
6. **CLI Usage**: Use the built-in help system to understand parameter options

## Example Usage

### CLI Examples

```bash
# Basic Wave analysis with demo data
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fastest

# Wave with strong trend configuration
uv run run_analysis.py demo --rule wave:339,10,2,strongtrend,22,11,4,fast,primezone,22,open -d plotly

# Wave with reverse signals for contrarian strategy
uv run run_analysis.py demo --rule wave:33,10,2,fast,22,11,4,fast,reverse,22,open -d fastest

# Wave with zone-based filtering
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,primezone,22,open -d fastest

# Multiple Wave configurations for comparison
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open,wave:33,10,2,strongtrend,22,11,4,fast,reverse,22,open -d plotly

# Wave with fast display mode for real-time analysis
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fastzonereverse,22,11,4,fast,prime,10,close -d fast

# Compare fast vs fastest modes
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fast
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fastest
```

### Programmatic Examples

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
buy_signals = result[result['_Signal'] == 1.0]
sell_signals = result[result['_Signal'] == 2.0]

print(f"Buy signals: {len(buy_signals)}")
print(f"Sell signals: {len(sell_signals)}")

# Analyze wave values
print(f"Wave1 range: {result['wave1'].min():.2f} to {result['wave1'].max():.2f}")
print(f"Wave2 range: {result['wave2'].min():.2f} to {result['wave2'].max():.2f}")
```
