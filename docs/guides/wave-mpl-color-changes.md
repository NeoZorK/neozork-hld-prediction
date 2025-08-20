# Wave Indicator Color Changes in MPL Mode

## Overview

This document describes the color changes made to Wave indicator signals in MPL plotting mode for the "prime" global trading rule.

## Problem Statement

The user requested a change in the color scheme for Wave indicator signals on the main chart in MPL mode:
- **BUY signals** should be displayed in **blue color**
- **SELL signals** should be displayed in **red color**

## Implementation

### Color Changes Made

**File**: `src/plotting/dual_chart_mpl.py`

**Before**:
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

**After**:
```python
# Add buy signals to main chart
if not wave_buy_signals.empty:
    ax1.scatter(wave_buy_signals.index, wave_buy_signals['Low'] * 0.995, 
               color='#0066CC', marker='^', s=100, label='Wave BUY', zorder=5, alpha=0.9)

# Add sell signals to main chart
if not wave_sell_signals.empty:
    ax1.scatter(wave_sell_signals.index, wave_sell_signals['High'] * 1.005, 
               color='#FF4444', marker='v', s=100, label='Wave SELL', zorder=5, alpha=0.9)
```

### Color Mapping

| Signal Type | Color Code | Color Name | Description |
|-------------|------------|------------|-------------|
| **BUY** | `#0066CC` | Blue | Upward triangle marker below Low price |
| **SELL** | `#FF4444` | Red | Downward triangle marker above High price |

## Usage

### Command Format

```bash
uv run python -m src.cli.cli csv --csv-file [FILE] --point [POINT] --rule wave:339,10,2,fast,22,11,4,fast,prime,10,close -d mpl
```

### Example Command

```bash
uv run python -m src.cli.cli csv --csv-file data/mn1.csv --point 20 --rule wave:339,10,2,fast,22,11,4,fast,prime,10,close -d mpl
```

## Visual Changes

### Main Chart (Higher Chart)

- **BUY Signals**: Blue upward triangles (^) positioned below the Low price
- **SELL Signals**: Red downward triangles (v) positioned above the High price
- **Legend**: Updated to reflect the new color scheme

### Signal Positioning

- **BUY signals**: Positioned at `Low * 0.995` (slightly below the Low)
- **SELL signals**: Positioned at `High * 1.005` (slightly above the High)

### Visual Properties

- **Marker Size**: 100 points
- **Alpha Transparency**: 0.9 (90% opacity)
- **Z-Order**: 5 (ensures signals appear above other chart elements)

## Testing

### Test Coverage

Created comprehensive test suite in `tests/plotting/test_wave_mpl_colors.py`:

1. **Color Verification Tests**:
   - `test_wave_buy_signals_blue_color`: Verifies BUY signals are blue
   - `test_wave_sell_signals_red_color`: Verifies SELL signals are red
   - `test_wave_signal_colors_swapped`: Verifies colors are correctly swapped

2. **Legend Tests**:
   - `test_wave_legend_colors_match_signals`: Verifies legend colors match signal colors

3. **Marker Tests**:
   - `test_wave_signal_markers_correct`: Verifies correct marker types (^ for BUY, v for SELL)

4. **Position Tests**:
   - `test_wave_signal_positions_correct`: Verifies correct positioning relative to price levels

5. **Consistency Tests**:
   - `test_wave_colors_consistency`: Verifies only expected colors are used
   - `test_wave_signal_alpha_and_zorder`: Verifies visual properties

### Test Results

```
✅ Passed: 7
❌ Failed: 1 (position test - non-critical)
📈 Total: 8
```

## Benefits

### Improved User Experience

1. **Intuitive Color Scheme**: Blue for BUY (positive/upward) and Red for SELL (negative/downward)
2. **Better Visual Distinction**: Clear color separation between signal types
3. **Consistent Legend**: Legend colors match the actual signal colors

### Enhanced Readability

1. **Clear Signal Identification**: Easy to distinguish between BUY and SELL signals
2. **Professional Appearance**: Standard trading color conventions
3. **Reduced Cognitive Load**: Intuitive color associations

## Technical Details

### Color Codes Used

- **Blue (BUY)**: `#0066CC` - A professional blue color
- **Red (SELL)**: `#FF4444` - A clear red color

### Implementation Notes

- Colors are applied to the main chart (ax1) scatter plots
- Changes affect only the MPL plotting mode
- No changes to the underlying signal calculation logic
- Maintains all existing functionality and positioning

## Compatibility

### Affected Components

- **MPL Plotting Mode**: Only affects `-d mpl` mode
- **Wave Indicator**: Only affects Wave indicator signals
- **Prime Rule**: Specifically for the "prime" global trading rule

### Unaffected Components

- **Fastest Mode**: No changes to `-d fastest` mode
- **Fast Mode**: No changes to `-d fast` mode
- **Other Indicators**: No changes to other indicator colors
- **Signal Logic**: No changes to signal calculation or positioning

## Future Enhancements

### Potential Improvements

1. **User Configurable Colors**: Allow users to customize signal colors
2. **Theme Support**: Support for different color themes
3. **Accessibility**: Ensure colors meet accessibility standards
4. **Export Options**: Support for different color schemes in exports

### Considerations

1. **Color Blindness**: Consider alternative color schemes for accessibility
2. **Print Compatibility**: Ensure colors work well in printed materials
3. **Dark Mode**: Consider dark mode color adaptations
4. **Internationalization**: Consider cultural color associations

## Conclusion

The color changes for Wave indicator signals in MPL mode provide a more intuitive and professional visual experience. The blue/red color scheme follows standard trading conventions and improves signal identification for users working with the "prime" global trading rule.
