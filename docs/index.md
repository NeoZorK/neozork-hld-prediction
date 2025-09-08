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
- [Scripts Structure](development/scripts-structure.md) - **NEW**: Utility scripts organization and structure
- [Refactoring Guide](development/REFACTORING_SUMMARY.md) - **NEW**: Code refactoring guidelines and recent improvements
- [Test Reorganization Report](development/TEST_REORGANIZATION_REPORT.md) - **NEW**: Comprehensive report on test files reorganization

### Testing
- [Testing Documentation](testing/index.md) - Comprehensive testing documentation
- [Test Structure](testing/test-structure.md) - **NEW**: Detailed test organization and structure
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
- [Technical Indicators](guides/indicators.md) - Available technical indicators (including new [COT](reference/indicators/sentiment/cot-indicator.md), [Put/Call Ratio](reference/indicators/sentiment/putcallratio-indicator.md), [SuperTrend](reference/indicators/trend/supertrend-indicator.md), [SMA](reference/indicators/trend/sma-indicator.md), [Wave](reference/indicators/trend/wave-indicator.md) with full seaborn mode support)
- [Analysis Tools](guides/analysis-tools.md) - Analysis and visualization tools
- [CLI Interface](guides/cli-interface.md) - Command-line interface usage
- [Batch CSV Processing](guides/batch-csv-processing.md) - **NEW**: Batch processing of CSV folders

### 🎯 SMA Indicator Tutorials (New!)
- [Complete SMA Tutorial](guides/adding-sma-indicator-tutorial.md) - Full implementation guide across all display modes
- [Quick Start Guide](guides/sma-quick-start-guide.md) - Get started with SMA in minutes
- [Practical Examples](guides/sma-practical-examples.md) - Real-world trading scenarios
- [Testing Guide](guides/sma-testing-guide.md) - Comprehensive testing framework
- [Tutorials Summary](guides/sma-tutorials-summary.md) - Complete overview and quick reference

### 🌊 Wave Indicator Tutorials (New!)
- [Complete Wave Tutorial](guides/adding-wave-indicator-tutorial.md) - Advanced dual-system indicator implementation with fast mode support
- [Wave Indicator Documentation](reference/indicators/trend/wave-indicator.md) - Comprehensive technical reference with display modes
- [Wave Implementation Summary](guides/adding-wave-indicator-summary.md) - Quick implementation overview
- [Wave Testing and Fixes](guides/wave-indicator-fixes-summary.md) - Testing framework and bug fixes
- [Wave Fast Mode Support](guides/wave-indicator-fast-mode-support.md) - ⭐ **NEW** Fast mode implementation details
- [Wave Fast-Fastest Parity](guides/wave-indicator-fast-fastest-parity-final-summary.md) - ⭐ **NEW** Visual parity implementation
- [Wave MPL Color Changes](guides/wave-mpl-color-changes.md) - ⭐ **NEW** MPL mode color customization for prime rule
- [Wave Prime Rule Fix](guides/wave-prime-rule-fix-all-modes.md) - ⭐ **NEW** Global trading rule fixes across all display modes
- [Wave Seaborn Mode](guides/wave-indicator-seaborn-mode.md) - ⭐ **NEW** Complete Wave indicator support for seaborn mode (-d sb)
- [Wave Seaborn Integration Summary](guides/wave-seaborn-integration-summary.md) - ⭐ **NEW** Technical implementation summary for seaborn mode
- [Wave Terminal Mode](guides/wave-indicator-terminal-mode.md) - ⭐ **NEW** Complete Wave indicator support for terminal mode (-d term)
- [Wave Terminal Signals Fix](development/WAVE_TERMINAL_SIGNALS_IMPLEMENTATION.md) - ⭐ **NEW** Signal display logic fixes for terminal mode

### Reference
- [API Reference](reference/index.md) - Complete API documentation
- [Configuration](reference/configuration.md) - Configuration options
- [MCP Server](reference/mcp-servers/README.md) - Model Context Protocol server
- [Advanced Metrics](reference/advanced-metrics.md) - Advanced analysis metrics
- [Plotting Reference](reference/plotting/) - **UPDATED**: Enhanced plotting documentation with refactored dual chart fast
- [COT Indicator](reference/indicators/sentiment/cot-indicator.md) - **NEW**: Sentiment indicator documentation
- [Put/Call Ratio Indicator](reference/indicators/sentiment/putcallratio-indicator.md) - **NEW**: Sentiment indicator documentation
- [SuperTrend Indicator](reference/indicators/trend/supertrend-indicator.md) - **NEW**: Trend indicator documentation
- [SMA Indicator](reference/indicators/trend/sma-indicator.md) - **NEW**: Simple Moving Average documentation

### Interactive ML Trading System
- [Interactive ML Trading System](interactive/index.md) - **NEW**: Comprehensive interactive system for ML trading strategy development
- [Interactive System README](interactive/README.md) - **NEW**: Complete system overview and quick start guide
- [Interactive System README Complete](interactive/README_COMPLETE.md) - **NEW**: Comprehensive implementation plan and architecture details
- [Strategic Plan (English)](interactive/INTERACTIVE_ML_TRADING_STRATEGY_PLAN_EN.md) - **NEW**: Complete strategic plan for robust profitable ML trading strategies
- [Стратегический План (Русский)](interactive/INTERACTIVE_ML_TRADING_STRATEGY_PLAN_RU.md) - **NEW**: Полный стратегический план для робастных прибыльных ML торговых стратегий
- [Next Steps Plan](interactive/next-steps-plan.md) - **NEW**: Production development roadmap and implementation plan
- [Phase 4 Completion Summary](interactive/PHASE4_COMPLETION_SUMMARY.md) - **NEW**: Final completion summary for Phase 4 Advanced Features

### Business Plans
- [Commercialization Plan (English)](business/commercialization-plan-en.md) - **NEW**: Comprehensive commercialization strategy for SaaS platform
- [План Коммерциализации (Русский)](business/commercialization-plan-ru.md) - **NEW**: Комплексная стратегия коммерциализации для SaaS платформы
- [Pocket Hedge Fund Launch Guide](business/POCKET_HEDGE_FUND_LAUNCH.md) - **NEW**: Complete launch instructions and implementation guide
- [SaaS Platform Launch Guide](business/SAAS_PLATFORM_LAUNCH.md) - **NEW**: Comprehensive SaaS platform launch guide
- [Pocket Hedge Fund README](business/pocket-hedge-fund-readme.md) - **NEW**: Technical documentation for Pocket Hedge Fund
- [SaaS Platform README](business/saas-platform-readme.md) - **NEW**: Technical documentation for SaaS platform

### Release Notes
- [Release Notes](release-notes/index.md) - **NEW**: Complete release history and migration guides
- [v0.6.0 Release](release-notes/v0.6.0-release-summary.md) - **NEW**: Latest release with documentation updates

### Documentation Updates
- [v0.6.0 Documentation Update Summary](meta/DOCUMENTATION_UPDATE_V0.6.0_SUMMARY.md) - **NEW**: Comprehensive documentation update report

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

### Interactive ML Trading System
- **Interactive Menu System**: Modern, colorful user interface with progress indicators
- **Advanced ML/DL**: Apple MLX integration, Deep Reinforcement Learning, Ensemble methods
- **Risk Management**: Monte Carlo simulations, VaR/CVaR, Dynamic position sizing
- **Multi-Exchange Trading**: CEX and DEX integration with Web3 support
- **Real-time Monitoring**: Prometheus/Grafana metrics and intelligent alerting

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

# Wave indicator with seaborn mode
nz csv --csv-file data/mn1.csv --point 50 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d sb

# Batch convert CSV folder
nz csv --csv-folder mql5_feed --point 0.00001
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