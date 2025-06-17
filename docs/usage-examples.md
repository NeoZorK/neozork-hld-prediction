# Usage Examples

Common commands and use cases.

## Quick Reference

View all examples:
```bash
python run_analysis.py --examples
```

## Demo Mode

```bash
# Basic demo
python run_analysis.py demo
nz demo

# Specific rules
nz demo --rule PHLD
nz demo --rule PV_HighLow
nz demo --rule SR

# Different plot backends
nz demo -d plotly
nz demo -d seaborn
```

## Real Data Analysis

### Yahoo Finance
```bash
# Single ticker
nz yf -t AAPL --period 1mo --point 0.01

# Multiple timeframes
nz yf -t MSFT --period 3mo --interval 1h

# Show cached data
nz show yf aapl
```

### CSV Files
```bash
# Analyze CSV (MT5 export format)
nz csv --csv-file data/EURUSD_M1.csv --point 0.0001

# With specific rule
nz csv --csv-file data.csv --rule PHLD --point 0.01
```

### Exchange Rate API (Real-time FX)
```bash
# Current EUR/USD rate
nz exrate -t EURUSD --start 2025-01-01 --end 2025-06-01 --point 0.00001

# With indicators
nz exrate -t GBPJPY --start 2025-01-01 --end 2025-06-01 --point 0.01 --rule PV

# Different currency formats
nz exrate -t EUR/USD --start 2025-01-01 --end 2025-06-01 --point 0.00001
nz exrate -t EUR_USD --start 2025-01-01 --end 2025-06-01 --point 0.00001

# Terminal plotting (great for SSH/Docker)
nz exrate -t USDCAD --start 2025-01-01 --end 2025-06-01 --point 0.00001 -d term

# Show cached exchange rate data
nz show exrate
```

**Note:** Exchange Rate API provides current rates only (free plan). Date ranges are ignored.

### Binance Data
```bash
# Cryptocurrency analysis
nz binance -t BTCUSDT --period 1d --point 0.01
```

## Data Management

### Show Data
```bash
# List available data
nz show

# Show specific source
nz show yf
nz show binance
nz show exrate
```

### Cache Management
```bash
# Clear cache
nz clear-cache

# Force refresh
nz yf -t AAPL --period 1mo --force-refresh
```

## EDA and Analysis

```bash
# Run EDA batch processing
python -m src.eda.eda_batch_check

# Generate plots
python -m src.plotting.fastest_auto_plot data/file.parquet

# Data quality checks
python -m src.eda.data_quality
```

## Docker Usage

```bash
# Run in container
docker compose run --rm neozork-hld nz demo

# Interactive session
docker compose run --rm neozork-hld bash
```

For installation: [Getting Started](getting-started.md)  
For analysis tools: [Analysis & EDA](analysis-eda.md)