# Examples

This section provides practical examples and use cases for the NeoZork HLD Prediction project, including UV package management and adaptive testing.

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
```

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

## 📊 Analysis Examples

### [Indicator Examples](indicator-examples.md)
Technical indicator calculation and usage examples.

**Covers:**
- Momentum indicators (MACD, Stochastic)
- Oscillators (RSI, CCI)
- Trend indicators (EMA, ADX)
- Volatility indicators (ATR, Bollinger Bands)
- Volume indicators (OBV, VWAP)
- Support & Resistance (Pivot Points, Fibonacci)
- Predictive indicators (HMA, Time Series)
- Probability indicators (Monte Carlo, Kelly)
- Sentiment indicators (Fear & Greed, COT)

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

# 3. Run analysis
docker-compose exec neozork nz yfinance AAPL --rule PHLD

# 4. Generate visualizations
docker-compose exec neozork python -m src.plotting.fast_plot

# 5. Export results
docker-compose exec neozork python -m src.export.csv_export
```

### Development Workflow
```bash
# 1. Local development
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

# 2. Run tests
pytest tests/ -v

# 3. Check code quality
python scripts/check_uv_mode.py --verbose

# 4. Docker testing
docker-compose up -d
docker-compose exec neozork pytest tests/docker/ -v
```

### UV Package Management Workflow
```bash
# 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Configure environment
export UV_ONLY_MODE=true
export UV_CACHE_DIR=./.uv_cache

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Verify installation
python scripts/check_uv_mode.py

# 5. Run tests
pytest tests/docker/test_uv_simple.py -v
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