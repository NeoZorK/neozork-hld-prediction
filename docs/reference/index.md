# Reference Documentation

This section provides comprehensive technical reference documentation for the NeoZork HLD Prediction project, including UV package management and adaptive testing.

## 🚀 Quick Reference

### [API Reference](api-reference.md)
Complete API documentation for all modules and functions.

### [Configuration Reference](configuration.md)
Configuration options and environment variables.

### [UV Package Manager Reference](uv-reference.md) ⭐ **NEW**
Comprehensive reference for UV package manager usage.

**Highlights:**
- **UV Commands**: Complete command reference
- **Environment Variables**: UV configuration options
- **Docker Integration**: UV in containerized environments
- **Performance Tuning**: UV optimization techniques
- **Troubleshooting**: Common UV issues and solutions

## 📚 Core Reference

### [Core Calculations](core-calculation.md)
Core calculation engine and mathematical foundations.

### [Advanced Metrics](advanced-metrics.md)
Advanced financial metrics and calculations.

### [MCP Server Reference](mcp-servers/README.md)
Model Context Protocol server documentation.

## 🔧 Technical Indicators Reference

### [Indicators Overview](indicators/index.md)
Complete reference for all technical indicators.

### Momentum Indicators
- **[MACD Indicator](indicators/momentum/macd-indicator.md)** - Moving Average Convergence Divergence

### Oscillators
- **[RSI Indicator](indicators/oscillators/rsi-indicator.md)** - Relative Strength Index
- **[CCI Indicator](indicators/oscillators/cci-indicator.md)** - Commodity Channel Index
- **[Stochastic Indicator](indicators/oscillators/stochastic-indicator.md)** - Stochastic oscillator

### Trend Indicators
- **[EMA Indicator](indicators/trend/ema-indicator.md)** - Exponential Moving Average
- **[ADX Indicator](indicators/trend/adx-indicator.md)** - Average Directional Index
- **[SAR Indicator](indicators/trend/sar-indicator.md)** - Parabolic SAR

### Volatility Indicators
- **[ATR Indicator](indicators/volatility/atr-indicator.md)** - Average True Range
- **[Bollinger Bands](indicators/volatility/bollinger-bands-indicator.md)** - Bollinger Bands
- **[Standard Deviation](indicators/volatility/stdev-indicator.md)** - Standard Deviation

### Volume Indicators
- **[OBV Indicator](indicators/volume/obv-indicator.md)** - On-Balance Volume
- **[VWAP Indicator](indicators/volume/vwap-indicator.md)** - Volume Weighted Average Price

### Support & Resistance
- **[Donchian Channels](indicators/support-resistance/donchian-channels-indicator.md)** - Donchian Channels
- **[Fibonacci Retracements](indicators/support-resistance/fibonacci-retracements-indicator.md)** - Fibonacci levels
- **[Pivot Points](indicators/support-resistance/pivot-points-indicator.md)** - Pivot point calculations

### Predictive Indicators
- **[HMA Indicator](indicators/predictive/hma-indicator.md)** - Hull Moving Average
- **[Time Series Forecast](indicators/predictive/tsforecast-indicator.md)** - Time series forecasting

### Probability Indicators
- **[Monte Carlo](indicators/probability/montecarlo-indicator.md)** - Monte Carlo simulation
- **[Kelly Criterion](indicators/probability/kelly-indicator.md)** - Kelly Criterion

### Sentiment Indicators
- **[Fear & Greed](indicators/sentiment/fear-greed-indicator.md)** - Market sentiment
- **[COT Indicator](indicators/sentiment/cot-indicator.md)** - Commitments of Traders
- **[Put/Call Ratio](indicators/sentiment/putcallratio-indicator.md)** - Options sentiment, contrarian signals

## 🧪 Testing Reference

### [Testing Framework](testing-framework.md)
Complete testing framework documentation.

### [UV Testing Reference](uv-testing-reference.md) ⭐ **NEW**
Specialized reference for UV package manager testing.

**Includes:**
- **Test Structure**: UV test organization and patterns
- **Environment Detection**: Docker vs local environment detection
- **Adaptive Testing**: Environment-aware test execution
- **Performance Testing**: UV vs pip performance comparison
- **Integration Testing**: End-to-end UV validation

### Test Categories Reference
```python
# Docker Environment Tests
def test_docker_uv_full_validation():
    """Full UV validation in Docker environment."""
    assert check_uv_variables()
    assert check_uv_paths()
    assert check_uv_commands()
    assert check_uv_packages()

# Local Environment Tests
def test_local_uv_basic_validation():
    """Basic UV validation in local environment."""
    assert check_uv_installation()
    assert check_local_directories()
    assert check_uv_basic_commands()

# Adaptive Tests
def test_adaptive_uv_validation():
    """Adaptive UV validation for both environments."""
    if is_docker_environment():
        # Full validation in Docker
        assert check_uv_variables()
        assert check_uv_paths()
        assert check_uv_commands()
    else:
        # Basic validation in local
        assert check_uv_installation()
        assert check_local_directories()
```

## 🔧 UV Package Manager Reference

### UV Commands Reference
```bash
# Basic Commands
uv --version                    # Check UV version
uv --help                       # Show help
uv pip --help                   # Show pip help

# Package Management
uv pip install package          # Install package
uv pip install -r requirements.txt  # Install from requirements
uv pip install --upgrade package    # Upgrade package
uv pip uninstall package        # Uninstall package
uv pip list                     # List installed packages
uv pip show package             # Show package details
uv pip freeze                   # Freeze requirements

# Virtual Environment Management
uv venv                         # Create virtual environment
uv venv --python 3.11           # Create with specific Python
uv venv --name myenv            # Create with custom name
source .venv/bin/activate       # Activate environment
deactivate                      # Deactivate environment

# Cache Management
uv cache clean                  # Clean cache
uv cache info                   # Cache information
uv cache dir                    # Show cache directory

# Performance Commands
uv pip install --no-cache       # Install without cache
uv pip install --upgrade        # Upgrade all packages
uv pip install --force-reinstall # Force reinstall
```

### UV Environment Variables Reference
```bash
# Core UV Configuration
UV_ONLY_MODE=true              # Enable UV-only mode
UV_CACHE_DIR=./.uv_cache       # Set cache directory
UV_VENV_DIR=./.venv            # Set virtual environment directory
UV_PYTHON=python3.11           # Set Python version
UV_PIP_INDEX_URL=https://pypi.org/simple/  # Set package index

# Docker Environment
UV_ONLY_MODE=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv
PYTHONPATH=/app/src
LOG_LEVEL=INFO

# Local Environment
export UV_ONLY_MODE=true
export UV_CACHE_DIR=./.uv_cache
export UV_VENV_DIR=./.venv
export PYTHONPATH=./src
```

### UV Configuration Files Reference
```toml
# uv.toml configuration
[project]
name = "neozork-hld-prediction"
version = "2.0.0"
description = "Financial analysis with UV package management"

[tool.uv]
python = "3.11"
cache-dir = "./.uv_cache"
venv-dir = "./.venv"

[tool.uv.dependencies]
pandas = "^2.0.0"
numpy = "^1.24.0"
matplotlib = "^3.7.0"

[tool.uv.dev-dependencies]
pytest = "^7.4.0"
black = "^23.3.0"
flake8 = "^6.0.0"
```

## 🐳 Docker Reference

### [Docker Configuration](docker-configuration.md)
Docker configuration and environment setup.

### [UV in Docker Reference](uv-docker-reference.md) ⭐ **NEW**
Specialized reference for UV package manager in Docker.

**Covers:**
- **Container Setup**: UV installation in containers
- **Environment Variables**: Docker-specific UV configuration
- **Volume Management**: UV cache and virtual environment volumes
- **Performance**: UV performance optimization in Docker
- **Troubleshooting**: Common Docker UV issues

### Docker Commands Reference
```bash
# Container Management
docker-compose up -d            # Start services
docker-compose down             # Stop services
docker-compose ps               # Show service status
docker-compose logs -f          # Follow logs
docker-compose exec neozork bash # Access container

# UV Commands in Docker
docker-compose exec neozork uv-install    # Install dependencies
docker-compose exec neozork uv-update     # Update dependencies
docker-compose exec neozork uv-test       # Test UV functionality
docker-compose exec neozork uv --version  # Check UV version

# Testing in Docker
docker-compose exec neozork pytest tests/docker/test_uv_simple.py -v
docker-compose exec neozork pytest tests/docker/test_uv_commands.py -v
docker-compose exec neozork pytest tests/docker/test_uv_only_mode.py -v
```

## 📊 Data Sources Reference

### [Data Sources API](data-sources-api.md)
Complete API reference for data sources.

### [Exchange Rate API](exchange-rate-api-complete.md)
Real-time exchange rate data API.

### Data Source Configuration Reference
```python
# Polygon API Configuration
POLYGON_API_KEY = "your_api_key"
POLYGON_BASE_URL = "https://api.polygon.io"

# YFinance Configuration
YFINANCE_TIMEOUT = 30
YFINANCE_RETRIES = 3

# Binance Configuration
BINANCE_API_KEY = "your_api_key"
BINANCE_SECRET_KEY = "your_secret_key"
BINANCE_BASE_URL = "https://api.binance.com"

# MQL5 Configuration
MQL5_LOGIN = "your_login"
MQL5_PASSWORD = "your_password"
MQL5_SERVER = "your_server"
```

## 🔍 CLI Reference

### [CLI Commands](cli-commands.md)
Complete command-line interface reference.

### CLI Commands Reference
```bash
# Basic Analysis Commands
nz demo --rule PHLD                    # Run demo analysis
nz yfinance AAPL --rule PHLD           # Analyze specific symbol
nz binance BTCUSDT --interval H1       # Cryptocurrency analysis
nz mql5 EURUSD --interval H4           # Forex analysis

# Data Source Commands
nz polygon AAPL --interval 1D          # Polygon data
nz yfinance AAPL --period 1y           # YFinance data
nz binance BTCUSDT --limit 1000        # Binance data
nz mql5 EURUSD --count 500             # MQL5 data

# Analysis Parameters
nz yfinance AAPL --rule PHLD --plot    # Generate plots
nz yfinance AAPL --rule PHLD --export  # Export results
nz yfinance AAPL --rule PHLD --verbose # Verbose output
```

## 🧪 Testing Commands Reference

### UV Testing Commands
```bash
# Basic UV Testing
python scripts/check_uv_mode.py --verbose
python scripts/check_uv_mode.py --debug
python scripts/check_uv_mode.py --docker-only

# UV Test Execution
pytest tests/docker/test_uv_simple.py -v
pytest tests/docker/test_uv_commands.py -v
pytest tests/docker/test_uv_only_mode.py -v

# Docker UV Testing
docker-compose exec neozork uv-test
docker-compose exec neozork pytest tests/docker/ -v
docker-compose exec neozork python scripts/check_uv_mode.py
```

### Environment Detection Reference
```python
# Environment Detection Functions
def is_docker_environment():
    """Check if running in Docker container."""
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'

def check_uv_variables():
    """Check UV environment variables."""
    required_vars = ['UV_ONLY_MODE', 'UV_CACHE_DIR', 'UV_VENV_DIR']
    return all(os.environ.get(var) for var in required_vars)

def check_uv_paths():
    """Check UV paths and directories."""
    cache_dir = os.environ.get('UV_CACHE_DIR', '/app/.uv_cache')
    venv_dir = os.environ.get('UV_VENV_DIR', '/app/.venv')
    return os.path.exists(cache_dir) and os.path.exists(venv_dir)

def check_uv_commands():
    """Check UV command availability."""
    try:
        subprocess.run(['uv', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
```

## 📈 Performance Reference

### [Performance Metrics](performance-metrics.md)
Performance benchmarks and optimization guidelines.

### UV Performance Reference
```bash
# UV vs Pip Performance Comparison
# Installation Speed (packages/second)
uv: 150-300 packages/second
pip: 5-15 packages/second

# Dependency Resolution
uv: 0.1-1.0 seconds
pip: 10-60 seconds

# Virtual Environment Creation
uv: 0.5-2.0 seconds
pip: 5-15 seconds

# Cache Efficiency
uv: 95-99% cache hit rate
pip: 60-80% cache hit rate
```

## 🔒 Security Reference

### [Security Guidelines](security-guidelines.md)
Security best practices and considerations.

### UV Security Reference
```bash
# Package Verification
uv pip install --require-hashes package  # Require package hashes
uv pip install --no-deps package         # Install without dependencies
uv pip install --only-binary package     # Install only binary packages

# Environment Isolation
uv venv --isolated                       # Create isolated environment
uv pip install --user package            # Install for user only
uv pip install --target ./local package  # Install to specific directory
```

## 🚨 Troubleshooting Reference

### [Troubleshooting Guide](troubleshooting-guide.md)
Common issues and solutions.

### UV Troubleshooting Reference
```bash
# Common UV Issues and Solutions

# Issue: UV not found
# Solution: Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Issue: Cache directory not accessible
# Solution: Create cache directory
mkdir -p ./.uv_cache

# Issue: Virtual environment not found
# Solution: Create virtual environment
uv venv

# Issue: Package installation fails
# Solution: Check network and try again
uv pip install --upgrade pip
uv pip install package-name

# Issue: Import errors
# Solution: Check Python path
export PYTHONPATH=$PYTHONPATH:./src
```

## 📚 Additional Resources

### Documentation
- **Getting Started**: Basic setup and installation
- **Examples**: Practical usage examples
- **Guides**: Step-by-step tutorials
- **API Documentation**: External API references

### Tools and Libraries
- **UV Documentation**: Official UV documentation
- **Docker Documentation**: Docker usage guides
- **Pytest Documentation**: Testing framework guides
- **Python Documentation**: Python language reference

### Community
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Community discussions
- **Documentation**: Comprehensive guides and references

---

**Last Updated**: 2024
**Version**: 2.0.0 (UV-Only Mode) 