# NeoZork HLD Prediction

Machine Learning enhancement of proprietary trading indicators using Python.

## Quick Start

```bash
# Clone and install
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction
pip install -r requirements.txt

# Run demo
python run_analysis.py demo

# Get current EUR/USD rate with Pressure Vector indicator
python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001 --rule PV

# Docker alternative
docker compose up --build
```

## Features

- **Indicator Replication:** Python implementation of MQL5 HLD indicator
- **ML Enhancement:** Improved predictions using OHLCV data
- **Multiple Data Sources:** Yahoo Finance, Polygon.io, Binance, Exchange Rate API, CSV files
- **Indicator Export:** Export calculated indicators to Parquet, CSV, and JSON formats
- **Real-time FX Data:** Current exchange rates from 160+ currencies
- **Analysis Tools:** Comprehensive EDA and plotting capabilities
- **Docker Support:** Containerized development environment

## Documentation

📚 **[Complete Documentation](docs/index.md)**

### Quick Links

- [Getting Started](docs/getting-started.md) - Overview and setup
- [Usage Examples](docs/usage-examples.md) - Common commands
- [Indicator Export](docs/indicator-export.md) - Export calculated indicators
- [Exchange Rate API](docs/exchange-rate-api-complete.md) - Real-time FX data
- [Docker Setup](docs/docker.md) - Containerized development
- [Analysis Tools](docs/analysis-eda.md) - EDA and plotting

### Development
- [Testing](docs/testing.md) - Test framework
- [CI/CD](docs/ci-cd.md) - GitHub Actions
- [Scripts](docs/scripts.md) - Automation tools
- [Project Structure](docs/project-structure.md) - Code organization

## Requirements

- Python 3.12+
- Docker (optional)
- API keys for live data (optional)

## License

[Add your license here]