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

## Export Flags Usage

Export flags (`--export-parquet`, `--export-csv`, `--export-json`) are only allowed in `demo` mode. They are forbidden in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, and `exrate` modes.

### Testimonial: How to Export and View Indicators

1. **Download or Convert Data**
   - Download data using yfinance:
     ```bash
     python run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01
     ```
   - Or convert your CSV:
     ```bash
     python run_analysis.py csv --csv-file data.csv --point 0.01
     ```
2. **Apply Indicator and Export**
   - Use `show` mode with a rule and export flags:
     ```bash
     python run_analysis.py show yfinance AAPL --rule PHLD --export-parquet --export-csv --export-json
     ```
3. **View Exported Indicator Files**
   - Use `show ind` to view the exported indicators:
     ```bash
     python run_analysis.py show ind parquet
     python run_analysis.py show ind csv
     python run_analysis.py show ind json
     ```
   - Parquet files will show charts, CSV/JSON will show tabular data with indicators.

> Note: Export flags are not allowed in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, or `exrate` modes. Use `demo` mode for direct export, or use the workflow above for real data.