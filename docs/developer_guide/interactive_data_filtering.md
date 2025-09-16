# Interactive Data Filtering System

## Overview

The Interactive Data Filtering System replaces the static data loading menu with a dynamic, searchable interface that allows users to filter data by multiple criteria including format, source, symbol, and indicator.

## Features

### 1. Quick Filter Interface
Users can enter filter criteria in a single string format:
```
parquet binance BTCUSDT wave
json csvexport EURUSD rsi
csv polygon AAPL macd
```

### 2. Step-by-Step Filtering
Interactive guided filtering through each criterion:
- Format (parquet, json, csv)
- Source (binance, csvexport, polygon, yfinance)
- Symbol (BTCUSDT, EURUSD, BTCUSD, etc.)
- Indicator (wave, rsi_mom, macd, etc.)

### 3. Advanced Search Capabilities
- Keyword search across filenames and metadata
- Timeframe filtering (M5, D1, H1, etc.)
- Partial matching with autocomplete
- Real-time validation and error handling

## Usage

### Accessing the Filter System

1. Start the interactive application:
   ```bash
   uv run ./interactive
   ```

2. Navigate to "Load Data" → "Indicators"

3. Choose from three filtering options:
   - **Quick Filter**: Enter criteria in one line
   - **Step-by-Step**: Guided filtering process
   - **Show All Data**: View available data first

### Quick Filter Examples

```bash
# Load parquet data from Binance for BTCUSDT with wave indicator
parquet binance BTCUSDT wave

# Load JSON data from CSV export for EURUSD with RSI indicator
json csvexport EURUSD rsi

# Load CSV data from Polygon for AAPL with MACD indicator
csv polygon AAPL macd
```

### Step-by-Step Filtering

1. **Format Selection**: Choose from available formats
2. **Source Selection**: Select data source
3. **Symbol Selection**: Pick trading pair
4. **Indicator Selection**: Choose technical indicator

### Advanced Features

#### Keyword Search
```python
# Search for files containing specific keywords
filtered_files = data_filter.search_files_by_keywords(
    files_info, 
    ["BTC", "wave", "M5"]
)
```

#### Timeframe Filtering
```python
# Filter by specific timeframes
filtered_files = data_filter.filter_by_timeframe(
    files_info, 
    ["M5", "D1", "H1"]
)
```

#### Statistics and Analysis
```python
# Get detailed statistics about filtered files
stats = data_filter.get_file_statistics(filtered_files)
data_filter.display_statistics(filtered_files)
```

## Implementation Details

### DataFilter Class

The `DataFilter` class provides the core filtering functionality:

```python
from src.interactive.data_management.data_filter import DataFilter

# Initialize filter
data_filter = DataFilter()

# Set available data
data_filter.set_available_data(files_info)

# Apply filters
filtered_files = data_filter.filter_files(
    files_info,
    format_filter="parquet",
    source_filter="binance",
    symbol_filter="BTCUSDT",
    indicator_filter="wave"
)
```

### Key Methods

- `filter_files()`: Main filtering method
- `quick_filter()`: Single-string filtering
- `search_files_by_keywords()`: Keyword-based search
- `filter_by_timeframe()`: Timeframe-based filtering
- `get_filter_suggestions()`: Get available filter values
- `display_filtered_results()`: Show filtered results
- `get_file_statistics()`: Get statistics about filtered files

## Error Handling

The system includes comprehensive error handling:

- **Input Validation**: Validates filter criteria against available options
- **Partial Matching**: Suggests alternatives for invalid inputs
- **Autocomplete**: Auto-completes partial matches when unique
- **Error Recovery**: Allows retry on invalid inputs
- **Graceful Degradation**: Continues operation even with some errors

## Testing

The system includes comprehensive unit tests:

```bash
# Run all data filter tests
uv run pytest tests/test_data_filter.py -v

# Run specific test
uv run pytest tests/test_data_filter.py::TestDataFilter::test_quick_filter -v
```

## Benefits

1. **Improved User Experience**: Intuitive filtering interface
2. **Flexible Search**: Multiple ways to find and filter data
3. **Real-time Feedback**: Immediate validation and suggestions
4. **Error Prevention**: Comprehensive input validation
5. **Scalability**: Handles large datasets efficiently
6. **Maintainability**: Well-structured, tested code

## Future Enhancements

- **Saved Filters**: Save and reuse common filter combinations
- **Filter History**: Track and recall previous filter selections
- **Advanced Search**: Regex-based pattern matching
- **Bulk Operations**: Apply filters to multiple datasets
- **Export Filters**: Save filter configurations to files
