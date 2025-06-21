# Volume Weighted Average Price (VWAP)

## Description

Volume Weighted Average Price (VWAP) is a trading benchmark that gives the average price a security has traded at throughout the day, based on both volume and price. It is important because it provides traders with insight into both the trend and value of a security. VWAP is commonly used by institutional traders to assess whether they received a good price for their trades.

## Formula

```
VWAP = Σ(Price × Volume) / Σ(Volume)
```

where:
- `Price` - typical price for each period (usually (High + Low + Close) / 3)
- `Volume` - volume for each period
- `Σ` - sum over all periods from the start of the day/session

### Alternative Formula
```
VWAP = Σ(Typical Price × Volume) / Σ(Volume)
```

where:
- `Typical Price = (High + Low + Close) / 3`

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule vwap(close)
python run_analysis.py yfinance --ticker AAPL --rule vwap(open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate VWAP
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Price relative to VWAP
- **Above VWAP**: Price is trading above the volume-weighted average
- **Below VWAP**: Price is trading below the volume-weighted average
- **At VWAP**: Price is trading at the volume-weighted average

### Trading signals
- **Buy signal**: Price crosses above VWAP with volume confirmation
- **Sell signal**: Price crosses below VWAP with volume confirmation
- **Support/Resistance**: VWAP often acts as dynamic support/resistance

### Volume analysis
- **High volume**: VWAP is more reliable when volume is high
- **Low volume**: VWAP may be less reliable when volume is low
- **Volume confirmation**: Price moves with volume confirm VWAP signals

## Advantages

✅ **Incorporates both price and volume**  
✅ **Widely used by institutional traders**  
✅ **Provides fair value assessment**  
✅ **Works on intraday timeframes**  
✅ **Good for execution quality analysis**  

## Disadvantages

❌ **Resets daily (for daily VWAP)**  
❌ **May not work well on longer timeframes**  
❌ **Requires volume data**  
❌ **Can be lagging in fast markets**  
❌ **May not work well in low-volume markets**  

## Interpretation Examples

### Strong uptrend
In a strong uptrend, price consistently trades above VWAP, with VWAP acting as support.

### Weak trend
In a weak trend, price may cross VWAP frequently, indicating lack of conviction.

### Volume confirmation
Price moves away from VWAP with high volume often indicate strong directional movement.

## Combined Usage

### With other indicators
- **With RSI**: VWAP shows fair value, RSI shows overbought/oversold
- **With MACD**: VWAP shows trend, MACD shows momentum
- **With Bollinger Bands**: VWAP shows fair value, BB shows volatility

### Trading strategies
- **Mean reversion**: Trade when price deviates significantly from VWAP
- **Trend following**: Use VWAP as dynamic support/resistance
- **Execution quality**: Compare execution price to VWAP

## Calculation Features

### Cumulative calculation
VWAP is calculated cumulatively throughout the day, making it sensitive to the starting point.

### Volume weighting
VWAP gives more weight to periods with higher volume, making it more representative of actual trading activity.

### Typical price
VWAP typically uses the typical price (High + Low + Close) / 3, though closing price can also be used.

## Sources

- [Investopedia - Volume Weighted Average Price](https://www.investopedia.com/terms/v/vwap.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView VWAP Documentation](https://www.tradingview.com/support/solutions/43000516359-volume-weighted-average-price-vwap/)

## Related Indicators

- **OBV** - On-Balance Volume
- **Money Flow Index** - volume-weighted oscillator
- **Chaikin Money Flow** - volume-weighted indicator
- **Accumulation/Distribution Line** - volume-based indicator
- **Volume Rate of Change** - volume momentum indicator 