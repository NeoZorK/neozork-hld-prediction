# Average Directional Index (ADX)

## Description

Average Directional Index (ADX) is a trend indicator that measures the strength of a trend regardless of its direction. ADX doesn't show the direction of the trend, only its strength. Values above 25 typically indicate a strong trend, while values below 20 indicate a weak trend or sideways movement.

## Formula

### True Range (TR)
```
TR = max(High - Low, |High - Previous Close|, |Low - Previous Close|)
```

### Directional Movement (DM)
```
+DM = High - Previous High (if positive, otherwise 0)
-DM = Previous Low - Low (if positive, otherwise 0)
```

### Smoothed Values
```
TR14 = Sum(TR) over 14 periods
+DM14 = Sum(+DM) over 14 periods
-DM14 = Sum(-DM) over 14 periods
```

### Directional Indicators
```
+DI14 = (+DM14 / TR14) × 100
-DI14 = (-DM14 / TR14) × 100
```

### ADX
```
DX = |+DI14 - (-DI14)| / (+DI14 + (-DI14)) × 100
ADX = Average(DX) over 14 periods
```

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `period` | Period for ADX calculation | 14 | 5-50 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule adx(14,close)
python run_analysis.py yfinance --ticker EURUSD=X --rule adx(20,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate ADX
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Trend strength
- **Very weak trend**: ADX < 20
- **Weak trend**: ADX 20-25
- **Strong trend**: ADX 25-50
- **Very strong trend**: ADX > 50
- **Extremely strong trend**: ADX > 75

### Trend direction (via +DI and -DI)
- **Uptrend**: +DI > -DI
- **Downtrend**: -DI > +DI
- **Buy signal**: +DI crosses -DI from below when ADX > 25
- **Sell signal**: -DI crosses +DI from below when ADX > 25

### Divergences
- **Bullish divergence**: Price rises while ADX falls
- **Bearish divergence**: Price falls while ADX rises

## Advantages

✅ **Measures trend strength**  
✅ **Works on all markets**  
✅ **Good for trend confirmation**  
✅ **Helps avoid false signals**  
✅ **Effective for medium-term trading**  

## Disadvantages

❌ **Lagging indicator**  
❌ **May give false signals in volatile markets**  
❌ **Doesn't show trend direction**  
❌ **Requires additional indicators for direction**  
❌ **May be slow in fast reversals**  

## Interpretation Examples

### Strong uptrend
ADX > 25, +DI > -DI, and ADX is rising. This indicates a strong uptrend with increasing strength.

### Weak trend
ADX < 20, +DI and -DI are close to each other. This indicates sideways movement or weak trend.

### Trend reversal
ADX falls from high values while +DI and -DI converge. This may indicate weakening trend and possible reversal.

## Combined Usage

### With other indicators
- **With RSI**: ADX shows trend strength, RSI shows overbought/oversold
- **With MACD**: ADX confirms trend strength, MACD shows direction
- **With Bollinger Bands**: ADX shows trend strength, BB shows volatility

### Trading strategies
- **Trend-following**: Trade only when ADX > 25
- **Counter-trend**: Trade against trend when ADX < 20
- **Breakout**: Enter position when ADX rises above 25

## Sources

- [Investopedia - Average Directional Index](https://www.investopedia.com/terms/a/adx.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView ADX Documentation](https://www.tradingview.com/support/solutions/43000516350-average-directional-index-adx/)

## Related Indicators

- **+DI/-DI** - directional indicators
- **DMI** - Directional Movement Index
- **RSI** - for overbought/oversold identification
- **MACD** - for trend direction identification
- **Bollinger Bands** - for volatility identification 