# Pivot Indicator Fix for Dual Chart Fastest Mode

## Problem

When using the command `uv run run_analysis.py show csv mn1 -d fastest --rule pivot:open`, the following error occurred:

```
Final plotting mode selected: 'fastest'
Dual chart mode detected for rule: pivot:open
Error: Error in dual chart plotting: tuple indices must be integers or slices, not str. Falling back to standard plotting.
Generating plot using Plotly...
```

## Root Cause

The error occurred in the file `src/plotting/dual_chart_plot.py` in the `calculate_additional_indicator` function. The `calculate_pivot_points` function returns a tuple of three elements `(pivot_point, resistance_1, support_1)`, but the code was trying to access the result as a dictionary:

```python
# Incorrect code (before fix)
pivot_result = calculate_pivot_points(df, price_type)
result_df['pivot'] = pivot_result['pivot']  # Error: pivot_result is a tuple, not a dictionary
result_df['r1'] = pivot_result['r1']
result_df['r2'] = pivot_result['r2']
result_df['s1'] = pivot_result['s1']
result_df['s2'] = pivot_result['s2']
```

## Fix

Fixed the code in file `src/plotting/dual_chart_plot.py` (lines 256-264):

```python
# Correct code (after fix)
elif indicator_name == 'pivot':
    price_type = 'open' if len(params) > 0 and params[0].lower() == 'open' else 'close'
    
    # calculate_pivot_points returns tuple: (pivot_point, resistance_1, support_1)
    pivot_point, resistance_1, support_1 = calculate_pivot_points(df, price_type)
    result_df['pivot'] = pivot_point
    result_df['r1'] = resistance_1
    result_df['s1'] = support_1
```

## Changes

1. **Removed non-existent columns**: Removed references to `r2` and `s2` which are not returned by the `calculate_pivot_points` function
2. **Proper tuple unpacking**: The function result is now properly unpacked into separate variables
3. **Added comment**: Explanation that the function returns a tuple

## Testing

Created test `tests/plotting/test_dual_chart_pivot_fix.py` to verify the fix:

- `test_pivot_open_rule_no_error`: Verifies that the `pivot:open` rule doesn't cause an error
- `test_pivot_close_rule_no_error`: Verifies that the `pivot:close` rule doesn't cause an error  
- `test_pivot_default_rule_no_error`: Verifies that the `pivot:close` rule (default) doesn't cause an error
- `test_pivot_values_are_reasonable`: Verifies that pivot point values are within reasonable limits
- `test_pivot_relationship_holds`: Verifies mathematical relationships between pivot points (R1 ≥ Pivot ≥ S1)

## Result

After the fix, the command `uv run run_analysis.py show csv mn1 -d fastest --rule pivot:open` executes successfully and creates a dual chart with pivot points without errors.

## Files Affected by the Fix

- `src/plotting/dual_chart_plot.py` - main fix
- `tests/plotting/test_dual_chart_pivot_fix.py` - new test
- `docs/development/pivot_indicator_fix.md` - this documentation

## Related Indicators

A similar problem could have occurred with other indicators that return tuples:
- `calculate_donchain` - returns `(upper, middle, lower)`
- `calculate_fiboretr` - returns `(fib_236, fib_382, fib_618)`  
- `calculate_adx` - returns `(adx, plus_di, minus_di)`

These indicators are already properly handled in the code. 