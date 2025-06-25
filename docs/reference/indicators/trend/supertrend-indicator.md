# SuperTrend

## Description

SuperTrend is a trend-following indicator that shows dynamic support and resistance levels. It consists of a line that follows the price and changes color based on the trend direction. SuperTrend is designed to provide clear trend signals and can be used for both entry/exit decisions and stop-loss placement.

## Formula

### Basic ATR Calculation
```
TR = max(High - Low, |High - Previous Close|, |Low - Previous Close|)
ATR = Average(TR) over n periods
```

### SuperTrend Calculation
```
Basic Upper Band = (High + Low) / 2 + (Multiplier × ATR)
Basic Lower Band = (High + Low) / 2 - (Multiplier × ATR)
```

### Final SuperTrend
- **For uptrend**: SuperTrend = Basic Lower Band
- **For downtrend**: SuperTrend = Basic Upper Band

### Trend Direction
- **Uptrend**: Price above SuperTrend
- **Downtrend**: Price below SuperTrend

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `period` | Period for ATR calculation | 10 | 5-50 |
| `multiplier` | ATR multiplier | 3 | 1-5 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule supertrend(10,3,close)
python run_analysis.py yfinance --ticker BTCUSDT --rule supertrend(14,2.5,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate SuperTrend
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Trend direction
- **Uptrend**: SuperTrend line below price (typically green)
- **Downtrend**: SuperTrend line above price (typically red)
- **Trend reversal**: SuperTrend line switches sides

### Entry/Exit signals
- **Buy signal**: Price crosses above SuperTrend line
- **Sell signal**: Price crosses below SuperTrend line
- **Stop-loss**: SuperTrend line serves as dynamic stop-loss

### Support/Resistance
- **Support**: SuperTrend acts as support in uptrend
- **Resistance**: SuperTrend acts as resistance in downtrend
- **Dynamic levels**: Support/resistance levels adjust with volatility

## Advantages

✅ **Shows clear trend direction**  
✅ **Provides dynamic stop-loss levels**  
✅ **Works well in trending markets**  
✅ **Adapts to market volatility**  
✅ **Good for risk management**  

## Disadvantages

❌ **Can give false signals in sideways markets**  
❌ **May lag in fast markets**  
❌ **Sensitive to parameter settings**  
❌ **Doesn't work well in choppy markets**  
❌ **May result in whipsaws in volatile conditions**  

## Interpretation Examples

### Strong trend
In a strong trend, SuperTrend follows price closely, providing effective support/resistance and clear trend direction.

### Volatile market
In volatile markets, SuperTrend may generate frequent signals as it adapts to changing volatility levels.

### Trend reversal
When SuperTrend line switches sides, it often signals a trend reversal, though confirmation from other indicators is recommended.

## Combined Usage

### With other indicators
- **With RSI**: SuperTrend shows direction, RSI shows overbought/oversold
- **With MACD**: SuperTrend confirms trend, MACD shows momentum
- **With Volume**: SuperTrend shows levels, Volume confirms conviction

### Trading strategies
- **Trend following**: Use SuperTrend for trend direction and stop-loss
- **Breakout trading**: Enter when price breaks above/below SuperTrend
- **Risk management**: Use SuperTrend as trailing stop-loss

## Calculation Features

### ATR-based volatility
SuperTrend uses ATR to adapt to market volatility, making it more responsive in volatile markets and less sensitive in quiet markets.

### Dynamic bands
The basic bands are calculated using the midpoint of high and low prices, adjusted by ATR multiplier.

### Trend persistence
SuperTrend maintains its position until price crosses it, providing trend continuity.

## Sources

- [Investopedia - SuperTrend](https://www.investopedia.com/terms/s/supertrend.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView SuperTrend Documentation](https://www.tradingview.com/support/solutions/43000516354-supertrend/)

## Related Indicators

- **Parabolic SAR** - similar trend-following indicator
- **ATR** - for volatility measurement
- **Bollinger Bands** - for volatility context
- **Moving Averages** - for trend direction
- **ADX** - for trend strength confirmation 