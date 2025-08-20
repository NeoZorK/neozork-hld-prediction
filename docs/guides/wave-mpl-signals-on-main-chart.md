# Wave Indicator Signals on Main Chart - MPL Mode

## Overview

Wave indicator signals are now displayed on the main chart (OHLC) in MPL mode, providing a comprehensive view of both price action and trading signals in a single chart.

## Feature Description

### Signal Display on Main Chart

The Wave indicator signals are now shown on the upper chart (OHLC candlesticks) with the following features:

- **BUY Signals**: Red upward triangles (^) positioned below the low of each candle
- **SELL Signals**: Blue downward triangles (v) positioned above the high of each candle
- **Clear Color Coding**: Consistent with the indicator chart colors
- **Proper Legend**: "Wave BUY" and "Wave SELL" entries in the legend

### Visual Integration

The signals are integrated seamlessly with the existing chart elements:

1. **Candlesticks**: Modern green/red color scheme
2. **Support/Resistance**: Blue/orange dashed lines
3. **Wave Signals**: Red/blue triangles with proper positioning
4. **Legend**: Professional styling with shadow and rounded corners

## Technical Implementation

### Signal Detection

```python
# Get Wave buy and sell signals
wave_buy_signals = display_df[display_df[plot_color_col] == 1]  # BUY = 1
wave_sell_signals = display_df[display_df[plot_color_col] == 2]  # SELL = 2
```

### Signal Positioning

```python
# Add buy signals to main chart
if not wave_buy_signals.empty:
    ax1.scatter(wave_buy_signals.index, wave_buy_signals['Low'] * 0.995, 
               color='#FF4444', marker='^', s=100, label='Wave BUY', zorder=5, alpha=0.9)

# Add sell signals to main chart
if not wave_sell_signals.empty:
    ax1.scatter(wave_sell_signals.index, wave_sell_signals['High'] * 1.005, 
               color='#0066CC', marker='v', s=100, label='Wave SELL', zorder=5, alpha=0.9)
```

### Legend Integration

The legend is created after all signals are added to ensure proper display:

```python
# Add legend to main chart after all signals are added
ax1.legend(loc='upper right', framealpha=0.9, fancybox=True, shadow=True, fontsize=9)
```

## Usage Example

### Command
```bash
uv run python -m src.cli.cli csv --csv-file data.csv --point 20 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d mpl
```

### Visual Output

The MPL mode now provides:

1. **Upper Chart (OHLC)**:
   - Candlesticks with modern colors
   - Wave BUY signals (red triangles)
   - Wave SELL signals (blue triangles)
   - Support/resistance lines
   - Professional legend

2. **Lower Chart (Indicator)**:
   - Wave indicator lines with color segments
   - Fast Line (dotted red)
   - MA Line (teal)
   - Zero reference line

## Benefits

### Enhanced Analysis
- **Single View**: See price action and signals together
- **Clear Signals**: Easy identification of entry/exit points
- **Professional Appearance**: Modern styling and colors
- **Comprehensive Legend**: All elements properly labeled

### Improved User Experience
- **Better Context**: Signals in relation to price levels
- **Reduced Clutter**: Clean, organized display
- **Professional Quality**: High-quality matplotlib rendering
- **Consistent Styling**: Uniform color scheme throughout

## Test Coverage

### Comprehensive Testing
- ✅ Signal display on main chart
- ✅ BUY signal positioning and styling
- ✅ SELL signal positioning and styling
- ✅ Mixed signal scenarios
- ✅ No signal scenarios
- ✅ Legend integration
- ✅ Color coding verification
- ✅ Marker style validation
- ✅ Positioning accuracy
- ✅ Overall integration

### Quality Assurance
- All 10 tests pass
- No regression in existing functionality
- Proper signal positioning confirmed
- Legend integration verified

## Technical Details

### Signal Values
- **BUY Signal**: `_Plot_Color = 1`
- **SELL Signal**: `_Plot_Color = 2`
- **No Signal**: `_Plot_Color = 0`

### Color Scheme
- **Wave BUY**: `#FF4444` (modern red)
- **Wave SELL**: `#0066CC` (modern blue)
- **Consistent**: Matches indicator chart colors

### Positioning Logic
- **BUY Signals**: Positioned at `Low * 0.995` (slightly below candle)
- **SELL Signals**: Positioned at `High * 1.005` (slightly above candle)
- **Z-Order**: 5 (above candlesticks for visibility)

## Future Enhancements

### Potential Improvements
1. **Signal Strength**: Visual indication of signal strength
2. **Custom Markers**: User-defined marker styles
3. **Signal Labels**: Price values on signal markers
4. **Interactive Features**: Hover tooltips for signal details
5. **Export Options**: High-resolution signal charts

### Maintenance
- Regular testing of signal positioning
- Color scheme consistency checks
- Performance optimization for large datasets
- User feedback integration

## Conclusion

The addition of Wave indicator signals to the main chart in MPL mode provides:

- ✅ **Enhanced Analysis**: Price action and signals in one view
- ✅ **Professional Display**: Modern styling and clear signals
- ✅ **Better Context**: Signals positioned relative to price levels
- ✅ **Comprehensive Legend**: All elements properly labeled
- ✅ **Quality Assurance**: Full test coverage and validation

Users now get a complete trading view with both price action and Wave indicator signals displayed together for optimal analysis and decision-making.
