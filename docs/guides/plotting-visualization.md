# Plotting and Visualization Guide

Complete guide to plotting and visualization capabilities in the Neozork HLD Prediction project.

## Overview

The plotting module provides multiple visualization backends and specialized plotting functions for financial data analysis.

## Available Plotting Backends

### 1. Matplotlib (`plotting.py`)

Traditional static plotting with high customization.

#### Features
- **Static plots** - High-quality static images
- **Customizable** - Full control over appearance
- **Publication ready** - Professional quality output
- **Multiple formats** - PNG, PDF, SVG, JPG

#### Usage Example

```python
from src.plotting.plotting import create_plot

# Create basic OHLCV plot
plot = create_plot(
    data=price_data,
    indicators={'rsi': rsi_data, 'macd': macd_data},
    title='AAPL Analysis',
    save_path='plots/aapl_analysis.png'
)
```

### 2. Plotly (`plotly_plot.py`)

Interactive web-based plotting.

#### Features
- **Interactive plots** - Zoom, pan, hover tooltips
- **Web integration** - Embed in web applications
- **Real-time updates** - Dynamic data visualization
- **Multiple chart types** - Candlestick, line, bar charts

#### Usage Example

```python
from src.plotting.plotly_plot import create_interactive_plot

# Create interactive plot
fig = create_interactive_plot(
    data=price_data,
    indicators={'rsi': rsi_data},
    title='Interactive AAPL Analysis'
)

# Display in browser
fig.show()

# Save as HTML
fig.write_html('plots/interactive_aapl.html')
```

### 3. Seaborn (`seaborn_plot.py`)

Statistical data visualization.

#### Features
- **Statistical plots** - Distribution, correlation analysis
- **Modern aesthetics** - Clean, professional appearance
- **Statistical insights** - Built-in statistical analysis
- **Integration** - Works with pandas and matplotlib

#### Usage Example

```python
from src.plotting.seaborn_plot import create_statistical_plot

# Create statistical analysis plot
plot = create_statistical_plot(
    data=price_data,
    analysis_type='correlation',
    title='Price Correlation Analysis'
)
```

### 4. MPLFinance (`mplfinance_plot.py`)

Specialized financial plotting.

#### Features
- **Financial charts** - Candlestick, OHLC charts
- **Technical indicators** - Built-in indicator plotting
- **Volume analysis** - Volume profile visualization
- **Pattern recognition** - Chart pattern identification

#### Usage Example

```python
from src.plotting.mplfinance_plot import create_financial_plot

# Create financial chart
plot = create_financial_plot(
    data=price_data,
    indicators=['rsi', 'macd'],
    volume=True,
    title='Financial Analysis'
)
```

### 5. Terminal (`term_plot.py`)

ASCII/Unicode plotting for terminal environments.

#### Features
- **Terminal output** - No GUI required
- **Lightweight** - Minimal resource usage
- **Remote friendly** - Works on servers
- **Real-time** - Live data visualization

#### Usage Example

```python
from src.plotting.term_plot import create_terminal_plot

# Create terminal plot
plot = create_terminal_plot(
    data=price_data,
    width=80,
    height=20,
    title='Terminal Analysis'
)

# Display in terminal
print(plot)
```

## Specialized Plotting Functions

### 1. Dual Chart Fast (`dual_chart_fast.py`) - **REFACTORED**

Optimized dual-chart plotting with modular indicator functions.

#### Features
- **Modular Architecture**: 21 individual indicator functions for easy maintenance
- **Dynamic Height**: Automatic screen height detection and adjustment
- **Enhanced Performance**: Bokeh-based rendering for large datasets
- **Comprehensive Testing**: 31 new test cases with 100% pass rate
- **Backward Compatibility**: 100% compatible with existing code

#### Recent Refactoring (2025-07-05)
- **21 Indicator Functions**: Each indicator type has its own dedicated function
- **Improved Code Organization**: Main function reduced from ~760 to ~200 lines
- **Enhanced Maintainability**: Easy to add new indicators or modify existing ones
- **Better Testability**: Independent testing of each indicator function

#### Usage Example

```python
from src.plotting.dual_chart_fast import plot_dual_chart_fast

# Create dual chart with dynamic height
result = plot_dual_chart_fast(
    df=data,
    rule="macd:8,21,5,open",
    title="MACD Analysis",
    height=None  # Triggers dynamic calculation
)

# With custom dimensions (will be reduced by 10%)
result = plot_dual_chart_fast(
    df=data,
    rule="rsi:14,30,70,open",
    title="RSI Analysis",
    width=1800,
    height=1100
)
```

#### Supported Indicators
All 21 indicators are supported with individual plotting functions:
- RSI, MACD, EMA, Bollinger Bands, ATR, CCI, VWAP, Pivot Points
- HMA, TSF, Monte Carlo, Kelly, Donchian Channel, Fibonacci
- OBV, Standard Deviation, ADX, SAR, RSI Momentum, RSI Divergence, Stochastic

### 2. Fast Plotting (`fast_plot.py`)

Optimized for speed and performance.

#### Features
- **High performance** - Optimized for large datasets
- **Memory efficient** - Minimal memory usage
- **Batch processing** - Multiple plots simultaneously
- **Caching** - Reuse plot components

#### Usage Example

```python
from src.plotting.fast_plot import create_fast_plot

# Create fast plot
plot = create_fast_plot(
    data=price_data,
    indicators=['rsi', 'macd'],
    optimize_for='speed',
    cache_enabled=True
)
```

### 2. Auto Plotting (`fastest_auto_plot.py`)

Automatic plot generation with smart defaults.

#### Features
- **Auto-detection** - Automatically choose best plot type
- **Smart defaults** - Optimal settings for data type
- **Batch processing** - Generate multiple plots
- **Template system** - Reusable plot templates

#### Usage Example

```python
from src.plotting.fastest_auto_plot import create_auto_plot

# Create auto plot
plot = create_auto_plot(
    data=price_data,
    indicators=indicator_data,
    template='financial_analysis'
)
```

### 3. Testing and Quality Assurance

#### Dual Chart Fast Testing
```bash
# Run comprehensive refactored tests
uv run pytest tests/plotting/test_dual_chart_fast_refactored.py -v

# Run all dual chart fast tests
uv run pytest tests/plotting/test_dual_chart_fast_*.py -v

# Test specific indicator functions
uv run pytest tests/plotting/test_dual_chart_fast_refactored.py::TestDualChartFastRefactored::test_plot_rsi_indicator -v
```

#### Test Coverage
- **31 New Tests**: Covering all 21 indicator functions
- **10 Original Tests**: Ensuring backward compatibility
- **Total**: 41 tests with 100% pass rate
- **Coverage**: All indicator functions and edge cases tested

### 3. PHLD Plotting (`term_phld_plot.py`)

Specialized plotting for PHLD (Price High Low Direction) analysis.

#### Features
- **PHLD visualization** - Specialized PHLD charts
- **Direction indicators** - Clear buy/sell signals
- **Confidence levels** - Signal strength visualization
- **Pattern recognition** - PHLD pattern identification

#### Usage Example

```python
from src.plotting.term_phld_plot import create_phld_plot

# Create PHLD plot
plot = create_phld_plot(
    data=price_data,
    phld_signals=phld_data,
    confidence_threshold=0.7,
    show_patterns=True
)
```

### 4. Pressure Vector Plotting (`fixed_term_pv_plot.py`)

Specialized plotting for Pressure Vector analysis.

#### Features
- **Vector visualization** - Pressure direction and magnitude
- **Component analysis** - Individual vector components
- **Threshold levels** - Pressure threshold visualization
- **Trend analysis** - Pressure trend identification

#### Usage Example

```python
from src.plotting.fixed_term_pv_plot import create_pv_plot

# Create Pressure Vector plot
plot = create_pv_plot(
    data=price_data,
    pv_data=pressure_vector_data,
    show_components=True,
    threshold_levels=[0.5, 0.7, 0.9]
)
```

### 5. Support Resistance Plotting (`fixed_term_sr_plot.py`)

Specialized plotting for Support/Resistance analysis.

#### Features
- **Level visualization** - Support and resistance levels
- **Strength indicators** - Level strength visualization
- **Breakout detection** - Level break identification
- **Historical analysis** - Level persistence over time

#### Usage Example

```python
from src.plotting.fixed_term_sr_plot import create_sr_plot

# Create Support/Resistance plot
plot = create_sr_plot(
    data=price_data,
    sr_levels=support_resistance_data,
    show_strength=True,
    breakout_alerts=True
)
```

## Plot Generation System (`plotting_generation.py`)

Advanced plot generation with multiple backends.

### Features
- **Multi-backend support** - Choose from all available backends
- **Template system** - Predefined plot templates
- **Batch generation** - Generate multiple plots
- **Export options** - Multiple output formats

### Usage Example

```python
from src.plotting.plotting_generation import PlotGenerator

# Initialize generator
generator = PlotGenerator()

# Generate plot with specific backend
plot = generator.generate_plot(
    data=price_data,
    indicators=indicator_data,
    backend='plotly',
    template='financial_analysis',
    export_formats=['html', 'png']
)
```

## Plot Templates

### Available Templates

1. **`financial_analysis`** - Complete financial analysis
2. **`technical_indicators`** - Technical indicator focus
3. **`price_action`** - Price action analysis
4. **`volume_analysis`** - Volume-focused analysis
5. **`correlation_analysis`** - Correlation and statistical analysis

### Template Usage

```python
from src.plotting.plotting_generation import PlotGenerator

# Use predefined template
generator = PlotGenerator()
plot = generator.generate_plot(
    data=price_data,
    template='financial_analysis',
    backend='plotly'
)

# Custom template
custom_template = {
    'layout': {'title': 'Custom Analysis'},
    'indicators': ['rsi', 'macd'],
    'style': 'dark'
}

plot = generator.generate_plot(
    data=price_data,
    template=custom_template,
    backend='matplotlib'
)
```

## Export Options

### Supported Formats

- **PNG** - High-quality static images
- **PDF** - Vector graphics for printing
- **SVG** - Scalable vector graphics
- **HTML** - Interactive web plots
- **JPG** - Compressed images
- **Terminal** - ASCII/Unicode output

### Export Usage

```python
# Single format export
plot.save('analysis.png')

# Multiple format export
plot.export(['png', 'pdf', 'html'])

# Custom export settings
plot.export(
    formats=['png', 'pdf'],
    dpi=300,
    width=1200,
    height=800
)
```

## Performance Optimization

### Optimization Strategies

1. **Backend selection** - Choose appropriate backend for use case
2. **Data sampling** - Sample large datasets for plotting
3. **Caching** - Cache plot components
4. **Batch processing** - Generate multiple plots efficiently

### Performance Tips

```python
# Use fast plotting for large datasets
from src.plotting.fast_plot import create_fast_plot

# Sample data for plotting
sampled_data = price_data.sample(n=1000)

# Enable caching
plot = create_fast_plot(
    data=sampled_data,
    cache_enabled=True,
    optimize_for='speed'
)
```

## Customization

### Style Customization

```python
# Custom style configuration
style_config = {
    'background_color': '#1e1e1e',
    'text_color': '#ffffff',
    'grid_color': '#333333',
    'indicator_colors': ['#ff6b6b', '#4ecdc4', '#45b7d1']
}

plot = create_plot(
    data=price_data,
    style=style_config,
    backend='plotly'
)
```

### Layout Customization

```python
# Custom layout
layout_config = {
    'title': 'Custom Analysis',
    'xaxis_title': 'Time',
    'yaxis_title': 'Price',
    'width': 1200,
    'height': 800,
    'showlegend': True
}

plot = create_plot(
    data=price_data,
    layout=layout_config,
    backend='matplotlib'
)
```

## Integration Examples

### CLI Integration

```bash
# Generate plot from CLI
python run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule RSI --plot

# Specify plot backend
python run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule RSI --plot-backend plotly

# Export plot
python run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule RSI --plot --export-plot png,pdf
```

### Programmatic Integration

```python
from src.data.data_acquisition import DataAcquisition
from src.plotting.plotting_generation import PlotGenerator

# Fetch data
manager = DataAcquisition()
data = manager.fetch_data(symbol='AAPL', period='1y')

# Generate plot
generator = PlotGenerator()
plot = generator.generate_plot(
    data=data,
    template='financial_analysis',
    backend='plotly'
)

# Display and save
plot.show()
plot.save('aapl_analysis.html')
```

## Error Handling

### Common Issues

```python
# Handle missing data
try:
    plot = create_plot(data=price_data)
except ValueError as e:
    print(f"Data error: {e}")
    # Handle missing or invalid data

# Handle backend errors
try:
    plot = create_plot(data=price_data, backend='plotly')
except ImportError as e:
    print(f"Backend not available: {e}")
    # Fallback to available backend
```

## Testing

### Plot Testing

```bash
# Run plotting tests
pytest tests/plotting/ -v

# Test specific backends
pytest tests/plotting/test_plotly_plot.py -v
pytest tests/plotting/test_matplotlib_plot.py -v

# Test performance
pytest tests/plotting/test_performance.py -v
```

## Related Documentation

- **[CLI Interface](cli-interface.md)** - Command-line plotting
- **[Data Sources](../api/data-sources.md)** - Data acquisition
- **[Technical Indicators](../reference/indicators/)** - Indicator documentation
- **[Export Functions](export-functions.md)** - Data export capabilities 