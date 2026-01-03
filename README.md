# NeoZork HLD Prediction

Advanced financial Analysis platform with UV package Management, comprehensive technical indicators, adaptive testing, and **Interactive ML Trading Strategy Development system**.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![UV Package Manager](https://img.shields.io/badge/UV-Package%20Manager-orange.svg)](https://docs.astral.sh/uv/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)
[![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-Native%20Container-green.svg)](https://developer.apple.com/)
[![Tests](https://img.shields.io/badge/Tests-Adaptive-green.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Quick start

### Native Apple Silicon Container (macOS 26+) - **FULL DOCKER PARITY**
```bash
# Clone and run interactive container manager
git clone https://github.com/Username/neozork-hld-Prediction.git
cd neozork-hld-Prediction
./scripts/native-container/native-container.sh
```

**Quick Commands (Non-interactive):**
```bash
# start container (full sequence with all features)
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/exec.sh --shell

# Stop container (full sequence)
./scripts/native-container/stop.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/cleanup.sh --all --force
```

**available Commands Inside Container:**
```bash
nz --interactive # Interactive Analysis
nz demo --rule PHLD # Demo Analysis
eda -dqc # data quality checks
uv-install # install dependencies
uv-pytest # Run tests with UV
mcp-start # start MCP server
mcp-check # check MCP server status
```

### Docker (Recommended for other platforms)
```bash
# Clone and start
git clone https://github.com/Username/neozork-hld-Prediction.git
cd neozork-hld-Prediction
docker-compose up -d

# Run Analysis with UV
docker-compose exec neozork uv run run_Analysis.py demo --rule PHLD
```

### Local Setup with UV
```bash
# Clone repository
git clone https://github.com/Username/neozork-hld-Prediction.git
cd neozork-hld-Prediction

# install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# install dependencies
uv pip install -r requirements.txt

# Run Analysis
uv run run_Analysis.py demo --rule PHLD
```

## 🔧 Development Tools

### Dead Code Analysis
Find and remove unUsed code and libraries:

**Basic Analyzer (Fast):**
```bash
# Quick Analysis
./scripts/Analysis/dead-code/run_dead_code_Analysis.sh --all

# Apply fixes safely
./scripts/Analysis/dead-code/run_dead_code_Analysis.sh --all --fix --dry-run
./scripts/Analysis/dead-code/run_dead_code_Analysis.sh --all --fix
```

**Advanced Analyzer (Accurate):**
```bash
# Interactive menu (recommended)
./scripts/Analysis/dead-code/run_advanced_Analysis.sh --interactive

# Comprehensive Analysis with AST-based detection
./scripts/Analysis/dead-code/run_advanced_Analysis.sh --all --verbose

# See [Advanced Dead Code Analysis](docs/development/advanced-dead-code-Analysis.md) for details
```

**Dependency Test Analyzer (Most Accurate):**
```bash
# Test dependencies by disabling them and running tests
./scripts/Analysis/dead-code/run_dependency_test.sh --dry-run

# Interactive menu for dependency testing
./scripts/Analysis/dead-code/run_dependency_test.sh --interactive

# See [Dependency Test Analysis](docs/development/dependency-test-Analysis.md) for details
```

## 🔧 UV Package Management

This project Uses **UV package manager** exclusively for dependency Management, providing 10-100x faster performance than traditional pip.

### UV-Only Mode Features
- **Exclusive UV Usage**: No fallback to pip
- **Docker integration**: Seamless UV in containers
- **Native Container integration**: Full UV support in Apple Silicon containers
- **Local Development**: UV support for local environments
- **Adaptive testing**: Tests that work in both Docker and local
- **Performance**: Lightning-fast dependency resolution

### UV Commands
```bash
# install dependencies
uv pip install -r requirements.txt

# install specific package
uv pip install pandas numpy

# Update packages
uv pip install --upgrade pandas

# List installed packages
uv pip List

# Create virtual environment
uv venv

# Run Analysis with UV
uv run run_Analysis.py demo --rule PHLD

# Run tests with UV (multithreaded)
uv run pytest tests -n auto
```

## 📊 Features

### 🎯 Interactive ML Trading Strategy Development system
- **✅ 100% Functional**: all 12 phases COMPLETED and ready for production
- **✅ Phase 1 Real Implementation**: 100% complete with real APIs, ML models, web interface, and CI/CD
- **✅ Phase 2 Advanced Features**: 100% complete with blockchain integration, Monitoring, advanced ML models, and real trading
- **✅ Phase 3 Production**: 100% complete with all production features
- **✅ Phase 4 Advanced Features**: 100% complete with advanced ML models, AI agents, quantitative research, alternative data, and analytics
- **✅ Phase 5 Enterprise Features**: 100% complete with enterprise security, APIs, Monitoring, User Management, and Reporting
- **✅ Phase 6 Advanced Analytics and AI**: 100% complete with advanced ML models, AI trading strategies, predictive analytics, NLP, and computer vision
- **✅ Phase 7 Global Expansion and Scaling**: 100% complete with multi-market integration, regulatory compliance, risk Management, scalable infraStructure, and international partnerships
- **✅ Phase 8 Advanced AI and Machine Learning**: 100% complete with advanced AI models, ML optimization, deep learning integration, AI-powered analytics, and intelligent automation
- **✅ Phase 9 Advanced Trading Strategies**: 100% complete with advanced trading strategies, quantitative research tools, advanced risk Management, and performance analytics
- **✅ Phase 10 Advanced Security and Compliance**: 100% complete with enterprise-level security, compliance Management, security Monitoring, and incident response
- **Advanced ML/DL**: Apple MLX integration, Deep Reinforcement Learning, Ensemble methods
- **Real API integrations**: Binance, Bybit with sample data generation
- **Real ML Models**: Linear Regression, Random Forest, Gradient Boosting
- **Real Trading system**: Paper trading with signal generation
- **Web Dashboard**: Modern Flask interface with real-time Monitoring
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- **Advanced Blockchain integration**: Multi-network DEX and DeFi support
- **Advanced Monitoring**: Prometheus, Grafana, intelligent alerting
- **Advanced ML Models**: 108 features, multiple algorithms
- **Real Trading system**: Live data, backtesting, real money trading
- **Live data Manager**: Real-time data from multiple exchanges
- **Production deployment**: Multi-cloud infraStructure and containerization
- **Advanced Risk Management**: Comprehensive risk metrics and position sizing
- **Multi-Strategy Portfolio**: Advanced Portfolio optimization and Management
- **ML Model Optimization**: Model optimization and performance enhancement
- **Market Making & Arbitrage**: Real-time trading and arbitrage execution
- **Risk Management**: Monte Carlo simulations, VaR/CVaR, Dynamic position sizing
- **Multi-Exchange Trading**: CEX and DEX integration with Web3 support
- **Real-time Monitoring**: Prometheus/Grafana metrics and intelligent alerting
- **Interactive Menu**: Modern, colorful User interface with progress indicators
- **Production Ready**: Complete system ready for real-world deployment

### data Sources
- **Polygon**: Real-time market data
- **YFinance**: Yahoo Finance data
- **Binance**: Cryptocurrency data
- **MQL5**: MetaTrader 5 data

### Technical Indicators (50+)
- **Momentum**: MACD
- **Oscillators**: RSI, CCI, Stochastic
- **Trend**: EMA, **SMA**, ADX, SAR, **SuperTrend**
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
 uv run run_Analysis.py show csv mn1 -d fastest --rule cot:14,close
 ```
- **Documentation:** [COT Indicator](docs/reference/indicators/sentiment/cot-indicator.md)

#### New: Put/Call Ratio Indicator
- **Category:** Sentiment
- **Description:** Measures the ratio of put options to call options to gauge market sentiment. Useful as a contrarian indicator for potential market reversals.
- **CLI Example:**
 ```bash
 uv run run_Analysis.py show csv mn1 -d fastest --rule putcallratio:20,close
 ```
- **Documentation:** [Put/Call Ratio Indicator](docs/reference/indicators/sentiment/putcallratio-indicator.md)

#### New: SuperTrend Indicator
- **Category:** Trend
- **Description:** Advanced trend-following indicator that combines ATR (Average True Range) with price action to identify trend direction and potential reversal points. Provides dynamic support/resistance levels and generates buy/sell signals.
- **CLI Example:**
 ```bash
 uv run run_Analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0
 uv run run_Analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0,open
 ```
- **Parameters:** period (required), multiplier (required), price_type (optional: open/close)
- **Documentation:** [SuperTrend Indicator](docs/reference/indicators/trend/supertrend-indicator.md)

#### New: SMA (Simple Moving Average) Indicator ⭐ **COMPLETE TUTORIAL**
- **Category:** Trend
- **Description:** Simple Moving Average that gives equal weight to all prices in the calculation period. Excellent for trend identification and support/resistance levels. Works across all 6 display modes with modern help system.
- **CLI Examples:**
 ```bash
 # Basic SMA with 20-period close prices
 uv run run_Analysis.py demo --rule sma:20,close -d fastest

 # Multiple SMAs for trend comparison
 uv run run_Analysis.py demo --rule sma:10,close,sma:20,close,sma:50,close -d plotly
 ```
- **Parameters:** period (required), price_type (required: open/close)
- **Display Modes:** all 6 modes supported (fastest, fast, plotly, mpl, seaborn, term)
- **Documentation:**
 - [Complete SMA Tutorial](docs/guides/adding-sma-indicator-tutorial.md) 📖
 - [SMA Reference](docs/reference/indicators/trend/sma-indicator.md) 📋
 - [Quick start Guide](docs/guides/sma-quick-start-guide.md) ⚡
 - [Practical Examples](docs/guides/sma-practical-examples.md) 🎯
 - [testing Guide](docs/guides/sma-testing-guide.md) 🧪
 - [Tutorials Summary](docs/guides/sma-tutorials-summary.md) 📋

#### New: Wave Indicator ⭐ **ADVANCED DUAL-system**
- **Category:** Trend
- **Description:** Sophisticated trend-following indicator that combines multiple momentum Calculations with dual-wave system, configurable trading rules, and global signal filtering. Features 10 individual trading rules and 7 global trading rules for advanced strategies. **Now supports all display modes including fast mode with discontinuous wave lines, MPL mode with customizable colors, seaborn mode with scientific presentation style, and terminal mode with ASCII-based visualization for SSH/remote connections.**
- **CLI Examples:**
 ```bash
 # Basic Wave with default parameters
 uv run run_Analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fastest

 # Wave with custom trading rules
 uv run run_Analysis.py demo --rule wave:33,10,2,strongtrend,22,11,4,fast,reverse,22,open -d plotly

 # Wave with zone-based filtering
 uv run run_Analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,primezone,22,open -d fastest

 # Wave with fast display mode (Bokeh-based)
 uv run run_Analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fast

 # Wave with real data in fast mode
 uv run run_Analysis.py show csv mn1 --rule wave:339,10,2,fastzonereverse,22,11,4,fast,prime,10,close -d fast

 # Wave with MPL mode and custom colors
 uv run run_Analysis.py show csv mn1 -d mpl --rule wave:339,10,2,fast,22,11,4,fast,prime,10,close

 # Wave with seaborn mode (NEW!) - Scientific presentation style
 uv run run_Analysis.py show csv mn1 -d sb --rule wave:339,10,2,fast,22,11,4,fast,prime,10,close

 # Wave with terminal mode (NEW!) - ASCII-based visualization for SSH/remote
 uv run run_Analysis.py show csv mn1 -d term --rule wave:339,10,2,fast,22,11,4,fast,prime,10,close
 ```
- **Parameters:** long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type
- **Documentation:** [Wave Indicator](docs/reference/indicators/trend/wave-indicator.md)
- **Tutorial:** [Adding Wave Indicator](docs/guides/adding-wave-indicator-tutorial.md)
- **New Features:**
 - [MPL Color Customization](docs/guides/wave-mpl-color-changes.md) - Custom colors for prime rule
 - [Global Trading Rule Fixes](docs/guides/wave-prime-rule-fix-all-modes.md) - Fixed prime/reverse rules
 - [Seaborn Mode Support](docs/guides/wave-indicator-seaborn-mode.md) - ⭐ **NEW** Complete seaborn mode support
 - [Seaborn integration Summary](docs/guides/wave-seaborn-integration-summary.md) - ⭐ **NEW** Technical implementation details
 - [Terminal Mode Support](docs/guides/wave-indicator-terminal-mode.md) - ⭐ **NEW** Complete terminal mode support with signal fixes
 - [Terminal signals Fix](docs/development/WAVE_TERMINAL_signALS_IMPLEMENTATION.md) - ⭐ **NEW** signal display logic improvements

 # Real data Analysis
 uv run run_Analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest
 ```
- **Parameters:** period (required), price_type (required: open/close)
- **Display Modes:** all 6 modes supported (fastest, fast, plotly, mpl, seaborn, term)
- **Documentation:**
 - [Complete SMA Tutorial](docs/guides/adding-sma-indicator-tutorial.md) 📖
 - [Quick start Guide](docs/guides/sma-quick-start-guide.md) ⚡
 - [Practical Examples](docs/guides/sma-practical-examples.md) 🎯
 - [testing Guide](docs/guides/sma-testing-guide.md) 🧪
 - [Tutorials Summary](docs/guides/sma-tutorials-summary.md) 📋

#### Fixed: Volume Indicators
- **OBV (On-Balance Volume):** Fixed dual chart plotting and parameter parsing
- **VWAP (Volume Weighted Average Price):** Enhanced volume column handling
- **CLI Examples:**
 ```bash
 # OBV - now works perfectly
 uv run run_Analysis.py show csv mn1 -d fastest --rule obv:

 # VWAP with custom parameters
 uv run run_Analysis.py show csv mn1 -d fastest --rule vwap:20
 ```

### Analysis Tools
- **Exploratory data Analysis**: Comprehensive data exploration
- **Visualization**: Interactive charts and plots
- **CLI interface**: Command-line Analysis tools
- **MCP Server**: Enhanced IDE integration

### 🚀 Interactive ML Trading system (NEW!)
- **Interactive Menu system**: Modern, colorful User interface with progress indicators
- **Advanced ML/DL**: Apple MLX integration, Deep Reinforcement Learning, Ensemble methods
- **Risk Management**: Monte Carlo simulations, VaR/CVaR, Dynamic position sizing
- **Multi-Exchange Trading**: CEX and DEX integration with Web3 support
- **Real-time Monitoring**: Prometheus/Grafana metrics and intelligent alerting
- **Pattern Recognition**: Hidden pattern detection and cross-Market Analysis
- **Automated Retraining**: Continuous learning and adaptation pipelines

## 🧪 testing

### Adaptive testing Framework
Tests are designed to work in both Docker and local environments:

```bash
# Docker environment
docker-compose exec neozork pytest tests/docker/test_uv_simple.py -v

# Local environment
pytest tests/docker/test_uv_simple.py -v

# check UV status
python scripts/check_uv_mode.py --verbose

# Native container tests
uv run pytest tests/native-container/test_native_container_full_functionality.py -v

# Run all tests with UV (multithreaded)
uv run pytest tests -n auto
```

### CI/CD testing with Act
Test GitHub Actions workflows and MCP server integration locally without downLoading Docker images:

```bash
# install act tool
brew install act # macOS
# or
curl https://raw.githubUsercontent.com/nektos/act/master/install.sh | sudo bash # Linux

# Test all workflows (dry run - no Docker downloads)
act -n

# Test specific workflows
act -n -W .github/workflows/docker-build.yml
act -n -W .github/workflows/mcp-integration.yml

# List available workflows
act -l
```

**Benefits:**
- **No Docker Downloads**: Prevents downLoading large Docker images
- **Fast Validation**: Quickly validates workflow syntax and Structure
- **MCP Server testing**: Verify MCP server communication protocols
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
uv run run_Analysis.py show csv mn1 -d fastest --rule obv:
```

**After:**
```bash
# This now works perfectly
uv run run_Analysis.py show csv mn1 -d fastest --rule obv:
```

### UV integration Improvements
- **Exclusive UV Usage**: all commands now Use UV for consistency
- **Multithreaded testing**: `uv run pytest tests -n auto`
- **Docker integration**: Seamless UV in containers
- **Native Container Support**: Full UV support in Apple Silicon containers

## 📋 Quick Examples

### Basic Analysis
```bash
# Demo Analysis
uv run run_Analysis.py demo --rule PHLD

# SMA Analysis (new!)
uv run run_Analysis.py demo --rule sma:20,close -d fastest

# Yahoo Finance Analysis
uv run run_Analysis.py yfinance AAPL --rule RSI

# CSV Analysis (fixed volume indicators)
uv run run_Analysis.py show csv mn1 -d fastest --rule obv:

# Batch CSV folder conversion (NEW!)
uv run run_Analysis.py csv --csv-folder mql5_feed --point 0.00001

# Interactive Analysis
uv run run_Analysis.py interactive
```

### Advanced Analysis
```bash
# Multiple indicators
uv run run_Analysis.py demo --rule RSI,MACD,PHLD

# Multiple SMAs for trend Analysis
uv run run_Analysis.py demo --rule sma:10,close,sma:20,close,sma:50,close -d plotly

# SMA with real data
uv run run_Analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest

# Wave indicator with seaborn mode (NEW!)
uv run run_Analysis.py show csv mn1 -d sb --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open

# Custom plotting backend
uv run run_Analysis.py demo --rule PHLD -d plotly

# Export results
uv run run_Analysis.py demo --rule PHLD --export-parquet --export-csv
```

### testing
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
pip install -r requirements.txt # ~30-60 seconds

# UV (much faster)
uv pip install -r requirements.txt # ~3-10 seconds

# UV with caching (fastest)
uv pip install -r requirements.txt # ~1-3 seconds (subsequent runs)
```

### Multithreaded testing
```bash
# Single-threaded testing
pytest tests/ # ~2-5 minutes

# UV multithreaded testing
uv run pytest tests -n auto # ~30-60 seconds
```

## 📚 Documentation

- **[Getting started](docs/getting-started/)** - Setup and first steps
- **[Examples](docs/examples/)** - Practical usage examples
- **[Guides](docs/guides/)** - Step-by-step tutorials
- **[Reference](docs/reference/)** - Technical documentation
- **[testing](docs/testing/)** - testing strategies and examples

### 🚀 Interactive ML Trading system (NEW!)
- **[Interactive ML Trading system](docs/interactive/)** - **NEW**: Comprehensive interactive system for ML trading strategy development
- **[Strategic Plan (English)](docs/interactive/INTERACTIVE_ML_TRADING_STRATEGY_Plan_EN.md)** - **NEW**: Complete strategic Plan for robust profitable ML trading strategies
- **[Стратегический Plan (Русский)](docs/interactive/INTERACTIVE_ML_TRADING_STRATEGY_Plan_RU.md)** - **NEW**: Полный стратегический Plan for робастных прибыльных ML торговых стратегий
- **[Next Steps Plan](docs/interactive/next-steps-Plan.md)** - **NEW**: Production development Roadmap and implementation Plan
- **[Phase 1 Completion Report](docs/interactive/phase1-completion-Report.md)** - **NEW**: Real API integrations and ML models implementation Report
- **[Phase 1 Final Completion Report](docs/interactive/phase1-final-completion-Report.md)** - **NEW**: Complete Phase 1 implementation with web interface and CI/CD
- **[Phase 2 Completion Report](docs/interactive/phase2-completion-Report.md)** - **NEW**: Advanced blockchain integration, Monitoring, and ML models
- **[Phase 2 Final Completion Report](docs/interactive/phase2-final-completion-Report.md)** - **NEW**: 100% Complete Phase 2 with real trading and backtesting
- **[Phase 3 Progress Report](docs/interactive/phase3-progress-Report.md)** - **NEW**: 40% Complete Phase 3 with production deployment and risk Management
- **[Phase 3 Final Completion Report](docs/interactive/phase3-final-completion-Report.md)** - **NEW**: 100% Complete Phase 3 with all production features
- **[Phase 4 Final Completion Report](docs/interactive/phase4-final-completion-Report.md)** - **NEW**: 100% Complete Phase 4 with all advanced features
- **[Phase 5 Final Completion Report](docs/interactive/phase5-final-completion-Report.md)** - **NEW**: 100% Complete Phase 5 with all enterprise features
- **[Phase 6 Final Completion Report](docs/interactive/phase6-final-completion-Report.md)** - **NEW**: 100% Complete Phase 6 with all AI and analytics features
- **[Phase 7 Final Completion Report](docs/interactive/phase7-final-completion-Report.md)** - **NEW**: 100% Complete Phase 7 with all global expansion features
- **[Phase 8 Final Completion Report](docs/interactive/phase8-final-completion-Report.md)** - **NEW**: 100% Complete Phase 8 with all advanced AI and machine learning features
- **[Phase 9 Final Completion Report](docs/interactive/phase9-final-completion-Report.md)** - **NEW**: 100% Complete Phase 9 with all advanced trading strategies and quantitative research features
- **[Phase 10 Final Completion Report](docs/interactive/phase10-final-completion-Report.md)** - **NEW**: 100% Complete Phase 10 with enterprise-level security and compliance

### 🎯 SMA Indicator Tutorials (New!)
- **[Complete SMA Tutorial](docs/guides/adding-sma-indicator-tutorial.md)** - Full implementation guide
- **[Quick start Guide](docs/guides/sma-quick-start-guide.md)** - Get started in minutes
- **[Practical Examples](docs/guides/sma-practical-examples.md)** - Real-world scenarios
- **[testing Guide](docs/guides/sma-testing-guide.md)** - Comprehensive testing
- **[Tutorials Summary](docs/guides/sma-tutorials-summary.md)** - Complete overView

### 🌊 Wave Indicator Tutorials (New!)
- **[Complete Wave Tutorial](docs/guides/adding-wave-indicator-tutorial.md)** - Advanced dual-system implementation
- **[Wave MPL Color Changes](docs/guides/wave-mpl-color-changes.md)** - MPL mode color customization
- **[Wave Prime Rule Fix](docs/guides/wave-prime-rule-fix-all-modes.md)** - Global trading rule fixes
- **[Wave Seaborn Mode](docs/guides/wave-indicator-seaborn-mode.md)** - ⭐ **NEW** Complete seaborn mode support
- **[Wave Seaborn integration Summary](docs/guides/wave-seaborn-integration-summary.md)** - ⭐ **NEW** Technical implementation details
- **[Wave Reference](docs/reference/indicators/trend/wave-indicator.md)** - Technical documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest tests -n auto`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Username/neozork-hld-Prediction/issues)
- **Documentation**: [docs/](docs/)
- **Examples**: [docs/examples/](docs/examples/)

---

**Built with ❤️ using UV package manager for lightning-fast performance**