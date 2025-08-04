# SuperTrend Hover Tool Fix (Fast Mode Only)

## Problem

When using the command with `-d fast` mode:
```bash
uv run run_analysis.py show csv gbp -d fast --rule supertrend:10,3,open
```

The hover tool displayed "???" values for fields:
- Date
- SuperTrend  
- Direction

**Note**: This fix applies only to `-d fast` mode. Other modes (fastest, plotly, mpl, etc.) are not affected.

## Problem Cause

The problem was that the hover tool for the SuperTrend indicator used incorrect data columns:

1. **Incorrect hover mode**: Used `mode='mouse'` instead of `mode='vline'`
2. **Incorrect data columns**: Hover tool always used `@supertrend`, but data could be in `PPrice1`/`PPrice2` columns
3. **Missing data in ColumnDataSource**: Not all necessary columns were passed to the data source

## Solution

### 1. Fix hover mode

Changed hover mode from `mouse` to `vline` for better compatibility:

```python
# Before:
mode='mouse'

# After:
mode='vline'
```

### 2. Dynamic column selection

Added logic for dynamic selection of correct columns:

```python
elif indicator_name == 'supertrend':
    # Check if we have PPrice1/PPrice2 or direct supertrend column
    has_pprice = 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns
    if has_pprice:
        # Use PPrice1 for hover (support level)
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("SuperTrend", "@PPrice1{0.5f}"),
                ("Direction", "@Direction{0.0f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    else:
        # Use direct supertrend column
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("SuperTrend", "@supertrend{0.5f}"),
                ("Direction", "@Direction{0.0f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
```

### 3. Improve data passing to ColumnDataSource

Added ensuring that all necessary columns are passed to the data source:

```python
# Add supertrend values to both display_df and source for hover tool
display_df['supertrend'] = supertrend_values
if source is not None:
    source.data['supertrend'] = supertrend_values
    
    # Also ensure PPrice1 and PPrice2 are in source for fallback hover
    source.data['PPrice1'] = p1
    source.data['PPrice2'] = p2
    
    # Ensure Direction is also in the main source for hover tool
    if 'Direction' not in source.data:
        source.data['Direction'] = direction
        
    # Ensure all required columns are in source for proper hover functionality
    source.data['index'] = display_df['index'] if 'index' in display_df.columns else display_df.index
```

## Testing

Created comprehensive test `tests/plotting/test_fast_supertrend_hover_fix.py` which checks:

1. **Hover with PPrice1/PPrice2 columns**: Verifies that `@PPrice1` is used
2. **Hover with direct supertrend column**: Verifies that `@supertrend` is used
3. **Formatters**: Verifies correctness of date formatters
4. **Missing columns**: Verifies work when some columns are missing
5. **Missing Direction**: Verifies work without Direction column

## Affected Files

- `src/plotting/fast_plot.py` - Main fix for fast mode
- `tests/plotting/test_fast_supertrend_hover_fix.py` - New test for fast mode

## Result

After the fix, the hover tool for SuperTrend indicator correctly displays:

- **Date**: Correct date in YYYY-MM-DD HH:MM format
- **SuperTrend**: Numeric SuperTrend value with 0.5f precision
- **Direction**: Numeric trend direction value with 0.0f precision

## Verification

To verify the fix, run:

```bash
# Test hover tool for fast mode
uv run pytest tests/plotting/test_fast_supertrend_hover_fix.py -v

# Check in browser (fast mode only)
uv run run_analysis.py show csv gbp -d fast --rule supertrend:10,3,open
```

The chart will open in the browser, and when hovering over the SuperTrend indicator, correct values will be displayed instead of "???".

**Important**: This fix works only for `-d fast` mode. For other modes (fastest, plotly, mpl), use the corresponding commands. 