# Put/Call Ratio Indicator

## Overview

**Put/Call Ratio** is a sentiment indicator that measures the ratio of put options to call options. It is widely used to gauge market sentiment and potential turning points. A high ratio indicates bearish sentiment (more puts than calls), while a low ratio suggests bullish sentiment (more calls than puts).

- **Category:** Sentiment
- **File:** `src/calculation/indicators/sentiment/putcallratio_ind.py`
- **CLI Rule:** `putcallratio:period,price_type`

## Parameters

| Parameter   | Type   | Description                                      | Default |
|-------------|--------|--------------------------------------------------|---------|
| period      | int    | Calculation period (number of bars)              | 20      |
| price_type  | str    | Price type for calculation: `open` or `close`    | close   |

**Example:**
```
--rule putcallratio:20,close
```

## Calculation Logic

1. **Price Change Calculation:**
   - Calculate percentage change of the selected price series (open/close).
2. **Volume Segmentation:**
   - For each rolling window of `period` bars:
     - Sum volume on bars where price change < 0 (bearish volume).
     - Sum volume on bars where price change > 0 (bullish volume).
3. **Put/Call Ratio:**
   - `putcall_ratio = bearish_volume / bullish_volume` (if bullish_volume > 0, else 1.0)
4. **Sentiment Normalization:**
   - Convert ratio to a 0-100 sentiment scale (50 = neutral):
     - `sentiment = 50 + (1 - putcall_ratio) * 25`
     - Values > 50: bullish, < 50: bearish

## Output Columns

- `PutCallRatio`: Sentiment value (0-100)
- `PutCallRatio_Signal`: Trading signal (BUY, SELL, NOTRADE)
- `PPrice1`: Support level (based on sentiment volatility)
- `PPrice2`: Resistance level (based on sentiment volatility)
- `Direction`: Signal direction (numeric)
- `Diff`: Deviation from neutral (PutCallRatio - 50)

## Visualization (Fastest Mode)

- **Main Line:** Put/Call Ratio sentiment (0-100 scale)
- **Signal Line:** Trading signals (BUY/SELL/NOTRADE)
- **Histogram:** Deviation from neutral (Diff)
- **Thresholds:**
  - Bullish: 60
  - Bearish: 40
  - Neutral: 50
- **Support/Resistance:**
  - Calculated as `Open * (1 ± volatility_factor)`

## Interpretation

- **Put/Call Ratio > 60:** Strong bullish sentiment (contrarian: possible overbought)
- **Put/Call Ratio < 40:** Strong bearish sentiment (contrarian: possible oversold)
- **Crossing 50:** Sentiment shift
- **Divergence:** If price rises but Put/Call Ratio falls, possible reversal

## Best Practices

- Use as a contrarian indicator: extreme values often precede reversals
- Combine with trend or momentum indicators for confirmation
- Works best on markets with active options trading
- Adjust period for your timeframe (shorter = more sensitive)

## Integration with Other Indicators

- **Trend:** Combine with moving averages (EMA, HMA) to filter signals
- **Momentum:** Use with RSI or MACD for confirmation
- **Volatility:** Overlay with ATR or Bollinger Bands to assess risk

## Example CLI Usage

```
uv run run_analysis.py show csv mn1 -d fastest --rule putcallratio:20,close
```

## Example Chart

![Put/Call Ratio Example Chart](../../../../results/plots/dual_chart_fastest.html)

## References
- [Investopedia: Put/Call Ratio](https://www.investopedia.com/terms/p/putcallratio.asp)
- [Sentiment Indicators in Trading](https://www.investopedia.com/articles/active-trading/061914/using-putcall-ratio-gauge-market-sentiment.asp) 