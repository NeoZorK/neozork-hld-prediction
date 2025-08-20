# Examples

This section provides practical examples and use cases for the NeoZork HLD Prediction project, including UV package management, adaptive testing, and recent fixes.

## 🚀 Quick Examples

### [Quick Examples](quick-examples.md)
Fast start examples to get you up and running quickly.

**Includes:**
- Basic analysis examples
- UV package management
- Docker usage
- First analysis run

### [Usage Examples](usage-examples.md)
Comprehensive workflows and real-world usage scenarios.

**Covers:**
- Data source integration
- Technical indicator usage
- Analysis workflows
- Result interpretation

## 🔧 UV Package Management Examples

### [UV Setup Examples](uv-examples.md) ⭐ **NEW**
Examples of UV package manager configuration and usage.

**Highlights:**
- **Docker UV Integration**: UV usage in containers
- **Local UV Setup**: UV for local development
- **Adaptive Testing**: Tests that work in both environments
- **Performance Comparison**: UV vs traditional pip

### UV Commands Examples
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

# Activate virtual environment
source .venv/bin/activate

# Run analysis with UV
uv run run_analysis.py demo --rule PHLD

# Run tests with UV (multithreaded)
uv run pytest tests -n auto
```

### Docker UV Examples
```bash
# Install dependencies in container
docker-compose exec neozork uv-install

# Update dependencies
docker-compose exec neozork uv-update

# Test UV functionality
docker-compose exec neozork uv-test

# Check UV status
docker-compose exec neozork python scripts/check_uv_mode.py

# Run analysis with UV in container
docker-compose exec neozork uv run run_analysis.py demo --rule PHLD
```

## 📊 Analysis Examples

### [Indicator Examples](indicator-examples.md)
Technical indicator calculation and usage examples.

**Covers:**
- Momentum indicators (MACD, Stochastic)
- Oscillators (RSI, CCI)
- Trend indicators (EMA, ADX, SuperTrend, Wave)
- Volatility indicators (ATR, Bollinger Bands)
- Volume indicators (OBV, VWAP)
- Support & Resistance (Pivot Points, Fibonacci)
- Predictive indicators (HMA, Time Series)
- Probability indicators (Monte Carlo, Kelly)
- Sentiment indicators (Fear & Greed, COT, Put/Call Ratio)

### [Wave Indicator Examples](wave-indicator-examples.md) ⭐ **NEW**
Advanced examples for the complex Wave indicator.

**Highlights:**
- **Complex Parameter Management**: Multiple parameter combinations
- **Real-World Scenarios**: Stock, crypto, and forex analysis
- **Trading Strategies**: Conservative, aggressive, and balanced approaches
- **Market Conditions**: Bull market, bear market, and sector-specific analysis
- **Parameter Optimization**: Guidelines for different market types
- **Troubleshooting**: Common issues and solutions

### Volume Indicators Examples ⭐ **FIXED**
```bash
# OBV (On-Balance Volume) - Fixed dual chart plotting
uv run run_analysis.py show csv mn1 -d fastest --rule obv:

# VWAP (Volume Weighted Average Price)
uv run run_analysis.py show csv mn1 -d fastest --rule vwap:20

# OBV with custom parameters
uv run run_analysis.py show csv mn1 -d fastest --rule obv:20,close
```

### Sentiment Indicators Examples ⭐ **NEW**
```bash
# COT (Commitments of Traders)
uv run run_analysis.py show csv mn1 -d fastest --rule cot:14,close

# Put/Call Ratio
uv run run_analysis.py show csv mn1 -d fastest --rule putcallratio:20,close
```

### Trend Indicators Examples ⭐ **NEW**
```bash
# SuperTrend with default parameters
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0

# SuperTrend with custom price type
uv run run_analysis.py show csv mn1 -d fastest --rule supertrend:10,3.0,open
```

### [EDA Examples](eda-examples.md)
Exploratory Data Analysis examples and workflows.

**Includes:**
- Data quality assessment
- Statistical analysis
- Correlation analysis
- Data visualization
- Pattern recognition

### [Docker Examples](docker-examples.md)
Containerized deployment and usage examples.

**Features:**
- Docker setup examples
- Container management
- UV integration in Docker
- Environment configuration
- Service orchestration

## 🧪 Testing Examples

### [Testing Examples](testing-examples.md)
Comprehensive testing examples and best practices.

**Includes:**
- Unit test examples
- Integration test examples
- UV-specific tests
- Adaptive testing patterns

### UV Testing Examples
```bash
# Run UV-specific tests (Docker)
pytest tests/docker/test_uv_only_mode.py -v

# Run simple tests (both environments)
pytest tests/docker/test_uv_simple.py -v

# Run command tests (Docker)
pytest tests/docker/test_uv_commands.py -v

# Check UV mode (both environments)
python scripts/check_uv_mode.py --verbose

# Run all tests with UV (multithreaded)
uv run pytest tests -n auto
```

### Adaptive Testing Examples
```python
# Example: Environment detection
def test_uv_availability():
    """Test UV availability in current environment."""
    if is_docker_environment():
        # Full validation in Docker
        assert check_uv_variables()
        assert check_uv_paths()
        assert check_uv_commands()
    else:
        # Basic validation in local environment
        assert check_uv_installation()
        assert check_local_directories()
```

## 🔧 Development Examples

### [Script Examples](script-examples.md)
Utility scripts and automation examples.

**Covers:**
- Data processing scripts
- Analysis automation
- UV management scripts
- Environment setup scripts
- Debugging utilities

### [MCP Examples](mcp-examples.md)
Model Context Protocol server examples.

**Includes:**
- MCP server setup
- IDE integration
- Environment detection
- Server configuration
- Usage examples

## 📈 Real-World Scenarios

### Financial Analysis Workflow
```bash
# 1. Setup environment
docker-compose up -d

# 2. Install dependencies
docker-compose exec neozork uv-install

# 3. Run analysis with UV
docker-compose exec neozork uv run run_analysis.py yfinance AAPL --rule PHLD

# 4. Generate visualizations
docker-compose exec neozork uv run python -m src.plotting.fast_plot

# 5. Export results
docker-compose exec neozork uv run python -m src.export.csv_export
```

### Development Workflow
```bash
# 1. Local development with UV
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

# 2. Run tests with UV (multithreaded)
uv run pytest tests -n auto

# 3. Run specific test categories
uv run pytest tests/calculation/ -n auto
uv run pytest tests/cli/ -n auto

# 4. Check UV status
python scripts/check_uv_mode.py --verbose
```

### Native Container Workflow
```bash
# 1. Setup native container
./scripts/native-container/setup.sh

# 2. Run container
./scripts/native-container/run.sh

# 3. Access shell
./scripts/native-container/exec.sh --shell

# 4. Run analysis with UV
nz demo --rule PHLD
uv run run_analysis.py show csv mn1 -d fastest --rule obv:
```

## 🐛 Recent Fixes & Improvements

### Volume Indicators Fix ⭐ **FIXED**
**Issue:** OBV indicator had dual chart plotting errors and parameter parsing issues.

**Fix:** 
- Fixed parameter parsing for `--rule obv:` (empty parameters after colon)
- Fixed volume column handling for volume-based indicators
- Fixed dual chart plotting for OBV with proper argument passing

**Before:**
```bash
# This would fail
uv run run_analysis.py show csv mn1 -d fastest --rule obv:
```

**After:**
```bash
# This now works perfectly
uv run run_analysis.py show csv mn1 -d fastest --rule obv:
```

### UV Integration Improvements
- **Exclusive UV Usage**: No fallback to pip
- **Multithreaded Testing**: `uv run pytest tests -n auto`
- **Docker Integration**: Seamless UV in containers
- **Native Container Support**: Full UV support in Apple Silicon containers

### New Indicators Added
- **SuperTrend**: Advanced trend-following indicator
- **COT**: Commitments of Traders sentiment indicator  
- **Put/Call Ratio**: Options sentiment indicator

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

## 📋 Command Reference

### Basic Commands
```bash
# Demo analysis
uv run run_analysis.py demo --rule PHLD

# Yahoo Finance analysis
uv run run_analysis.py yfinance AAPL --rule RSI

# CSV analysis
uv run run_analysis.py show csv mn1 -d fastest --rule obv:

# Interactive analysis
uv run run_analysis.py interactive
```

### Advanced Commands
```bash
# Multiple indicators
uv run run_analysis.py demo --rule RSI,MACD,PHLD

# Custom plotting backend
uv run run_analysis.py demo --rule PHLD -d plotly

# Export results
uv run run_analysis.py demo --rule PHLD --export-parquet --export-csv
```

### Testing Commands
```bash
# Run all tests
uv run pytest tests -n auto

# Run specific test categories
uv run pytest tests/calculation/ -n auto
uv run pytest tests/cli/ -n auto

# Run with coverage
uv run pytest tests/ --cov=src -n auto
```

## 🎯 Example Categories

### For Beginners
- **Quick Examples**: Fast start with basic functionality
- **UV Setup Examples**: Package management basics
- **Docker Examples**: Containerized usage

### For Developers
- **Testing Examples**: Comprehensive testing patterns
- **Script Examples**: Automation and utilities
- **MCP Examples**: IDE integration

### For Analysts
- **Indicator Examples**: Technical analysis
- **EDA Examples**: Data exploration
- **Usage Examples**: Real-world workflows

### For DevOps
- **Docker Examples**: Container management
- **UV Examples**: Package management
- **Testing Examples**: Quality assurance

## 📚 Example Structure

### Code Examples
Each example includes:
- **Complete Code**: Ready-to-run code snippets
- **Explanation**: Detailed comments and documentation
- **Expected Output**: Sample results and outputs
- **Troubleshooting**: Common issues and solutions

### Configuration Examples
- **Environment Setup**: Configuration files and variables
- **Docker Configuration**: Container setup and management
- **UV Configuration**: Package manager settings

### Workflow Examples
- **Step-by-step**: Detailed workflow instructions
- **Best Practices**: Recommended approaches
- **Error Handling**: Common issues and solutions

## 🔍 Example Testing

### UV Examples Testing
```bash
# Test UV setup examples
pytest tests/docker/test_uv_simple.py -v

# Test UV commands
pytest tests/docker/test_uv_commands.py -v

# Test comprehensive UV functionality
pytest tests/docker/test_uv_only_mode.py -v
```

### Adaptive Examples Testing
```bash
# Test in Docker environment
docker-compose exec neozork pytest tests/docker/test_uv_simple.py -v

# Test in local environment
pytest tests/docker/test_uv_simple.py -v

# Test environment detection
python scripts/check_uv_mode.py --verbose
```

## 📊 Example Outputs

### UV Status Output
```
UV Package Manager Status:
✓ UV is installed and available
✓ UV-only mode is enabled
✓ Cache directory is accessible
✓ Virtual environment is configured
✓ All UV commands are working

Environment: Docker Container
Cache Directory: /app/.uv_cache
Virtual Environment: /app/.venv
Python Path: /app/src
```

### Test Results Output
```
============================= test session starts ==============================
platform linux -- Python 3.11.0, pytest-7.4.0, pluggy-1.2.0
rootdir: /app
plugins: cov-4.1.0, hypothesis-6.75.3, mock-3.11.1
collected 15 items

tests/docker/test_uv_simple.py::test_uv_installation PASSED        [  6%]
tests/docker/test_uv_simple.py::test_uv_version PASSED             [ 13%]
tests/docker/test_uv_simple.py::test_uv_cache_directory PASSED     [ 20%]
tests/docker/test_uv_simple.py::test_uv_venv_directory PASSED      [ 27%]
tests/docker/test_uv_simple.py::test_uv_commands PASSED            [ 33%]
tests/docker/test_uv_simple.py::test_uv_pip_install PASSED         [ 40%]
tests/docker/test_uv_simple.py::test_uv_pip_list PASSED            [ 47%]
tests/docker/test_uv_simple.py::test_uv_venv_creation PASSED       [ 53%]
tests/docker/test_uv_simple.py::test_uv_cache_functionality PASSED [ 60%]
tests/docker/test_uv_simple.py::test_uv_environment_variables PASSED [ 67%]
tests/docker/test_uv_simple.py::test_uv_python_path PASSED         [ 73%]
tests/docker/test_uv_simple.py::test_uv_package_import PASSED      [ 80%]
tests/docker/test_uv_simple.py::test_uv_development_mode PASSED    [ 87%]
tests/docker/test_uv_simple.py::test_uv_performance PASSED         [ 93%]
tests/docker/test_uv_simple.py::test_uv_integration PASSED         [100%]

============================== 15 passed in 2.34s ==============================
```

## 🚨 Troubleshooting Examples

### Common UV Issues
```bash
# Issue: UV not found
# Solution: Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Issue: Cache directory not accessible
# Solution: Create cache directory
mkdir -p ./.uv_cache

# Issue: Virtual environment not found
# Solution: Create virtual environment
uv venv
```

### Common Test Issues
```bash
# Issue: Tests fail in local environment
# Solution: Check environment detection
python scripts/check_uv_mode.py --debug

# Issue: Docker tests fail
# Solution: Check container environment
docker-compose exec neozork env | grep UV
```

## 📚 Additional Resources

- **Documentation**: Comprehensive guides and references
- **GitHub Repository**: Source code and issues
- **Community**: Discussions and support
- **Testing**: Test suite and validation tools

---

**Last Updated**: 2024
**Version**: 2.0.0 (UV-Only Mode) 