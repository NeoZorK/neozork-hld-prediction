# Usage Examples

Common commands and use cases.

## Quick Reference

View all examples:
```bash
python run_analysis.py --examples
```

## Interactive Mode

The interactive mode provides a guided interface for selecting indicators and configuring analysis:

```bash
# Start interactive mode
python run_analysis.py --interactive
nz --interactive
```

### Interactive Mode Features

The interactive mode includes the following options:

1. **Select Analysis Mode** - Choose data source (demo, CSV, Yahoo Finance, etc.)
2. **Select Indicator** - Browse and select from available indicators
3. **Configure Data Source** - Set up data source parameters
4. **Configure Plotting** - Choose visualization method
5. **Configure Export** - Select export formats
6. **Show Current Configuration** - Display current settings
7. **Run Analysis** - Execute the analysis with current configuration
8. **Exit** - Exit interactive mode

### Interactive Mode Example

```bash
$ python run_analysis.py --interactive

Welcome to NeoZork HLD Prediction Interactive Mode!

Available options:
1. Select Analysis Mode
2. Select Indicator
3. Configure Data Source
4. Configure Plotting
5. Configure Export
6. Show Current Configuration
7. Run Analysis
8. Exit

Enter your choice (1-8): 1

Available analysis modes:
1. Demo (demo data)
2. Yahoo Finance (yf)
3. CSV (csv files)
4. Binance (binance)
5. Exchange Rate (exrate)

Enter your choice (1-5): 2

Selected: Yahoo Finance
Enter symbol (e.g., AAPL): AAPL
Enter period (e.g., 1mo): 1mo
Enter point value (e.g., 0.01): 0.01

Configuration updated!
```

## Data Source Examples

### Demo Data
```bash
# Basic demo
python run_analysis.py demo

# Demo with specific indicator
python run_analysis.py demo --rule RSI
python run_analysis.py demo --rule MACD
python run_analysis.py demo --rule EMA

# Demo with different backends
python run_analysis.py demo -d plotly
python run_analysis.py demo -d seaborn
python run_analysis.py demo -d term
```

### Yahoo Finance
```bash
# Basic Yahoo Finance
python run_analysis.py yf -t AAPL --period 1mo --point 0.01

# With specific indicators
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule MACD
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule BB

# Different timeframes
python run_analysis.py yf -t AAPL --period 1d --point 0.01 --rule RSI
python run_analysis.py yf -t AAPL --period 1w --point 0.01 --rule RSI
python run_analysis.py yf -t AAPL --period 1y --point 0.01 --rule RSI

# Multiple symbols
python run_analysis.py yf -t AAPL,MSFT,GOOGL --period 1mo --point 0.01 --rule RSI
```

### CSV Files
```bash
# Basic CSV analysis
python run_analysis.py csv --csv-file data.csv --point 0.01

# With specific indicators
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule RSI
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule MACD

# With date filtering
python run_analysis.py csv --csv-file data.csv --point 0.01 --start-date 2024-01-01
python run_analysis.py csv --csv-file data.csv --point 0.01 --end-date 2024-12-31
```

### Binance
```bash
# Basic Binance
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01

# With specific indicators
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule RSI
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule MACD

# Different intervals
python run_analysis.py binance -t BTCUSDT --interval H1 --point 0.01 --rule RSI
python run_analysis.py binance -t BTCUSDT --interval M15 --point 0.01 --rule RSI
```

### Exchange Rate API
```bash
# Basic exchange rate
python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001

# With specific indicators
python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001 --rule RSI
python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001 --rule PV

# Different currency pairs
python run_analysis.py exrate -t GBPUSD --interval D1 --point 0.00001 --rule RSI
python run_analysis.py exrate -t USDJPY --interval D1 --point 0.01 --rule RSI
```

## Technical Indicators

### Trend Indicators
```bash
# EMA (Exponential Moving Average)
python run_analysis.py demo --rule EMA

# ADX (Average Directional Index)
python run_analysis.py demo --rule ADX

# SAR (Parabolic SAR)
python run_analysis.py demo --rule SAR
```

### Oscillators
```bash
# RSI (Relative Strength Index)
python run_analysis.py demo --rule RSI

# Stochastic Oscillator
python run_analysis.py demo --rule STOCH

# CCI (Commodity Channel Index)
python run_analysis.py demo --rule CCI
```

### Momentum Indicators
```bash
# MACD (Moving Average Convergence Divergence)
python run_analysis.py demo --rule MACD
```

### Volatility Indicators
```bash
# ATR (Average True Range)
python run_analysis.py demo --rule ATR

# Bollinger Bands
python run_analysis.py demo --rule BB

# Standard Deviation
python run_analysis.py demo --rule STD
```

### Volume Indicators
```bash
# OBV (On-Balance Volume)
python run_analysis.py demo --rule OBV

# VWAP (Volume Weighted Average Price)
python run_analysis.py demo --rule VWAP
```

### Support/Resistance
```bash
# Donchian Channels
python run_analysis.py demo --rule DONCH

# Fibonacci Retracements
python run_analysis.py demo --rule FIB

# Pivot Points
python run_analysis.py demo --rule PIVOT
```

### Predictive Indicators
```bash
# HMA (Hull Moving Average)
python run_analysis.py demo --rule HMA

# Time Series Forecast
python run_analysis.py demo --rule TSF
```

### Probability Indicators
```bash
# Kelly Criterion
python run_analysis.py demo --rule KELLY

# Monte Carlo Simulation
python run_analysis.py demo --rule MONTE
```

### Sentiment Indicators
```bash
# Commitment of Traders
python run_analysis.py demo --rule COT

# Fear & Greed Index
python run_analysis.py demo --rule FNG

# Social Sentiment
python run_analysis.py demo --rule SENT
```

## Export Options

### Parquet Export
```bash
# Export to Parquet
python run_analysis.py demo --rule RSI --export-parquet

# Export with custom filename
python run_analysis.py demo --rule RSI --export-parquet --output results.parquet
```

### CSV Export
```bash
# Export to CSV
python run_analysis.py demo --rule RSI --export-csv

# Export with custom filename
python run_analysis.py demo --rule RSI --export-csv --output results.csv
```

### JSON Export
```bash
# Export to JSON
python run_analysis.py demo --rule RSI --export-json

# Export with custom filename
python run_analysis.py demo --rule RSI --export-json --output results.json
```

### Multiple Formats
```bash
# Export to multiple formats
python run_analysis.py demo --rule RSI --export-parquet --export-csv --export-json
```

## Visualization Backends

### Plotly (Interactive)
```bash
# Interactive plots with Plotly
python run_analysis.py demo --rule RSI -d plotly

# Save Plotly figures
python run_analysis.py demo --rule RSI -d plotly --save-plot
```

### Seaborn (Static)
```bash
# Static plots with Seaborn
python run_analysis.py demo --rule RSI -d seaborn

# Save Seaborn figures
python run_analysis.py demo --rule RSI -d seaborn --save-plot
```

### Matplotlib (Static)
```bash
# Static plots with Matplotlib
python run_analysis.py demo --rule RSI -d matplotlib

# Save Matplotlib figures
python run_analysis.py demo --rule RSI -d matplotlib --save-plot
```

### Terminal (Text-based)
```bash
# Text-based plots for SSH/Docker
python run_analysis.py demo --rule RSI -d term

# Fastest backend for large datasets
python run_analysis.py demo --rule RSI -d fastest
```

## Advanced Usage

### Multiple Indicators
```bash
# Analyze multiple indicators
python run_analysis.py demo --rule RSI,MACD,EMA

# Compare indicators
python run_analysis.py demo --rule RSI --rule MACD --rule EMA
```

### Custom Parameters
```bash
# Custom RSI period
python run_analysis.py demo --rule RSI --rsi-period 21

# Custom MACD parameters
python run_analysis.py demo --rule MACD --macd-fast 8 --macd-slow 21 --macd-signal 5

# Custom Bollinger Bands
python run_analysis.py demo --rule BB --bb-period 20 --bb-std 2
```

### Data Filtering
```bash
# Filter by date range
python run_analysis.py yf -t AAPL --period 1y --point 0.01 --start-date 2024-01-01 --end-date 2024-06-30

# Filter by volume
python run_analysis.py yf -t AAPL --period 1y --point 0.01 --min-volume 1000000
```

### Performance Optimization
```bash
# Use fastest backend for large datasets
python run_analysis.py yf -t AAPL --period 5y --point 0.01 -d fastest

# Use terminal backend for SSH/Docker
python run_analysis.py yf -t AAPL --period 1y --point 0.01 -d term
```

## Show Mode

### View Available Data
```bash
# Show available data sources
python run_analysis.py show data

# Show available indicators
python run_analysis.py show indicators

# Show available symbols
python run_analysis.py show symbols
```

### View Calculated Indicators
```bash
# Show calculated indicators
python run_analysis.py show ind

# Show indicators from Parquet file
python run_analysis.py show ind parquet

# Show indicators from CSV file
python run_analysis.py show ind csv
```

### View Data Statistics
```bash
# Show data statistics
python run_analysis.py show stats

# Show data statistics for specific file
python run_analysis.py show stats --file data.parquet
```

## Testing and Validation

### Run Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/calculation/ -v
python -m pytest tests/cli/ -v
python -m pytest tests/data/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage Analysis
```bash
# Analyze test coverage
python tests/zzz_analyze_test_coverage.py

# Analyze with verbose output
python tests/zzz_analyze_test_coverage.py --verbose
```

### MCP Server Testing
```bash
# Test stdio mode
python tests/test_stdio.py

# Test MCP functionality
python -m pytest tests/mcp/ -v
```

## MCP Server Integration

### Auto-start MCP Servers
```bash
# Start MCP servers
python scripts/auto_start_mcp.py

# Start with configuration
python scripts/auto_start_mcp.py --config mcp_auto_config.json

# Start in debug mode
python scripts/auto_start_mcp.py --debug

# Show server status
python scripts/auto_start_mcp.py --status

# Stop servers
python scripts/auto_start_mcp.py --stop
```

### Manual MCP Server Management
```bash
# Start PyCharm GitHub Copilot MCP server
python pycharm_github_copilot_mcp.py

# Start with stdio mode for testing
python pycharm_github_copilot_mcp.py --stdio

# Start with debug logging
python pycharm_github_copilot_mcp.py --debug
```

## Utility Scripts

### Fix Imports
```bash
# Fix imports automatically
python scripts/fix_imports.py

# Fix with verbose output
python scripts/fix_imports.py --verbose

# Fix specific file
python scripts/fix_imports.py --file src/calculation/indicators/rsi_ind.py
```

### Debug Scripts
```bash
# Debug Binance connection
python scripts/debug_scripts/debug_binance_connection.py

# Check Parquet files
python scripts/debug_scripts/debug_check_parquet.py

# Debug indicators
python scripts/debug_scripts/debug_indicators.py

# Debug CLI
python scripts/debug_scripts/debug_cli.py
```

### Data Management
```bash
# Create test Parquet file
python scripts/create_test_parquet.py

# Recreate CSV from Parquet
python scripts/recreate_csv.py

# Analyze requirements
python scripts/analyze_requirements.py
```

## Docker Usage

### Basic Docker Commands
```bash
# Build and run container
docker compose up --build

# Run demo in container
docker compose run --rm neozork-hld python run_analysis.py demo

# Interactive session in container
docker compose run --rm neozork-hld bash

# Run tests in container
docker compose run --rm neozork-hld python -m pytest tests/
```

### Docker with Data Mounting
```bash
# Mount data directory
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld python run_analysis.py csv --csv-file data.csv

# Mount results directory
docker compose run --rm -v $(pwd)/results:/app/results neozork-hld python run_analysis.py demo --export-parquet
```

## EDA (Exploratory Data Analysis)

### Basic EDA
```bash
# Run EDA script
bash eda

# EDA with UV
uv run ./eda

# EDA with verbose output
bash eda --verbose

# EDA with export
bash eda --export-results
```

### EDA in Docker
```bash
# Run EDA in container
docker compose run --rm neozork-hld bash eda

# EDA with UV in container
docker compose run --rm neozork-hld uv run ./eda
```

## Workflow Examples

### Complete Analysis Pipeline
```bash
# 1. Load data
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 2. Calculate indicators
python run_analysis.py show yf AAPL --rule RSI --export-parquet
python run_analysis.py show yf AAPL --rule MACD --export-parquet

# 3. View results
python run_analysis.py show ind parquet

# 4. Run tests
python -m pytest tests/ --cov=src --cov-report=html

# 5. Analyze coverage
python tests/zzz_analyze_test_coverage.py
```

### Development Workflow
```bash
# 1. Fix imports
python scripts/fix_imports.py

# 2. Create test data
python scripts/create_test_parquet.py

# 3. Run tests
python -m pytest tests/ -v

# 4. Analyze coverage
python tests/zzz_analyze_test_coverage.py

# 5. Start MCP servers
python scripts/auto_start_mcp.py
```

### Debugging Workflow
```bash
# 1. Check data
python scripts/debug_scripts/debug_check_parquet.py

# 2. Check connections
python scripts/debug_scripts/debug_binance_connection.py

# 3. Debug indicators
python scripts/debug_scripts/debug_indicators.py

# 4. Debug CLI
python scripts/debug_scripts/debug_cli.py

# 5. Debug MCP servers
python scripts/debug_scripts/debug_mcp_servers.py
```

## Performance Tips

### Large Datasets
```bash
# Use fastest backend
python run_analysis.py yf -t AAPL --period 5y --point 0.01 -d fastest

# Use terminal backend for SSH/Docker
python run_analysis.py yf -t AAPL --period 1y --point 0.01 -d term

# Filter data to reduce size
python run_analysis.py yf -t AAPL --period 1y --point 0.01 --start-date 2024-01-01
```

### Memory Optimization
```bash
# Use smaller timeframes
python run_analysis.py yf -t AAPL --period 1mo --point 0.01

# Use fewer indicators
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI

# Export results to free memory
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI --export-parquet
```

## Troubleshooting

### Common Issues
```bash
# Check data quality
python scripts/debug_scripts/debug_check_parquet.py

# Check connections
python scripts/debug_scripts/debug_binance_connection.py

# Check indicators
python scripts/debug_scripts/debug_indicators.py

# Check CLI
python scripts/debug_scripts/debug_cli.py

# Check MCP servers
python scripts/debug_scripts/debug_mcp_servers.py
```

### Performance Issues
```bash
# Use fastest backend
python run_analysis.py demo -d fastest

# Clear cache
python scripts/clear_cache.py

# Check system resources
python scripts/debug_scripts/debug_system_resources.py
```

### Docker Issues
```bash
# Rebuild container
docker compose build --no-cache

# Check container logs
docker compose logs neozork-hld

# Interactive debugging
docker compose run --rm neozork-hld bash
```

---

📚 **Additional Resources:**
- **[Quick Examples](quick-examples.md)** - Fast start examples
- **[Indicator Examples](indicator-examples.md)** - Technical indicator examples
- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Testing Examples](testing-examples.md)** - Testing examples
- **[Script Examples](script-examples.md)** - Utility script examples
- **[Docker Examples](docker-examples.md)** - Docker examples
- **[EDA Examples](eda-examples.md)** - EDA examples