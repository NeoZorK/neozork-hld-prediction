# Data Cleaning System Documentation

## Overview

The Data Cleaning System is a comprehensive tool for cleaning financial time series data from multiple sources and formats. It provides automated detection and fixing of common data quality issues with detailed reporting and progress tracking.

## Features

- **Multi-format Support**: Handles Parquet, JSON, and CSV files
- **Multi-source Support**: Works with data from Binance, Polygon, yfinance, and CSV conversions
- **Seven Cleaning Procedures**: Comprehensive data quality checks
- **Interactive CLI**: User-friendly command-line interface
- **Progress Tracking**: Real-time progress bars with ETA
- **Detailed Reporting**: Comprehensive cleaning reports and statistics
- **Automatic Fixing**: Smart automatic fixing of detected issues

## Supported Data Sources

### 1. CSV Converted Data
- **Location**: `data/cache/csv_converted/`
- **Format**: `SYMBOL_PERIOD_TIMEFRAME.parquet`
- **Example**: `GBPUSD_PERIOD_MN1.parquet`

### 2. Raw Parquet Data
- **Location**: `data/raw_parquet/`
- **Format**: `source_SYMBOL_TIMEFRAME.parquet`
- **Example**: `binance_BTCUSD_1h.parquet`

### 3. Indicators Data
- **Locations**: 
  - `data/indicators/parquet/`
  - `data/indicators/json/`
  - `data/indicators/csv/`
- **Format**: `source_SYMBOL_TIMEFRAME_indicator.format`
- **Example**: `polygon_ETHUSD_daily_rsi.json`

## Cleaning Procedures

### 1. Time Series Gaps Detection
- Detects missing time periods in time series data
- Uses median frequency to identify gaps
- Provides gap duration and size information

### 2. Duplicates Detection
- Finds exact duplicate rows
- Groups duplicates for analysis
- Provides sample data for verification

### 3. NaN Values Detection
- Identifies missing values in all columns
- Calculates percentage of missing values
- Provides detailed statistics

### 4. Zero Values Detection
- Detects zero values in numeric columns
- Includes warning about legitimate zero values
- Calculates percentage of zero values

### 5. Negative Values Detection
- Finds negative values in numeric columns
- Includes warning about legitimate negative values
- Calculates percentage of negative values

### 6. Infinity Values Detection
- Detects infinite values (inf, -inf)
- Identifies problematic calculations
- Calculates percentage of infinite values

### 7. Outliers Detection
- Uses multiple methods: IQR, Z-Score, Isolation Forest
- Provides comprehensive outlier analysis
- Calculates percentage of outliers

## Usage

### Basic Usage

```bash
python clear_data.py -f <filename>
```

### Examples

```bash
# Clean CSV converted data
python clear_data.py -f GBPUSD_PERIOD_MN1.parquet

# Clean raw parquet data
python clear_data.py -f binance_BTCUSD_1h.parquet

# Clean indicators data
python clear_data.py -f polygon_ETHUSD_daily_rsi.json
```

### Interactive Workflow

1. **File Validation**: System validates the file exists in supported directories
2. **File Information**: Displays comprehensive file metadata
3. **Cleaning Procedures**: Shows list of procedures to be performed
4. **User Confirmation**: Asks for confirmation to proceed
5. **Procedure Execution**: Runs each procedure with progress tracking
6. **Issue Review**: Shows detailed results for each procedure
7. **Fix Confirmation**: Asks whether to fix detected issues
8. **Final Report**: Displays comprehensive cleaning summary
9. **Save Confirmation**: Asks whether to save cleaned data

## Output Structure

Cleaned data is saved to:
```
data/fixed/<source>/<format>/<symbol>/<indicator>/<timeframe>/
```

Example:
```
data/fixed/binance/parquet/BTCUSD/rsi/1h/BTCUSD_1h_rsi_cleaned.parquet
```

## Configuration

The system automatically detects:
- File format from extension
- Data source from filename pattern
- Symbol and timeframe from filename
- Indicator name (for indicators data)
- DateTime columns for gap detection

## Error Handling

- **Invalid File**: Clear error message with supported directories list
- **Unsupported Format**: Error message with supported formats
- **Data Loading Errors**: Graceful error handling with informative messages
- **Cleaning Errors**: Continues with other procedures if one fails

## Progress Tracking

- Real-time progress bars for each procedure
- ETA calculations based on processing speed
- Animated progress indicators
- Detailed step-by-step progress

## Reporting

### File Information Report
- File size, format, source
- Symbol, timeframe, indicator
- Row and column counts
- Date range and datetime format

### Cleaning Results Report
- Issues found and fixed for each procedure
- Before and after statistics
- Memory usage optimization
- Data quality improvements

### Final Summary Report
- Overall cleaning statistics
- Fix rates and success metrics
- File size reductions
- Data quality improvements

## Dependencies

- pandas
- numpy
- scipy
- scikit-learn
- pyarrow (for parquet support)

## Installation

```bash
# Install dependencies
pip install pandas numpy scipy scikit-learn pyarrow

# Or use uv
uv add pandas numpy scipy scikit-learn pyarrow
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
uv run pytest tests/data_cleaning/ -n auto

# Run specific test module
uv run pytest tests/data_cleaning/test_data_validator.py -v

# Run with coverage
uv run pytest tests/data_cleaning/ --cov=src/data_cleaning --cov-report=html
```

## Architecture

The system is built with a modular architecture:

- **Main Script**: `clear_data.py` - CLI interface and orchestration
- **Data Validator**: File validation and metadata extraction
- **File Operations**: Multi-format data I/O
- **Cleaning Procedures**: Seven data cleaning algorithms
- **Progress Tracker**: Real-time progress monitoring
- **Reporting**: Comprehensive reporting and statistics

## Contributing

When adding new cleaning procedures:

1. Add detection method to `CleaningProcedures` class
2. Add fixing method for the procedure
3. Update the main workflow in `clear_data.py`
4. Add comprehensive tests
5. Update documentation

## License

This project is part of the Neozork HLD Prediction system.
