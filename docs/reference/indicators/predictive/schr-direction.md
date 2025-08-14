# SCHR Direction (SCHR_DIR)

## Overview

SCHR Direction is a predictive indicator that shows the fastest direction of High and Low lines based on Volume Price Ratio (VPR) analysis. It provides two separate lines (High and Low) that help identify potential trading opportunities.

## Key Features

- **Dual Line Display**: Shows two separate lines (High and Low) for better analysis
- **Volume-Based**: Uses Volume Price Ratio (VPR) for calculations
- **Fixed Parameters**: Optimized parameters for consistent performance
- **Trading Signals**: Generates BUY/SELL signals based on price position relative to lines

## Trading Rules

### Signal Generation
- **BUY Signal**: When open price is higher than both High and Low lines
- **SELL Signal**: When open price is lower than both High and Low lines
- **NO TRADE**: When open price is between the High and Low lines

### Line Behavior
- **High Line (Blue)**: Represents resistance levels, colored as SELL signal
- **Low Line (Gold)**: Represents support levels, colored as BUY signal
- **Strong Exceed Mode**: Lines only update when they exceed both previous values and current price levels

## Parameters

### grow_percent (float)
- **Range**: 1.0 - 95.0
- **Default**: 1.0
- **Description**: Growth percentage for line calculation
  - Lower values (1-25): More aggressive signals, tighter line separation
  - Higher values (50-95): More conservative signals, wider line separation

### Fixed Parameters
- **Shift External/Internal**: False (internal mode)
- **Fixed Price**: True (always uses Open price)
- **Fake Line**: False (uses previous bar data)
- **Strong Exceed**: True (strong exceed mode)
- **Lines Count**: BothLines (always shows both lines)

## Calculation Method

### VPR (Volume Price Ratio) Calculation
```
DIFF = (High - Low) / Point
VPR = Volume / DIFF (when DIFF != 0 and Volume != DIFF)
```

### Direction Lines Calculation
```
C_VPR = 0.5 * log(π)
Grow_Factor = 95 / 100 (internal mode)

Dir_High = Open + ((DIFF * C_VPR * Point) - (C_VPR³ * VPR * Point)) * Grow_Factor
Dir_Low = Open - ((DIFF * C_VPR * Point) + (C_VPR³ * VPR * Point)) * Grow_Factor
```

### Line Logic (Strong Exceed Mode)
- **High Line**: Updates only when new value > previous high AND new value > current high
- **Low Line**: Updates only when new value < previous low AND new value < current low

## Usage

### Command Line
```bash
# Default usage (1% growth)
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR

# With custom growth percentage
uv run run_analysis.py show csv gbp -d fastest --rule schr_dir:50
uv run run_analysis.py show csv gbp -d fastest --rule schr_dir:95
```

### Parameters
- **grow_percent** (float): Growth percentage for line calculation (1-95, default: 1)
  - Lower values (1-25): More aggressive signals, tighter line separation
  - Higher values (50-95): More conservative signals, wider line separation

## Output Columns

- **PPrice1**: High line values (resistance)
- **PPrice2**: Low line values (support)
- **PColor1**: High line color (2 = SELL)
- **PColor2**: Low line color (1 = BUY)
- **Direction**: Trading signals (0 = NOTRADE, 1 = BUY, 2 = SELL)
- **SCHR_DIR_Diff**: Price difference in points
- **SCHR_DIR_VPR**: Volume Price Ratio
- **SCHR_DIR_Price_Type**: Always "Open"
- **SCHR_DIR_Grow_Percent**: Always 95.0
- **SCHR_DIR_Strong_Exceed**: Always True
- **SCHR_DIR_Shift_External_Internal**: Always False

## Visual Display

The indicator displays as a dual chart with:
- **Primary Chart**: OHLC candlesticks
- **Secondary Chart**: Two separate lines
  - Blue line (High line) - resistance levels
  - Gold line (Low line) - support levels
  - Buy/Sell markers at signal points

## Advantages

- **Fast Direction Prediction**: Quickly identifies potential price direction
- **Volume-Based Analysis**: Incorporates volume data for better accuracy
- **Clear Visual Signals**: Dual line display makes it easy to identify opportunities
- **Consistent Performance**: Fixed parameters ensure reliable results

## Limitations

- **Fixed Parameters**: No customization options
- **Volume Dependency**: Requires volume data for calculations
- **Signal Frequency**: May generate fewer signals due to strict criteria

## Technical Notes

- Based on MQL5 SCHR_DIR.mq5 indicator by Shcherbyna Rostyslav
- Uses previous bar data for calculations (fake_line = False)
- Implements strong exceed mode for more reliable signals
- Optimized for MT5 compatibility and performance

## Related Indicators

- **Support/Resistance**: Similar concept but different calculation method
- **Bollinger Bands**: Also uses dual lines for analysis
- **Donchian Channels**: Similar high/low line concept
