# Adding SMA Indicator to All Display Modes - Complete Tutorial

## Overview

This comprehensive tutorial demonstrates how to add the **SMA (Simple Moving Average)** indicator to all display modes in the neozork-hld-prediction platform. The SMA indicator is already fully implemented and serves as a perfect example of how to add custom indicators to the platform.

## What You'll Learn

- ✅ How SMA indicator is integrated into all display modes
- ✅ How to use SMA with different plotting backends
- ✅ How modern help system works for SMA
- ✅ How to test SMA across all modes
- ✅ Best practices for indicator implementation

## Prerequisites

- Basic understanding of Python and pandas
- Access to the neozork-hld-prediction codebase
- UV package manager installed

## Display Modes Overview

The platform supports multiple display modes for different use cases:

| Mode | Backend | Use Case | Performance |
|------|---------|----------|-------------|
| `fastest` | Plotly + Dask + Datashader | Large datasets, best performance | ⭐⭐⭐⭐⭐ |
| `fast` | Dask + Datashader + Bokeh | Quick visualization | ⭐⭐⭐⭐ |
| `plotly` | Plotly | Interactive analysis | ⭐⭐⭐ |
| `mpl` | Matplotlib Finance | Professional charts | ⭐⭐⭐ |
| `sb` | Seaborn | Statistical analysis | ⭐⭐⭐ |
| `term` | Plotext | Terminal/SSH environments | ⭐⭐ |

## SMA Indicator Implementation

### 1. Core SMA Module

**File:** `src/calculation/indicators/trend/sma_ind.py`

The SMA indicator is implemented as a complete module with:

- **Calculation function**: `calculate_sma()`
- **Signal generation**: `calculate_sma_signals()`
- **Rule application**: `apply_rule_sma()`

```python
def calculate_sma(price_series: pd.Series, period: int = 20) -> pd.Series:
    """Calculate Simple Moving Average."""
    if period <= 0:
        raise ValueError("SMA period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for SMA calculation")
        return pd.Series(index=price_series.index, dtype=float)
    
    return price_series.rolling(window=period, min_periods=period).mean()
```

### 2. Platform Integration

#### Constants and Rules
- **File:** `src/common/constants.py`
  - Added `SMA = 12` to TradingRule enum

- **File:** `src/calculation/rules.py`
  - Imported `apply_rule_sma`
  - Added SMA to RULE_FUNCTIONS dictionary

#### CLI Integration
- **File:** `src/cli/cli.py`
  - Added SMA to valid indicators list
  - Added `parse_sma_parameters()` function
  - Added SMA to help system

#### Modern Help System
- **File:** `src/cli/error_handling.py`
  - Comprehensive SMA help information
  - Examples, tips, and common errors

## Using SMA Across All Display Modes

### 1. Fastest Mode (Default)

```bash
# Basic SMA usage
uv run run_analysis.py demo --rule sma:20,close -d fastest

# Custom period and price type
uv run run_analysis.py demo --rule sma:50,open -d fastest

# With real data
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest
```

**Features:**
- Best performance for large datasets
- Interactive Plotly charts
- Datashader for efficient rendering
- Hover tooltips with detailed information

### 2. Fast Mode

```bash
# Fast mode with SMA
uv run run_analysis.py demo --rule sma:20,close -d fast

# Multiple indicators
uv run run_analysis.py demo --rule sma:20,close,rsi:14 -d fast
```

**Features:**
- Bokeh-based interactive charts
- Good performance for medium datasets
- Multiple indicator support

### 3. Plotly Mode

```bash
# Interactive Plotly charts
uv run run_analysis.py demo --rule sma:20,close -d plotly

# Alternative syntax
uv run run_analysis.py demo --rule sma:20,close -d plt
```

**Features:**
- Full interactive capabilities
- Zoom, pan, hover tooltips
- Export to HTML
- Professional appearance

### 4. Matplotlib Finance Mode

```bash
# Professional candlestick charts
uv run run_analysis.py demo --rule sma:20,close -d mpl

# Alternative syntax
uv run run_analysis.py demo --rule sma:20,close -d mplfinance
```

**Features:**
- Professional candlestick charts
- Static image output
- Publication-ready quality
- Traditional technical analysis style

### 5. Seaborn Mode

```bash
# Statistical analysis plots
uv run run_analysis.py demo --rule sma:20,close -d seaborn

# Alternative syntax
uv run run_analysis.py demo --rule sma:20,close -d sb
```

**Features:**
- Statistical analysis focus
- Clean, modern styling
- Good for research and analysis
- Multiple plot types

### 6. Terminal Mode

```bash
# Terminal-based charts
uv run run_analysis.py demo --rule sma:20,close -d term

# Perfect for SSH/remote access
uv run run_analysis.py yfinance --ticker BTC-USD --period 1mo --point 0.01 --rule sma:20,close -d term
```

**Features:**
- Text-based charts
- Works in any terminal
- No GUI dependencies
- Perfect for servers and SSH

## SMA Parameters and Usage

### Parameter Format
```
sma:period,price_type
```

### Parameters
- **period** (int): SMA calculation period (default: 20)
- **price_type** (string): Price type for calculation (open/close, default: close)

### Examples

```bash
# Standard SMA with close prices
uv run run_analysis.py demo --rule sma:20,close -d fastest

# Long-term SMA with open prices
uv run run_analysis.py demo --rule sma:50,open -d plotly

# Short-term SMA for day trading
uv run run_analysis.py demo --rule sma:10,close -d mpl

# Multiple SMAs for comparison
uv run run_analysis.py demo --rule sma:20,close,sma:50,close -d fastest
```

## Modern Help System

### Getting Help

```bash
# General help
uv run run_analysis.py --help

# SMA-specific help
uv run run_analysis.py demo --rule sma --help

# Show mode help
uv run run_analysis.py show --help
```

### Help Features
- **Comprehensive parameter descriptions**
- **Usage examples**
- **Tips and best practices**
- **Common error solutions**
- **Interactive help system**

## Testing SMA Across All Modes

### Automated Testing

```bash
# Run all tests
uv run pytest tests/ -n auto

# Test SMA specifically
uv run pytest tests/calculation/indicators/trend/test_sma_indicator.py -v

# Test CLI integration
uv run pytest tests/cli/ -k "sma" -v

# Test plotting modes
uv run pytest tests/plotting/ -k "sma" -v
```

### Manual Testing

```bash
# Test each mode with SMA
for mode in fastest fast plotly mpl seaborn term; do
    echo "Testing $mode mode..."
    uv run run_analysis.py demo --rule sma:20,close -d $mode
done
```

## Implementation Details

### 1. Dual Chart Support

Each plotting mode includes SMA support:

#### Fastest Mode
```python
def add_sma_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """Add SMA indicator to the secondary subplot."""
    if 'sma' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['sma'],
                mode='lines',
                name='SMA',
                line=dict(color='blue', width=2)
            ),
            row=2, col=1
        )
```

#### Fast Mode
```python
def _plot_sma_indicator(indicator_fig, source, display_df):
    """Plot SMA indicator on the given figure."""
    if 'sma' in display_df.columns:
        indicator_fig.line(
            'index', 'sma',
            source=source,
            line_color='blue',
            line_width=3,
            legend_label='SMA'
        )
```

#### Terminal Mode
```python
def _add_sma_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SMA indicator to subplot."""
    sma_columns = [col for col in chunk.columns if col.upper().startswith('SMA')]
    for sma_col in sma_columns:
        sma_values = chunk[sma_col].fillna(0).tolist()
        plt.plot(x_values, sma_values, color="blue+", label=sma_col)
```

### 2. CLI Integration

#### Parameter Parsing
```python
def parse_sma_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SMA parameters: period,price_type"""
    try:
        params = params_str.split(',')
        if len(params) != 2:
            raise ValueError(f"SMA requires exactly 2 parameters")
        
        period = int(params[0])
        price_type = params[1].lower()
        
        if price_type not in ['open', 'close']:
            raise ValueError(f"SMA price_type must be 'open' or 'close'")
        
        return 'sma', {
            'sma_period': period,
            'price_type': PriceType.OPEN if price_type == 'open' else PriceType.CLOSE
        }
    except Exception as e:
        raise ValueError(f"Invalid SMA parameters: {params_str}. Error: {e}")
```

#### Help System
```python
'sma': {
    'name': 'SMA (Simple Moving Average)',
    'description': 'Simple moving average that gives equal weight to all prices.',
    'format': 'sma:period,price_type',
    'parameters': [
        ('period', 'int', 'SMA period', '20'),
        ('price_type', 'string', 'Price type for calculation', 'close')
    ],
    'examples': [
        ('sma:20,close', 'Standard SMA with close prices'),
        ('sma:50,open', 'Long-term SMA with open prices')
    ],
    'tips': [
        'Use period 20 for standard analysis',
        'Shorter periods are more responsive',
        'Longer periods provide smoother signals'
    ]
}
```

## Best Practices

### 1. Parameter Validation
- Always validate input parameters
- Provide meaningful error messages
- Use appropriate default values

### 2. Performance Optimization
- Use vectorized operations with pandas
- Handle edge cases (insufficient data)
- Implement efficient calculations

### 3. User Experience
- Provide comprehensive help
- Include usage examples
- Add helpful tips and warnings

### 4. Testing
- Write comprehensive unit tests
- Test all display modes
- Include edge case testing

## Troubleshooting

### Common Issues

1. **"Invalid SMA parameters"**
   - Check parameter format: `sma:period,price_type`
   - Ensure period is positive integer
   - Use 'open' or 'close' for price_type

2. **"No SMA columns found"**
   - Verify indicator calculation completed
   - Check column names in output
   - Ensure proper data format

3. **Performance issues**
   - Use 'fastest' mode for large datasets
   - Consider data filtering
   - Check available memory

### Debug Commands

```bash
# Debug SMA calculation
uv run run_analysis.py demo --rule sma:20,close -d term --debug

# Check data structure
uv run run_analysis.py show data/your_file.parquet

# Test specific mode
uv run run_analysis.py demo --rule sma:20,close -d fastest --verbose
```

## Summary

The SMA indicator demonstrates a complete implementation across all display modes:

✅ **Core Calculation**: Efficient SMA calculation with proper validation  
✅ **Signal Generation**: BUY/SELL signals based on price crosses  
✅ **Multi-Mode Support**: Works in all 6 display modes  
✅ **Modern Help**: Comprehensive help system with examples  
✅ **CLI Integration**: Full command-line support  
✅ **Testing**: Complete test coverage  
✅ **Documentation**: Detailed implementation guide  

This implementation serves as a template for adding other custom indicators to the platform while maintaining consistency across all display modes and providing excellent user experience.

## Next Steps

- Explore other indicators (RSI, MACD, EMA, etc.)
- Learn about custom indicator development
- Study the platform architecture
- Contribute new indicators

For more information, see the [Complete Indicator Development Guide](adding-custom-indicators.md).
