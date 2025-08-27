# NeoZork HLD Prediction - Documentation

Welcome to the comprehensive documentation for the NeoZork HLD Prediction project. This project provides advanced financial analysis tools with support for multiple data sources and technical indicators.

## 🚀 Quick Start

### Native Apple Silicon Container (macOS 26+)
```bash
# Clone and run interactive container manager
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction
./scripts/native-container/native-container.sh
```

**Quick Commands (Non-interactive):**
```bash
# Start container (full sequence)
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/exec.sh --shell

# Stop container (full sequence)
./scripts/native-container/stop.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/cleanup.sh --all --force
```

**Interactive Menu Options:**
1. Start Container (Full Sequence) - Smart startup (handles already running containers)
2. Stop Container (Full Sequence)  
3. Show Container Status
4. Help
0. Exit

### Docker Environment (Recommended for other platforms)
```bash
# Build and start the container
docker-compose up

# Run analysis
nz demo --rule PHLD

# Run EDA
eda
```

### Local Environment
```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt

# Run analysis
python run_analysis.py demo --rule PHLD
```

## 📚 Documentation Structure

### 🎯 Getting Started
- **[Getting Started Guide](getting-started/getting-started.md)** - Complete setup instructions
- **[Project Structure](getting-started/project-structure.md)** - Understanding the codebase
- **[UV Setup Guide](getting-started/uv-setup.md)** - UV package manager configuration
- **[Quick Start Native Container](getting-started/QUICK_START_NATIVE_CONTAINER.md)** - Apple Silicon container setup

### 🐳 Containers & Deployment
- **[Container Documentation](containers/index.md)** - Comprehensive container documentation
- **[Native Container](containers/native-container/index.md)** - Apple Silicon optimized container
- **[Docker Container](containers/docker-setup.md)** - Cross-platform container solution
- **[Container Comparison](containers/native-vs-docker-comparison.md)** - Performance and feature comparison
- **[Production Deployment](deployment/index.md)** - Production environment setup

### 🔧 Development
- **[Development Guide](development/index.md)** - Development environment setup and guidelines
- **[Testing Documentation](testing/index.md)** - Comprehensive testing documentation
- **[Code Style & Standards](development/code-style.md)** - Coding standards and conventions
- **[Debugging Guide](development/debugging.md)** - Debugging tools and techniques
- **[Scripts Structure](development/scripts-structure.md)** - Utility scripts organization

### 📊 Features & Analysis
- **[Data Sources](api/data-sources.md)** - Supported financial data sources
- **[Technical Indicators](reference/indicators/)** - Available technical indicators
- **[Analysis Tools](guides/analysis-tools.md)** - Analysis and visualization tools
- **[CLI Interface](guides/cli-interface.md)** - Command-line interface usage
- **[Plotting & Visualization](reference/plotting/)** - Visualization tools and modes

### 🤖 Machine Learning
- **[ML Documentation](ml/index.md)** - Comprehensive machine learning platform
- **[Feature Engineering](ml/feature_engineering_guide.md)** - Automated feature generation
- **[EDA Integration](ml/eda_integration_guide.md)** - Integrated EDA and Feature Engineering
- **[Usage Instructions](ml/USAGE_INSTRUCTIONS.md)** - Comprehensive usage guide

### 📋 Reference
- **[API Reference](reference/index.md)** - Complete API documentation
- **[Configuration](reference/configuration.md)** - Configuration options
- **[MCP Server](reference/mcp-servers/README.md)** - Model Context Protocol server
- **[Advanced Metrics](reference/advanced-metrics.md)** - Advanced analysis metrics

### 📖 Guides & Tutorials
- **[Guides Index](guides/index.md)** - Step-by-step tutorials and guides
- **[Examples](examples/index.md)** - Practical usage examples
- **[Release Notes](release-notes/index.md)** - Release history and migration guides

### 📈 EDA & Analysis
- **[EDA Documentation](eda/index.md)** - Exploratory Data Analysis tools
- **[Time Series Analysis](eda/time-series-analysis.md)** - Time series analysis techniques

### 📋 Reports & Status
- **[Reports Index](reports/index.md)** - Development reports and status updates
- **[Documentation Reorganization Report](reports/DOCUMENTATION_REORGANIZATION_REPORT.md)** - Complete reorganization documentation

## 🎯 Key Features

### UV Package Management
- **UV-Only Mode**: Exclusive use of UV package manager for faster, more reliable dependency management
- **Docker Integration**: Seamless UV integration in Docker containers
- **Native Container Support**: Native Apple Silicon container with 30-50% performance improvement
- **Local Development**: UV support for local development environments
- **Adaptive Testing**: Tests that work in both Docker and local environments

### Financial Analysis
- **Multiple Data Sources**: Polygon, YFinance, Binance, MQL5
- **Technical Indicators**: 50+ indicators including RSI, MACD, Bollinger Bands, SMA, Wave, SuperTrend
- **Real-time Analysis**: Live data processing and analysis
- **Visualization**: Interactive charts and plots across 6 display modes

### Development Tools
- **MCP Server**: Enhanced IDE integration with intelligent autocompletion
- **Comprehensive Testing**: 100% test coverage with pytest
- **Docker Support**: Containerized development and deployment
- **CLI Tools**: Command-line interface for analysis and EDA

## 🧪 Testing

### Docker Environment
```bash
# Run all tests
pytest tests/ -v

# Run UV-specific tests
pytest tests/docker/test_uv_only_mode.py -v

# Run simple tests
pytest tests/docker/test_uv_simple.py -v
```

### Local Environment
```bash
# Run adaptive tests (work in both environments)
pytest tests/docker/test_uv_simple.py -v

# Run comprehensive tests
pytest tests/docker/test_uv_only_mode.py -v

# Run CLI tests
python tests/cli/comprehensive/run_all_cli_tests.py

# Check UV mode
python scripts/check_uv_mode.py --verbose
```

### Test Categories
- **UV-Specific Tests**: Package manager validation
- **Environment Tests**: Docker vs local detection
- **Integration Tests**: End-to-end functionality
- **Performance Tests**: UV vs pip comparison
- **CLI Tests**: Command-line interface validation
- **Native Container Tests**: Full functionality validation

## 📊 Project Structure

```
neozork-hld-prediction/
├── src/                    # Source code
│   ├── calculation/        # Technical indicators
│   ├── data/              # Data acquisition
│   ├── eda/               # Exploratory data analysis
│   ├── plotting/          # Visualization tools
│   ├── ml/                # Machine learning modules
│   └── cli/               # Command-line interface
├── tests/                 # Test suite
│   ├── docker/            # Docker-specific tests
│   ├── ml/                # Machine learning tests
│   └── ...                # Other test categories
├── docs/                  # Documentation
│   ├── getting-started/   # Setup and first steps
│   ├── containers/        # Container documentation
│   ├── development/       # Development guides
│   ├── testing/           # Testing documentation
│   ├── guides/            # Tutorials and guides
│   ├── reference/         # Technical reference
│   ├── ml/                # Machine learning docs
│   ├── api/               # API documentation
│   ├── examples/          # Usage examples
│   └── release-notes/     # Release history
├── scripts/               # Utility scripts
│   ├── mcp/               # MCP server management
│   ├── analysis/          # Analysis and testing
│   ├── utilities/         # Utility and setup
│   ├── demos/             # Demonstration scripts
│   ├── debug/             # Debugging scripts
│   ├── docker/            # Docker-specific scripts
│   └── native-container/  # Native container scripts
├── data/                  # Data storage
└── results/               # Analysis results
```

## 🚀 Quick Examples

### Basic Analysis
```bash
# Run demo analysis
nz demo --rule PHLD

# Analyze specific symbol
nz yfinance AAPL --rule PHLD

# Custom timeframe
nz mql5 EURUSD --interval H4 --rule PHLD

# Wave indicator with seaborn mode
nz csv --csv-file data/mn1.csv --point 50 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d sb
```

### UV Package Management
```bash
# Install dependencies (Docker)
uv-install

# Update dependencies (Docker)
uv-update

# Check UV status
uv-test

# Local UV usage
uv pip install pandas
uv pip list
```

### Development
```bash
# Run tests
pytest tests/ -v

# Check code quality
python scripts/check_uv_mode.py

# Start MCP server
python neozork_mcp_server.py
```

## 📈 Performance

- **UV Package Manager**: 10-100x faster than pip
- **Docker Optimization**: Optimized container builds
- **Native Container**: 30-50% performance improvement on Apple Silicon
- **Caching**: Intelligent caching for data and packages
- **Parallel Processing**: Multi-threaded analysis capabilities

## 🔒 Security

- **Non-root Containers**: Secure Docker execution
- **Package Verification**: UV's built-in security checks
- **Environment Isolation**: Proper environment separation
- **Input Validation**: Comprehensive input sanitization

## 🤝 Contributing

See [Development Guide](development/contributing.md) for contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the relevant documentation sections
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join project discussions on GitHub
- **Testing**: Use the comprehensive test suite for validation

---

**Last Updated**: 2024
**Version**: 2.0.0 (UV-Only Mode)