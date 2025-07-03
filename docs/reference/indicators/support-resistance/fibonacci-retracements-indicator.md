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
| `levels` | Fibonacci retracement levels | [0.236, 0.382, 0.618] | Any float values between 0 and 1 |
| `period` | Swing calculation period | 20 | Any positive integer |

## Usage

### CLI Commands

#### Basic Usage
```bash
# Use default Fibonacci levels
uv run run_analysis.py show csv mn1 -d fastest --rule fibo

# Use all standard Fibonacci levels
uv run run_analysis.py show csv mn1 -d fastest --rule fibo:all

# Use custom Fibonacci levels
uv run run_analysis.py show csv mn1 -d fastest --rule fibo:0.236,0.5,0.786

# Use multiple custom levels
uv run run_analysis.py show csv mn1 -d fastest --rule fibo:0.236,0.382,0.5,0.618,0.786
```

#### Examples with Different Data Sources
```bash
# Yahoo Finance data
uv run run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 --rule fibo:all -d fastest

# Binance data
uv run run_analysis.py binance --symbol BTCUSDT --interval 1h --point 0.01 --rule fibo:0.236,0.618 -d fastest

# CSV file
uv run run_analysis.py csv --csv-file data.csv --point 0.01 --rule fibo:0.236,0.5,0.786 -d fastest
```

### Programmatic Usage
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate Fibonacci Retracements with custom levels
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signal Generation

### Buy Signals
- **Price crosses above support levels**: When price moves above 61.8%, 38.2%, or 23.6% levels
- **Price near support with momentum**: When price is within 0.5% of support levels and showing upward momentum

### Sell Signals
- **Price crosses below resistance levels**: When price moves below 23.6%, 38.2%, or 61.8% levels
- **Price near resistance with downward momentum**: When price is within 0.5% of resistance levels and showing downward momentum

### Signal Logic
```python
# Buy conditions
buy_condition_618 = (price > fib_618) & (price.shift(1) <= fib_618.shift(1))
buy_condition_382 = (price > fib_382) & (price.shift(1) <= fib_382.shift(1))
buy_condition_236 = (price > fib_236) & (price.shift(1) <= fib_236.shift(1))

# Sell conditions
sell_condition_236 = (price < fib_236) & (price.shift(1) >= fib_236.shift(1))
sell_condition_382 = (price < fib_382) & (price.shift(1) >= fib_382.shift(1))
sell_condition_618 = (price < fib_618) & (price.shift(1) >= fib_618.shift(1))
```

## Trading Strategy

### Support and Resistance Levels
- **23.6% level**: Shallow retracement, strong trend continuation
- **38.2% level**: Moderate retracement, common reversal point
- **50.0% level**: Half retracement, psychological level
- **61.8% level**: Deep retracement, potential trend reversal
- **78.6% level**: Very deep retracement, trend reversal likely

### Trading Rules
- **Buy signal**: Price bounces from Fibonacci support level
- **Sell signal**: Price rejects from Fibonacci resistance level
- **Trend continuation**: Price respects Fibonacci levels and continues trend

### Extension Levels
- **127.2%**: Extension beyond the swing
- **161.8%**: Golden ratio extension
- **261.8%**: Deep extension level

## Advantages

✅ **Identifies key support/resistance levels**  
✅ **Based on mathematical principles**  
✅ **Works in trending markets**  
✅ **Provides clear entry/exit points**  
✅ **Widely recognized by traders**  
✅ **Customizable levels for different strategies**  
✅ **Supports multiple timeframes**  

## Disadvantages

❌ **Subjective swing point selection**  
❌ **May not work in sideways markets**  
❌ **Requires trend identification**  
❌ **Can give false signals**  
❌ **Multiple levels may create confusion**  

## Best Practices

### Level Selection
- **Conservative**: Use 23.6%, 38.2%, 61.8% for major levels
- **Aggressive**: Add 50% and 78.6% for more opportunities
- **Custom**: Create levels specific to your trading strategy

### Timeframe Considerations
- **Higher timeframes**: More reliable signals, fewer false breaks
- **Lower timeframes**: More signals, higher noise
- **Multiple timeframes**: Confirm signals across different periods

### Risk Management
- **Stop Loss**: Place below/above key Fibonacci levels
- **Take Profit**: Use next Fibonacci level as target
- **Position Sizing**: Reduce size when multiple levels cluster

## Interpretation Examples

### Strong Uptrend
In a strong uptrend, price may retrace to 23.6% or 38.2% levels before continuing higher, providing entry opportunities.

### Weak Trend
In a weak trend, price may retrace deeper to 61.8% or 78.6% levels, indicating potential trend reversal.

### Multiple Timeframes
Fibonacci levels from higher timeframes often provide stronger support/resistance than those from lower timeframes.

## Combined Usage

### With Other Indicators
- **With RSI**: Fibonacci levels show support/resistance, RSI shows overbought/oversold
- **With Moving Averages**: Fibonacci levels show retracement points, MA shows trend
- **With Volume**: Fibonacci levels show levels, Volume confirms reversals

### Trading Strategies
- **Retracement trading**: Buy/sell at Fibonacci levels
- **Trend continuation**: Use Fibonacci levels for entry in trend direction
- **Risk management**: Place stop-loss beyond key Fibonacci levels

## Calculation Features

### Fibonacci Sequence
The levels are based on the Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...

### Golden Ratio
The 61.8% level is based on the golden ratio (φ ≈ 1.618), which appears frequently in nature and markets.

### Psychological Levels
The 50% level is not a true Fibonacci number but is included due to its psychological significance.

## Performance Metrics

### Signal Distribution
- **Buy Signals**: Generated when price crosses above support levels
- **Sell Signals**: Generated when price crosses below resistance levels
- **Signal Balance**: Improved algorithm provides balanced buy/sell signals

### Risk Metrics
- **Win Ratio**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profit to gross loss
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return measure

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