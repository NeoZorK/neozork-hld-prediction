# Terminal Chunked Plot Refactoring Documentation

## Overview

The `term_chunked_plot.py` module has been refactored into multiple smaller, more maintainable modules. This refactoring improves code organization, makes it easier to fix indentation issues, and enhances maintainability.

## Module Structure

The original large file (2757 lines) has been split into the following modules:

### Core Modules

1. **`term_chunked_plot_base.py`**
   - Base utility functions
   - Functions: `get_terminal_plot_size()`, `calculate_optimal_chunk_size()`, `split_dataframe_into_chunks()`, `parse_rsi_rule()`, `draw_ohlc_candles()`

2. **`term_chunked_plot_helpers.py`**
   - Helper functions for colors, field plotting, signals, and statistics
   - Functions: `_get_field_color()`, `_plot_single_field_chunk()`, `_has_trading_signals()`, `_add_trading_signals_to_chunk()`, `_show_chunk_statistics()`, `_show_field_statistics()`

3. **`term_chunked_plot_overlays.py`**
   - Functions to add specific overlays to chunk plots
   - Functions: `_add_pv_overlays_to_chunk()`, `_add_sr_overlays_to_chunk()`, `_add_phld_overlays_to_chunk()`, `_add_rsi_overlays_to_chunk()`, `_add_macd_overlays_to_chunk()`

4. **`term_chunked_plot_indicators.py`**
   - All indicator functions for subplots
   - Functions: `_add_macd_chart_to_subplot()`, `_add_indicator_chart_to_subplot()`, and all `_add_*_indicator_to_subplot()` functions

### Plotting Function Modules

Each plotting function has its own module:

- **`term_chunked_plot_ohlcv.py`** - `plot_ohlcv_chunks()`
- **`term_chunked_plot_auto.py`** - `plot_auto_chunks()`
- **`term_chunked_plot_pv.py`** - `plot_pv_chunks()`
- **`term_chunked_plot_sr.py`** - `plot_sr_chunks()`
- **`term_chunked_plot_phld.py`** - `plot_phld_chunks()`
- **`term_chunked_plot_rsi.py`** - `plot_rsi_chunks()`
- **`term_chunked_plot_macd.py`** - `plot_macd_chunks()`
- **`term_chunked_plot_indicator.py`** - `plot_indicator_chunks()`

### Main Module

**`term_chunked_plot.py`**
- Main entry point that imports and re-exports all functions
- Contains `plot_chunked_terminal()` function
- Maintains backward compatibility with existing code

## Import Structure

All functions are still imported from the main module for backward compatibility:

```python
from src.plotting.term_chunked_plot import (
    plot_ohlcv_chunks,
    plot_auto_chunks,
    plot_pv_chunks,
    plot_sr_chunks,
    plot_phld_chunks,
    plot_rsi_chunks,
    plot_macd_chunks,
    plot_indicator_chunks,
    plot_chunked_terminal,
    calculate_optimal_chunk_size,
    split_dataframe_into_chunks,
    parse_rsi_rule,
    get_terminal_plot_size,
    draw_ohlc_candles,
    _add_wave_indicator_to_subplot,
)
```

## Benefits of Refactoring

1. **Easier Maintenance**: Each module is now less than 300 lines, making it easier to understand and maintain
2. **Simplified Indentation Fixes**: Each file can be fixed independently
3. **Better Organization**: Related functions are grouped together logically
4. **Improved Testability**: Smaller modules are easier to test
5. **Backward Compatibility**: All existing code continues to work without changes

## File Sizes

After refactoring:
- `term_chunked_plot.py`: ~135 lines (main entry point)
- `term_chunked_plot_base.py`: ~150 lines
- `term_chunked_plot_helpers.py`: ~300 lines
- `term_chunked_plot_overlays.py`: ~200 lines
- `term_chunked_plot_indicators.py`: ~887 lines (largest, but contains all indicator functions)
- Individual plotting modules: ~150-250 lines each

## Testing

All tests continue to work with the refactored structure. The main test file is:
- `tests/plotting/test_term_chunked_plot.py`
- `tests/src/plotting/test_term_chunked_plot.py`
- `tests/plotting/test_wave_terminal_plot.py`

Tests import functions from the main `term_chunked_plot` module, so no test changes are required.

## Migration Guide

No migration is required! All existing code continues to work because:
1. All functions are re-exported from the main module
2. Function signatures remain unchanged
3. Import paths remain the same

## Future Improvements

With the refactored structure, future improvements can include:
1. Further splitting of large indicator functions
2. Adding unit tests for individual modules
3. Creating base classes for common plotting functionality
4. Implementing better error handling patterns
5. Adding type hints consistently across all modules

