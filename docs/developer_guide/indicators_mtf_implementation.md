# Indicators MTF Implementation Guide

This document provides technical details about the implementation of the Indicators MTF (Multi-Timeframe) structure functionality.

## Architecture Overview

The Indicators MTF functionality is implemented using a modular architecture with the following components:

```
src/interactive/data_management/indicators/
├── indicators_mtf_creator.py      # Main MTF creation logic
├── indicators_analyzer.py         # Data analysis and validation
├── indicators_loader.py           # Data loading functionality
└── indicators_processor.py        # Data processing and cleaning
```

## Core Components

### IndicatorsMTFCreator

The main class responsible for creating MTF structures from indicators data.

**Key Methods:**
- `create_mtf_from_processed_data()`: Creates MTF structure from processed data
- `create_and_save_mtf_structure()`: Creates and saves MTF structure to disk
- `create_mtf_from_all_indicators()`: Processes all indicators and creates MTF structures
- `_group_data_by_symbol()`: Groups data by trading symbol
- `_extract_symbol_from_data()`: Extracts symbol from filename or data

**Dependencies:**
- pandas: Data manipulation
- numpy: Numerical operations
- pathlib: File system operations
- json: Metadata serialization

### Data Flow

1. **Data Loading**: Load indicators data from various formats (parquet, csv, json)
2. **Data Processing**: Clean and validate the loaded data
3. **Symbol Grouping**: Group data by trading symbol
4. **MTF Creation**: Create Multi-Timeframe structure
5. **Cross-Feature Engineering**: Generate cross-timeframe features
6. **Data Quality Assessment**: Calculate quality metrics
7. **Structure Validation**: Validate MTF structure integrity
8. **File Persistence**: Save to disk with metadata

## Implementation Details

### Symbol Detection Algorithm

The system uses a multi-step approach to detect trading symbols:

1. **Filename Analysis**: Parse filename for common symbol patterns
2. **Data Inspection**: Check data structure for symbol information
3. **Pattern Matching**: Use regex patterns for known trading pairs
4. **Fallback Handling**: Default to 'UNKNOWN' if detection fails

```python
def _extract_symbol_from_data(self, filename: str, data: Dict[str, Any]) -> str:
    # Try filename patterns first
    if '_' in filename:
        parts = filename.split('_')
        for part in parts:
            if part.upper() in KNOWN_SYMBOLS:
                return part.upper()
    
    # Try data structure
    if 'symbol' in data:
        return data['symbol'].upper()
    
    # Fallback
    return 'UNKNOWN'
```

### Timeframe Priority System

Timeframes are prioritized for main timeframe selection:

```python
timeframe_priority = {
    'M1': 1, 'M5': 2, 'M15': 3, 'M30': 4,
    'H1': 5, 'H4': 6, 'D1': 7, 'W1': 8, 'MN1': 9
}
```

### Cross-Timeframe Feature Engineering

The system creates various cross-timeframe features:

- **Lagged Values**: Previous values with configurable lags
- **Moving Averages**: Multiple window sizes
- **Volatility Measures**: Rolling standard deviation
- **Momentum Indicators**: Percentage change calculations

```python
def _create_cross_timeframe_features(self, organized_data, main_timeframe):
    cross_features = {}
    
    for timeframe in other_timeframes:
        # Create lagged values
        for lag in [1, 2, 3, 5, 10]:
            df[f'{indicator}_{timeframe}_lag_{lag}'] = df['value'].shift(lag)
        
        # Create moving averages
        for window in [5, 10, 20, 50]:
            df[f'{indicator}_{timeframe}_ma_{window}'] = df['value'].rolling(window).mean()
        
        # Create volatility measures
        df[f'{indicator}_{timeframe}_volatility'] = df['value'].rolling(20).std()
```

### Data Quality Metrics

The system calculates comprehensive data quality metrics:

```python
def _calculate_data_quality_metrics(self, mtf_data):
    metrics = {
        'completeness': 0.0,    # Non-null percentage
        'consistency': 0.0,     # Data type consistency
        'validity': 0.0,        # Value range validity
        'overall_score': 0.0    # Weighted average
    }
    
    # Completeness calculation
    total_cells = df.size
    non_null_cells = df.count().sum()
    metrics['completeness'] = (non_null_cells / total_cells) * 100
    
    # Consistency calculation
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    metrics['consistency'] = (len(numeric_cols) / len(df.columns)) * 100
    
    # Validity calculation
    # Check for reasonable value ranges and patterns
    # ...
    
    return metrics
```

## File Structure

### Main Data File Format

The main data file contains indicators as columns:

```python
# Pivot table creation
pivot_df = main_df.pivot_table(
    index='timestamp',
    columns='indicator',
    values='value',
    aggfunc='first'
)

# Add metadata columns
pivot_df['symbol'] = symbol.upper()
pivot_df['timeframe'] = main_timeframe
```

### Metadata Structure

Comprehensive metadata is stored in JSON format:

```python
metadata = {
    'created_at': datetime.now().isoformat(),
    'symbol': symbol,
    'source': source,
    'main_timeframe': main_timeframe,
    'timeframes': timeframes,
    'indicators': indicators,
    'total_rows': total_rows,
    'data_quality': quality_metrics,
    'main_data_shape': main_data.shape,
    'cross_timeframes_count': len(cross_features)
}
```

## Error Handling

### Exception Handling Strategy

The system uses a comprehensive error handling approach:

1. **Graceful Degradation**: Continue processing even if some files fail
2. **Detailed Logging**: Log all errors with context information
3. **User Feedback**: Provide clear error messages to users
4. **Recovery Mechanisms**: Attempt to recover from common errors

```python
try:
    # Process data
    result = self.create_mtf_structure(data)
    return {'status': 'success', 'data': result}
except FileNotFoundError as e:
    print_error(f"File not found: {e}")
    return {'status': 'error', 'message': str(e)}
except pd.errors.EmptyDataError as e:
    print_error(f"Empty data file: {e}")
    return {'status': 'error', 'message': str(e)}
except Exception as e:
    print_error(f"Unexpected error: {e}")
    return {'status': 'error', 'message': str(e)}
```

### Validation Framework

The system includes comprehensive validation:

```python
def _validate_mtf_structure(self, mtf_data):
    errors = []
    
    # Check required fields
    required_fields = ['symbol', 'main_timeframe', 'indicators', 'timeframes', 'main_data']
    for field in required_fields:
        if field not in mtf_data:
            errors.append(f"Missing required field: {field}")
    
    # Check data integrity
    if mtf_data['main_data'].empty:
        errors.append("Main data is empty")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }
```

## Performance Optimization

### Memory Management

- **Chunked Processing**: Process large datasets in chunks
- **Memory Monitoring**: Track memory usage during processing
- **Garbage Collection**: Explicit cleanup of large objects

### Progress Tracking

- **Real-time Updates**: Show progress with ETA calculations
- **Speed Monitoring**: Track processing speed
- **User Feedback**: Provide meaningful progress messages

```python
def _show_mtf_progress(self, message: str, progress: float, start_time: float):
    bar_length = 40
    filled_length = int(bar_length * progress)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    
    # Calculate ETA
    elapsed_time = time.time() - start_time
    if progress > 0:
        eta_seconds = (elapsed_time / progress) - elapsed_time
        eta_str = self._format_time(eta_seconds)
    else:
        eta_str = "Calculating..."
    
    print(f"\r{message} [{bar}] {int(progress * 100)}% ETA: {eta_str}", end="")
```

## Testing Strategy

### Unit Tests

Comprehensive unit tests cover all major functionality:

- **Data Loading Tests**: Test various data formats and sources
- **Symbol Detection Tests**: Test symbol extraction algorithms
- **MTF Creation Tests**: Test MTF structure creation
- **Error Handling Tests**: Test error scenarios and recovery
- **Validation Tests**: Test data validation and quality metrics

### Integration Tests

Integration tests verify end-to-end functionality:

- **Menu Integration**: Test interactive menu integration
- **File System Tests**: Test file creation and organization
- **Data Pipeline Tests**: Test complete data processing pipeline

### Test Data

Mock data generators create realistic test scenarios:

```python
def create_sample_indicators_data(self):
    timestamps = pd.date_range('2023-01-01', periods=100, freq='1min')
    
    rsi_data = pd.DataFrame({
        'timestamp': timestamps,
        'value': np.random.uniform(0, 100, 100),
        'indicator': 'RSI',
        'timeframe': 'M1'
    }).set_index('timestamp')
    
    return {'btcusdt_rsi_m1.parquet': {'data': rsi_data, ...}}
```

## Configuration

### Path Configuration

The system uses configurable paths:

```python
def __init__(self):
    self.project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    self.data_root = self.project_root / "data"
    self.cleaned_root = self.data_root / "cleaned_data"
    self.mtf_root = self.cleaned_root / "mtf_structures"
    self.indicators_mtf_root = self.mtf_root / "indicators"
```

### Symbol Configuration

Known trading symbols are configurable:

```python
KNOWN_SYMBOLS = [
    'BTCUSDT', 'ETHUSDT', 'EURUSD', 'GBPUSD',
    'GOOG', 'TSLA', 'US500', 'XAUUSD'
]
```

## Future Enhancements

### Planned Features

1. **Parallel Processing**: Multi-threaded data processing
2. **Caching System**: Intelligent caching of processed data
3. **Custom Indicators**: Support for user-defined indicators
4. **Real-time Updates**: Live data processing capabilities
5. **Advanced Features**: More sophisticated cross-timeframe features

### Extension Points

The system is designed for easy extension:

- **Custom Symbol Detectors**: Add new symbol detection algorithms
- **Custom Feature Engineers**: Add new cross-timeframe features
- **Custom Validators**: Add new data validation rules
- **Custom Exporters**: Add new output formats

## Maintenance

### Code Quality

- **Type Hints**: Comprehensive type annotations
- **Documentation**: Detailed docstrings and comments
- **Error Messages**: Clear and actionable error messages
- **Logging**: Structured logging for debugging

### Monitoring

- **Performance Metrics**: Track processing times and memory usage
- **Error Rates**: Monitor error frequencies and patterns
- **Data Quality**: Track data quality trends over time
- **User Feedback**: Collect and analyze user feedback

## Conclusion

The Indicators MTF implementation provides a robust, scalable solution for organizing indicators data in a Multi-Timeframe structure. The modular architecture, comprehensive error handling, and extensive testing make it suitable for production use in machine learning and trading applications.
