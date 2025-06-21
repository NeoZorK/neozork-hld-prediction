# MACD (Moving Average Convergence Divergence) Indicator

## Overview

The MACD (Moving Average Convergence Divergence) is a trend-following momentum indicator that shows the relationship between two moving averages of a price. It consists of three components:

- **MACD Line**: The difference between a fast EMA and a slow EMA
- **Signal Line**: An EMA of the MACD line
- **Histogram**: The difference between the MACD line and the signal line

## Formula

```
MACD Line = Fast EMA - Slow EMA
Signal Line = EMA(MACD Line)
Histogram = MACD Line - Signal Line
```

## Parameters

- **fast_period** (default: 12): Period for the fast EMA
- **slow_period** (default: 26): Period for the slow EMA  
- **signal_period** (default: 9): Period for the signal line EMA
- **price_type** (default: close): Price type to use (open/close)

## Usage

### Command Line

```bash
# Basic usage with default parameters
python run_analysis.py demo --rule MACD

# Custom parameters
python run_analysis.py demo --rule MACD --price-type open

# With specific data source
python run_analysis.py yfinance --ticker AAPL --period 1y --rule MACD
```

### Interactive Mode

```bash
python run_analysis.py interactive
# Select MACD from the indicator list
```

## Trading Signals

### Buy Signals
- MACD line crosses above the signal line (bullish crossover)
- MACD line is above the signal line and both are above zero

### Sell Signals  
- MACD line crosses below the signal line (bearish crossover)
- MACD line is below the signal line and both are below zero

## Interpretation

### Trend Analysis
- **Bullish Trend**: MACD line above signal line and both above zero
- **Bearish Trend**: MACD line below signal line and both below zero
- **Sideways Market**: MACD line and signal line oscillating around zero

### Divergence
- **Bullish Divergence**: Price makes lower lows while MACD makes higher lows
- **Bearish Divergence**: Price makes higher highs while MACD makes lower highs

### Momentum
- **Strong Momentum**: Large histogram bars
- **Weak Momentum**: Small histogram bars
- **Momentum Reversal**: Histogram bars change direction

## Advantages

- ✅ Identifies trend changes effectively
- ✅ Shows momentum shifts clearly
- ✅ Good for trend confirmation
- ✅ Widely used and recognized

## Disadvantages

- ❌ Lagging indicator
- ❌ Can give false signals in sideways markets
- ❌ Sensitive to parameter choice
- ❌ May miss quick reversals

## Example Output

```
MACD_Line: [-0.123, -0.098, -0.045, 0.012, 0.089]
MACD_Signal: [-0.145, -0.123, -0.098, -0.067, -0.023]
MACD_Histogram: [0.022, 0.025, 0.053, 0.079, 0.112]
MACD_Trading_Signal: [NOTRADE, NOTRADE, BUY, BUY, BUY]
```

## Related Indicators

- **RSI**: For overbought/oversold confirmation
- **Bollinger Bands**: For volatility context
- **EMA**: For trend confirmation
- **Stochastic**: For momentum confirmation

## References

- Technical Analysis of the Financial Markets by John J. Murphy
- MACD Wikipedia: https://en.wikipedia.org/wiki/MACD 