# Quick Start Guide

Get up and running with NeoZork HLD Prediction in minutes.

## 1. Initial Setup

```bash
# Clone and enter directory
git clone <repository_url>
cd neozork-hld-prediction

# Create directories and environment
./scripts/init_dirs.sh

# Install dependencies
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. First Analysis

### Demo Mode (No setup required)
```bash
# Basic demo
python run_analysis.py demo

# Demo with specific rule
python run_analysis.py demo --rule PHLD

# Demo with different plotting
python run_analysis.py demo --rule PV -d plotly
```

### Using the `nz` Shortcut
```bash
# Equivalent to above commands
nz demo
nz demo --rule PHLD
nz demo --rule PV -d plotly
```

## 3. Real Data Analysis

### Yahoo Finance (Free)
```bash
# Forex analysis
nz yf -t EURUSD=X --period 1mo --point 0.00001

# Stock analysis
nz yf -t AAPL --period 6mo --point 0.01

# Crypto analysis
nz yf -t BTC-USD --start 2024-01-01 --end 2024-12-31 --point 0.01
```

### CSV Files
```bash
# Analyze MT5 exported data
nz csv --csv-file data/your_file.csv --point 0.01 --rule PHLD
```

## 4. Explore Your Data

### Show Cached Data
```bash
# List all cached files
nz show

# Find specific data
nz show yf aapl
nz show binance btc
```

### Data Quality Checks
```bash
# Check for data issues
python src/eda/eda_batch_check.py --data-quality-checks

# Fix common issues
python src/eda/eda_batch_check.py --fix-files --fix-all
```

## 5. Available Rules

| Rule | Description |
|------|-------------|
| `PHLD` | Predict High Low Direction |
| `PV` | Pressure Vector |
| `SR` | Support Resistance |
| `PV_HighLow` | PV High/Low analysis |
| `OHLCV` | Basic OHLCV data only |
| `AUTO` | Show all available fields |

## 6. Plotting Options

| Backend | Command | Best For |
|---------|---------|----------|
| `fastest` | `-d fastest` | Large datasets (default) |
| `fast` | `-d fast` | Quick visualization |
| `plotly` | `-d plotly` | Interactive plots |
| `mplfinance` | `-d mplfinance` | Professional charts |
| `seaborn` | `-d seaborn` | Statistical plots |
| `term` | `-d term` | Terminal/Docker |

## 7. Common Workflows

### Quick Analysis
```bash
# Fast analysis with plotting
nz demo --rule PHLD -d plotly
```

### Comprehensive Analysis
```bash
# Fetch data, analyze, and save
nz yf -t EURUSD=X --period 3mo --point 0.00001 --rule PHLD -d mplfinance

# Check data quality
python src/eda/eda_batch_check.py --basic-stats --correlation-analysis

# Run tests
python -m pytest tests/ -v
```

### Docker Workflow
```bash
# Build and run in container
docker compose build
docker compose up

# Interactive container
docker compose run --rm neozork-hld
```

## Next Steps

- 📚 Read [Usage Examples](usage-examples.md) for comprehensive command reference
- 🐳 Set up [Docker](docker.md) for isolated environment
- 🔧 Explore [Scripts](scripts.md) for automation tools
- 📊 Use [EDA Tools](eda-tools.md) for data analysis

## Getting Help

```bash
# Show all commands
python run_analysis.py --help

# Show usage examples
python run_analysis.py --examples

# List available scripts
ls scripts/
```
