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

- SMA indicator already implemented (from previous tutorial)
- Basic understanding of matplotlib, seaborn, and terminal plotting
- Access to the neozork-hld-prediction codebase

## Step-by-Step Implementation

### Step 1: Add SMA Support to Matplotlib Mode (-d mpl)

**File:** `src/plotting/dual_chart_mpl.py`

Add SMA indicator support after the EMA section:

```python
elif indicator_name == 'ema':
    y_axis_label = 'Price'
    if 'ema' in display_df.columns:
        ax2.plot(display_df.index, display_df['ema'], 
                color='orange', linewidth=3, label='EMA')

elif indicator_name == 'sma':
    y_axis_label = 'Price'
    if 'sma' in display_df.columns:
        ax2.plot(display_df.index, display_df['sma'], 
                color='blue', linewidth=3, label='SMA')
```

**Key Features:**
- Uses matplotlib's `ax2.plot()` for line plotting
- Blue color scheme consistent with other modes
- Linewidth of 3 for good visibility
- Proper label for legend

### Step 2: Add SMA Support to Seaborn Mode (-d sb)

**File:** `src/plotting/dual_chart_seaborn.py`

Add SMA indicator support after the EMA section:

```python
elif indicator_name == 'ema':
    if 'ema' in display_df.columns:
        sns.lineplot(data=display_df, x=display_df.index, y='ema', 
                    ax=ax2, color='orange', linewidth=3, label='EMA')

elif indicator_name == 'sma':
    if 'sma' in display_df.columns:
        sns.lineplot(data=display_df, x=display_df.index, y='sma', 
                    ax=ax2, color='blue', linewidth=3, label='SMA')
```

**Key Features:**
- Uses seaborn's `sns.lineplot()` for modern styling
- Blue color scheme consistent with other modes
- Linewidth of 3 for good visibility
- Proper label for legend
- Integrates with seaborn's modern aesthetic

### Step 3: Terminal Mode (-d term) Support

The terminal mode (`-d term`) automatically supports SMA through the existing indicator column detection system. The `dual_chart_terminal.py` file already includes logic to:

1. **Detect indicator columns** based on the rule name
2. **Display indicator data** in tabular format
3. **Show summary statistics** for the indicator

**Automatic Support:**
```python
# Find indicator columns
indicator_columns = []
for col in display_df.columns:
    if col.lower().startswith(indicator_name.lower()):
        indicator_columns.append(col)

# Display indicator data
if indicator_columns:
    # Create indicator table header
    indicator_header = f"{'Date':<20}"
    for col in indicator_columns:
        indicator_header += f" {col:<15}"
    output_lines.append(indicator_header)
```

## Testing Your Implementation

### Test Matplotlib Mode

```bash
# Test SMA with matplotlib mode
uv run run_analysis.py show csv mn1 -d mpl --rule sma:20,close

# Test with different parameters
uv run run_analysis.py show csv mn1 -d mpl --rule sma:50,open
```

**Expected Output:**
- Dual chart with OHLC candlesticks on top
- SMA line in blue on secondary chart
- Proper legend and axis labels
- Interactive matplotlib window

### Test Seaborn Mode

```bash
# Test SMA with seaborn mode
uv run run_analysis.py show csv mn1 -d sb --rule sma:20,close

# Test with different parameters
uv run run_analysis.py show csv mn1 -d sb --rule sma:50,open
```

**Expected Output:**
- Modern seaborn-styled dual chart
- SMA line in blue on secondary chart
- Clean, professional appearance
- Saved as PNG file

### Test Terminal Mode

```bash
# Test SMA with terminal mode
uv run run_analysis.py show csv mn1 -d term --rule sma:20,close

# Test with different parameters
uv run run_analysis.py show csv mn1 -d term --rule sma:50,open
```

**Expected Output:**
- Terminal-based dual chart display
- SMA data in tabular format
- Summary statistics
- Navigation controls for chunked viewing

## Code Integration Details

### Matplotlib Integration

The matplotlib mode uses the standard matplotlib plotting library:

```python
# Key integration points
elif indicator_name == 'sma':
    y_axis_label = 'Price'  # Set Y-axis label
    if 'sma' in display_df.columns:  # Check if SMA data exists
        ax2.plot(display_df.index, display_df['sma'],  # Plot SMA line
                color='blue', linewidth=3, label='SMA')  # Styling
```

### Seaborn Integration

The seaborn mode uses seaborn's enhanced plotting capabilities:

```python
# Key integration points
elif indicator_name == 'sma':
    if 'sma' in display_df.columns:  # Check if SMA data exists
        sns.lineplot(data=display_df, x=display_df.index, y='sma',  # Plot SMA line
                    ax=ax2, color='blue', linewidth=3, label='SMA')  # Styling
```

### Terminal Integration

The terminal mode automatically handles SMA through its generic indicator system:

```python
# Automatic indicator detection
indicator_name = rule.split(':', 1)[0].lower().strip() if ':' in rule else rule

# Find indicator columns
indicator_columns = []
for col in display_df.columns:
    if col.lower().startswith(indicator_name.lower()):
        indicator_columns.append(col)
```

## Verification Commands

### 1. Test All Modes

```bash
# Test all three modes with SMA
uv run run_analysis.py show csv mn1 -d mpl --rule sma:20,close
uv run run_analysis.py show csv mn1 -d sb --rule sma:20,close
uv run run_analysis.py show csv mn1 -d term --rule sma:20,close
```

### 2. Test Different Parameters

```bash
# Test with different SMA periods
uv run run_analysis.py show csv mn1 -d mpl --rule sma:10,close
uv run run_analysis.py show csv mn1 -d sb --rule sma:50,close
uv run run_analysis.py show csv mn1 -d term --rule sma:100,close

# Test with different price types
uv run run_analysis.py show csv mn1 -d mpl --rule sma:20,open
uv run run_analysis.py show csv mn1 -d sb --rule sma:20,open
uv run run_analysis.py show csv mn1 -d term --rule sma:20,open
```

### 3. Verify Help System

```bash
# Test help system for all modes
uv run run_analysis.py show csv mn1 -d mpl --rule sma:invalid
uv run run_analysis.py show csv mn1 -d sb --rule sma:invalid
uv run run_analysis.py show csv mn1 -d term --rule sma:invalid
```

## Expected Results

### Matplotlib Mode (-d mpl)
- ✅ Interactive matplotlib window opens
- ✅ OHLC candlesticks on main chart
- ✅ Blue SMA line on secondary chart
- ✅ Proper legend and axis labels
- ✅ Support/resistance levels displayed

### Seaborn Mode (-d sb)
- ✅ Modern seaborn-styled chart
- ✅ OHLC candlesticks on main chart
- ✅ Blue SMA line on secondary chart
- ✅ Professional appearance
- ✅ PNG file saved to results/plots/

### Terminal Mode (-d term)
- ✅ Terminal-based display
- ✅ OHLC data in tabular format
- ✅ SMA values in separate table
- ✅ Summary statistics
- ✅ Navigation controls for chunked viewing

## Troubleshooting

### Common Issues

1. **SMA line not appearing**
   - Check if 'sma' column exists in display_df
   - Verify indicator calculation completed successfully
   - Ensure proper column name matching

2. **Wrong colors or styling**
   - Verify color='blue' is set correctly
   - Check linewidth=3 for visibility
   - Ensure proper label='SMA' for legend

3. **Terminal mode not showing SMA data**
   - Check indicator column detection logic
   - Verify rule parsing works correctly
   - Ensure SMA calculation added 'sma' column

### Debug Commands

```bash
# Debug with verbose output
uv run run_analysis.py show csv mn1 -d mpl --rule sma:20,close --verbose

# Check data structure
uv run run_analysis.py show csv mn1 --rule sma:20,close --debug
```

## Best Practices

### 1. Consistent Styling
- Use blue color for SMA across all modes
- Maintain linewidth=3 for good visibility
- Use consistent label='SMA' for legends

### 2. Error Handling
- Always check if 'sma' column exists before plotting
- Provide fallback behavior if data is missing
- Log appropriate messages for debugging

### 3. Performance
- Matplotlib mode: Interactive, good for analysis
- Seaborn mode: Static images, good for reports
- Terminal mode: Text-based, good for servers/automation

### 4. Integration
- Follow existing code patterns in each file
- Maintain consistency with other indicators
- Ensure proper axis labels and legends

## Summary

You have successfully added SMA indicator support to all remaining dual chart modes:

✅ **Matplotlib Mode (-d mpl)**: Interactive plotting with blue SMA line
✅ **Seaborn Mode (-d sb)**: Modern styled charts with blue SMA line  
✅ **Terminal Mode (-d term)**: Text-based display with SMA data tables

All modes now support:
- SMA calculation and display
- Consistent blue color scheme
- Proper legends and labels
- Error handling and validation
- Integration with existing help system

The SMA indicator is now fully integrated across all dual chart modes in the neozork-hld-prediction platform!
