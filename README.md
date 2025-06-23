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

# Get current EUR/USD rate with Pressure Vector indicator
python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001 --rule PV

# Docker alternative
docker compose up --build
```

## ✨ Features

- **Indicator Replication:** Python implementation of MQL5 HLD indicator
- **ML Enhancement:** Improved predictions using OHLCV data
- **Multiple Data Sources:** Yahoo Finance, Polygon.io, Binance, Exchange Rate API, CSV files
- **Indicator Export:** Export calculated indicators to Parquet, CSV, and JSON formats
- **Real-time FX Data:** Current exchange rates from 160+ currencies
- **Analysis Tools:** Comprehensive EDA and plotting capabilities
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
python scripts/run_cursor_mcp.py --test --report

# Start auto-start server
python scripts/auto_start_mcp.py start

# Manual server start
python pycharm_github_copilot_mcp.py
```

📚 **[MCP Servers Documentation](docs/mcp-servers/README.md)**

## 📚 Documentation

📚 **[Complete Documentation](docs/index.md)**

### Quick Links

- [Getting Started](docs/getting-started.md) - Overview and setup
- [Quick Examples](docs/quick-examples.md) - Fast start examples and common workflows
- [Usage Examples](docs/usage-examples.md) - Comprehensive examples and workflows
- [Indicator Export](docs/indicator-export.md) - Export calculated indicators
- [Exchange Rate API](docs/exchange-rate-api-complete.md) - Real-time FX data
- [Docker Setup](docs/docker.md) - Containerized development
- [Analysis Tools](docs/analysis-eda.md) - EDA and plotting

### Development
- [Testing](docs/testing.md) - Test framework
- [CI/CD](docs/ci-cd.md) - GitHub Actions
- [Scripts](docs/scripts.md) - Automation tools
- [Project Structure](docs/project-structure.md) - Code organization

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
python scripts/run_cursor_mcp.py --test --report

# Enable debug mode
export LOG_LEVEL=DEBUG
python pycharm_github_copilot_mcp.py

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
- Review the [quick examples](docs/quick-examples.md) for fast start
- Review the [usage examples](docs/usage-examples.md) for comprehensive workflows
- Contact the development team