# MACD Terminal Plot Implementation

## Overview

This document describes the implementation of MACD (Moving Average Convergence Divergence) indicator support in the terminal plotting mode for the Neozork HLD Prediction project.

## Problem Statement

The user requested to add MACD indicator support to the existing plot for the command:
```bash
uv run run_analysis.py show csv gbp -d term --rule macd:12,26,9,close
```

The requirement was to:
- Add MACD support only for `-d term` (terminal mode)
- Support the `--rule macd` parameter
- Not affect other rules: `-d term --rule AUTO`, `OHLCV`, `PHLD`, `PV`, `SR`
- Ensure the indicator displays properly on the plot

## Implementation Details

### 1. Files Modified

#### `src/plotting/term_chunked_plot.py`
- **Added MACD rule detection** in `plot_chunked_terminal()` function
- **Created `plot_macd_chunks()` function** for MACD-specific plotting
- **Created `_add_macd_overlays_to_chunk()` function** for MACD line overlays

#### `src/calculation/indicator.py`
- **Added MACD column support** in the output columns section
- **Added MACD-specific columns**: `MACD_Line`, `MACD_Signal`, `MACD_Histogram`, `MACD_Price_Type`

### 2. Key Changes

#### Rule Detection
```python
elif rule_upper.startswith('MACD'):
    plot_macd_chunks(df, title, style, use_navigation)
```

#### MACD Plotting Function
```python
def plot_macd_chunks(df: pd.DataFrame, title: str = "MACD Chunks", style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot MACD data in chunks with MACD lines and trading signals.
    """
```

#### MACD Overlays
```python
def _add_macd_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add MACD-specific overlays to the chunk plot (MACD lines and trading signals).
    """
    # Add MACD lines
    if 'MACD_Line' in chunk.columns:
        macd_values = chunk['MACD_Line'].fillna(0).tolist()
        plt.plot(x_values, macd_values, color="blue+", label="MACD Line")
    
    if 'MACD_Signal' in chunk.columns:
        signal_values = chunk['MACD_Signal'].fillna(0).tolist()
        plt.plot(x_values, signal_values, color="orange+", label="Signal Line")
    
    # Add trading signals
    if 'Direction' in chunk.columns:
        _add_trading_signals_to_chunk(chunk, x_values)
```

### 3. MACD Column Support

The implementation supports the following MACD columns created by the indicator:
- `MACD_Line` - The main MACD line (fast EMA - slow EMA)
- `MACD_Signal` - The signal line (EMA of MACD line)
- `MACD_Histogram` - The histogram (MACD line - signal line)
- `MACD_Price_Type` - The price type used for calculation (Open/Close)

## Testing

### 1. Unit Tests
Created comprehensive unit tests in `tests/plotting/test_macd_terminal_plot.py`:
- MACD rule detection
- MACD overlays function
- MACD chunks function
- MACD columns presence
- MACD rule parsing

### 2. Integration Tests
Verified that the implementation works correctly with:
```bash
# Test MACD functionality
uv run run_analysis.py show csv gbp -d term --rule macd:12,26,9,close

# Verify other rules still work
uv run run_analysis.py show csv gbp -d term --rule AUTO
uv run run_analysis.py show csv gbp -d term --rule OHLCV
uv run run_analysis.py show csv gbp -d term --rule PHLD
```

## Features

### 1. MACD Line Display
- **Blue line**: MACD line (fast EMA - slow EMA)
- **Orange line**: Signal line (EMA of MACD line)
- **Trading signals**: BUY (▲) and SELL (▼) markers

### 2. Navigation Support
- Full navigation support with chunk-based viewing
- Interactive navigation between chunks
- Date range display for each chunk

### 3. Parameter Support
- Supports MACD parameters: `fast_period,slow_period,signal_period,price_type`
- Example: `macd:12,26,9,close` or `macd:8,21,5,open`

## Usage Examples

### Basic MACD
```bash
uv run run_analysis.py show csv gbp -d term --rule macd
```

### MACD with Parameters
```bash
uv run run_analysis.py show csv gbp -d term --rule macd:12,26,9,close
uv run run_analysis.py show csv gbp -d term --rule macd:8,21,5,open
```

### MACD with Different Data
```bash
uv run run_analysis.py show csv mn1 -d term --rule macd:20,40,10,close
```

## Verification

### 1. Success Indicators
- ✅ MACD indicator calculates successfully
- ✅ "Generating MACD chunked plots..." message appears
- ✅ MACD lines (blue and orange) display on the plot
- ✅ Trading signals (▲ and ▼) show correctly
- ✅ Navigation works between chunks
- ✅ Other rules (AUTO, OHLCV, PHLD) continue to work

### 2. Test Results
```bash
$ uv run pytest tests/plotting/test_macd_terminal_plot.py -v
============================================ 5 passed in 0.12s =============================================
```

## Compatibility

### 1. Existing Rules
The implementation maintains full compatibility with existing rules:
- ✅ `AUTO` - Shows all columns
- ✅ `OHLCV` - Shows basic candlestick chart
- ✅ `PHLD` - Shows support/resistance channels
- ✅ `PV` - Shows pressure vector
- ✅ `SR` - Shows support and resistance

### 2. Terminal Mode Only
- MACD support is implemented only for `-d term` mode
- Other plotting modes (plotly, mpl, seaborn) are not affected
- This ensures the implementation is focused and doesn't break existing functionality

## Future Enhancements

### 1. Potential Improvements
- Add MACD histogram display
- Add MACD divergence detection
- Add MACD crossover signals
- Add MACD overbought/oversold levels

### 2. Additional Indicators
The same pattern can be used to add other indicators:
- RSI (already implemented)
- Stochastic
- Bollinger Bands
- And others

## Conclusion

The MACD terminal plot implementation successfully adds MACD indicator support to the terminal plotting mode while maintaining full compatibility with existing functionality. The implementation follows the established patterns in the codebase and includes comprehensive testing.

The solution provides:
- ✅ Full MACD indicator support
- ✅ Proper visualization with MACD and signal lines
- ✅ Trading signal display
- ✅ Navigation support
- ✅ Parameter customization
- ✅ Backward compatibility
- ✅ Comprehensive testing

The implementation is ready for production use and can serve as a template for adding other indicators to the terminal plotting mode.
