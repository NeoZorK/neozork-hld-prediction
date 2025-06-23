# Debug Scripts

This document describes the debug scripts available in the `scripts/debug_scripts/` directory.

## Overview

Debug scripts are utility scripts designed to test and verify various components of the system, particularly external API connections and data sources.

## Available Scripts

### API Connection Scripts

#### `debug_binance.py`
Tests Binance API connection and data fetching.

**Usage:**
```bash
python scripts/debug_scripts/debug_binance.py
```

**Requirements:**
- `BINANCE_API_KEY` environment variable
- `BINANCE_API_SECRET` environment variable

**What it does:**
- Creates a BinanceFetcher instance
- Fetches recent BTCUSDT data (1h timeframe, 10 records)
- Reports success or failure

#### `debug_polygon.py`
Tests Polygon API connection and data fetching.

**Usage:**
```bash
python scripts/debug_scripts/debug_polygon.py
```

**Requirements:**
- `POLYGON_API_KEY` environment variable

**What it does:**
- Creates a PolygonFetcher instance
- Fetches recent AAPL data (daily timeframe, 10 records)
- Reports success or failure

#### `debug_yfinance.py`
Tests YFinance data fetching.

**Usage:**
```bash
python scripts/debug_scripts/debug_yfinance.py
```

**What it does:**
- Tests YFinance data fetching for various symbols
- No API key required

### Data Analysis Scripts

#### `examine_parquet.py`
Analyzes Parquet files in the data directory.

**Usage:**
```bash
python scripts/debug_scripts/examine_parquet.py
```

**What it does:**
- Scans for Parquet files in data directories
- Displays file information and sample data
- Helps verify data integrity

#### `examine_binance_parquet.py`
Specifically analyzes Binance Parquet files.

**Usage:**
```bash
python scripts/debug_scripts/examine_binance_parquet.py
```

### Connection Testing Scripts

#### `debug_binance_connection.py`
Detailed Binance connection testing.

**Usage:**
```bash
python scripts/debug_scripts/debug_binance_connection.py
```

#### `debug_polygon_connection.py`
Detailed Polygon connection testing.

**Usage:**
```bash
python scripts/debug_scripts/debug_polygon_connection.py
```

#### `debug_polygon_resolve.py`
Tests Polygon symbol resolution.

**Usage:**
```bash
python scripts/debug_scripts/debug_polygon_resolve.py
```

### Data Processing Scripts

#### `debug_csv_reader.py`
Tests CSV file reading functionality.

**Usage:**
```bash
python scripts/debug_scripts/debug_csv_reader.py
```

#### `debug_check_parquet.py`
Basic Parquet file checking.

**Usage:**
```bash
python scripts/debug_scripts/debug_check_parquet.py
```

## Running in Docker

All debug scripts can be run inside the Docker container:

```bash
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_binance.py
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_polygon.py
```

## Integration with Test Runner

These scripts are integrated with the Docker test runner (`tests/run_tests_docker.py`) and can be executed as part of the test suite:

```bash
# Run all external data source tests
python tests/run_tests_docker.py --all

# Run specific category
python tests/run_tests_docker.py --categories binance
python tests/run_tests_docker.py --categories polygon
python tests/run_tests_docker.py --categories yfinance
python tests/run_tests_docker.py --categories parquet
```

## Error Handling

All debug scripts include proper error handling and will:
- Check for required environment variables
- Provide informative error messages
- Exit with appropriate status codes (0 for success, 1 for failure)

## Environment Variables

Make sure to set the following environment variables for API testing:

```bash
export BINANCE_API_KEY="your_binance_api_key"
export BINANCE_API_SECRET="your_binance_api_secret"
export POLYGON_API_KEY="your_polygon_api_key"
```

These can be set in your shell or in the `docker.env` file for Docker usage. 