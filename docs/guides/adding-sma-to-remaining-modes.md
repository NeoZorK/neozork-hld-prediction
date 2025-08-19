# Adding SMA Indicator to Remaining Modes (-d mpl, -d sb, -d term)

## Overview

This tutorial demonstrates how to add SMA (Simple Moving Average) indicator support to the remaining dual chart modes in the neozork-hld-prediction platform. We'll cover the three modes that were not initially supported:

- **`-d mpl`**: Matplotlib-based dual chart mode
- **`-d sb`**: Seaborn-based dual chart mode  
- **`-d term`**: Terminal-based dual chart mode

## What You'll Learn

- ✅ How to add SMA support to matplotlib dual chart mode
- ✅ How to add SMA support to seaborn dual chart mode
- ✅ How to add SMA support to terminal dual chart mode
- ✅ How to test each mode with SMA indicator
- ✅ Best practices for multi-mode indicator integration

## Prerequisites

- SMA indicator already implemented and working with `-d fastest` and `-d fast` modes
- Basic understanding of the platform's plotting architecture
- Access to the neozork-hld-prediction codebase

## Step 1: Add SMA Support to Matplotlib Mode (-d mpl)

### 1.1 Update dual_chart_mpl.py

Add SMA support to the indicator dispatch logic:

```python
# In src/plotting/dual_chart_mpl.py
elif indicator_name == 'sma':
    y_axis_label = 'Price'
    if 'sma' in display_df.columns:
        ax2.plot(display_df.index, display_df['sma'], 
                color='blue', linewidth=3, label='SMA')
```

### 1.2 Test Matplotlib Mode

```bash
uv run run_analysis.py show csv mn1 -d mpl --rule sma:20,close
```

**Expected Result**: Interactive matplotlib window with OHLC chart on top and SMA line on bottom.

## Step 2: Add SMA Support to Seaborn Mode (-d sb)

### 2.1 Update dual_chart_seaborn.py

Add SMA support to the indicator dispatch logic:

```python
# In src/plotting/dual_chart_seaborn.py
elif indicator_name == 'sma':
    if 'sma' in display_df.columns:
        sns.lineplot(data=display_df, x=display_df.index, y='sma', 
                    ax=ax2, color='blue', linewidth=3, label='SMA')
```

### 2.2 Test Seaborn Mode

```bash
uv run run_analysis.py show csv mn1 -d sb --rule sma:20,close
```

**Expected Result**: Interactive seaborn plot with OHLC chart on top and SMA line on bottom.

## Step 3: Add SMA Support to Terminal Mode (-d term)

### 3.1 Update term_chunked_plot.py

Add SMA support to the indicator dispatch logic:

```python
# In src/plotting/term_chunked_plot.py
elif indicator_upper == 'SMA':
    _add_sma_indicator_to_subplot(chunk, x_values)
```

### 3.2 Add SMA Indicator Function

Create the `_add_sma_indicator_to_subplot` function:

```python
def _add_sma_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SMA indicator to subplot."""
    try:
        # Look for SMA columns (case insensitive)
        sma_columns = [col for col in chunk.columns if col.upper().startswith('SMA') or col.lower() == 'sma']
        
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        for sma_col in sma_columns:
            sma_values = chunk[sma_col].fillna(0).tolist()
            try:
                # Try to plot with numeric x_values
                plt.plot(numeric_x_values, sma_values, color="blue+", label=sma_col)
            except Exception as plot_error:
                # If plotting fails, skip this column
                continue
        
        # Debug: print available columns if no SMA found
        if not sma_columns:
            logger.print_warning(f"No SMA columns found. Available columns: {list(chunk.columns)}")
        
    except Exception as e:
        logger.print_error(f"Error adding SMA indicator: {e}")
```

### 3.3 Update Indicator Search Logic

Fix the column search logic in terminal mode:

```python
# In src/plotting/term_chunked_plot.py
# Look for columns containing the indicator name
indicator_columns = [col for col in chunk.columns if indicator_name.upper() in col.upper()]

if not indicator_columns:
    # Try exact match (case insensitive)
    if indicator_name.lower() in [col.lower() for col in chunk.columns]:
        indicator_columns = [col for col in chunk.columns if col.lower() == indicator_name.lower()]
    elif indicator_name in chunk.columns:
        indicator_columns = [indicator_name]
```

### 3.4 Add SMA to Supported Indicators List

Update the list of supported indicators:

```python
# In src/plotting/term_chunked_plot.py
elif rule_upper in ['STOCHASTIC', 'CCI', 'BOLLINGER_BANDS', 'EMA', 'SMA', 'ADX', 'SAR', 
                   'SUPERTREND', 'ATR', 'STANDARD_DEVIATION', 'OBV', 'VWAP',
                   'HMA', 'TIME_SERIES_FORECAST', 'MONTE_CARLO', 'KELLY_CRITERION',
                   'PUT_CALL_RATIO', 'COT', 'FEAR_GREED', 'PIVOT_POINTS',
                   'FIBONACCI_RETRACEMENT', 'DONCHIAN_CHANNEL']:
    plot_indicator_chunks(df, rule_upper, title, style, use_navigation, rule)
```

### 3.5 Add SMA Calculation Support

Add SMA calculation support in `cli_show_mode.py`:

```python
# In src/cli/cli_show_mode.py
# Calculate additional indicator for terminal mode if needed
if ':' in args.rule:
    try:
        from src.plotting.dual_chart_plot import calculate_additional_indicator
        result_df = calculate_additional_indicator(result_df, args.rule)
    except Exception as e:
        print(f"Could not calculate additional indicator: {e}")
```

### 3.6 Test Terminal Mode

```bash
uv run run_analysis.py show csv mn1 -d term --rule sma:20,close
```

**Expected Result**: Terminal-based plot with OHLC chart on top and SMA line on bottom, with navigation controls.

## Step 4: Add SMA to Indicators List

### 4.1 Update indicators_search.py

Add SMA to the trend category:

```python
# In src/cli/indicators_search.py
categories = {
    "trend": ["ema_ind.py", "sma_ind.py", "adx_ind.py", "sar_ind.py", "supertrend_ind.py"],
    # ... other categories
}
```

### 4.2 Test Indicators List

```bash
uv run run_analysis.py --indicators
```

**Expected Result**: SMA should appear in the trend category.

## Step 5: Verify All Modes Work

Test all modes to ensure SMA works correctly:

```bash
# Test all modes
uv run run_analysis.py show csv mn1 -d fastest --rule sma:20,close
uv run run_analysis.py show csv mn1 -d fast --rule sma:20,close
uv run run_analysis.py show csv mn1 -d mpl --rule sma:20,close
uv run run_analysis.py show csv mn1 -d sb --rule sma:20,close
uv run run_analysis.py show csv mn1 -d term --rule sma:20,close
```

## Troubleshooting

### Common Issues

1. **SMA line not appearing in terminal mode**
   - Check if `calculate_additional_indicator` is being called
   - Verify that the `sma` column exists in the DataFrame
   - Check the column search logic in `_add_sma_indicator_to_subplot`

2. **Wrong colors or styling**
   - Ensure consistent color schemes across all modes
   - Check that the plotting libraries support the specified colors

3. **Performance issues**
   - Terminal mode may be slower due to chunked plotting
   - Consider optimizing the SMA calculation for large datasets

### Debug Commands

```bash
# Check if SMA appears in indicators list
uv run run_analysis.py --indicators | grep -i sma

# Test with different parameters
uv run run_analysis.py show csv mn1 -d term --rule sma:50,open

# Check for errors in terminal mode
uv run run_analysis.py show csv mn1 -d term --rule sma:20,close 2>&1 | grep -i error
```

## Best Practices

1. **Consistent Implementation**: Ensure SMA works the same way across all modes
2. **Error Handling**: Add proper error handling for missing columns or calculation failures
3. **Performance**: Optimize calculations for large datasets
4. **Documentation**: Keep documentation updated with new features
5. **Testing**: Test all modes after making changes

## Summary

After completing this tutorial, SMA will be fully supported across all dual chart modes:

- ✅ **fastest**: Plotly-based interactive charts
- ✅ **fast**: Bokeh-based interactive charts  
- ✅ **mpl**: Matplotlib-based interactive charts
- ✅ **sb**: Seaborn-based interactive charts
- ✅ **term**: Terminal-based chunked charts

All modes will display the SMA line in the secondary subplot with consistent styling and functionality.

## Next Steps

1. **Add More Indicators**: Use this pattern to add other indicators to all modes
2. **Optimize Performance**: Improve calculation and plotting performance
3. **Add More Features**: Implement additional indicator parameters and options
4. **Enhance UI**: Improve the user interface and navigation controls
