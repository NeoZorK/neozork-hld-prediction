# Parabolic SAR (SAR)

## Description

Parabolic SAR (Stop and Reverse) is a trend-following indicator that shows potential reversal points in price trends. It appears as a series of dots placed above or below the price chart, with the dots switching sides when a trend reversal occurs. SAR is particularly useful for setting trailing stop-loss levels and identifying trend direction.

## Formula

### For Uptrend (SAR below price)
```
SAR = Previous SAR + AF × (EP - Previous SAR)
```

### For Downtrend (SAR above price)
```
SAR = Previous SAR + AF × (EP - Previous SAR)
```

where:
- `AF` - Acceleration Factor (starts at 0.02, increases by 0.02 each time EP reaches new extreme)
- `EP` - Extreme Point (highest high for uptrend, lowest low for downtrend)
- `SAR` - Stop and Reverse level

### Constraints
- SAR cannot be placed beyond the previous period's high/low
- AF has a maximum value (typically 0.20)

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `acceleration` | Initial acceleration factor | 0.02 | 0.01-0.1 |
| `maximum` | Maximum acceleration factor | 0.20 | 0.1-0.5 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule sar(0.02,0.2,close)
python run_analysis.py yfinance --ticker EURUSD=X --rule sar(0.01,0.15,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate SAR
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Trend direction
- **Uptrend**: SAR dots below price
- **Downtrend**: SAR dots above price
- **Trend reversal**: SAR dots switch from above to below price (or vice versa)

### Stop-loss levels
- **Trailing stop**: SAR provides dynamic stop-loss levels
- **Exit signal**: Price crossing SAR indicates trend reversal
- **Risk management**: SAR helps manage position risk

### Entry signals
- **Buy signal**: SAR dots switch from above to below price
- **Sell signal**: SAR dots switch from below to above price
- **Trend confirmation**: SAR direction confirms trend

## Advantages

✅ **Shows trend reversals clearly**  
✅ **Provides trailing stop-loss levels**  
✅ **Works well in trending markets**  
✅ **Simple to interpret**  
✅ **Good for risk management**  

## Disadvantages

❌ **Can give false signals in sideways markets**  
❌ **May lag in fast markets**  
❌ **Sensitive to parameter settings**  
❌ **Doesn't work well in choppy markets**  
❌ **May result in frequent whipsaws**  

## Interpretation Examples

### Strong trend
In a strong trend, SAR follows price closely, providing effective trailing stops and clear trend direction.

### Sideways market
In a sideways market, SAR may generate frequent false signals as dots switch sides frequently.

### Trend reversal
When SAR dots switch sides, it often signals a trend reversal, though confirmation from other indicators is recommended.

## Combined Usage

### With other indicators
- **With ADX**: SAR shows direction, ADX shows trend strength
- **With RSI**: SAR shows reversals, RSI shows overbought/oversold
- **With MACD**: SAR confirms trend changes, MACD shows momentum

### Trading strategies
- **Trend following**: Use SAR for trend direction and stop-loss
- **Breakout trading**: Enter when SAR confirms trend change
- **Risk management**: Use SAR as trailing stop-loss

## Calculation Features

### Acceleration factor
AF starts at 0.02 and increases by 0.02 each time the extreme point is reached, up to the maximum value.

### Extreme points
For uptrends, EP is the highest high since the trend began. For downtrends, EP is the lowest low.

### SAR constraints
SAR cannot be placed beyond the previous period's high or low, ensuring it stays within reasonable bounds.

## Sources

- [Investopedia - Parabolic SAR](https://www.investopedia.com/terms/p/parabolic-sar.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView SAR Documentation](https://www.tradingview.com/support/solutions/43000516353-parabolic-sar/)

## Related Indicators

- **SuperTrend** - similar trend-following indicator
- **ADX** - for trend strength confirmation
- **Moving Averages** - for trend direction
- **Bollinger Bands** - for volatility context
- **ATR** - for volatility measurement 