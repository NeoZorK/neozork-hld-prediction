# Usage Examples

Comprehensive command reference for all analysis modes and options.

## Quick Reference Command

View all examples in the terminal:
```bash
python run_analysis.py --examples
```

## Demo Mode

Perfect for testing without external data dependencies.

```bash
# Basic demo
python run_analysis.py demo
nz demo

# Specific trading rules
nz demo --rule PV_HighLow
nz demo --rule PHLD
nz demo --rule SR

# Different plotting backends
nz demo -d mpl
nz demo --rule PHLD -d plotly
nz demo --rule PV -d seaborn
```

## CSV File Analysis

Analyze MT5 exported data or custom CSV files.

```bash
# Basic CSV analysis
nz csv --csv-file data/your_file.csv --point 0.01

# With specific rules
nz csv --csv-file data/EURUSD_M1.csv --point 0.00001 --rule PHLD
nz csv --csv-file data/XAUUSD_MN1.csv --point 0.01 --rule SR

# With advanced plotting
nz csv --csv-file data/BTCUSD.csv --point 0.01 --rule PV -d plotly
nz csv --csv-file data/stocks.csv --point 0.01 --rule PHLD -d mplfinance
```

## Yahoo Finance Mode

Free real-time and historical data.

### Forex Analysis
```bash
# Major pairs
nz yf -t EURUSD=X --period 1mo --point 0.00001
nz yf -t GBPUSD=X --period 3mo --point 0.00001 --rule PHLD
nz yf -t USDJPY=X --start 2024-01-01 --end 2024-06-01 --point 0.001

# With specific date ranges
nz yf -t EURUSD=X --start 2024-01-01 --end 2024-12-31 --point 0.00001 -d mpl
```

### Stock Analysis
```bash
# Popular stocks
nz yf -t AAPL --period 6mo --point 0.01
nz yf -t TSLA --period 1y --point 0.01 --rule SR
nz yf -t MSFT --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule PV

# With advanced analysis
nz yf -t AAPL --period 1y --rule PHLD -d seaborn
```

### Cryptocurrency
```bash
# Major crypto pairs
nz yf -t BTC-USD --period 3mo --point 0.01
nz yf -t ETH-USD --period 6mo --point 0.01 --rule PHLD
nz yf -t BTC-USD --start 2024-01-01 --end 2024-12-31 --point 0.01 -d plotly
```

## Polygon.io Mode

Professional-grade market data (requires API key).

### Setup
Add to your `.env` file:
```env
POLYGON_API_KEY=your_polygon_api_key_here
```

### Usage Examples
```bash
# Stock data
nz polygon --ticker AAPL --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01
nz polygon --ticker TSLA --interval H1 --start 2024-01-01 --end 2024-06-01 --point 0.01 --rule PV

# Forex data
nz polygon --ticker C:EURUSD --interval H1 --start 2024-01-01 --end 2024-03-01 --point 0.00001
nz polygon --ticker C:GBPUSD --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.00001 --rule SR

# Crypto data
nz polygon --ticker X:BTCUSD --interval H1 --start 2024-01-01 --end 2024-02-01 --point 0.01 --rule PHLD
```

## Binance Mode

Cryptocurrency spot market data.

### Setup
Add to your `.env` file:
```env
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here
```

### Usage Examples
```bash
# Popular crypto pairs
nz binance --ticker BTCUSDT --interval H1 --start 2024-01-01 --end 2024-04-18 --point 0.01
nz binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule SR
nz binance --ticker ADAUSDT --interval H4 --start 2024-01-01 --end 2024-06-01 --point 0.001 --rule PHLD

# High-frequency analysis
nz binance --ticker BTCUSDT --interval M15 --start 2024-01-01 --end 2024-01-07 --point 0.01 --rule PV -d fastest
```

## Show Mode (Data Browsing)

Explore and analyze cached data files.

### List Data
```bash
# Show all cached files
nz show

# Filter by data source
nz show yf
nz show polygon
nz show binance
nz show csv
```

### Search and Filter
```bash
# Search by keywords
nz show yf aapl
nz show binance btc
nz show polygon eurusd
nz show csv xauusd mn1

# Multiple keywords
nz show binance btc h1
nz show yf aapl 2024
```

### Analyze Cached Data
```bash
# Analyze specific cached file
nz show yf aapl --rule PV
nz show binance btc --rule PHLD -d plotly

# With date filtering
nz show yf aapl --show-start 2024-01-01 --show-end 2024-06-01 --rule SR
```

## Advanced Options

### Trading Rules
```bash
# Specific trading rules
--rule PV_HighLow      # PV High/Low analysis
--rule Support_Resistants  # Support/Resistance
--rule Pressure_Vector     # Pressure Vector
--rule Predict_High_Low_Direction  # PHLD
--rule PHLD            # Alias for Predict_High_Low_Direction
--rule PV              # Alias for Pressure_Vector
--rule SR              # Alias for Support_Resistants
--rule OHLCV           # Basic OHLCV data only
--rule AUTO            # Show all available fields
```

### Plotting Backends
```bash
-d fastest      # Fastest for large datasets (default)
-d fast         # Fast plotting
-d plotly       # Interactive Plotly charts
-d mplfinance   # Professional mplfinance charts
-d mpl          # Matplotlib
-d seaborn      # Seaborn statistical plots
-d sb           # Seaborn alias
-d term         # Terminal plotting (for Docker/headless)
```

### Point Size Guidelines
```bash
# Forex majors
--point 0.00001  # EURUSD, GBPUSD, AUDUSD, etc.
--point 0.001    # USDJPY, USDCHF, etc.

# Stocks
--point 0.01     # Most stocks

# Crypto
--point 0.01     # BTC, ETH (high value)
--point 0.001    # Lower value altcoins
--point 0.0001   # Very low value tokens
```

## Error Cases and Troubleshooting

### Common Errors
```bash
# Missing required parameters
nz csv --csv-file data.csv          # Missing --point
nz yf -t EURUSD=X                   # Missing --period or --start/--end
nz polygon --ticker AAPL            # Missing date range and --point

# Correct versions
nz csv --csv-file data.csv --point 0.01
nz yf -t EURUSD=X --period 1mo --point 0.00001
nz polygon --ticker AAPL --interval D1 --start 2024-01-01 --end 2024-12-31 --point 0.01
```

### Cache Management
```bash
# Clear cache and rerun
rm data/cache/csv_converted/*.parquet
rm data/raw_parquet/*.parquet
nz csv --csv-file data.csv --point 0.01

# Specific cache removal
rm data/raw_parquet/yfinance_AAPL_*.parquet
nz yf -t AAPL --period 1mo --point 0.01
```

## Help Commands
```bash
# General help
python run_analysis.py -h
python run_analysis.py --help

# Show version
python run_analysis.py --version

# Show all examples
python run_analysis.py --examples

# Mode-specific help
nz csv --help
nz yf --help
nz show --help
```
