# Scripts Guide

Available scripts and automation tools.

## Main Scripts

### `run_analysis.py`
Main analysis engine:

```bash
python run_analysis.py demo
python run_analysis.py --examples
python run_analysis.py --help
```

### `nz` Command
Universal shortcut (works in Docker/local):

```bash
nz demo
nz yf -t AAPL --period 1mo
nz csv --csv-file data.csv
```

## Setup Scripts

### `scripts/init_dirs.sh`
Initialize project structure:

```bash
./scripts/init_dirs.sh
```

### `scripts/analyze_requirements.py`
Analyze dependencies:

```bash
python scripts/analyze_requirements.py
```

## Testing Scripts

### `test-workflow.sh`
Test GitHub Actions locally:

```bash
./test-workflow.sh
```

### `scripts/run_tests.py`
Run all tests:

```bash
python scripts/run_tests.py
```

## Utility Scripts

Data conversion and test file management:

### `scripts/recreate_csv.py`
Convert JSON indicator files to CSV format:

```bash
python scripts/recreate_csv.py
```

### `scripts/create_test_parquet.py`
Convert JSON indicator files to Parquet format:

```bash
python scripts/create_test_parquet.py
```

For detailed usage and troubleshooting: [Utility Scripts](utility-scripts.md)

## Debug Scripts

Located in `scripts/debug_scripts/`:

- `debug_yfinance.py` - Test Yahoo Finance connection
- `debug_polygon_connection.py` - Test Polygon API
- `debug_binance_connection.py` - Test Binance API
- `examine_parquet.py` - Inspect Parquet files

```bash
python scripts/debug_scripts/debug_yfinance.py
```

For more details: [Debug Scripts](debug-scripts.md)