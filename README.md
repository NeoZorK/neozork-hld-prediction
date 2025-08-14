# NeoZork HLD Prediction

Advanced financial analysis platform with UV package management, comprehensive technical indicators, and adaptive testing.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![UV Package Manager](https://img.shields.io/badge/UV-Package%20Manager-orange.svg)](https://docs.astral.sh/uv/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)
[![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-Native%20Container-green.svg)](https://developer.apple.com/)
[![Tests](https://img.shields.io/badge/Tests-Adaptive-green.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Quick Start

### Native Apple Silicon Container (macOS 26+) - **FULL DOCKER PARITY**
```bash
# Clone and run interactive container manager
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction
./scripts/native-container/native-container.sh
```

**Quick Commands (Non-interactive):**
```bash
# Start container (full sequence with all features)
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/exec.sh --shell

# Stop container (full sequence)
./scripts/native-container/stop.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/cleanup.sh --all --force
```

**Available Commands Inside Container:**
```bash
nz --interactive                    # Interactive analysis
nz demo --rule PHLD                # Demo analysis
eda -dqc                           # Data quality checks
uv-install                         # Install dependencies
uv-pytest                          # Run tests with UV
mcp-start                          # Start MCP server
mcp-check                          # Check MCP server status
```

### Docker (Recommended for other platforms)
```bash
# Clone and start
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction
docker-compose up -d

# Run analysis with UV
docker-compose exec neozork uv run run_analysis.py demo --rule PHLD
```

### Local Setup with UV
```bash
# Clone repository
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction

# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt

# Run analysis
uv run run_analysis.py demo --rule PHLD
```

## 🔧 Development Tools

### Dead Code Analysis
Find and remove unused code and libraries:
```bash
# Quick analysis
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all

# Apply fixes safely
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix --dry-run
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix

# See [Dead Code Analysis Guide](docs/development/dead-code-analysis.md) for details
```

## 🔧 UV Package Management

This project uses **UV package manager** exclusively for dependency management, providing 10-100x faster performance than traditional pip.

### UV-Only Mode Features
- **Exclusive UV Usage**: No fallback to pip
- **Docker Integration**: Seamless UV in containers
- **Native Container Integration**: Full UV support in Apple Silicon containers
- **Local Development**: UV support for local environments
- **Adaptive Testing**: Tests that work in both Docker and local
- **Performance**: Lightning-fast dependency resolution

### UV Commands
```bash
# Install dependencies
uv pip install -r requirements.txt

# Install specific package
uv pip install pandas numpy

# Update packages
uv pip install --upgrade pandas

# List installed packages
uv pip list

# Create virtual environment
uv venv

# Run analysis with UV
uv run run_analysis.py demo --rule PHLD

# Run tests with UV (multithreaded)
uv run pytest tests -n auto
```

## 📊 Features

### Data Sources
- **Polygon**: Real-time market data
- **YFinance**: Yahoo Finance data
- **Binance**: Cryptocurrency data
- **MQL5**: MetaTrader 5 data

### Technical Indicators (50+)
- **Momentum**: MACD
- **Oscillators**: RSI, CCI, Stochastic
- **Trend**: EMA, ADX, SAR, **SuperTrend**
- **Volatility**: ATR, Bollinger Bands
- **Volume**: OBV, VWAP
- **Support & Resistance**: Pivot Points, Fibonacci
- **Predictive**: HMA, Time Series Forecast
- **Probability**: Monte Carlo, Kelly Criterion
- **Sentiment**: Fear & Greed, **COT**, Put/Call Ratio

#### New: COT (Commitments of Traders) Indicator
- **Category:** Sentiment
- **Description:** Analyzes futures market positioning to gauge institutional sentiment. Useful for trend confirmation and reversal spotting.
- **CLI Example:**
  ```bash
  uv run run_analysis.py show csv mn1 -d fastest --rule cot:14,close
  ```
- **Documentation:** [COT Indicator](docs/reference/indicators/sentiment/cot-indicator.md)

#### New: Put/Call Ratio Indicator
- **Category:** Sentiment
- **Description:** Measures the ratio of put options to call options to gauge market sentiment. Useful as a contrarian indicator for potential market reversals.
- **CLI Example:**
  ```bash
  uv run run_analysis.py show csv mn1 -d fastest --rule putcallratio:20,close
  ```
- **Documentation:** [Put/Call Ratio Indicator](docs/reference/indicators/sentiment/putcallratio-indicator.md)

#### New: SuperTrend Indicator
- **Category:** Trend
- **Description:** Advanced trend-following indicator that combines ATR (Average True Range) with price action to identify trend direction and potential reversal points. Provides dynamic support/resistance levels and generates buy/sell signals.
- **CLI Example:**
  ```bash
  uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0
  uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0,open
  ```
- **Parameters:** period (required), multiplier (required), price_type (optional: open/close)
- **Documentation:** [SuperTrend Indicator](docs/reference/indicators/trend/supertrend-indicator.md)

#### Fixed: Volume Indicators
- **OBV (On-Balance Volume):** Fixed dual chart plotting and parameter parsing
- **VWAP (Volume Weighted Average Price):** Enhanced volume column handling
- **CLI Examples:**
  ```bash
  # OBV - now works perfectly
  uv run run_analysis.py show csv mn1 -d fastest --rule obv:
  
  # VWAP with custom parameters
  uv run run_analysis.py show csv mn1 -d fastest --rule vwap:20
  ```

### Analysis Tools
- **Exploratory Data Analysis**: Comprehensive data exploration
- **Visualization**: Interactive charts and plots
- **CLI Interface**: Command-line analysis tools
- **MCP Server**: Enhanced IDE integration

## 🧪 Testing

### Adaptive Testing Framework
Tests are designed to work in both Docker and local environments:

```bash
# Docker environment
docker-compose exec neozork pytest tests/docker/test_uv_simple.py -v

# Local environment
pytest tests/docker/test_uv_simple.py -v

# Check UV status
python scripts/check_uv_mode.py --verbose

# Native container tests
uv run pytest tests/native-container/test_native_container_full_functionality.py -v

# Run all tests with UV (multithreaded)
uv run pytest tests -n auto
```

### CI/CD Testing with Act
Test GitHub Actions workflows and MCP server integration locally without downloading Docker images:

```bash
# Install act tool
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux

# Test all workflows (dry run - no Docker downloads)
act -n

# Test specific workflows
act -n -W .github/workflows/docker-build.yml
act -n -W .github/workflows/mcp-integration.yml

# List available workflows
act -l
```

**Benefits:**
- **No Docker Downloads**: Prevents downloading large Docker images
- **Fast Validation**: Quickly validates workflow syntax and structure
- **MCP Server Testing**: Verify MCP server communication protocols
- **Resource Efficient**: Uses minimal system resources

## 🐛 Recent Fixes & Improvements

### Volume Indicators Fix
**Issue:** OBV indicator had dual chart plotting errors and parameter parsing issues.

**Fix:** 
- Fixed parameter parsing for `--rule obv:` (empty parameters after colon)
- Fixed volume column handling for volume-based indicators
- Fixed dual chart plotting for OBV with proper argument passing

**Before:**
```bash
# This would fail with parameter parsing error
uv run run_analysis.py show csv mn1 -d fastest --rule obv:
```

**After:**
```bash
# This now works perfectly
uv run run_analysis.py show csv mn1 -d fastest --rule obv:
```

### UV Integration Improvements
- **Exclusive UV Usage**: All commands now use UV for consistency
- **Multithreaded Testing**: `uv run pytest tests -n auto`
- **Docker Integration**: Seamless UV in containers
- **Native Container Support**: Full UV support in Apple Silicon containers

## 📋 Quick Examples

### Basic Analysis
```bash
# Demo analysis
uv run run_analysis.py demo --rule PHLD

# Yahoo Finance analysis
uv run run_analysis.py yfinance AAPL --rule RSI

# CSV analysis (fixed volume indicators)
uv run run_analysis.py show csv mn1 -d fastest --rule obv:

# Interactive analysis
uv run run_analysis.py interactive
```

### Advanced Analysis
```bash
# Multiple indicators
uv run run_analysis.py demo --rule RSI,MACD,PHLD

# Custom plotting backend
uv run run_analysis.py demo --rule PHLD -d plotly

# Export results
uv run run_analysis.py demo --rule PHLD --export-parquet --export-csv
```

### Testing
```bash
# Run all tests (multithreaded)
uv run pytest tests -n auto

# Run specific test categories
uv run pytest tests/calculation/ -n auto
uv run pytest tests/cli/ -n auto

# Run with coverage
uv run pytest tests/ --cov=src -n auto
```

## 🚀 Performance Examples

### UV vs Traditional pip
```bash
# Traditional pip (slower)
pip install -r requirements.txt  # ~30-60 seconds

# UV (much faster)
uv pip install -r requirements.txt  # ~3-10 seconds

# UV with caching (fastest)
uv pip install -r requirements.txt  # ~1-3 seconds (subsequent runs)
```

### Multithreaded Testing
```bash
# Single-threaded testing
pytest tests/  # ~2-5 minutes

# UV multithreaded testing
uv run pytest tests -n auto  # ~30-60 seconds
```

## 📚 Documentation

- **[Getting Started](docs/getting-started/)** - Setup and first steps
- **[Examples](docs/examples/)** - Practical usage examples
- **[Guides](docs/guides/)** - Step-by-step tutorials
- **[Reference](docs/reference/)** - Technical documentation
- **[Testing](docs/testing/)** - Testing strategies and examples

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest tests -n auto`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/username/neozork-hld-prediction/issues)
- **Documentation**: [docs/](docs/)
- **Examples**: [docs/examples/](docs/examples/)

---

**Built with ❤️ using UV package manager for lightning-fast performance**