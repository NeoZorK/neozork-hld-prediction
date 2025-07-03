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

## 📚 Documentation Sections

### Getting Started
- [Getting Started Guide](getting-started/getting-started.md) - Complete setup instructions
- [Project Structure](getting-started/project-structure.md) - Understanding the codebase
- [Installation Guide](getting-started/installation.md) - Step-by-step installation

### Containers
- [Container Documentation](containers/index.md) - **NEW**: Comprehensive container documentation
- [Native Container](containers/native-container/index.md) - Apple Silicon optimized container
- [Docker Container](containers/docker-setup.md) - Cross-platform container solution
- [Container Comparison](containers/native-vs-docker-comparison.md) - Performance and feature comparison

### Development
- [Development Setup](development/setup.md) - Setting up development environment
- [Testing Guide](development/testing.md) - Running tests and validation
- [Code Style](development/code-style.md) - Coding standards and conventions
- [Debugging](development/debugging.md) - Debugging tools and techniques

### Testing
- [Testing Documentation](testing/index.md) - Comprehensive testing documentation
- [UV-Only Mode Tests](testing/docker/uv-only-mode-tests.md) - Docker UV testing
- [CLI Testing](testing/cli/comprehensive-testing.md) - Command-line interface testing

### Deployment
- [Native Container Setup](containers/native-container-setup.md) - Native Apple Silicon container setup
- [Docker Setup](containers/docker-setup.md) - Containerized deployment
- [UV-Only Mode](containers/uv-only-mode.md) - UV package manager configuration
- [Production Deployment](deployment/production.md) - Production environment setup
- [Monitoring](deployment/monitoring.md) - System monitoring and logging

### Features
- [Data Sources](guides/data-sources.md) - Supported financial data sources
- [Technical Indicators](guides/indicators.md) - Available technical indicators (including new [Put/Call Ratio](reference/indicators/sentiment/putcallratio-indicator.md))
- [Analysis Tools](guides/analysis-tools.md) - Analysis and visualization tools
- [CLI Interface](guides/cli-interface.md) - Command-line interface usage

### Reference
- [API Reference](reference/index.md) - Complete API documentation
- [Configuration](reference/configuration.md) - Configuration options
- [MCP Server](reference/mcp-servers/README.md) - Model Context Protocol server
- [Advanced Metrics](reference/advanced-metrics.md) - Advanced analysis metrics
- [Put/Call Ratio Indicator](reference/indicators/sentiment/putcallratio-indicator.md) - **NEW**: Sentiment indicator documentation

## 🔧 Key Features

### UV Package Management
- **UV-Only Mode**: Exclusive use of UV package manager for faster, more reliable dependency management
- **Docker Integration**: Seamless UV integration in Docker containers
- **Native Container Support**: **NEW**: Native Apple Silicon container with 30-50% performance improvement
- **Local Development**: UV support for local development environments
- **Adaptive Testing**: Tests that work in both Docker and local environments

### Financial Analysis
- **Multiple Data Sources**: Polygon, YFinance, Binance, MQL5
- **Technical Indicators**: 50+ indicators including RSI, MACD, Bollinger Bands
- **Real-time Analysis**: Live data processing and analysis
- **Visualization**: Interactive charts and plots

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

### Testing Documentation
- [Testing Documentation](testing/index.md) - Comprehensive testing guide
- [UV-Only Mode Tests](testing/docker/uv-only-mode-tests.md) - Docker UV testing details
- [CLI Testing](testing/cli/comprehensive-testing.md) - CLI testing suite documentation
- [CI/CD Testing](development/ci-cd.md#testing-github-actions-integration-with-act) - GitHub Actions workflow testing with Act
- [MCP Server Testing](reference/mcp-servers/README.md#cicd-testing-with-act) - MCP server integration testing

## 📊 Project Structure

```
neozork-hld-prediction/
├── src/                    # Source code
│   ├── calculation/        # Technical indicators
│   ├── data/              # Data acquisition
│   ├── eda/               # Exploratory data analysis
│   ├── plotting/          # Visualization tools
│   └── cli/               # Command-line interface
├── tests/                 # Test suite
│   ├── docker/            # Docker-specific tests
│   └── ...                # Other test categories
├── docs/                  # Documentation
│   ├── containers/        # Container documentation
│   │   ├── native-container/  # Native container docs
│   │   └── index.md       # Container overview
│   ├── testing/           # Testing documentation
│   │   ├── docker/        # Docker testing docs
│   │   └── cli/           # CLI testing docs
│   └── ...                # Other documentation
├── scripts/               # **REORGANIZED**: Utility scripts
│   ├── mcp/               # MCP server management scripts
│   ├── analysis/          # Analysis and testing scripts
│   ├── utilities/         # Utility and setup scripts
│   ├── demos/             # Demonstration scripts
│   ├── debug/             # Debugging scripts
│   ├── docker/            # Docker-specific scripts
│   └── native-container/  # Native container scripts
├── data/                  # Data storage
└── results/               # Analysis results
```

### Scripts Organization

The `scripts/` directory has been reorganized for better maintainability:

#### **MCP Scripts** (`scripts/mcp/`)
- **neozork_mcp_manager.py** - Unified MCP server manager with autostart and monitoring
- **start_mcp_server_daemon.py** - MCP server daemon startup script
- **check_mcp_status.py** - MCP server status checking and diagnostics
- **test_mcp_server_detection.py** - MCP server detection testing
- **debug_mcp_detection.py** - MCP server detection debugging

#### **Analysis Scripts** (`scripts/analysis/`)
- **analyze_requirements.py** - Python imports analysis and requirements optimization
- **auto_pyproject_from_requirements.py** - Generate pyproject.toml from requirements.txt
- **generate_test_coverage.py** - Test coverage analysis and reporting
- **fix_test_coverage.py** - Test coverage fixes and improvements
- **manage_test_results.py** - Test results management and analysis

#### **Utility Scripts** (`scripts/utilities/`)
- **fix_imports.py** - Fix relative imports in test files
- **setup_ide_configs.py** - IDE configuration setup
- **init_dirs.sh** - Directory structure initialization
- **recreate_csv.py** - CSV file recreation utilities
- **create_test_parquet.py** - Test Parquet file creation
- **check_uv_mode.py** - UV mode verification
- **test_uv_docker.py** - UV Docker integration testing

#### **Demo Scripts** (`scripts/demos/`)
- **demo_universal_metrics.py** - Universal metrics demonstration

#### **Debug Scripts** (`scripts/debug/`)
- **debug_binance.py** - Binance API debugging
- **debug_binance_connection.py** - Binance connection debugging
- **debug_polygon.py** - Polygon API debugging
- **debug_polygon_connection.py** - Polygon connection debugging
- **debug_polygon_resolve.py** - Polygon resolution debugging
- **debug_yfinance.py** - YFinance API debugging
- **examine_parquet.py** - Parquet file examination
- **examine_binance_parquet.py** - Binance Parquet file examination
- **debug_check_parquet.py** - Parquet file checking
- **debug_csv_reader.py** - CSV reader debugging

#### **Container Scripts**
- **Docker Scripts** (`scripts/docker/`) - Docker container testing and workflows
- **Native Container Scripts** (`scripts/native-container/`) - Apple Silicon container management

## 🚀 Quick Examples

### Basic Analysis
```bash
# Run demo analysis
nz demo --rule PHLD

# Analyze specific symbol
nz yfinance AAPL --rule PHLD

# Custom timeframe
nz mql5 EURUSD --interval H4 --rule PHLD
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