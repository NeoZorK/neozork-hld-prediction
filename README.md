# NeoZorK HLD Prediction

**NeoZorK HLD Prediction** helps developers and traders build robust trading algorithms and machine learning prediction models from scratch, with tools for development, deployment, and monitoring. The platform provides a complete workflow from data analysis to model deployment.

Advanced financial analysis platform with UV package management, comprehensive technical indicators, and adaptive testing.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![UV Package Manager](https://img.shields.io/badge/UV-Package%20Manager-orange.svg)](https://docs.astral.sh/uv/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)
[![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-Native%20Container-green.svg)](https://developer.apple.com/)
[![Tests](https://img.shields.io/badge/Tests-Adaptive-green.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Main Project Functionality

This project provides two core components to help build robust trading algorithms and ML prediction models from scratch:

### 📊 **run_analysis.py** - Financial Analysis Engine
- Comprehensive financial data analysis
- Technical indicator calculations
- Data visualization and reporting
- Export capabilities for further analysis

### 🤖 **interactive_system.py** - Interactive ML Development
- Interactive data exploration and analysis
- Automated feature engineering
- Machine learning model development
- Real-time data quality monitoring




## 💰 Support the Project

If you find this project helpful and would like to support the development, consider making a donation:

### Bitcoin (BTC)
**Wallet Address**: `bc1qm0ynz8tk2em3zr8agv5j3550vpm420z3hxdfkq`

[![Bitcoin](https://img.shields.io/badge/Bitcoin-Donate-orange.svg?style=flat&logo=bitcoin)](bitcoin:bc1qm0ynz8tk2em3zr8agv5j3550vpm420z3hxdfkq)

> 💡 **QR Code**: Scan the QR code below or copy the wallet address above to send your donation.

<div align="center">

![Bitcoin QR Code](https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=bc1qm0ynz8tk2em3zr8agv5j3550vpm420z3hxdfkq)

</div>

### Why Support?
- 🚀 **Continuous Development**: Help fund new features and improvements
- 🐛 **Bug Fixes**: Support faster bug resolution and updates
- 📚 **Documentation**: Better documentation and tutorials
- 💡 **New Features**: Development of additional analysis tools
- 🌟 **Community**: Help grow the financial analysis community

---

## 🚀 Quick Start

> ⚠️ **Note**: Docker and Apple Silicon containers are currently on pause due to active ML model development. Please use local setup for now.

### Native Apple Silicon Container
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

### Local Setup with UV (Currently Recommended)
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

### Machine Learning Platform
Advanced ML capabilities with automated feature engineering and integrated EDA:

**Quick Start:**
```bash
# Run interactive system
python scripts/ml/interactive_system.py


**Documentation:** [Complete ML Documentation](docs/ml/index.md)
- [Feature Engineering Guide](docs/ml/feature_engineering_guide.md)
- [ML Module Overview](docs/ml/ml-module-overview.md)
- [EDA Integration Guide](docs/ml/eda_integration_guide.md)

## 🔧 UV Package Management

This project uses **UV package manager** exclusively for dependency management, providing 10-100x faster performance than traditional pip.

### UV-Only Mode Features
- **Exclusive UV Usage**: No fallback to pip
- **Local Development**: UV support for local environments
- **Performance**: Lightning-fast dependency resolution
- **Future Plans**: Container integration will resume after ML model development

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

### Analysis Capabilities
- **Technical Analysis**: Comprehensive financial data analysis
- **Data Visualization**: Interactive charts and plots
- **Export Functions**: Multiple format export capabilities
- **Real-time Processing**: Live data analysis and monitoring















  
  



### Analysis Tools
- **Exploratory Data Analysis**: Comprehensive data exploration
- **Visualization**: Interactive charts and plots
- **CLI Interface**: Command-line analysis tools
- **MCP Server**: Enhanced IDE integration

## 🧪 Testing

### Adaptive Testing Framework
Tests are designed to work in local environments (container support temporarily paused):

```bash
# Local environment (currently recommended)
pytest tests/docker/test_uv_simple.py -v

# Check UV status
python scripts/check_uv_mode.py --verbose

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

### General Improvements
- Enhanced data processing capabilities
- Improved error handling and user feedback
- Better performance optimization
- Streamlined workflow processes

### UV Integration Improvements
- **Exclusive UV Usage**: All commands now use UV for consistency
- **Multithreaded Testing**: `uv run pytest tests -n auto`
- **Local Development**: Optimized for local development environments
- **Future Plans**: Container integration will resume after ML model development

## 📋 Quick Examples

### Basic Analysis
```bash
# Demo analysis
uv run run_analysis.py demo --rule PHLD

# Yahoo Finance analysis
uv run run_analysis.py yfinance AAPL

# CSV analysis
uv run run_analysis.py show csv mn1 -d fastest

# CSV folder processing (NEW!)
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 -d fastest

# CSV folder with mask filtering (NEW!)
uv run run_analysis.py csv --csv-folder mql5_feed EURUSD --point 0.00001
uv run run_analysis.py csv --csv-folder mql5_feed --csv-mask AAPL --point 0.00001
uv run run_analysis.py csv --csv-folder mql5_feed EURUSD --point 0.00001 --export-parquet

# Interactive analysis
uv run run_analysis.py interactive
```

### Advanced Analysis
```bash
# Multiple analysis rules
uv run run_analysis.py demo --rule PHLD

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

- **[Documentation Index](docs/index.md)** - Complete documentation overview
- **[Getting Started](docs/getting-started/)** - Setup and first steps
- **[Guides & Tutorials](docs/guides/)** - Step-by-step tutorials and guides
- **[Reference](docs/reference/)** - Technical documentation
- **[API Documentation](docs/api/)** - API references and data sources
- **[Examples](docs/examples/)** - Practical usage examples
- **[Testing](docs/testing/)** - Testing strategies and examples
- **[Reports](docs/reports/)** - Development reports and status updates



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