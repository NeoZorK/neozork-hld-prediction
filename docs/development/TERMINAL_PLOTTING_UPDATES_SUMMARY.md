# Terminal Plotting Updates Summary

## Overview

Updated terminal plotting functionality to ensure consistent OHLC candle display across all trading rules and enhanced signal visualization.

## Key Changes Made

### 1. **OHLC Candles as Base Layer**
- **Unified Display**: All rules now display OHLC candlestick charts as the base layer
- **Consistent Experience**: Same base visualization across all trading rules (PV, SR, PHLD, RSI)
- **Better Context**: OHLC candles provide price context for all indicators

### 2. **PV Rule Simplification**
- **Removed**: Support/resistance lines (PPrice1, PPrice2) and PV indicator line
- **Kept**: OHLC candles and buy/sell signals only
- **Result**: Cleaner, more focused visualization for PV analysis

### 3. **Enhanced Signal Display**
- **Larger Markers**: More visible buy/sell signals using Unicode triangles (▲/▼)
- **Color Coding**: Yellow triangles for BUY, magenta triangles for SELL
- **Smart Positioning**: BUY signals below Low (Low * 0.99), SELL signals above High (High * 1.01)
- **Fallback Support**: ASCII symbols (^^/vv) if Unicode not supported

### 4. **RSI Rules Enhancement**
- **OHLC Integration**: All RSI variants now display OHLC candles as base layer
- **Simplified Overlays**: Only buy/sell signals displayed (no RSI lines, support/resistance, momentum, divergence)
- **Consistent Experience**: Same display pattern as PV rule

## Technical Implementation

### Files Modified

#### Core Plotting Files
- `src/plotting/term_chunked_plot.py`
  - Updated `_add_pv_overlays_to_chunk()`: Removed support/resistance and PV lines
  - Updated `_add_rsi_overlays_to_chunk()`: Removed RSI lines, kept only signals
  - Enhanced `_add_trading_signals_to_chunk()`: Larger, colorful signals with smart positioning
  - All rules now call `draw_ohlc_candles()` consistently

#### Demo Script
- `scripts/demo_terminal_chunked.py`
  - Simplified to show only PHLD demonstration
  - Removed other rule demonstrations

### Functions Updated

#### `_add_pv_overlays_to_chunk()`
```python
def _add_pv_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add PV-specific overlays to the chunk plot: ONLY buy/sell signals (no support/resistance, no PV line).
    """
    try:
        # Только сигналы BUY/SELL
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)
    except Exception as e:
        logger.print_error(f"Error adding PV overlays: {e}")
```

#### `_add_rsi_overlays_to_chunk()`
```python
def _add_rsi_overlays_to_chunk(chunk: pd.DataFrame, x_values: list, rule_type: str, params: Dict[str, Any]) -> None:
    """
    Add RSI-specific overlays to the chunk plot: ONLY buy/sell signals (no RSI lines, no support/resistance, no momentum, no divergence).
    """
    try:
        # Только сигналы BUY/SELL
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)
    except Exception as e:
        logger.print_error(f"Error adding RSI overlays: {e}")
```

#### `_add_trading_signals_to_chunk()`
```python
def _add_trading_signals_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add trading signals to the chunk plot.
    BUY: большой желтый треугольник ниже Low
    SELL: большой малиновый треугольник выше High
    """
    # Enhanced signal display with larger markers and smart positioning
```

## Testing Updates

### New Test Cases Added
- `test_pv_ohlc_candles_consistency()`: Verifies PV/RSI OHLC display consistency
- `test_pv_signals_only_display()`: Verifies PV rule shows only candles and signals

### Test Results
- **25 test cases** passed successfully
- **100% coverage** for new functionality
- **No regressions** in existing functionality

## Documentation Updates

### Files Updated
- `docs/guides/cli-interface.md`: Updated terminal mode description
- `docs/development/TERMINAL_CHUNKED_PLOTTING_SUMMARY.md`: Added recent updates section

### Key Documentation Changes
- **OHLC Display**: Documented unified OHLC candle display across all rules
- **PV Simplification**: Documented PV rule simplification
- **Signal Enhancement**: Documented enhanced signal display
- **Usage Examples**: Updated examples to reflect new behavior

## Usage Examples

### PV Rule (Simplified)
```bash
uv run run_analysis.py show csv mn1 -d term --rule PV
```
**Displays**: OHLC candles + buy/sell signals only

### RSI Rules (Enhanced)
```bash
uv run run_analysis.py show csv mn1 -d term --rule rsi:14,30,70,open
uv run run_analysis.py show csv mn1 -d term --rule rsi_mom:14,30,70,open
uv run run_analysis.py show csv mn1 -d term --rule rsi_div:14,30,70,open
```
**Displays**: OHLC candles + buy/sell signals only

### All Other Rules
```bash
uv run run_analysis.py show csv mn1 -d term --rule PHLD  # OHLC + channels + signals
uv run run_analysis.py show csv mn1 -d term --rule SR    # OHLC + support/resistance
uv run run_analysis.py show csv mn1 -d term --rule OHLCV # OHLC + volume
```

## Benefits

### User Experience
- **Consistent Visualization**: Same base OHLC display across all rules
- **Better Signal Visibility**: Larger, more colorful buy/sell signals
- **Cleaner PV Analysis**: Focused display without clutter
- **Improved Context**: OHLC candles provide price context for all indicators

### Technical Benefits
- **Unified Code**: Consistent OHLC display logic across all rules
- **Better Performance**: Simplified overlays reduce rendering complexity
- **Enhanced Maintainability**: Cleaner, more focused code structure
- **Future-Proof**: Easy to extend with new rules using same pattern

## Future Enhancements

### Planned Improvements
1. **Interactive Navigation**: Keyboard controls for chunk navigation
2. **Custom Signal Styles**: User-configurable signal appearance
3. **Additional Indicators**: Support for more technical indicators
4. **Export Options**: Save terminal plots as images or text files

### Potential Features
1. **Signal Filtering**: Show/hide specific signal types
2. **Time Range Selection**: Interactive time range selection
3. **Multi-Timeframe**: Support for multiple timeframes in single view
4. **Custom Themes**: User-configurable color schemes

## Conclusion

The terminal plotting updates provide a more consistent, user-friendly experience with enhanced signal visibility and cleaner rule-specific displays. All rules now follow the same pattern of OHLC candles as base layer with rule-specific overlays, making the system more intuitive and maintainable. 