# Test Suite Documentation

This directory contains the comprehensive test suite for the Neozork HLD Prediction project, optimized for both local development and Docker environments.

## Test Structure

### Core Test Files
- `eda/` - Exploratory Data Analysis tests
- `interactive/` - Interactive system tests
- `ml/` - Machine learning tests
- `data/` - Data processing tests
- `calculation/` - Technical indicator calculation tests
- `plotting/` - Visualization tests
- `cli/` - Command line interface tests

### Fast Test Files (Docker Optimized)
- `eda/test_time_series_analysis_fast.py` - Fast time series analysis tests
- `test_visualization_manager_fast.py` - Fast visualization tests
- `interactive/test_core_fast.py` - Fast interactive system tests

### Test Runners
- `run_fast_tests.py` - Python script for running fast tests
- `run_optimized_tests.py` - Optimized test runner

## Docker Optimization

### Problem
Some tests were failing in Docker when running with `pytest -n >= 5` due to:
- Timeouts (> 10 seconds)
- Resource constraints
- Large datasets
- Complex computations

### Solution
1. **Test Splitting**: Large tests split into smaller, focused tests
2. **Fast Test Versions**: Optimized test files with smaller datasets
3. **Timeout Protection**: Added timeout mechanisms
4. **Resource Limits**: Reduced parallel processes and dataset sizes

### Optimized Tests
- `test_analyze_volatility` → Split into multiple focused tests
- `test_comprehensive_analysis` → Split into basic, no-data, and small-dataset versions
- `test_create_statistics_plots_many_columns_basic` → Reduced columns and dataset size
- `test_run_feature_engineering_analysis` → Added timeout protection

## Running Tests

### Local Development
```bash
# Run all tests
uv run pytest tests -n auto

# Run only fast tests
uv run pytest tests -m "fast"

# Run excluding slow tests
uv run pytest tests -m "not slow"

# Run specific test file
uv run pytest tests/eda/test_time_series_analysis.py
```

### Docker Environment
```bash
# Run fast tests only
uv run python tests/run_fast_tests.py

# Run specific failing tests
uv run python tests/run_fast_tests.py --specific

# Run with shell script
./scripts/testing/run_tests_docker_optimized.sh fast

# Run with limited parallelism
uv run pytest tests -n 4 --timeout=15
```

### Test Categories
```bash
# Unit tests
uv run pytest tests -m "unit"

# Integration tests
uv run pytest tests -m "integration"

# Docker-specific tests
uv run pytest tests -m "docker"
```

## Configuration

### pytest.ini
- Global timeout: 30 seconds
- Parallel processes: auto (limited to 4 in Docker)
- Worker distribution: worksteal
- Max worker restarts: 3

### Environment Variables
- `MAX_WORKERS`: Number of parallel workers (default: 4)
- `TIMEOUT`: Test timeout in seconds (default: 15)
- `MAX_FAIL`: Maximum number of failures (default: 5)

## Test Markers

### Built-in Markers
- `@pytest.mark.fast` - Fast tests for Docker
- `@pytest.mark.slow` - Slow tests (exclude in Docker)
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.docker` - Docker-specific tests

### Usage
```python
import pytest

@pytest.mark.fast
def test_fast_function():
    """This test runs quickly and is safe for Docker."""
    pass

@pytest.mark.slow
def test_slow_function():
    """This test is slow and should be excluded in Docker."""
    pass
```

## Best Practices

### Writing Tests
1. **Use Small Datasets**: 20-50 data points for fast tests
2. **Add Timeouts**: Use `signal.alarm()` for long operations
3. **Handle Exceptions**: Gracefully handle plotting issues
4. **Mock Dependencies**: Mock external services and heavy operations
5. **Clean Up**: Clean up resources after tests

### Test Organization
1. **One Test Per Function**: Each test should test one specific behavior
2. **Descriptive Names**: Use clear, descriptive test names
3. **Arrange-Act-Assert**: Structure tests with clear sections
4. **Fixtures**: Use fixtures for common setup
5. **Documentation**: Document complex test logic

### Performance
1. **Dataset Size**: Use appropriate dataset sizes for test type
2. **Parallelization**: Design tests to run in parallel
3. **Resource Management**: Clean up files, connections, etc.
4. **Caching**: Cache expensive operations when possible

## Troubleshooting

### Common Issues
1. **Timeout Errors**: Increase timeout or optimize test
2. **Memory Errors**: Reduce dataset size
3. **Import Errors**: Check dependencies in Docker
4. **Plotting Errors**: Add exception handling

### Debug Commands
```bash
# Run single test with verbose output
uv run pytest tests/eda/test_time_series_analysis_fast.py::TestTimeSeriesAnalyzerFast::test_analyze_volatility_fast -v -s

# Run with coverage
uv run pytest tests --cov=src --cov-report=html

# Run with memory profiling
uv run pytest tests --memray

# Run with performance profiling
uv run pytest tests --durations=10
```

## Continuous Integration

### GitHub Actions
Tests are automatically run on:
- Pull requests
- Push to main branch
- Scheduled runs

### Docker CI
- Uses optimized test settings
- Runs fast tests only
- Limited to 4 parallel processes
- 15-second timeout per test

## Monitoring

### Performance Metrics
- Test execution time
- Memory usage
- CPU utilization
- Success rate

### Regular Maintenance
- Monitor test performance
- Update timeout values
- Optimize slow tests
- Add new fast tests for new features

## Documentation

For detailed information about test optimization for Docker, see:
- `docs/testing/test-optimization-docker.md` - Comprehensive optimization guide
- `docs/testing/` - Additional testing documentation

## Contributing

When adding new tests:
1. Follow the established patterns
2. Add appropriate markers
3. Optimize for Docker if needed
4. Update documentation
5. Run tests locally and in Docker
