# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

NeoZork HLD Prediction is a **financial analysis platform** featuring advanced technical indicators, UV package management, and multi-environment deployment (Docker, Native containers, Local). The platform provides comprehensive technical indicator calculations with 50+ indicators across momentum, oscillators, trend, volatility, volume, and sentiment analysis.

## Development Commands

### Package Management (UV-Based)
This project exclusively uses **UV package manager** for 10-100x faster dependency management:

```bash
# Install dependencies
uv pip install -r requirements.txt

# Install specific packages
uv pip install pandas numpy

# Run analysis with UV
uv run run_analysis.py demo --rule PHLD

# Run tests with multithreading
uv run pytest tests -n auto

# Create virtual environment
uv venv

# List installed packages
uv pip list
```

### Build and Run Commands

```bash
# Docker environment (recommended for most platforms)
docker-compose up -d
docker-compose exec neozork uv run run_analysis.py demo --rule PHLD

# Native Apple Silicon container (macOS 26+)
./scripts/native-container/native-container.sh

# Local development
uv run run_analysis.py demo --rule PHLD
uv run run_analysis.py yfinance AAPL --rule RSI
uv run run_analysis.py interactive
```

### Testing

```bash
# Run all tests (multithreaded)
uv run pytest tests -n auto

# Run specific test categories
uv run pytest tests/calculation/ -n auto
uv run pytest tests/cli/ -n auto
uv run pytest tests/docker/ -n auto

# Run with coverage
uv run pytest tests/ --cov=src -n auto

# Check UV status
python scripts/check_uv_mode.py --verbose

# Test GitHub Actions locally (without Docker downloads)
act -n  # Dry run
act -n -W .github/workflows/docker-build.yml
act -l  # List workflows
```

### Linting and Code Quality

```bash
# Dead code analysis (basic)
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all

# Advanced dead code analysis
./scripts/analysis/dead-code/run_advanced_analysis.sh --interactive

# Dependency testing analysis
./scripts/analysis/dead-code/run_dependency_test.sh --dry-run
```

### MCP Server Operations

```bash
# Start MCP server
python start_mcp_server.py
# Or inside container:
mcp-start

# Check MCP server status
python scripts/check_mcp_status.py
# Or inside container:
mcp-check
```

## Architecture Overview

### Core Structure
```
src/
├── cli/                 # Command-line interface and argument parsing
├── calculation/         # Technical indicator calculations (50+ indicators)
├── data/               # Data acquisition from multiple sources
├── plotting/           # Multiple plotting backends (Plotly, mplfinance, terminal)
├── export/             # Data export (Parquet, CSV, JSON)
├── workflow/           # Main orchestration logic
├── utils/              # Utilities and Docker browser patching
├── common/             # Shared constants and logging
└── eda/                # Exploratory data analysis tools
```

### Data Flow Architecture
1. **Data Acquisition** (`src/data/`) - Fetches from YFinance, Polygon, Binance, MQL5, CSV
2. **Point Size Determination** (`src/utils/`) - Calculates appropriate scaling for indicators
3. **Indicator Calculation** (`src/calculation/`) - Applies 50+ technical indicators with parameter parsing
4. **Plotting Generation** (`src/plotting/`) - Multi-backend plotting (fastest, plotly, mplfinance, seaborn, terminal)
5. **Export** (`src/export/`) - Saves results in multiple formats
6. **Reporting** (`src/workflow/`) - Generates comprehensive analysis summaries

### Multi-Environment Support
- **Docker Mode**: Automatic webbrowser patching for containerized environments
- **Native Container**: Apple Silicon optimized containers with full Docker parity
- **Local Development**: UV-based dependency management with fallbacks
- **Environment Detection**: Automatic detection via `IN_DOCKER` flag and `/.dockerenv`

### Technical Indicator System
The platform supports **50+ technical indicators** organized by category:
- **Momentum**: MACD, Stochastic
- **Oscillators**: RSI, CCI with variants (RSI_MOM, RSI_DIV)
- **Trend**: EMA, ADX, SAR, **SuperTrend**
- **Volatility**: ATR, Bollinger Bands
- **Volume**: OBV, VWAP
- **Sentiment**: Fear & Greed, **COT**, Put/Call Ratio
- **Predictive**: HMA, Time Series Forecast
- **Support/Resistance**: Pivot Points, Fibonacci

### Parameter System
Indicators support flexible parameter passing:
```bash
# Format: indicator:param1,param2,param3,param4
uv run run_analysis.py show csv mn1 --rule rsi:14,30,70,open
uv run run_analysis.py show csv mn1 --rule supertrend:10,3.0,close
uv run run_analysis.py show csv mn1 --rule feargreed:14,close
```

### Plotting Backend System
Multiple plotting backends with automatic fallbacks:
- **fastest**: Plotly+Dask+Datashader (default, best for large datasets)
- **plotly**: Interactive HTML plots
- **mpl/mplfinance**: Static financial charts
- **seaborn**: Statistical visualizations
- **term**: Terminal ASCII charts (Docker-friendly)

Docker environments automatically force terminal mode for compatibility.

### Testing Architecture
- **Adaptive Testing**: Tests work in both Docker and local environments
- **Multithreaded**: Uses pytest-xdist for parallel execution
- **Environment-Specific**: Separate test suites for Docker vs native container vs local
- **CI/CD Integration**: GitHub Actions with Act local testing support

## Development Guidelines

### Rule System
The codebase uses a `TradingRule` enum system for indicators. When adding new indicators:
1. Add to `rule_aliases_map` in `src/calculation/indicator_calculation.py`
2. Update `TradingRule` enum in `src/common/constants.py`
3. Implement calculation logic in appropriate module under `src/calculation/`

### Data Sources Integration
New data sources should follow the pattern in `src/data/data_acquisition.py`:
1. Implement fetch function with error handling
2. Return standardized OHLCV DataFrame with DatetimeIndex
3. Add caching support via Parquet files
4. Include data validation and point size estimation

### Environment Detection Pattern
Use the established pattern for environment detection:
```python
IN_DOCKER = os.environ.get('DOCKER_CONTAINER', False) or os.path.exists('/.dockerenv')
```

### Volume-Based Indicators
Special handling is required for volume-based indicators (OBV, VWAP, COT, PutCallRatio) - they preserve the `Volume` column instead of renaming to `TickVolume`.

### MCP Integration
The project includes MCP (Model Context Protocol) server integration for IDE enhancement. The server configuration is in `.cursor/settings.json` with Python path and environment variables properly configured.

### Error Handling
Use the structured logging system from `src.common.logger` with appropriate error levels and rich console formatting for user-friendly output.

## Key Files

- `run_analysis.py` - Main entry point with comprehensive CLI
- `nz` - Universal script that works in Docker/local environments  
- `eda` - Data exploration and quality checking script
- `src/workflow/workflow.py` - Main orchestration logic
- `src/calculation/indicator_calculation.py` - Core indicator calculation dispatcher
- `src/cli/cli_show_mode.py` - "Show" mode for data inspection
- `neozork_mcp_server.py` - MCP server for IDE integration

## Testing Strategy

Tests are organized by functionality and environment:
- `tests/calculation/` - Indicator calculation tests
- `tests/cli/` - Command-line interface tests  
- `tests/docker/` - Docker-specific functionality
- `tests/eda/` - Data analysis tests
- `tests/native-container/` - Native container tests

The testing framework automatically adapts to the runtime environment and uses parallel execution for efficiency.
