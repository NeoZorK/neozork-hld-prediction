# Testing Guide

## Overview

This guide covers comprehensive testing strategies for the Neozork HLD Prediction system, including unit testing, integration testing, performance testing, and CLI testing.

## Testing Philosophy

### Core Principles
- **100% Coverage**: All code must be covered by tests
- **Parallel Execution**: Tests run in parallel for speed
- **Comprehensive Validation**: Test all functionality and edge cases
- **Automated Testing**: CI/CD integration for all tests
- **Fast Feedback**: Quick test execution for development

### Test Categories
1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions
3. **Performance Tests**: Ensure performance requirements
4. **CLI Tests**: Verify command-line interface functionality

## Test Structure

### Directory Organization
```
tests/
├── unit/                    # Unit tests
│   ├── core/               # Core module tests
│   ├── data/               # Data module tests
│   ├── analysis/           # Analysis module tests
│   ├── ml/                 # ML module tests
│   ├── cli/                # CLI module tests
│   └── utils/              # Utility tests
├── integration/             # Integration tests
├── performance/             # Performance tests
├── conftest.py             # Test configuration
└── run_all_tests.py        # Main test runner
```

### Test File Naming
- **Unit Tests**: `test_<module_name>.py`
- **Integration Tests**: `test_<feature>_integration.py`
- **Performance Tests**: `test_<component>_performance.py`
- **CLI Tests**: `test_cli_<command>.py`

## Running Tests

### Quick Start
```bash
# Run all tests
uv run python tests/run_all_tests.py

# Run specific test categories
uv run python tests/run_all_tests.py unit
uv run python tests/run_all_tests.py integration
uv run python tests/run_all_tests.py performance
uv run python tests/run_all_tests.py cli

# Run with pattern matching
uv run python tests/run_all_tests.py --pattern "test_base"
```

### Direct Pytest Commands
```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test categories
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v
uv run pytest tests/performance/ -v

# Run specific test files
uv run pytest tests/unit/core/test_base.py -v

# Run tests matching pattern
uv run pytest tests/ -k "test_base" -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html
```

### Parallel Execution
```bash
# Run tests in parallel
uv run pytest tests/ -n auto

# Specify number of workers
uv run pytest tests/ -n 4

# Run with performance optimization
uv run pytest tests/ -n auto --dist=loadfile
```

## Unit Testing

### Test Structure
```python
# tests/unit/core/test_base.py
import pytest
from src.core.base import BaseComponent

class TestBaseComponent:
    """Test cases for BaseComponent class."""
    
    def test_initialization(self):
        """Test component initialization."""
        config = {"test": "value"}
        component = BaseComponent("test_component", config)
        
        assert component.name == "test_component"
        assert component.config == config
        assert component.created_at is not None
    
    def test_string_representation(self):
        """Test string representation."""
        component = BaseComponent("test_component", {})
        str_repr = str(component)
        
        assert "test_component" in str_repr
        assert "BaseComponent" in str_repr
    
    @pytest.mark.parametrize("invalid_name", ["", None, 123])
    def test_invalid_name_raises_error(self, invalid_name):
        """Test that invalid names raise appropriate errors."""
        with pytest.raises(ValueError):
            BaseComponent(invalid_name, {})
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test with valid config
        valid_config = {"setting": "value"}
        component = BaseComponent("test", valid_config)
        assert component.config == valid_config
        
        # Test with invalid config
        with pytest.raises(ValueError):
            BaseComponent("test", None)
```

### Test Fixtures
```python
# tests/conftest.py
import pytest
import pandas as pd
from datetime import datetime, timedelta

@pytest.fixture
def sample_ohlcv_data():
    """Provide sample OHLCV data for testing."""
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=100),
        end=datetime.now(),
        freq='1H'
    )
    
    data = pd.DataFrame({
        'open': [100 + i * 0.1 for i in range(len(dates))],
        'high': [101 + i * 0.1 for i in range(len(dates))],
        'low': [99 + i * 0.1 for i in range(len(dates))],
        'close': [100.5 + i * 0.1 for i in range(len(dates))],
        'volume': [1000 + i * 10 for i in range(len(dates))]
    }, index=dates)
    
    return data

@pytest.fixture
def mock_config():
    """Provide mock configuration for testing."""
    return {
        "data": {"cache_dir": "/tmp/test_cache"},
        "analysis": {"default_timeframe": "1H"},
        "ml": {"default_algorithm": "random_forest"}
    }

@pytest.fixture
def temp_file(tmp_path):
    """Provide temporary file for testing."""
    return tmp_path / "test_data.csv"
```

### Mocking and Patching
```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.data.sources.base import BaseDataSource

class TestBaseDataSource:
    """Test cases for BaseDataSource class."""
    
    def test_fetch_data_with_mock(self):
        """Test data fetching with mocked dependencies."""
        # Create mock data
        mock_data = pd.DataFrame({'test': [1, 2, 3]})
        
        # Mock the data source
        with patch.object(BaseDataSource, 'fetch_data', return_value=mock_data):
            source = BaseDataSource("mock_source", {})
            result = source.fetch_data()
            
            assert result.equals(mock_data)
    
    def test_external_api_call(self):
        """Test external API calls with mocking."""
        with patch('requests.get') as mock_get:
            # Configure mock response
            mock_response = Mock()
            mock_response.json.return_value = {"data": "test"}
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            # Test the function that makes API call
            result = fetch_from_api("test_url")
            assert result == {"data": "test"}
    
    def test_file_operations(self, tmp_path):
        """Test file operations with temporary files."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        # Test file reading
        with open(test_file, 'r') as f:
            content = f.read()
        
        assert content == "test content"
```

## Integration Testing

### Component Integration Tests
```python
# tests/integration/test_data_pipeline.py
import pytest
from src.data.sources.csv import CSVDataSource
from src.data.processors.cleaner import DataCleaner
from src.analysis.indicators.trend import MovingAverage

class TestDataPipeline:
    """Test data processing pipeline integration."""
    
    def test_end_to_end_pipeline(self, sample_ohlcv_data, temp_file):
        """Test complete data processing pipeline."""
        # Save sample data to temporary file
        sample_ohlcv_data.to_csv(temp_file)
        
        # Create pipeline components
        source = CSVDataSource(str(temp_file), {})
        cleaner = DataCleaner({})
        indicator = MovingAverage(20, {})
        
        # Execute pipeline
        raw_data = source.fetch_data()
        clean_data = cleaner.process_data(raw_data)
        sma_values = indicator.calculate(clean_data['close'])
        
        # Verify results
        assert not clean_data.empty
        assert not sma_values.empty
        assert len(sma_values) == len(clean_data)
        assert sma_values.iloc[-1] is not None
    
    def test_ml_training_pipeline(self, sample_ohlcv_data):
        """Test machine learning training pipeline."""
        from src.ml.models.regression import RandomForestModel
        from src.ml.features.technical import TechnicalFeatures
        
        # Create ML components
        feature_engineer = TechnicalFeatures({})
        model = RandomForestModel({})
        
        # Prepare data
        features = feature_engineer.create_features(sample_ohlcv_data)
        target = sample_ohlcv_data['close'].shift(-1).dropna()
        features = features.iloc[:-1]  # Align with target
        
        # Train model
        model.train(features, target)
        
        # Verify training
        assert model.is_trained
        assert model.model is not None
        
        # Test prediction
        predictions = model.predict(features.iloc[-10:])
        assert len(predictions) == 10
        assert all(not pd.isna(pred) for pred in predictions)
```

### System Integration Tests
```python
# tests/integration/test_system_integration.py
import pytest
from src.cli.core.cli import CLI
from src.core.config import Config

class TestSystemIntegration:
    """Test system-wide integration."""
    
    def test_cli_with_real_data(self, sample_ohlcv_data, temp_file):
        """Test CLI with actual data processing."""
        # Save sample data
        sample_ohlcv_data.to_csv(temp_file)
        
        # Initialize CLI
        cli = CLI()
        
        # Test analyze command
        result = cli.run(['analyze', '--data', str(temp_file), '--indicators', 'sma'])
        
        # Verify command execution
        assert result is not None
        assert result.success
    
    def test_configuration_integration(self):
        """Test configuration system integration."""
        # Load configuration
        config = Config()
        
        # Test configuration access
        cache_dir = config.get("data.cache_dir")
        assert cache_dir is not None
        
        # Test configuration update
        config.set("test.setting", "test_value")
        assert config.get("test.setting") == "test_value"
        
        # Test configuration persistence
        config.save()
        new_config = Config()
        assert new_config.get("test.setting") == "test_value"
```

## Performance Testing

### Performance Test Structure
```python
# tests/performance/test_data_processing_performance.py
import pytest
import time
import pandas as pd
from src.data.processors.cleaner import DataCleaner

class TestDataProcessingPerformance:
    """Performance tests for data processing."""
    
    @pytest.mark.performance
    def test_large_dataset_processing(self):
        """Test processing performance with large datasets."""
        # Create large dataset
        large_data = pd.DataFrame({
            'value': range(100000),
            'category': ['A', 'B', 'C'] * 33334
        })
        
        cleaner = DataCleaner({})
        
        # Measure processing time
        start_time = time.time()
        result = cleaner.process_data(large_data)
        processing_time = time.time() - start_time
        
        # Performance assertions
        assert processing_time < 5.0  # Should complete within 5 seconds
        assert len(result) == len(large_data)
        
        # Log performance metrics
        print(f"Processed {len(large_data)} rows in {processing_time:.2f} seconds")
        print(f"Processing rate: {len(large_data)/processing_time:.0f} rows/second")
    
    @pytest.mark.performance
    def test_memory_usage(self):
        """Test memory usage during processing."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process large dataset
        large_data = pd.DataFrame({
            'value': range(50000),
            'category': ['A', 'B', 'C'] * 16667
        })
        
        cleaner = DataCleaner({})
        result = cleaner.process_data(large_data)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory assertions
        assert memory_increase < 100  # Should not increase by more than 100MB
        
        print(f"Memory usage: {initial_memory:.1f}MB -> {final_memory:.1f}MB")
        print(f"Memory increase: {memory_increase:.1f}MB")
    
    @pytest.mark.performance
    def test_concurrent_processing(self):
        """Test concurrent processing performance."""
        from concurrent.futures import ThreadPoolExecutor
        import numpy as np
        
        # Create multiple datasets
        datasets = [
            pd.DataFrame({'value': range(10000) + i * 1000})
            for i in range(5)
        ]
        
        cleaner = DataCleaner({})
        
        # Process sequentially
        start_time = time.time()
        sequential_results = [cleaner.process_data(data) for data in datasets]
        sequential_time = time.time() - start_time
        
        # Process concurrently
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            concurrent_results = list(executor.map(cleaner.process_data, datasets))
        concurrent_time = time.time() - start_time
        
        # Performance assertions
        assert concurrent_time < sequential_time
        assert len(concurrent_results) == len(sequential_results)
        
        print(f"Sequential time: {sequential_time:.2f}s")
        print(f"Concurrent time: {concurrent_time:.2f}s")
        print(f"Speedup: {sequential_time/concurrent_time:.2f}x")
```

### Benchmark Tests
```python
# tests/performance/test_benchmarks.py
import pytest
import time
from src.analysis.indicators.trend import MovingAverage

class TestBenchmarks:
    """Benchmark tests for critical operations."""
    
    @pytest.mark.benchmark
    def test_moving_average_calculation(self, benchmark):
        """Benchmark moving average calculation."""
        import numpy as np
        
        # Create test data
        data = pd.Series(np.random.random(10000))
        
        def calculate_sma():
            return MovingAverage(20, {}).calculate(data)
        
        # Run benchmark
        result = benchmark(calculate_sma)
        
        # Verify result
        assert len(result) == len(data)
        assert not result.isna().all()
    
    @pytest.mark.benchmark
    def test_dataframe_operations(self, benchmark):
        """Benchmark DataFrame operations."""
        import numpy as np
        
        # Create large DataFrame
        df = pd.DataFrame({
            'A': np.random.random(100000),
            'B': np.random.random(100000),
            'C': np.random.random(100000)
        })
        
        def perform_operations():
            result = df.copy()
            result['D'] = result['A'] + result['B']
            result['E'] = result['C'] * 2
            result['F'] = result['D'] / result['E']
            return result
        
        # Run benchmark
        result = benchmark(perform_operations)
        
        # Verify result
        assert len(result) == 100000
        assert 'F' in result.columns
```

## CLI Testing

### CLI Command Tests
```python
# tests/unit/cli/test_cli.py
import pytest
from unittest.mock import patch, MagicMock
from src.cli.core.cli import CLI

class TestCLI:
    """Test CLI functionality."""
    
    def test_cli_initialization(self):
        """Test CLI initialization."""
        cli = CLI()
        assert cli is not None
        assert hasattr(cli, 'parser')
    
    def test_help_command(self):
        """Test help command."""
        cli = CLI()
        
        # Test global help
        with patch('sys.argv', ['neozork', '--help']):
            result = cli.run()
            assert result is not None
        
        # Test command-specific help
        with patch('sys.argv', ['neozork', 'analyze', '--help']):
            result = cli.run()
            assert result is not None
    
    def test_version_command(self):
        """Test version command."""
        cli = CLI()
        
        with patch('sys.argv', ['neozork', '--version']):
            result = cli.run()
            assert result is not None
    
    def test_analyze_command(self):
        """Test analyze command."""
        cli = CLI()
        
        with patch('sys.argv', ['neozork', 'analyze', '--data', 'test.csv']):
            result = cli.run()
            assert result is not None
    
    def test_invalid_command(self):
        """Test invalid command handling."""
        cli = CLI()
        
        with patch('sys.argv', ['neozork', 'invalid_command']):
            result = cli.run()
            assert result is not None
            # Should handle invalid command gracefully
```

### CLI Integration Tests
```python
# tests/integration/test_cli_integration.py
import pytest
import subprocess
import tempfile
import os
from src.cli.core.cli import CLI

class TestCLIIntegration:
    """Test CLI integration with real commands."""
    
    def test_cli_with_real_file(self, sample_ohlcv_data):
        """Test CLI with actual data file."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_ohlcv_data.to_csv(f.name)
            temp_file = f.name
        
        try:
            # Test CLI with real file
            cli = CLI()
            result = cli.run(['analyze', '--data', temp_file, '--indicators', 'sma'])
            
            # Verify execution
            assert result is not None
            
        finally:
            # Cleanup
            os.unlink(temp_file)
    
    def test_cli_subprocess(self, sample_ohlcv_data):
        """Test CLI as subprocess."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_ohlcv_data.to_csv(f.name)
            temp_file = f.name
        
        try:
            # Run CLI as subprocess
            result = subprocess.run([
                'uv', 'run', 'python', '-m', 'src.cli.core.cli',
                'analyze', '--data', temp_file, '--indicators', 'sma'
            ], capture_output=True, text=True)
            
            # Verify execution
            assert result.returncode == 0
            assert 'analysis' in result.stdout.lower()
            
        finally:
            # Cleanup
            os.unlink(temp_file)
```

## Test Configuration

### Pytest Configuration
```ini
# pytest.ini
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
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    -n auto
markers =
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests
    slow: Slow running tests
    cli: CLI tests
    ml: Machine learning tests
    data: Data processing tests
    analysis: Analysis tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### Coverage Configuration
```ini
# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */test_*
    */__pycache__/*
    */venv/*
    */.venv/*
    */env/*
    */.env/*

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

[html]
directory = coverage_html
title = Neozork HLD Prediction Coverage Report

[xml]
output = coverage.xml
```

## Test Data Management

### Test Data Fixtures
```python
# tests/conftest.py
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@pytest.fixture(scope="session")
def large_test_dataset():
    """Provide large test dataset for performance testing."""
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=365),
        end=datetime.now(),
        freq='1H'
    )
    
    data = pd.DataFrame({
        'open': np.random.random(len(dates)) * 100 + 50,
        'high': np.random.random(len(dates)) * 100 + 50,
        'low': np.random.random(len(dates)) * 100 + 50,
        'close': np.random.random(len(dates)) * 100 + 50,
        'volume': np.random.randint(1000, 10000, len(dates))
    }, index=dates)
    
    return data

@pytest.fixture(scope="function")
def small_test_dataset():
    """Provide small test dataset for unit testing."""
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=10),
        end=datetime.now(),
        freq='1H'
    )
    
    data = pd.DataFrame({
        'open': [100 + i * 0.1 for i in range(len(dates))],
        'high': [101 + i * 0.1 for i in range(len(dates))],
        'low': [99 + i * 0.1 for i in range(len(dates))],
        'close': [100.5 + i * 0.1 for i in range(len(dates))],
        'volume': [1000 + i * 10 for i in range(len(dates))]
    }, index=dates)
    
    return data

@pytest.fixture(scope="session")
def mock_api_responses():
    """Provide mock API responses for testing."""
    return {
        "success": {"status": "success", "data": [1, 2, 3]},
        "error": {"status": "error", "message": "API error"},
        "empty": {"status": "success", "data": []}
    }
```

### Test Data Cleanup
```python
# tests/conftest.py
import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture(scope="function")
def temp_directory():
    """Provide temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="function")
def temp_file_factory(temp_directory):
    """Provide temporary file factory."""
    def create_temp_file(suffix=".txt", content=""):
        temp_file = Path(temp_directory) / f"test_file{suffix}"
        temp_file.write_text(content)
        return temp_file
    
    return create_temp_file
```

## Continuous Integration Testing

### GitHub Actions Test Workflow
```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
        test-type: [unit, integration, performance]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install UV
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
    
    - name: Install dependencies
      run: uv sync --frozen-lockfile
    
    - name: Run ${{ matrix.test-type }} tests
      run: |
        if [ "${{ matrix.test-type }}" = "unit" ]; then
          uv run pytest tests/unit/ --cov=src --cov-report=xml
        elif [ "${{ matrix.test-type }}" = "integration" ]; then
          uv run pytest tests/integration/ --cov=src --cov-report=xml
        else
          uv run pytest tests/performance/ --cov=src --cov-report=xml
        fi
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Pre-commit Testing
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
        stages: [commit]
        args: [tests/unit/, -v, --tb=short]
```

## Test Reporting and Monitoring

### Coverage Reports
```bash
# Generate HTML coverage report
uv run pytest tests/ --cov=src --cov-report=html

# Generate XML coverage report
uv run pytest tests/ --cov=src --cov-report=xml

# Generate terminal coverage report
uv run pytest tests/ --cov=src --cov-report=term-missing

# Generate all coverage reports
uv run pytest tests/ --cov=src --cov-report=html --cov-report=xml --cov-report=term-missing
```

### Test Results Summary
```bash
# Run tests with summary
uv run pytest tests/ --tb=short -q

# Generate JUnit XML report
uv run pytest tests/ --junitxml=test-results.xml

# Generate test report
uv run pytest tests/ --html=test-report.html --self-contained-html
```

## Troubleshooting Tests

### Common Test Issues

#### Import Errors
```bash
# Check Python path
uv run python -c "import sys; print(sys.path)"

# Check package installation
uv run python -c "import src; print(src.__file__)"

# Reinstall package
uv run pip install -e .
```

#### Test Failures
```bash
# Run specific failing test
uv run pytest tests/unit/core/test_base.py::TestBaseComponent::test_initialization -v -s

# Debug test with pdb
uv run pytest tests/unit/core/test_base.py::TestBaseComponent::test_initialization -v -s --pdb

# Run with maximum verbosity
uv run pytest tests/unit/core/test_base.py::TestBaseComponent::test_initialization -vvv -s
```

#### Performance Test Issues
```bash
# Run performance tests separately
uv run pytest tests/performance/ -v -s

# Skip slow tests
uv run pytest tests/ -m "not slow" -v

# Run with performance profiling
uv run pytest tests/performance/ --durations=10
```

### Test Debugging
```python
# Add debugging to tests
import pdb

def test_debug_function():
    """Test with debugging."""
    # Set breakpoint
    pdb.set_trace()
    
    # Test logic here
    result = function_to_test()
    
    # Assertions
    assert result is not None
```

## Best Practices

### Test Design
1. **Arrange-Act-Assert**: Structure tests clearly
2. **Single Responsibility**: Each test tests one thing
3. **Descriptive Names**: Use clear test names
4. **Proper Setup/Teardown**: Use fixtures appropriately
5. **Mock External Dependencies**: Isolate unit tests

### Test Maintenance
1. **Keep Tests Fast**: Avoid slow operations in unit tests
2. **Use Appropriate Scopes**: Choose fixture scopes wisely
3. **Clean Test Data**: Ensure tests don't leave artifacts
4. **Update Tests**: Keep tests in sync with code changes
5. **Review Test Coverage**: Regularly check coverage reports

### Performance Testing
1. **Baseline Measurements**: Establish performance baselines
2. **Realistic Data**: Use realistic test data sizes
3. **Environment Consistency**: Test in consistent environments
4. **Regression Detection**: Monitor for performance regressions
5. **Resource Monitoring**: Track memory and CPU usage

## Support and Resources

### Testing Resources
- **Pytest Documentation**: https://docs.pytest.org/
- **Coverage.py**: https://coverage.readthedocs.io/
- **Pytest-xdist**: https://pytest-xdist.readthedocs.io/
- **Pytest-cov**: https://pytest-cov.readthedocs.io/

### Getting Help
- **Test Issues**: Check test output and error messages
- **Coverage Issues**: Review coverage reports
- **Performance Issues**: Use profiling tools
- **Community**: GitHub Issues and Discussions
