# Wave Indicator with Terminal Mode (-d term)

## Overview

The Wave indicator is now fully supported in terminal mode using the `-d term` option. This provides a high-quality, ASCII-based visualization of the Wave indicator with dual charts showing both price action and indicator values, perfect for terminal environments and SSH connections.

## Key Features

### ✅ Dual Chart Display
- **Upper Chart**: OHLC candlestick chart with **BUY/SELL signals**
- **Lower Chart**: Wave indicator values with color-coded signals

### ✅ Trading Signals on Price Chart
- **BUY Signals**: Yellow triangles (▲▲) displayed below the Low price
- **SELL Signals**: Magenta triangles (▼▼) displayed above the High price
- **Signal Source**: Automatically detects `_Plot_Color`, `_Signal`, or `Direction` columns

### ✅ Interactive Navigation
- Navigate between chunks with `n/p/s/e/c/d/q` commands
- Real-time signal visualization
- Comprehensive statistics display

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
| trend1 | First trend period | 2 |
| tr1 | First trend type | fast |
| long2 | Second long period | 22 |
| fast2 | Second fast period | 11 |
| trend2 | Second trend period | 4 |
| tr2 | Second trend type | fast |
| global_tr | Global trend type | prime |
| sma_period | SMA period | 22 |
| price_type | Price type to use | open |

## Signal Interpretation

### Signal Values
- **0**: NO TRADE (no signal)
- **1**: BUY signal (yellow triangle)
- **2**: SELL signal (magenta triangle)

### Signal Display
- **Upper Chart**: Trading signals are displayed directly on the OHLC candlestick chart
- **Lower Chart**: Wave indicator values with color-coded signal segments

## Navigation Commands

| Command | Action |
|---------|--------|
| `n` | Next chunk |
| `p` | Previous chunk |
| `s` | Start (first chunk) |
| `e` | End (last chunk) |
| `c` | Choose specific chunk |
| `d` | Choose specific date |
| `q` | Quit |

## Technical Implementation

### Signal Detection
The system automatically detects trading signals from multiple sources:
1. `_Plot_Color` column (Wave indicator primary)
2. `_Signal` column (Wave indicator alternative)
3. `Direction` column (Standard indicator format)

### Chart Rendering
- **OHLC Chart**: ASCII-based candlestick representation
- **Signal Markers**: Unicode triangles for BUY/SELL signals
- **Wave Chart**: Color-coded indicator values with signal segments

## Error Handling
- **Robust Error Management**: Graceful handling of missing data
- **Column Flexibility**: Support for multiple naming conventions
- **Fallback Rendering**: Automatic fallback for unsupported Unicode characters

## Performance
- **Fast Rendering**: Optimized for terminal environments
- **Memory Efficient**: Chunked processing for large datasets
- **SSH Compatible**: Works perfectly over remote connections

## Examples

### Basic Wave Indicator
```bash
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d term
```

### Real Data Analysis
```bash
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d term
```

## Troubleshooting

### Common Issues
1. **No signals displayed**: Check if `_Plot_Color` or `_Signal` columns exist
2. **Unicode errors**: Terminal may not support triangle characters
3. **Performance issues**: Use smaller chunk sizes for large datasets

### Debug Mode
Enable debug output to see detailed signal processing:
```bash
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d term --debug
```
