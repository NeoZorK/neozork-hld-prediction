# Getting Started

Welcome to the NeoZork HLD Prediction project! This section will help you get up and running quickly.

## Quick Start Guides

- **[Basic Setup](getting-started.md)** - Standard setup instructions
- **[Native Container Quick Start](QUICK_START_NATIVE_CONTAINER.md)** - Quick start for Apple Silicon native containers
- **[Project Structure](project-structure.md)** - Understanding the project layout

## Prerequisites

Before you begin, make sure you have:

- Python 3.11+ installed
- UV package manager (recommended)
- Docker (for containerized setup)
- Native container application (for Apple Silicon, macOS 26+)

## Setup Options

### 1. Local Setup with UV
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt

# Run analysis
python run_analysis.py demo --rule PHLD
```

### 2. Docker Setup
```bash
# Start container
docker-compose up -d

# Run analysis
docker-compose exec neozork nz demo --rule PHLD
```

### 3. Native Apple Silicon Container (macOS 26+)
```bash
# Run interactive container manager
./scripts/native-container/native-container.sh
```

## Next Steps

After setup, explore:

- **[Examples](../examples/)** - Practical usage examples
- **[Guides](../guides/)** - Step-by-step tutorials
- **[Reference](../reference/)** - Technical documentation

## 📚 Getting Started Guides

### [Getting Started Guide](getting-started.md)
Complete step-by-step guide for setting up the project.

**Covers:**
- System requirements
- Installation methods
- Initial configuration
- First analysis run
- Troubleshooting common issues

### [Project Structure](project-structure.md)
Understanding the codebase organization and architecture.

**Highlights:**
- Directory structure explanation
- Key components overview
- File organization principles
- Module relationships

### [Installation Guide](INSTALLATION_GUIDE.md)
Detailed installation instructions for different environments.

**Includes:**
- Prerequisites
- Environment-specific setup
- Configuration options
- Verification steps

## 🔧 UV Package Management

### What is UV?
UV is a modern Python package manager that's 10-100x faster than pip.

**Key Benefits:**
- **Speed**: Lightning-fast dependency resolution
- **Reliability**: Intelligent conflict resolution
- **Caching**: Persistent package cache
- **Virtual Environments**: Fast environment creation

### UV-Only Mode
The project uses UV exclusively for package management.

**Features:**
- **Exclusive Usage**: No fallback to pip
- **Docker Integration**: Seamless UV in containers
- **Local Development**: UV support for local environments
- **Adaptive Testing**: Tests that work in both Docker and local

### UV Setup Commands
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version

# Install project dependencies
uv pip install -r requirements.txt

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

## 🐳 Docker Setup

### Docker Benefits
- **Consistent Environment**: Same setup across all machines
- **Isolation**: No conflicts with system packages
- **Easy Deployment**: Ready-to-run containers
- **UV Integration**: Pre-configured UV environment

### Docker Commands
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Access container
docker-compose exec neozork bash

# Stop services
docker-compose down
```

### Docker Environment Variables
```bash
# UV configuration
UV_ONLY_MODE=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv

# Application configuration
PYTHONPATH=/app/src
LOG_LEVEL=INFO
```

## 🧪 Testing Your Setup

### Docker Environment
```bash
# Test UV functionality
docker-compose exec neozork uv-test

# Run comprehensive tests
docker-compose exec neozork pytest tests/docker/test_uv_only_mode.py -v

# Run simple tests
docker-compose exec neozork pytest tests/docker/test_uv_simple.py -v
```

### Local Environment
```bash
# Check UV status
python scripts/check_uv_mode.py --verbose

# Run adaptive tests
pytest tests/docker/test_uv_simple.py -v

# Test basic functionality
python -c "import pandas; print('Setup successful!')"
```

## 🚀 First Analysis

### Demo Analysis
```bash
# Docker environment
docker-compose exec neozork nz demo --rule PHLD

# Local environment
python run_analysis.py demo --rule PHLD
```

### Custom Analysis
```bash
# Analyze specific symbol
nz yfinance AAPL --rule PHLD

# Use different data source
nz binance BTCUSDT --interval H1 --rule PHLD

# Custom timeframe
nz mql5 EURUSD --interval H4 --rule PHLD
```

## 📊 Project Features

### Data Sources
- **Polygon**: Real-time market data
- **YFinance**: Yahoo Finance data
- **Binance**: Cryptocurrency data
- **MQL5**: MetaTrader 5 data

### Technical Indicators
- **Momentum**: MACD
- **Oscillators**: RSI, CCI, Stochastic
- **Trend**: EMA, ADX, SAR
- **Volatility**: ATR, Bollinger Bands
- **Volume**: OBV, VWAP
- **Support & Resistance**: Pivot Points, Fibonacci
- **Predictive**: HMA, Time Series Forecast
- **Probability**: Monte Carlo, Kelly Criterion
- **Sentiment**: Fear & Greed, COT

### Analysis Tools
- **Exploratory Data Analysis**: Comprehensive data exploration
- **Visualization**: Interactive charts and plots
- **CLI Interface**: Command-line analysis tools
- **MCP Server**: Enhanced IDE integration

## 🔍 Verification Checklist

### Docker Setup
- [ ] Docker and Docker Compose installed
- [ ] Container builds successfully
- [ ] Services start without errors
- [ ] UV commands work in container
- [ ] Tests pass in Docker environment

### Local Setup
- [ ] Python 3.8+ installed
- [ ] UV package manager installed
- [ ] Dependencies installed successfully
- [ ] Virtual environment activated
- [ ] Tests pass in local environment

### General Verification
- [ ] Can import project modules
- [ ] Can run demo analysis
- [ ] Can access data sources
- [ ] Can generate visualizations
- [ ] CLI commands work

## 🚨 Common Issues

### UV Installation Problems
```bash
# Check if UV is in PATH
which uv

# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH manually
export PATH="$HOME/.cargo/bin:$PATH"
```

### Docker Issues
```bash
# Check Docker installation
docker --version
docker-compose --version

# Clean build
docker-compose build --no-cache

# Check container logs
docker-compose logs neozork
```

### Import Errors
```bash
# Check Python path
echo $PYTHONPATH

# Add src to path
export PYTHONPATH=$PYTHONPATH:./src

# Install in development mode
uv pip install -e .
```

## 📚 Next Steps

### For Beginners
1. [Getting Started Guide](getting-started.md) - Complete setup
2. [Project Structure](project-structure.md) - Understand the codebase
3. [Examples](../examples/) - Learn through examples
4. [Guides](../guides/) - Step-by-step tutorials

### For Developers
1. [Development Setup](../development/setup.md) - Development environment
2. [Testing Guide](../development/testing.md) - Testing framework
3. [Code Style](../development/code-style.md) - Coding standards
4. [Contributing](../development/contributing.md) - Contribution guidelines

### For Analysts
1. [Data Sources](../guides/data-sources.md) - Available data providers
2. [Technical Indicators](../guides/indicators.md) - Indicator documentation
3. [Analysis Tools](../guides/analysis-tools.md) - Analysis capabilities
4. [CLI Interface](../guides/cli-interface.md) - Command-line usage

## 🆘 Getting Help

### Documentation
- **This Guide**: Getting started information
- **Examples**: Practical usage examples
- **Guides**: Step-by-step tutorials
- **Reference**: Technical documentation

### Community
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Community discussions
- **Documentation**: Comprehensive guides and references

### Support
- **Troubleshooting**: Common issues and solutions
- **Testing**: Verify your setup with tests
- **Debugging**: Tools and techniques for problem-solving

---

**Last Updated**: 2024
**Version**: 2.0.0 (UV-Only Mode) 