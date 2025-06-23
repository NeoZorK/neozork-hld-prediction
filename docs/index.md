# Documentation Index

Complete guide to NeoZork HLD Prediction project with AI-powered development assistance.

## 🚀 Quick Start

- **[Getting Started](getting-started.md)** - Project overview, installation, and quick setup
- **[Usage Examples](usage-examples.md)** - Common commands and use cases

## 🤖 AI-Powered Development

- **[MCP Servers](mcp-servers/README.md)** - Model Context Protocol servers for intelligent development
  - **[Setup Guide](mcp-servers/SETUP.md)** - Detailed configuration and installation
  - **[Usage Guide](mcp-servers/USAGE.md)** - Examples and API documentation
  - **[Changes Summary](mcp-servers/CHANGES_SUMMARY.md)** - Updates and improvements

## 📊 Core Documentation

- **[Docker](docker.md)** - Containerized development
- **[Exchange Rate API](exchange-rate-api-complete.md)** - Real-time forex data integration
- **[Indicator Export](indicator-export.md)** - Export calculated indicators to multiple formats
- **[UV Setup](uv-setup.md)** - Fast package manager

## 🔧 Tools & Analysis

- **[Analysis & EDA](analysis-eda.md)** - Data analysis and exploration tools
- **[Scripts](scripts.md)** - Available scripts and automation
- **[Utility Scripts](utility-scripts.md)** - Data conversion and test file management utilities
- **[Debug Scripts](debug-scripts.md)** - Testing and debugging tools

## 💻 Development

- **[Testing](testing.md)** - Testing framework and validation
- **[CI/CD](ci-cd.md)** - GitHub Actions and local testing
- **[Project Structure](project-structure.md)** - Directory organization

## 📈 MCP Server Features

### PyCharm GitHub Copilot MCP Server
- **Smart Autocompletion:** Financial symbols, timeframes, technical indicators
- **Context-Aware Suggestions:** AI-powered code completion
- **GitHub Copilot Integration:** Enhanced AI assistance

### Auto-Start MCP Server
- **Intelligent Detection:** Automatically detects running IDEs
- **Condition-Based Startup:** Starts servers based on project conditions
- **Health Monitoring:** Continuous monitoring and automatic restart

### Quick MCP Setup
```bash
# Test MCP servers
python scripts/run_cursor_mcp.py --test --report

# Start auto-start server
python scripts/auto_start_mcp.py start

# Manual server start
python pycharm_github_copilot_mcp.py
```

## 📝 Export Flags: Allowed Modes

Export flags (`--export-parquet`, `--export-csv`, `--export-json`) are only available in `demo` mode. They are not allowed in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, or `exrate` modes.

### Example Workflow

1. **Download or Convert Data**
   - Download with yfinance:
     ```bash
     python run_analysis.py yfinance --ticker EURUSD=X --period 1y --point 0.00001
     ```
   - Or convert from CSV:
     ```bash
     python run_analysis.py csv --csv-file mydata.csv --point 0.01
     ```
2. **Apply Indicator and Export**
   - Use show mode with a rule and export flags:
     ```bash
     python run_analysis.py show yfinance EURUSD=X --rule PHLD --export-parquet --export-csv --export-json
     ```
3. **View Exported Indicators**
   - Use show ind to view the exported files:
     ```bash
     python run_analysis.py show ind parquet
     python run_analysis.py show ind csv
     python run_analysis.py show ind json
     ```

> Export flags are not available in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, or `exrate` modes. Use `demo` for direct export, or the above workflow for real data.

## 👥 Navigation by Role

### New Users
1. [Getting Started](getting-started.md)
2. [Usage Examples](usage-examples.md)
3. [MCP Servers](mcp-servers/README.md) - For AI assistance

### Developers
1. [Project Structure](project-structure.md)
2. [Testing](testing.md)
3. [CI/CD](ci-cd.md)
4. [Debug Scripts](debug-scripts.md)
5. [MCP Servers Setup](mcp-servers/SETUP.md) - IDE configuration

### Data Scientists
1. [Exchange Rate API](exchange-rate-api-complete.md)
2. [Analysis & EDA](analysis-eda.md)
3. [Usage Examples](usage-examples.md)
4. [Scripts](scripts.md)
5. [MCP Servers Usage](mcp-servers/USAGE.md) - Advanced examples

### DevOps
1. [Docker](docker.md)
2. [CI/CD](ci-cd.md)
3. [UV Setup](uv-setup.md)
4. [MCP Servers](mcp-servers/README.md) - Server deployment

## 🎯 By Task

**Setup:**
- [Getting Started](getting-started.md) (includes installation)
- [MCP Servers Setup](mcp-servers/SETUP.md) (AI assistance setup)

**Usage:**
- [Usage Examples](usage-examples.md) → [Exchange Rate API](exchange-rate-api-complete.md) → [Analysis & EDA](analysis-eda.md)
- [MCP Servers Usage](mcp-servers/USAGE.md) (AI-powered development)

**Development:**
- [Project Structure](project-structure.md) → [Testing](testing.md) → [CI/CD](ci-cd.md)
- [MCP Servers](mcp-servers/README.md) (AI assistance)

**Deployment:**
- [Docker](docker.md) → [CI/CD](ci-cd.md) → [MCP Servers](mcp-servers/README.md)

## 📊 Performance Metrics

| Feature | Performance |
|---------|-------------|
| MCP Server Startup | < 3s |
| Autocompletion Response | 5-15ms |
| File Indexing | 50ms/file |
| Memory Usage | 25-50MB |
| Test Coverage | 100% |

## 🔧 IDE Integration

### Supported IDEs
- **PyCharm:** MCP plugin with GitHub Copilot integration
- **Cursor:** AI Assistant with MCP server support
- **VS Code:** MCP extension with Copilot enhancement

### Quick IDE Setup
1. Install MCP plugin/extension for your IDE
2. Configure server settings
3. Enable GitHub Copilot (optional)
4. Restart IDE for changes to take effect

## 🐛 Troubleshooting

### MCP Server Issues
- Check server status: `python scripts/run_cursor_mcp.py --test --report`
- Enable debug mode: `export LOG_LEVEL=DEBUG`
- Verify dependencies: `pip list | grep -E "(watchdog|psutil)"`

### General Issues
- Ensure Python 3.12+ is installed
- Check all dependencies: `pip install -e .`
- Verify API keys for live data sources
- Check logs in `logs/` directory

# Neozork HLD Prediction

A comprehensive financial analysis tool for high-low direction prediction using technical indicators.

## Quick Start

```bash
# Install dependencies
pip install uv && uv sync

# Run demo analysis
python run_analysis.py demo

# Try interactive mode
python run_analysis.py interactive

# View all examples
python run_analysis.py --examples
```

## Features

- **Multiple Data Sources**: Yahoo Finance, Binance, Polygon.io, CSV files, Exchange Rate API
- **Technical Indicators**: RSI, MACD, EMA, Bollinger Bands, ATR, Stochastic, VWAP, and more
- **Interactive Mode**: Guided interface for analysis configuration
- **Export Options**: Parquet, CSV, JSON formats
- **MCP Servers**: GitHub Copilot integration for enhanced development
- **Comprehensive Testing**: Full test suite with coverage analysis
- **Docker Support**: Containerized deployment
- **Multiple Plotting Backends**: Plotly, Seaborn, Matplotlib, Terminal

## Documentation

- **[Getting Started](getting-started.md)** - Installation and basic setup
- **[Examples Overview](examples-overview.md)** - Complete overview of all examples
- **[Quick Examples](quick-examples.md)** - Fast start examples and common workflows
- **[Usage Examples](usage-examples.md)** - Comprehensive examples and workflows
- **[Indicator Examples](indicator-examples.md)** - Technical indicator usage examples
- **[MCP Examples](mcp-examples.md)** - MCP server usage examples
- **[Testing Examples](testing-examples.md)** - Testing and coverage examples
- **[Script Examples](script-examples.md)** - Utility and debug script examples
- **[Docker Examples](docker-examples.md)** - Docker deployment and development examples
- **[EDA Examples](eda-examples.md)** - Exploratory Data Analysis examples
- **[Project Structure](project-structure.md)** - Code organization overview
- **[Testing Guide](testing.md)** - Running tests and coverage analysis
- **[MCP Servers](mcp-servers/)** - GitHub Copilot integration setup
- **[Scripts](scripts.md)** - Utility and debug scripts
- **[Indicators](indicators/)** - Technical indicator documentation

## Quick Examples

### Basic Analysis
```bash
# Demo with RSI
python run_analysis.py demo --rule RSI

# Yahoo Finance data
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI

# CSV file analysis
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule MACD
```

### Interactive Mode
```bash
# Start interactive session
python run_analysis.py interactive

# Discover indicators
python run_analysis.py --indicators
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Test coverage
python tests/zzz_analyze_test_coverage.py
```

### MCP Servers
```bash
# Auto-start MCP servers
python scripts/auto_start_mcp.py

# Test stdio mode
python tests/test_stdio.py
```

## Data Sources

- **Yahoo Finance**: Free stock and forex data
- **Binance**: Cryptocurrency data
- **Polygon.io**: Professional market data (API key required)
- **Exchange Rate API**: Real-time forex rates
- **CSV Files**: Custom data import

## Technical Indicators

### Trend Indicators
- EMA (Exponential Moving Average)
- ADX (Average Directional Index)
- SAR (Parabolic SAR)

### Oscillators
- RSI (Relative Strength Index)
- Stochastic Oscillator
- CCI (Commodity Channel Index)

### Momentum Indicators
- MACD (Moving Average Convergence Divergence)
- Stochastic Oscillator

### Volatility Indicators
- ATR (Average True Range)
- Bollinger Bands
- Standard Deviation

### Volume Indicators
- OBV (On-Balance Volume)
- VWAP (Volume Weighted Average Price)

### Support/Resistance
- Donchian Channels
- Fibonacci Retracements
- Pivot Points

### Predictive Indicators
- HMA (Hull Moving Average)
- Time Series Forecast

### Probability Indicators
- Kelly Criterion
- Monte Carlo Simulation

### Sentiment Indicators
- Commitment of Traders
- Fear & Greed Index
- Social Sentiment

## Development

### Project Structure
```
neozork-hld-prediction/
├── src/                    # Main source code
│   ├── calculation/        # Indicator calculations
│   ├── cli/               # Command line interface
│   ├── data/              # Data acquisition
│   ├── eda/               # Exploratory data analysis
│   ├── export/            # Data export
│   ├── plotting/          # Visualization
│   └── workflow/          # Analysis workflows
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── docs/                  # Documentation
├── data/                  # Data storage
└── mcp_auto_config.json   # MCP server configuration
```

### Key Components

- **CLI Interface**: `src/cli/cli.py` - Main command line interface
- **Indicator Calculations**: `src/calculation/` - Technical indicator implementations
- **Data Acquisition**: `src/data/` - Data fetching from various sources
- **MCP Servers**: `pycharm_github_copilot_mcp.py` - GitHub Copilot integration
- **Testing**: `tests/` - Comprehensive test suite

### Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Test specific components
python -m pytest tests/calculation/indicators/ -v
python -m pytest tests/cli/ -v
python -m pytest tests/data/ -v
```

### MCP Server Integration

The project includes MCP (Model Context Protocol) servers for enhanced development experience:

- **Auto-Start Server**: `scripts/auto_start_mcp.py` - Automatic server management
- **PyCharm Integration**: `pycharm_github_copilot_mcp.py` - GitHub Copilot support
- **Testing**: `tests/test_stdio.py` - Server functionality testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support:
- Check the [documentation](docs/)
- Review [examples overview](examples-overview.md) for complete guide
- Review [quick examples](quick-examples.md) for fast start
- Review [usage examples](usage-examples.md) for comprehensive workflows
- Review [indicator examples](indicator-examples.md) for technical analysis
- Review [MCP examples](mcp-examples.md) for AI integration
- Review [testing examples](testing-examples.md) for test coverage
- Review [script examples](script-examples.md) for utilities and debugging
- Review [Docker examples](docker-examples.md) for containerized deployment
- Review [EDA examples](eda-examples.md) for data analysis
- Run `python run_analysis.py --help` for CLI help
- Use `python run_analysis.py --examples` for command examples