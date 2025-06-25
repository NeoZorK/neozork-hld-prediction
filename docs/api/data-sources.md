# Data Sources Reference

Comprehensive documentation for all data acquisition sources and fetchers.

## Overview

The data acquisition module provides unified access to multiple financial data sources through a consistent interface.

## Data Sources

### 1. Yahoo Finance (`yfinance_fetcher.py`)

Free stock and forex data from Yahoo Finance.

#### Features
- **Real-time data** - Live market data
- **Historical data** - Extensive historical datasets
- **Multiple timeframes** - 1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo, 3mo
- **Global markets** - Stocks, forex, commodities, indices

#### Usage Example

```python
from src.data.fetchers.yfinance_fetcher import YFinanceFetcher

# Initialize fetcher
fetcher = YFinanceFetcher()

# Fetch stock data
data = fetcher.fetch_data(
    symbol='AAPL',
    period='1y',
    interval='1d',
    point_size=0.01
)

# Fetch forex data
forex_data = fetcher.fetch_data(
    symbol='EURUSD=X',
    period='6mo',
    interval='1h',
    point_size=0.00001
)
```

#### Parameters
- **`symbol`** - Stock/forex symbol (e.g., 'AAPL', 'EURUSD=X')
- **`period`** - Data period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
- **`interval`** - Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
- **`point_size`** - Price precision for calculations

### 2. Binance (`binance_fetcher.py`)

Cryptocurrency data from Binance exchange.

#### Features
- **Real-time crypto data** - Live cryptocurrency prices
- **Multiple pairs** - All available trading pairs
- **High-frequency data** - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
- **WebSocket support** - Real-time streaming data

#### Usage Example

```python
from src.data.fetchers.binance_fetcher import BinanceFetcher

# Initialize fetcher
fetcher = BinanceFetcher()

# Fetch BTC/USDT data
data = fetcher.fetch_data(
    symbol='BTCUSDT',
    interval='1h',
    limit=1000,
    point_size=0.01
)
```

#### Parameters
- **`symbol`** - Trading pair (e.g., 'BTCUSDT', 'ETHUSDT')
- **`interval`** - Time interval
- **`limit`** - Number of data points (max 1000)
- **`point_size`** - Price precision

### 3. Polygon.io (`polygon_fetcher.py`)

Professional market data (requires API key).

#### Features
- **Professional data** - High-quality market data
- **Real-time feeds** - Live market data streams
- **Historical data** - Comprehensive historical datasets
- **Multiple asset classes** - Stocks, forex, crypto, options

#### Setup

```bash
# Set API key
export POLYGON_API_KEY="your_api_key_here"
```

#### Usage Example

```python
from src.data.fetchers.polygon_fetcher import PolygonFetcher

# Initialize fetcher
fetcher = PolygonFetcher(api_key="your_api_key")

# Fetch stock data
data = fetcher.fetch_data(
    symbol='AAPL',
    from_date='2024-01-01',
    to_date='2024-12-01',
    interval='1d',
    point_size=0.01
)
```

#### Parameters
- **`symbol`** - Asset symbol
- **`from_date`** - Start date (YYYY-MM-DD)
- **`to_date`** - End date (YYYY-MM-DD)
- **`interval`** - Time interval
- **`point_size`** - Price precision

### 4. Exchange Rate API (`exrate_fetcher.py`)

Real-time forex exchange rates.

#### Features
- **160+ currencies** - Global currency coverage
- **Real-time rates** - Live exchange rates
- **Historical data** - Historical rate data
- **Multiple timeframes** - Daily, weekly, monthly data

#### Usage Example

```python
from src.data.fetchers.exrate_fetcher import ExRateFetcher

# Initialize fetcher
fetcher = ExRateFetcher()

# Fetch current EUR/USD rate
data = fetcher.fetch_data(
    base_currency='EUR',
    target_currency='USD',
    interval='D1',
    point_size=0.00001
)
```

#### Parameters
- **`base_currency`** - Base currency code (e.g., 'EUR', 'USD')
- **`target_currency`** - Target currency code (e.g., 'USD', 'GBP')
- **`interval`** - Time interval ('D1', 'W1', 'M1')
- **`point_size`** - Price precision

### 5. CSV Files (`csv_fetcher.py`)

Local CSV file data import.

#### Features
- **Local data** - Import your own CSV files
- **Flexible format** - Support for various CSV formats
- **Data validation** - Automatic data quality checks
- **Format conversion** - Convert to standard OHLCV format

#### CSV Format Requirements

```csv
timestamp,open,high,low,close,volume
2024-01-01 09:30:00,150.00,151.50,149.80,150.25,1000000
2024-01-01 09:31:00,150.25,150.80,150.10,150.60,950000
```

#### Usage Example

```python
from src.data.fetchers.csv_fetcher import CSVFetcher

# Initialize fetcher
fetcher = CSVFetcher()

# Load CSV file
data = fetcher.fetch_data(
    file_path='data/my_data.csv',
    point_size=0.01,
    date_column='timestamp',
    price_columns=['open', 'high', 'low', 'close'],
    volume_column='volume'
)
```

#### Parameters
- **`file_path`** - Path to CSV file
- **`point_size`** - Price precision
- **`date_column`** - Column name for timestamps
- **`price_columns`** - List of OHLC column names
- **`volume_column`** - Column name for volume data

### 6. Demo Data (`demo_fetcher.py`)

Synthetic data for testing and demonstration.

#### Features
- **Synthetic data** - Generated test data
- **Configurable** - Customizable data parameters
- **Consistent format** - Standard OHLCV format
- **No external dependencies** - Works offline

#### Usage Example

```python
from src.data.fetchers.demo_fetcher import DemoFetcher

# Initialize fetcher
fetcher = DemoFetcher()

# Generate demo data
data = fetcher.fetch_data(
    periods=1000,
    point_size=0.01,
    volatility=0.02,
    trend=0.001
)
```

#### Parameters
- **`periods`** - Number of data points
- **`point_size`** - Price precision
- **`volatility`** - Price volatility level
- **`trend`** - Price trend direction

## Data Acquisition Manager (`data_acquisition.py`)

Unified interface for all data sources.

### Features
- **Unified API** - Consistent interface across all sources
- **Source selection** - Automatic source selection based on symbol
- **Data validation** - Quality checks for all data
- **Error handling** - Robust error management
- **Caching** - Data caching for performance

### Usage Example

```python
from src.data.data_acquisition import DataAcquisition

# Initialize manager
manager = DataAcquisition()

# Fetch data from any source
data = manager.fetch_data(
    source='yfinance',  # or 'binance', 'polygon', 'exrate', 'csv'
    symbol='AAPL',
    period='1y',
    interval='1d',
    point_size=0.01
)

# Auto-detect source based on symbol
data = manager.fetch_data(
    symbol='BTCUSDT',  # Auto-detects Binance
    interval='1h',
    limit=1000,
    point_size=0.01
)
```

### Source Auto-Detection

The manager automatically selects the appropriate data source:

- **Stocks**: Yahoo Finance or Polygon.io
- **Forex**: Yahoo Finance or Exchange Rate API
- **Crypto**: Binance
- **Custom**: CSV files

## Data Format

### Standard OHLCV Format

All data sources return data in a consistent format:

```python
import pandas as pd

# Standard format
data = pd.DataFrame({
    'timestamp': pd.DatetimeIndex([...]),
    'open': [...],
    'high': [...],
    'low': [...],
    'close': [...],
    'volume': [...],
    'point_size': 0.01  # Price precision
})
```

### Data Quality Features

- **Automatic validation** - Check for missing values and outliers
- **Data cleaning** - Remove invalid data points
- **Format standardization** - Convert to standard OHLCV format
- **Time alignment** - Ensure proper chronological order

## Error Handling

### Common Errors

- **API rate limits** - Too many requests
- **Invalid symbols** - Symbol not found
- **Network issues** - Connection problems
- **Data format errors** - Invalid CSV format

### Error Recovery

```python
from src.data.data_acquisition import DataAcquisition

try:
    manager = DataAcquisition()
    data = manager.fetch_data(symbol='AAPL', period='1y')
except ConnectionError as e:
    print(f"Network error: {e}")
    # Retry with exponential backoff
except ValueError as e:
    print(f"Invalid parameters: {e}")
    # Validate parameters
except Exception as e:
    print(f"Unexpected error: {e}")
    # Log and handle gracefully
```

## Performance Optimization

### Caching

```python
from src.data.data_acquisition import DataAcquisition

# Enable caching
manager = DataAcquisition(enable_cache=True, cache_ttl=3600)

# Cached data will be reused for 1 hour
data = manager.fetch_data(symbol='AAPL', period='1d')
```

### Batch Processing

```python
# Fetch multiple symbols efficiently
symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
data_dict = {}

for symbol in symbols:
    data_dict[symbol] = manager.fetch_data(symbol=symbol, period='1mo')
```

## Testing

### Unit Tests

```bash
# Run data fetcher tests
pytest tests/data/fetchers/ -v

# Run specific fetcher tests
pytest tests/data/fetchers/test_yfinance_fetcher.py -v
pytest tests/data/fetchers/test_binance_fetcher.py -v
```

### Integration Tests

```bash
# Run integration tests
pytest tests/data/integration/ -v

# Test data quality
pytest tests/data/test_data_quality.py -v
```

## Configuration

### Environment Variables

```bash
# API Keys
export POLYGON_API_KEY="your_polygon_api_key"
export BINANCE_API_KEY="your_binance_api_key"
export BINANCE_SECRET_KEY="your_binance_secret"

# Cache settings
export DATA_CACHE_ENABLED="true"
export DATA_CACHE_TTL="3600"

# Rate limiting
export YFINANCE_RATE_LIMIT="100"
export BINANCE_RATE_LIMIT="1200"
```

## Related Documentation

- **[Core Calculations](../reference/core-calculation.md)** - Data processing
- **[CLI Interface](../guides/cli-interface.md)** - Command-line usage
- **[Export Functions](../guides/export-functions.md)** - Data export
- **[Analysis Tools](../guides/analysis-tools.md)** - Data analysis 