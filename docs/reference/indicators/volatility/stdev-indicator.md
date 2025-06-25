# Standard Deviation

## Description

Standard Deviation is a statistical measure of price volatility that shows how much prices deviate from their average value. It is a key component of many technical indicators, including Bollinger Bands, and helps traders understand the volatility characteristics of a security.

## Formula

```
Standard Deviation = √(Σ(x - μ)² / n)
```

where:
- `x` - individual price values
- `μ` - mean (average) price over the period
- `n` - number of periods
- `Σ` - sum of all values

### Rolling Standard Deviation
```
Rolling StdDev = √(Σ(Price - SMA)² / Period)
```

where:
- `SMA` - Simple Moving Average over the period
- `Period` - number of periods for calculation

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `period` | Period for calculation | 20 | 5-100 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule stdev(20,close)
python run_analysis.py yfinance --ticker AAPL --rule stdev(14,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate Standard Deviation
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Volatility measurement
- **High volatility**: High standard deviation values
- **Low volatility**: Low standard deviation values
- **Volatility expansion**: Standard deviation rising
- **Volatility contraction**: Standard deviation falling

### Market conditions
- **Trending market**: Standard deviation may be elevated
- **Sideways market**: Standard deviation may be lower
- **Breakout potential**: Low standard deviation may precede volatility expansion

### Statistical significance
- **Normal distribution**: About 68% of values within ±1 standard deviation
- **Wide distribution**: About 95% of values within ±2 standard deviations
- **Extreme values**: About 99.7% of values within ±3 standard deviations

## Advantages

✅ **Measures price dispersion accurately**  
✅ **Statistical foundation**  
✅ **Works on all timeframes**  
✅ **Not affected by price direction**  
✅ **Key component of other indicators**  

## Disadvantages

❌ **Doesn't show price direction**  
❌ **May lag in fast-moving markets**  
❌ **Requires interpretation for trading decisions**  
❌ **Sensitive to period choice**  
❌ **Assumes normal distribution**  

## Interpretation Examples

### High volatility period
High standard deviation values indicate increased price dispersion, suggesting higher risk and potentially larger price movements.

### Low volatility period
Low standard deviation values indicate decreased price dispersion, suggesting lower risk and potentially smaller price movements.

### Volatility expansion
When standard deviation rises from low levels, it may indicate the start of a trending move or increased market activity.

## Combined Usage

### With other indicators
- **With Bollinger Bands**: Standard deviation determines band width
- **With Moving Averages**: Standard deviation shows volatility around MA
- **With ATR**: Standard deviation shows statistical volatility, ATR shows true range

### Trading strategies
- **Volatility breakout**: Trade when standard deviation expands from low levels
- **Risk assessment**: Use standard deviation to assess potential price movements
- **Position sizing**: Adjust position size based on volatility levels

## Calculation Features

### Statistical properties
Standard deviation measures the square root of the average squared deviation from the mean, providing a measure of dispersion.

### Rolling calculation
Standard deviation is typically calculated on a rolling basis, using a fixed number of periods.

### Normalization
Standard deviation is measured in the same units as price, making it easy to interpret.

## Sources

- [Investopedia - Standard Deviation](https://www.investopedia.com/terms/s/standarddeviation.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView Standard Deviation Documentation](https://www.tradingview.com/support/solutions/43000516356-standard-deviation/)

## Related Indicators

- **Bollinger Bands** - use standard deviation for band width
- **ATR** - alternative volatility measure
- **Keltner Channels** - use ATR for channel width
- **Volatility Ratio** - compares current to historical volatility
- **Price Channels** - use standard deviation for channel boundaries 