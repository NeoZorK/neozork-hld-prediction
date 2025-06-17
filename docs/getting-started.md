# Getting Started

## Overview

NeoZork HLD Prediction enhances a proprietary trading indicator using Machine Learning techniques. The project focuses on:

- **Indicator Replication:** Python implementation of MQL5 HLD indicator
- **ML Enhancement:** Improved predictions using OHLCV data and ML models
- **Multiple Data Sources:** Demo data, CSV files, Yahoo Finance, Polygon.io, Binance
- **Validation:** Rigorous time-series validation and performance evaluation

## Quick Setup

```bash
# Clone repository
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction

# Install dependencies
pip install -r requirements.txt
# or use UV: uv sync

# Run demo
python run_analysis.py demo
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

# CSV file analysis
python run_analysis.py csv --csv-file data/your_file.csv --point 0.01

# Show cached data
python run_analysis.py show yf aapl
```

### Using Docker
```bash
# Build and run
docker compose up --build

# Interactive mode
docker compose run --rm neozork-hld bash
```

## Key Features

- **Core Calculations:** Pressure Vector, Support/Resistance, HLD Direction
- **Data Validation:** Compare Python vs MQL5 results
- **EDA Tools:** Comprehensive data analysis and quality checks
- **Plotting:** Multiple visualization options (matplotlib, plotly, seaborn)
- **CI/CD:** Automated testing and Docker builds

## Next Steps

1. **Installation:** [Full Installation Guide](installation.md)
2. **Usage Examples:** [Usage Examples](usage-examples.md) 
3. **Docker:** [Docker Setup](docker.md)
4. **Analysis Tools:** [Analysis & EDA](analysis-eda.md)
5. **API Setup:** Configure API keys for live data sources

For comprehensive documentation: [Documentation Index](index.md)
