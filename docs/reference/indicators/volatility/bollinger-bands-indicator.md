# Bollinger Bands

## Description

Bollinger Bands is a volatility indicator consisting of three lines: a middle line (usually SMA) and two bands positioned above and below the middle line by a certain number of standard deviations. The bands expand and contract depending on market volatility.

## Formula

### Middle Band
```
Middle Band = SMA(Close, n)
```

### Upper Band
```
Upper Band = Middle Band + (k × Standard Deviation)
```

### Lower Band
```
Lower Band = Middle Band - (k × Standard Deviation)
```

where:
- `n` - period for SMA (usually 20)
- `k` - number of standard deviations (usually 2)
- `Standard Deviation` - standard deviation of prices over period n

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `period` | Period for SMA | 20 | 5-50 |
| `std_dev` | Number of standard deviations | 2 | 1-3 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule bb(20,2,close)
python run_analysis.py yfinance --ticker AAPL --rule bb(14,2.5,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate Bollinger Bands
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Support and resistance levels
- **Upper band**: Dynamic resistance
- **Lower band**: Dynamic support
- **Middle line**: Dynamic support/resistance

### Buy/Sell signals
- **Buy signal**: Price touches or breaks lower band
- **Sell signal**: Price touches or breaks upper band
- **Trend confirmation**: Price remains within bands

### Volatility
- **High volatility**: Bands expand
- **Low volatility**: Bands contract
- **Squeeze**: Bands contract strongly (precursor to strong movement)

### Bounces from bands
- **Bounce from upper band**: Sell signal
- **Bounce from lower band**: Buy signal
- **Band breakout**: Possible continuation of movement

## Advantages

✅ **Shows dynamic support/resistance levels**  
✅ **Measures market volatility**  
✅ **Helps identify overbought/oversold conditions**  
✅ **Effective for short-term trading**  
✅ **Works well in sideways markets**  

## Disadvantages

❌ **May give false signals in trending markets**  
❌ **Doesn't show trend direction**  
❌ **Sensitive to parameter choice**  
❌ **May lag in fast movements**  
❌ **Doesn't consider trading volume**  

## Interpretation Examples

### Sideways market
In a sideways market, price oscillates between upper and lower bands, bouncing off them. These are ideal conditions for trading from levels.

### Trending market
In a strong trend, price may "ride" the upper or lower band, which is not a reversal signal but confirms trend strength.

### Squeeze
When bands contract strongly, it indicates low volatility and foreshadows strong movement in any direction.

## Combined Usage

### With other indicators
- **With RSI**: BB show levels, RSI shows overbought/oversold
- **With MACD**: BB show volatility, MACD shows trend direction
- **With Volume**: BB show levels, Volume shows movement strength

### Trading strategies
- **Mean Reversion**: Trading from bands to middle line
- **Breakout**: Trading on band breakouts
- **Squeeze**: Waiting for breakout after band contraction

## Calculation Features

### Standard deviation
Standard deviation is calculated as:
```
σ = √(Σ(x - μ)² / n)
```
where x is prices, μ is average price, n is period.

### Percent B (%B)
Additional indicator showing price position relative to bands:
```
%B = (Price - Lower Band) / (Upper Band - Lower Band)
```

## Sources

- [Investopedia - Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView Bollinger Bands Documentation](https://www.tradingview.com/support/solutions/43000516351-bollinger-bands/)

## Related Indicators

- **Keltner Channels** - similar indicator using ATR
- **Donchian Channels** - channels based on highs and lows
- **RSI** - for overbought/oversold identification
- **MACD** - for trend direction identification
- **ATR** - for volatility measurement 