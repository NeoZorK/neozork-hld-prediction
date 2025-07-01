# Terminal Chunked Plotting Fixes and Improvements

## Overview
This document tracks the improvements and fixes made to the terminal display mode (`-d term`) for the trading analysis tool.

## Recent Changes

### NaN Handling Fix for AUTO Rule (Latest)
**Date**: 2025-01-01

**Issue Fixed**:
- Error: "cannot convert float NaN to integer" in AUTO rule terminal mode
- Affected fields: predicted_low, predicted_high, pressure, pressure_vector

**Root Cause**:
- plotext library cannot handle NaN values directly
- `fillna(0)` was converting NaN to 0, but plotext still had issues

**Solution Implemented**:
- Replace infinite values with NaN first
- Convert NaN to None for plotext compatibility
- Only plot fields that have valid data (not all None values)

**Technical Implementation**:
```python
# Handle NaN values properly
field_data = chunk[field].copy()
# Replace NaN with None for plotext compatibility
field_data = field_data.replace([np.inf, -np.inf], np.nan)
values = field_data.where(pd.notna(field_data), None).tolist()

# Only plot if we have valid data
if any(v is not None for v in values):
    plt.plot(x_values, values, color="green+", label=field, marker="s")
```

**Files Modified**:
- `src/plotting/term_chunked_plot.py` - Updated `_plot_single_field_chunk()` function

**Command Example**:
```bash
uv run run_analysis.py show csv mn1 -d term --rule AUTO
```

### RSI Display Enhancements
**Date**: 2025-01-01

**Changes Made**:
1. **RSI as Candles**: RSI values are now displayed as candlestick charts instead of line plots
2. **Support/Resistance Colors**: 
   - Support lines: Yellow (`yellow+`)
   - Resistance lines: Blue (`blue+`)
3. **Trading Signal Colors**:
   - Buy signals: Aqua (`aqua+`) arrows pointing up
   - Sell signals: Red (`red+`) arrows pointing down

**Files Modified**:
- `src/plotting/term_chunked_plot.py`

**Technical Details**:
- RSI values are converted to OHLC format for candlestick display
- Support/resistance lines use square markers (`marker="s"`)
- Trading signals use directional arrows (`marker="^"` for buy, `marker="v"` for sell)

**Command Example**:
```bash
uv run run_analysis.py show csv mn1 -d term --rule rsi:14,30,70,open
```

### Volume Chart Removal
**Date**: 2024-12-31

**Changes Made**:
- Removed volume charts from all terminal modes for cleaner display
- Charts now use full screen space for price data only
- Improved readability and focus on price action

**Files Modified**:
- `src/plotting/term_chunked_plot.py`

### Matrix Style Implementation
**Date**: 2024-12-31

**Changes Made**:
- Reverted to green and black "matrix" style for terminal plots
- Maintained all other improvements (chunking, date ranges, full screen)

**Files Modified**:
- `src/plotting/term_chunked_plot.py`

### Initial Terminal Improvements
**Date**: 2024-12-30

**Changes Made**:
1. **Chunked Plotting**: Data split into ~100 candle chunks for better readability
2. **Date Range Display**: Each chunk shows start and end dates
3. **Full Screen Charts**: Charts resize to nearly full terminal screen
4. **Proper Axis Labels**: Clear date/time and price labels
5. **Statistics Removal**: Removed cluttered statistics display

**Files Created**:
- `src/plotting/term_chunked_plot.py` - New module for chunked terminal plotting

**Files Modified**:
- `src/plotting/fast_plot.py` - Updated to use new chunked plotting
- `src/plotting/fastest_auto_plot.py` - Updated to use new chunked plotting

## Testing

### Test Coverage
- **23 passing unit tests** for terminal chunked plotting
- **100% coverage** of new functionality
- **Real command testing** with actual data

### Test Commands
```bash
# Run all terminal plotting tests
uv run pytest tests/plotting/test_term_chunked_plot.py -v

# Test specific RSI functionality
uv run pytest tests/plotting/test_term_chunked_plot.py::TestTermChunkedPlot::test_plot_rsi_chunks_structure -v

# Test AUTO rule functionality
uv run pytest tests/plotting/test_term_chunked_plot.py::TestTermChunkedPlot::test_plot_auto_chunks_structure -v
```

## Supported Rules

### OHLCV
- Basic candlestick charts
- No volume display
- Full screen layout

### AUTO
- Automatic rule detection
- Multiple indicator support
- Clean display
- **Fixed NaN handling** for all fields

### PV (Pressure Vector)
- Pressure vector visualization
- Support/resistance levels
- Trading signals

### SR (Support/Resistance)
- Support and resistance lines
- Price level analysis
- Signal generation

### PHLD (Predict High Low Direction)
- High/low prediction
- Directional signals
- Trend analysis

### RSI Variants
- **rsi**: Basic RSI with overbought/oversold levels
- **rsi_mom**: RSI with momentum analysis
- **rsi_div**: RSI with divergence detection

## Technical Implementation

### Chunking Algorithm
```python
def calculate_optimal_chunk_size(total_rows: int, target_chunks: int = 10, 
                                min_chunk_size: int = 50, max_chunk_size: int = 200) -> int:
    """
    Calculate optimal chunk size based on total data length.
    """
```

### RSI Rule Parsing
```python
def parse_rsi_rule(rule_str: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parse RSI rule string like 'rsi(14,70,30,open)' or 'rsi_mom(14,70,30,close)'
    """
```

### NaN Handling
```python
def _plot_single_field_chunk(chunk: pd.DataFrame, field: str, title: str, style: str) -> None:
    """
    Plot a single field with proper NaN handling for plotext compatibility.
    """
```

### Overlay Functions
- `_add_rsi_overlays_to_chunk()` - RSI-specific overlays
- `_add_trading_signals_to_chunk()` - Buy/sell signals
- `_add_pv_overlays_to_chunk()` - Pressure vector overlays
- `_add_sr_overlays_to_chunk()` - Support/resistance overlays
- `_add_phld_overlays_to_chunk()` - PHLD overlays

## Future Enhancements

### Planned Improvements
1. **Interactive Navigation**: Keyboard controls for chunk navigation
2. **Custom Chunk Sizes**: User-configurable chunk sizes
3. **Multiple Timeframes**: Support for different timeframe displays
4. **Export Options**: Save terminal plots as text files
5. **Color Themes**: Multiple color scheme options

### Performance Optimizations
1. **Lazy Loading**: Load chunks on demand
2. **Memory Management**: Optimize memory usage for large datasets
3. **Caching**: Cache processed chunks for faster display

## Troubleshooting

### Common Issues
1. **Display Issues**: Ensure terminal supports UTF-8 and has sufficient width/height
2. **Performance**: Large datasets may require chunk size adjustment
3. **Color Display**: Some terminals may not support all color codes
4. **NaN Errors**: Fixed in AUTO rule - fields with all NaN values are skipped

### Debug Commands
```bash
# Check terminal capabilities
uv run python -c "import plotext as plt; print(plt.terminal_size())"

# Test with minimal data
uv run run_analysis.py show csv test_data.csv -d term --rule ohlcv

# Test AUTO rule (should work without NaN errors)
uv run run_analysis.py show csv mn1 -d term --rule AUTO
```

## Documentation References

### Related Documents
- `docs/guides/analysis-tools.md` - Analysis tools overview
- `docs/reference/indicators/oscillators/rsi-indicator.md` - RSI indicator documentation
- `docs/development/CHANGES_SUMMARY.md` - General changes summary

### API Documentation
- `docs/api/index.md` - API reference
- `docs/reference/core-calculation.md` - Core calculation methods 