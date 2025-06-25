# Export Functions Guide

Complete guide to data export capabilities in the Neozork HLD Prediction project.

## Overview

The export module provides comprehensive data export functionality in multiple formats for analysis results, indicators, and processed data.

## Available Export Formats

### 1. CSV Export (`csv_export.py`)

Export data to Comma-Separated Values format.

#### Features
- **Universal compatibility** - Works with all spreadsheet applications
- **Human readable** - Easy to inspect and edit
- **Lightweight** - Small file sizes
- **Text-based** - Version control friendly

#### Usage Example

```python
from src.export.csv_export import CSVExporter

# Initialize exporter
exporter = CSVExporter()

# Export price data with indicators
exporter.export_data(
    data=price_data,
    indicators={'rsi': rsi_data, 'macd': macd_data},
    output_path='data/export/aapl_analysis.csv',
    include_timestamp=True,
    include_metadata=True
)

# Export indicators only
exporter.export_indicators(
    indicators={'rsi': rsi_data, 'macd': macd_data},
    output_path='data/export/indicators.csv'
)
```

#### Export Options
- **`include_timestamp`** - Include timestamp column
- **`include_metadata`** - Include calculation metadata
- **`separate_files`** - Export each indicator to separate file
- **`compression`** - Enable gzip compression

### 2. JSON Export (`json_export.py`)

Export data to JavaScript Object Notation format.

#### Features
- **Structured data** - Hierarchical data representation
- **Web integration** - Native JavaScript support
- **Metadata support** - Rich metadata inclusion
- **Human readable** - Easy to parse and debug

#### Usage Example

```python
from src.export.json_export import JSONExporter

# Initialize exporter
exporter = JSONExporter()

# Export with metadata
exporter.export_data(
    data=price_data,
    indicators={'rsi': rsi_data, 'macd': macd_data},
    output_path='data/export/aapl_analysis.json',
    include_metadata=True,
    pretty_print=True
)

# Export indicators with parameters
exporter.export_indicators(
    indicators={'rsi': rsi_data, 'macd': macd_data},
    parameters={'rsi_period': 14, 'macd_fast': 12, 'macd_slow': 26},
    output_path='data/export/indicators.json'
)
```

#### Export Options
- **`include_metadata`** - Include calculation metadata
- **`pretty_print`** - Human-readable formatting
- **`include_parameters`** - Include indicator parameters
- **`compression`** - Enable gzip compression

### 3. Parquet Export (`parquet_export.py`)

Export data to Apache Parquet format.

#### Features
- **High performance** - Columnar storage format
- **Compression** - Efficient data compression
- **Schema evolution** - Support for schema changes
- **Big data ready** - Compatible with big data tools

#### Usage Example

```python
from src.export.parquet_export import ParquetExporter

# Initialize exporter
exporter = ParquetExporter()

# Export with compression
exporter.export_data(
    data=price_data,
    indicators={'rsi': rsi_data, 'macd': macd_data},
    output_path='data/export/aapl_analysis.parquet',
    compression='snappy',
    include_metadata=True
)

# Export with partitioning
exporter.export_data(
    data=price_data,
    indicators={'rsi': rsi_data, 'macd': macd_data},
    output_path='data/export/partitioned/',
    partition_by=['year', 'month'],
    compression='gzip'
)
```

#### Export Options
- **`compression`** - Compression algorithm (snappy, gzip, brotli)
- **`include_metadata`** - Include calculation metadata
- **`partition_by`** - Partition data by columns
- **`row_group_size`** - Row group size for optimization

## Unified Export Interface

### Export Manager (`export_manager.py`)

Centralized export management with multiple format support.

#### Features
- **Multi-format export** - Export to multiple formats simultaneously
- **Batch processing** - Export multiple datasets
- **Format validation** - Validate export formats
- **Error handling** - Robust error management

#### Usage Example

```python
from src.export.export_manager import ExportManager

# Initialize manager
manager = ExportManager()

# Export to multiple formats
manager.export_data(
    data=price_data,
    indicators={'rsi': rsi_data, 'macd': macd_data},
    formats=['csv', 'json', 'parquet'],
    output_dir='data/export/',
    filename='aapl_analysis'
)

# Batch export multiple symbols
symbols = ['AAPL', 'GOOGL', 'MSFT']
for symbol in symbols:
    data = fetch_data(symbol)
    manager.export_data(
        data=data,
        indicators=calculate_indicators(data),
        formats=['parquet'],
        output_dir=f'data/export/{symbol}/',
        filename=f'{symbol}_analysis'
    )
```

## Export Configuration

### Export Settings

```python
# Export configuration
export_config = {
    'formats': ['csv', 'json', 'parquet'],
    'compression': 'snappy',
    'include_metadata': True,
    'include_timestamp': True,
    'output_directory': 'data/export/',
    'filename_template': '{symbol}_{date}_{indicators}',
    'separate_files': False,
    'pretty_print': True
}

# Use configuration
manager = ExportManager(config=export_config)
manager.export_data(data=price_data, indicators=indicator_data)
```

### Environment Variables

```bash
# Export settings
export EXPORT_FORMATS="csv,json,parquet"
export EXPORT_COMPRESSION="snappy"
export EXPORT_INCLUDE_METADATA="true"
export EXPORT_OUTPUT_DIR="data/export/"

# Performance settings
export EXPORT_BATCH_SIZE="1000"
export EXPORT_MAX_WORKERS="4"
```

## CLI Integration

### Export Commands

```bash
# Export from CLI
python run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule RSI --export-csv

# Export to multiple formats
python run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule RSI --export-csv --export-json --export-parquet

# Export with custom settings
python run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule RSI \
    --export-csv --export-json --export-parquet \
    --export-dir data/custom_export/ \
    --export-compression snappy
```

### Export Options

- **`--export-csv`** - Export to CSV format
- **`--export-json`** - Export to JSON format
- **`--export-parquet`** - Export to Parquet format
- **`--export-dir`** - Custom export directory
- **`--export-compression`** - Compression algorithm
- **`--export-separate`** - Export indicators to separate files

## Data Export Workflows

### 1. Basic Export Workflow

```python
from src.data.data_acquisition import DataAcquisition
from src.calculation.indicator_calculation import IndicatorCalculator
from src.export.export_manager import ExportManager

# Fetch data
manager = DataAcquisition()
data = manager.fetch_data(symbol='AAPL', period='1y')

# Calculate indicators
calculator = IndicatorCalculator()
indicators = calculator.calculate_indicators(
    data=data,
    indicators=['rsi', 'macd', 'bollinger_bands']
)

# Export results
export_manager = ExportManager()
export_manager.export_data(
    data=data,
    indicators=indicators,
    formats=['csv', 'json', 'parquet'],
    output_dir='data/export/',
    filename='aapl_analysis'
)
```

### 2. Batch Export Workflow

```python
# Batch export multiple symbols
symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
indicators_list = ['rsi', 'macd', 'bollinger_bands']

for symbol in symbols:
    # Fetch data
    data = manager.fetch_data(symbol=symbol, period='1y')
    
    # Calculate indicators
    calculated_indicators = calculator.calculate_indicators(
        data=data,
        indicators=indicators_list
    )
    
    # Export
    export_manager.export_data(
        data=data,
        indicators=calculated_indicators,
        formats=['parquet'],
        output_dir=f'data/export/{symbol}/',
        filename=f'{symbol}_analysis'
    )
```

### 3. Real-time Export Workflow

```python
import time
from datetime import datetime

# Real-time data export
while True:
    # Fetch latest data
    data = manager.fetch_data(symbol='AAPL', period='1d', interval='1m')
    
    # Calculate indicators
    indicators = calculator.calculate_indicators(data=data, indicators=['rsi'])
    
    # Export with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_manager.export_data(
        data=data,
        indicators=indicators,
        formats=['parquet'],
        output_dir='data/realtime/',
        filename=f'aapl_realtime_{timestamp}'
    )
    
    # Wait for next update
    time.sleep(60)  # Update every minute
```

## Export File Organization

### Directory Structure

```
data/export/
├── aapl_analysis.csv
├── aapl_analysis.json
├── aapl_analysis.parquet
├── indicators/
│   ├── rsi.csv
│   ├── macd.csv
│   └── bollinger_bands.csv
├── partitioned/
│   ├── year=2024/
│   │   ├── month=01/
│   │   ├── month=02/
│   │   └── ...
│   └── ...
└── metadata/
    ├── calculation_parameters.json
    ├── data_quality_report.json
    └── export_log.txt
```

### File Naming Conventions

```python
# Automatic file naming
filename_template = "{symbol}_{date}_{indicators}_{format}"

# Examples:
# aapl_20241201_rsi_macd.csv
# googl_20241201_bollinger_bands.json
# msft_20241201_all_indicators.parquet
```

## Performance Optimization

### Export Performance Tips

1. **Use appropriate formats** - Parquet for large datasets, CSV for small datasets
2. **Enable compression** - Reduce file sizes and I/O time
3. **Batch processing** - Export multiple datasets together
4. **Parallel processing** - Use multiple workers for large exports

### Performance Configuration

```python
# Performance-optimized export
export_config = {
    'compression': 'snappy',  # Fast compression
    'batch_size': 10000,      # Large batch size
    'max_workers': 4,         # Parallel processing
    'chunk_size': 1000,       # Memory-efficient chunks
    'use_memory_mapping': True  # Memory mapping for large files
}

manager = ExportManager(config=export_config)
```

## Error Handling

### Export Error Recovery

```python
from src.export.export_manager import ExportManager

try:
    manager = ExportManager()
    manager.export_data(data=price_data, indicators=indicator_data)
except IOError as e:
    print(f"File system error: {e}")
    # Retry with different directory
except ValueError as e:
    print(f"Data validation error: {e}")
    # Validate and clean data
except Exception as e:
    print(f"Unexpected error: {e}")
    # Log error and continue
```

### Export Validation

```python
# Validate export files
def validate_export(file_path, expected_format):
    try:
        if expected_format == 'csv':
            # Validate CSV file
            df = pd.read_csv(file_path)
            return len(df) > 0
        elif expected_format == 'parquet':
            # Validate Parquet file
            df = pd.read_parquet(file_path)
            return len(df) > 0
        elif expected_format == 'json':
            # Validate JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data is not None
    except Exception as e:
        print(f"Validation error for {file_path}: {e}")
        return False
```

## Testing

### Export Testing

```bash
# Run export tests
pytest tests/export/ -v

# Test specific formats
pytest tests/export/test_csv_export.py -v
pytest tests/export/test_json_export.py -v
pytest tests/export/test_parquet_export.py -v

# Test performance
pytest tests/export/test_performance.py -v
```

### Export Validation Tests

```bash
# Test export validation
pytest tests/export/test_export_validation.py -v

# Test file integrity
pytest tests/export/test_file_integrity.py -v
```

## Related Documentation

- **[Data Sources](../api/data-sources.md)** - Data acquisition
- **[CLI Interface](cli-interface.md)** - Command-line export
- **[Core Calculations](../reference/core-calculation.md)** - Data processing
- **[Analysis Tools](analysis-tools.md)** - Data analysis features 