# Fibonacci Retracements

## Description

Fibonacci Retracements are a technical analysis tool that uses horizontal lines to indicate areas of support or resistance at the key Fibonacci levels before the price continues in the original direction. These levels are based on the Fibonacci sequence and are commonly used to identify potential reversal points in trending markets.

## Formula

### Fibonacci Levels
```
23.6% = High - (0.236 × (High - Low))
38.2% = High - (0.382 × (High - Low))
50.0% = High - (0.500 × (High - Low))
61.8% = High - (0.618 × (High - Low))
78.6% = High - (0.786 × (High - Low))
```

where:
- `High` - highest point of the swing
- `Low` - lowest point of the swing
- `High - Low` - total range of the swing

### For Downtrend
```
23.6% = Low + (0.236 × (High - Low))
38.2% = Low + (0.382 × (High - Low))
50.0% = Low + (0.500 × (High - Low))
61.8% = Low + (0.618 × (High - Low))
78.6% = Low + (0.786 × (High - Low))
```

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `swing_high` | Swing high price | None | Any positive value |
| `swing_low` | Swing low price | None | Any positive value |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule fibo(100,80,close)
python run_analysis.py yfinance --ticker EURUSD=X --rule fibo(1.2000,1.1800,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate Fibonacci Retracements
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Support and resistance levels
- **23.6% level**: Shallow retracement, strong trend continuation
- **38.2% level**: Moderate retracement, common reversal point
- **50.0% level**: Half retracement, psychological level
- **61.8% level**: Deep retracement, potential trend reversal
- **78.6% level**: Very deep retracement, trend reversal likely

### Trading signals
- **Buy signal**: Price bounces from Fibonacci support level
- **Sell signal**: Price rejects from Fibonacci resistance level
- **Trend continuation**: Price respects Fibonacci levels and continues trend

### Extension levels
- **127.2%**: Extension beyond the swing
- **161.8%**: Golden ratio extension
- **261.8%**: Deep extension level

## Advantages

✅ **Identifies key support/resistance levels**  
✅ **Based on mathematical principles**  
✅ **Works in trending markets**  
✅ **Provides clear entry/exit points**  
✅ **Widely recognized by traders**  

## Disadvantages

❌ **Subjective swing point selection**  
❌ **May not work in sideways markets**  
❌ **Requires trend identification**  
❌ **Can give false signals**  
❌ **Multiple levels may create confusion**  

## Interpretation Examples

### Strong uptrend
In a strong uptrend, price may retrace to 23.6% or 38.2% levels before continuing higher, providing entry opportunities.

### Weak trend
In a weak trend, price may retrace deeper to 61.8% or 78.6% levels, indicating potential trend reversal.

### Multiple timeframes
Fibonacci levels from higher timeframes often provide stronger support/resistance than those from lower timeframes.

## Combined Usage

### With other indicators
- **With RSI**: Fibonacci levels show support/resistance, RSI shows overbought/oversold
- **With Moving Averages**: Fibonacci levels show retracement points, MA shows trend
- **With Volume**: Fibonacci levels show levels, Volume confirms reversals

### Trading strategies
- **Retracement trading**: Buy/sell at Fibonacci levels
- **Trend continuation**: Use Fibonacci levels for entry in trend direction
- **Risk management**: Place stop-loss beyond key Fibonacci levels

## Calculation Features

### Fibonacci sequence
The levels are based on the Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...

### Golden ratio
The 61.8% level is based on the golden ratio (φ ≈ 1.618), which appears frequently in nature and markets.

### Psychological levels
The 50% level is not a true Fibonacci number but is included due to its psychological significance.

## Sources

- [Investopedia - Fibonacci Retracements](https://www.investopedia.com/terms/f/fibonacciretracement.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView Fibonacci Retracements Documentation](https://www.tradingview.com/support/solutions/43000516358-fibonacci-retracements/)

## Related Indicators

- **Pivot Points** - for support/resistance levels
- **Donchian Channels** - for dynamic levels
- **Bollinger Bands** - for volatility-based levels
- **Moving Averages** - for trend-based levels
- **Support/Resistance Lines** - for static levels 