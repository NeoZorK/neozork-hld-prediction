# Stochastic Oscillator

## Description

Stochastic Oscillator is a momentum indicator that compares a closing price to its price range over a specific period. The indicator oscillates between 0 and 100 and is used to identify overbought and oversold conditions.

## Formula

### %K (Fast Stochastic)
```
%K = ((Close - Lowest Low) / (Highest High - Lowest Low)) × 100
```

### %D (Slow Stochastic)
```
%D = SMA(%K, n)
```

where:
- `Close` - current closing price
- `Lowest Low` - lowest price over K period
- `Highest High` - highest price over K period
- `n` - period for smoothing %D

## Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `k_period` | Period for %K calculation | 14 | 1-100 |
| `d_period` | Period for smoothing %D | 3 | 1-50 |
| `slowing` | Period for smoothing %K | 3 | 1-50 |
| `price_type` | Price type for calculation | 'close' | 'open', 'close' |

## Usage

### CLI command
```bash
python run_analysis.py demo --rule stoch(14,3,3,close)
python run_analysis.py yfinance --ticker AAPL --rule stoch(20,5,5,open)
```

### Programmatic call
```python
from src.calculation.indicator_calculation import calculate_indicator

# Calculate Stochastic Oscillator
result_df = calculate_indicator(args, ohlcv_df, point_size)
```

## Signals

### Overbought/Oversold levels
- **Overbought**: %K > 80 or %D > 80
- **Oversold**: %K < 20 or %D < 20

### Buy/Sell signals
- **Buy signal**: %K crosses %D from below in oversold zone
- **Sell signal**: %K crosses %D from above in overbought zone

### Divergences
- **Bullish divergence**: Price makes new lows while Stochastic doesn't
- **Bearish divergence**: Price makes new highs while Stochastic doesn't

## Advantages

✅ **Identifies overbought/oversold conditions**  
✅ **Shows momentum shifts**  
✅ **Works well in range-bound markets**  
✅ **Simple to interpret**  
✅ **Effective for short-term trading**  

## Disadvantages

❌ **Can give false signals in trending markets**  
❌ **May lag in fast markets**  
❌ **Sensitive to parameter choice**  
❌ **Doesn't consider trading volume**  
❌ **Can stay in extreme zones for extended periods**  

## Interpretation Examples

### Strong trend
In a strong uptrend, Stochastic may remain in overbought zone (>80) for extended periods, which is not necessarily a sell signal.

### Range-bound market
In a range-bound market, Stochastic effectively shows entry and exit levels when reaching extreme values.

### Divergence
If price is rising but Stochastic doesn't confirm the rise (bearish divergence), it may signal a possible trend reversal.

## Sources

- [Investopedia - Stochastic Oscillator](https://www.investopedia.com/terms/s/stochasticoscillator.asp)
- [Technical Analysis of the Financial Markets by John J. Murphy](https://www.amazon.com/Technical-Analysis-Financial-Markets-Comprehensive/dp/0735200661)
- [TradingView Stochastic Documentation](https://www.tradingview.com/support/solutions/43000516347-stochastic-oscillator/)

## Related Indicators

- **RSI** - another oscillator for overbought/oversold identification
- **CCI** - Commodity Channel Index, similar concept
- **Williams %R** - inverse Stochastic Oscillator
- **MACD** - for trend signal confirmation 