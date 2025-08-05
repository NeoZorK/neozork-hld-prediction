# Plotting Modes Comparison: Matplotlib vs Seaborn

Complete guide to understanding the differences between `-d mpl` (Matplotlib) and `-d sb` (Seaborn) plotting modes in the Neozork HLD Prediction project.

## Overview

The project supports multiple plotting backends for dual-chart visualization, each optimized for different use cases and visual preferences. This guide explains the key differences between the two primary static plotting modes: Matplotlib (`-d mpl`) and Seaborn (`-d sb`).

## Quick Reference

| Aspect | `-d mpl` (Matplotlib) | `-d sb` (Seaborn) |
|--------|----------------------|-------------------|
| **Library** | Pure Matplotlib | Seaborn + Matplotlib |
| **Style** | Technical/Classic | Scientific/Modern |
| **Performance** | Faster | Slightly slower |
| **Customization** | High control | Automated styling |
| **Grid Style** | Basic/None | White grid |
| **Color Palette** | Standard | "husl" palette |
| **Best For** | Technical analysis | Presentations/Reports |

## Detailed Comparison

### 1. **Visual Style and Aesthetics**

#### Matplotlib Mode (`-d mpl`)
- **Appearance**: Classic technical analysis style
- **Grid**: Minimal or no grid lines
- **Colors**: Standard matplotlib color scheme
- **Background**: Default matplotlib background
- **Typography**: Standard system fonts

#### Seaborn Mode (`-d sb`)
- **Appearance**: Modern scientific publication style
- **Grid**: Clean white grid with subtle lines
- **Colors**: Harmonious "husl" color palette
- **Background**: White background with grid
- **Typography**: Optimized fonts for readability

### 2. **Technical Implementation**

#### Matplotlib Mode (`-d mpl`)
```python
# Uses direct matplotlib plotting
ax2.plot(display_df.index, display_df['rsi'], 
         color='purple', linewidth=3, label='RSI')
```

#### Seaborn Mode (`-d sb`)
```python
# Uses seaborn's statistical plotting
sns.lineplot(data=display_df, x=display_df.index, y='rsi', 
             ax=ax2, color='purple', linewidth=3, label='RSI')
```

### 3. **Style Configuration**

#### Matplotlib Mode (`-d mpl`)
- No automatic style configuration
- Manual control over all visual elements
- Requires explicit styling for each component

#### Seaborn Mode (`-d sb`)
```python
# Automatic style configuration
sns.set_style("whitegrid")
sns.set_palette("husl")
```

### 4. **Performance Characteristics**

#### Matplotlib Mode (`-d mpl`)
- **Speed**: Faster rendering
- **Memory**: Lower memory usage
- **Complexity**: Direct plotting calls
- **Overhead**: Minimal additional processing

#### Seaborn Mode (`-d sb`)
- **Speed**: Slightly slower due to statistical processing
- **Memory**: Higher memory usage for style calculations
- **Complexity**: Statistical plotting with automatic enhancements
- **Overhead**: Additional statistical computations

### 5. **Supported Indicators**

Both modes support the same comprehensive set of technical indicators:

#### Trend Indicators
- EMA (Exponential Moving Average)
- HMA (Hull Moving Average)
- TSF (Time Series Forecast)
- ADX (Average Directional Index)

#### Oscillators
- RSI (Relative Strength Index)
- Stochastic (%K, %D)
- Stochastic Oscillator
- CCI (Commodity Channel Index)
- MACD (Moving Average Convergence Divergence)

#### Volatility Indicators
- ATR (Average True Range)
- Bollinger Bands
- Standard Deviation

#### Volume Indicators
- VWAP (Volume Weighted Average Price)
- OBV (On-Balance Volume)

#### Support/Resistance
- Pivot Points
- Fibonacci Levels
- Donchian Channels

#### Advanced Indicators
- Monte Carlo Simulation
- Kelly Criterion
- Put/Call Ratio
- Fear & Greed Index

### 6. **Use Cases and Recommendations**

#### When to Use Matplotlib Mode (`-d mpl`)

**✅ Best for:**
- High-frequency trading analysis
- Large dataset processing
- Technical analysis workflows
- Custom styling requirements
- Performance-critical applications
- Server environments with limited resources

**🎯 Example Use Cases:**
```bash
# Technical analysis with custom styling
uv run run_analysis.py show csv gbp -d mpl --rule rsi:14,30,70,close

# High-frequency data processing
uv run run_analysis.py show csv eur -d mpl --rule macd:12,26,9,close

# Custom indicator analysis
uv run run_analysis.py show csv usd -d mpl --rule bollinger:20,2,close
```

#### When to Use Seaborn Mode (`-d sb`)

**✅ Best for:**
- Research presentations
- Academic publications
- Statistical analysis reports
- Modern UI applications
- Data science workflows
- Professional reports

**🎯 Example Use Cases:**
```bash
# Research presentation
uv run run_analysis.py show csv gbp -d sb --rule stoch:14,3,close

# Statistical analysis report
uv run run_analysis.py show csv eur -d sb --rule rsi:14,30,70,close

# Academic publication
uv run run_analysis.py show csv usd -d sb --rule macd:12,26,9,close
```

### 7. **Output Quality and Formats**

#### Matplotlib Mode (`-d mpl`)
- **Output**: PNG files
- **Quality**: High-resolution static images
- **Size**: Optimized file sizes
- **Compatibility**: Universal image format support

#### Seaborn Mode (`-d sb`)
- **Output**: PNG files with enhanced styling
- **Quality**: Publication-ready images
- **Size**: Slightly larger due to enhanced styling
- **Compatibility**: Professional presentation ready

### 8. **Command Line Usage**

Both modes use identical command syntax:

```bash
# Matplotlib mode
uv run run_analysis.py show csv <symbol> -d mpl --rule <indicator>:<params>

# Seaborn mode
uv run run_analysis.py show csv <symbol> -d sb --rule <indicator>:<params>
```

**Example Commands:**
```bash
# RSI analysis in Matplotlib mode
uv run run_analysis.py show csv gbp -d mpl --rule rsi:14,30,70,close

# RSI analysis in Seaborn mode
uv run run_analysis.py show csv gbp -d sb --rule rsi:14,30,70,close

# Stochastic analysis in Matplotlib mode
uv run run_analysis.py show csv eur -d mpl --rule stoch:14,3,close

# Stochastic analysis in Seaborn mode
uv run run_analysis.py show csv eur -d sb --rule stoch:14,3,close
```

### 9. **File Output Locations**

Both modes save output to the same directory structure:

```
results/plots/
├── dual_chart_mpl.png      # Matplotlib mode output
└── dual_chart_seaborn.png  # Seaborn mode output
```

### 10. **Performance Benchmarks**

Based on internal testing with 383 data points:

| Mode | Rendering Time | Memory Usage | File Size |
|------|----------------|--------------|-----------|
| `-d mpl` | ~4.5 seconds | Lower | ~750KB |
| `-d sb` | ~5.0 seconds | Higher | ~790KB |

*Note: Actual performance may vary based on system specifications and data size.*

## Troubleshooting

### Common Issues

#### Matplotlib Mode Issues
- **Problem**: Inconsistent styling across different systems
- **Solution**: Use explicit style configurations

#### Seaborn Mode Issues
- **Problem**: Slower rendering with large datasets
- **Solution**: Consider switching to matplotlib mode for performance-critical applications

### Best Practices

1. **Choose Based on Use Case**: Use matplotlib for technical analysis, seaborn for presentations
2. **Test Both Modes**: Compare output quality for your specific needs
3. **Consider Performance**: Use matplotlib for large datasets or high-frequency analysis
4. **Maintain Consistency**: Stick to one mode within a project for consistency

## Summary

Both plotting modes provide excellent visualization capabilities with different strengths:

- **`-d mpl`**: Optimized for performance and technical analysis
- **`-d sb`**: Optimized for presentation quality and statistical analysis

The choice between them depends on your specific requirements for performance, aesthetics, and use case. Both modes support the same comprehensive set of technical indicators and provide high-quality output suitable for professional analysis.

## Related Documentation

- **[Plotting and Visualization](plotting-visualization.md)** - Complete plotting guide
- **[CLI Interface](cli-interface.md)** - Command-line interface documentation
- **[Parameterized Indicators](parameterized-indicators.md)** - Indicator usage guide
- **[Technical Indicators](../reference/indicators/)** - Technical indicator reference
