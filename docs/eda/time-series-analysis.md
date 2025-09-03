# Time Series Analysis Module

## Overview

The Time Series Analysis module provides comprehensive analysis capabilities for time series data, specifically designed for financial and trading data analysis. This module is part of the NeoZork HLD Prediction system and offers modern, full-featured time series analysis tools.

## Features

### 🔍 Stationarity Testing
- **ADF (Augmented Dickey-Fuller) Test**: Tests for unit roots in time series
- **KPSS Test**: Kwiatkowski-Phillips-Schmidt-Shin test for stationarity
- **Visual Analysis**: Rolling statistics, distribution plots, Q-Q plots
- **Automatic Interpretation**: Clear stationarity conclusions

### 📈 Trend Analysis
- **Linear Trend Detection**: Linear regression analysis with R² values
- **Moving Averages**: Short and long-term moving average analysis
- **Trend Strength Measurement**: Quantified trend strength over time
- **Visual Trend Lines**: Multiple trend indicators on plots

### 🔄 Seasonality Detection
- **FFT-based Period Detection**: Automatic seasonal period identification
- **Seasonal Decomposition**: Trend, seasonal, and residual components
- **Seasonal Strength Measurement**: Quantified seasonality strength
- **Multi-period Analysis**: Support for various seasonal patterns

### 📊 Volatility Analysis
- **Rolling Volatility**: Time-varying volatility measurement
- **Volatility Clustering**: Detection of volatility persistence
- **Volatility Distribution**: Statistical analysis of volatility patterns
- **Annualized Metrics**: Standardized volatility measures

### 🔗 Autocorrelation Analysis
- **ACF (Autocorrelation Function)**: Lag-based correlation analysis
- **PACF (Partial Autocorrelation Function)**: Partial correlation analysis
- **Significant Lag Detection**: Automatic identification of important lags
- **Confidence Intervals**: Statistical significance testing

### 🔮 Forecasting Capabilities
- **Naive Forecasting**: Simple last-value prediction
- **Seasonal Naive**: Seasonal pattern-based forecasting
- **ARIMA Models**: Autoregressive Integrated Moving Average models
- **Multi-method Comparison**: Side-by-side forecast evaluation

## Usage

### Basic Usage

```python
from src.batch_eda.time_series_analysis import TimeSeriesAnalyzer, analyze_time_series
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Quick analysis
results = analyze_time_series(data, 'close_price')

# Or use the analyzer class for more control
analyzer = TimeSeriesAnalyzer(data)
results = analyzer.comprehensive_analysis('close_price')
```

### Interactive System Integration

The time series analysis is fully integrated into the interactive system:

1. Load your data using the interactive system
2. Navigate to "EDA Analysis" → "Time Series Analysis"
3. Select the column to analyze
4. View comprehensive results and recommendations

### Advanced Usage

```python
# Initialize analyzer
analyzer = TimeSeriesAnalyzer(data)

# Individual analyses
stationarity_results = analyzer.analyze_stationarity('price')
trend_results = analyzer.analyze_trends('price', window=20)
seasonality_results = analyzer.analyze_seasonality('price', period=12)
volatility_results = analyzer.analyze_volatility('price', window=30)
autocorr_results = analyzer.analyze_autocorrelation('price', max_lag=50)
forecast_results = analyzer.forecast_series('price', periods=30)

# Comprehensive analysis
comprehensive_results = analyzer.comprehensive_analysis('price')

# Export results
analyzer.export_results('my_analysis.json')
```

## Output and Results

### Analysis Results Structure

```python
{
    'timestamp': '2024-01-15T10:30:00',
    'column': 'close_price',
    'analyses': {
        'stationarity': {
            'tests': {
                'adf': {'statistic': -2.5, 'p_value': 0.01, 'is_stationary': True},
                'kpss': {'statistic': 0.3, 'p_value': 0.1, 'is_stationary': True}
            },
            'plot_path': 'results/plots/time_series/stationarity_analysis_close_price_20240115_103000.png'
        },
        'trends': {
            'trend_analysis': {
                'linear': {
                    'slope': 0.05,
                    'r_squared': 0.75,
                    'trend_direction': 'increasing'
                }
            }
        },
        'seasonality': {
            'detected_period': 12,
            'seasonality_analysis': {
                'decomposition': {
                    'seasonal_strength': 0.3,
                    'has_seasonality': True
                }
            }
        },
        'volatility': {
            'volatility_analysis': {
                'mean_volatility': 0.15,
                'has_clustering': True
            }
        },
        'autocorrelation': {
            'autocorrelation_analysis': {
                'max_acf_lag': 5,
                'max_pacf_lag': 2
            }
        },
        'forecast': {
            'forecast_results': {
                'forecasts': {
                    'naive': [100.5, 100.5, ...],
                    'arima': [101.2, 101.8, ...]
                }
            }
        }
    },
    'summary': {
        'key_findings': [
            'Series appears to be stationary (ADF test)',
            'Series shows increasing trend (R² = 0.750)',
            'Strong seasonality detected (strength: 0.300)'
        ],
        'recommendations': [
            'Consider trend-following models',
            'Use seasonal models (SARIMA, seasonal decomposition)',
            'Consider GARCH models for volatility modeling'
        ]
    }
}
```

### Generated Plots

The module automatically generates and saves high-quality plots:

- **Stationarity Analysis**: Original series, rolling statistics, distribution, Q-Q plot
- **Trend Analysis**: Time series with trend lines, trend strength over time
- **Seasonality Analysis**: Original, trend, seasonal, and residual components
- **Volatility Analysis**: Returns, rolling volatility, volatility distribution
- **Autocorrelation Analysis**: ACF and PACF plots with confidence intervals
- **Forecast Analysis**: Original series with multiple forecast methods

## Configuration Options

### Analysis Parameters

```python
# Customize analysis parameters
analyzer = TimeSeriesAnalyzer(data)

# Stationarity analysis
stationarity_results = analyzer.analyze_stationarity('price')

# Trend analysis with custom window
trend_results = analyzer.analyze_trends('price', window=30)

# Seasonality analysis with custom period
seasonality_results = analyzer.analyze_seasonality('price', period=24)

# Volatility analysis with custom window
volatility_results = analyzer.analyze_volatility('price', window=20)

# Autocorrelation analysis with custom max lag
autocorr_results = analyzer.analyze_autocorrelation('price', max_lag=100)

# Forecasting with custom parameters
forecast_results = analyzer.forecast_series('price', periods=60, model_type='arima')
```

## Data Requirements

### Minimum Data Requirements

- **Stationarity Analysis**: At least 50 observations
- **Seasonality Analysis**: At least 100 observations
- **Forecasting**: At least 50 observations
- **Other Analyses**: No strict minimum (but more data = better results)

### Data Format

The module supports various data formats:

```python
# DataFrame with datetime index
data = pd.DataFrame({
    'close': [100, 101, 102, ...],
    'volume': [1000, 1100, 1200, ...]
}, index=pd.date_range('2020-01-01', periods=100, freq='D'))

# DataFrame with date column
data = pd.DataFrame({
    'date': ['2020-01-01', '2020-01-02', ...],
    'close': [100, 101, 102, ...]
})

# The module will automatically handle datetime conversion
```

## Error Handling

The module includes comprehensive error handling:

- **Insufficient Data**: Clear error messages with minimum requirements
- **Invalid Columns**: Automatic fallback to available numeric columns
- **Analysis Failures**: Graceful degradation with error reporting
- **Missing Dependencies**: Clear import error messages

## Performance Considerations

### Optimization Tips

1. **Data Size**: For large datasets (>10,000 observations), consider sampling
2. **Memory Usage**: Results are automatically saved to disk to manage memory
3. **Parallel Processing**: Individual analyses can be run in parallel
4. **Caching**: Results are cached to avoid recomputation

### Memory Management

```python
# For large datasets, process in chunks
chunk_size = 1000
for i in range(0, len(data), chunk_size):
    chunk = data.iloc[i:i+chunk_size]
    analyzer = TimeSeriesAnalyzer(chunk)
    results = analyzer.comprehensive_analysis('price')
    # Process results...
```

## Integration with Other Modules

### Feature Engineering Integration

```python
# Use time series analysis results for feature engineering
from src.ml.feature_engineering.temporal_features import TemporalFeatureGenerator

# Get seasonal period from analysis
seasonality_results = analyzer.analyze_seasonality('price')
seasonal_period = seasonality_results['detected_period']

# Use in feature generation
temporal_generator = TemporalFeatureGenerator()
features = temporal_generator.generate_features(data, seasonal_period=seasonal_period)
```

### ML Pipeline Integration

```python
# Use analysis results for model selection
if stationarity_results['tests']['adf']['is_stationary']:
    # Use stationary models
    model = ARIMA(data['price'], order=(1, 0, 1))
else:
    # Use non-stationary models with differencing
    model = ARIMA(data['price'], order=(1, 1, 1))
```

## Examples

### Financial Data Analysis

```python
# Analyze stock price data
import yfinance as yf

# Download data
ticker = yf.Ticker('AAPL')
data = ticker.history(period='1y')

# Analyze
analyzer = TimeSeriesAnalyzer(data)
results = analyzer.comprehensive_analysis('Close')

# Check for trading opportunities
if results['summary']['key_findings']:
    for finding in results['summary']['key_findings']:
        print(f"Finding: {finding}")
```

### Cryptocurrency Analysis

```python
# Analyze cryptocurrency data
import ccxt

# Get data
exchange = ccxt.binance()
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1d', limit=365)
data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
data.set_index('timestamp', inplace=True)

# Analyze
analyzer = TimeSeriesAnalyzer(data)
results = analyzer.comprehensive_analysis('close')
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install statsmodels scipy scikit-learn matplotlib seaborn
   ```

2. **Memory Errors**: For large datasets, use chunking or sampling

3. **Plot Generation Errors**: Ensure write permissions to results directory

4. **Analysis Failures**: Check data quality and minimum requirements

### Debug Mode

```python
# Enable debug mode for detailed error information
import logging
logging.basicConfig(level=logging.DEBUG)

analyzer = TimeSeriesAnalyzer(data)
results = analyzer.comprehensive_analysis('price')
```

## Contributing

To contribute to the time series analysis module:

1. Follow the existing code style and patterns
2. Add comprehensive tests for new features
3. Update documentation for any changes
4. Ensure backward compatibility

## License

This module is part of the NeoZork HLD Prediction system and follows the same licensing terms.
