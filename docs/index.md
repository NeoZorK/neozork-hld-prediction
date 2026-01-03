# NeoZork HLD Prediction Project Documentation

## 🎯 Project OverView

The NeoZork HLD Prediction project is a comprehensive financial Analysis and Prediction system that provides advanced trading capabilities, machine learning models, and fund Management tools.

## 📊 Current Implementation Status

**Overall Project Status**: 35% Complete

### ✅ **Fully Implemented (Production Ready)**
- **Core Trading InfraStructure** (95%): Technical indicators, data processing, plotting
- **Interactive ML system** (90%): ML models, feature engineering, backtesting
- **Documentation** (85%): Comprehensive documentation and guides

### 🚧 **Partially Implemented (In Development)**
- **Pocket Hedge fund** (15%): Fund Management framework, API endpoints
- **SaaS platform** (20%): Multi-tenancy, billing system
- **Security & Compliance** (60%): Security framework, Monitoring

### ❌ **Not Implemented (Stubs Only)**
- **Real database integration** (0%): No persistent data storage
- **Real Authentication** (0%): No User Authentication system
- **Real Trading Execution** (0%): No actual trade execution
- **Investor Portal** (0%): No User interface

## 🚨 Critical Issues

### High Priority
1. **database integration** - No data persistence
2. **Authentication system** - No User security
3. **Real Trading Execution** - No actual trading
4. **Investor Portal** - No User interface

### Medium Priority
1. **Blockchain integration** - No DeFi features
2. **Strategy Marketplace** - No strategy sharing
3. **Community Features** - No social trading

## 🎯 Development Roadmap

### Phase 1: foundation (Months 1-3)
- Implement database integration
- Implement Authentication system
- Implement real trading execution
- Implement investor portal

### Phase 2: Core Features (Months 4-6)
- Complete fund Management
- Implement strategy marketplace
- Implement community features
- Implement blockchain integration

### Phase 3: Advanced Features (Months 7-9)
- Implement advanced analytics
- Implement mobile app
- Implement advanced AI
- Implement compliance features

## 📈 Success Metrics

### Current State
- **Functional components**: 35%
- **Production Ready**: 15%
- **Test coverage**: 60%
- **Documentation**: 85%

### Target State (6 months)
- **Functional components**: 80%
- **Production Ready**: 60%
- **Test coverage**: 90%
- **Documentation**: 95%

---

*Last updated: 2024-12-19*
*Status: Accurate and up-to-date*

---

## 🚀 Quick start

## 🚀 Quick start

### Native Apple Silicon Container (macOS 26+)
```bash
# Clone and run interactive container manager
git clone https://github.com/Username/neozork-hld-Prediction.git
cd neozork-hld-Prediction
./scripts/native-container/native-container.sh
```

**Quick Commands (Non-interactive):**
```bash
# start container (full sequence)
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/exec.sh --shell

# Stop container (full sequence)
./scripts/native-container/stop.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/cleanup.sh --all --force
```

**Interactive Menu Options:**
1. start Container (Full Sequence) - Smart startup (handles already running containers)
2. Stop Container (Full Sequence)
3. Show Container Status
4. Help
0. Exit

### Docker Environment (Recommended for other platforms)
```bash
# Build and start the container
docker-compose up

# Run Analysis
nz demo --rule PHLD

# Run EDA
eda
```

### Local Environment
```bash
# install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# install dependencies
uv pip install -r requirements.txt

# Run Analysis
python run_Analysis.py demo --rule PHLD
```

## 📚 Documentation Sections

### Getting started
- [Getting started Guide](getting-started/getting-started.md) - Complete setup instructions
- [Project Structure](getting-started/project-Structure.md) - Understanding the codebase
- [installation Guide](getting-started/installation.md) - Step-by-step installation

### 🚀 Run and Test Guides / Run and Test Guides
- [Complete Manual (English)](run-and-test-guides/english/complete-manual-en.md) - **NEW**: Complete run and test manual
- [Complete Manual (Русский)](run-and-test-guides/russian/complete-manual-ru.md) - **NEW**: Complete guide on Launch and testing
- [Quick start (English)](run-and-test-guides/english/quick-start-en.md) - **NEW**: Quick start guide
- [Quick start (Русский)](run-and-test-guides/russian/quick-start-ru.md) - **NEW**: Quick start
- [testing Guide (English)](run-and-test-guides/english/testing-guide-en.md) - **NEW**: Comprehensive testing guide
- [testing Guide (Русский)](run-and-test-guides/russian/testing-guide-ru.md) - **NEW**: guide on testing
- [deployment Guide (English)](run-and-test-guides/english/deployment-guide-en.md) - **NEW**: deployment guide
- [deployment Guide (Русский)](run-and-test-guides/russian/deployment-guide-ru.md) - **NEW**: guide on deployment
- [Troubleshooting](run-and-test-guides/Troubleshooting.md) - **NEW**: Common Issues and solutions
- [FAQ](run-and-test-guides/faq.md) - **NEW**: Frequently Asked Questions

### Containers
- [Container Documentation](containers/index.md) - **NEW**: Comprehensive container documentation
- [Native Container](containers/native-container/index.md) - Apple Silicon optimized container
- [Docker Container](containers/docker-setup.md) - Cross-platform container solution
- [Container Comparison](containers/native-vs-docker-comparison.md) - Performance and feature comparison

### Development
- [Development Setup](development/setup.md) - Setting up development environment
- [Documentation Sync Report](development/DOCUMENTATION_SYNC_FINAL_Report.md) - **NEW**: Complete documentation Synchronization Report
- [testing Guide](development/testing.md) - Running tests and validation
- [Code Style](development/code-style.md) - Coding standards and conventions
- [Debugging](development/debugging.md) - Debugging tools and techniques
- [Scripts Structure](development/scripts-Structure.md) - **NEW**: Utility scripts organization and Structure
- [Refactoring Guide](development/REFACTORING_SUMMARY.md) - **NEW**: Code refactoring guidelines and recent improvements
- [Test Reorganization Report](development/TEST_REorganization_Report.md) - **NEW**: Comprehensive Report on test files reorganization

### testing
- [testing Documentation](testing/index.md) - Comprehensive testing documentation
- [Test Structure](testing/test-Structure.md) - **NEW**: Detailed test organization and Structure
- [UV-Only Mode tests](testing/docker/uv-only-mode-tests.md) - Docker UV testing
- [CLI testing](testing/cli/comprehensive-testing.md) - Command-line interface testing

### deployment
- [Native Container Setup](containers/native-container-setup.md) - Native Apple Silicon container setup
- [Docker Setup](containers/docker-setup.md) - Containerized deployment
- [UV-Only Mode](containers/uv-only-mode.md) - UV package manager configuration
- [Production deployment](deployment/production.md) - Production environment setup
- [Monitoring](deployment/Monitoring.md) - system Monitoring and logging

### Features
- [data Sources](guides/data-sources.md) - Supported financial data sources
- [Technical Indicators](guides/indicators.md) - available Technical indicators (including new [COT](reference/indicators/sentiment/cot-indicator.md), [Put/Call Ratio](reference/indicators/sentiment/putcallratio-indicator.md), [SuperTrend](reference/indicators/trend/supertrend-indicator.md), [SMA](reference/indicators/trend/sma-indicator.md), [Wave](reference/indicators/trend/wave-indicator.md) with full seaborn mode support)
- [Analysis Tools](guides/Analysis-tools.md) - Analysis and visualization tools
- [CLI interface](guides/cli-interface.md) - Command-line interface usage
- [Batch CSV Processing](guides/batch-csv-processing.md) - **NEW**: Batch processing of CSV folders

### 🎯 SMA Indicator Tutorials (New!)
- [Complete SMA Tutorial](guides/adding-sma-indicator-tutorial.md) - Full implementation guide across all display modes
- [Quick start Guide](guides/sma-quick-start-guide.md) - Get started with SMA in minutes
- [Practical Examples](guides/sma-practical-examples.md) - Real-world trading scenarios
- [testing Guide](guides/sma-testing-guide.md) - Comprehensive testing framework
- [Tutorials Summary](guides/sma-tutorials-summary.md) - Complete overView and quick reference

### 🌊 Wave Indicator Tutorials (New!)
- [Complete Wave Tutorial](guides/adding-wave-indicator-tutorial.md) - Advanced dual-system indicator implementation with fast mode support
- [Wave Indicator Documentation](reference/indicators/trend/wave-indicator.md) - Comprehensive Technical reference with display modes
- [Wave Implementation Summary](guides/adding-wave-indicator-summary.md) - Quick implementation overView
- [Wave testing and Fixes](guides/wave-indicator-fixes-summary.md) - testing framework and bug fixes
- [Wave Fast Mode Support](guides/wave-indicator-fast-mode-support.md) - ⭐ **NEW** Fast mode implementation details
- [Wave Fast-Fastest Parity](guides/wave-indicator-fast-fastest-parity-final-summary.md) - ⭐ **NEW** Visual parity implementation
- [Wave MPL Color Changes](guides/wave-mpl-color-changes.md) - ⭐ **NEW** MPL mode color customization for prime rule
- [Wave Prime Rule Fix](guides/wave-prime-rule-fix-all-modes.md) - ⭐ **NEW** Global trading rule fixes across all display modes
- [Wave Seaborn Mode](guides/wave-indicator-seaborn-mode.md) - ⭐ **NEW** Complete Wave indicator support for seaborn mode (-d sb)
- [Wave Seaborn integration Summary](guides/wave-seaborn-integration-summary.md) - ⭐ **NEW** Technical implementation summary for seaborn mode
- [Wave Terminal Mode](guides/wave-indicator-terminal-mode.md) - ⭐ **NEW** Complete Wave indicator support for terminal mode (-d term)
- [Wave Terminal signals Fix](development/WAVE_TERMINAL_signALS_IMPLEMENTATION.md) - ⭐ **NEW** signal display logic fixes for terminal mode

### Reference
- [API Reference](reference/index.md) - Complete API documentation
- [Configuration](reference/configuration.md) - Configuration options
- [MCP Server](reference/mcp-servers/README.md) - Model Context Protocol server
- [Advanced Metrics](reference/advanced-metrics.md) - Advanced Analysis metrics
- [Plotting Reference](reference/plotting/) - **UPDATED**: Enhanced plotting documentation with refactored dual chart fast
- [COT Indicator](reference/indicators/sentiment/cot-indicator.md) - **NEW**: Sentiment indicator documentation
- [Put/Call Ratio Indicator](reference/indicators/sentiment/putcallratio-indicator.md) - **NEW**: Sentiment indicator documentation
- [SuperTrend Indicator](reference/indicators/trend/supertrend-indicator.md) - **NEW**: Trend indicator documentation
- [SMA Indicator](reference/indicators/trend/sma-indicator.md) - **NEW**: Simple Moving Average documentation

### Interactive ML Trading system
- [Interactive ML Trading system](interactive/index.md) - **100% Functional**: Comprehensive interactive system for ML trading strategy development
- [Interactive system README](interactive/README.md) - Complete system overView and Quick start guide
- [Interactive system README Complete](interactive/README_COMPLETE.md) - Comprehensive implementation Plan and architecture details
- [Strategic Plan (English)](interactive/INTERACTIVE_ML_TRADING_STRATEGY_Plan_EN.md) - Complete strategic Plan for robust profitable ML trading strategies
- [Стратегический Plan (Русский)](interactive/INTERACTIVE_ML_TRADING_STRATEGY_Plan_RU.md) - Полный стратегический Plan for робастных прибыльных ML торговых стратегий
- [Next Steps Plan](interactive/next-steps-Plan.md) - Production development Roadmap and implementation Plan
- [Phase 4 Completion Summary](interactive/PHASE4_COMPLETION_SUMMARY.md) - Final completion summary for Phase 4 Advanced Features

### Pocket Hedge fund (80% Functional)
- [Pocket Hedge fund OverView](pocket_hedge_fund/index.md) - **NEW**: Complete platform overView and status
- [API Documentation](pocket_hedge_fund/api/index.md) - **NEW**: Complete REST API reference with examples
- [database Documentation](pocket_hedge_fund/database/index.md) - **NEW**: Full database schema and operations
- [Authentication Guide](pocket_hedge_fund/auth/index.md) - **NEW**: JWT, MFA, and RBAC implementation
- [React Frontend](pocket_hedge_fund/frontend/index.md) - **NEW**: Complete React TypeScript frontend documentation
- [mobile App](mobile_app/index.md) - **NEW**: React Native mobile application with biometric Authentication
- [Admin Panel](admin_panel/index.md) - **NEW**: Vue.js admin panel for SaaS platform Management
- [Fund Management](pocket_hedge_fund/fund_Management/) - Complete fund Management system with database integration
- [API Documentation](pocket_hedge_fund/api/) - RESTful API endpoints for fund operations
- [database Schema](pocket_hedge_fund/database/) - PostgreSQL database schema and models
- [Production deployment](pocket_hedge_fund/deployment/) - Production deployment and configuration
- [Authentication system](pocket_hedge_fund/auth/) - JWT-based Authentication and authorization

### Business Plans
- [commercialization Plan (English)](business/commercialization-Plan-en.md) - Comprehensive commercialization strategy for SaaS platform
- [Plan commercialization (Русский)](business/commercialization-Plan-ru.md) - Comprehensive strategy commercialization for SaaS platform
- [Pocket Hedge fund Launch Guide](business/POCKET_HEDGE_FUND_Launch.md) - **80% Functional**: Complete Launch instructions and implementation guide
### SaaS platform (100% Functional) ⭐ **COMPLETE**
- [SaaS platform OverView](saas/index.md) - **NEW**: Complete Technical platform overView
- [SaaS platform Launch Guide](business/SAAS_platform_Launch.md) - Business Launch guide
- [Frontend Dashboard](saas/frontend/) - **NEW**: React dashboard components
- [Usage Tracking](saas/usage_tracking/) - **NEW**: Advanced analytics system
- [Billing integration](saas/billing/) - **NEW**: Complete Stripe integration

### Release Notes
- [Release Notes](release-notes/index.md) - **NEW**: Complete release history and migration guides
- [v0.6.0 Release](release-notes/v0.6.0-release-summary.md) - **NEW**: Latest release with documentation updates

### Documentation Updates
- [v0.6.0 Documentation Update Summary](meta/DOCUMENTATION_UPDATE_V0.6.0_SUMMARY.md) - **NEW**: Comprehensive documentation update Report

## 🔧 Key Features

### UV Package Management
- **UV-Only Mode**: Exclusive Use of UV package manager for faster, more reliable dependency Management
- **Docker integration**: Seamless UV integration in Docker containers
- **Native Container Support**: **NEW**: Native Apple Silicon container with 30-50% performance improvement
- **Local Development**: UV support for local development environments
- **Adaptive testing**: tests that work in both Docker and local environments

### Financial Analysis
- **Multiple data Sources**: Polygon, YFinance, Binance, MQL5
- **Technical Indicators**: 50+ indicators including RSI, MACD, Bollinger Bands
- **Real-time Analysis**: Live data processing and Analysis
- **Visualization**: Interactive charts and plots

### Interactive ML Trading system
- **Interactive Menu system**: Modern, colorful User interface with progress indicators
- **Advanced ML/DL**: Apple MLX integration, Deep Reinforcement Learning, Ensemble methods
- **Risk Management**: Monte Carlo simulations, VaR/CVaR, Dynamic position sizing
- **Multi-Exchange Trading**: CEX and DEX integration with Web3 support
- **Real-time Monitoring**: Prometheus/Grafana metrics and intelligent alerting

### Development Tools
- **MCP Server**: Enhanced IDE integration with intelligent autocompletion
- **Comprehensive testing**: 100% test coverage with pytest
- **Docker Support**: Containerized development and deployment
- **CLI Tools**: Command-line interface for Analysis and EDA

## 🧪 testing

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

# check UV mode
python scripts/check_uv_mode.py --verbose
```

### Test Categories
- **UV-specific tests**: Package manager validation
- **Environment tests**: Docker vs local detection
- **integration tests**: End-to-end functionality
- **Performance tests**: UV vs pip comparison
- **CLI tests**: Command-line interface validation
- **Native Container tests**: Full functionality validation

### testing Documentation
- [testing Documentation](testing/index.md) - Comprehensive testing guide
- [UV-Only Mode tests](testing/docker/uv-only-mode-tests.md) - Docker UV testing details
- [CLI testing](testing/cli/comprehensive-testing.md) - CLI testing suite documentation
- [CI/CD testing](development/ci-cd.md#testing-github-actions-integration-with-act) - GitHub Actions workflow testing with Act
- [MCP Server testing](reference/mcp-servers/README.md#cicd-testing-with-act) - MCP server integration testing

## 📊 Project Structure

```
neozork-hld-Prediction/
├── src/ # Source code
│ ├── calculation/ # Technical indicators
│ ├── data/ # data acquisition
│ ├── eda/ # Exploratory data Analysis
│ ├── plotting/ # Visualization tools
│ └── cli/ # Command-line interface
├── tests/ # Test suite
│ ├── docker/ # Docker-specific tests
│ └── ... # Other test categories
├── docs/ # Documentation
│ ├── containers/ # Container documentation
│ │ ├── native-container/ # Native container docs
│ │ └── index.md # Container overView
│ ├── testing/ # testing documentation
│ │ ├── docker/ # Docker testing docs
│ │ └── cli/ # CLI testing docs
│ └── ... # Other documentation
├── scripts/ # **REORGANIZED**: Utility scripts
│ ├── mcp/ # MCP server Management scripts
│ ├── Analysis/ # Analysis and testing scripts
│ ├── utilities/ # Utility and setup scripts
│ ├── demos/ # Demonstration scripts
│ ├── debug/ # Debugging scripts
│ ├── docker/ # Docker-specific scripts
│ └── native-container/ # Native container scripts
├── data/ # data storage
└── results/ # Analysis results
```

### Scripts organization

The `scripts/` directory has been reorganized for better maintainability:

#### **MCP Scripts** (`scripts/mcp/`)
- **neozork_mcp_manager.py** - Unified MCP server manager with autostart and Monitoring
- **start_mcp_server_daemon.py** - MCP server daemon startup script
- **check_mcp_status.py** - MCP server status checking and diagnostics
- **test_mcp_server_detection.py** - MCP server detection testing
- **debug_mcp_detection.py** - MCP server detection debugging

#### **Analysis Scripts** (`scripts/Analysis/`)
- **analyze_requirements.py** - Python imports Analysis and requirements optimization
- **auto_pyproject_from_requirements.py** - Generate pyproject.toml from requirements.txt
- **generate_test_coverage.py** - Test coverage Analysis and Reporting
- **fix_test_coverage.py** - Test coverage fixes and improvements
- **manage_test_results.py** - Test results Management and Analysis

#### **Utility Scripts** (`scripts/utilities/`)
- **fix_imports.py** - Fix relative imports in test files
- **setup_ide_configs.py** - IDE configuration setup
- **init_dirs.sh** - Directory Structure initialization
- **recreate_csv.py** - CSV file recreation utilities
- **create_test_parquet.py** - Test Parquet file creation
- **check_uv_mode.py** - UV mode verification
- **test_uv_docker.py** - UV Docker integration testing

#### **Demo Scripts**
- **scripts/demos/demo_universal_metrics.py** - Universal metrics demonstration
- **interactive/advanced_ml/demo_self_learning_engine.py** - Self-Learning Engine demonstration

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
- **Native Container Scripts** (`scripts/native-container/`) - Apple Silicon container Management

## 🚀 Quick Examples

### Basic Analysis
```bash
# Run demo Analysis
nz demo --rule PHLD

# Analyze specific symbol
nz yfinance AAPL --rule PHLD

# Custom Timeframe
nz mql5 EURUSD --interval H4 --rule PHLD

# Wave indicator with seaborn mode
nz csv --csv-file data/mn1.csv --point 50 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d sb

# Batch convert CSV folder
nz csv --csv-folder mql5_feed --point 0.00001
```

### UV Package Management
```bash
# install dependencies (Docker)
uv-install

# Update dependencies (Docker)
uv-update

# check UV status
uv-test

# Local UV usage
uv pip install pandas
uv pip List
```

### Development
```bash
# Run tests
pytest tests/ -v

# check code quality
python scripts/check_uv_mode.py

# start MCP server
python neozork_mcp_server.py
```

## 📈 Performance

- **UV Package Manager**: 10-100x faster than pip
- **Docker Optimization**: Optimized container builds
- **Native Container**: 30-50% performance improvement on Apple Silicon
- **Caching**: Intelligent caching for data and packages
- **Parallel Processing**: Multi-threaded Analysis capabilities

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

- **Documentation**: check the relevant documentation sections
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join project discussions on GitHub
- **testing**: Use the comprehensive test suite for validation

---

**Last Updated**: 2024
**Version**: 2.0.0 (UV-Only Mode)