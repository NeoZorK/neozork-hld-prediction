# Time Series Forecast Indicator

## Overview

The Time Series Forecast (TSF) indicator uses linear regression to predict future price movements. It calculates a linear regression line over a specified period and projects it forward to estimate where the price might be heading.

## Formula

```
For each point i:
  Window = Price[i-period:i]
  x = [0, 1, 2, ..., period-1]
  y = Window values
  slope, intercept = linear_regression(x, y)
  TSF[i] = slope × period + intercept
```

Where:
- **linear_regression**: Simple linear regression (y = mx + b)
- **slope**: Rate of change
- **intercept**: Starting value
- **period**: Lookback period for calculation

## Parameters

- **period** (default: 14): Forecast calculation period
- **price_type** (default: close): Price type to use (open/close)

## Usage

### Command Line

```bash
# Basic usage with default parameters
python run_analysis.py demo --rule TSForecast

# Custom parameters
python run_analysis.py demo --rule TSForecast --price-type open

# With specific data source
python run_analysis.py yfinance --ticker AAPL --period 1y --rule TSForecast
```

### Interactive Mode

```bash
python run_analysis.py interactive
# Select TSForecast from the indicator list
```

## Trading Signals

### Buy Signals
- Price is below forecast and forecast is rising
- Price crosses above forecast line
- Forecast slope is positive and increasing

### Sell Signals
- Price is above forecast and forecast is falling
- Price crosses below forecast line
- Forecast slope is negative and decreasing

## Interpretation

### Trend Analysis
- **Bullish Forecast**: Positive slope, price expected to rise
- **Bearish Forecast**: Negative slope, price expected to fall
- **Sideways Forecast**: Near-zero slope, price expected to remain stable

### Price vs Forecast
- **Price Above Forecast**: Potential overvaluation
- **Price Below Forecast**: Potential undervaluation
- **Price Near Forecast**: Fair value

### Momentum
- **Strong Momentum**: Large difference between price and forecast
- **Weak Momentum**: Small difference between price and forecast
- **Momentum Reversal**: Forecast direction changes

## Advantages

- ✅ Provides price predictions
- ✅ Based on statistical methods
- ✅ Good for trend analysis
- ✅ Helps identify potential price targets

## Disadvantages

- ❌ Assumes linear relationships
- ❌ May not work in volatile markets
- ❌ Requires stable trends
- ❌ Can be sensitive to outliers

## Example Output

```
TSForecast: [150.25, 151.34, 152.67, 153.89, 155.12]
TSForecast_Signal: [NOTRADE, NOTRADE, BUY, BUY, BUY]
```

## Related Indicators

- **EMA**: For trend confirmation
- **Bollinger Bands**: For volatility context
- **RSI**: For momentum confirmation
- **MACD**: For trend confirmation

## References

- Technical Analysis of the Financial Markets by John J. Murphy
- Linear Regression Wikipedia: https://en.wikipedia.org/wiki/Linear_regression 