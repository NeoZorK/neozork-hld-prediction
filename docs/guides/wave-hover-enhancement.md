# Wave Indicator Hover Enhancement

## Overview

The Wave indicator in fastest mode has been enhanced to provide more detailed information on hover. When users hover over Wave indicator lines on the lower chart, they now see both the numerical value and the color significance.

## Features

### Enhanced Hover Information

When hovering over Wave indicator lines, users now see:

- **Wave Value**: The numerical value of the Wave indicator
- **Color Information**: What the color represents:
  - **Red (BUY)**: Buy signal
  - **Blue (SELL)**: Sell signal  
  - **Black (NOTRADE)**: No trade signal (not visible on chart)

### Third Wave Hover Trace

A third hover trace named "wave" has been added that:

- **Shows values only for red/blue segments**: Only displays hover information where there are valid buy/sell signals
- **Invisible markers**: Uses transparent markers so it doesn't interfere with the visual display
- **Simple hover template**: Shows "wave Value: X.XXXXXX" without color information
- **No legend entry**: Doesn't appear in the chart legend

### Fast Line and MA Line Enhancements

Additional hover information has been added to:

- **Fast Line**: Shows "Red (Signal)" to indicate it's a signal line
- **MA Line**: Shows "Light Blue (MA)" to indicate it's a moving average

## Implementation Details

### Code Changes

The enhancement was implemented in `src/plotting/dual_chart_fastest.py`:

1. **Modified `create_discontinuous_line_traces` function**:
   - Added color name determination logic
   - Enhanced hover template to include color information

2. **Updated hover templates**:
   - Wave segments: `'<b>Wave</b><br>Value: %{y:.6f}<br>Color: {color_name}<extra></extra>'`
   - Third wave trace: `'<b>wave</b><br>Value: %{y:.6f}<extra></extra>'`
   - Fast Line: `'<b>Fast Line</b><br>Value: %{y:.6f}<br>Color: Red (Signal)<extra></extra>'`
   - MA Line: `'<b>MA Line</b><br>Value: %{y:.6f}<br>Color: Light Blue (MA)<extra></extra>'`

### Color Mapping

The system maps colors to trading signals:

```python
color_name = "Red (BUY)" if color == 'red' else "Blue (SELL)" if color == 'blue' else "Black (NOTRADE)"
```

## Usage

### Command Example

```bash
uv run run_analysis.py show csv mn1 -d fastest --rule wave:339,10,2,fast,22,11,4,fast,prime,55,open
```

### Expected Behavior

1. **Lower Chart**: Shows Wave indicator with colored segments
2. **Hover Effect**: 
   - Red segments show "Wave Value: X.XXXXXX Color: Red (BUY)"
   - Blue segments show "Wave Value: X.XXXXXX Color: Blue (SELL)"
   - Third wave trace shows "wave Value: X.XXXXXX" (only on red/blue segments)
   - Fast Line shows "Fast Line Value: X.XXXXXX Color: Red (Signal)"
   - MA Line shows "MA Line Value: X.XXXXXX Color: Light Blue (MA)"

## Testing

### Test Coverage

The enhancement is fully tested in `tests/plotting/test_wave_hover_enhancement.py`:

- ✅ Hover template creation
- ✅ Color mapping correctness
- ✅ Wave indicator integration
- ✅ Third wave hover trace
- ✅ Third wave hover data filtering
- ✅ Fast Line hover template
- ✅ MA Line hover template

### Running Tests

```bash
uv run pytest tests/plotting/test_wave_hover_enhancement.py -v
```

## Benefits

1. **Improved User Experience**: Users can quickly understand what each color represents
2. **Better Signal Interpretation**: Clear indication of buy/sell signals
3. **Consistent Information**: All Wave-related lines show enhanced hover information
4. **Maintains Performance**: No impact on chart rendering speed

## Technical Notes

- Hover information is only shown for the first segment of each color to avoid duplicates
- Color information is determined at trace creation time
- Templates use Plotly's standard formatting with `<extra></extra>` to hide default hover box
- All changes are backward compatible with existing functionality
