# COT (Commitments of Traders) Indicator

## Overview

**COT (Commitments of Traders)** is a sentiment indicator that analyzes futures market positioning to gauge institutional and large trader sentiment. It is commonly used to confirm trends or spot potential reversals based on the aggregated positions of commercial and non-commercial traders.

- **Category:** Sentiment
- **File:** `src/calculation/indicators/sentiment/cot_ind.py`
- **CLI Rule:** `cot:period,price_type`

## Parameters

| Parameter   | Type   | Description                                      | Default |
|-------------|--------|--------------------------------------------------|---------|
| period      | int    | Calculation period (number of bars)              | 20      |
| price_type  | str    | Price type for calculation: `open` or `close`    | close   |

**Example:**
```
--rule cot:14,close
```

## Calculation Logic

1. **Price Change Calculation:**
   - Calculate percentage change of the selected price series (open/close).
2. **Volume-Weighted Price Change:**
   - For each rolling window of `period` bars:
     - Compute volume-weighted average of price changes (VWAP change).
3. **Volume Momentum:**
   - Calculate mean of volume percentage changes in the window.
4. **Price Momentum:**
   - Calculate mean of price changes in the window.
5. **COT Sentiment:**
   - Combine all factors: `(price_momentum + vwap_change + volume_momentum) / 3`
   - Normalize to 0-100 scale: `cot_index = (tanh(sentiment * 5) + 1) * 50`

## Output Columns

- `COT`: Sentiment value (0-100)
- `COT_Signal`: Trading signal (BUY, SELL, NOTRADE)
- `PPrice1`: Support level (based on sentiment volatility)
- `PPrice2`: Resistance level (based on sentiment volatility)
- `Direction`: Signal direction (numeric)
- `Diff`: Deviation from neutral (COT - 50)

## Visualization (Fastest Mode)

- **Main Line:** COT sentiment (0-100 scale, dark blue)
- **Signal Line:** EMA(9) of COT (orange, dashed)
- **Histogram:** Deviation from signal (green/red bars)
- **Thresholds:**
  - Bullish: 70 (green)
  - Bearish: 30 (red)
  - Neutral: 50 (gray)
- **Support/Resistance:**
  - Calculated as `Open * (1 ± volatility_factor)`

## Interpretation

- **COT > 70:** Strong bullish sentiment (trend confirmation or overbought)
- **COT < 30:** Strong bearish sentiment (trend confirmation or oversold)
- **Crossing 50:** Sentiment shift
- **Divergence:** If price rises but COT falls, possible reversal
- **Flat COT:** Indicates indecision or consolidation

## Best Practices

- Use as a trend confirmation tool: strong COT supports trend direction
- Combine with momentum or trend indicators for robust signals
- Works best on assets with active futures markets
- Adjust period for your timeframe (shorter = more sensitive)

## Integration with Other Indicators

- **Trend:** Combine with EMA, HMA, or MACD to filter signals
- **Momentum:** Use with RSI or Stochastic for confirmation
- **Volatility:** Overlay with ATR or Bollinger Bands to assess risk

## Example CLI Usage

```
uv run run_analysis.py show csv mn1 -d fastest --rule cot:14,close
```

## Example Chart

![COT Example Chart](../../../../results/plots/dual_chart_fastest.html)

## References
- [CFTC Commitments of Traders](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)
- [Investopedia: Commitments of Traders](https://www.investopedia.com/terms/c/cot.asp)
- [Sentiment Indicators in Trading](https://www.investopedia.com/articles/active-trading/061914/using-putcall-ratio-gauge-market-sentiment.asp) 