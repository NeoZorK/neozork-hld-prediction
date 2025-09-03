# Development Guide

## Overview

This guide provides comprehensive information for developers working on the Neozork HLD Prediction system, including development setup, coding standards, testing practices, and contribution guidelines.

## Development Environment Setup

### Prerequisites
- **Python**: 3.9+ (3.11+ recommended)
- **UV**: Python package manager
- **Git**: Version control
- **IDE**: VS Code, PyCharm, or similar with Python support

### Initial Setup
```bash
# Clone repository
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction

# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Verify installation
uv run pytest tests/ -v
```

### Development Dependencies
```bash
# Install development dependencies
uv sync --group dev

# Install additional tools
uv add --dev black isort mypy flake8 ruff pytest-cov pytest-xdist
```

## Project Structure

### Source Code Organization
```
src/
├── core/           # Core functionality and interfaces
│   ├── base.py     # Base classes
│   ├── config.py   # Configuration management
│   ├── exceptions.py # Exception hierarchy
│   └── interfaces.py # Abstract interfaces
├── data/           # Data handling
│   ├── sources/    # Data sources
│   ├── processors/ # Data processors
│   ├── storage/    # Data storage
│   └── validation/ # Data validation
├── analysis/       # Analysis engine
│   ├── indicators/ # Technical indicators
│   ├── statistics/ # Statistical analysis
│   ├── patterns/   # Pattern recognition
│   └── pipeline/   # Analysis pipelines
├── ml/             # Machine learning
│   ├── models/     # ML models
│   ├── features/   # Feature engineering
│   ├── training/   # Training pipelines
│   └── evaluation/ # Model evaluation
├── cli/            # Command line interface
│   ├── core/       # CLI core functionality
│   ├── commands/   # Command implementations
│   └── parsers/    # Argument parsers
└── utils/          # Utility functions
    ├── file_utils.py
    ├── math_utils.py
    └── time_utils.py
```

### Test Organization
```
tests/
├── unit/           # Unit tests
│   ├── core/       # Core module tests
│   ├── data/       # Data module tests
│   ├── analysis/   # Analysis module tests
│   ├── ml/         # ML module tests
│   ├── cli/        # CLI module tests
│   └── utils/      # Utility tests
├── integration/    # Integration tests
├── performance/    # Performance tests
└── conftest.py     # Test configuration
```

## Coding Standards

### Python Style Guide
- **PEP 8**: Follow Python style guide
- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Line Length**: Maximum 88 characters (Black formatter default)

### Code Formatting
```bash
# Format code with Black
uv run black src/ tests/

# Sort imports with isort
uv run isort src/ tests/

# Check code formatting
uv run black --check src/ tests/
uv run isort --check-only src/ tests/
```

### Linting and Type Checking
```bash
# Run linting with flake8
uv run flake8 src/ tests/

# Run fast linting with ruff
uv run ruff check src/ tests/

# Run type checking with mypy
uv run mypy src/

# Fix issues automatically
uv run ruff check --fix src/ tests/
```

### Code Quality Tools
```bash
# Run all quality checks
uv run black --check src/ tests/
uv run isort --check-only src/ tests/
uv run mypy src/
uv run ruff check src/ tests/
uv run flake8 src/ tests/
```

## Development Workflow

### Feature Development
1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Implement Feature**
   - Write code following coding standards
   - Add comprehensive tests
   - Update documentation

3. **Test Implementation**
   ```bash
   # Run unit tests
   uv run pytest tests/unit/ -v
   
   # Run specific test file
   uv run pytest tests/unit/core/test_base.py -v
   
   # Run with coverage
   uv run pytest tests/unit/ --cov=src --cov-report=html
   ```

4. **Code Quality Check**
   ```bash
   # Run all quality checks
   uv run black src/ tests/
   uv run isort src/ tests/
   uv run mypy src/
   uv run ruff check src/ tests/
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/new-feature-name
   # Create Pull Request on GitHub
   ```

### Bug Fixes
1. **Create Bug Fix Branch**
   ```bash
   git checkout -b fix/bug-description
   ```

2. **Fix Bug**
   - Identify root cause
   - Implement fix
   - Add regression test

3. **Test Fix**
   ```bash
   # Run specific test for the bug
   uv run pytest tests/unit/ -k "test_bug_description"
   
   # Run all tests to ensure no regressions
   uv run pytest tests/unit/ -v
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "fix: resolve bug description"
   git push origin fix/bug-description
   ```

## Testing Practices

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
```

### Test Categories

#### Unit Tests
- **Purpose**: Test individual components in isolation
- **Scope**: Single function, method, or class
- **Dependencies**: Mock external dependencies
- **Execution**: Fast, can run in parallel

#### Integration Tests
- **Purpose**: Test component interactions
- **Scope**: Multiple components working together
- **Dependencies**: Real or test dependencies
- **Execution**: Slower, may require setup

#### Performance Tests
- **Purpose**: Ensure performance requirements are met
- **Scope**: End-to-end workflows
- **Dependencies**: Real data and dependencies
- **Execution**: Slowest, run separately

### Test Data Management
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
```

### Test Execution Strategies

#### Quick Development Tests
```bash
# Run only unit tests (fastest)
uv run pytest tests/unit/ -v

# Run specific module tests
uv run pytest tests/unit/core/ -v

# Run tests matching pattern
uv run pytest tests/unit/ -k "test_base" -v
```

#### Comprehensive Testing
```bash
# Run all tests with coverage
uv run pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run tests in parallel
uv run pytest tests/ -n auto

# Run tests with verbose output
uv run pytest tests/ -v -s
```

#### Performance Testing
```bash
# Run only performance tests
uv run pytest tests/performance/ -v

# Run with performance profiling
uv run pytest tests/performance/ --durations=10
```

## Code Quality Standards

### Documentation Standards
```python
class TechnicalIndicator(BaseComponent):
    """
    Base class for technical indicators.
    
    This class provides the foundation for all technical indicators
    in the system, including common functionality for parameter
    validation, calculation, and result formatting.
    
    Attributes:
        name (str): The name of the indicator
        config (dict): Configuration parameters
        period (int): Calculation period for the indicator
        
    Example:
        >>> indicator = MovingAverage(20, {"name": "SMA"})
        >>> result = indicator.calculate(price_data)
    """
    
    def __init__(self, period: int, config: dict):
        """
        Initialize the technical indicator.
        
        Args:
            period: The calculation period for the indicator
            config: Configuration dictionary containing indicator parameters
            
        Raises:
            ValueError: If period is less than 2
            ConfigError: If required configuration is missing
        """
        super().__init__(f"technical_indicator_{period}", config)
        self.period = period
        self._validate_parameters()
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """
        Calculate the indicator values.
        
        Args:
            data: Input data containing OHLCV information
            
        Returns:
            Series containing calculated indicator values
            
        Raises:
            DataError: If input data is invalid or insufficient
            CalculationError: If calculation fails
        """
        # Implementation here
        pass
```

### Error Handling Standards
```python
from src.core.exceptions import DataError, ValidationError, CalculationError

def calculate_indicator(data: pd.DataFrame, period: int) -> pd.Series:
    """
    Calculate technical indicator with proper error handling.
    
    Args:
        data: Input data for calculation
        period: Calculation period
        
    Returns:
        Calculated indicator values
        
    Raises:
        DataError: For data-related issues
        ValidationError: For parameter validation issues
        CalculationError: For calculation failures
    """
    try:
        # Validate input data
        if data.empty:
            raise DataError("Input data is empty")
        
        if len(data) < period:
            raise DataError(f"Insufficient data: need {period}, got {len(data)}")
        
        # Validate parameters
        if period < 2:
            raise ValidationError("Period must be at least 2")
        
        # Perform calculation
        result = perform_calculation(data, period)
        
        if result is None or result.empty:
            raise CalculationError("Calculation produced no results")
        
        return result
        
    except (DataError, ValidationError, CalculationError):
        # Re-raise specific errors
        raise
    except Exception as e:
        # Wrap unexpected errors
        raise CalculationError(f"Unexpected error during calculation: {e}") from e
```

### Performance Standards
```python
import time
from functools import wraps
from src.core.exceptions import PerformanceError

def performance_monitor(threshold_seconds: float = 1.0):
    """
    Decorator to monitor function performance.
    
    Args:
        threshold_seconds: Maximum allowed execution time
        
    Raises:
        PerformanceError: If execution exceeds threshold
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                execution_time = time.time() - start_time
                if execution_time > threshold_seconds:
                    raise PerformanceError(
                        f"Function {func.__name__} exceeded performance threshold: "
                        f"{execution_time:.2f}s > {threshold_seconds}s"
                    )
                
                return result
                
            except PerformanceError:
                raise
            except Exception as e:
                # Log performance issue but don't fail on other errors
                logger.warning(
                    f"Performance monitoring failed for {func.__name__}: {e}"
                )
                return func(*args, **kwargs)
        
        return wrapper
    return decorator

# Usage
@performance_monitor(threshold_seconds=0.5)
def fast_calculation(data: pd.DataFrame) -> pd.Series:
    """Perform fast calculation with performance monitoring."""
    return data.rolling(window=20).mean()
```

## Development Tools

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
        
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: uv run pytest
        language: system
        pass_filenames: false
        always_run: true
```

### IDE Configuration

#### VS Code Settings
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

#### PyCharm Configuration
- **Project Interpreter**: Set to `.venv/bin/python`
- **Code Style**: Configure to use Black formatter
- **Inspections**: Enable all Python inspections
- **Testing**: Configure pytest as test runner

### Debugging Tools
```python
import logging
import pdb
from src.core.config import Config

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug mode in configuration
config = Config()
config.set("development.debug_mode", True)

# Add breakpoints for debugging
def debug_function(data):
    """Function with debugging support."""
    # Set breakpoint
    pdb.set_trace()
    
    # Process data
    result = process_data(data)
    
    # Log debug information
    logger.debug(f"Input data shape: {data.shape}")
    logger.debug(f"Result shape: {result.shape}")
    
    return result
```

## Code Review Guidelines

### Review Checklist
- [ ] **Functionality**: Does the code work as intended?
- [ ] **Tests**: Are there comprehensive tests?
- [ ] **Documentation**: Is the code well-documented?
- [ ] **Style**: Does the code follow style guidelines?
- [ ] **Performance**: Is the code performant?
- [ ] **Security**: Are there any security concerns?
- [ ] **Error Handling**: Is error handling appropriate?
- [ ] **Dependencies**: Are dependencies appropriate?

### Review Comments
```python
# Good review comment
# Consider adding input validation here to prevent potential errors

# Better review comment
# Add input validation for the 'period' parameter:
# if period < 2:
#     raise ValueError("Period must be at least 2")

# Best review comment
# The 'period' parameter should be validated to prevent runtime errors.
# Consider adding this validation at the beginning of the method:
# 
# if not isinstance(period, int) or period < 2:
#     raise ValueError("Period must be a positive integer >= 2")
# 
# This would catch invalid inputs early and provide clear error messages.
```

## Performance Optimization

### Profiling Tools
```bash
# Install profiling tools
uv add --dev cProfile line_profiler memory_profiler

# Profile with cProfile
uv run python -m cProfile -o profile.stats script.py

# Analyze profile results
uv run python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative')
p.print_stats(20)
"

# Line-by-line profiling
uv run python -m line_profiler script.py

# Memory profiling
uv run python -m memory_profiler script.py
```

### Optimization Techniques
```python
# Use vectorized operations instead of loops
# Before (slow)
def calculate_sma_slow(prices, period):
    result = []
    for i in range(len(prices)):
        if i < period - 1:
            result.append(None)
        else:
            window = prices[i-period+1:i+1]
            result.append(sum(window) / period)
    return result

# After (fast)
def calculate_sma_fast(prices, period):
    return prices.rolling(window=period).mean()

# Use caching for expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(parameters):
    # Expensive computation
    return result

# Use parallel processing for large datasets
from concurrent.futures import ProcessPoolExecutor
import numpy as np

def parallel_process(data_chunks):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_chunk, data_chunks))
    return np.concatenate(results)
```

## Security Considerations

### Input Validation
```python
import re
from src.core.exceptions import ValidationError

def validate_file_path(file_path: str) -> str:
    """
    Validate and sanitize file path.
    
    Args:
        file_path: Input file path
        
    Returns:
        Sanitized file path
        
    Raises:
        ValidationError: If path is invalid or unsafe
    """
    if not file_path or not isinstance(file_path, str):
        raise ValidationError("File path must be a non-empty string")
    
    # Check for path traversal attempts
    if ".." in file_path or file_path.startswith("/"):
        raise ValidationError("Invalid file path")
    
    # Sanitize path
    sanitized = re.sub(r'[^\w\-_./]', '', file_path)
    
    if not sanitized:
        raise ValidationError("File path contains no valid characters")
    
    return sanitized

def validate_numeric_input(value, min_val=None, max_val=None):
    """
    Validate numeric input values.
    
    Args:
        value: Input value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Validated numeric value
        
    Raises:
        ValidationError: If value is invalid
    """
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"Value must be numeric, got: {value}")
    
    if min_val is not None and num_value < min_val:
        raise ValidationError(f"Value must be >= {min_val}, got: {num_value}")
    
    if max_val is not None and num_value > max_val:
        raise ValidationError(f"Value must be <= {max_val}, got: {num_value}")
    
    return num_value
```

### Secure Configuration
```python
import os
from pathlib import Path

class SecureConfig:
    """Secure configuration management."""
    
    def __init__(self):
        self.config_dir = Path.home() / ".neozork"
        self.config_file = self.config_dir / "config.json"
        
        # Ensure secure permissions
        self._ensure_secure_permissions()
    
    def _ensure_secure_permissions(self):
        """Ensure configuration files have secure permissions."""
        if self.config_dir.exists():
            # Set directory permissions to 700 (user only)
            self.config_dir.chmod(0o700)
        
        if self.config_file.exists():
            # Set file permissions to 600 (user read/write only)
            self.config_file.chmod(0o600)
    
    def load_config(self):
        """Load configuration with security checks."""
        if not self.config_file.exists():
            return self._get_default_config()
        
        # Verify file permissions
        stat = self.config_file.stat()
        if stat.st_mode & 0o777 != 0o600:
            raise SecurityError("Configuration file has insecure permissions")
        
        # Load and validate configuration
        config = self._load_json_file(self.config_file)
        return self._validate_config(config)
```

## Continuous Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: Continuous Integration

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
    
    - name: Run linting
      run: |
        uv run black --check src/ tests/
        uv run isort --check-only src/ tests/
        uv run flake8 src/ tests/
        uv run mypy src/
    
    - name: Run tests
      run: |
        uv run pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Pre-commit Configuration
```bash
# Install pre-commit
uv add --dev pre-commit

# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files

# Run specific hook
uv run pre-commit run black --all-files
```

## Troubleshooting

### Common Development Issues

#### Import Errors
```bash
# Check Python path
uv run python -c "import sys; print(sys.path)"

# Check package installation
uv run python -c "import src; print(src.__file__)"

# Reinstall package in development mode
uv run pip install -e .
```

#### Test Failures
```bash
# Run tests with verbose output
uv run pytest tests/ -v -s

# Run specific failing test
uv run pytest tests/unit/core/test_base.py::TestBaseComponent::test_initialization -v -s

# Debug test with pdb
uv run pytest tests/unit/core/test_base.py::TestBaseComponent::test_initialization -v -s --pdb
```

#### Performance Issues
```bash
# Profile specific function
uv run python -m cProfile -o profile.stats -m pytest tests/unit/ -k "test_performance"

# Analyze memory usage
uv run python -m memory_profiler script.py

# Check for memory leaks
uv run python -m tracemalloc script.py
```

### Getting Help
- **Documentation**: Check `docs/` directory
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Wiki**: Project wiki for common problems
- **Code Examples**: Review test files and examples

## Contributing Guidelines

### Contribution Process
1. **Fork Repository**: Create your own fork
2. **Create Branch**: Create feature/fix branch
3. **Make Changes**: Implement your changes
4. **Add Tests**: Ensure comprehensive test coverage
5. **Update Documentation**: Update relevant documentation
6. **Submit PR**: Create pull request with clear description

### Code Review Process
1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Peer Review**: At least one maintainer reviews code
3. **Address Feedback**: Respond to review comments
4. **Merge**: Code is merged after approval

### Release Process
1. **Version Bump**: Update version in `pyproject.toml`
2. **Changelog**: Update `CHANGELOG.md`
3. **Tag Release**: Create git tag for version
4. **Deploy**: Automated deployment to PyPI

## Support and Resources

### Development Resources
- **Python Documentation**: https://docs.python.org/
- **Pytest Documentation**: https://docs.pytest.org/
- **Black Formatter**: https://black.readthedocs.io/
- **MyPy Type Checker**: https://mypy.readthedocs.io/

### Community
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share ideas
- **Contributor Guidelines**: Follow project contribution standards
- **Code of Conduct**: Maintain respectful development environment
