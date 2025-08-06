# Terminal Plot Size Update for -d term Mode

## Summary

Updated the terminal plot size for `-d term` mode to increase the chart height from 25 lines to 45 lines (10% reduction from full 50 lines instead of 50% reduction).

## Change Details

### Before:
- **Height**: 25 lines (50% reduction from 50 lines)
- **Result**: Very compact, but potentially too small for detailed viewing

### After:
- **Height**: 45 lines (10% reduction from 50 lines)
- **Result**: Better balance between compactness and readability

## Code Changes

Updated the `get_terminal_plot_size()` function in `src/plotting/term_chunked_plot.py`:

```python
def get_terminal_plot_size() -> Tuple[int, int]:
    """
    Determine the plot size for terminal mode based on whether -d term is used.
    
    Returns:
        Tuple[int, int]: (width, height) for the plot
    """
    # Check if -d term is explicitly used in command line arguments
    is_term_mode = False
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv):
            if arg in ['-d', '--draw'] and i + 1 < len(sys.argv):
                if sys.argv[i + 1] == 'term':
                    is_term_mode = True
                    break
    
    if is_term_mode:
        # Reduced height for -d term mode
        return (200, 45)  # Reduced from 50 to 45 (10% reduction)
    else:
        # Default size for other terminal modes
        return (200, 50)
```

## Testing Results

### Test 1: -d term mode (updated height)
```bash
uv run run_analysis.py show csv gbp -d term
```
**Result**: ✅ Chart displays with 45-line height (improved readability)

### Test 2: Other modes (unchanged)
```bash
uv run run_analysis.py show csv gbp -d fastest
```
**Result**: ✅ Chart displays with full height (no change)

## Benefits

1. **Better Readability**: 45 lines provide more detail while still being compact
2. **Improved User Experience**: Better balance between size and information density
3. **Maintained Compatibility**: All other plotting modes remain unchanged
4. **Consistent Logic**: Same conditional detection, just different height value

## Files Modified

- `src/plotting/term_chunked_plot.py` - Updated height from 25 to 45 lines
- `docs/development/TERMINAL_PLOT_SIZE_REDUCTION_SUMMARY.md` - Updated documentation

## Technical Details

- **Detection Method**: Same `sys.argv` parsing logic
- **Height Change**: 25 → 45 lines (20-line increase)
- **Reduction**: 50% → 10% reduction from full size
- **Performance**: No impact (same function call overhead)

## Future Considerations

- Could make height configurable via environment variable
- Could add command-line parameter for custom heights
- Could implement different heights for different terminal types 