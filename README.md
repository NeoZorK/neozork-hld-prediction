# NeoZork HLD Prediction

Machine Learning enhancement of proprietary trading indicators using Python with intelligent AI assistance.

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction
pip install -e .

# Run demo
python run_analysis.py demo

# Explore trading metrics encyclopedia
python run_analysis.py --metric

# Start interactive mode
python run_analysis.py --interactive

# Get current EUR/USD rate with Pressure Vector indicator
python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001 --rule PV
```

## 🐳 Docker Quick Start

```bash
# Build and run with UV package manager (recommended)
docker compose build --build-arg USE_UV=true && docker compose run --rm neozork-hld

# Or build with pip package manager
docker compose build --build-arg USE_UV=false && docker compose run --rm neozork-hld

# View generated plots
# Check ./results/plots/ directory on your host system
```

📚 **[Docker Setup Guide](docs/deployment/docker-setup.md)**

## ✨ Features

- **Indicator Replication:** Python implementation of MQL5 HLD indicator
- **ML Enhancement:** Improved predictions using OHLCV data
- **Multiple Data Sources:** Yahoo Finance, Polygon.io, Binance, Exchange Rate API, CSV files
- **Indicator Export:** Export calculated indicators to Parquet, CSV, and JSON formats
- **Real-time FX Data:** Current exchange rates from 160+ currencies
- **Analysis Tools:** Comprehensive EDA and plotting capabilities
- **Trading Metrics Encyclopedia:** Comprehensive guide to quantitative trading metrics and strategy tips
- **Interactive Mode:** Guided setup and analysis with built-in metrics encyclopedia
- **Docker Support:** Containerized development environment
- **AI-Powered Development:** MCP servers with GitHub Copilot integration

## 🤖 MCP Servers

Intelligent development assistance with Model Context Protocol (MCP) servers:

### PyCharm GitHub Copilot MCP Server
- **Smart Autocompletion:** Financial symbols, timeframes, technical indicators
- **Context-Aware Suggestions:** AI-powered code completion based on project context
- **GitHub Copilot Integration:** Enhanced AI assistance for financial analysis

### Auto-Start MCP Server
- **Intelligent Detection:** Automatically detects running IDEs (PyCharm, Cursor, VS Code)
- **Condition-Based Startup:** Starts servers based on project conditions
- **Health Monitoring:** Continuous monitoring and automatic restart on failures

**Quick Setup:**
```bash
# Test MCP servers
python scripts/check_mcp_status.py

# Manual server start
python neozork_mcp_server.py
```

📚 **[MCP Servers Documentation](docs/reference/mcp-servers/README.md)**

## 📚 Documentation

📚 **[Complete Documentation](docs/index.md)**

### Documentation Categories

#### 🚀 [Getting Started](docs/getting-started/)
- [Installation & Setup](docs/getting-started/getting-started.md)
- [Project Structure](docs/getting-started/project-structure.md)
- [UV Setup](docs/getting-started/uv-setup.md)

#### 💡 [Examples](docs/examples/)
- [Quick Examples](docs/examples/quick-examples.md) - Fast start examples
- [Usage Examples](docs/examples/usage-examples.md) - Comprehensive workflows
- [Indicator Examples](docs/examples/indicator-examples.md) - Technical analysis
- [MCP Examples](docs/examples/mcp-examples.md) - AI integration
- [Testing Examples](docs/examples/testing-examples.md) - Test coverage
- [Script Examples](docs/examples/script-examples.md) - Utilities and debugging
- [Docker Examples](docs/examples/docker-examples.md) - Containerized deployment
- [EDA Examples](docs/examples/eda-examples.md) - Data analysis

#### 📖 [Guides](docs/guides/)
- [Scripts Guide](docs/guides/scripts.md) - Automation tools
- [Testing Guide](docs/guides/testing.md) - Test framework
- [Docker Guide](docs/guides/docker.md) - Containerized development
- [Analysis & EDA Guide](docs/guides/analysis-eda.md) - Data analysis tools
- [Debug Scripts](docs/guides/debug-scripts.md) - Troubleshooting
- [Utility Scripts](docs/guides/utility-scripts.md) - Data conversion utilities
- [Indicator Export](docs/guides/indicator-export.md) - Export calculated indicators
- [Copilot Instructions](docs/guides/copilot-instructions.md) - AI assistance setup

#### 📋 [Reference](docs/reference/)
- [Technical Indicators](docs/reference/indicators/) - Complete indicator reference
- [MCP Servers](docs/reference/mcp-servers/) - Server documentation

#### 🔧 [Development](docs/development/)
- [CI/CD Guide](docs/development/ci-cd.md) - GitHub Actions and deployment

#### 🌐 [API](docs/api/)
- [Exchange Rate API](docs/api/exchange-rate-api-complete.md) - Real-time FX data

### Quick Navigation by User Type

#### 👶 **For Beginners**
1. [Getting Started](docs/getting-started/)
2. [Quick Examples](docs/examples/quick-examples.md)
3. [Examples Overview](docs/examples/examples-overview.md)

#### 👨‍💻 **For Developers**
1. [Getting Started](docs/getting-started/)
2. [Testing Examples](docs/examples/testing-examples.md)
3. [Script Examples](docs/examples/script-examples.md)
4. [MCP Examples](docs/examples/mcp-examples.md)
5. [Development](docs/development/) guides

#### 📊 **For Analysts**
1. [Getting Started](docs/getting-started/)
2. [Indicator Examples](docs/examples/indicator-examples.md)
3. [EDA Examples](docs/examples/eda-examples.md)
4. [Reference](docs/reference/) for technical details

#### 🐳 **For DevOps**
1. [Docker Examples](docs/examples/docker-examples.md)
2. [Testing Examples](docs/examples/testing-examples.md)
3. [Development](docs/development/) CI/CD guides

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Test MCP servers specifically
pytest tests/mcp/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 📋 Requirements

- Python 3.12+
- Docker (optional)
- API keys for live data (optional)
- MCP plugin for your IDE (optional)

## 🔧 IDE Setup

### PyCharm
1. Install MCP plugin from Settings → Plugins
2. Configure MCP server in Settings → Languages & Frameworks → MCP Servers
3. Enable GitHub Copilot for enhanced AI assistance

### Cursor
1. Open Settings (Cmd/Ctrl + ,)
2. Add MCP server configuration in AI Assistant section
3. Restart Cursor for changes to take effect

### VS Code
1. Install MCP Extension
2. Configure in settings.json
3. Enable GitHub Copilot extension

## 📊 Performance

| Feature | Performance |
|---------|-------------|
| MCP Server Startup | < 3s |
| Autocompletion Response | 5-15ms |
| File Indexing | 50ms/file |
| Memory Usage | 25-50MB |

## 🐛 Troubleshooting

### MCP Server Issues
```bash
# Check server status
python scripts/check_mcp_status.py

# Enable debug mode
export LOG_LEVEL=DEBUG
python neozork_mcp_server.py

# Check dependencies
pip list | grep -E "(watchdog|psutil)"
```

### General Issues
- Ensure Python 3.12+ is installed
- Check all dependencies are installed: `pip install -e .`
- Verify API keys for live data sources
- Check logs in `logs/` directory

## 📄 License

[Add your license here]

## 📝 Export Flags Usage

Export flags (`--export-parquet`, `--export-csv`, `--export-json`) are only allowed in `demo` mode. They are forbidden in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, and `exrate` modes.

### How to Export and View Indicators

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `pytest tests/ -v`
6. Submit a pull request

## 📞 Support

- Create an issue on GitHub
- Check the troubleshooting section
- Review the [Examples](docs/examples/) section for common use cases
- Review the [Guides](docs/guides/) for detailed tutorials
- Consult the [Reference](docs/reference/) for technical details
- Contact the development team