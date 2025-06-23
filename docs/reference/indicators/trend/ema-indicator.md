# Exponential Moving Average (EMA)

## Description

Exponential Moving Average (EMA) is a type of moving average that gives greater weight to recent prices compared to older ones. This makes EMA more sensitive to current price changes and faster to react to new trends.

## Formula

```
EMA = (Price × Multiplier) + (Previous EMA × (1 - Multiplier))
```

where:
- `Multiplier = 2 / (Period + 1)`
- `Price` - current price (Open, Close, High, Low or their combination)
- `Previous EMA` - previous EMA value

### Alternative formula
```
EMA = Price × k + EMA(y) × (1 - k)
```

where:
- `k = 2 / (n + 1)` - smoothing coefficient
- `n` - EMA period
- `EMA(y)` - EMA of previous period

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `period` | Period for EMA calculation | 20 | 1-200 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule ema(20,close)
python run_analysis.py yfinance --ticker AAPL --rule ema(50,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate EMA
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Trend signals
- **Uptrend**: Price above EMA
- **Downtrend**: Price below EMA
- **Sideways trend**: Price oscillating around EMA

### Buy/Sell signals
- **Buy signal**: Price crosses EMA from below
- **Sell signal**: Price crosses EMA from above
- **Trend confirmation**: Price remains on one side of EMA

### Multiple EMAs
- **Golden cross**: Short EMA crosses long EMA from below
- **Death cross**: Short EMA crosses long EMA from above

## Advantages

✅ **Quickly responds to price changes**  
✅ **Reduces lag compared to SMA**  
✅ **Good for trend identification**  
✅ **Simple to interpret**  
✅ **Effective for short-term trading**  

## Disadvantages

❌ **Can be more volatile**  
❌ **May give false signals in choppy markets**  
❌ **Sensitive to period choice**  
❌ **Doesn't consider trading volume**  
❌ **May lag in fast reversals**  

## Interpretation Examples

### Strong trend
In a strong uptrend, price remains above EMA and EMA has positive slope. Any pullbacks to EMA can serve as entry points.

### Weak trend
In a weak trend, price often crosses EMA, which can lead to multiple false signals.

### Trend reversal
Trend reversal often begins with price crossing through EMA in the opposite direction.

## Comparison with SMA

| Characteristic | EMA | SMA |
|----------------|-----|-----|
| Sensitivity | High | Low |
| Lag | Less | More |
| Volatility | Higher | Lower |
| False signals | More | Less |
| Suitable for | Short-term trading | Long-term trading |

## Popular periods

- **9 EMA**: Very short-term trend
- **12 EMA**: Short-term trend
- **20 EMA**: Medium-term trend
- **50 EMA**: Long-term trend
- **200 EMA**: Very long-term trend

## Sources

- [Investopedia - Exponential Moving Average](https://www.investopedia.com/terms/e/ema.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView EMA Documentation](https://www.tradingview.com/support/solutions/43000516349-exponential-moving-average-ema/)

## Related Indicators

- **SMA** - simple moving average
- **WMA** - weighted moving average
- **HMA** - Hull Moving Average
- **Bollinger Bands** - use SMA as center line
- **MACD** - based on difference of two EMAs 