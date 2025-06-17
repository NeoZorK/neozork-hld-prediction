# Getting Started

## Overview

NeoZork HLD Prediction enhances a proprietary trading indicator using Machine Learning techniques. The project focuses on:

- **Indicator Replication:** Python implementation of MQL5 HLD indicator
- **ML Enhancement:** Improved predictions using OHLCV data and ML models
- **Multiple Data Sources:** Demo data, CSV files, Yahoo Finance, Polygon.io, Binance, Exchange Rate API
- **Real-time FX Data:** Current exchange rates from 160+ currencies
- **Validation:** Rigorous time-series validation and performance evaluation

## Prerequisites

- **Python 3.12+**
- **Git**
- **Docker** (optional, for containerized usage)

## Installation

### Quick Install

```bash
# Clone repository
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction

# Install with UV (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Or install with pip
pip install -r requirements.txt
```

### API Keys (Optional)

For data fetching, set environment variables: (.env file or directly in your shell)

```bash
export POLYGON_API_KEY="your_key_here"
export BINANCE_API_KEY="your_key_here"
export BINANCE_API_SECRET="your_secret_here"
export EXCHANGE_RATE_API_KEY="your_key_here"  # Get free key from exchangerate-api.com
```

## Basic Usage

### Demo Mode
```bash
# Basic demo
python run_analysis.py demo

# Demo with specific rule
python run_analysis.py demo --rule PHLD
```

### Real Data Analysis
```bash
# Yahoo Finance data
python run_analysis.py yf -t AAPL --period 1mo --point 0.01

# Current exchange rates (Exchange Rate API)
python run_analysis.py exrate -t EURUSD --start 2025-01-01 --end 2025-06-01 --point 0.00001

# CSV file analysis
python run_analysis.py csv --csv-file data/your_file.csv --point 0.01

# Show cached data
python run_analysis.py show yf aapl
python run_analysis.py show exrate

# Faster with UV
uv run run_analysis.py demo -d term —rule PHLD
```

### Using Docker
```bash
# Build and run
docker compose up --build

# Build with uv
docker compose build --build-arg USE_UV=true 

# Interactive mode
docker compose run --rm neozork-hld bash

#Run Docker with uv
uv run ./nz demo
```


### EDA and Analysis
```bash
# Run EDA
python -m src.eda.eda_batch_check

#Run EDA script in Docker with uv
uv run ./eda -h

# Generate plots
python -m src.plotting.fastest_auto_plot data/file.parquet
```

## Troubleshooting

**ImportError issues:**
```bash
pip install --upgrade -r requirements.txt
```

**Permission errors:**
```bash
chmod +x scripts/*.sh
```

**Docker issues:**
```bash
docker compose build --no-cache
```

## Key Features

- **Core Calculations:** Pressure Vector, Support/Resistance, HLD Direction
- **Data Validation:** Compare Python vs MQL5 results
- **EDA Tools:** Comprehensive data analysis and quality checks
- **Plotting:** Multiple visualization options (matplotlib, plotly, seaborn)
- **CI/CD:** Automated testing and Docker builds

## Next Steps

1. **Usage Examples:** [Usage Examples](usage-examples.md) 
2. **Docker:** [Docker Setup](docker.md)
3. **Analysis Tools:** [Analysis & EDA](analysis-eda.md)
4. **Scripts:** [Scripts Guide](scripts.md)
5. **Testing:** [Testing Guide](testing.md)

For comprehensive documentation: [Documentation Index](index.md)
