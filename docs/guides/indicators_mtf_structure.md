# Indicators MTF Structure Guide

This guide explains how to use the new Indicators MTF (Multi-Timeframe) structure functionality in the NeoZork Interactive ML Trading Strategy Development system.

## Overview

The Indicators MTF structure functionality allows you to save all indicators data in a well-organized Multi-Timeframe structure, similar to the Raw Parquet functionality. This creates a standardized format for machine learning applications, feature engineering, and cross-timeframe analysis.

## Features

- **Automatic Symbol Detection**: Automatically detects trading symbols from filenames and data
- **Multi-Timeframe Support**: Organizes data by timeframes (M1, M5, M15, H1, H4, D1, W1, MN1)
- **Cross-Timeframe Features**: Creates cross-timeframe features for ML applications
- **Structured Organization**: Saves data in a consistent MTF structure
- **Progress Tracking**: Real-time progress updates during processing
- **Data Quality Metrics**: Calculates completeness, consistency, and validity scores

## Usage

### Through Interactive Menu

1. Start the interactive system:
   ```bash
   uv run ./interactive
   ```

2. Navigate to the data loading menu:
   - Select "Load Data" from the main menu
   - Select "Indicators" from the data loading submenu

3. Choose the MTF structure option:
   - The system will analyze your indicators data
   - Select option "2. Save all indicators to MTF structure"
   - The system will process all indicators and create MTF structures

### Programmatic Usage

```python
from src.interactive.data_management.indicators import IndicatorsMTFCreator

# Initialize the MTF creator
mtf_creator = IndicatorsMTFCreator()

# Load your indicators data (example)
indicators_data = {
    'btcusdt_rsi_m1.parquet': {
        'indicator': 'RSI',
        'timeframe': 'M1',
        'symbol': 'BTCUSDT',
        'data': rsi_dataframe,
        'rows': 1000
    },
    'btcusdt_macd_m1.parquet': {
        'indicator': 'MACD',
        'timeframe': 'M1',
        'symbol': 'BTCUSDT',
        'data': macd_dataframe,
        'rows': 1000
    }
}

# Create MTF structures for all symbols
result = mtf_creator.create_mtf_from_all_indicators(indicators_data)

if result['status'] == 'success':
    print(f"Created MTF structures for {result['summary']['total_symbols']} symbols")
    print(f"Success rate: {result['summary']['success_rate']:.1f}%")
```

## Output Structure

The MTF structure is saved in `data/cleaned_data/mtf_structures/indicators/` with the following organization:

```
data/cleaned_data/mtf_structures/indicators/
├── btcusdt/
│   ├── btcusdt_main_m1.parquet          # Main timeframe data
│   ├── mtf_metadata.json                # Metadata and statistics
│   └── cross_timeframes/                # Cross-timeframe features
│       ├── btcusdt_h1_cross.parquet
│       ├── btcusdt_d1_cross.parquet
│       └── ...
├── ethusdt/
│   ├── ethusdt_main_m1.parquet
│   ├── mtf_metadata.json
│   └── cross_timeframes/
│       └── ...
└── ...
```

## File Formats

### Main Data File (`*_main_*.parquet`)

Contains the main timeframe data with indicators as columns:

| timestamp | RSI | MACD | symbol | timeframe |
|-----------|-----|------|--------|-----------|
| 2023-01-01 00:00:00 | 50.5 | 0.12 | BTCUSDT | M1 |
| 2023-01-01 00:01:00 | 52.1 | 0.15 | BTCUSDT | M1 |
| ... | ... | ... | ... | ... |

### Cross-Timeframe Files (`*_cross.parquet`)

Contains cross-timeframe features for ML applications:

| timestamp | RSI_H1_lag_1 | RSI_H1_ma_5 | MACD_H1_volatility | ... |
|-----------|--------------|-------------|-------------------|-----|
| 2023-01-01 00:00:00 | 48.2 | 49.1 | 2.3 | ... |
| 2023-01-01 00:01:00 | 49.1 | 49.5 | 2.1 | ... |
| ... | ... | ... | ... | ... |

### Metadata File (`mtf_metadata.json`)

Contains comprehensive metadata about the MTF structure:

```json
{
  "created_at": "2023-01-01T00:00:00",
  "symbol": "BTCUSDT",
  "source": "indicators",
  "main_timeframe": "M1",
  "timeframes": ["M1", "H1", "D1"],
  "indicators": ["RSI", "MACD", "SMA"],
  "total_rows": 1000,
  "data_quality": {
    "completeness": 95.5,
    "consistency": 98.2,
    "validity": 92.1,
    "overall_score": 95.3
  },
  "main_data_shape": [1000, 5],
  "cross_timeframes_count": 2
}
```

## Supported Indicators

The system supports various technical indicators:

- **RSI** (Relative Strength Index)
- **MACD** (Moving Average Convergence Divergence)
- **SMA** (Simple Moving Average)
- **EMA** (Exponential Moving Average)
- **Bollinger Bands**
- **Stochastic Oscillator**
- **Williams %R**
- **Custom indicators** (any indicator with value column)

## Supported Timeframes

- **M1** (1 minute)
- **M5** (5 minutes)
- **M15** (15 minutes)
- **M30** (30 minutes)
- **H1** (1 hour)
- **H4** (4 hours)
- **D1** (1 day)
- **W1** (1 week)
- **MN1** (1 month)

## Data Quality Metrics

The system calculates several data quality metrics:

- **Completeness**: Percentage of non-null values
- **Consistency**: Data type consistency across columns
- **Validity**: Reasonable value ranges and patterns
- **Overall Score**: Weighted average of all metrics

## Cross-Timeframe Features

The system automatically creates cross-timeframe features for ML applications:

- **Lagged Values**: Previous values from higher timeframes
- **Moving Averages**: Various window sizes
- **Volatility Measures**: Rolling standard deviation
- **Momentum Indicators**: Percentage change calculations

## Error Handling

The system includes comprehensive error handling:

- **File Loading Errors**: Graceful handling of corrupted or missing files
- **Data Processing Errors**: Validation and cleaning of indicator data
- **MTF Creation Errors**: Fallback mechanisms for failed structures
- **Progress Tracking**: Real-time error reporting during processing

## Performance Considerations

- **Memory Efficient**: Processes data in chunks to minimize memory usage
- **Progress Tracking**: Real-time progress updates with ETA calculations
- **Parallel Processing**: Supports concurrent processing where possible
- **Caching**: Intelligent caching of processed data

## Integration with ML Pipeline

The MTF structure is designed for seamless integration with machine learning workflows:

1. **Feature Engineering**: Use cross-timeframe features for model training
2. **Data Validation**: Leverage data quality metrics for preprocessing
3. **Time Series Analysis**: Structured data format for time series models
4. **Backtesting**: Consistent data format for strategy backtesting

## Troubleshooting

### Common Issues

1. **No Data Loaded**: Check that indicator files exist in the correct format
2. **Symbol Detection Failed**: Ensure filenames contain recognizable symbol patterns
3. **MTF Creation Failed**: Verify data quality and format consistency
4. **Memory Issues**: Reduce batch size or process fewer files at once

### Debug Mode

Enable debug logging for detailed error information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Examples

### Basic Usage Example

```python
# Load indicators data
from src.interactive.data_management.indicators import IndicatorsLoader, IndicatorsMTFCreator

loader = IndicatorsLoader()
mtf_creator = IndicatorsMTFCreator()

# Load all indicators
result = loader.load_indicators_data()
if result['status'] == 'success':
    # Create MTF structures
    mtf_result = mtf_creator.create_mtf_from_all_indicators(result['data'])
    print(f"Created {mtf_result['summary']['successful']} MTF structures")
```

### Custom Symbol Processing

```python
# Process specific symbols
symbols_data = {
    'BTCUSDT': {
        'M1': {
            'btcusdt_rsi_m1.parquet': rsi_data,
            'btcusdt_macd_m1.parquet': macd_data
        }
    }
}

for symbol, timeframes in symbols_data.items():
    result = mtf_creator.create_and_save_mtf_structure(
        timeframes, symbol, 'M1', 'indicators'
    )
    print(f"Processed {symbol}: {result['status']}")
```

## Best Practices

1. **Data Organization**: Keep indicator files well-organized by symbol and timeframe
2. **Naming Conventions**: Use consistent naming patterns for automatic symbol detection
3. **Data Quality**: Regularly validate data quality metrics
4. **Backup**: Keep backups of original indicator data
5. **Monitoring**: Monitor MTF creation success rates and error patterns

## Support

For additional support or questions about the Indicators MTF structure functionality:

- Check the test files in `tests/test_indicators_mtf_creator.py`
- Review the source code in `src/interactive/data_management/indicators/`
- Consult the main documentation in `docs/`

## Changelog

### Version 1.0.0
- Initial implementation of Indicators MTF structure functionality
- Support for automatic symbol detection
- Cross-timeframe feature engineering
- Data quality metrics calculation
- Integration with interactive menu system
