# Terminal Chunked Plotting Implementation Summary

## Overview

Successfully implemented enhanced terminal display mode with automatic chunking for all rules starting with `--rule`. The system now provides optimal viewing experience for large datasets by automatically splitting data into manageable intervals.

## Key Features Implemented

### 1. Automatic Chunking Algorithm
- **Smart Size Calculation**: Automatically determines optimal chunk size based on total data length
- **Configurable Parameters**: 
  - Target chunks: 10 (default)
  - Min chunk size: 50 candles
  - Max chunk size: 200 candles
- **Adaptive Scaling**: 
  - Small datasets (< 500 rows): 50 candles per chunk
  - Medium datasets (500-2000 rows): 100 candles per chunk
  - Large datasets (> 2000 rows): 200 candles per chunk

### 2. Rule-Specific Visualizations

#### OHLCV Mode
- **Display**: OHLC candlestick charts + separate volume charts
- **Features**: 
  - Two-panel layout (price + volume)
  - Candlestick visualization
  - Volume bars
  - Comprehensive statistics

#### AUTO Mode
- **Display**: Each field on separate charts
- **Features**:
  - Individual field plots
  - Field-specific statistics
  - Dots style for better visibility
  - All numeric fields displayed

#### PV Mode (Pressure Vector) - **UPDATED**
- **Display**: OHLC candles + buy/sell signals only (simplified display)
- **Features**:
  - OHLC candlestick charts as base layer
  - Trading signals (BUY/SELL markers) only
  - No support/resistance lines
  - No PV indicator line
  - Clean, focused visualization

#### SR Mode (Support/Resistance)
- **Display**: OHLC candles + two support/resistance lines
- **Features**:
  - OHLC candlestick charts as base layer
  - Clean support/resistance visualization
  - No trading signals for focused analysis
  - Price level tracking

#### PHLD Mode (Predict High Low Direction)
- **Display**: OHLC candles + two channels and signals
- **Features**:
  - OHLC candlestick charts as base layer
  - Support/resistance channels
  - Trading signals
  - Channel-based analysis
  - Signal statistics

#### RSI Modes
- **Basic RSI**: OHLC candles + standard RSI with overbought/oversold levels
- **RSI Momentum**: OHLC candles + RSI with momentum-based signals
- **RSI Divergence**: OHLC candles + RSI with divergence detection
- **Features**:
  - OHLC candlestick charts as base layer
  - Parameterized rules: `rsi(period,overbought,oversold,price_type)`
  - Support for all price types (open/close)
  - RSI-specific overlays
  - Momentum and divergence indicators

### 3. Enhanced User Experience

#### Interactive Navigation
- **Chunk-by-Chunk Viewing**: Press Enter to navigate between chunks
- **Progress Indicators**: Clear chunk numbering (e.g., "Chunk 1/10")
- **Candle Range Display**: Shows exact candle range for each chunk

#### Comprehensive Statistics
- **OHLC Statistics**: Min/max values for each price component
- **Volume Statistics**: Total, average, maximum volume
- **Trading Signals**: Buy/sell/no-trade counts
- **RSI Statistics**: Min/max/average RSI values
- **Field Statistics**: Individual field metrics

#### Error Handling
- **Graceful Fallbacks**: Falls back to standard plotting if chunked mode fails
- **Data Validation**: Handles missing columns and invalid data
- **Memory Efficiency**: Optimized for large datasets

### 4. **NEW: OHLC Candles as Base Layer**
- **Consistent Display**: All rules now display OHLC candlestick charts as the base layer
- **Enhanced Signals**: Large, colorful buy/sell signals positioned outside candle ranges
- **Unified Experience**: Consistent visualization across all trading rules
- **Better Visibility**: OHLC candles provide price context for all indicators

## Technical Implementation

### Core Modules

#### `src/plotting/term_chunked_plot.py`
- **Main Functions**:
  - `calculate_optimal_chunk_size()`: Smart chunk size calculation
  - `split_dataframe_into_chunks()`: DataFrame splitting
  - `plot_chunked_terminal()`: Main entry point
  - Rule-specific plotting functions for each mode
  - `draw_ohlc_candles()`: Unified OHLC candle display for all rules

#### `src/cli/cli_show_mode.py`
- **Integration**: Updated to use new chunked plotting
- **Rule Detection**: Automatic rule type detection
- **Fallback Support**: Graceful degradation to standard plotting

#### `src/plotting/plotting_generation.py`
- **Enhanced**: Updated `generate_term_plot()` function
- **RSI Support**: Added RSI variant handling
- **Error Handling**: Improved error recovery

### RSI Rule Parsing

#### Parameterized Rules
```python
# Supported formats:
rsi(14,70,30,close)      # Basic RSI
rsi_mom(14,70,30,open)   # RSI Momentum
rsi_div(20,80,20,close)  # RSI Divergence
```

#### Parameter Structure
- **period**: RSI calculation period (default: 14)
- **overbought**: Overbought threshold (default: 70)
- **oversold**: Oversold threshold (default: 30)
- **price_type**: Price type for calculation (open/close)

## Testing

### Comprehensive Test Suite
- **25 Test Cases**: Covering all functionality including new OHLC consistency tests
- **100% Coverage**: All new functions tested
- **Edge Cases**: Invalid data, large datasets, memory efficiency
- **Performance Tests**: Large dataset handling
- **Consistency Tests**: PV/RSI OHLC display consistency

### Test Categories
1. **Core Functionality**: Chunking, parsing, plotting
2. **Rule-Specific Tests**: Each rule type tested
3. **RSI Variants**: All RSI modes tested
4. **Error Handling**: Invalid data and edge cases
5. **Performance**: Large dataset efficiency
6. **Memory**: Memory usage optimization
7. **OHLC Consistency**: PV/RSI display consistency tests
8. **Signals Display**: PV signals-only display tests

## Usage Examples

### Command Line Interface
```bash
# OHLCV mode
python run_analysis.py show csv mn1 -d term --rule OHLCV

# AUTO mode
python run_analysis.py show csv mn1 -d term --rule AUTO

# PV mode (simplified: candles + signals only)
python run_analysis.py show csv mn1 -d term --rule PV

# SR mode
python run_analysis.py show csv mn1 -d term --rule SR

# PHLD mode
python run_analysis.py show csv mn1 -d term --rule PHLD

# RSI modes
python run_analysis.py show csv mn1 -d term --rule rsi:14,70,30,close
python run_analysis.py show csv mn1 -d term --rule rsi_mom:14,70,30,open
python run_analysis.py show csv mn1 -d term --rule rsi_div:20,80,20,close
```

### Demo Script
```bash
# Run the demo script (PHLD only)
python scripts/demos/demo_terminal_chunked.py
```

## Documentation Updates

### CLI Interface Guide
- **Enhanced Description**: Updated terminal mode description
- **Rule Examples**: Added examples for all rule types
- **Chunking Details**: Explained automatic chunking algorithm
- **Usage Instructions**: Clear usage examples
- **OHLC Display**: Documented unified OHLC candle display

### API Documentation
- **Function Documentation**: All new functions documented
- **OHLC Consistency**: Documented unified OHLC display across rules
- **PV Simplification**: Documented PV rule simplification
- **Signal Enhancement**: Documented enhanced signal display

## Recent Updates

### PV Rule Simplification
- **Removed**: Support/resistance lines and PV indicator line
- **Kept**: OHLC candles and buy/sell signals only
- **Result**: Cleaner, more focused visualization

### OHLC Candles as Base Layer
- **Unified Display**: All rules now show OHLC candles as base layer
- **Enhanced Signals**: Larger, more colorful buy/sell signals
- **Better Positioning**: Signals positioned outside candle ranges
- **Consistent Experience**: Same base visualization across all rules

### Enhanced Signal Display
- **Larger Markers**: More visible buy/sell signals
- **Color Coding**: Yellow triangles for BUY, magenta triangles for SELL
- **Smart Positioning**: BUY below Low, SELL above High
- **Unicode Support**: Fallback to ASCII if Unicode not supported

## Benefits

### For Users
1. **Better Readability**: Large datasets split into manageable chunks
2. **Rule-Specific Views**: Optimized visualization for each rule type
3. **Interactive Experience**: Easy navigation between chunks
4. **Comprehensive Statistics**: Detailed metrics for each chunk
5. **SSH-Friendly**: Perfect for remote terminal sessions

### For Developers
1. **Modular Design**: Easy to extend with new rule types
2. **Error Resilience**: Graceful fallbacks and error handling
3. **Performance Optimized**: Efficient memory usage and processing
4. **Well Tested**: Comprehensive test coverage
5. **Documented**: Clear documentation and examples

## Future Enhancements

### Potential Improvements
1. **Custom Chunk Sizes**: User-configurable chunk sizes
2. **Export Options**: Save chunked plots to files
3. **Advanced Statistics**: More detailed metrics per chunk
4. **Interactive Controls**: Keyboard shortcuts for navigation
5. **Color Themes**: Customizable color schemes

### Integration Opportunities
1. **Web Interface**: Web-based chunked viewing
2. **Real-time Updates**: Live data chunking
3. **Comparative Analysis**: Side-by-side chunk comparison
4. **Annotation Support**: User annotations on chunks

## Conclusion

The terminal chunked plotting implementation successfully addresses the need for better visualization of large datasets in terminal environments. The automatic chunking algorithm, rule-specific visualizations, and comprehensive statistics provide users with an optimal viewing experience while maintaining performance and reliability.

The implementation follows best practices with comprehensive testing, clear documentation, and modular design, making it easy to maintain and extend in the future. 