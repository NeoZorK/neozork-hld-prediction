# Stochastic Oscillator Indicator

## Overview

The Stochastic Oscillator is a momentum indicator that compares a closing price to its price range over a specific period. It consists of two lines:

- **%K Line**: The raw stochastic value
- **%D Line**: A smoothed version of %K (usually a 3-period SMA)

## Formula

```
%K = ((Close - Lowest Low) / (Highest High - Lowest Low)) × 100
%D = SMA(%K, 3)
```

Where:
- **Close**: Current closing price
- **Lowest Low**: Lowest low over the lookback period
- **Highest High**: Highest high over the lookback period

## Parameters

- **k_period** (default: 14): Period for %K calculation
- **d_period** (default: 3): Period for %D smoothing
- **slowing** (default: 3): Smoothing period for %K
- **price_type** (default: close): Price type to use (open/close)

## Usage

### Command Line

```bash
# Basic usage with default parameters
python run_analysis.py demo --rule StochOscillator

# Custom parameters
python run_analysis.py demo --rule StochOscillator --price-type open

# With specific data source
python run_analysis.py yfinance --ticker AAPL --period 1y --rule StochOscillator
```

### Interactive Mode

```bash
python run_analysis.py interactive
# Select StochOscillator from the indicator list
```

## Trading Signals

### Buy Signals
- %K crosses above %D from oversold levels (below 20)
- %K and %D both rise from oversold territory

### Sell Signals
- %K crosses below %D from overbought levels (above 80)
- %K and %D both fall from overbought territory

## Interpretation

### Overbought/Oversold Levels
- **Overbought**: Values above 80 (potential sell signal)
- **Oversold**: Values below 20 (potential buy signal)
- **Neutral**: Values between 20 and 80

### Divergence
- **Bullish Divergence**: Price makes lower lows while Stochastic makes higher lows
- **Bearish Divergence**: Price makes higher highs while Stochastic makes lower highs

### Momentum
- **Strong Momentum**: %K and %D moving in the same direction
- **Weak Momentum**: %K and %D moving in opposite directions
- **Momentum Reversal**: %K and %D cross over

## Advantages

- ✅ Identifies overbought/oversold conditions effectively
- ✅ Shows momentum shifts clearly
- ✅ Good for range-bound markets
- ✅ Helps identify potential reversals

## Disadvantages

- ❌ Can give false signals in trending markets
- ❌ May lag in fast markets
- ❌ Sensitive to parameter choice
- ❌ May stay overbought/oversold for extended periods

## Example Output

```
StochOsc_K: [25.5, 32.1, 45.8, 67.2, 78.9]
StochOsc_D: [28.3, 34.2, 48.1, 65.4, 76.2]
StochOsc_Signal: [NOTRADE, NOTRADE, BUY, NOTRADE, SELL]
```

## Related Indicators

- **RSI**: For additional momentum confirmation
- **MACD**: For trend confirmation
- **Bollinger Bands**: For volatility context
- **CCI**: For additional oscillator confirmation

## References

- Technical Analysis of the Financial Markets by John J. Murphy
- Stochastic Oscillator Wikipedia: https://en.wikipedia.org/wiki/Stochastic_oscillator 