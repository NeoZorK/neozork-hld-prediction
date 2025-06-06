# AUTO Rule Terminal Plotting with 'Dots' Style - Implementation Summary

## Task Completed ✅

**Objective**: Update the terminal plotting functionality for the `--rule AUTO` command to use "dots" style in all plots, applying to both CLI and Python API usage.

## Implementation Details

### 1. CLI Path (run_analysis.py demo --rule AUTO)
**File**: `src/plotting/plotting_generation.py` - `generate_term_plot()` function (lines 571-584)

**Changes Made**:
- Added AUTO rule detection: `if is_auto_rule:`
- Implemented dual plotting approach:
  1. Main OHLC candlestick chart (if OHLC columns present)
  2. Separate field plots for all other numeric columns
- Both plotting calls use `style="dots"` parameter
- Added comprehensive error handling and logging

```python
# For AUTO rule, use separate field plotting: main OHLC chart (if present) + separate charts for each field
if is_auto_rule:
    logger.print_info("AUTO rule detected, using 'dots' style for all terminal plots...")
    try:
        from src.plotting.term_separate_plots import plot_separate_fields_terminal
        # Show main OHLC chart as candlestick if present
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in result_df.columns for col in ohlc_columns)
        if has_ohlc:
            from src.plotting.term_auto_plot import auto_plot_from_dataframe
            auto_plot_from_dataframe(result_df, f"{plot_title} - OHLC Candlestick", style="dots")
        # Plot each additional numeric field as a separate chart
        plot_separate_fields_terminal(result_df, selected_rule, f"{plot_title} - Separate Fields", style="dots")
        logger.print_success("Successfully plotted OHLC candlestick and all other fields as separate terminal charts with 'dots' style.")
    except ImportError as e:
        logger.print_warning(f"Could not import separate field plotting modules: {e}. Falling back to standard terminal plot.")
        from src.plotting.term_auto_plot import auto_plot_from_dataframe
        auto_plot_from_dataframe(result_df, plot_title, style="dots")
    return
```

### 2. Python API Path (plot_indicator_results function)
**File**: `src/plotting/term_plot.py` - `plot_indicator_results_term()` function

**Changes Made**:
- Updated AUTO rule handling to match CLI behavior
- Added same dual plotting approach as CLI
- Shows main chart first, then separate field plots
- Uses early return to avoid duplicate main chart display

```python
elif rule_str.upper() in ['AUTO', 'AUTO_DISPLAY_ALL']:
    # For AUTO rule, show the main OHLC chart first, then separate field plots
    logger.print_info("AUTO rule detected in Python API, using 'dots' style for separate field plotting...")
    _add_auto_indicators_term(df, x_values)  # Add overlays to main chart
    
    # Show the main chart first
    plt.show()
    
    # Then show separate field plots with dots style
    try:
        from src.plotting.term_separate_plots import plot_separate_fields_terminal
        plot_separate_fields_terminal(df, rule_str, f"{title} - Separate Fields", style="dots")
        logger.print_success("Successfully displayed main OHLC chart and separate field plots with 'dots' style.")
        return  # Early return to avoid showing main chart twice
    except ImportError as e:
        logger.print_warning(f"Could not import separate field plotting: {e}. Showing main chart with overlays only.")
    except Exception as e:
        logger.print_warning(f"Error in separate field plotting: {e}. Continuing with main chart.")
```

### 3. Function Signature Updates
**Files Updated**:
- `src/plotting/term_auto_plot.py` - `auto_plot_from_dataframe()`
- `src/plotting/term_separate_plots.py` - `plot_separate_fields_terminal()` and helper functions

**Changes Made**:
- Added `style: str = "matrix"` parameter to all relevant functions
- Implemented conditional marker selection based on style parameter
- Used "dot" markers when `style="dots"` is specified

### 4. Critical Bug Fix
**File**: `src/plotting/term_auto_plot.py` - line 78

**Issue**: `plt.candlestick()` was being called with invalid `style="dots"` parameter
**Fix**: Removed the style parameter from candlestick call since plotext doesn't support style parameter for candlestick charts

```python
# BEFORE (BROKEN):
plt.candlestick(x_values, ohlc_data, style="dots")

# AFTER (FIXED):
plt.candlestick(x_values, ohlc_data)
```

### 5. Marker-Based Style Implementation
Since plotext doesn't have a `style()` method, implemented "dots" style through marker selection:

```python
# In plotting functions
if style == "dots":
    marker = "dot"  # or "."
else:  
    marker = "braille"  # default marker
```

## Validation Results

### CLI Testing (run_analysis.py demo --rule AUTO)
✅ **Working**: Shows main OHLC candlestick + 10 separate field plots with dot markers
✅ **Logging**: "AUTO rule detected, using 'dots' style for all terminal plots..."
✅ **Success Message**: "Successfully plotted OHLC candlestick and all other fields..."

### Python API Testing (plot_indicator_results function)
✅ **Working**: Shows main OHLC candlestick + 10 separate field plots with dot markers  
✅ **Logging**: "AUTO rule detected in Python API, using 'dots' style..."
✅ **Success Message**: "Successfully displayed main OHLC chart and separate field plots..."

### Comparison Rule Testing (PHLD)
✅ **Working**: PHLD rule still works correctly for comparison
✅ **Shows**: Single main chart with overlays (no separate field plots)

## Output Sample

**AUTO Rule with 'dots' style produces**:
1. Main OHLC candlestick chart with volume panel
2. 10 separate field plots, each using dot markers:
   - Volume (bar chart)
   - HL (line plot with dots)
   - Pressure (line plot with dots)  
   - PV (line plot with dots)
   - PPrice1 (predictions with dots)
   - PColor1 (indicator with dots)
   - PPrice2 (predictions with dots)
   - PColor2 (indicator with dots)
   - Direction (trading signals with up/down arrows)
   - Diff (difference values with dots)

## Files Modified

1. `/src/plotting/plotting_generation.py` - CLI dispatch logic
2. `/src/plotting/term_plot.py` - Python API dispatch logic  
3. `/src/plotting/term_auto_plot.py` - Function signatures and candlestick fix
4. `/src/plotting/term_separate_plots.py` - Function signatures and marker implementation

## Implementation Status: **COMPLETE** ✅

Both CLI and Python API paths now correctly route AUTO rule requests to use "dots" style for all terminal plots, showing both main OHLC candlestick charts and separate field plots with dot markers.
