# Wave Indicator with Terminal Mode (-d term)

## Overview

The Wave indicator is now fully supported in terminal mode using the `-d term` option. This provides a high-quality, ASCII-based visualization of the Wave indicator with dual charts showing both price action and indicator values, perfect for terminal environments and SSH connections.

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

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `long1` | First long period | 339 | > 0 |
| `fast1` | First fast period | 10 | > 0 |
| `trend1` | First trend period | 2 | > 0 |
| `tr1` | First trading rule | fast | See Trading Rules |
| `long2` | Second long period | 22 | > 0 |
| `fast2` | Second fast period | 11 | > 0 |
| `trend2` | Second trend period | 4 | > 0 |
| `tr2` | Second trading rule | fast | See Trading Rules |
| `global_tr` | Global trading rule | prime | See Global Rules |
| `sma_period` | SMA calculation period | 22 | > 0 |
| `price_type` | Price type for calculation | open | open/close |

## Trading Rules (tr1, tr2)

| Rule | Description |
|------|-------------|
| `fast` | Basic momentum comparison |
| `zone` | Simple zone-based signals |
| `strongtrend` | Strong trend confirmation |
| `weaktrend` | Weak trend signals |
| `fastzonereverse` | Reverse signals in zones |
| `bettertrend` | Enhanced trend signals |
| `betterfast` | Improved fast trading |
| `rost` | Reverse momentum signals |
| `trendrost` | Trend-based reverse signals |
| `bettertrendrost` | Enhanced trend reverse signals |

## Global Trading Rules (global_tr)

| Rule | Description |
|------|-------------|
| `prime` | Prime rule - generates signals when both wave indicators agree |
| `reverse` | Reverse rule - reverses signals when both wave indicators agree |
| `primezone` | Prime Zone rule - BUY only in negative zone, SELL only in positive zone |
| `reversezone` | Reverse Zone rule - reverses zone-filtered signals when both agree |
| `newzone` | New Zone rule - generates signals when wave indicators disagree |
| `longzone` | Long Zone rule - always generates opposite signal to last confirmed signal |
| `longzonereverse` | Long Zone Reverse rule - always uses the last confirmed signal |

## Terminal Display Features

### Dual Chart Layout

The terminal mode displays two charts:

1. **Top Chart (50% height)**: OHLC candlestick chart with trading signals
2. **Bottom Chart (50% height)**: Wave indicator visualization

### Wave Indicator Elements

The bottom chart displays:

- **Wave Line (BUY)**: Red line for BUY signals (`_Plot_Color == 1`)
- **Wave Line (SELL)**: Blue line for SELL signals (`_Plot_Color == 2`)
- **Fast Line**: Red line for momentum indicator
- **MA Line**: Light blue line for moving average
- **Zero Line**: White reference line at zero level

### Signal Visualization

- **BUY Signals**: Red lines only when `_Plot_Color == 1`
- **SELL Signals**: Blue lines only when `_Plot_Color == 2`
- **No Trade**: No lines displayed when `_Plot_Color == 0`
- **Valid Data**: Lines only shown when data is not NaN or 0

### Navigation System

The terminal mode includes an interactive navigation system:

- **`n`** - Next chunk
- **`p`** - Previous chunk  
- **`s`** - Start (first chunk)
- **`e`** - End (last chunk)
- **`c`** - Choose chunk by number
- **`d`** - Choose chunk by date (YYYY-MM-DD or YYYY-MM-DD HH:MM)
- **`h`** or **`?`** - Show help
- **`q`** - Quit navigation
- **Enter** - Continue to next chunk

## Example Output

```
     ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
1.717┤ ██ OHLC Candles                                                                    │ █ █           ││
1.673┤                                 │ │       │                                        █ █ █ │ █ │ █ █ █│
1.630┤                               │ █ █   │ │ █ █ █ █ █ █ │ │ │                      █ █ │ █ █ █ █ █ │ ││
1.542┤█     │ │               █  █ █ █ █ █ █ █ █ █ │ █ │ │ █ █ █ █ █ █ │ │ │ █ █  █ █ █ █         │        │
1.498┤█ █ █ █ █ █ █ █ █ █ █ █ █  │ │ │                     │     │ │ █ █ █ █ █ │                           │
1.454┤│ │ █   █ │ █ █ │ │ │                                                                                │
     └─────────────────────────────────────────────────────────────────────────────────────────────────────┘
Price

       ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
 0.0304┤ ▞▞ Wave (BUY)                                                                        ▗▄▄▄▗▄▄▄▄▄▞▀▀│
 0.0214┤ ▞▞ Wave (SELL)                                     ▗                               ▗▗▞▀▀▀▘        │
 0.0123┤ ▞▞ Fast Line                           ▄▄▄▄▄▀▀▀▀▀▀▘▀▀▀▀▀▀▀▀▄▄▄▄       ▗▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▞▀▀▀▀│
-0.0058┤ ▞▞ MA Line     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
-0.0149┤ ▞▞ Zero Line              ▄▄▄▄▄▀▀▀▘     ▚▄▄▄▄▀▀▀▀▀▀▀▀▘                                            │
-0.0239┤      ▝▀▝▀▀▀▀▀▚▄▄▄▄▄▄▄▄▄▄▄▀▀                                                                       │
       └┬───────────────────┬─────────┬───────────────────┬─────────┬───────────────────┬─────────┬────────┘
    01/06/1993       01/04/1994  01/09/1994          01/07/1995  01/12/1995      01/10/1996  01/03/1997

WAVE Value                                           Date/Time

[Navigation: type 'n/p/s/e/c/d/q' -> next/previous/start/end/choose chunk/choose date/quit]
Current: Chunk 1/8 (1993-06-01 00:00:00 to 1997-07-01 00:00:00)
Press Enter to continue or type navigation command:
```

## Advanced Usage Examples

### Example 1: Default Parameters

```bash
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d term
```

### Example 2: Custom Parameters for Short-term Analysis

```bash
uv run run_analysis.py show csv mn1 --rule wave:50,5,10,fast,20,3,7,fast,prime,15,open -d term
```

### Example 3: Long-term Trend Analysis

```bash
uv run run_analysis.py show csv mn1 --rule wave:500,20,50,strongtrend,100,15,30,strongtrend,primezone,50,close -d term
```

### Example 4: Reverse Strategy

```bash
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fast,22,11,4,fast,reverse,22,open -d term
```

## Technical Implementation

### Column Support

The terminal mode supports multiple column naming conventions:

- **Wave Data**: `_Plot_Wave` or `_plot_wave`
- **Signal Colors**: `_Plot_Color` or `_plot_color`
- **Fast Line**: `_Plot_FastLine` or `_plot_fastline`
- **MA Line**: `MA_Line`

### Signal Processing

- **BUY Signals**: `_Plot_Color == 1` (red lines)
- **SELL Signals**: `_Plot_Color == 2` (blue lines)
- **No Trade**: `_Plot_Color == 0` (no lines)

### Error Handling

The terminal mode includes robust error handling:

- Graceful handling of missing columns
- Support for different column naming conventions
- Proper handling of zero and NaN values
- Fallback behavior for invalid data

## Benefits

1. **Terminal Compatibility**: Works in any terminal environment
2. **SSH Support**: Perfect for remote server analysis
3. **Low Resource Usage**: Minimal CPU and memory requirements
4. **Interactive Navigation**: Easy data exploration
5. **High Contrast**: Clear visualization in monochrome terminals
6. **Real-time Analysis**: Fast rendering for large datasets

## Comparison with Other Modes

| Feature | Terminal (-d term) | Fastest (-d fastest) | Fast (-d fast) | MPL (-d mpl) |
|---------|-------------------|---------------------|----------------|--------------|
| Environment | Terminal/SSH | Browser | Browser | Static Image |
| Interactivity | Navigation | Full | Full | None |
| Resource Usage | Low | High | Medium | Low |
| Rendering Speed | Fast | Very Fast | Fast | Medium |
| Data Size Support | Large | Very Large | Large | Medium |

## Troubleshooting

### Common Issues

1. **No Wave Lines Displayed**: Check if `_Plot_Color` contains valid signals (1 or 2)
2. **Missing Data**: Ensure sufficient data points for calculation (minimum 339 for default parameters)
3. **Navigation Not Working**: Press `h` for help or `q` to quit

### Performance Tips

1. **Large Datasets**: Use chunked navigation to explore data efficiently
2. **Real-time Analysis**: Terminal mode is optimized for fast rendering
3. **Memory Usage**: Terminal mode uses minimal memory compared to browser-based modes

## Integration

The Wave indicator terminal mode integrates seamlessly with:

- **Universal Trading Metrics**: Full metrics analysis display
- **Chunked Plotting**: Efficient data visualization
- **Navigation System**: Interactive data exploration
- **Error Handling**: Robust error management
- **Column Flexibility**: Support for multiple naming conventions
