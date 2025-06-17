# Testing Guide

Comprehensive testing framework for validation, unit tests, and quality assurance.

## Testing Framework

The project uses Python's built-in `unittest` framework with additional testing tools:
- **pytest** for advanced test features
- **BATS** for shell script testing
- **Custom validators** for data integrity

## Quick Test Commands

### Run All Tests
```bash
# Using unittest
python -m unittest discover tests

# Using pytest (recommended)
pytest tests/ --maxfail=3 --disable-warnings -v

# Specific test categories
pytest tests/cli/ -v
pytest tests/data/ -v
pytest tests/calculation/ -v
```

### Run Specific Tests
```bash
# Single test file
python -m unittest tests.cli.test_cli_all_commands

# Single test case
python -m unittest tests.cli.test_cli_all_commands.TestCliAllCommands.test_help

# Using pytest
pytest tests/cli/test_cli_all_commands.py::TestCliAllCommands::test_help -v
```

## Test Categories

### 1. Unit Tests
**Location:** `tests/`

```bash
# Core calculation tests
pytest tests/calculation/ -v

# Data processing tests
pytest tests/data/ -v

# CLI interface tests
pytest tests/cli/ -v

# Utility function tests
pytest tests/utils/ -v
```

### 2. Integration Tests
**Location:** `tests/workflow/`

```bash
# Full workflow tests
pytest tests/workflow/ -v

# End-to-end pipeline tests
python tests/workflow/test_full_pipeline.py
```

### 3. Shell Script Tests
**Location:** `tests/scripts/`

```bash
# Test init_dirs.sh script
bats tests/scripts/test_init_dirs.bats

# All shell script tests
find tests/scripts/ -name "*.bats" -exec bats {} \;
```

### 4. Docker Tests
**Location:** `tests/docker/`

```bash
# Docker build and functionality tests
pytest tests/docker/ -v

# Test container startup
python tests/docker/test_docker_build.py
```

## Test Environment Setup

### Prerequisites
```bash
# Install testing dependencies
pip install pytest bats-core

# macOS
brew install bats-core

# Linux
sudo apt-get install bats
```

### Environment Configuration
Create test-specific configuration:
```bash
# Copy environment template
cp .env.example .env.test

# Set test-specific values
export TESTING=true
export LOG_LEVEL=DEBUG
```

## CLI Testing

### Testing All CLI Commands
```bash
# Comprehensive CLI test
python tests/cli/test_cli_all_commands.py

# Test specific modes
pytest tests/cli/test_demo_mode.py
pytest tests/cli/test_csv_mode.py
pytest tests/cli/test_api_modes.py
```

### Manual CLI Testing
```bash
# Test help commands
python run_analysis.py --help
python run_analysis.py --version
python run_analysis.py --examples

# Test demo mode
python run_analysis.py demo
python run_analysis.py demo --rule PHLD

# Test error handling
python run_analysis.py csv  # Should show error
python run_analysis.py yf   # Should show error
```

## Data Validation Tests

### Data Quality Testing
```bash
# Run EDA validation tests
pytest tests/eda/ -v

# Test data integrity
python tests/data/test_data_integrity.py

# Validate calculations
python tests/calculation/test_indicator_accuracy.py
```

### API Connection Tests
```bash
# Test all data sources
pytest tests/data/test_api_connections.py

# Individual API tests
python scripts/debug_scripts/debug_yfinance.py
python scripts/debug_scripts/debug_polygon_connection.py
python scripts/debug_scripts/debug_binance_connection.py
```

## Performance Testing

### Benchmark Tests
```bash
# Performance benchmarks
pytest tests/performance/ -v

# Memory usage tests
python tests/performance/test_memory_usage.py

# Speed benchmarks
python tests/performance/test_calculation_speed.py
```

### Load Testing
```bash
# Large dataset tests
pytest tests/performance/test_large_datasets.py -v -s

# Concurrent processing tests
python tests/performance/test_parallel_processing.py
```

## MCP Server Testing

### MCP Integration Tests
```bash
# Test MCP server functionality
pytest tests/mcp/ -v

# Test server startup
python tests/mcp/test_mcp_server.py

# Test IDE integration
python tests/mcp/test_mcp_integration.py
```

## Continuous Integration

### GitHub Actions Testing
```bash
# Test workflow locally
chmod +x test-workflow.sh
./test-workflow.sh

# Manual workflow testing
act -j test

# Docker CI testing
act -j docker-build
```

### Pre-commit Testing
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run all pre-commit checks
pre-commit run --all-files
```

## Test Data Management

### Sample Data Creation
```bash
# Generate test datasets
python tests/data/generate_test_data.py

# Create mock API responses
python tests/data/create_mock_data.py
```

### Test Data Location
```
tests/
├── data/
│   ├── sample_csv/
│   ├── mock_responses/
│   └── test_datasets/
├── fixtures/
└── resources/
```

## Custom Test Utilities

### Test Helpers
```python
# Common test utilities
from tests.utils.test_helpers import (
    create_test_dataframe,
    mock_api_response,
    assert_dataframe_equal,
    cleanup_test_files
)

# Usage in tests
def test_calculation():
    df = create_test_dataframe()
    result = calculate_indicator(df)
    assert_dataframe_equal(result, expected)
```

### Fixtures
```python
# Common test fixtures
@pytest.fixture
def sample_ohlcv_data():
    return create_test_dataframe()

@pytest.fixture
def mock_api_client():
    return MockAPIClient()
```

## Test Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --disable-warnings
    --maxfail=3
```

### Coverage Configuration
```bash
# Install coverage
pip install coverage pytest-cov

# Run tests with coverage
pytest --cov=src tests/

# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html
```

## Debugging Tests

### Debug Failed Tests
```bash
# Run with debug output
pytest -v -s tests/path/to/test.py

# Drop into debugger on failure
pytest --pdb tests/path/to/test.py

# Debug specific test
python -m pdb tests/path/to/test.py
```

### Test Isolation
```bash
# Run tests in isolation
pytest --forked tests/

# Parallel test execution
pytest -n 4 tests/  # 4 processes
```

## Quality Assurance

### Code Quality Tests
```bash
# Linting
flake8 src/ tests/
black --check src/ tests/

# Type checking
mypy src/

# Security scanning
bandit -r src/
```

### Documentation Tests
```bash
# Test docstrings
pytest --doctest-modules src/

# Test documentation examples
python -m doctest docs/examples.md
```

## Test Reporting

### Test Results
```bash
# JUnit XML format
pytest --junitxml=test-results.xml

# HTML report
pytest --html=test-report.html

# JSON report
pytest --json-report --json-report-file=test-report.json
```

### CI Integration
```yaml
# GitHub Actions test step
- name: Run tests
  run: |
    pytest tests/ --junitxml=test-results.xml
    
- name: Upload test results
  uses: actions/upload-artifact@v2
  with:
    name: test-results
    path: test-results.xml
```

## Best Practices

### Writing Tests
1. **Use descriptive test names**
2. **Follow AAA pattern** (Arrange, Act, Assert)
3. **Keep tests independent**
4. **Use appropriate assertions**
5. **Mock external dependencies**

### Test Organization
1. **Mirror source code structure**
2. **Group related tests**
3. **Use fixtures for common setup**
4. **Separate unit and integration tests**

### Maintenance
1. **Run tests frequently**
2. **Keep tests updated with code changes**
3. **Monitor test performance**
4. **Remove obsolete tests**
