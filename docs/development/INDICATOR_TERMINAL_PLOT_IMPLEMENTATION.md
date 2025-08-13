# Indicator Terminal Plot Implementation

## Overview

This document describes the implementation of a universal indicator plotting system for terminal mode (`-d term`) that supports all available indicators with dual subplot architecture.

## Architecture

### Dual Subplot Design

The system uses a dual subplot layout where:
- **Top subplot (50% height)**: OHLC candlestick chart with trading signals
- **Bottom subplot (50% height)**: Indicator-specific visualization

This design ensures optimal visibility for both price action and indicator data.

### Universal Function Structure

The implementation consists of:

1. **Main Function**: `plot_indicator_chunks()` - Universal plotting function for all indicators
2. **Dispatcher Function**: `_add_indicator_chart_to_subplot()` - Routes to specific indicator functions
3. **Specialized Functions**: Individual functions for each indicator type

## Supported Indicators

### Momentum Indicators
- **MACD**: Moving Average Convergence Divergence
  - Command: `uv run run_analysis.py show csv gbp -d term --rule macd:12,26,9,close`
  - Features: MACD Line, Signal Line, Histogram

### Oscillators
- **RSI**: Relative Strength Index
  - Command: `uv run run_analysis.py show csv gbp -d term --rule rsi:14,70,30,close`
  - Features: RSI line with overbought/oversold levels (70/30)

- **Stochastic**: Stochastic Oscillator
  - Command: `uv run run_analysis.py show csv gbp -d term --rule stoch:14,3,close`
  - Features: %K and %D lines with overbought/oversold levels (80/20)

- **CCI**: Commodity Channel Index
  - Command: `uv run run_analysis.py show csv gbp -d term --rule cci:20,close`
  - Features: CCI line with overbought/oversold levels (±100)

### Trend Indicators
- **EMA**: Exponential Moving Average
  - Command: `uv run run_analysis.py show csv gbp -d term --rule ema:20,close`
  - Features: Multiple EMA lines

- **ADX**: Average Directional Index
  - Command: `uv run run_analysis.py show csv gbp -d term --rule adx:14`
  - Features: ADX, DI+, DI- lines

- **SAR**: Parabolic SAR
  - Command: `uv run run_analysis.py show csv gbp -d term --rule sar:0.02,0.2`
  - Features: SAR dots

- **SuperTrend**: SuperTrend Indicator
  - Command: `uv run run_analysis.py show csv gbp -d term --rule supertrend:10,3`
  - Features: SuperTrend line

### Volatility Indicators
- **Bollinger Bands**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule bollinger:20,2`
  - Features: Upper, Middle, Lower bands

- **ATR**: Average True Range
  - Command: `uv run run_analysis.py show csv gbp -d term --rule atr:14`
  - Features: ATR line

- **Standard Deviation**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule std:20`
  - Features: Standard deviation line

### Volume Indicators
- **OBV**: On-Balance Volume
  - Command: `uv run run_analysis.py show csv gbp -d term --rule obv`
  - Features: OBV line

- **VWAP**: Volume Weighted Average Price
  - Command: `uv run run_analysis.py show csv gbp -d term --rule vwap`
  - Features: VWAP line

### Predictive Indicators
- **HMA**: Hull Moving Average
  - Command: `uv run run_analysis.py show csv gbp -d term --rule hma:20`
  - Features: HMA line

- **Time Series Forecast**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule tsf:20`
  - Features: TSF line

### Probability Indicators
- **Monte Carlo**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule monte_carlo:1000`
  - Features: Monte Carlo simulation results

- **Kelly Criterion**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule kelly:20`
  - Features: Kelly fraction line

### Sentiment Indicators
- **Put/Call Ratio**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule putcall`
  - Features: Put/Call ratio with neutral line (1.0)

- **COT**: Commitments of Traders
  - Command: `uv run run_analysis.py show csv gbp -d term --rule cot`
  - Features: COT line

- **Fear & Greed**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule fear_greed`
  - Features: Fear & Greed index with extreme levels (20/80)

### Support/Resistance Indicators
- **Pivot Points**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule pivot`
  - Features: PP, R1, R2, R3, S1, S2, S3 levels

- **Fibonacci Retracement**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule fibonacci`
  - Features: Fibonacci levels (0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%)

- **Donchian Channel**
  - Command: `uv run run_analysis.py show csv gbp -d term --rule donchian:20`
  - Features: Upper, Middle, Lower channels

## Implementation Details

### Core Functions

#### `plot_indicator_chunks()`
Universal function that handles all indicators with dual subplot layout:

```python
def plot_indicator_chunks(df: pd.DataFrame, indicator_name: str, title: str = "Indicator Chunks", 
                         style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Universal function to plot any indicator data in chunks with dual subplot layout.
    
    Args:
        df (pd.DataFrame): DataFrame with indicator data
        indicator_name (str): Name of the indicator (RSI, Stochastic, CCI, etc.)
        title (str): Base title for plots
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
```

#### `_add_indicator_chart_to_subplot()`
Dispatcher function that routes to specific indicator functions:

```python
def _add_indicator_chart_to_subplot(chunk: pd.DataFrame, x_values: list, indicator_name: str) -> None:
    """
    Add indicator chart to a separate subplot with proper scaling.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (list): X-axis values
        indicator_name (str): Name of the indicator
    """
```

### Specialized Functions

Each indicator has its own specialized function that handles:
- Data extraction from DataFrame
- Proper scaling and visualization
- Indicator-specific features (overbought/oversold levels, multiple lines, etc.)

Example for RSI:
```python
def _add_rsi_indicator_to_subplot(chunk: pd.DataFrame, x_values: list, rule: str = "") -> None:
    """Add RSI indicator to subplot."""
    try:
        if 'RSI' in chunk.columns:
            rsi_values = chunk['RSI'].fillna(50).tolist()
            plt.plot(x_values, rsi_values, color="purple+", label="RSI")
            
            # Extract overbought/oversold levels from rule
            overbought_level = 70  # default
            oversold_level = 30    # default
            
            if rule and ':' in rule:
                try:
                    # Parse rule like "rsi:14,10,90,open" -> extract 10 and 90
                    params = rule.split(':')[1].split(',')
                    if len(params) >= 3:
                        oversold_level = float(params[1])    # second parameter
                        overbought_level = float(params[2])  # third parameter
                except (ValueError, IndexError):
                    # If parsing fails, use defaults
                    pass
            
            # Add overbought/oversold lines with extracted levels
            plt.plot(x_values, [overbought_level] * len(x_values), color="red+")
            plt.plot(x_values, [oversold_level] * len(x_values), color="green+")
            plt.plot(x_values, [50] * len(x_values), color="white+")
        
    except Exception as e:
        logger.print_error(f"Error adding RSI indicator: {e}")
```

## Integration with Existing System

### Rule Dispatching

The system integrates with the existing rule dispatching mechanism in `plot_chunked_terminal()`:

```python
def plot_chunked_terminal(df: pd.DataFrame, rule: str, title: str = "Chunked Terminal Plot", 
                         style: str = "matrix", use_navigation: bool = False) -> None:
    try:
        rule_upper = rule.upper()
        
        # Handle RSI variants with dual subplot
        if rule_upper.startswith('RSI'):
            plot_indicator_chunks(df, 'RSI', title, style, use_navigation)
        
        # Handle MACD (keep existing MACD logic for compatibility)
        elif rule_upper.startswith('MACD'):
            plot_macd_chunks(df, title, style, use_navigation)
        
        # Handle all other indicators with dual subplot
        elif rule_upper in ['STOCHASTIC', 'CCI', 'BOLLINGER_BANDS', 'EMA', 'ADX', 'SAR', 
                           'SUPERTREND', 'ATR', 'STANDARD_DEVIATION', 'OBV', 'VWAP',
                           'HMA', 'TIME_SERIES_FORECAST', 'MONTE_CARLO', 'KELLY_CRITERION',
                           'PUT_CALL_RATIO', 'COT', 'FEAR_GREED', 'PIVOT_POINTS',
                           'FIBONACCI_RETRACEMENT', 'DONCHIAN_CHANNEL']:
            plot_indicator_chunks(df, rule_upper, title, style, use_navigation)
        
        # Handle parameterized indicators
        elif ':' in rule:
            indicator_name = rule.split(':')[0].upper()
            plot_indicator_chunks(df, indicator_name, title, style, use_navigation)
        
        else:
            # Try to use as generic indicator
            plot_indicator_chunks(df, rule_upper, title, style, use_navigation)
        
    except Exception as e:
        logger.print_error(f"Error in chunked terminal plotting: {e}")
```

## Technical Considerations

### Plotext Compatibility

The implementation is designed to work with the `plotext` library, which has some limitations:
- No support for `linestyle` parameter
- No support for `alpha` parameter
- No support for `axhline` function
- No support for `heights` parameter in subplots

These limitations are handled by:
- Removing unsupported parameters
- Using different colors instead of line styles
- Commenting out unsupported functions

### Error Handling

Each function includes comprehensive error handling:
- Try-catch blocks around all plotting operations
- Graceful fallback for missing data columns
- Informative error messages for debugging

### Performance Optimization

The system is optimized for:
- Efficient data chunking for large datasets
- Minimal memory usage
- Fast rendering in terminal environment

## Custom Level Support

### RSI Custom Levels

The RSI indicator supports customizable overbought/oversold levels through the rule parameter:

**Default Levels**: 30 (oversold) / 70 (overbought)
**Custom Levels**: Can be specified in the rule format `rsi:period,oversold,overbought,price_type`

**Examples**:
- `rsi:14,10,90,open` - Uses levels 10 and 90
- `rsi:14,20,80,close` - Uses levels 20 and 80
- `rsi:14,30,70,high` - Uses default levels 30 and 70

**Implementation**:
- Levels are extracted from the rule parameter during parsing
- Falls back to default levels (30/70) if parsing fails
- Supports any numeric values for custom levels

### Parameter Parsing

The system parses rule parameters in the format:
```
indicator:param1,param2,param3,param4
```

For RSI specifically:
- `param1`: Period (e.g., 14)
- `param2`: Oversold level (e.g., 10, 20, 30)
- `param3`: Overbought level (e.g., 70, 80, 90)
- `param4`: Price type (e.g., open, close, high, low)

## Testing

### Unit Tests

Comprehensive unit tests are available in `tests/plotting/test_indicator_terminal_plot.py`:

- Tests for all individual indicator functions
- Tests for the universal plotting function
- Tests for error handling and edge cases
- Tests for all supported indicator types
- Tests for custom level parsing (RSI)

### Integration Tests

The system has been tested with real data using commands like:
```bash
uv run run_analysis.py show csv gbp -d term --rule rsi:14,70,30,close
uv run run_analysis.py show csv gbp -d term --rule stoch:14,3,close
uv run run_analysis.py show csv gbp -d term --rule cci:20,close
```

## Usage Examples

### Basic Usage
```bash
# RSI with default parameters
uv run run_analysis.py show csv gbp -d term --rule rsi

# RSI with custom parameters
uv run run_analysis.py show csv gbp -d term --rule rsi:14,70,30,close

# Stochastic oscillator
uv run run_analysis.py show csv gbp -d term --rule stoch:14,3,close

# CCI indicator
uv run run_analysis.py show csv gbp -d term --rule cci:20,close
```

### Navigation
All plots support interactive navigation:
- `n` - Next chunk
- `p` - Previous chunk
- `s` - Start (first chunk)
- `e` - End (last chunk)
- `c` - Choose chunk number
- `d` - Choose date
- `q` - Quit

## Future Enhancements

### Planned Features
1. **Custom Color Schemes**: User-configurable colors for different indicators
2. **Multiple Indicators**: Support for displaying multiple indicators simultaneously
3. **Custom Overlays**: User-defined overlay lines and levels
4. **Export Options**: Save plots as text files or images

### Potential Improvements
1. **Performance**: Further optimization for very large datasets
2. **Memory Usage**: Reduced memory footprint for long time series
3. **Visualization**: Enhanced visual elements and styling options
4. **Interactivity**: More advanced navigation and interaction features

## Troubleshooting

### Common Issues

1. **Indicator not displaying**: Check if the indicator column exists in the DataFrame
2. **Plot errors**: Verify that the data contains valid numeric values
3. **Navigation issues**: Ensure the terminal supports the required escape sequences

### Debug Information

The system provides detailed debug information:
- Indicator calculation status
- Data validation results
- Plotting operation logs
- Error messages with context

## Conclusion

The universal indicator terminal plotting system provides a comprehensive solution for displaying all available indicators in terminal mode. The dual subplot architecture ensures optimal visibility while maintaining compatibility with the existing codebase. The modular design allows for easy extension and maintenance.
