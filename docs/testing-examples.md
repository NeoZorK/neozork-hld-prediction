# Testing Examples

Comprehensive examples for testing the project.

## Overview

The project includes extensive testing infrastructure:

- **Unit Tests** - Individual component testing
- **Integration Tests** - Component interaction testing
- **Performance Tests** - Performance and optimization testing
- **Coverage Analysis** - Test coverage reporting
- **Debug Testing** - Troubleshooting and debugging

## Running Tests

### Basic Test Commands
```bash
# Run all tests
python -m pytest tests/

# Run tests with verbose output
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run tests and stop on first failure
python -m pytest tests/ -x

# Run tests and show local variables on failure
python -m pytest tests/ -l
```

### Test Categories
```bash
# Run calculation tests
python -m pytest tests/calculation/ -v

# Run CLI tests
python -m pytest tests/cli/ -v

# Run data tests
python -m pytest tests/data/ -v

# Run EDA tests
python -m pytest tests/eda/ -v

# Run export tests
python -m pytest tests/export/ -v

# Run plotting tests
python -m pytest tests/plotting/ -v

# Run workflow tests
python -m pytest tests/workflow/ -v
```

### Specific Test Files
```bash
# Run specific test files
python -m pytest tests/test_stdio.py -v
python -m pytest tests/mcp/test_auto_start_mcp.py -v
python -m pytest tests/calculation/indicators/test_coverage_summary.py -v

# Run CLI examples test
python -m pytest tests/cli/test_cli_examples.py -v

# Run interactive mode test
python -m pytest tests/cli/test_interactive_mode.py -v
```

## Indicator Testing

### Testing Specific Indicators
```bash
# Test RSI indicator
python -m pytest tests/calculation/indicators/oscillators/test_rsi_ind_calc.py -v

# Test MACD indicator
python -m pytest tests/calculation/indicators/momentum/test_macd_indicator.py -v

# Test EMA indicator
python -m pytest tests/calculation/indicators/trend/test_ema_indicator.py -v

# Test Bollinger Bands
python -m pytest tests/calculation/indicators/volatility/test_bb_indicator.py -v

# Test ATR indicator
python -m pytest tests/calculation/indicators/volatility/test_atr_indicator.py -v
```

### Testing Indicator Categories
```bash
# Test all oscillators
python -m pytest tests/calculation/indicators/oscillators/ -v

# Test all momentum indicators
python -m pytest tests/calculation/indicators/momentum/ -v

# Test all trend indicators
python -m pytest tests/calculation/indicators/trend/ -v

# Test all volatility indicators
python -m pytest tests/calculation/indicators/volatility/ -v

# Test all volume indicators
python -m pytest tests/calculation/indicators/volume/ -v
```

### Testing Edge Cases
```bash
# Test edge cases
python -m pytest tests/calculation/indicators/edge_cases/ -v

# Test mathematical validation
python -m pytest tests/calculation/indicators/validation/ -v

# Test performance
python -m pytest tests/calculation/indicators/performance/ -v
```

## Data Testing

### Testing Data Fetchers
```bash
# Test Binance fetcher
python -m pytest tests/data/fetchers/test_binance_fetcher.py -v

# Test CSV fetcher
python -m pytest tests/data/fetchers/test_csv_fetcher.py -v

# Test Yahoo Finance fetcher
python -m pytest tests/data/fetchers/test_yfinance_fetcher.py -v

# Test exchange rate fetcher
python -m pytest tests/data/fetchers/test_exrate_current_fetcher.py -v
```

### Testing Data Acquisition
```bash
# Test data acquisition
python -m pytest tests/data/test_data_acquisition.py -v

# Test data quality
python -m pytest tests/eda/test_data_quality.py -v

# Test data processing
python -m pytest tests/data/test_data_processing.py -v
```

## CLI Testing

### Testing CLI Commands
```bash
# Test CLI examples
python -m pytest tests/cli/test_cli_examples.py -v

# Test CLI indicators integration
python -m pytest tests/cli/test_cli_indicators_integration.py -v

# Test CLI all commands
python -m pytest tests/cli/test_cli_all_commands.py -v

# Test interactive mode
python -m pytest tests/cli/test_interactive_mode.py -v
```

### Testing CLI Indicators
```bash
# Test RSI CLI
python -m pytest tests/cli/indicators/oscillators/test_show_rsi_ind.py -v

# Test CLI oscillators
python -m pytest tests/cli/indicators/oscillators/ -v
```

## MCP Testing

### Testing MCP Servers
```bash
# Test stdio mode
python tests/test_stdio.py

# Test auto-start MCP
python -m pytest tests/mcp/test_auto_start_mcp.py -v

# Test PyCharm GitHub Copilot MCP
python -m pytest tests/mcp/test_pycharm_github_copilot_mcp.py -v

# Test MCP functionality
python -m pytest tests/mcp/ -v
```

### Testing MCP Integration
```bash
# Test MCP server integration
python scripts/run_cursor_mcp.py --test

# Test MCP with coverage
python -m pytest tests/mcp/ --cov=src.mcp --cov-report=html
```

## EDA Testing

### Testing EDA Components
```bash
# Test basic stats
python -m pytest tests/eda/test_basic_stats.py -v

# Test data quality
python -m pytest tests/eda/test_data_quality.py -v

# Test correlation analysis
python -m pytest tests/eda/test_correlation_analysis.py -v

# Test feature importance
python -m pytest tests/eda/test_feature_importance.py -v
```

### Testing EDA Scripts
```bash
# Test EDA script
python -m pytest tests/scripts/test_eda_script.py -v

# Test init directories
python -m pytest tests/scripts/test_init_dirs.bats -v
```

## Export Testing

### Testing Export Functionality
```bash
# Test export functionality
python -m pytest tests/export/test_export_functionality.py -v

# Test CSV export
python -m pytest tests/export/test_csv_export.py -v

# Test JSON export
python -m pytest tests/export/test_json_export.py -v

# Test Parquet export
python -m pytest tests/export/test_parquet_export.py -v
```

## Plotting Testing

### Testing Plotting Components
```bash
# Test fast plot
python -m pytest tests/plotting/test_fast_plot.py -v

# Test fastest auto plot
python -m pytest tests/plotting/test_fastest_auto_plot.py -v

# Test plotting backends
python -m pytest tests/plotting/test_plotting_backends.py -v

# Test plotting performance
python -m pytest tests/plotting/test_plotting_performance.py -v
```

## Coverage Analysis

### Running Coverage Analysis
```bash
# Run coverage analysis
python tests/zzz_analyze_test_coverage.py

# Run with verbose output
python tests/zzz_analyze_test_coverage.py --verbose

# Generate coverage report
python -m pytest tests/ --cov=src --cov-report=html

# Generate coverage badge
python -m pytest tests/ --cov=src --cov-report=html --cov-branch
```

### Coverage Reports
```bash
# Generate HTML coverage report
python -m pytest tests/ --cov=src --cov-report=html

# Generate XML coverage report
python -m pytest tests/ --cov=src --cov-report=xml

# Generate terminal coverage report
python -m pytest tests/ --cov=src --cov-report=term-missing

# Generate multiple coverage reports
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term --cov-report=xml
```

## Performance Testing

### Performance Tests
```bash
# Run performance tests
python -m pytest tests/calculation/indicators/performance/ -v

# Test plotting performance
python -m pytest tests/plotting/test_plotting_performance.py -v

# Test data processing performance
python -m pytest tests/data/test_data_performance.py -v
```

### Benchmarking
```bash
# Run benchmarks
python -m pytest tests/benchmarks/ -v

# Test memory usage
python -m pytest tests/performance/test_memory_usage.py -v

# Test execution time
python -m pytest tests/performance/test_execution_time.py -v
```

## Debug Testing

### Debug Mode Testing
```bash
# Run tests with debug output
python -m pytest tests/ -s -v

# Run specific test with debugger
python -m pytest tests/test_stdio.py::test_stdio_mode -s --pdb

# Run tests and show print statements
python -m pytest tests/ -s

# Run tests with maximum verbosity
python -m pytest tests/ -vvv
```

### Debugging Specific Tests
```bash
# Debug stdio test
python -m pytest tests/test_stdio.py -s --pdb

# Debug MCP test
python -m pytest tests/mcp/test_auto_start_mcp.py -s --pdb

# Debug indicator test
python -m pytest tests/calculation/indicators/oscillators/test_rsi_ind_calc.py -s --pdb
```

## Parallel Testing

### Running Tests in Parallel
```bash
# Run tests in parallel
python -m pytest tests/ -n auto

# Run with specific number of workers
python -m pytest tests/ -n 4

# Run specific category in parallel
python -m pytest tests/calculation/ -n auto
```

## Continuous Integration

### CI/CD Testing
```bash
# Run tests for CI
python -m pytest tests/ --cov=src --cov-report=xml

# Run tests with coverage badge
python -m pytest tests/ --cov=src --cov-report=html --cov-branch

# Run tests and upload coverage
python -m pytest tests/ --cov=src --cov-report=xml
codecov
```

### GitHub Actions Example
```yaml
name: Test and Deploy
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: |
          python -m pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Docker Testing

### Testing in Docker
```bash
# Run tests in container
docker compose run --rm neozork-hld python -m pytest tests/

# Run tests with coverage in container
docker compose run --rm neozork-hld python -m pytest tests/ --cov=src --cov-report=html

# Run specific tests in container
docker compose run --rm neozork-hld python -m pytest tests/calculation/ -v
```

### Docker Test Commands
```bash
# Test container
python -m pytest tests/docker/test_container.py -v

# Test Docker base
python -m pytest tests/docker/test_docker_base.py -v

# Test Docker functionality
python -m pytest tests/docker/ -v
```

## Workflow Testing

### Testing Workflows
```bash
# Test reporting
python -m pytest tests/workflow/test_reporting.py -v

# Test workflow
python -m pytest tests/workflow/test_workflow.py -v

# Test workflow integration
python -m pytest tests/workflow/ -v
```

## Troubleshooting

### Common Test Issues
```bash
# Issue: Import errors
python -m pytest tests/ --tb=short

# Issue: Test failures
python -m pytest tests/ -x --pdb

# Issue: Coverage issues
python -m pytest tests/ --cov=src --cov-report=term-missing

# Issue: Performance issues
python -m pytest tests/ --durations=10
```

### Test Debugging
```bash
# Debug test failures
python -m pytest tests/ -s -v --tb=long

# Debug specific test
python -m pytest tests/test_stdio.py::test_stdio_mode -s --pdb

# Debug with print statements
python -m pytest tests/ -s

# Debug with maximum verbosity
python -m pytest tests/ -vvv
```

### Test Environment
```bash
# Check test environment
python -c "import pytest; print(pytest.__version__)"
python -c "import coverage; print(coverage.__version__)"

# Check test dependencies
pip list | grep pytest
pip list | grep coverage

# Check test configuration
python -m pytest --version
```

## Advanced Testing

### Custom Test Fixtures
```python
# Example: Custom test fixture
import pytest
import pandas as pd

@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return pd.DataFrame({
        'open': [100, 101, 102],
        'high': [105, 106, 107],
        'low': [95, 96, 97],
        'close': [103, 104, 105],
        'volume': [1000, 1100, 1200]
    })

def test_indicator_with_sample_data(sample_data):
    """Test indicator with sample data."""
    # Test implementation
    pass
```

### Test Data Management
```bash
# Create test data
python scripts/create_test_parquet.py

# Recreate CSV from Parquet
python scripts/recreate_csv.py

# Clean test data
rm -rf tests/test_data/
```

---

📚 **Additional Resources:**
- **[Usage Examples](usage-examples.md)** - Comprehensive usage examples
- **[Quick Examples](quick-examples.md)** - Fast start examples
- **[Indicator Examples](indicator-examples.md)** - Technical indicator examples
- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Script Examples](script-examples.md)** - Utility script examples
- **[Docker Examples](docker-examples.md)** - Docker examples
- **[EDA Examples](eda-examples.md)** - EDA examples 