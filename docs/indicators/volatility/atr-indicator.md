# Average True Range (ATR)

## Description

Average True Range (ATR) is a volatility indicator that measures market volatility by decomposing the entire range of an asset price for a specific period. ATR does not indicate price direction, but rather the degree of price volatility. It is commonly used to set stop-loss levels and determine position sizing.

## Formula

### True Range (TR)
```
TR = max(High - Low, |High - Previous Close|, |Low - Previous Close|)
```

### Average True Range (ATR)
```
ATR = Average(TR) over n periods
```

where:
- `High` - current period's high
- `Low` - current period's low
- `Previous Close` - previous period's closing price
- `n` - number of periods for averaging

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `period` | Period for ATR calculation | 14 | 5-50 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule atr(14,close)
python run_analysis.py yfinance --ticker EURUSD=X --rule atr(20,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate ATR
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Volatility measurement
- **High volatility**: ATR values are high
- **Low volatility**: ATR values are low
- **Volatility expansion**: ATR rising
- **Volatility contraction**: ATR falling

### Stop-loss placement
- **Dynamic stop-loss**: Use ATR multiplier for stop-loss distance
- **Position sizing**: Adjust position size based on ATR
- **Risk management**: ATR helps determine appropriate risk levels

### Market conditions
- **Trending market**: ATR may be elevated
- **Sideways market**: ATR may be lower
- **Breakout potential**: Low ATR may precede volatility expansion

## Advantages

✅ **Measures market volatility accurately**  
✅ **Helps with stop-loss placement**  
✅ **Useful for position sizing**  
✅ **Works on all timeframes**  
✅ **Not affected by price direction**  

## Disadvantages

❌ **Doesn't show price direction**  
❌ **May lag in fast-moving markets**  
❌ **Requires interpretation for trading decisions**  
❌ **Sensitive to period choice**  
❌ **May not work well in all market conditions**  

## Interpretation Examples

### High volatility period
High ATR values indicate increased market volatility, suggesting wider stop-losses and potentially larger price movements.

### Low volatility period
Low ATR values indicate decreased market volatility, suggesting tighter stop-losses and potentially smaller price movements.

### Volatility expansion
When ATR rises from low levels, it may indicate the start of a trending move or increased market activity.

## Combined Usage

### With other indicators
- **With SuperTrend**: ATR provides volatility context for SuperTrend bands
- **With Bollinger Bands**: ATR shows volatility, BB shows price levels
- **With Moving Averages**: ATR shows volatility, MA shows trend

### Trading strategies
- **Volatility breakout**: Trade when ATR expands from low levels
- **Risk management**: Use ATR for stop-loss placement
- **Position sizing**: Adjust position size inversely to ATR

## Calculation Features

### True Range components
TR considers three scenarios:
1. Current high minus current low
2. Current high minus previous close
3. Current low minus previous close

### Smoothing
ATR is typically smoothed using a simple moving average, though exponential moving average can also be used.

### Absolute values
ATR is always positive and measured in the same units as price.

## Sources

- [Investopedia - Average True Range](https://www.investopedia.com/terms/a/atr.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView ATR Documentation](https://www.tradingview.com/support/solutions/43000516355-average-true-range-atr/)

## Related Indicators

- **Bollinger Bands** - use standard deviation for volatility
- **SuperTrend** - uses ATR for band calculation
- **Keltner Channels** - use ATR for channel width
- **Standard Deviation** - alternative volatility measure
- **Volatility Ratio** - compares current to historical volatility 