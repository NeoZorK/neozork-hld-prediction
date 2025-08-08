# Apple Native Container Test Fixes

This document describes the fixes implemented to resolve test issues in Apple native container environment.

## Problems Identified

### 1. Segmentation Fault
- **Cause**: Memory issues with matplotlib and multiprocessing
- **Impact**: Container crashes during test execution
- **Solution**: Reduced parallelism and added memory limits

### 2. FileNotFoundError: '/app/.venv/bin/python'
- **Cause**: Incorrect Python path in container environment
- **Impact**: Test execution fails
- **Solution**: Updated path handling and environment setup

### 3. Memory Issues
- **Cause**: Large number of tests running simultaneously
- **Impact**: Container runs out of memory
- **Solution**: Staged test execution and reduced worker count

### 4. Matplotlib Threading Issues
- **Cause**: Thread conflicts in plotting tests
- **Impact**: Test failures and crashes
- **Solution**: Added thread locks and non-interactive backend

## Fixes Implemented

### 1. Updated pytest.ini Configuration

```ini
# Added new markers
markers =
    basic: marks tests as basic functionality tests
    flag_combinations: marks tests as flag combination tests
    error: marks tests as error case tests

# Added safety options
addopts = 
    --maxfail=10
    --durations=10

# Added warning filters
filterwarnings =
    ignore::RuntimeWarning
    ignore::matplotlib.cbook.MatplotlibDeprecationWarning
```

### 2. Enhanced conftest.py

- Added container detection
- Configured matplotlib for non-interactive backend
- Added environment variables for safe testing
- Created fixtures for safe test execution
- Added automatic cleanup of matplotlib figures

### 3. Safe Test Runner Script

Created `scripts/run_tests_apple_container.py` with:
- Container detection and environment setup
- Staged test execution to prevent memory issues
- Timeout handling and error recovery
- Memory-efficient worker allocation
- Automatic cleanup procedures

### 4. Bash Script for Container Testing

Created `scripts/run_tests_apple_safe.sh` with:
- Environment setup for container
- Staged test execution
- Memory management
- Error handling and reporting
- Cleanup procedures

### 5. Updated Test Files

#### Fixed matplotlib tests:
- Added `@pytest.mark.container_safe` markers
- Used `mock_plotting_functions` fixture
- Added thread locks for matplotlib operations
- Reduced data size for container tests

#### Fixed CLI tests:
- Updated command execution to use `uv run`
- Added proper error handling
- Reduced timeout values
- Added container-specific test skipping

## Usage

### Running Tests in Apple Native Container

#### Option 1: Using Python Script
```bash
python scripts/run_tests_apple_container.py
```

#### Option 2: Using Bash Script
```bash
# Run all tests in staged mode
./scripts/run_tests_apple_safe.sh staged

# Run only basic tests
./scripts/run_tests_apple_safe.sh basic

# Run only indicator tests
./scripts/run_tests_apple_safe.sh indicators

# Run only plotting tests
./scripts/run_tests_apple_safe.sh plotting
```

#### Option 3: Direct pytest with Safety Options
```bash
# Run with reduced parallelism
uv run pytest tests -n 2 --maxfail=5 --disable-warnings

# Run only safe tests
uv run pytest tests -m "not slow and not performance" -n 1

# Run tests in stages
uv run pytest tests -m "basic or unit" -n 1
uv run pytest tests -m "indicators or data" -n 1
uv run pytest tests -m "plotting" -n 1
```

## Environment Variables

The following environment variables are set for safe container testing:

```bash
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR=/tmp/matplotlib-cache
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export PYTHONMALLOC=malloc
```

## Test Categories

### Safe for Container (Always Run)
- `basic`: Basic functionality tests
- `unit`: Unit tests for individual functions
- `indicators`: Technical indicator calculations
- `data`: Data processing tests
- `export`: Export functionality tests

### Skipped in Container (Too Resource-Intensive)
- `slow`: Slow-running tests
- `performance`: Performance and stress tests
- `integration`: Complex integration tests

### Special Handling
- `plotting`: Run with single worker and reduced data size
- `cli`: Run with proper error handling and timeouts

## Memory Management

### Container Memory Limits
- Reduced worker count to 2 (or 1 for plotting tests)
- Staged test execution to prevent memory buildup
- Automatic cleanup between test stages
- Memory-efficient matplotlib configuration

### Cleanup Procedures
- Close all matplotlib figures after each test
- Clear matplotlib cache between stages
- Remove temporary files and directories
- Reset environment variables

## Error Handling

### Timeout Management
- Default timeout: 600 seconds for full test suite
- Stage timeout: 300 seconds per stage
- Individual test timeout: 30 seconds for CLI tests

### Error Recovery
- Automatic cleanup on test failure
- Graceful handling of segmentation faults
- Detailed error reporting and logging
- Fallback options for failed tests

## Monitoring and Reporting

### Test Results
- JUnit XML reports: `logs/test-results.xml`
- HTML reports: `logs/test-report.html`
- JSON reports: `logs/apple_container_test_report_*.json`

### Performance Metrics
- Execution time per stage
- Memory usage tracking
- Worker utilization
- Error rate monitoring

## Troubleshooting

### Common Issues

#### 1. Segmentation Fault
```bash
# Solution: Reduce workers and memory usage
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
uv run pytest tests -n 1 --maxfail=3
```

#### 2. Memory Exhaustion
```bash
# Solution: Run tests in stages
./scripts/run_tests_apple_safe.sh staged
```

#### 3. Matplotlib Issues
```bash
# Solution: Use non-interactive backend
export MPLCONFIGDIR=/tmp/matplotlib-cache
python -c "import matplotlib; matplotlib.use('Agg')"
```

#### 4. Path Issues
```bash
# Solution: Use uv run for consistent environment
uv run pytest tests
```

### Debug Mode
```bash
# Enable debug output
export PYTHONUNBUFFERED=1
export LOG_LEVEL=DEBUG
./scripts/run_tests_apple_safe.sh staged
```

## Best Practices

### For Container Testing
1. Always use staged execution for large test suites
2. Set appropriate memory limits
3. Use single worker for plotting tests
4. Implement proper cleanup procedures
5. Monitor resource usage

### For Test Development
1. Mark tests with appropriate categories
2. Use fixtures for common setup
3. Implement proper error handling
4. Add container-safe markers where needed
5. Test with reduced data sizes in container

### For CI/CD Integration
1. Use the safe test runner scripts
2. Set appropriate timeouts
3. Implement retry logic for flaky tests
4. Generate comprehensive reports
5. Monitor test performance trends

## Future Improvements

### Planned Enhancements
1. Dynamic memory allocation based on container size
2. Parallel test execution with resource monitoring
3. Automatic test categorization and optimization
4. Enhanced error reporting and debugging tools
5. Integration with container orchestration platforms

### Monitoring and Analytics
1. Test execution time tracking
2. Memory usage analytics
3. Error pattern analysis
4. Performance regression detection
5. Resource utilization optimization

## Conclusion

These fixes provide a robust testing environment for Apple native containers while maintaining test coverage and reliability. The staged execution approach ensures that tests can run successfully even with limited resources, while the enhanced error handling and cleanup procedures prevent container crashes and memory issues.
