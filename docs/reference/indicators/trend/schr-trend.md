# SCHR_TREND Indicator

## Overview

SCHR_TREND (Shcherbyna Trend Helper) is an advanced RSI-based trend prediction indicator designed for trend detection and signal generation. It's based on the MQL5 SCHR_Trend.mq5 indicator by Shcherbyna Rostyslav.

## Key Features

- **Trend Detection**: Excellent for identifying trend direction and strength
- **Multiple Trading Rule Modes**: 10 different trading rule modes for various strategies
- **Purchase Power Analysis**: Advanced analysis using multiple RSI periods
- **RSI-Based**: Built on Relative Strength Index calculations
- **Open Price Focus**: Designed to work with Open prices for optimal performance
- **Extreme Signal Detection**: Identifies overbought/oversold conditions

## Mathematical Foundation

### Core Calculation

The SCHR_TREND indicator uses a sophisticated RSI-based algorithm:

1. **RSI Calculation**:
   - RSI = 100 - (100 / (1 + RS))
   - RS = Average Gain / Average Loss
   - Uses specified period for smoothing

2. **Trading Rule Modes**:
   - **First Classic**: >95 Sell, <5 Buy
   - **First Trend**: >95 Buy, <5 Sell
   - **Trend**: Best Up 70| Down 30 with trend continuation
   - **Zone**: >50 Buy, <50 Sell with extreme detection
   - **First Zone**: Include New Extreme Signals
   - **First Strong Zone**: Without New Extreme Signals
   - **Purchase Power**: 10 indicators analysis
   - **Purchase Power by Count**: Count-based analysis
   - **Purchase Power Extreme**: Only extreme signals
   - **Purchase Power Weak**: Weak signal analysis

3. **Signal Generation**:
   - **0.0 (NOTRADE)**: No trading signal
   - **1.0 (BUY)**: Buy signal - upward trend detected
   - **2.0 (SELL)**: Sell signal - downward trend detected
   - **3.0 (DBL_BUY)**: Double buy signal - strong upward trend
   - **4.0 (DBL_SELL)**: Double sell signal - strong downward trend

### Purchase Power Calculation

For Purchase Power modes, the indicator calculates 10 RSI values with periods:
- Period 1: `period * 1`
- Period 2: `period * 2`
- Period 3: `period * 3`
- ...up to Period 10: `period * 10`

The system then analyzes:
- Buy count: Number of RSI values > 50
- Sell count: Number of RSI values < 50
- Buy power: Sum of buy RSI values
- Sell power: Sum of sell RSI values

## Usage

### Basic Usage

```bash
# Basic SCHR_TREND with default settings (period=2, tr_mode=zone, extreme_up=95, extreme_down=5)
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_TREND
```

### With Parameters

```bash
# SCHR_TREND with custom period and zone mode
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_TREND:5,zone,90,10

# SCHR_TREND with first classic mode
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_TREND:3,firstclassic,95,5

# SCHR_TREND with purchase power mode
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_TREND:2,purchasepower,95,5

# SCHR_TREND with custom extreme points
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_TREND:4,trend,85,15
```

### Parameter Format

```
SCHR_TREND:period,tr_mode,extreme_up,extreme_down
```

- **period**: RSI period (default: 2)
- **tr_mode**: Trading rule mode (default: zone)
- **extreme_up**: Extreme up point (default: 95)
- **extreme_down**: Extreme down point (default: 5)

### Trading Rule Modes

| Mode | Description | Best For |
|------|-------------|----------|
| `firstclassic` | >95 Sell, <5 Buy | Classic extreme reversal |
| `firsttrend` | >95 Buy, <5 Sell | Trend following with extremes |
| `trend` | Best Up 70\| Down 30 | Trend continuation |
| `zone` | >50 Buy, <50 Sell | Zone-based trading |
| `firstzone` | Include New Extreme Signals | First signal detection |
| `firststrongzone` | Without New Extreme Signals | Strong trend detection |
| `purchasepower` | 10 indicators analysis | Multi-timeframe analysis |
| `purchasepower_bycount` | Count-based analysis | Simple power analysis |
| `purchasepower_extreme` | Only extreme signals | Extreme condition trading |
| `purchasepower_weak` | Weak signal analysis | Conservative trading |

## Signal Interpretation

### Direction Values

- **0.0 (NOTRADE)**: No trading signal
- **1.0 (BUY)**: Buy signal - upward trend detected
- **2.0 (SELL)**: Sell signal - downward trend detected
- **3.0 (DBL_BUY)**: Double buy signal - strong upward trend
- **4.0 (DBL_SELL)**: Double sell signal - strong downward trend

### Signal Generation Logic

1. **Basic Signal**: Based on RSI value and trading rule mode
2. **Trend Continuation**: Some modes maintain previous trend direction
3. **Extreme Detection**: Identifies overbought/oversold conditions
4. **Purchase Power**: Analyzes multiple RSI periods for consensus

## Trading Strategy

### Recommended Settings

#### Conservative Trading
```bash
SCHR_TREND:5,firststrongzone,90,10
```
- Longer period for stability
- Strong zone detection
- Conservative extreme points

#### Balanced Trading
```bash
SCHR_TREND:2,zone,95,5
```
- Standard period
- Zone-based signals
- Standard extreme points

#### Aggressive Trading
```bash
SCHR_TREND:1,purchasepower,85,15
```
- Short period for sensitivity
- Purchase power analysis
- Wider extreme range

#### Trend Following
```bash
SCHR_TREND:3,trend,90,10
```
- Medium period
- Trend continuation
- Moderate extreme points

## Performance Characteristics

### Strengths

- **Excellent Trend Detection**: Superior trend identification capabilities
- **Multiple Trading Modes**: Flexible strategy adaptation
- **Purchase Power Analysis**: Advanced multi-timeframe analysis
- **Extreme Signal Detection**: Clear overbought/oversold identification
- **Signal Clarity**: Distinct buy/sell signals with strength indication

### Limitations

- **Complex Parameter Tuning**: Multiple parameters require careful optimization
- **RSI Dependencies**: Performance depends on RSI effectiveness
- **Multiple Calculations**: Purchase power modes require significant computation
- **Parameter Sensitivity**: Results vary significantly with parameter changes

## Technical Implementation

### Data Requirements

- **Minimum Data Points**: `period + 1` for basic calculation
- **Price Type**: Open prices (default) or Close prices
- **Data Quality**: Clean OHLCV data required

### Calculation Complexity

- **Basic Modes**: O(n) complexity
- **Purchase Power Modes**: O(n * 10) complexity due to multiple RSI calculations
- **Memory Usage**: Moderate for basic modes, higher for purchase power modes

### Optimization Tips

1. **Use Appropriate Period**: Shorter periods for fast markets, longer for stable markets
2. **Choose Trading Mode**: Match mode to trading strategy and time horizon
3. **Adjust Extreme Points**: Tune extreme levels based on market volatility
4. **Monitor Performance**: Track signal accuracy and adjust parameters accordingly

## Integration Examples

### Python API

```python
from src.calculation.indicators.trend.schr_trend_ind import SCHRTrendIndicator, TradingRuleMode

# Create indicator instance
indicator = SCHRTrendIndicator(
    period=2,
    tr_mode=TradingRuleMode.TR_Zone,
    extreme_up=95,
    extreme_down=5
)

# Calculate indicator
result = indicator.calculate(df)
```

### Rule Application

```python
from src.calculation.rules import apply_rule_schr_trend

# Apply trading rule
result = apply_rule_schr_trend(
    df=df,
    point=0.0001,
    period=2,
    tr_mode='zone',
    extreme_up=95,
    extreme_down=5
)
```

## Related Indicators

- **SCHR_ROST**: ADX-based trend indicator
- **RSI**: Relative Strength Index (base calculation)
- **MACD**: Moving Average Convergence Divergence
- **ADX**: Average Directional Index

## References

- **Original MQL5**: SCHR_Trend.mq5 by Shcherbyna Rostyslav
- **Algorithm**: RSI-based trend detection with multiple trading rules
- **Implementation**: Python port with enhanced parameter validation
