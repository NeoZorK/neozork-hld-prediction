# SCHR Direction (SCHR_DIR)

## Overview

SCHR Direction is a premium predictive indicator that shows the fastest direction of High and Low prices based on Volume Price Ratio (VPR) analysis. This indicator is based on the MQL5 SCHR_DIR.mq5 indicator by Shcherbyna Rostyslav.

## Description

SCHR Direction calculates direction lines (High and Low) using a sophisticated algorithm that combines:
- Volume Price Ratio (VPR) analysis
- Price difference calculations
- Configurable growth percentages
- Multiple line types (Upper, Lower, Both)

The indicator predicts price direction by analyzing the relationship between volume and price ranges, providing early signals for potential market movements.

## Key Features

- **Fast Direction Prediction**: Provides quick directional signals based on VPR analysis
- **Volume-Based Analysis**: Uses volume data to enhance prediction accuracy
- **Multiple Line Types**: Supports Upper, Lower, or Both line calculations
- **Configurable Parameters**: Highly customizable with 6 main parameters
- **Strong/Weak Exceed Modes**: Different sensitivity levels for signal generation

## Mathematical Foundation

### Core Formulas

1. **VPR Constant**: `C_VPR = 0.5 * log(π)` ≈ 0.57236
2. **Price Difference**: `DIFF = (High - Low) / Point`
3. **Volume Price Ratio**: `VPR = Volume / DIFF` (when valid)
4. **Direction Lines**:
   - `Dir_High = Price + ((DIFF * C_VPR * Point) - (C_VPR³ * VPR * Point)) * Grow_Factor`
   - `Dir_Low = Price - ((DIFF * C_VPR * Point) + (C_VPR³ * VPR * Point)) * Grow_Factor`

### Grow Factor Calculation

- **Internal Mode**: `Grow_Factor = Grow_Percent / 100`
- **External Mode**: `Grow_Factor = (100 + Grow_Percent) / 100`

## Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `grow_percent` | int | 95 | 1-99 | Growth percentage for scaling direction lines |
| `shift_external_internal` | bool | false | true/false | External vs Internal shift mode |
| `fixed_price` | bool | true | true/false | Use Open price vs Close price |
| `fake_line` | bool | false | true/false | Use current vs previous bar data |
| `strong_exceed` | bool | true | true/false | Strong vs weak exceed mode |
| `lines_count` | int | 2 | 0-2 | Line type: 0=Upper, 1=Lower, 2=Both |

## Usage

### Basic Usage

```bash
# Default parameters
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR

# With custom parameters
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR:80,false,true,false,true,2
```

### Parameter Examples

```bash
# Conservative settings (lower growth, strong exceed)
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR:50,false,true,false,true,2

# Aggressive settings (higher growth, weak exceed)
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR:99,true,false,true,false,2

# Upper line only
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR:95,false,true,false,true,0

# Lower line only
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR:95,false,true,false,true,1
```

## Output Columns

The indicator generates the following output columns:

| Column | Description |
|--------|-------------|
| `PPrice1` | Predicted Low (Support level) |
| `PPrice2` | Predicted High (Resistance level) |
| `Direction` | Trading signals (BUY/SELL/NOTRADE) |
| `SCHR_DIR_High` | High direction line values |
| `SCHR_DIR_Low` | Low direction line values |
| `SCHR_DIR_Diff` | Price difference in points |
| `SCHR_DIR_VPR` | Volume Price Ratio values |
| `SCHR_DIR_Price_Type` | Price type used (Open/Close) |
| `SCHR_DIR_Grow_Percent` | Applied growth percentage |
| `SCHR_DIR_Strong_Exceed` | Strong exceed mode flag |

## Trading Signals

### Signal Generation Logic

1. **Strong Exceed Mode** (default):
   - High Line: `Dir_High > Prev_High AND Dir_High > Current_High`
   - Low Line: `Dir_Low < Prev_Low AND Dir_Low < Current_Low`

2. **Weak Exceed Mode**:
   - High Line: `Dir_High > Prev_High`
   - Low Line: `Dir_Low < Prev_Low`

### Signal Interpretation

- **BUY Signal**: Generated when Low direction line exceeds previous low
- **SELL Signal**: Generated when High direction line exceeds previous high
- **NOTRADE**: No clear directional signal

## Advantages

✅ **Fast Direction Prediction**: Provides early directional signals
✅ **Volume Integration**: Uses volume data for enhanced accuracy
✅ **Multiple Configurations**: Highly customizable parameters
✅ **Flexible Line Types**: Support for different line combinations
✅ **Strong/Weak Modes**: Different sensitivity levels available

## Limitations

❌ **Complex Calculation**: Sophisticated algorithm may be resource-intensive
❌ **Parameter Sensitivity**: Results highly dependent on parameter choice
❌ **Volume Dependency**: Requires reliable volume data
❌ **Market Conditions**: Performance may vary in different market conditions

## Best Practices

### Parameter Selection

1. **Grow Percent**: Start with 95 for most markets, adjust based on volatility
2. **Strong vs Weak Exceed**: Use Strong for conservative trading, Weak for aggressive
3. **Line Types**: Use Both Lines for comprehensive analysis
4. **Price Type**: Fixed Price (Open) generally provides better results

### Market Conditions

- **Trending Markets**: Works best in trending conditions
- **High Volume**: Requires sufficient volume for accurate VPR calculation
- **Timeframes**: Suitable for various timeframes (M1 to MN1)

### Risk Management

- Always use stop-losses based on the predicted levels
- Consider combining with other indicators for confirmation
- Monitor volume conditions for signal reliability
- Test parameters on historical data before live trading

## Integration with Other Indicators

SCHR_DIR can be effectively combined with:

- **Support/Resistance Indicators**: For level confirmation
- **Volume Indicators**: For volume trend analysis
- **Trend Indicators**: For trend direction confirmation
- **Oscillators**: For overbought/oversold conditions

## Performance Considerations

- **Calculation Speed**: Moderate computational requirements
- **Memory Usage**: Efficient memory usage for large datasets
- **Real-time Performance**: Suitable for real-time trading applications
- **Historical Analysis**: Excellent for backtesting and analysis

## Troubleshooting

### Common Issues

1. **No Signals Generated**: Check volume data availability and parameter settings
2. **Extreme Values**: Adjust grow_percent to more conservative levels
3. **Inconsistent Results**: Verify data quality and parameter consistency
4. **Performance Issues**: Consider reducing data size or optimizing parameters

### Debug Information

The indicator provides detailed debug information including:
- VPR calculation values
- Direction line calculations
- Parameter validation
- Signal generation logic

## Related Indicators

- **PHLD**: Predict High Low Direction (simplified version)
- **PV**: Pressure Vector (volume-based analysis)
- **SR**: Support Resistance (level-based analysis)

## References

- Original MQL5 implementation: SCHR_DIR.mq5 by Shcherbyna Rostyslav
- Volume Price Ratio theory and applications
- Technical analysis principles for directional trading
