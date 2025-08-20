# SMA (Simple Moving Average) Indicator

## Overview

The **SMA (Simple Moving Average)** indicator is a fundamental trend-following technical indicator that calculates the average price over a specified period, giving equal weight to all prices in the calculation period.

## Category
**Trend Indicators**

## Description

SMA is one of the most widely used technical indicators in financial analysis. It smooths out price data by creating a constantly updated average price, which helps identify trend direction and potential support/resistance levels.

### Key Features
- **Equal Weighting**: All prices in the period have equal importance
- **Trend Identification**: Clear trend direction visualization
- **Support/Resistance**: Dynamic support and resistance levels
- **Multiple Timeframes**: Works across all timeframes
- **Universal Compatibility**: Works with all display modes

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `period` | int | 20 | Calculation period for the moving average |
| `price_type` | string | close | Price type to use (open/close) |

## Usage

### CLI Command Format
```bash
uv run run_analysis.py demo --rule sma:period,price_type -d display_mode
```

### Examples

#### Basic SMA with 20-period close prices
```bash
uv run run_analysis.py demo --rule sma:20,close -d fastest
```

#### SMA with open prices
```bash
uv run run_analysis.py demo --rule sma:20,open -d plotly
```

#### Multiple SMAs for trend comparison
```bash
uv run run_analysis.py demo --rule sma:10,close,sma:20,close,sma:50,close -d plotly
```

#### SMA with real data
```bash
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest
```

## Display Modes

SMA indicator works across all 6 display modes:

- **`fastest`** - Plotly+Dask+Datashader (best for large datasets)
- **`fast`** - Dask+Datashader+Bokeh for quick visualization
- **`plotly`** - Interactive HTML plots with Plotly
- **`mpl`** - Static images with mplfinance
- **`seaborn`** - Statistical plots with Seaborn
- **`term`** - Terminal ASCII charts with plotext

## Calculation Method

The SMA is calculated using the following formula:

```
SMA = (P₁ + P₂ + ... + Pₙ) / n
```

Where:
- `P₁, P₂, ..., Pₙ` are the prices for each period
- `n` is the number of periods

### Implementation Details

```python
def sma_calculation(period: int, source_arr: pd.Series) -> pd.Series:
    """
    Calculates Simple Moving Average (SMA) for the given period and source array.
    
    Args:
        period (int): Calculation period for SMA
        source_arr (pd.Series): Source data array
        
    Returns:
        pd.Series: Series with SMA values for each index
    """
    result = pd.Series(0.0, index=source_arr.index)
    
    for i in range(len(source_arr)):
        if i < period - 1:
            # For initial values, use the current value
            result.iloc[i] = source_arr.iloc[i]
        else:
            # Calculate SMA for the period ending at current index
            start_idx = i - period + 1
            end_idx = i + 1
            sma_value = source_arr.iloc[start_idx:end_idx].mean()
            result.iloc[i] = sma_value
    
    return result
```

## Trading Signals

### Trend Identification
- **Uptrend**: Price above SMA indicates bullish trend
- **Downtrend**: Price below SMA indicates bearish trend
- **Sideways**: Price oscillating around SMA indicates consolidation

### Support and Resistance
- **Support**: SMA acts as dynamic support in uptrends
- **Resistance**: SMA acts as dynamic resistance in downtrends

### Signal Generation
- **Buy Signal**: Price crosses above SMA
- **Sell Signal**: Price crosses below SMA

## Comparison with Other Moving Averages

| Characteristic | SMA | EMA | HMA |
|----------------|-----|-----|-----|
| **Weighting** | Equal | Exponential | Hull |
| **Lag** | High | Medium | Low |
| **Sensitivity** | Low | Medium | High |
| **Smoothness** | High | Medium | Low |
| **Use Case** | Trend identification | Trend following | Fast signals |

## Advantages

✅ **Simple and Reliable**: Easy to understand and implement  
✅ **Universal Application**: Works across all markets and timeframes  
✅ **Trend Clarity**: Clear trend direction identification  
✅ **Support/Resistance**: Dynamic support and resistance levels  
✅ **Multiple Timeframes**: Effective across different periods  
✅ **Low Noise**: Smooths out price fluctuations  

## Disadvantages

❌ **Lag**: Delayed signal generation due to equal weighting  
❌ **False Signals**: May generate signals in sideways markets  
❌ **Parameter Sensitivity**: Performance depends on period selection  
❌ **No Volume Consideration**: Doesn't account for trading volume  

## Best Practices

### Period Selection
- **Short-term**: 5-20 periods for quick signals
- **Medium-term**: 20-50 periods for trend identification
- **Long-term**: 50-200 periods for major trend analysis

### Multiple Timeframe Analysis
- Use multiple SMAs for confirmation
- Combine short and long-term SMAs
- Look for convergence/divergence patterns

### Risk Management
- Use SMA as part of a broader strategy
- Combine with volume and momentum indicators
- Set appropriate stop-loss levels

## Related Indicators

- **EMA (Exponential Moving Average)** - Weighted moving average
- **HMA (Hull Moving Average)** - Fast moving average
- **Bollinger Bands** - Uses SMA as center line
- **MACD** - Based on moving average convergence/divergence

## Tutorials and Examples

- **[Complete SMA Tutorial](docs/guides/adding-sma-indicator-tutorial.md)** - Full implementation guide
- **[Quick Start Guide](docs/guides/sma-quick-start-guide.md)** - Get started in minutes
- **[Practical Examples](docs/guides/sma-practical-examples.md)** - Real-world scenarios
- **[Testing Guide](docs/guides/sma-testing-guide.md)** - Comprehensive testing

## Testing

The SMA indicator has comprehensive test coverage:

```bash
# Run SMA-specific tests
uv run pytest tests/calculation/indicators/trend/test_sma_ind.py -v

# Run all trend indicator tests
uv run pytest tests/calculation/indicators/trend/ -v

# Run with coverage
uv run pytest tests/calculation/indicators/trend/test_sma_ind.py --cov=src.calculation.indicators.trend.sma_ind -v
```

## Implementation Status

- ✅ **Core Calculation**: Fully implemented
- ✅ **CLI Integration**: Complete with help system
- ✅ **Display Modes**: All 6 modes supported
- ✅ **Parameter Validation**: Comprehensive validation
- ✅ **Error Handling**: Robust error handling
- ✅ **Documentation**: Complete documentation
- ✅ **Testing**: 100% test coverage
- ✅ **Examples**: Multiple usage examples

## Version History

- **v1.0.0**: Initial implementation with basic functionality
- **v1.1.0**: Added support for all display modes
- **v1.2.0**: Enhanced parameter validation and error handling
- **v1.3.0**: Complete documentation and tutorial suite
- **v2.0.0**: Full integration with UV package management
