# Commodity Channel Index (CCI)

## Description

Commodity Channel Index (CCI) is an oscillator that measures the current price level relative to an average price level over a given time period. Originally developed for commodity markets, it is now widely used across all financial markets.

## Formula

```
CCI = (Typical Price - SMA(Typical Price, n)) / (0.015 × Mean Deviation)
```

where:
- `Typical Price = (High + Low + Close) / 3`
- `SMA(Typical Price, n)` - simple moving average of typical price over period n
- `Mean Deviation` - average deviation from SMA
- `0.015` - normalization constant (typically 0.015)

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `period` | Period for CCI calculation | 20 | 5-100 |
| `constant` | Normalization constant | 0.015 | 0.001-0.1 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule cci(20,0.015,close)
python run_analysis.py yfinance --ticker EURUSD=X --rule cci(14,0.02,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate CCI
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Overbought/Oversold levels
- **Overbought**: CCI > +100
- **Oversold**: CCI < -100
- **Strong overbought**: CCI > +200
- **Strong oversold**: CCI < -200

### Buy/Sell signals
- **Buy signal**: CCI crosses -100 from below
- **Sell signal**: CCI crosses +100 from above
- **Strong buy signal**: CCI crosses -200 from below
- **Strong sell signal**: CCI crosses +200 from above

### Divergences
- **Bullish divergence**: Price makes new lows while CCI rises
- **Bearish divergence**: Price makes new highs while CCI falls

## Advantages

✅ **Identifies cyclical trends**  
✅ **Works well for commodity markets**  
✅ **Shows overbought/oversold levels**  
✅ **Effective for short-term trading**  
✅ **Fewer false signals compared to other oscillators**  

## Disadvantages

❌ **Can be volatile**  
❌ **May give false signals in non-cyclical markets**  
❌ **Requires careful parameter tuning**  
❌ **Doesn't consider trading volume**  
❌ **May lag in fast markets**  

## Interpretation Examples

### Cyclical market
CCI is particularly effective in markets with clear cycles, such as commodity markets, where prices tend to revert to the mean.

### Trending market
In a strong trend, CCI may remain in extreme zones for extended periods, which is not necessarily a reversal signal.

### Divergence
If price is rising but CCI doesn't confirm the rise (bearish divergence), it may indicate weakening trend and possible reversal.

## Calculation Features

### Typical price
CCI uses typical price (High + Low + Close) / 3, making it more sensitive to intraday movements.

### Normalization constant
The 0.015 constant ensures that approximately 70-80% of CCI values fall within the -100 to +100 range.

### Mean deviation
Mean Deviation is calculated as the average absolute deviation from SMA, making CCI more robust to outliers.

## Sources

- [Investopedia - Commodity Channel Index](https://www.investopedia.com/terms/c/commoditychannelindex.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView CCI Documentation](https://www.tradingview.com/support/solutions/43000516348-commodity-channel-index-cci/)

## Related Indicators

- **RSI** - another oscillator for overbought/oversold identification
- **Stochastic** - momentum oscillator
- **Williams %R** - inverse oscillator
- **Bollinger Bands** - for volatility identification
- **ATR** - for volatility measurement 