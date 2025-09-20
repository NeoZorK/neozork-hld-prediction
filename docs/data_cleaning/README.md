# Data Cleaning System

## Quick Start

```bash
# Clean a data file
uv run python clear_data.py -f <filename>

# Examples
uv run python clear_data.py -f GBPUSD_PERIOD_MN1.parquet
uv run python clear_data.py -f binance_BTCUSD_1h.parquet
uv run python clear_data.py -f polygon_ETHUSD_daily_rsi.json
```

## Features

- ✅ **7 Cleaning Procedures**: Gaps, Duplicates, NaN, Zeros, Negative, Infinity, Outliers
- ✅ **Multi-format Support**: Parquet, JSON, CSV
- ✅ **Multi-source Support**: Binance, Polygon, yfinance, CSV conversions
- ✅ **Interactive CLI**: User-friendly command-line interface
- ✅ **Progress Tracking**: Real-time progress bars with ETA
- ✅ **Detailed Reporting**: Comprehensive cleaning reports
- ✅ **Automatic Fixing**: Smart automatic fixing of detected issues
- ✅ **100% Test Coverage**: Comprehensive unit tests

## Supported Data Sources

| Source | Location | Format | Example |
|--------|----------|--------|---------|
| CSV Converted | `data/cache/csv_converted/` | `SYMBOL_PERIOD_TIMEFRAME.parquet` | `GBPUSD_PERIOD_MN1.parquet` |
| Raw Parquet | `data/raw_parquet/` | `source_SYMBOL_TIMEFRAME.parquet` | `binance_BTCUSD_1h.parquet` |
| Indicators | `data/indicators/{parquet,json,csv}/` | `source_SYMBOL_TIMEFRAME_indicator.format` | `polygon_ETHUSD_daily_rsi.json` |

## Installation

```bash
# Install dependencies
uv add pandas numpy scipy scikit-learn pyarrow

# Or install from requirements
pip install -r requirements.txt
```

## Testing

```bash
# Run all tests
uv run pytest tests/data_cleaning/ -n auto

# Run with coverage
uv run pytest tests/data_cleaning/ --cov=src/data_cleaning --cov-report=html
```

## Architecture

```
clear_data.py                 # Main CLI script
src/data_cleaning/
├── __init__.py              # Module initialization
├── data_validator.py        # File validation & metadata extraction
├── file_operations.py       # Multi-format I/O operations
├── cleaning_procedures.py   # 7 cleaning algorithms
├── progress_tracker.py      # Progress bars & ETA
└── reporting.py             # Detailed reporting & statistics
```

## Documentation

- [Full Documentation](index.md)
- [API Reference](api_reference.md)

## License

Part of the Neozork HLD Prediction system.
