# On-Balance Volume (OBV)

## Description

On-Balance Volume (OBV) is a volume-based indicator that measures buying and selling pressure by adding volume on up days and subtracting volume on down days. It helps identify whether volume is flowing into or out of a security and can confirm price trends or signal potential reversals.

## Formula

```
OBV = Previous OBV + Current Volume (if Close > Previous Close)
OBV = Previous OBV - Current Volume (if Close < Previous Close)
OBV = Previous OBV (if Close = Previous Close)
```

where:
- `Previous OBV` - OBV value from the previous period
- `Current Volume` - volume for the current period
- `Close` - closing price for current period
- `Previous Close` - closing price from previous period

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule obv(close)
python run_analysis.py yfinance --ticker AAPL --rule obv(open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate OBV
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Trend confirmation
- **Bullish trend**: OBV rising along with price
- **Bearish trend**: OBV falling along with price
- **Trend strength**: Strong correlation between OBV and price movement

### Divergences
- **Bullish divergence**: Price making lower lows while OBV making higher lows
- **Bearish divergence**: Price making higher highs while OBV making lower highs
- **Reversal signal**: Divergence often precedes price reversal

### Volume analysis
- **High volume days**: Significant OBV changes indicate strong conviction
- **Low volume days**: Small OBV changes suggest weak conviction
- **Volume climax**: Extreme OBV movements may signal exhaustion

## Advantages

✅ **Measures buying and selling pressure**  
✅ **Confirms price trends**  
✅ **Identifies potential reversals through divergences**  
✅ **Simple to interpret**  
✅ **Works on all timeframes**  

## Disadvantages

❌ **Can be noisy on intraday charts**  
❌ **Doesn't provide specific entry/exit points**  
❌ **May lag in fast-moving markets**  
❌ **Requires price confirmation**  
❌ **Sensitive to volume data quality**  

## Interpretation Examples

### Strong uptrend
Price and OBV both rising steadily indicates strong buying pressure and confirms the uptrend.

### Weak trend
Price rising but OBV flat or declining suggests weak buying pressure and potential trend reversal.

### Divergence
Price making new highs while OBV making lower highs indicates weakening buying pressure and possible reversal.

## Combined Usage

### With other indicators
- **With RSI**: OBV confirms trend, RSI shows overbought/oversold
- **With MACD**: OBV shows volume flow, MACD shows momentum
- **With Bollinger Bands**: OBV confirms breakouts, BB shows volatility

### Trading strategies
- **Trend confirmation**: Use OBV to confirm price trends
- **Divergence trading**: Trade reversals when OBV diverges from price
- **Volume analysis**: Use OBV to assess conviction behind price moves

## Calculation Features

### Cumulative nature
OBV is cumulative, meaning each value builds upon the previous one, making it sensitive to the starting point.

### Volume weighting
OBV gives equal weight to all volume, regardless of price movement size.

### Zero line
OBV has no fixed zero line, so absolute values are less important than the direction and pattern.

## Sources

- [Investopedia - On-Balance Volume](https://www.investopedia.com/terms/o/onbalancevolume.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView OBV Documentation](https://www.tradingview.com/support/solutions/43000516352-on-balance-volume-obv/)

## Related Indicators

- **VWAP** - Volume Weighted Average Price
- **Accumulation/Distribution Line** - similar volume-based indicator
- **Money Flow Index** - volume-weighted RSI
- **Chaikin Money Flow** - volume-weighted oscillator
- **Volume Rate of Change** - volume momentum indicator 