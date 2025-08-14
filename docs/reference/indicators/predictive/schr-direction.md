# SCHR Direction (SCHR_DIR)

## Overview

SCHR Direction is a premium predictive indicator that shows the fastest direction of High and Low prices based on Volume Price Ratio (VPR) analysis. This indicator is based on the MQL5 SCHR_DIR.mq5 indicator by Shcherbyna Rostyslav and has been optimized with fixed parameters for optimal performance and MT5 compatibility.

## Description

SCHR Direction calculates direction lines (High and Low) using a sophisticated algorithm that combines:
- Volume Price Ratio (VPR) analysis
- Price difference calculations
- Fixed growth percentage (1%)
- Both lines always displayed

The indicator predicts price direction by analyzing the relationship between volume and price ranges, providing early signals for potential market movements. All parameters are fixed for optimal performance and consistency with the original MQL5 implementation.

## Key Features

- **Fast Direction Prediction**: Provides quick directional signals based on VPR analysis
- **Volume-Based Analysis**: Uses volume data to enhance prediction accuracy
- **Fixed Parameters**: Optimized settings for consistent performance
- **MT5 Compatibility**: Matches the original MQL5 indicator behavior
- **Both Lines Always Shown**: Comprehensive analysis with both High and Low direction lines

## Mathematical Foundation

### Core Formulas

1. **VPR Constant**: `C_VPR = 0.5 * log(π)` ≈ 0.57236
2. **Price Difference**: `DIFF = (High - Low) / Point`
3. **Volume Price Ratio**: `VPR = Volume / DIFF` (when valid)
4. **Direction Lines**:
   - `Dir_High = Price + ((DIFF * C_VPR * Point) - (C_VPR³ * VPR * Point)) * Grow_Factor`
   - `Dir_Low = Price - ((DIFF * C_VPR * Point) + (C_VPR³ * VPR * Point)) * Grow_Factor`

### Fixed Parameters

- **Grow Factor**: `Grow_Factor = 1 / 100` (1% in internal mode)
- **Price Type**: Always uses Open price
- **Data Source**: Always uses previous bar data
- **Exceed Mode**: Always uses strong exceed mode
- **Lines Display**: Always shows both High and Low lines

## Parameters

**No Parameters Required**

All parameters are fixed for optimal performance:
- `grow_percent` = 1 (always 1%)
- `shift_external_internal` = false (always internal mode)
- `fixed_price` = true (always use Open price)
- `fake_line` = false (always use previous bar data)
- `strong_exceed` = true (always strong exceed mode)
- `lines_count` = both lines (always show both lines)

## Usage

### Basic Usage

```bash
# No parameters required - all values are fixed
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR
```

### Command Examples

```bash
# Standard usage
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR

# With other indicators
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR --rule RSI
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
| `SCHR_DIR_Price_Type` | Price type used (always "Open") |
| `SCHR_DIR_Grow_Percent` | Applied growth percentage (always 1) |
| `SCHR_DIR_Strong_Exceed` | Strong exceed mode flag (always true) |

## Trading Signals

### Signal Generation Logic

**Strong Exceed Mode (Fixed)**:
- High Line: `Dir_High > Prev_High AND Dir_High > Current_High`
- Low Line: `Dir_Low < Prev_Low AND Dir_Low < Current_Low`

### Signal Interpretation

- **BUY Signal**: Generated when Low direction line exceeds previous low
- **SELL Signal**: Generated when High direction line exceeds previous high
- **NOTRADE**: No clear directional signal

## Advantages

✅ **Optimized Performance**: Fixed parameters ensure consistent results
✅ **MT5 Compatibility**: Matches original MQL5 indicator behavior
✅ **Fast Direction Prediction**: Provides early directional signals
✅ **Volume Integration**: Uses volume data for enhanced accuracy
✅ **Both Lines Always Shown**: Comprehensive analysis
✅ **No Parameter Tuning**: Ready to use without configuration

## Limitations

❌ **No Parameter Customization**: Fixed settings cannot be adjusted
❌ **Volume Dependency**: Requires reliable volume data
❌ **Market Conditions**: Performance may vary in different market conditions

## Best Practices

### Usage Guidelines

1. **Volume Data**: Ensure sufficient volume data is available
2. **Timeframes**: Suitable for various timeframes (M1 to MN1)
3. **Market Conditions**: Works best in trending conditions
4. **Combination**: Can be effectively combined with other indicators

### Risk Management

- Always use stop-losses based on the predicted levels
- Consider combining with other indicators for confirmation
- Monitor volume conditions for signal reliability
- Test on historical data before live trading

## Integration with Other Indicators

SCHR_DIR can be effectively combined with:

- **Support/Resistance Indicators**: For level confirmation
- **Volume Indicators**: For volume trend analysis
- **Trend Indicators**: For trend direction confirmation
- **Momentum Indicators**: For momentum confirmation

## Technical Notes

### Fixed Parameter Benefits

1. **Consistency**: Same results across different sessions
2. **Performance**: Optimized calculations without parameter overhead
3. **Compatibility**: Matches original MQL5 implementation
4. **Simplicity**: No parameter tuning required

### Calculation Optimization

- Uses Open price for consistent base calculations
- Previous bar data for stable signal generation
- 1% growth factor for optimal sensitivity
- Strong exceed mode for reliable signals

## Migration from Previous Version

If you were using SCHR_DIR with custom parameters:

1. **Remove Parameters**: No longer specify parameters in the command
2. **Update Commands**: Change from `schr_dir:95,false,true,false,true,2` to `schr_dir`
3. **Verify Results**: Check that the new fixed parameters provide desired performance
4. **Test Integration**: Ensure compatibility with your existing trading strategy

The new fixed parameters are optimized for the most common use cases and provide consistent performance across different market conditions.
