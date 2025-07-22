# Parameterized Indicators

This guide explains how to use parameterized indicators in the NeoZorK HLD Prediction tool.

## Overview

The tool now supports parameterized indicator rules in the format `indicator:param1,param2,param3,param4`. This allows you to specify custom parameters for technical indicators directly in the command line.

## Basic Syntax

```bash
--rule indicator:param1,param2,param3,param4
```

Where:
- `indicator` is the indicator name (e.g., `rsi`, `macd`, `ema`)
- `param1,param2,param3,param4` are the specific parameters for that indicator
- Parameters are separated by commas
- No spaces around the colon or commas

## Supported Indicators and Parameters

### RSI (Relative Strength Index)
```bash
--rule rsi:period,oversold,overbought,price_type
```

**Parameters:**
- `period` (int): RSI calculation period (default: 14)
- `oversold` (float): Oversold threshold (default: 30)
- `overbought` (float): Overbought threshold (default: 70)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default RSI settings
uv run run_analysis.py show csv mn1 gbp --rule rsi -d fastest

# Custom RSI with open prices
uv run run_analysis.py show csv mn1 gbp --rule rsi:14,30,70,open -d fastest

# Custom RSI with different thresholds
uv run run_analysis.py show csv mn1 gbp --rule rsi:21,25,75,close -d fastest
```

### MACD (Moving Average Convergence Divergence)
```bash
--rule macd:fast_period,slow_period,signal_period,price_type
```

**Parameters:**
- `fast_period` (int): Fast EMA period (default: 12)
- `slow_period` (int): Slow EMA period (default: 26)
- `signal_period` (int): Signal line period (default: 9)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default MACD settings
uv run run_analysis.py show csv mn1 gbp --rule macd -d fastest

# Custom MACD with open prices
uv run run_analysis.py show csv mn1 gbp --rule macd:8,21,5,open -d fastest
```

### Stochastic

> **Note:** `stoch`, `stochastic`, and `stochoscillator` are exact synonyms. No matter which name you use, the CLI will always process and display the rule as `stoch:...`.

```bash
--rule stoch:k_period,d_period,price_type
--rule stochastic:k_period,d_period,price_type
--rule stochoscillator:k_period,d_period,price_type
```

**Parameters:**
- `k_period` (int): %K period (default: 14)
- `d_period` (int): %D period (default: 3)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# All these commands are equivalent and will be processed as stoch:14,3,close
uv run run_analysis.py show csv mn1 gbp --rule stoch:14,3,close -d fastest
uv run run_analysis.py show csv mn1 gbp --rule stochastic:14,3,close -d fastest
uv run run_analysis.py show csv mn1 gbp --rule stochoscillator:14,3,close -d fastest

# Custom Stochastic with open prices (all aliases work identically)
uv run run_analysis.py show csv mn1 gbp --rule stoch:14,3,open -d fastest
uv run run_analysis.py show csv mn1 gbp --rule stochastic:14,3,open -d fastest
uv run run_analysis.py show csv mn1 gbp --rule stochoscillator:14,3,open -d fastest
```

> **Result:**
> Regardless of which alias you use, the CLI will always show and process the rule as `stoch:...` in all logs, help, and reports.

### EMA (Exponential Moving Average)
```bash
--rule ema:period,price_type
```

**Parameters:**
- `period` (int): EMA period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default EMA settings
uv run run_analysis.py show csv mn1 gbp --rule ema -d fastest

# Custom EMA with open prices
uv run run_analysis.py show csv mn1 gbp --rule ema:20,open -d fastest
```

### Bollinger Bands
```bash
--rule bb:period,std_dev,price_type
```

**Parameters:**
- `period` (int): Moving average period (default: 20)
- `std_dev` (float): Standard deviation multiplier (default: 2.0)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default Bollinger Bands settings
uv run run_analysis.py show csv mn1 gbp --rule bb -d fastest

# Custom Bollinger Bands with open prices
uv run run_analysis.py show csv mn1 gbp --rule bb:20,2.5,open -d fastest
```

### ATR (Average True Range)
```bash
--rule atr:period
```

**Parameters:**
- `period` (int): ATR period (default: 14)

**Examples:**
```bash
# Default ATR settings
uv run run_analysis.py show csv mn1 gbp --rule atr -d fastest

# Custom ATR period
uv run run_analysis.py show csv mn1 gbp --rule atr:21 -d fastest
```

### CCI (Commodity Channel Index)
```bash
--rule cci:period,price_type
```

**Parameters:**
- `period` (int): CCI period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default CCI settings
uv run run_analysis.py show csv mn1 gbp --rule cci -d fastest

# Custom CCI with open prices
uv run run_analysis.py show csv mn1 gbp --rule cci:20,open -d fastest
```

### VWAP (Volume Weighted Average Price)
```bash
--rule vwap:price_type
```

**Parameters:**
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default VWAP settings
uv run run_analysis.py show csv mn1 gbp --rule vwap -d fastest

# VWAP with open prices
uv run run_analysis.py show csv mn1 gbp --rule vwap:open -d fastest
```

### Pivot Points
```bash
--rule pivot:price_type
```

**Parameters:**
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default Pivot Points settings
uv run run_analysis.py show csv mn1 gbp --rule pivot -d fastest

# Pivot Points with open prices
uv run run_analysis.py show csv mn1 gbp --rule pivot:open -d fastest
```

### HMA (Hull Moving Average)
```bash
--rule hma:period,price_type
```

**Parameters:**
- `period` (int): HMA period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default HMA settings
uv run run_analysis.py show csv mn1 gbp --rule hma -d fastest

# Custom HMA with open prices
uv run run_analysis.py show csv mn1 gbp --rule hma:20,open -d fastest
```

### TSF (Time Series Forecast)

> **Note:** `tsf` and `tsforecast` are exact synonyms. No matter which name you use, the CLI will always process and display the rule as `tsf:...`.

```bash
--rule tsf:period,price_type
--rule tsforecast:period,price_type
```

**Parameters:**
- `period` (int): TSF period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# All these commands are equivalent and will be processed as tsf:20,close
uv run run_analysis.py show csv mn1 gbp --rule tsf:20,close -d fastest
uv run run_analysis.py show csv mn1 gbp --rule tsforecast:20,close -d fastest
```

### Monte Carlo Simulation

> **Note:** `monte`, `montecarlo`, and `mc` are exact synonyms. No matter which name you use, the CLI will always process and display the rule as `monte:...`.

```bash
--rule monte:simulations,period
--rule montecarlo:simulations,period
--rule mc:simulations,period
```

**Parameters:**
- `simulations` (int): Number of simulations (default: 1000)
- `period` (int): Simulation period (default: 252)

**Examples:**
```bash
# All these commands are equivalent and will be processed as monte:1000,252
uv run run_analysis.py show csv mn1 gbp --rule monte:1000,252 -d fastest
uv run run_analysis.py show csv mn1 gbp --rule montecarlo:1000,252 -d fastest
uv run run_analysis.py show csv mn1 gbp --rule mc:1000,252 -d fastest
```

### Kelly Criterion
```bash
--rule kelly:period
```

**Parameters:**
- `period` (int): Kelly period (default: 20)

**Examples:**
```bash
# Default Kelly settings
uv run run_analysis.py show csv mn1 gbp --rule kelly -d fastest

# Custom Kelly period
uv run run_analysis.py show csv mn1 gbp --rule kelly:20 -d fastest
```

### Put/Call Ratio
```bash
--rule putcallratio:period,price_type
```

**Parameters:**
- `period` (int): Put/Call ratio period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default Put/Call Ratio settings
uv run run_analysis.py show csv mn1 gbp --rule putcallratio -d fastest

# Custom Put/Call Ratio with open prices
uv run run_analysis.py show csv mn1 gbp --rule putcallratio:20,open -d fastest
```

### COT (Commitment of Traders)
```bash
--rule cot:period,price_type
```

**Parameters:**
- `period` (int): COT calculation period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default COT settings
uv run run_analysis.py show csv mn1 gbp --rule cot -d fastest

# Custom COT with open prices
uv run run_analysis.py show csv mn1 gbp --rule cot:20,open -d fastest
```

### Fear & Greed

> **Note:** `feargreed` and `fg` are exact synonyms. No matter which name you use, the CLI will always process and display the rule as `feargreed:...`.

```bash
--rule feargreed:period,price_type
--rule fg:period,price_type
```

**Parameters:**
- `period` (int): Fear & Greed period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# All these commands are equivalent and will be processed as feargreed:20,close
uv run run_analysis.py show csv mn1 gbp --rule feargreed:20,close -d fastest
uv run run_analysis.py show csv mn1 gbp --rule fg:20,close -d fastest
```

### Fibonacci Retracements
```bash
--rule fibo:level1,level2,level3,... or --rule fibo:all
```

**Parameters:**
- `level1,level2,level3,...` (float): Custom Fibonacci retracement levels (default: 0.236,0.382,0.618)
- `all`: Use all standard Fibonacci levels (0.236,0.382,0.5,0.618,0.786)

**Examples:**
```bash
# Default Fibonacci settings (0.236, 0.382, 0.618)
uv run run_analysis.py show csv mn1 gbp --rule fibo -d fastest

# Use all standard Fibonacci levels
uv run run_analysis.py show csv mn1 gbp --rule fibo:all -d fastest

# Custom Fibonacci levels
uv run run_analysis.py show csv mn1 gbp --rule fibo:0.236,0.382,0.5,0.618,0.786 -d fastest

# Minimal levels for aggressive trading
uv run run_analysis.py show csv mn1 gbp --rule fibo:0.236,0.618 -d fastest

# Extended levels for conservative trading
uv run run_analysis.py show csv mn1 gbp --rule fibo:0.236,0.382,0.5,0.618,0.786,0.886 -d fastest
```

**Signal Generation:**
- **Buy Signals**: Price crosses above support levels or near support with upward momentum
- **Sell Signals**: Price crosses below resistance levels or near resistance with downward momentum
- **Balanced**: Improved algorithm provides equal buy/sell signal opportunities

### OBV (On-Balance Volume)
```bash
--rule obv
```

**Parameters:**
- None required

**Examples:**
```bash
# OBV (no parameters needed)
uv run run_analysis.py show csv mn1 gbp --rule obv -d fastest
```

### Standard Deviation
```bash
--rule stdev:period,price_type
```

**Parameters:**
- `period` (int): Standard deviation period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default Standard Deviation settings
uv run run_analysis.py show csv mn1 gbp --rule stdev -d fastest

# Custom Standard Deviation with open prices
uv run run_analysis.py show csv mn1 gbp --rule stdev:20,open -d fastest
```

### ADX (Average Directional Index)
```bash
--rule adx:period
```

**Parameters:**
- `period` (int): ADX period (default: 14)

**Examples:**
```bash
# Default ADX settings
uv run run_analysis.py show csv mn1 gbp --rule adx -d fastest

# Custom ADX period
uv run run_analysis.py show csv mn1 gbp --rule adx:14 -d fastest
```

### SAR (Parabolic SAR)
```bash
--rule sar:acceleration,maximum
```

**Parameters:**
- `acceleration` (float): Acceleration factor (default: 0.02)
- `maximum` (float): Maximum acceleration (default: 0.2)

**Examples:**
```bash
# Default SAR settings
uv run run_analysis.py show csv mn1 gbp --rule sar -d fastest

# Custom SAR parameters
uv run run_analysis.py show csv mn1 gbp --rule sar:0.02,0.2 -d fastest
```

### SuperTrend
```bash
--rule supertrend:period,multiplier[,price_type]
```

**Parameters:**
- `period` (int): ATR period for SuperTrend calculation (required)
- `multiplier` (float): ATR multiplier (required)
- `price_type` (string): Price type for calculation - `open` or `close` (optional, default: close)

**Examples:**
```bash
# SuperTrend with required parameters
uv run run_analysis.py show csv mn1 gbp --rule supertrend:10,3.0 -d fastest

# SuperTrend with optional price type
uv run run_analysis.py show csv mn1 gbp --rule supertrend:10,3.0,open -d fastest
```

### Bollinger Bands
```bash
--rule bb:period,std_dev,price_type
```

**Parameters:**
- `period` (int): Moving average period (default: 20)
- `std_dev` (float): Standard deviation multiplier (default: 2.0)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default Bollinger Bands settings
uv run run_analysis.py show csv mn1 gbp --rule bb -d fastest

# Custom Bollinger Bands with open prices
uv run run_analysis.py show csv mn1 gbp --rule bb:20,2.5,open -d fastest
```

### ATR (Average True Range)
```bash
--rule atr:period
```

**Parameters:**
- `period` (int): ATR period (default: 14)

**Examples:**
```bash
# Default ATR settings
uv run run_analysis.py show csv mn1 gbp --rule atr -d fastest

# Custom ATR period
uv run run_analysis.py show csv mn1 gbp --rule atr:21 -d fastest
```

### Standard Deviation
```bash
--rule stdev:period,price_type
```

**Parameters:**
- `period` (int): Standard deviation period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default Standard Deviation settings
uv run run_analysis.py show csv mn1 gbp --rule stdev -d fastest

# Custom Standard Deviation with open prices
uv run run_analysis.py show csv mn1 gbp --rule stdev:20,open -d fastest
```

### OBV (On-Balance Volume)
```bash
--rule obv
```

**Parameters:**
- None required

**Examples:**
```bash
# OBV (no parameters needed)
uv run run_analysis.py show csv mn1 gbp --rule obv -d fastest
```

### VWAP (Volume Weighted Average Price)
```bash
--rule vwap:price_type
```

**Parameters:**
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default VWAP settings
uv run run_analysis.py show csv mn1 gbp --rule vwap -d fastest

# VWAP with open prices
uv run run_analysis.py show csv mn1 gbp --rule vwap:open -d fastest
```

### HMA (Hull Moving Average)
```bash
--rule hma:period,price_type
```

**Parameters:**
- `period` (int): HMA period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# Default HMA settings
uv run run_analysis.py show csv mn1 gbp --rule hma -d fastest

# Custom HMA with open prices
uv run run_analysis.py show csv mn1 gbp --rule hma:20,open -d fastest
```

### TSF (Time Series Forecast)

> **Note:** `tsf` and `tsforecast` are exact synonyms. No matter which name you use, the CLI will always process and display the rule as `tsf:...`.

```bash
--rule tsf:period,price_type
--rule tsforecast:period,price_type
```

**Parameters:**
- `period` (int): TSF period (default: 20)
- `price_type` (string): Price type for calculation - `open` or `close` (default: close)

**Examples:**
```bash
# All these commands are equivalent and will be processed as tsf:20,close
uv run run_analysis.py show csv mn1 gbp --rule tsf:20,close -d fastest
uv run run_analysis.py show csv mn1 gbp --rule tsforecast:20,close -d fastest
```

## Error Handling

The system provides clear error messages for invalid parameter formats:

```bash
# Invalid parameter count
uv run run_analysis.py show csv mn1 gbp --rule rsi:14,30,70 -d fastest
# Error: RSI requires exactly 4 parameters: period,oversold,overbought,price_type. Got: 14,30,70

# Invalid price type
uv run run_analysis.py show csv mn1 gbp --rule rsi:14,30,70,high -d fastest
# Error: RSI price_type must be 'open' or 'close', got: high

# Invalid format
uv run run_analysis.py show csv mn1 gbp --rule rsi:14,30,70:open -d fastest
# Error: Invalid rule format: rsi:14,30,70:open

# SuperTrend missing required parameters
uv run run_analysis.py show csv mn1 gbp --rule supertrend:10 -d fastest
# Error: SuperTrend requires exactly 2-3 parameters: period,multiplier[,price_type]. Got: 10

# SuperTrend invalid price type
uv run run_analysis.py show csv mn1 gbp --rule supertrend:10,3.0,high -d fastest
# Error: SuperTrend price_type must be 'open' or 'close', got: high
```

## Best Practices

1. **Use Default Values**: If you don't need custom parameters, use the simple format: `--rule rsi`

2. **Price Type Consistency**: Be consistent with price type usage across your analysis

3. **Parameter Validation**: Always check the parameter requirements for each indicator

4. **Whitespace**: Avoid spaces around the colon and commas in parameter strings

5. **Testing**: Test your parameterized rules with small datasets first

## Compatibility

Parameterized indicators are compatible with all data sources:
- CSV files
- Yahoo Finance
- Binance
- Exchange Rate API
- MQL5 data

## Examples with Different Data Sources

```bash
# CSV file with parameterized RSI
uv run run_analysis.py csv --csv-file data.csv --point 0.01 --rule rsi:14,30,70,open -d fastest

# Yahoo Finance with parameterized MACD
uv run run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule macd:8,21,5,close -d fastest

# Binance with parameterized EMA
uv run run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule ema:20,open -d fastest

# CSV file with SuperTrend
uv run run_analysis.py csv --csv-file data.csv --point 0.01 --rule supertrend:10,3.0 -d fastest

# Yahoo Finance with SuperTrend
uv run run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule supertrend:14,2.5,open -d fastest
```

## Migration from Old Format

If you were using the old format with separate arguments, you can now use the parameterized format:

**Old format:**
```