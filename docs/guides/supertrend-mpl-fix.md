# SuperTrend MPL Display Fix

## Problem

The SuperTrend indicator was not displaying in `mpl` mode when using the command:
```bash
uv run run_analysis.py show csv gbp -d mpl --rule supertrend:10,3,open
```

## Cause

The file `src/plotting/dual_chart_mpl.py` lacked SuperTrend indicator processing. While other display modes (fastest, fast) had full SuperTrend support, the mpl mode did not contain the corresponding code.

## Solution

Added SuperTrend indicator processing to the file `src/plotting/dual_chart_mpl.py`:

### Added code

```python
elif indicator_name == 'supertrend':
    y_axis_label = 'Price'
    
    # Check for SuperTrend columns
    has_supertrend = 'SuperTrend' in display_df.columns
    has_direction = 'SuperTrend_Direction' in display_df.columns
    has_signal = 'SuperTrend_Signal' in display_df.columns
    
    if has_supertrend:
        # Plot SuperTrend line
        supertrend_values = display_df['SuperTrend']
        ax2.plot(display_df.index, supertrend_values, 
                color='blue', linewidth=3, label='SuperTrend')
        
        # Plot price series for reference
        if 'Open' in display_df.columns:
            ax2.plot(display_df.index, display_df['Open'], 
                    color='gray', linewidth=1, alpha=0.7, label='Price')
        
        # Add trend direction visualization
        if has_direction:
            trend_direction = display_df['SuperTrend_Direction']
            
            # Color segments based on trend direction
            uptrend_mask = trend_direction == 1
            downtrend_mask = trend_direction == -1
            
            if uptrend_mask.any():
                ax2.plot(display_df.index[uptrend_mask], supertrend_values[uptrend_mask], 
                        color='green', linewidth=4, alpha=0.8, label='Uptrend')
            
            if downtrend_mask.any():
                ax2.plot(display_df.index[downtrend_mask], supertrend_values[downtrend_mask], 
                        color='red', linewidth=4, alpha=0.8, label='Downtrend')
        
        # Add signal points
        if has_signal:
            buy_signals = display_df['SuperTrend_Signal'] == 1  # BUY
            sell_signals = display_df['SuperTrend_Signal'] == 2  # SELL
            
            if buy_signals.any():
                ax2.scatter(display_df.index[buy_signals], supertrend_values[buy_signals], 
                          color='green', s=50, marker='^', label='Buy Signal')
            
            if sell_signals.any():
                ax2.scatter(display_df.index[sell_signals], supertrend_values[sell_signals], 
                          color='red', s=50, marker='v', label='Sell Signal')
    
    # Fallback: use PPrice1/PPrice2 if SuperTrend column not available
    elif 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns:
        # Create SuperTrend values from PPrice1/PPrice2
        p1 = display_df['PPrice1']
        p2 = display_df['PPrice2']
        direction = display_df.get('Direction', pd.Series(0, index=display_df.index))
        
        # Use PPrice1 as SuperTrend (support level)
        supertrend_values = p1
        ax2.plot(display_df.index, supertrend_values, 
                color='blue', linewidth=3, label='SuperTrend (Support)')
        
        # Also plot resistance level
        ax2.plot(display_df.index, p2, 
                color='orange', linewidth=2, linestyle='--', label='Resistance')
        
        # Add signal points if available
        if 'Direction' in display_df.columns:
            buy_signals = direction == 1  # BUY
            sell_signals = direction == 2  # SELL
            
            if buy_signals.any():
                ax2.scatter(display_df.index[buy_signals], supertrend_values[buy_signals], 
                          color='green', s=50, marker='^', label='Buy Signal')
            
            if sell_signals.any():
                ax2.scatter(display_df.index[sell_signals], supertrend_values[sell_signals], 
                          color='red', s=50, marker='v', label='Sell Signal')
```

## Functionality

### Main capabilities

1. **SuperTrend line display**: The main indicator line is displayed in blue
2. **Trend direction visualization**: 
   - Green color for uptrend
   - Red color for downtrend
3. **Signal points**:
   - Green upward triangles for buy signals
   - Red downward triangles for sell signals
4. **Fallback mode**: If SuperTrend columns are not available, PPrice1/PPrice2 is used

### Supported parameters

- `period`: ATR period (default: 10)
- `multiplier`: ATR multiplier (default: 3.0)
- `price_type`: Price type (`open` or `close`)

### Usage examples

```bash
# Basic usage
uv run run_analysis.py show csv gbp -d mpl --rule supertrend:10,3,open

# With other parameters
uv run run_analysis.py show csv gbp -d mpl --rule supertrend:14,2.5,close

# Short period, low multiplier (more sensitive)
uv run run_analysis.py show csv gbp -d mpl --rule supertrend:5,2.0,open
```

## Testing

A comprehensive test suite has been created in `tests/plotting/test_dual_chart_mpl_supertrend.py`:

- ✅ Test with SuperTrend columns
- ✅ Test with fallback PPrice1/PPrice2 columns
- ✅ Test signal points
- ✅ Test trend direction
- ✅ Test parameter parsing
- ✅ Test error handling

All tests pass successfully.

## Result

Now the SuperTrend indicator displays correctly in `mpl` mode with all functions:

- ✅ Main SuperTrend line
- ✅ Trend color coding
- ✅ Signal points
- ✅ Support for various parameters
- ✅ Fallback operation mode
- ✅ Complete test coverage

## Compatibility

The fix is fully compatible with existing code and does not affect other indicators or display modes. 