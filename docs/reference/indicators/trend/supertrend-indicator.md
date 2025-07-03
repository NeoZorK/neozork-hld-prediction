# SuperTrend Indicator

## Overview

The SuperTrend indicator is an advanced trend-following technical analysis tool that combines Average True Range (ATR) with price action to identify trend direction and potential reversal points. It provides dynamic support and resistance levels and generates buy/sell signals based on trend changes.

## Features

- **Trend Direction Detection**: Identifies uptrend and downtrend periods
- **Dynamic Support/Resistance**: Provides adaptive support and resistance levels
- **Signal Generation**: Generates buy and sell signals on trend reversals
- **ATR Integration**: Uses Average True Range for volatility-based calculations
- **Dual Chart Visualization**: Displays on dual chart with modern color-coded styling

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `period` | int | Yes | - | ATR period for SuperTrend calculation |
| `multiplier` | float | Yes | - | ATR multiplier for sensitivity adjustment |
| `price_type` | string | No | `close` | Price type to use: `open` or `close` |

## CLI Usage

### Basic Usage (Two Required Parameters)
```bash
# Using close price (default)
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0

# Using open price
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0,open
```

### Parameter Examples
```bash
# Short period, low multiplier (more sensitive)
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:5,2.0

# Long period, high multiplier (less sensitive)
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:50,4.0

# Using open price with custom parameters
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:14,2.5,open
```

## Calculation Method

The SuperTrend indicator calculates dynamic support and resistance levels using the following formula:

1. **ATR Calculation**: Average True Range over the specified period
2. **Basic Upper Band**: `(High + Low) / 2 + (Multiplier × ATR)`
3. **Basic Lower Band**: `(High + Low) / 2 - (Multiplier × ATR)`
4. **Final Upper Band**: Adjusts based on trend direction
5. **Final Lower Band**: Adjusts based on trend direction
6. **SuperTrend Line**: Uses upper band in downtrend, lower band in uptrend

## Signal Generation

### Buy Signal
- Generated when price crosses above the SuperTrend line
- Indicates potential trend reversal from downtrend to uptrend
- SuperTrend line changes from red to green

### Sell Signal
- Generated when price crosses below the SuperTrend line
- Indicates potential trend reversal from uptrend to downtrend
- SuperTrend line changes from green to red

## Visual Representation

### Dual Chart Mode
- **Primary Chart**: OHLC candlesticks with SuperTrend line overlay
- **Secondary Chart**: SuperTrend line with color-coded trend direction
  - **Green**: Uptrend
  - **Red**: Downtrend
  - **Markers**: BUY/SELL signals at trend reversals

### Color Coding
- **Green Line**: Uptrend period
- **Red Line**: Downtrend period
- **Triangle Markers**: Trend reversal signals
- **Semi-transparent**: Enhanced visual appeal

## Parameter Selection Guide

### Period Selection
- **Short Period (5-10)**: More sensitive, more signals, higher noise
- **Medium Period (10-20)**: Balanced sensitivity and signal quality
- **Long Period (20-50)**: Less sensitive, fewer signals, lower noise

### Multiplier Selection
- **Low Multiplier (1.0-2.0)**: Tighter bands, more signals
- **Medium Multiplier (2.0-3.0)**: Balanced sensitivity
- **High Multiplier (3.0-5.0)**: Wider bands, fewer signals

### Price Type Selection
- **Close Price**: Traditional approach, less noise
- **Open Price**: More responsive to gap openings

## Trading Strategy

### Entry Rules
1. **Long Position**: Enter when price crosses above SuperTrend line
2. **Short Position**: Enter when price crosses below SuperTrend line

### Exit Rules
1. **Stop Loss**: Exit when price crosses back through SuperTrend line
2. **Take Profit**: Use additional indicators or fixed targets

### Risk Management
- **Position Sizing**: Based on ATR and account size
- **Stop Loss**: Dynamic based on SuperTrend line
- **Multiple Timeframes**: Confirm signals across different periods

## Performance Metrics

The SuperTrend indicator provides comprehensive trading metrics:

- **Win Ratio**: Percentage of profitable trades
- **Risk/Reward Ratio**: Average profit vs average loss
- **Profit Factor**: Gross profit divided by gross loss
- **Total Return**: Overall strategy performance
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return measure

## Advantages

1. **Trend Following**: Excellent for trending markets
2. **Dynamic Levels**: Adapts to market volatility
3. **Clear Signals**: Binary buy/sell signals
4. **Visual Clarity**: Easy to interpret on charts
5. **Customizable**: Adjustable sensitivity parameters

## Limitations

1. **Lag**: May lag in choppy or sideways markets
2. **False Signals**: Can generate signals in ranging markets
3. **Parameter Sensitivity**: Results vary with parameter selection
4. **Market Conditions**: Works best in trending markets

## Best Practices

1. **Parameter Optimization**: Test different period/multiplier combinations
2. **Market Conditions**: Use in trending markets, avoid in choppy conditions
3. **Confirmation**: Combine with other indicators for signal confirmation
4. **Risk Management**: Always use proper position sizing and stop losses
5. **Multiple Timeframes**: Confirm signals across different timeframes

## Related Indicators

- **ATR**: Used in SuperTrend calculation
- **EMA**: Alternative trend-following indicator
- **ADX**: Trend strength confirmation
- **Bollinger Bands**: Volatility-based support/resistance

## Example Output

```
=== CALCULATED INDICATOR DATA ===
  DateTime   Open   High    Low  Close  PPrice1  PPrice2  Direction
1993-10-01 1.4950 1.5395 1.4700 1.4780 1.351837 1.365423        0.0
1993-11-01 1.4825 1.4981 1.4635 1.4863 1.355349 1.368971        0.0
...

================================================================================
                       UNIVERSAL TRADING METRICS ANALYSIS                       
                                Rule: SUPERTREND                                
                         Generated: 2025-07-03 17:22:30                         
================================================================================

🎯 SIGNAL STATISTICS:
   Buy Signals:       4
   Sell Signals:      4
   No Trade Signals:  375
   Total Signals:     8

💎 CORE TRADING METRICS:
   🎯 Win Ratio:        33.3% 🔴
   ⚖️  Risk/Reward:      2.43 🟢
   💰 Profit Factor:    1.22 🔴
   📈 Total Return:     11.5% 🟡
   💵 Net Return:       2.73% 🔴
   🔄 Total Trades:     8 (Buy: 4, Sell: 4)
```

## Technical Implementation

### File Location
- **Calculation**: `src/calculation/indicators/trend/supertrend_ind.py`
- **CLI Integration**: `src/cli/cli.py`
- **Dual Chart**: `src/plotting/dual_chart_fastest.py`
- **Tests**: `tests/cli/test_supertrend_cli.py`

### Key Functions
- `calculate_supertrend()`: Main calculation function
- `apply_rule_supertrend()`: Trading rule application
- `parse_supertrend_parameters()`: CLI parameter parsing

### Dependencies
- pandas: Data manipulation
- numpy: Numerical calculations
- plotly: Visualization (dual chart mode)

## Version History

- **v2.0.0**: Added SuperTrend indicator with dual chart support
- **v2.0.1**: Enhanced parameter validation and error handling
- **v2.0.2**: Improved visual representation with color-coded trends 