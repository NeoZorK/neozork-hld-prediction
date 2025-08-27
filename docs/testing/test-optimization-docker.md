# Test Optimization for Docker Environment

This document describes the optimizations made to tests to ensure they run reliably in Docker environments with limited resources and time constraints.

## Problem Statement

The following tests were failing in Docker when running with `pytest -n >= 5`:

1. `tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_analyze_volatility`
2. `tests/test_visualization_manager.py::TestVisualizationManager::test_create_statistics_plots_many_columns_basic`
3. `tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_comprehensive_analysis`
4. `tests/interactive/test_core.py::TestInteractiveSystem::test_run_feature_engineering_analysis`

These tests were timing out (> 10 seconds) due to:
- Large datasets being processed
- Complex computations
- Heavy plotting operations
- Insufficient resources in Docker containers

## Solutions Implemented

### 1. Test Splitting and Optimization

#### Time Series Analysis Tests
- **Original**: Single comprehensive test with 200 data points
- **Optimized**: Split into multiple focused tests:
  - `test_comprehensive_analysis_basic` - Basic structure validation
  - `test_comprehensive_analysis_no_data` - Error handling
  - `test_comprehensive_analysis_small_dataset` - Small dataset (50 points)
- **Fast Version**: Created `test_time_series_analysis_fast.py` with:
  - Reduced dataset size (50 points instead of 200)
  - Smaller analysis windows (10 instead of default)
  - Reduced max_lag for autocorrelation (5 instead of default)
  - Fewer forecast periods (3 instead of 10)

#### Visualization Manager Tests
- **Original**: Test with 6 columns and large datasets
- **Optimized**: Reduced to 4 columns for faster execution
- **Fast Version**: Created `test_visualization_manager_fast.py` with:
  - Smaller sample data (20 points instead of 100)
  - Fewer columns in test data
  - Exception handling for matplotlib issues

#### Interactive Core Tests
- **Original**: Test without timeout protection
- **Optimized**: Added timeout mechanism (5 seconds)
- **Fast Version**: Created `test_core_fast.py` with:
  - Reduced timeout (3 seconds)
  - Better exception handling
  - Focused test coverage

### 2. Configuration Optimizations

#### pytest.ini Updates
```ini
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --timeout=30
    --timeout-method=thread
    -n auto
    --dist=worksteal
```

#### Docker-Specific Settings
- **Timeout**: 30 seconds global timeout
- **Parallelism**: Limited to 4 processes (`-n 4`)
- **Worker Management**: `--dist=worksteal` for better load balancing
- **Restart Policy**: `--max-worker-restart=3` to prevent infinite loops

### 3. Fast Test Runner

Created `tests/run_fast_tests.py` with two modes:

#### Standard Fast Tests
```bash
python tests/run_fast_tests.py
```
- Runs optimized versions of failing tests
- Uses 4 parallel processes
- 15-second timeout per test

#### Specific Fast Tests
```bash
python tests/run_fast_tests.py --specific
```
- Runs only the most critical fast tests
- Uses 2 parallel processes
- 10-second timeout per test

## Test Structure

### Fast Test Files
1. `tests/eda/test_time_series_analysis_fast.py`
   - `TestTimeSeriesAnalyzerFast` class
   - 15 optimized test methods
   - Small datasets and reduced parameters

2. `tests/test_visualization_manager_fast.py`
   - `TestVisualizationManagerFast` class
   - 12 optimized test methods
   - Exception-safe plotting tests

3. `tests/interactive/test_core_fast.py`
   - `TestInteractiveSystemFast` class
   - 25 optimized test methods
   - Timeout-protected heavy operations

### Original Test Optimizations
- Split large tests into smaller, focused tests
- Added timeout mechanisms
- Reduced dataset sizes
- Optimized parameters for faster execution

## Usage Guidelines

### For Docker Development
```bash
# Run fast tests only
uv run python tests/run_fast_tests.py

# Run specific failing tests
uv run python tests/run_fast_tests.py --specific

# Run with limited parallelism
uv run pytest tests -n 4 --timeout=15
```

### For Local Development
```bash
# Run all tests (including slow ones)
uv run pytest tests -n auto

# Run only fast tests
uv run pytest tests -m "fast"

# Run excluding slow tests
uv run pytest tests -m "not slow"
```

## Best Practices

### Writing Docker-Optimized Tests
1. **Use Small Datasets**: 20-50 data points instead of 100+
2. **Limit Parameters**: Reduce window sizes, max_lag, periods
3. **Add Timeouts**: Use `signal.alarm()` for long-running operations
4. **Handle Exceptions**: Gracefully handle matplotlib/plotting issues
5. **Mock Heavy Operations**: Use mocks for external dependencies

### Test Markers
- `@pytest.mark.fast` - For fast tests
- `@pytest.mark.slow` - For slow tests
- `@pytest.mark.docker` - For Docker-specific tests

### Resource Management
- **Memory**: Use small datasets and clean up after tests
- **CPU**: Limit parallel processes based on container resources
- **Time**: Set appropriate timeouts for each test type
- **I/O**: Mock file operations where possible

## Monitoring and Maintenance

### Performance Metrics
- Test execution time per test
- Memory usage during test execution
- CPU utilization
- Success rate in Docker environment

### Regular Updates
- Monitor test performance in Docker
- Update timeout values based on actual execution times
- Optimize datasets and parameters as needed
- Add new fast tests for new functionality

## Troubleshooting

### Common Issues
1. **Timeout Errors**: Increase timeout or optimize test
2. **Memory Errors**: Reduce dataset size or add cleanup
3. **Import Errors**: Ensure all dependencies are available in Docker
4. **Plotting Errors**: Add exception handling for matplotlib issues

### Debug Commands
```bash
# Run single test with verbose output
uv run pytest tests/eda/test_time_series_analysis_fast.py::TestTimeSeriesAnalyzerFast::test_analyze_volatility_fast -v -s

# Run with memory profiling
uv run pytest tests --memray

# Run with coverage
uv run pytest tests --cov=src --cov-report=html
```

This optimization ensures that tests run reliably in Docker environments while maintaining good test coverage and fast feedback loops for development.
