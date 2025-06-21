# HMA (Hull Moving Average) Indicator

## Overview

The Hull Moving Average (HMA) is a type of moving average that reduces lag while maintaining smoothness. It was developed by Alan Hull and is designed to be more responsive to recent price changes than traditional moving averages.

## Formula

```
WMA1 = WMA(Price, Period/2)
WMA2 = WMA(Price, Period)
Raw HMA = 2 × WMA1 - WMA2
HMA = WMA(Raw HMA, √Period)
```

Where:
- **WMA**: Weighted Moving Average
- **Period**: The calculation period
- **√Period**: Square root of the period

## Parameters

- **period** (default: 20): HMA calculation period
- **price_type** (default: close): Price type to use (open/close)

## Usage

### Command Line

```bash
# Basic usage with default parameters
python run_analysis.py demo --rule HMA

# Custom parameters
python run_analysis.py demo --rule HMA --price-type open

# With specific data source
python run_analysis.py yfinance --ticker AAPL --period 1y --rule HMA
```

### Interactive Mode

```bash
python run_analysis.py interactive
# Select HMA from the indicator list
```

## Trading Signals

### Buy Signals
- Price crosses above HMA
- HMA is sloping upward
- Price is above HMA and HMA is rising

### Sell Signals
- Price crosses below HMA
- HMA is sloping downward
- Price is below HMA and HMA is falling

## Interpretation

### Trend Analysis
- **Bullish Trend**: Price above HMA and HMA sloping upward
- **Bearish Trend**: Price below HMA and HMA sloping downward
- **Sideways Market**: HMA moving horizontally

### Support/Resistance
- **Dynamic Support**: HMA acts as support in uptrends
- **Dynamic Resistance**: HMA acts as resistance in downtrends

### Momentum
- **Strong Momentum**: Large distance between price and HMA
- **Weak Momentum**: Small distance between price and HMA
- **Momentum Reversal**: Price crosses HMA

## Advantages

- ✅ Reduces lag compared to traditional moving averages
- ✅ Maintains smoothness
- ✅ Good for trend identification
- ✅ More responsive to recent price changes

## Disadvantages

- ❌ Can be more volatile than traditional MAs
- ❌ May give false signals in choppy markets
- ❌ Sensitive to parameter choice
- ❌ May not work well in sideways markets

## Example Output

```
HMA: [150.25, 151.34, 152.67, 153.89, 155.12]
HMA_Signal: [NOTRADE, NOTRADE, BUY, BUY, BUY]
```

## Related Indicators

- **EMA**: For comparison with traditional moving averages
- **Bollinger Bands**: For volatility context
- **RSI**: For momentum confirmation
- **MACD**: For trend confirmation

## References

- Hull Moving Average Wikipedia: https://en.wikipedia.org/wiki/Hull_moving_average
- Technical Analysis of the Financial Markets by John J. Murphy 