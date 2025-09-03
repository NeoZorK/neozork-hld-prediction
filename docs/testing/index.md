# Testing Guide

The Neozork HLD Prediction system includes a comprehensive testing framework designed to ensure code quality, reliability, and maintainability.

## Overview

Our testing strategy follows these principles:

- **100% Test Coverage**: All new features must have complete test coverage
- **Parallel Execution**: Tests run in parallel for faster execution
- **Multiple Test Types**: Unit, integration, and performance tests
- **Automated Testing**: CI/CD integration with automated test execution
- **Quality Gates**: Tests must pass before code can be merged

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── core/               # Core module tests
│   ├── data/               # Data module tests
│   ├── analysis/           # Analysis module tests
│   ├── ml/                 # Machine learning tests
│   ├── cli/                # CLI tests
│   └── utils/              # Utility tests
├── integration/             # Integration tests
│   ├── test_system_integration.py
│   └── test_workflow_integration.py
├── performance/             # Performance tests
│   ├── test_performance.py
│   └── test_benchmarks.py
├── conftest.py             # Pytest configuration
└── run_all_tests.py        # Main test runner
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
uv run tests/run_all_tests.py

# Run with verbose output
uv run tests/run_all_tests.py --verbose

# Run specific test types
uv run tests/run_all_tests.py --type unit
uv run tests/run_all_tests.py --type integration
uv run tests/run_all_tests.py --type performance
```

### Advanced Test Execution

```bash
# Run CLI tests only
uv run tests/run_all_tests.py --cli-only

# Run tests matching pattern
uv run tests/run_all_tests.py --pattern "test_cli"

# Disable parallel execution
uv run tests/run_all_tests.py --no-parallel

# Disable coverage reporting
uv run tests/run_all_tests.py --no-coverage
```

### Direct Pytest Execution

```bash
# Run all tests with pytest
uv run pytest tests -n auto

# Run specific test file
uv run pytest tests/unit/cli/test_cli.py -v

# Run tests with coverage
uv run pytest tests --cov=src --cov-report=html -n auto

# Run tests matching pattern
uv run pytest tests -k "test_cli" -v
```

## Test Types

### Unit Tests

Unit tests verify individual components in isolation.

**Location**: `tests/unit/`

**Characteristics**:
- Test single functions or classes
- Mock external dependencies
- Fast execution
- High isolation

**Example**:
```python
def test_cli_initialization():
    """Test CLI initialization."""
    cli = CLI("test-cli")
    
    assert cli.name == "test-cli"
    assert cli.command_manager is not None
    assert cli.parser is not None
```

### Integration Tests

Integration tests verify component interactions.

**Location**: `tests/integration/`

**Characteristics**:
- Test multiple components together
- Use real or realistic data
- Verify data flow between components
- Test error handling across boundaries

**Example**:
```python
def test_data_analysis_pipeline():
    """Test complete data analysis pipeline."""
    # Create data source
    source = CSVDataSource("test_data", {"file_path": "test.csv"})
    
    # Create analysis pipeline
    pipeline = AnalysisPipeline("test_pipeline")
    pipeline.add_data_source(source)
    pipeline.add_analysis_step(SMAIndicator("sma", {"period": 20}))
    
    # Execute pipeline
    results = pipeline.execute()
    
    assert "sma" in results
    assert len(results["sma"]) > 0
```

### Performance Tests

Performance tests verify system performance characteristics.

**Location**: `tests/performance/`

**Characteristics**:
- Measure execution time
- Monitor memory usage
- Test scalability
- Benchmark critical operations

**Example**:
```python
def test_large_dataset_performance():
    """Test performance with large datasets."""
    import time
    
    # Create large dataset
    large_data = pd.DataFrame({
        "close": np.random.randn(100000),
        "volume": np.random.randint(1000, 10000, 100000)
    })
    
    # Measure execution time
    start_time = time.time()
    indicator = SMAIndicator("sma", {"period": 50})
    result = indicator.calculate(large_data)
    execution_time = time.time() - start_time
    
    # Performance assertions
    assert execution_time < 5.0  # Should complete within 5 seconds
    assert len(result) == 100000
```

### CLI Tests

CLI tests verify all command-line interface functionality.

**Location**: `tests/unit/cli/`

**Characteristics**:
- Test all CLI commands and flags
- Verify help text and error messages
- Test argument validation
- Verify exit codes

**Example**:
```python
def test_cli_help_command():
    """Test CLI help command."""
    cli = CLI("test-cli")
    
    # Test general help
    result = cli.run(["--help"])
    assert result == 0
    
    # Test command-specific help
    result = cli.run(["analyze", "--help"])
    assert result == 0
```

## Test Configuration

### Pytest Configuration

**File**: `pytest.ini`

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests
    slow: Slow running tests
    cli: CLI specific tests
```

### Coverage Configuration

**File**: `.coveragerc`

```ini
[run]
source = src
omit = 
    */tests/*
    */__pycache__/*
    */venv/*
    */env/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod
```

## Writing Tests

### Test Naming Conventions

- **Test files**: `test_<module_name>.py`
- **Test classes**: `Test<ClassName>`
- **Test methods**: `test_<description>`

### Test Structure

```python
"""
Unit tests for <module_name> module.

This module tests the <description>.
"""

import pytest
from unittest.mock import Mock, patch
from src.module import ClassName


class TestClassName:
    """Test cases for ClassName class."""
    
    def test_method_name(self):
        """Test method description."""
        # Arrange
        instance = ClassName("test")
        
        # Act
        result = instance.method()
        
        # Assert
        assert result == expected_value
    
    def test_method_with_mock(self):
        """Test method with mocked dependencies."""
        # Arrange
        with patch('src.module.ExternalClass') as mock_external:
            mock_external.return_value.method.return_value = "mocked_result"
            instance = ClassName("test")
        
        # Act
        result = instance.method_with_external()
        
        # Assert
        assert result == "mocked_result"
        mock_external.assert_called_once()
```

### Test Data

**Location**: `tests/fixtures/`

```python
# conftest.py
@pytest.fixture
def sample_ohlcv_data():
    """Provide sample OHLCV data for testing."""
    return pd.DataFrame({
        'timestamp': pd.date_range('2023-01-01', periods=100, freq='H'),
        'open': np.random.randn(100),
        'high': np.random.randn(100),
        'low': np.random.randn(100),
        'close': np.random.randn(100),
        'volume': np.random.randint(1000, 10000, 100)
    })

@pytest.fixture
def mock_data_source():
    """Provide mock data source for testing."""
    source = Mock()
    source.fetch.return_value = sample_ohlcv_data()
    source.is_available.return_value = True
    return source
```

### Assertions and Matchers

```python
# Basic assertions
assert result == expected_value
assert len(result) > 0
assert "key" in result

# Exception testing
with pytest.raises(ValueError):
    function_that_raises_error()

# Approximate equality for floats
assert result == pytest.approx(expected_value, rel=1e-6)

# Collection testing
assert all(item > 0 for item in result)
assert any(item < 0 for item in result)
```

## Mocking and Patching

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch, MagicMock

def test_with_mocked_dependency():
    """Test with mocked external dependency."""
    with patch('src.module.external_api') as mock_api:
        mock_api.get_data.return_value = {"key": "value"}
        
        result = function_under_test()
        
        assert result["key"] == "value"
        mock_api.get_data.assert_called_once()
```

### Mocking File Operations

```python
def test_file_operations():
    """Test file operations with mocked filesystem."""
    with patch('builtins.open', mock_open(read_data='test data')):
        with patch('pathlib.Path.exists', return_value=True):
            result = read_file("test.txt")
            assert result == "test data"
```

## Test Execution Strategies

### Parallel Execution

Tests run in parallel by default using pytest-xdist:

```bash
# Auto-detect number of CPU cores
uv run pytest tests -n auto

# Specify number of processes
uv run pytest tests -n 4

# Disable parallel execution
uv run pytest tests -n 0
```

### Test Selection

```bash
# Run tests by marker
uv run pytest tests -m "unit"
uv run pytest tests -m "integration"
uv run pytest tests -m "not slow"

# Run tests by pattern
uv run pytest tests -k "test_cli"
uv run pytest tests -k "not test_performance"

# Run specific test file
uv run pytest tests/unit/cli/test_cli.py
```

### Test Discovery

```bash
# List all tests without running
uv run pytest tests --collect-only

# List tests by pattern
uv run pytest tests -k "test_cli" --collect-only

# Show test configuration
uv run pytest tests --setup-show
```

## Continuous Integration

### GitHub Actions

Tests run automatically on every push and pull request:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          uv sync
      - run: uv run tests/run_all_tests.py --type unit
      - run: uv run tests/run_all_tests.py --type integration
      - run: uv run tests/run_all_tests.py --cli-only
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: uv run pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [tests, -n, auto]
```

## Performance Testing

### Benchmarking

```python
def test_performance_benchmark():
    """Benchmark critical operations."""
    import timeit
    
    # Benchmark data loading
    load_time = timeit.timeit(
        lambda: load_large_dataset("data.csv"),
        number=10
    )
    
    # Benchmark analysis
    analysis_time = timeit.timeit(
        lambda: analyze_data(large_dataset),
        number=5
    )
    
    # Performance assertions
    assert load_time < 2.0  # Load within 2 seconds
    assert analysis_time < 10.0  # Analysis within 10 seconds
```

### Memory Profiling

```python
def test_memory_usage():
    """Test memory usage of operations."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform operation
    result = memory_intensive_operation()
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory assertions (in MB)
    assert memory_increase < 100 * 1024 * 1024  # Less than 100MB increase
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `src/` is in Python path
2. **Test Discovery**: Check test file naming conventions
3. **Mock Issues**: Verify patch paths and mock setup
4. **Performance Flakiness**: Use appropriate timeouts and retries

### Debug Mode

```bash
# Enable pytest debug output
uv run pytest tests --tb=long -s

# Run single test with debug
uv run pytest tests/unit/cli/test_cli.py::TestCLI::test_init -s

# Enable logging
uv run pytest tests --log-cli-level=DEBUG
```

### Test Isolation

```python
@pytest.fixture(autouse=True)
def reset_state():
    """Reset global state between tests."""
    # Reset any global state
    yield
    # Cleanup after test
```

## Best Practices

### Test Design

- **Single Responsibility**: Each test should verify one thing
- **Descriptive Names**: Test names should clearly describe what they test
- **Arrange-Act-Assert**: Use clear test structure
- **Test Independence**: Tests should not depend on each other

### Test Data

- **Minimal Data**: Use only the data needed for the test
- **Realistic Data**: Use data that represents real-world scenarios
- **Edge Cases**: Test boundary conditions and error cases
- **Cleanup**: Clean up test data after tests

### Performance

- **Fast Execution**: Unit tests should run quickly
- **Efficient Mocking**: Mock only what's necessary
- **Resource Management**: Clean up resources properly
- **Parallel Execution**: Design tests for parallel execution

### Maintenance

- **Regular Updates**: Keep tests up to date with code changes
- **Refactoring**: Refactor tests when code changes
- **Documentation**: Document complex test scenarios
- **Review Process**: Include tests in code review process

## Related Documentation

- [Development Guide](../development/index.md)
- [CLI Documentation](../cli/index.md)
- [API Documentation](../api/index.md)
- [Contributing Guide](../contributing.md) 