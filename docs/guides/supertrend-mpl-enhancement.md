# SuperTrend MPL Mode Enhancement

## Overview

This document describes the enhancement made to the SuperTrend indicator plotting in mpl (mplfinance) mode to match the functionality and visual style of the fastest mode.

## Problem

Previously, the SuperTrend indicator in mpl mode was displayed as a simple purple line, while the fastest mode had enhanced functionality including:

- Color-coded trend segments (green for uptrend, red for downtrend)
- Signal change detection with golden highlighting
- BUY/SELL signal markers
- Enhanced segmentation with proper trend detection

## Solution

The `mplfinance_plot.py` file was enhanced to include the same SuperTrend logic as the fastest mode:

### Key Features Added

1. **Enhanced Trend Detection**
   - Determines trend direction based on price vs SuperTrend values
   - Uses the same logic as fastest mode: `trend = np.where(price_series > supertrend_values, 1, -1)`

2. **Color-Coded Segments**
   - Green (`#00C851`) for uptrend segments
   - Red (`#FF4444`) for downtrend segments  
   - Golden (`#FFC107`) for signal change points

3. **Signal Change Detection**
   - Detects BUY signals: `(trend == 1) & (trend.shift(1) == -1)`
   - Detects SELL signals: `(trend == -1) & (trend.shift(1) == 1)`
   - Highlights signal changes with golden color

4. **Enhanced Segmentation**
   - Breaks SuperTrend line into segments based on trend changes
   - Each segment is plotted with appropriate color
   - Signal change points are highlighted separately

5. **BUY/SELL Markers**
   - Triangle-up markers (^) for BUY signals in green
   - Triangle-down markers (v) for SELL signals in red
   - Large markers (100px) for visibility

### Implementation Details

The enhancement supports multiple data formats:

- **PPrice1/PPrice2 format**: Uses `PPrice1` and `PPrice2` columns with `Direction` column
- **SuperTrend format**: Uses `supertrend` or `SuperTrend` column with `Direction` column
- **Fallback handling**: Gracefully handles missing SuperTrend data

### Code Structure

```python
# Enhanced SuperTrend plotting (like fastest mode)
has_pprice = 'PPrice1' in df_results.columns and 'PPrice2' in df_results.columns
has_supertrend = 'supertrend' in df_results.columns or 'SuperTrend' in df_results.columns
has_direction = 'Direction' in df_results.columns

if has_pprice or has_supertrend:
    # Get supertrend values and direction
    if has_pprice:
        p1 = df_results['PPrice1']
        p2 = df_results['PPrice2']
        direction = df_results['Direction']
        
        # Handle NaN values properly
        valid_mask = ~(pd.isna(p1) | pd.isna(p2))
        supertrend_values = np.full(len(direction), np.nan)
        supertrend_values[valid_mask] = np.where(direction[valid_mask] > 0, p1[valid_mask], p2[valid_mask])
    else:
        supertrend_col = 'supertrend' if 'supertrend' in df_results.columns else 'SuperTrend'
        supertrend_values = df_results[supertrend_col]
        direction = df_results['Direction']
    
    # Determine trend direction (like in fastest mode)
    price_series = df_results['Close']
    trend = np.where(price_series > supertrend_values, 1, -1)
    trend = pd.Series(trend, index=df_results.index)
    
    # Colors like in fastest mode
    uptrend_color = '#00C851'  # Green
    downtrend_color = '#FF4444'  # Red
    signal_change_color = '#FFC107'  # Golden
    
    # Detect signal change points and create segments
    # ... segmentation logic ...
    
    # Add SuperTrend line segments with enhanced styling
    for seg_x, seg_y, seg_color in segments:
        if len(seg_x) > 1:
            seg_series = pd.Series(seg_y, index=seg_x)
            plots_to_add.append(mpf.make_addplot(
                seg_series, 
                panel=0, 
                color=seg_color, 
                width=2.5, 
                secondary_y=True
            ))
    
    # Add BUY/SELL signal markers
    buy_idx = df_results.index[(trend == 1) & (trend.shift(1) == -1)]
    sell_idx = df_results.index[(trend == -1) & (trend.shift(1) == 1)]
    
    if len(buy_idx) > 0:
        buy_y = supertrend_values[df_results.index.isin(buy_idx)]
        buy_series = pd.Series(buy_y, index=buy_idx)
        plots_to_add.append(mpf.make_addplot(
            buy_series,
            type='scatter', 
            markersize=100, 
            marker='^', 
            color=uptrend_color, 
            panel=0,
            secondary_y=True
        ))
```

## Usage

The enhanced SuperTrend plotting is automatically used when running commands like:

```bash
uv run run_analysis.py show csv gbp -d mpl --rule supertrend:10,3,open
```

## Testing

Comprehensive tests were added in `tests/plotting/test_mplfinance_supertrend.py` to verify:

- Enhanced plotting functionality
- Trend detection logic
- Signal change detection
- Segmentation logic
- Fallback column handling
- Missing data handling

## Benefits

1. **Consistency**: Mpl mode now matches fastest mode functionality
2. **Better Visualization**: Color-coded segments make trends easier to identify
3. **Signal Clarity**: BUY/SELL markers clearly show entry/exit points
4. **Enhanced UX**: Users get the same rich SuperTrend experience in mpl mode

## Compatibility

The enhancement maintains backward compatibility:
- Works with existing PPrice1/PPrice2 data format
- Supports both 'supertrend' and 'SuperTrend' column names
- Gracefully handles missing SuperTrend data
- No breaking changes to existing functionality

## Future Considerations

- Consider adding hover tooltips for SuperTrend segments
- Potential for additional customization options
- Integration with other plotting modes for consistency 