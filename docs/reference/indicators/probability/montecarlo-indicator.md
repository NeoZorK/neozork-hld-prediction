# Monte Carlo Oscillator (Probability)

## Overview

The Monte Carlo Oscillator is a probability-based indicator that uses random sampling (Monte Carlo simulation) to estimate the distribution of possible future price movements. It is designed to help traders assess the likelihood of different price scenarios and to visualize the probabilistic forecast as an oscillator, similar in style to MACD.

## How It Works

1. **Simulation**: For each point in the price series, the indicator runs multiple (e.g., 1000) random simulations of future price paths, based on the historical mean and standard deviation of returns.
2. **Forecast**: The median of all simulated end-prices is used as the Monte Carlo forecast for that point.
3. **Signal Line**: An Exponential Moving Average (EMA) of the forecast (default period: 9) is calculated, serving as a "signal line" (like in MACD).
4. **Histogram**: The difference between the forecast and the signal line is plotted as a histogram, highlighting the momentum and direction of the probabilistic forecast.
5. **Confidence Bands**: Upper and lower confidence bands are calculated using the rolling standard deviation of the forecast, scaled by a z-score (default: 1.96 for 95% confidence).
6. **Signals**: Buy and sell signals are generated based on crossovers between the forecast and the signal line, and the relationship between the current price and the forecast.

## Fields Explained

- **montecarlo**: The main Monte Carlo forecast (median of simulated future prices for each point).
- **montecarlo_signal**: The signal line, calculated as an EMA of the forecast. It smooths the forecast and helps identify trend changes.
- **montecarlo_histogram**: The difference between the forecast and the signal line. Positive values indicate upward momentum, negative values indicate downward momentum.
- **montecarlo_upper**: The upper confidence band, representing the upper bound of the forecast's 95% confidence interval.
- **montecarlo_lower**: The lower confidence band, representing the lower bound of the forecast's 95% confidence interval.
- **MonteCarlo_Signal_Line**: The trading signal (BUY, SELL, NOTRADE) based on crossovers and price/forecast relationships.
- **PPrice1 / PPrice2**: Support and resistance levels, set to the lower and upper confidence bands, respectively.
- **PColor1 / PColor2**: Colors for support/resistance (BUY/SELL).
- **Direction**: The same as MonteCarlo_Signal_Line, for compatibility with plotting.
- **Diff**: The difference between the actual price and the forecast (can be used as a divergence indicator).

## Visualization (MACD Style)

- **Main Line (Blue)**: Monte Carlo forecast ("montecarlo").
- **Signal Line (Red)**: EMA of the forecast ("montecarlo_signal").
- **Histogram (Green/Red Bars)**: Difference between forecast and signal line ("montecarlo_histogram").
- **Confidence Bands (Light Blue Dashed)**: Upper and lower confidence intervals ("montecarlo_upper", "montecarlo_lower").
- **Zero Line (Gray Dashed)**: Reference for histogram.
- **Buy/Sell Signals**: Generated when the forecast crosses the signal line and price is below/above forecast.

## Interpretation

- **Forecast above Signal Line**: Indicates a probabilistic upward trend; histogram is green.
- **Forecast below Signal Line**: Indicates a probabilistic downward trend; histogram is red.
- **Wide Confidence Bands**: High uncertainty/volatility in forecast.
- **Narrow Confidence Bands**: High confidence/low volatility in forecast.
- **Buy Signal**: Forecast crosses above signal line and price is below forecast.
- **Sell Signal**: Forecast crosses below signal line and price is above forecast.

## Example Output

| Date       | Price | montecarlo | montecarlo_signal | montecarlo_histogram | montecarlo_upper | montecarlo_lower | Signal |
|------------|-------|------------|------------------|----------------------|------------------|------------------|--------|
| 2024-01-01 | 1.100 | 1.120      | 1.115            | 0.005                | 1.140            | 1.100            | BUY    |
| 2024-01-02 | 1.105 | 1.118      | 1.116            | 0.002                | 1.138            | 1.098            | NOTRADE|
| 2024-01-03 | 1.110 | 1.115      | 1.117            | -0.002               | 1.135            | 1.095            | SELL   |

## Usage

```bash
uv run run_analysis.py show csv mn1 -d fastest --rule monte:100,252
```

## Best Practices

### Parameter Selection
- **Simulations**: Use 1000+ simulations for stable results. More simulations = more accurate but slower computation.
- **Period**: 252 (trading days) for annual forecast, 20 for short-term, 60 for medium-term.
- **Signal Period**: 9 (default) works well for most timeframes.

### Signal Interpretation
- **Strong Buy**: Forecast crosses above signal line + price below forecast + narrow confidence bands.
- **Strong Sell**: Forecast crosses below signal line + price above forecast + narrow confidence bands.
- **Weak Signal**: Wide confidence bands indicate high uncertainty - wait for confirmation.
- **False Signals**: Avoid trading when confidence bands are very wide (high volatility periods).

### Risk Management
- **Position Sizing**: Reduce position size when confidence bands are wide.
- **Stop Loss**: Use lower confidence band as dynamic stop loss for long positions.
- **Take Profit**: Use upper confidence band as dynamic take profit for long positions.
- **Divergence**: Monitor the "Diff" field for price-forecast divergence.

### Market Conditions
- **Trending Markets**: Monte Carlo performs best in trending markets with clear direction.
- **Sideways Markets**: Expect more false signals and wider confidence bands.
- **High Volatility**: Increase simulation count and be more conservative with position sizing.

## Integration with Other Indicators

### Complementary Indicators
- **RSI**: Use RSI to confirm overbought/oversold conditions when Monte Carlo signals occur.
- **MACD**: Compare Monte Carlo histogram with MACD histogram for trend confirmation.
- **Bollinger Bands**: Use BB width to confirm volatility levels shown by confidence bands.
- **ATR**: Use ATR to validate the volatility assumptions in Monte Carlo calculations.

### Confirmation Strategy
1. **Primary Signal**: Monte Carlo forecast crosses signal line.
2. **Price Confirmation**: Price is below/above forecast as expected.
3. **Volatility Check**: Confidence bands are not excessively wide.
4. **Volume Confirmation**: High volume on signal days increases reliability.

### Divergence Analysis
- **Bullish Divergence**: Price makes lower lows while Monte Carlo forecast makes higher lows.
- **Bearish Divergence**: Price makes higher highs while Monte Carlo forecast makes lower highs.
- **Histogram Divergence**: Monitor histogram pattern vs price action for early trend reversal signals.

## Example Charts

### Bullish Setup
```
Price:     ▲▲▲▲▲▲▲▲▲▲
Forecast:  ▲▲▲▲▲▲▲▲▲▲
Signal:    ▲▲▲▲▲▲▲▲▲▲
Histogram: ██████████ (Green bars)
Signal:    BUY (Forecast crosses above signal)
```

### Bearish Setup
```
Price:     ▼▼▼▼▼▼▼▼▼▼
Forecast:  ▼▼▼▼▼▼▼▼▼▼
Signal:    ▼▼▼▼▼▼▼▼▼▼
Histogram: ██████████ (Red bars)
Signal:    SELL (Forecast crosses below signal)
```

### High Uncertainty Period
```
Price:     ▲▼▲▼▲▼▲▼▲▼
Forecast:  ▲▼▲▼▲▼▲▼▲▼
Signal:    ▲▼▲▼▲▼▲▼▲▼
Histogram: ████░░░░░░ (Mixed colors)
Confidence: ██████████ (Wide bands)
Signal:    NOTRADE (Avoid trading)
```

## Performance Tips

### Computational Optimization
- Use fewer simulations (500-1000) for real-time analysis.
- Use more simulations (2000+) for backtesting and research.
- Consider using GPU acceleration for large datasets.

### Memory Management
- Monte Carlo calculations can be memory-intensive for large datasets.
- Consider chunking data for very long time series.
- Use appropriate data types (float32 vs float64) based on precision needs.

### Real-time Usage
- Pre-calculate Monte Carlo values for common timeframes.
- Use caching for repeated calculations.
- Implement incremental updates for new data points.

## References
- [Monte Carlo Method (Wikipedia)](https://en.wikipedia.org/wiki/Monte_Carlo_method)
- [MACD Oscillator (Investopedia)](https://www.investopedia.com/terms/m/macd.asp)
- [Financial Risk Management by Philippe Jorion](https://www.amazon.com/Financial-Risk-Management-Handbook-Professionals/dp/0471786227) 