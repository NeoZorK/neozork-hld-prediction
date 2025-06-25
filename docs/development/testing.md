# Testing Guide

## Overview

This project uses pytest for comprehensive testing with parallel execution support. All tests are organized in the `tests/` directory and follow a structured approach for maximum coverage and efficiency.

## Test Structure

```
tests/
├── conftest.py                    # Global pytest configuration
├── run_optimized_tests.py         # Optimized test runner
├── calculation/                   # Calculation module tests
├── cli/                          # CLI interface tests
│   └── comprehensive/            # Comprehensive CLI tests
├── data/                         # Data processing tests
├── eda/                          # EDA module tests
├── export/                       # Export functionality tests
├── plotting/                     # Plotting module tests
├── workflow/                     # Workflow tests
└── mcp/                          # MCP server tests
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
uv run pytest tests

# Run with parallel execution (recommended)
uv run pytest tests -n auto

# Run specific test category
uv run pytest tests/cli
uv run pytest tests/calculation

# Run with verbose output
uv run pytest tests -v
```

### Optimized Test Runner

Use the optimized test runner for better performance and reporting:

```bash
# Run all tests with optimization
python tests/run_optimized_tests.py

# Run specific categories
python tests/run_optimized_tests.py --categories cli calculation

# Run with specific markers
python tests/run_optimized_tests.py --markers unit integration

# Disable parallel execution
python tests/run_optimized_tests.py --no-parallel

# Save results to JSON
python tests/run_optimized_tests.py --save-results
```

### Parallel Testing

The project uses `pytest-xdist` for parallel test execution:

```bash
# Auto-detect number of workers
uv run pytest tests -n auto

# Specify number of workers
uv run pytest tests -n 4

# Run in parallel with specific options
uv run pytest tests -n auto --tb=short --disable-warnings
```

## Test Results Management

### Results Storage

Test results are automatically saved to `logs/test_results/` directory with timestamped filenames:

```
logs/
├── test_results/
│   ├── test_results_20250623_193622.json
│   ├── test_results_20250623_193618.json
│   └── ...
├── stats/
└── ...
```

### Managing Test Results

Use the test results management script for advanced operations:

```bash
# Generate report for last 7 days
python scripts/manage_test_results.py --action report

# Generate report for last 30 days
python scripts/manage_test_results.py --action report --days 30

# Clean old results (older than 30 days)
python scripts/manage_test_results.py --action clean --days 30

# Export results to CSV
python scripts/manage_test_results.py --action export --output test_results.csv

# Show latest test results
python scripts/manage_test_results.py --action latest
```

### Test Results Format

Each test result file contains:

```json
{
  "timestamp": "20250623_193622",
  "datetime": "2025-06-23T19:36:22.123456",
  "passed": 1018,
  "failed": 0,
  "skipped": 27,
  "errors": 0,
  "total": 1045,
  "success_rate": 100.0,
  "exit_status": "EXIT_OK"
}
```

## Test Categories

### Unit Tests
- **Location**: `tests/calculation/`, `tests/data/`, etc.
- **Purpose**: Test individual functions and classes
- **Marker**: `@pytest.mark.unit`

### Integration Tests
- **Location**: `tests/integration/`
- **Purpose**: Test component interactions
- **Marker**: `@pytest.mark.integration`

### CLI Tests
- **Location**: `tests/cli/`
- **Purpose**: Test command-line interface
- **Marker**: `@pytest.mark.cli`

### Performance Tests
- **Location**: Various test files
- **Purpose**: Test performance and stress scenarios
- **Marker**: `@pytest.mark.performance`

## Test Fixtures

### Global Fixtures (conftest.py)

- `test_data_dir`: Temporary test data directory
- `sample_data`: Sample financial data for testing
- `cli_script`: Path to main CLI script
- `python_executable`: Python executable path
- `temp_workspace`: Temporary workspace for tests
- `mock_data_files`: Mock data files
- `run_cli`: CLI command runner
- `performance_monitor`: Performance monitoring

### Usage Example

```python
def test_with_fixtures(sample_data, run_cli, performance_monitor):
    """Test using multiple fixtures"""
    # Use sample data
    csv_file = sample_data['csv_file']
    
    # Run CLI command
    return_code, stdout, stderr, execution_time = run_cli([
        'python', 'run_analysis.py', 'csv', 
        '--csv-file', csv_file, '--point', '0.01'
    ])
    
    assert return_code == 0
    assert execution_time < 60
```

## Test Markers

### Available Markers

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.performance`: Performance tests
- `@pytest.mark.cli`: CLI tests
- `@pytest.mark.data`: Data processing tests
- `@pytest.mark.indicators`: Technical indicator tests
- `@pytest.mark.export`: Export functionality tests
- `@pytest.mark.plotting`: Visualization tests

### Custom Markers

```python
@pytest.mark.slow
def test_slow_operation():
    """Test that takes a long time"""
    pass

@pytest.mark.flag_combinations
def test_flag_combinations():
    """Test different flag combinations"""
    pass
```

## Test Configuration

### pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "performance: Performance tests",
    "cli: CLI tests",
    "data: Data processing tests",
    "indicators: Technical indicator tests",
    "export: Export functionality tests",
    "plotting: Visualization tests",
]
```

### Environment Variables

```bash
# Set test environment
export PYTEST_TIMEOUT=120
export PYTEST_WORKERS=auto
export PYTEST_VERBOSE=true
```

## Performance Optimization

### Parallel Execution

- Use `-n auto` for automatic worker detection
- Use `-n 4` for specific number of workers
- Monitor CPU usage during parallel execution

### Test Data Management

- Use session-scoped fixtures for expensive setup
- Clean up temporary files automatically
- Use mock data for fast tests

### Memory Management

- Monitor memory usage with `performance_monitor` fixture
- Clean up large objects after tests
- Use generators for large datasets

## Best Practices

### Test Organization

1. **Group related tests**: Use descriptive class names
2. **Use meaningful test names**: Describe what is being tested
3. **Keep tests independent**: Each test should be self-contained
4. **Use appropriate fixtures**: Share setup code efficiently

### Test Quality

1. **100% coverage**: All source files should have corresponding tests
2. **Edge cases**: Test boundary conditions and error scenarios
3. **Performance**: Monitor execution time and memory usage
4. **Documentation**: Document complex test scenarios

### Error Handling

```python
def test_error_scenarios():
    """Test error handling"""
    with pytest.raises(ValueError):
        function_with_invalid_input()
    
    with pytest.raises(FileNotFoundError):
        function_with_missing_file()
```

## Continuous Integration

### GitHub Actions

Tests are automatically run on:
- Pull requests
- Push to main branch
- Scheduled runs

### Local Development

```bash
# Run tests before committing
python tests/run_optimized_tests.py --save-results

# Run specific test suite
python tests/run_optimized_tests.py --categories cli --verbose

# Check test coverage
uv run pytest tests --cov=src --cov-report=html

# Generate test results report
python scripts/manage_test_results.py --action report --days 7
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure `src/` is in Python path
2. **Timeout errors**: Increase timeout or optimize slow tests
3. **Memory issues**: Use smaller test datasets
4. **Parallel conflicts**: Use `--no-parallel` for debugging

### Debug Mode

```bash
# Run single test with debug output
uv run pytest tests/test_specific.py::test_function -v -s

# Run with maximum verbosity
uv run pytest tests -vvv --tb=long
```

## Test Results

### Output Format

```
============================================================
📊 TEST EXECUTION SUMMARY
============================================================
⏱️  Execution Time: 45.23s
📈 Total Tests: 1018
✅ Passed: 1013
❌ Failed: 5
⏭️  Skipped: 27
💥 Errors: 0
🎯 Success Rate: 99.5%
⚡ Tests/Second: 22.5
============================================================
```

### Result Files

- `logs/test_results/test_results_YYYYMMDD_HHMMSS.json`: Detailed test results with timestamps
- `htmlcov/`: Coverage reports
- `logs/`: Test execution logs and other project logs

## Contributing

When adding new tests:

1. Follow the existing structure
2. Use appropriate fixtures
3. Add proper markers
4. Include edge cases
5. Document complex scenarios
6. Ensure parallel compatibility
7. Test results will be automatically saved to `logs/test_results/` 