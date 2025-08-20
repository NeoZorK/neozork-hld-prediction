# Wave Indicator Terminal Signals Fix

## Summary

Fixed the signal display logic in terminal mode (`-d term`) to match other plotting modes by using only `_Signal` column for trading signals instead of `_Plot_Color`, ensuring consistent behavior across all display modes.

## Problem

The terminal mode was displaying too many BUY/SELL signals on the upper chart because it was using the `_Plot_Color` column, which contains continuous signals for every data point. Other modes (mpl, seaborn, fastest, fast) use the `_Signal` column, which only contains signals when the wave direction actually changes.

## Solution

### 1. Updated Signal Detection Logic

**File**: `src/plotting/term_chunked_plot.py`

#### Modified `_has_trading_signals()` Function
```python
def _has_trading_signals(chunk: pd.DataFrame) -> bool:
    """Check if chunk has any trading signals."""
    return any(col in chunk.columns for col in ['Direction', '_Signal'])
```

**Changes**:
- Removed `_Plot_Color` from signal detection
- Now only checks for `_Signal` and `Direction` columns
- Matches the logic used in other plotting modes

#### Updated `_add_trading_signals_to_chunk()` Function
```python
def _add_trading_signals_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add trading signals to the chunk plot.
    BUY: large yellow triangle below Low
    SELL: large magenta triangle above High
    
    Supports signal sources (same as other modes):
    - _Signal column (wave indicator - only direction changes)
    - Direction column (standard indicator)
    """
    try:
        # Check for different signal sources (same priority as other modes)
        signal_source = None
        if '_Signal' in chunk.columns:
            signal_source = '_Signal'
        elif 'Direction' in chunk.columns:
            signal_source = 'Direction'
        else:
            return
        
        # Process signals using _Signal column (only direction changes)
        # ...
```

**Changes**:
- Removed support for `_Plot_Color` column
- Prioritizes `_Signal` over `Direction` (same as other modes)
- Only displays signals when wave direction changes

### 2. Updated All Signal Check Locations

Used `sed` command to replace all instances of:
```python
if 'Direction' in chunk.columns:
```
with:
```python
if _has_trading_signals(chunk):
```

**Locations Updated**:
- `plot_macd_chunks()` function
- `plot_indicator_chunks()` function  
- `plot_dual_chart_chunks()` function
- `plot_dual_chart_chunks_with_navigation()` function

### 3. Updated Tests

**File**: `tests/plotting/test_wave_terminal_signals.py`

**Changes**:
- Removed tests for `_Plot_Color` column
- Updated all tests to use `_Signal` column
- Maintained test coverage for new logic

## Results

### Before Fix
- **Signal Source**: `_Plot_Color` (continuous signals)
- **Signal Frequency**: Every data point with wave activity
- **Signal Count**: Too many signals cluttering the chart
- **Consistency**: Different from other modes

### After Fix
- **Signal Source**: `_Signal` (direction changes only)
- **Signal Frequency**: Only when wave direction changes
- **Signal Count**: Appropriate number of meaningful signals
- **Consistency**: Matches other plotting modes exactly

## Verification

### Test Commands
```bash
# Test with demo data
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d term

# Test with real data
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d term
```

### Expected Behavior
- **Upper Chart**: Shows BUY/SELL signals only when wave direction changes
- **Signal Count**: Significantly reduced, matching other modes
- **Signal Quality**: More meaningful trading signals
- **Visual Clarity**: Cleaner chart without signal clutter

## Impact

### Positive Effects
1. **Consistency**: Terminal mode now matches other plotting modes
2. **Signal Quality**: Only meaningful direction change signals displayed
3. **Visual Clarity**: Reduced signal clutter on price chart
4. **User Experience**: More intuitive signal interpretation

### Technical Benefits
1. **Code Consistency**: Same signal logic across all modes
2. **Maintainability**: Unified approach to signal handling
3. **Performance**: Reduced processing for signal display
4. **Reliability**: Consistent behavior across different data sources

## Documentation Updates

### Updated Files
1. **`docs/guides/wave-indicator-terminal-mode.md`**
   - Updated signal logic description
   - Added comparison table with other modes
   - Clarified signal source and frequency
   - Added troubleshooting section

2. **`tests/plotting/test_wave_terminal_signals.py`**
   - Updated all tests to use `_Signal` column
   - Removed `_Plot_Color` related tests
   - Maintained comprehensive test coverage

## Future Considerations

### Potential Enhancements
1. **Signal Filtering**: Add options for signal strength filtering
2. **Custom Signal Sources**: Allow user-defined signal column selection
3. **Signal Validation**: Add validation for signal consistency
4. **Performance Optimization**: Further optimize signal processing

### Monitoring
- Monitor signal quality across different timeframes
- Validate consistency with other plotting modes
- Ensure backward compatibility with existing workflows

## Conclusion

The fix successfully aligns the terminal mode signal display with other plotting modes, providing a consistent and meaningful trading signal experience. The reduction in signal clutter improves chart readability while maintaining the essential trading information that users need for decision-making.
