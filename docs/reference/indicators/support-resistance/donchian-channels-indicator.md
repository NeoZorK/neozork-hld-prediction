# Donchian Channels

## Description

Donchian Channels are a volatility indicator that shows the highest high and lowest low over a specific period. They consist of three lines: the upper channel (highest high), the lower channel (lowest low), and the middle line (average of upper and lower channels). Donchian Channels help identify support and resistance levels and can signal potential breakouts.

## Formula

### Upper Channel
```
Upper Channel = Highest High over n periods
```

### Lower Channel
```
Lower Channel = Lowest Low over n periods
```

### Middle Channel
```
Middle Channel = (Upper Channel + Lower Channel) / 2
```

where:
- `n` - number of periods for calculation
- `Highest High` - maximum high price over the period
- `Lowest Low` - minimum low price over the period

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `period` | Period for calculation | 20 | 5-100 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule donchain(20,close)
python run_analysis.py yfinance --ticker EURUSD=X --rule donchain(14,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate Donchian Channels
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Support and resistance
- **Upper channel**: Dynamic resistance level
- **Lower channel**: Dynamic support level
- **Middle channel**: Dynamic support/resistance level

### Breakout signals
- **Bullish breakout**: Price breaks above upper channel
- **Bearish breakout**: Price breaks below lower channel
- **Breakout confirmation**: Price closes beyond channel

### Channel width
- **Wide channels**: High volatility period
- **Narrow channels**: Low volatility period
- **Channel expansion**: Increasing volatility
- **Channel contraction**: Decreasing volatility

## Advantages

✅ **Shows clear support and resistance levels**  
✅ **Identifies potential breakouts**  
✅ **Measures volatility through channel width**  
✅ **Simple to interpret**  
✅ **Works on all timeframes**  

## Disadvantages

❌ **May lag in fast-moving markets**  
❌ **Can give false breakout signals**  
❌ **Sensitive to period choice**  
❌ **Doesn't show trend direction**  
❌ **May not work well in trending markets**  

## Interpretation Examples

### Sideways market
In a sideways market, price oscillates between upper and lower channels, providing clear entry and exit points.

### Trending market
In a trending market, price may "ride" one of the channels, indicating strong directional movement.

### Breakout
When price breaks above the upper channel or below the lower channel, it may signal the start of a new trend.

## Combined Usage

### With other indicators
- **With RSI**: Donchian Channels show levels, RSI shows overbought/oversold
- **With MACD**: Donchian Channels show breakouts, MACD shows momentum
- **With Volume**: Donchian Channels show levels, Volume confirms breakouts

### Trading strategies
- **Breakout trading**: Enter when price breaks above/below channels
- **Mean reversion**: Trade from channels to middle line
- **Range trading**: Trade within channel boundaries

## Calculation Features

### Rolling calculation
Donchian Channels are calculated on a rolling basis, using a fixed number of periods.

### Channel width
The width of the channels provides insight into market volatility and potential price movements.

### Middle line
The middle line serves as a dynamic support/resistance level and can be used for mean reversion strategies.

## Sources

- [Investopedia - Donchian Channels](https://www.investopedia.com/terms/d/donchianchannels.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView Donchian Channels Documentation](https://www.tradingview.com/support/solutions/43000516357-donchian-channels/)

## Related Indicators

- **Bollinger Bands** - similar volatility indicator
- **Keltner Channels** - use ATR for channel width
- **Price Channels** - alternative channel indicator
- **Pivot Points** - for support/resistance levels
- **Fibonacci Retracements** - for retracement levels 