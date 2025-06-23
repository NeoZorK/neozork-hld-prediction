# Pivot Points

## Description

Pivot Points are technical analysis indicators used to determine the overall trend of the market over different time frames. They are calculated using the high, low, and close prices of the previous trading session. Pivot Points provide support and resistance levels that can be used for trading decisions.

## Formula

### Standard Pivot Points
```
Pivot Point (PP) = (High + Low + Close) / 3

Resistance 1 (R1) = (2 × PP) - Low
Resistance 2 (R2) = PP + (High - Low)
Resistance 3 (R3) = High + 2(PP - Low)

Support 1 (S1) = (2 × PP) - High
Support 2 (S2) = PP - (High - Low)
Support 3 (S3) = Low - 2(High - PP)
```

where:
- `High` - highest price of the previous period
- `Low` - lowest price of the previous period
- `Close` - closing price of the previous period

### Fibonacci Pivot Points
```
Pivot Point (PP) = (High + Low + Close) / 3

R1 = PP + 0.382(High - Low)
R2 = PP + 0.618(High - Low)
R3 = PP + 1.000(High - Low)

S1 = PP - 0.382(High - Low)
S2 = PP - 0.618(High - Low)
S3 = PP - 1.000(High - Low)
```

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule pivot(close)
python run_analysis.py yfinance --ticker EURUSD=X --rule pivot(open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate Pivot Points
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Support and resistance levels
- **Pivot Point (PP)**: Primary support/resistance level
- **Resistance 1 (R1)**: First resistance level
- **Resistance 2 (R2)**: Second resistance level
- **Resistance 3 (R3)**: Third resistance level
- **Support 1 (S1)**: First support level
- **Support 2 (S2)**: Second support level
- **Support 3 (S3)**: Third support level

### Trading signals
- **Buy signal**: Price bounces from support level
- **Sell signal**: Price rejects from resistance level
- **Breakout**: Price breaks above resistance or below support

### Trend identification
- **Bullish**: Price above pivot point
- **Bearish**: Price below pivot point
- **Neutral**: Price at pivot point

## Advantages

✅ **Provides clear support/resistance levels**  
✅ **Simple to calculate and interpret**  
✅ **Works on all timeframes**  
✅ **Widely used by traders**  
✅ **Good for day trading**  

## Disadvantages

❌ **Static levels (don't change during session)**  
❌ **May not work well in trending markets**  
❌ **Requires previous session data**  
❌ **Can give false signals in volatile markets**  
❌ **May not work well on longer timeframes**  

## Interpretation Examples

### Sideways market
In a sideways market, price may bounce between support and resistance levels, providing clear entry and exit points.

### Trending market
In a trending market, price may break through pivot levels, indicating strong directional movement.

### Gap openings
When price gaps above or below pivot levels, it may indicate strong momentum in that direction.

## Combined Usage

### With other indicators
- **With RSI**: Pivot Points show levels, RSI shows overbought/oversold
- **With MACD**: Pivot Points show support/resistance, MACD shows momentum
- **With Volume**: Pivot Points show levels, Volume confirms breakouts

### Trading strategies
- **Range trading**: Trade between support and resistance levels
- **Breakout trading**: Enter when price breaks through pivot levels
- **Mean reversion**: Trade from extremes back to pivot point

## Calculation Features

### Daily calculation
Pivot Points are typically calculated daily using the previous day's high, low, and close.

### Multiple timeframes
Pivot Points can be calculated on different timeframes (daily, weekly, monthly).

### Custom periods
Some traders use custom periods (e.g., 4-hour, 8-hour) for pivot point calculations.

## Sources

- [Investopedia - Pivot Points](https://www.investopedia.com/terms/p/pivotpoint.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView Pivot Points Documentation](https://www.tradingview.com/support/solutions/43000516360-pivot-points/)

## Related Indicators

- **Fibonacci Retracements** - for retracement levels
- **Donchian Channels** - for dynamic levels
- **Bollinger Bands** - for volatility-based levels
- **Support/Resistance Lines** - for static levels
- **Moving Averages** - for trend-based levels 