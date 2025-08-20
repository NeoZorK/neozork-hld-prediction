# Wave Indicator with Terminal Mode (-d term)

## Overview

The Wave indicator is now fully supported in terminal mode using the `-d term` option. This provides a high-quality, ASCII-based visualization of the Wave indicator with dual charts showing both price action and indicator values, perfect for terminal environments and SSH connections.

## Key Features

### ✅ Dual Chart Display
- **Upper Chart**: OHLC candlestick chart with **BUY/SELL signals** (only direction changes)
- **Lower Chart**: Wave indicator values with color-coded signals

### ✅ Trading Signals on Price Chart
- **BUY Signals**: Yellow triangles (▲▲) displayed below the Low price
- **SELL Signals**: Magenta triangles (▼▼) displayed above the High price
- **Signal Source**: Uses `_Signal` column (only when direction changes) - same as other modes
- **Signal Logic**: Only displays signals when wave direction actually changes, not continuous signals

### ✅ Wave Indicator Display
- **Wave Line**: Discontinuous colored segments (red for BUY, blue for SELL)
- **Fast Line**: Thin red dotted line
- **MA Line**: Light blue moving average line
- **Zero Line**: Reference line at zero level

## Usage

### Basic Command

```bash
uv run run_analysis.py show csv <data_file> --rule wave:<parameters> -d term
```

### Example

```bash
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d term
```

## Parameters

The Wave indicator requires exactly 11 parameters in the following format:

```
wave:long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type
```

### Parameter Details

| Parameter | Description | Example |
|-----------|-------------|---------|
| long1 | First long period | 339 |
| fast1 | First fast period | 10 |
| trend1 | First trend filter | 2 |
| tr1 | First trend type | fast |
| long2 | Second long period | 22 |
| fast2 | Second fast period | 11 |
| trend2 | Second trend filter | 4 |
| tr2 | Second trend type | fast |
| global_tr | Global trend type | prime |
| sma_period | SMA period | 22 |
| price_type | Price type | open |

## Signal Logic

### Signal Display Priority
1. **`_Signal` column**: Primary source for trading signals (only direction changes)
2. **`Direction` column**: Fallback for standard indicators

### Signal Types
- **BUY (1)**: Wave direction changes to bullish
- **SELL (2)**: Wave direction changes to bearish  
- **NO TRADE (0)**: No direction change

### Signal Positioning
- **BUY signals**: Positioned below the Low price (Low * 0.99)
- **SELL signals**: Positioned above the High price (High * 1.01)

## Navigation

The terminal mode supports interactive navigation:

- **n**: Next chunk
- **p**: Previous chunk
- **s**: Start (first chunk)
- **e**: End (last chunk)
- **c**: Choose chunk number
- **d**: Choose specific date
- **q**: Quit

## Performance

- **Fast rendering**: Optimized for terminal environments
- **Low memory usage**: Efficient chunked processing
- **SSH compatible**: Works over remote connections
- **Unicode support**: Enhanced visual markers when available

## Comparison with Other Modes

| Feature | Terminal Mode | MPL Mode | Fastest Mode |
|---------|---------------|----------|--------------|
| Signal Source | `_Signal` only | `_Signal` only | `_Signal` only |
| Signal Frequency | Direction changes | Direction changes | Direction changes |
| Chart Type | ASCII | Matplotlib | Plotly |
| Navigation | Interactive | Static | Interactive |
| Performance | Fast | Medium | Very Fast |

## Troubleshooting

### No Signals Displayed
- Check if `_Signal` column exists in data
- Verify wave indicator parameters are correct
- Ensure sufficient data for calculation (minimum 339 points)

### Poor Signal Quality
- Review wave indicator parameters
- Check data quality and time period
- Consider adjusting trend filters

### Display Issues
- Ensure terminal supports Unicode characters
- Check terminal window size
- Verify color support in terminal

## Examples

### Basic Wave Analysis
```bash
# Analyze GBPUSD monthly data
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d term
```

### Demo Mode Testing
```bash
# Test with demo data
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d term
```

## Technical Notes

- **Signal Consistency**: Uses same signal logic as other plotting modes
- **Memory Efficient**: Processes data in chunks to handle large datasets
- **Cross-Platform**: Works on macOS, Linux, and Windows terminals
- **Real-time Ready**: Suitable for live trading signal monitoring
