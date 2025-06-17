# Debug Scripts

Tools for testing and debugging data connections and file formats.

## API Connection Tests

### `debug_yfinance.py`
Test Yahoo Finance data fetching:

```bash
python scripts/debug_scripts/debug_yfinance.py
```

### `debug_polygon_connection.py`
Test Polygon API connection:

```bash
export POLYGON_API_KEY="your_key"
python scripts/debug_scripts/debug_polygon_connection.py
```

### `debug_binance_connection.py`
Test Binance API connection:

```bash
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"
python scripts/debug_scripts/debug_binance_connection.py
```

## File Analysis Tools

### `examine_parquet.py`
Inspect Parquet file structure:

```bash
python scripts/debug_scripts/examine_parquet.py data/file.parquet
```

### `debug_check_parquet.py`
Validate Parquet files:

```bash
python scripts/debug_scripts/debug_check_parquet.py
```

### `debug_csv_reader.py`
Test CSV reading capabilities:

```bash
python scripts/debug_scripts/debug_csv_reader.py data/file.csv
```

## Usage Tips

- Run debug scripts before main analysis to verify data sources
- Check API keys are properly set before running connection tests
- Use file analysis tools to understand data structure before processing

For main scripts: [Scripts Guide](scripts.md)