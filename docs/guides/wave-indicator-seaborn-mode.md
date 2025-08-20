# Wave Indicator with Seaborn Mode (-d sb)

## Overview

The Wave indicator is now fully supported in Seaborn mode using the `-d sb` option. This provides a high-quality, scientific-style visualization of the Wave indicator with dual charts showing both price action and indicator values.

## Usage

### Basic Command

```bash
uv run python -m src.cli.cli csv --csv-file <data_file> --point <points> --rule wave:<parameters> -d sb
```

### Example

```bash
uv run python -m src.cli.cli csv --csv-file data/mn1.csv --point 50 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d sb
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
| `reversezone` | Reverse Zone rule - reverses zone-filtered signals |
| `newzone` | New Zone rule - generates signals when wave indicators disagree |
| `longzone` | Long Zone rule - always generates opposite signal to last confirmed signal |
| `longzonereverse` | Long Zone Reverse rule - always uses the last confirmed signal |

## Visual Features

### Main Chart (OHLC)
- **Candlesticks**: Modern green/red color scheme with enhanced styling
- **Wave Signals**: Blue upward triangles (^) for BUY signals, red downward triangles (v) for SELL signals
- **Support/Resistance**: Blue/orange dashed lines when available
- **Professional Legend**: Clean styling with shadow and rounded corners

### Indicator Chart
- **Wave Line**: Dynamic color-coded line segments
  - Red segments for BUY signals (`_Plot_Color == 1`)
  - Blue segments for SELL signals (`_Plot_Color == 2`)
  - Discontinuous line segments for clear signal visualization
- **Fast Line**: Red dotted line for momentum indicator
- **MA Line**: Light blue line for moving average
- **Zero Line**: Gray dashed reference line

### Signal Display
- **Smart Signal Filtering**: Uses `_Signal` column for actual trading signals (only when direction changes)
- **Proper Positioning**: BUY signals below candle lows, SELL signals above candle highs
- **Color Consistency**: Matches indicator chart colors
- **High Visibility**: Proper z-order and alpha transparency

## Technical Implementation

### Wave Indicator Processing
```python
elif indicator_name == 'wave':
    # Add Plot Wave (main indicator, single line with dynamic colors) - as per MQ5
    plot_wave_col = None
    plot_color_col = None
    if '_plot_wave' in display_df.columns:
        plot_wave_col = '_plot_wave'
    elif '_Plot_Wave' in display_df.columns:
        plot_wave_col = '_Plot_Wave'
    
    if '_plot_color' in display_df.columns:
        plot_color_col = '_plot_color'
    elif '_Plot_Color' in display_df.columns:
        plot_color_col = '_Plot_Color'
    
    if plot_wave_col and plot_color_col:
        # Create discontinuous line segments for different signal types
        valid_data_mask = display_df[plot_wave_col].notna() & (display_df[plot_wave_col] != 0)
        red_mask = (display_df[plot_color_col] == 1) & valid_data_mask
        blue_mask = (display_df[plot_color_col] == 2) & valid_data_mask
        
        # Plot red segments (BUY = 1)
        if red_mask.any():
            red_segments = _create_wave_line_segments(
                display_df.index, display_df[plot_wave_col], red_mask
            )
            for i, (seg_x, seg_y) in enumerate(red_segments):
                if i == 0:
                    ax2.plot(seg_x, seg_y, color='#FF4444', linewidth=1.5, label='Wave (BUY)', alpha=0.9)
                else:
                    ax2.plot(seg_x, seg_y, color='#FF4444', linewidth=1.5, alpha=0.9)
        
        # Plot blue segments (SELL = 2)
        if blue_mask.any():
            blue_segments = _create_wave_line_segments(
                display_df.index, display_df[plot_wave_col], blue_mask
            )
            for i, (seg_x, seg_y) in enumerate(blue_segments):
                if i == 0:
                    ax2.plot(seg_x, seg_y, color='#0066CC', linewidth=1.5, label='Wave (SELL)', alpha=0.9)
                else:
                    ax2.plot(seg_x, seg_y, color='#0066CC', linewidth=1.5, alpha=0.9)
```

### Signal Detection
```python
# Get Wave buy and sell signals - use _Signal for actual trading signals (only when direction changes)
signal_col = None
if '_signal' in display_df.columns:
    signal_col = '_signal'
elif '_Signal' in display_df.columns:
    signal_col = '_Signal'

if signal_col:
    # Use _Signal for actual trading signals (only when direction changes)
    wave_buy_signals = display_df[display_df[signal_col] == 1]  # BUY = 1
    wave_sell_signals = display_df[display_df[signal_col] == 2]  # SELL = 2
else:
    # Fallback to _Plot_Color if _Signal not available
    wave_buy_signals = display_df[display_df[plot_color_col] == 1]  # BUY = 1
    wave_sell_signals = display_df[display_df[plot_color_col] == 2]  # SELL = 2
```

## Comparison with Other Modes

| Feature | `-d sb` (Seaborn) | `-d mpl` (Matplotlib) | `-d fastest` (Plotly) |
|---------|-------------------|----------------------|----------------------|
| **Style** | Scientific presentation | Professional trading | Interactive web |
| **Performance** | Fast rendering | Fast rendering | Interactive |
| **File Format** | PNG image | PNG image | HTML file |
| **Interactivity** | Static | Static | Full interactive |
| **Wave Signals** | ✅ Complete | ✅ Complete | ✅ Complete |
| **Color Coding** | ✅ Dynamic | ✅ Dynamic | ✅ Dynamic |
| **Signal Filtering** | ✅ Smart | ✅ Smart | ✅ Smart |

## Best Practices

### Parameter Selection
- **For Trending Markets**: Use `strongtrend` or `bettertrend` trading rules
- **For Ranging Markets**: Use `zone` or `fast` trading rules
- **For Conservative Trading**: Use `prime` global rule
- **For Aggressive Trading**: Use `reverse` or `newzone` global rules

### Period Optimization
- **Short-term**: Use smaller periods (5-20)
- **Medium-term**: Use medium periods (20-100)
- **Long-term**: Use larger periods (100-500)

### Price Type Selection
- **Open Price**: Better for gap analysis and overnight moves
- **Close Price**: Better for trend analysis and end-of-day signals

## Troubleshooting

### Common Issues

1. **No Signals Displayed**
   - Check that parameters are valid
   - Ensure sufficient data points (at least max period)
   - Verify price type is correct

2. **Too Many Signals**
   - Use `_Signal` column instead of `_Plot_Color`
   - Adjust trading rules to be more conservative
   - Increase periods for smoother signals

3. **Poor Performance**
   - Reduce number of data points
   - Use simpler trading rules
   - Optimize period settings

### Error Messages

- **"Not enough data"**: Increase data points or reduce periods
- **"Invalid parameter"**: Check parameter format and ranges
- **"Missing columns"**: Ensure Wave indicator calculation completed successfully

## Examples

### Basic Wave Analysis
```bash
# Simple wave analysis with default parameters
uv run python -m src.cli.cli csv --csv-file data/eurusd.csv --point 100 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d sb
```

### Advanced Wave Analysis
```bash
# Advanced wave analysis with custom parameters
uv run python -m src.cli.cli csv --csv-file data/gbpusd.csv --point 200 --rule wave:100,20,5,strongtrend,50,15,3,zone,primezone,30,close -d sb
```

### Conservative Wave Strategy
```bash
# Conservative wave strategy for stable markets
uv run python -m src.cli.cli csv --csv-file data/usdjpy.csv --point 150 --rule wave:500,50,10,bettertrend,200,25,8,bettertrend,prime,50,open -d sb
```

## Performance Notes

- **Rendering Speed**: Seaborn mode provides fast rendering for large datasets
- **Memory Usage**: Efficient memory usage with optimized plotting
- **File Size**: PNG output provides good quality with reasonable file sizes
- **Scalability**: Handles datasets up to 10,000+ data points efficiently

## Future Enhancements

- **Custom Color Schemes**: User-defined color palettes
- **Advanced Signal Visualization**: Signal strength indicators
- **Export Options**: Multiple output formats
- **Real-time Updates**: Support for live data streaming
