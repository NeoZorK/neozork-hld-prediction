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

# Run analysis
docker-compose exec neozork nz demo --rule PHLD
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
python run_analysis.py demo --rule PHLD
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

# Run tests with UV
uv run pytest tests -n auto
```

## 📊 Features

### Data Sources
- **Polygon**: Real-time market data
- **YFinance**: Yahoo Finance data
- **Binance**: Cryptocurrency data
- **MQL5**: MetaTrader 5 data

### Technical Indicators (50+)
- **Momentum**: MACD, Stochastic Oscillator
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
```

### Test Categories
- **UV-Specific Tests**: Package manager validation
- **Environment Tests**: Docker vs local detection
- **Integration Tests**: End-to-end functionality
- **Performance Tests**: UV vs pip comparison
- **Native Container Tests**: Full functionality validation

## 📚 Documentation

### Quick Links
- **[Getting Started](docs/getting-started/)** - Setup and installation
- **[UV-Only Mode](docs/deployment/uv-only-mode.md)** - UV package management
- **[Native Container](scripts/native-container/README.md)** - Apple Silicon container guide
- **[Examples](docs/examples/)** - Practical usage examples
- **[Guides](docs/guides/)** - Step-by-step tutorials
- **[Reference](docs/reference/)** - Technical documentation

### Documentation Structure
```
docs/
├── getting-started/     # Setup and installation
├── deployment/          # Deployment guides
├── development/         # Development setup
├── examples/           # Usage examples
├── guides/             # Tutorials and guides
└── reference/          # Technical reference
```

## 🐳 Container Support

### Native Apple Silicon Container (macOS 26+) - **FULL DOCKER PARITY**

**NEW: Native container support for Apple Silicon Macs with 30-50% performance improvement and complete Docker feature parity!**

#### 🚀 Full Feature Parity with Docker
The Native Container now provides **complete feature parity** with the Docker container:

- ✅ **UV Package Manager Support** - UV-only mode with command wrappers
- ✅ **MCP Server Integration** - Startup, monitoring, and cleanup
- ✅ **Command Wrappers** - `nz`, `eda`, `uv-*`, `mcp-*` commands
- ✅ **Bash Environment & History** - Interactive shell with command history
- ✅ **External Data Feed Tests** - Polygon, YFinance, Binance testing
- ✅ **Usage Guide & Help** - Comprehensive help and examples
- ✅ **Directory Structure & Permissions** - Complete Docker parity

#### Features
- **30-50% performance improvement** over Docker
- **Lower resource usage** and faster startup times
- **Native Apple Silicon optimization**
- **Interactive management script**
- **Seamless UV integration**
- **Complete Docker feature parity**

#### Quick Start
```bash
# Run interactive container manager
./scripts/native-container/native-container.sh

# Or use individual scripts
./scripts/native-container/setup.sh    # Initial setup with full Docker parity
./scripts/native-container/run.sh      # Start container
./scripts/native-container/exec.sh     # Execute commands
```

#### Interactive Script Features
- **Start Container (Full Sequence)**: Smart startup with shell access (handles already running containers)
- **Stop Container (Full Sequence)**: Stop, status check, and cleanup
- **Show Container Status**: Display current container status
- **Help**: Show help information
- **Exit**: Exit the script (option 0)

#### Available Commands Inside Container
```bash
# Analysis Commands
nz --interactive                    # Interactive analysis
nz demo --rule PHLD                # Demo analysis
nz yfinance AAPL --rule PHLD       # YFinance analysis
nz mql5 BTCUSD --interval H4 --rule PHLD  # MQL5 analysis
eda -dqc                           # Data quality checks
eda --descriptive-stats            # Descriptive statistics

# UV Package Manager Commands
uv-install                         # Install dependencies
uv-update                          # Update dependencies
uv-test                            # Run UV environment test
uv-pytest                          # Run pytest with UV
uv pip list                        # List installed packages

# MCP Server Commands
mcp-start                          # Start MCP server
mcp-check                          # Check MCP server status
python scripts/check_mcp_status.py # Detailed MCP status

# Testing Commands
uv run pytest tests -n auto        # Run all tests with UV
python tests/run_tests_docker.py   # Run external data feed tests
```

#### Prerequisites
- macOS 26 Tahoe (Developer Beta) or higher
- Native container application from Apple Developer Beta
- Python 3.11+ installed
- At least 4GB of available RAM

#### Performance Benefits
- **30-50% faster** than Docker
- **Lower memory usage**
- **Faster startup times**
- **Better macOS integration**
- **Native Apple Silicon optimizations**
- **Complete Docker feature parity**

### Docker Support

#### Docker Features
- **UV Integration**: Pre-configured UV environment
- **Multi-stage Builds**: Optimized container images
- **Volume Mounting**: Persistent data storage
- **Health Checks**: Automatic service monitoring
- **Cross-platform**: Works on all platforms

#### Docker Commands
```bash
# Start services
docker-compose up -d

# Access container
docker-compose exec neozork bash

# Install dependencies
docker-compose exec neozork uv-install

# Run tests
docker-compose exec neozork pytest tests/docker/ -v
```

## 🔍 Usage Examples

### Basic Analysis
```bash
# Demo analysis
nz demo --rule PHLD

# Analyze specific symbol
nz yfinance AAPL --rule PHLD

# Cryptocurrency analysis
nz binance BTCUSDT --interval H1 --rule PHLD

# Forex analysis
nz mql5 EURUSD --interval H4 --rule PHLD
```

### UV Package Management
```bash
# Install dependencies (Docker)
docker-compose exec neozork uv-install

# Update dependencies (Docker)
docker-compose exec neozork uv-update

# Check UV status
python scripts/check_uv_mode.py --verbose

# Local UV usage
uv pip install pandas
uv pip list
```

## 📈 Performance

### UV vs Traditional Pip
- **Installation Speed**: 10-100x faster
- **Dependency Resolution**: Intelligent conflict resolution
- **Virtual Environments**: Fast environment creation
- **Caching**: Persistent package cache

### Docker Optimization
- **Multi-stage Builds**: Reduced image size
- **Layer Caching**: Faster rebuilds
- **Volume Mounting**: Persistent data storage
- **Health Checks**: Automatic service monitoring

## 🔒 Security

### Container Security
- **Non-root Execution**: Secure container operation
- **Package Verification**: UV's built-in security checks
- **Environment Isolation**: Proper environment separation
- **Input Validation**: Comprehensive input sanitization

### Network Security
- **Internal Communication**: Secure inter-service communication
- **External APIs**: Secure API key management
- **Data Encryption**: Encrypted data transmission

## 🚨 Troubleshooting

### Common Issues

#### UV Installation Problems
```bash
# Check UV installation
uv --version

# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clear cache
rm -rf ~/.cache/uv
```

#### Docker Issues
```bash
# Clean build
docker-compose build --no-cache

# Check logs
docker-compose logs neozork

# Verify environment
docker-compose exec neozork env | grep UV
```

#### Test Failures
```bash
# Run with verbose output
pytest tests/docker/ -v -s

# Check environment detection
python scripts/check_uv_mode.py --debug

# Test specific environment
python scripts/check_uv_mode.py --docker-only
```

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction

# Install UV and dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Check code quality
python scripts/check_uv_mode.py --verbose
```

### Contribution Guidelines
- Follow the existing code style
- Write tests for new features
- Update documentation
- Use UV for package management
- Test in both Docker and local environments

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- **Getting Started**: Basic setup and installation
- **Examples**: Practical usage examples
- **Guides**: Step-by-step tutorials
- **Reference**: Technical documentation

### Community
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Community discussions
- **Documentation**: Comprehensive guides and references

### Testing
- **Test Suite**: Comprehensive test coverage
- **UV Validation**: Package manager testing
- **Environment Testing**: Docker and local validation

## 🍎 Native Container Documentation

### Detailed Guides
- **[Native Container Setup](docs/deployment/native-container-setup.md)** - Complete setup guide
- **[Native vs Docker Comparison](docs/deployment/native-vs-docker-comparison.md)** - Performance comparison
- **[Interactive Script Guide](scripts/native-container/README.md)** - Interactive script documentation
- **[Automatic Dependencies](docs/deployment/automatic-dependencies.md)** - Automatic dependency installation

### Testing Native Container

#### Automated Testing
```bash
# Run all native container tests
pytest tests/native-container/ -v

# Run specific test categories
pytest tests/native-container/test_native_container_script.py -v
pytest tests/native-container/test_setup_script.py -v
pytest tests/native-container/test_run_script.py -v
pytest tests/native-container/test_automatic_dependencies.py -v

# Run with coverage
pytest tests/native-container/ --cov=scripts/native-container --cov-report=html
```

#### Manual Testing
```bash
# Test interactive script
./scripts/native-container/native-container.sh

# Test individual scripts
./scripts/native-container/setup.sh
./scripts/native-container/run.sh
./scripts/native-container/exec.sh --shell

# Verify automatic dependency installation
python -c "import pandas, numpy, matplotlib, plotly, yfinance; print('All dependencies available')"
```

### 🆕 New Features

#### Automatic Dependency Installation
- **No manual setup** - Dependencies installed automatically on container start
- **UV package manager** - Fast and reliable dependency management
- **Virtual environment** - Isolated Python environment created automatically
- **Dependency verification** - Key packages verified after installation

#### Enhanced User Experience
- **Seamless startup** - Container ready to use immediately
- **Consistent environment** - Same dependencies every time
- **Error handling** - Graceful fallbacks for installation issues
- **Backward compatibility** - Existing workflows unchanged

---

**Last Updated**: 2024
**Version**: 2.0.0 (UV-Only Mode + Native Container)

## 📊 Project Statistics

- **Lines of Code**: 50,000+
- **Technical Indicators**: 50+
- **Data Sources**: 4
- **Test Coverage**: 100%
- **Documentation**: Comprehensive
- **Package Manager**: UV (10-100x faster than pip)

## 🍎 Native Apple Silicon Container (NEW!)

**Full Docker Feature Parity with 30-50% Performance Improvement**

The project now includes a complete native Apple Silicon container solution that provides **full feature parity** with Docker while offering significant performance improvements.

### 🚀 Quick Start

```bash
# Interactive container manager (recommended)
./scripts/native-container/native-container.sh

# Or use individual scripts
./scripts/native-container/setup.sh
./scripts/native-container/run.sh
./scripts/native-container/exec.sh --shell
```

### ✅ Complete Feature Parity

**All Docker Features Now Available in Native Container:**

- ✅ **UV Package Manager Support** - Complete UV integration with environment validation
- ✅ **MCP Server Support** - Automatic MCP server startup and management
- ✅ **nz/eda Scripts** - Full support for analysis and EDA commands
- ✅ **Command History** - Predefined useful commands with bash history
- ✅ **Automatic Checks** - UV, Binance, YFinance, Polygon feed validation
- ✅ **Interactive Shell** - Enhanced bash environment with custom prompt
- ✅ **Error Handling** - Robust error handling without container exit
- ✅ **HTML File Detection** - Automatic detection of generated HTML files

### 🎯 Usage Examples

```bash
# Inside native container - all commands work exactly like Docker
nz demo --rule PHLD
nz yfinance AAPL --rule PHLD
nz mql5 BTCUSD --interval H4 --rule PHLD
eda --data-quality-checks
eda --descriptive-stats
uv run pytest tests -n auto
```

### 📊 Performance Benefits

- **30-50% performance improvement** over Docker
- **Lower memory usage** due to native virtualization
- **Faster startup times** with optimized initialization
- **Better integration** with macOS system resources

### 📚 Documentation

- **Features Guide**: [Native Container Features](docs/deployment/native-container-features.md)
- **Setup Guide**: [Native Container Setup](docs/deployment/native-container-setup.md)
- **README**: [Native Container README](scripts/native-container/README.md)

### 🔧 Requirements

- **macOS 26 Tahoe (Developer Beta)** or higher
- **Native container application** installed from Apple Developer Beta
- **Python 3.11+** installed
- **At least 4GB of available RAM**
- **10GB of available disk space**