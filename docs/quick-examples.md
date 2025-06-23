# Quick Examples

Fast start examples for common use cases.

## Quick Start

### 1. Demo Analysis
```bash
# Basic demo with default settings
python run_analysis.py demo

# Demo with specific indicator
python run_analysis.py demo --rule RSI

# Demo with interactive plots
python run_analysis.py demo --rule MACD -d plotly
```

### 2. Real Data Analysis
```bash
# Yahoo Finance data
python run_analysis.py yf -t AAPL --period 1mo --point 0.01

# CSV file analysis
python run_analysis.py csv --csv-file data.csv --point 0.01

# Binance cryptocurrency data
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01
```

### 3. Interactive Mode
```bash
# Start interactive mode
python run_analysis.py --interactive

# Interactive mode with alias
nz --interactive
```

## Common Indicators

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

# Stochastic Oscillator
python run_analysis.py demo --rule STOCH
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

## Data Sources

### Yahoo Finance
```bash
# Single symbol
python run_analysis.py yf -t AAPL --period 1mo --point 0.01

# Multiple symbols
python run_analysis.py yf -t AAPL,MSFT,GOOGL --period 1mo --point 0.01

# Different timeframes
python run_analysis.py yf -t AAPL --period 1d --point 0.01
python run_analysis.py yf -t AAPL --period 1w --point 0.01
python run_analysis.py yf -t AAPL --period 1y --point 0.01
```

### CSV Files
```bash
# Basic CSV analysis
python run_analysis.py csv --csv-file data.csv --point 0.01

# With date filtering
python run_analysis.py csv --csv-file data.csv --point 0.01 --start-date 2024-01-01
```

### Binance
```bash
# Cryptocurrency analysis
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01

# Different intervals
python run_analysis.py binance -t BTCUSDT --interval H1 --point 0.01
python run_analysis.py binance -t BTCUSDT --interval M15 --point 0.01
```

### Exchange Rate API
```bash
# Forex analysis
python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001

# Different currency pairs
python run_analysis.py exrate -t GBPUSD --interval D1 --point 0.00001
```

## Visualization Backends

### Interactive Plots
```bash
# Plotly (interactive)
python run_analysis.py demo --rule RSI -d plotly

# Save interactive plots
python run_analysis.py demo --rule RSI -d plotly --save-plot
```

### Static Plots
```bash
# Seaborn (static)
python run_analysis.py demo --rule RSI -d seaborn

# Matplotlib (static)
python run_analysis.py demo --rule RSI -d matplotlib
```

### Text-based Plots
```bash
# Terminal (for SSH/Docker)
python run_analysis.py demo --rule RSI -d term

# Fastest backend
python run_analysis.py demo --rule RSI -d fastest
```

## Export Options

### Multiple Formats
```bash
# Export to all formats
python run_analysis.py demo --rule RSI --export-parquet --export-csv --export-json

# Export with custom filenames
python run_analysis.py demo --rule RSI --export-parquet --output results.parquet
```

## Show Mode

### View Data
```bash
# Show available data
python run_analysis.py show data

# Show available indicators
python run_analysis.py show indicators

# Show calculated indicators
python run_analysis.py show ind
```

## Testing

### Quick Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/calculation/ -v
python -m pytest tests/cli/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## MCP Servers

### Auto-start
```bash
# Start MCP servers
python scripts/auto_start_mcp.py

# Check status
python scripts/auto_start_mcp.py --status

# Stop servers
python scripts/auto_start_mcp.py --stop
```

## Docker

### Quick Docker Commands
```bash
# Build and run
docker compose up --build

# Run demo in container
docker compose run --rm neozork-hld python run_analysis.py demo

# Interactive session
docker compose run --rm neozork-hld bash
```

## EDA (Exploratory Data Analysis)

### Quick EDA
```bash
# Run EDA script
bash eda

# EDA with UV
uv run ./eda
```

## Performance Tips

### Large Datasets
```bash
# Use fastest backend
python run_analysis.py yf -t AAPL --period 5y --point 0.01 -d fastest

# Use terminal backend for SSH/Docker
python run_analysis.py yf -t AAPL --period 1y --point 0.01 -d term
```

### Memory Optimization
```bash
# Use smaller timeframes
python run_analysis.py yf -t AAPL --period 1mo --point 0.01

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
```

### Performance Issues
```bash
# Use fastest backend
python run_analysis.py demo -d fastest

# Clear cache
python scripts/clear_cache.py
```

---

📚 **Additional Resources:**
- **[Usage Examples](usage-examples.md)** - Comprehensive usage examples
- **[Indicator Examples](indicator-examples.md)** - Technical indicator examples
- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Testing Examples](testing-examples.md)** - Testing examples
- **[Script Examples](script-examples.md)** - Utility script examples
- **[Docker Examples](docker-examples.md)** - Docker examples
- **[EDA Examples](eda-examples.md)** - EDA examples 