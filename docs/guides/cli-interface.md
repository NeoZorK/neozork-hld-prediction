# CLI Interface Guide

Complete guide to the command-line interface for the Neozork HLD Prediction project.

## Overview

The CLI interface provides a powerful command-line tool for data analysis, indicator calculations, and automated workflows with UV package management support.

## Main CLI Entry Point

### `run_analysis.py`

The main entry point for all CLI operations.

```bash
# Traditional Python
python run_analysis.py [mode] [options]

# With UV (recommended)
uv run run_analysis.py [mode] [options]
```

## Available Modes

### 1. Demo Mode

Run analysis with demo data for testing and demonstration.

```bash
# Basic demo
uv run run_analysis.py demo

# Demo with specific rule
uv run run_analysis.py demo --rule RSI

# Demo with custom plotting backend
uv run run_analysis.py demo --rule PV -d plotly
```

#### Demo Mode Options
- **`--rule`** - Trading rule to apply (RSI, MACD, PHLD, PV, SR, OBV, VWAP, SuperTrend, COT, Put/Call Ratio)
- **`-d`** - Drawing backend (fastest, plotly, mpl, seaborn, term)
- **`--export-parquet`** - Export results to Parquet format
- **`--export-csv`** - Export results to CSV format
- **`--export-json`** - Export results to JSON format

### 2. Yahoo Finance Mode

Fetch and analyze data from Yahoo Finance.

```bash
# Stock analysis
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule RSI

# Forex analysis
uv run run_analysis.py yfinance --ticker EURUSD=X --period 6mo --point 0.00001 --rule MACD

# Multiple indicators
uv run run_analysis.py yfinance --ticker GOOGL --period 1y --point 0.01 --rule PHLD,PV,SR
```

#### Yahoo Finance Options
- **`--ticker`** - Stock/forex symbol (required)
- **`--period`** - Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- **`--point`** - Price precision (required)
- **`--rule`** - Trading rule(s) to apply
- **`--interval`** - Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo, 3mo)

### 3. Binance Mode

Analyze cryptocurrency data from Binance.

```bash
# BTC/USDT analysis
uv run run_analysis.py binance --symbol BTCUSDT --interval 1h --point 0.01 --rule RSI

# Multiple timeframes
uv run run_analysis.py binance --symbol ETHUSDT --interval 4h --point 0.01 --rule MACD,PHLD
```

#### Binance Options
- **`--symbol`** - Trading pair (required)
- **`--interval`** - Time interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
- **`--point`** - Price precision (required)
- **`--rule`** - Trading rule(s) to apply
- **`--limit`** - Number of data points (max 1000)

### 4. CSV Mode

Analyze local CSV files.

```bash
# Basic CSV analysis
uv run run_analysis.py csv --csv-file data/my_data.csv --point 0.01 --rule RSI

# Custom column mapping
uv run run_analysis.py csv --csv-file data/custom.csv --point 0.01 --rule MACD \
    --date-col timestamp --price-cols open,high,low,close --volume-col volume
```

#### CSV Options
- **`--csv-file`** - Path to CSV file (required for single file processing)
- **`--csv-folder`** - Path to folder containing CSV files (required for batch processing)
- **`--point`** - Price precision (required for single file, defaults to 0.00001 for folder)
- **`--rule`** - Trading rule(s) to apply
- **`--date-col`** - Column name for timestamps
- **`--price-cols`** - Comma-separated OHLC column names
- **`--volume-col`** - Column name for volume data

### 4b. CSV Folder Mode ⭐ **NEW**

Process all CSV files in a folder with progress bars and ETA.

```bash
# Process all CSV files in folder
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001

# Process folder with specific rule
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --rule RSI

# Process folder with fastest backend
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 -d fastest

# Process folder with export
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --export-parquet
```

#### CSV Folder Features
- **Batch processing** - Process all CSV files in a folder
- **Progress bars** - Two-level progress tracking (overall + per file)
- **ETA calculation** - Estimated time remaining
- **File information** - Size and processing time per file
- **Error handling** - Continue processing even if some files fail
- **Default point value** - Automatically uses 0.00001 for folder processing

### 5. Exchange Rate Mode

Analyze forex data from Exchange Rate API.

```bash
# EUR/USD analysis
uv run run_analysis.py exrate --ticker EURUSD --interval D1 --point 0.00001 --rule PV

# Multiple currency pairs
uv run run_analysis.py exrate --ticker GBPUSD,USDJPY --interval D1 --point 0.00001 --rule SR
```

#### Exchange Rate Options
- **`--ticker`** - Currency pair(s) (required)
- **`--interval`** - Time interval (D1, W1, M1)
- **`--point`** - Price precision (required)
- **`--rule`** - Trading rule(s) to apply

### 6. Show Mode ⭐ **ENHANCED**

Display and analyze existing data with enhanced volume indicator support.

```bash
# Show available indicators
uv run run_analysis.py show ind

# Show specific indicator data
uv run run_analysis.py show ind parquet
uv run run_analysis.py show ind csv
uv run run_analysis.py show ind json

# Show with analysis
uv run run_analysis.py show yfinance AAPL --rule PHLD --export-parquet

# Volume indicators (FIXED)
uv run run_analysis.py show csv mn1 -d fastest --rule obv:
uv run run_analysis.py show csv mn1 -d fastest --rule vwap:20

# New sentiment indicators
uv run run_analysis.py show csv mn1 -d fastest --rule cot:14,close
uv run run_analysis.py show csv mn1 -d fastest --rule putcallratio:20,close

# New trend indicators
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0,open
```

#### Show Mode Options
- **`ind`** - Show indicator data
- **`yfinance`** - Show Yahoo Finance data with analysis
- **`csv`** - Show CSV data with analysis
- **`polygon`** - Show Polygon data with analysis
- **`binance`** - Show Binance data with analysis
- **`exrate`** - Show Exchange Rate data with analysis

### 7. Interactive Mode

Guided interactive analysis session.

```bash
# Start interactive session
uv run run_analysis.py interactive

# Interactive with preset options
uv run run_analysis.py interactive --preset stock_analysis
```

#### Interactive Mode Features
- **Guided setup** - Step-by-step configuration
- **Data source selection** - Choose from available sources
- **Indicator selection** - Select technical indicators
- **Parameter configuration** - Set indicator parameters
- **Analysis execution** - Run analysis with selected options

## Trading Rules

### Available Rules

#### Core Indicators
1. **RSI** - Relative Strength Index
2. **MACD** - Moving Average Convergence Divergence
3. **PHLD** - Price High Low Direction
4. **PV** - Pressure Vector
5. **SR** - Support Resistance

#### Volume Indicators ⭐ **FIXED**
6. **OBV** - On-Balance Volume (fixed dual chart plotting)
7. **VWAP** - Volume Weighted Average Price

#### New Trend Indicators ⭐ **NEW**
8. **SuperTrend** - Advanced trend-following indicator

#### New Sentiment Indicators ⭐ **NEW**
9. **COT** - Commitments of Traders
10. **Put/Call Ratio** - Options sentiment indicator

#### New Trend Indicators ⭐ **NEW**
11. **SMA** - Simple Moving Average (complete tutorial available)
12. **SuperTrend** - Advanced trend-following indicator
13. **Wave** - Advanced dual-system indicator with 10 trading rules

### Rule Combinations

```bash
# Single rule
uv run run_analysis.py demo --rule RSI

# Multiple rules
uv run run_analysis.py demo --rule RSI,MACD,PHLD

# Volume indicators (now working)
uv run run_analysis.py demo --rule OBV,VWAP

# All rules
uv run run_analysis.py demo --rule ALL
```

## Export Options

### Export Formats

- **Parquet** - High-performance columnar format
- **CSV** - Comma-separated values
- **JSON** - JavaScript Object Notation

### Export Usage

```bash
# Export to multiple formats
uv run run_analysis.py demo --rule PHLD --export-parquet --export-csv --export-json

# Export with custom filename
uv run run_analysis.py yfinance AAPL --rule RSI --export-csv --output-file my_analysis.csv
```

## 🐛 Recent Fixes & Improvements

### Volume Indicators Fix ⭐ **FIXED**
**Issue:** OBV indicator had dual chart plotting errors and parameter parsing issues.

**Fix:** 
- Fixed parameter parsing for `--rule obv:` (empty parameters after colon)
- Fixed volume column handling for volume-based indicators
- Fixed dual chart plotting for OBV with proper argument passing

**Before:**
```bash
# This would fail with parameter parsing error
uv run run_analysis.py show csv mn1 -d fastest --rule obv:
```

**After:**
```bash
# This now works perfectly
uv run run_analysis.py show csv mn1 -d fastest --rule obv:
```

### UV Integration
- **Exclusive UV Usage**: All commands now use UV for consistency
- **Multithreaded Testing**: `uv run pytest tests -n auto`
- **Docker Integration**: Seamless UV in containers
- **Native Container Support**: Full UV support in Apple Silicon containers

## Performance Optimization

### UV Package Management
```bash
# Fast dependency installation
uv pip install -r requirements.txt

# Fast test execution (multithreaded)
uv run pytest tests -n auto

# Fast analysis execution
uv run run_analysis.py demo --rule PHLD
```

### Docker Environment
```bash
# UV commands in Docker
docker-compose exec neozork uv-install
docker-compose exec neozork uv run run_analysis.py demo --rule PHLD
docker-compose exec neozork uv run pytest tests -n auto
```

## Environment-Specific Usage

### Local Development
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup environment
uv pip install -r requirements.txt

# Run analysis
uv run run_analysis.py demo --rule PHLD

# Run tests
uv run pytest tests -n auto
```

### Docker Environment
```bash
# Start container
docker-compose up -d

# Run analysis
docker-compose exec neozork uv run run_analysis.py demo --rule PHLD

# Run tests
docker-compose exec neozork uv run pytest tests -n auto
```

### Native Container (Apple Silicon)
```bash
# Setup and run
./scripts/native-container/setup.sh
./scripts/native-container/run.sh

# Access shell
./scripts/native-container/exec.sh --shell

# Run analysis
nz demo --rule PHLD
uv run run_analysis.py show csv mn1 -d fastest --rule obv:
```

## Troubleshooting

### Common Issues

#### UV Not Found
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

#### Volume Indicator Errors
```bash
# Ensure data has Volume column
uv run run_analysis.py show csv mn1 -d fastest --rule obv:

# Check data structure
python -c "import pandas as pd; df = pd.read_parquet('data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet'); print(df.columns.tolist())"
```

#### Docker UV Issues
```bash
# Check UV status in container
docker-compose exec neozork python scripts/check_uv_mode.py --verbose

# Reinstall UV in container
docker-compose exec neozork uv-install
```

## Advanced Usage

### Custom Indicator Parameters
```bash
# OBV with custom parameters
uv run run_analysis.py show csv mn1 -d fastest --rule obv:20,close

# SuperTrend with custom parameters
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0,open

# COT with custom parameters
uv run run_analysis.py show csv mn1 -d fastest --rule cot:14,close
```

### Batch Processing
```bash
# Process multiple symbols
for symbol in AAPL GOOGL MSFT; do
    uv run run_analysis.py yfinance --ticker $symbol --rule PHLD --export-csv
done

# Process multiple timeframes
for interval in 1h 4h 1d; do
    uv run run_analysis.py binance --symbol BTCUSDT --interval $interval --rule RSI
done
```

### Integration with Scripts
```bash
#!/bin/bash
# analysis_script.sh

# Run analysis with UV
uv run run_analysis.py demo --rule PHLD --export-csv

# Process results
python scripts/process_results.py

# Generate report
uv run python scripts/generate_report.py
```