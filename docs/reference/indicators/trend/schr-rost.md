# SCHR_ROST Indicator

## Overview

SCHR_ROST (Shcherbyna Rost) is an advanced ADX-based trend prediction indicator designed for trend detection and signal generation. It's based on the MQL5 SCHR_ROST.mq5 indicator by Shcherbyna Rostyslav.

## Key Features

- **Trend Detection**: Excellent for identifying trend direction and strength
- **Multiple Speed Modes**: 12 different speed settings from Snail to Future
- **Fast Reverse Signals**: Optional faster signal reversal for quick market changes
- **ADX-Based**: Built on Average Directional Index calculations
- **Open Price Focus**: Designed to work with Open prices for optimal performance

## Mathematical Foundation

### Core Calculation

The SCHR_ROST indicator uses a sophisticated ADX-based algorithm:

1. **Directional Movement Calculation**:
   - +DM (Plus Directional Movement) = max(price_diff, 0)
   - -DM (Minus Directional Movement) = max(-price_diff, 0)

2. **Smoothing**:
   - Smoothed +DM = ((period - 1) × prev_smoothed_dm + current_dm) / period
   - Smoothed -DM = ((period - 1) × prev_smoothed_dm + current_dm) / period

3. **Directional Indicators**:
   - +DI = (smoothed_+dm / true_range) × 100
   - -DI = (smoothed_-dm / true_range) × 100

4. **DX Calculation**:
   - DX = |+DI - -DI| / (+DI + -DI) × 100

5. **Volatility Index (VI)**:
   - VI = (current_dx - min_dx) / (max_dx - min_dx)

6. **Final Value**:
   - SCHR_ROST = ((period - VI) × prev_value + VI × current_price) / period

### Speed Constants

| Speed Mode | Period Value | Description |
|------------|--------------|-------------|
| Snail      | 1000         | Slowest response |
| Turtle     | 500          | Very slow response |
| Frog       | 200          | Slow response |
| Mouse      | 100          | Moderate-slow response |
| Cat        | 50           | Moderate response |
| Rabbit     | 30           | Moderate-fast response |
| Gepard     | 10           | Fast response |
| Slowest    | 5            | Very fast response |
| Slow       | 2            | Extremely fast response |
| Normal     | 1.01         | Standard response |
| Fast       | 0.683        | Ultra-fast response |
| Future     | 0.501        | Maximum sensitivity |

## Usage

### Basic Usage

```bash
# Basic SCHR_ROST with default settings (Future speed, no faster reverse)
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_ROST
```

### With Parameters

```bash
# SCHR_ROST with custom speed and faster reverse enabled
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_ROST:Future,true

# SCHR_ROST with Normal speed
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_ROST:Normal,false

# SCHR_ROST with Snail speed and faster reverse
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_ROST:Snail,true
```

### Parameter Format

```
SCHR_ROST:speed_period,faster_reverse
```

- **speed_period**: One of the 12 speed modes (Snail, Turtle, Frog, Mouse, Cat, Rabbit, Gepard, Slowest, Slow, Normal, Fast, Future)
- **faster_reverse**: Boolean value (true/false or 1/0) to enable faster signal reversal

## Signal Interpretation

### Direction Values

- **0.0 (NOTRADE)**: No trading signal
- **1.0 (BUY)**: Buy signal - upward trend detected
- **2.0 (SELL)**: Sell signal - downward trend detected

### Signal Generation Logic

1. **Basic Signal**: Based on SCHR_ROST value changes
   - If current_value > previous_value → BUY
   - If current_value < previous_value → SELL
   - If current_value == previous_value → Keep previous signal

2. **Faster Reverse**: When enabled and values are equal
   - Reverses the current signal direction
   - BUY becomes SELL, SELL becomes BUY

3. **Signal Output**: Only generates signals when direction changes

## Trading Strategy

### Recommended Settings

#### Conservative Trading
```bash
SCHR_ROST:Snail,false
```
- Slowest response, minimal noise
- Good for long-term trend following
- Fewer false signals

#### Balanced Trading
```bash
SCHR_ROST:Normal,false
```
- Standard response time
- Good balance between sensitivity and stability
- Suitable for most trading styles

#### Aggressive Trading
```bash
SCHR_ROST:Future,true
```
- Maximum sensitivity
- Fast signal generation
- Higher risk of false signals

### Best Practices

1. **Use with Volume**: Always combine with volume analysis for confirmation
2. **Multiple Timeframes**: Confirm signals across different timeframes
3. **Risk Management**: Use appropriate stop-losses due to potential false signals
4. **Market Conditions**: 
   - Best in trending markets
   - Exercise caution in low volatility (sleep markets)
   - May generate too many signals in choppy markets

## Performance Characteristics

### Strengths

- ✅ Excellent trend detection capability
- ✅ Multiple speed options for different trading styles
- ✅ Fast reverse option for quick market changes
- ✅ Based on proven ADX methodology
- ✅ Works well with Open prices

### Limitations

- ❌ May generate tiny noises (fast reverse signals)
- ❌ Sometimes produces false trend signals (2 out of 10)
- ❌ Too fast signal changes in low volatility markets
- ❌ Requires trend identification for optimal use

## Integration Examples

### With Other Indicators

```bash
# Combine with RSI for confirmation
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_ROST:Normal,false --rule RSI:14,30,70,close

# Combine with MACD for trend confirmation
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_ROST:Future,true --rule MACD:12,26,9,close
```

### Different Data Sources

```bash
# With Binance data
uv run run_analysis.py binance --symbol BTCUSDT --interval 1h --point 0.01 --rule SCHR_ROST:Fast,false

# With Yahoo Finance data
uv run run_analysis.py yfinance --ticker AAPL --period 1y --rule SCHR_ROST:Normal,true
```

## Technical Implementation

### File Location
- **Source**: `src/calculation/indicators/trend/schr_rost_ind.py`
- **Tests**: `tests/calculation/indicators/trend/test_schr_rost_ind.py`

### Key Classes and Functions

- `SCHRRostIndicator`: Main indicator class
- `calculate_schr_rost()`: Core calculation function
- `calculate_schr_rost_signals()`: Signal generation function
- `SpeedEnum`: Speed mode enumeration
- `apply_rule_schr_rost()`: Rule application function

### Dependencies

- pandas: Data manipulation
- numpy: Numerical calculations
- BaseIndicator: Base class for indicators
- TradingRule: Trading rule enumeration

## Troubleshooting

### Common Issues

1. **Too Many Signals**: Reduce speed or disable faster reverse
2. **No Signals**: Increase speed or enable faster reverse
3. **False Signals**: Use in trending markets only, combine with volume analysis
4. **Performance Issues**: Use appropriate speed setting for your timeframe

### Error Messages

- `Invalid speed_period`: Use one of the 12 valid speed modes
- `Invalid faster_reverse`: Use true/false or 1/0
- `Not enough data`: Ensure at least 2 data points are available

## Version History

- **v1.0**: Initial implementation based on MQL5 SCHR_ROST.mq5
- **v1.1**: Added parameter support and CLI integration
- **v1.2**: Enhanced signal generation and faster reverse logic

## References

- Original MQL5 implementation: `mql5_feed/indicators/PREMIUM/SCHR_ROST.mq5`
- Author: Shcherbyna Rostyslav (2018-2022)
- Based on: Average Directional Index (ADX) methodology
