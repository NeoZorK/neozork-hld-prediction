# Kelly Criterion Oscillator (Probability)

## Overview

The Kelly Criterion Oscillator is a probability-based indicator that calculates the optimal position size for trading based on the historical win probability and risk/reward ratio. It is visualized in MACD style: main line, signal line (EMA), histogram and threshold levels.

## How It Works

1. **Calculation**: For each point, the indicator computes the percentage price changes over a rolling window (period, e.g., 20 bars).
2. **Win/Loss Analysis**: It counts the number of positive (win) and negative (loss) returns in the window.
3. **Kelly Formula**: Calculates the Kelly fraction:
   
   \[
   f = \frac{bp - q}{b}
   \]
   where:
   - \(b\) = average win / average loss (odds)
   - \(p\) = win probability
   - \(q = 1 - p\) = loss probability

4. **Signal Line**: Exponential moving average (EMA, span=9) of the Kelly line.
5. **Histogram**: Difference between Kelly and signal line.
6. **Thresholds**: 0.1 (10%) — minimum level for signal, 0.25 (25%) — maximum allowed Kelly.

## Output Fields

- **kelly**: Main Kelly line (optimal capital fraction for trade)
- **kelly_signal**: EMA(9) of Kelly (signal line)
- **kelly_histogram**: Difference between Kelly and signal line
- **kelly_threshold_10**: Threshold line 0.1 (10%)
- **kelly_threshold_25**: Threshold line 0.25 (25%)

## Visualization (MACD-style)

- **Blue line**: Kelly fraction (main line)
- **Red line**: Signal line (EMA)
- **Green/Red bars**: Histogram (green — Kelly above signal line, red — below)
- **Orange dashed**: 10% threshold
- **Red dashed**: 25% threshold
- **Gray dashed**: Zero line

## Interpretation

- **Kelly > 0.1**: Signal to increase position (BUY), if line is rising
- **Kelly < 0.1**: Signal to decrease position (SELL), if line is falling
- **Histogram > 0**: Signal strengthening, Kelly above signal line
- **Histogram < 0**: Signal weakening, Kelly below signal line
- **Kelly > 0.25**: Not recommended, too aggressive

## Best Practices

- Use Kelly only with reliable historical data
- Do not exceed 25% Kelly (too high risk)
- Combine with trend filters (e.g., EMA, MACD)
- For volatile markets, reduce period (e.g., 10-15)
- For stable markets, increase period (20-30)
- Use signal line for confirmation

## Example Chart

```mermaid
graph LR
    A[Kelly Line (blue)] -- Above Signal --> B[Histogram (green)]
    A -- Below Signal --> C[Histogram (red)]
    D[Signal Line (red)]
    E[Threshold 0.1 (orange dashed)]
    F[Threshold 0.25 (red dashed)]
    G[Zero Line (gray dashed)]
```

## Integration with Other Indicators

- **MACD**: Use Kelly to filter MACD signals (e.g., only if Kelly > 0.1)
- **RSI**: Do not open trades on Kelly if RSI is in overbought/oversold zone
- **ATR**: Use ATR for dynamic position size management
- **Bollinger Bands**: Kelly can strengthen signals for breaking band boundaries

## References
- Kelly, J. L. (1956). "A New Interpretation of Information Rate". Bell System Technical Journal.
- Investopedia: [Kelly Criterion](https://www.investopedia.com/terms/k/kellycriterion.asp)

---

_Documentation prepared for dual chart fastest mode. All examples and recommendations are relevant only for this mode._ 