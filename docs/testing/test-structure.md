# Test Structure

This document describes the organization and structure of the test suite in the neozork-hld-prediction project.

## Test Directory Organization

The test suite follows a hierarchical structure that mirrors the source code organization:

```
tests/
├── calculation/           # Tests for calculation modules
│   └── indicators/       # Tests for technical indicators
│       ├── trend/        # Tests for trend indicators
│       │   ├── test_ma_line.py           # MA line indicator tests
│       │   ├── test_test_ma_line.py      # MA line functionality tests
│       │   ├── test_sma_indicator.py     # SMA indicator tests
│       │   ├── test_ema_indicator.py     # EMA indicator tests
│       │   ├── test_adx_indicator.py     # ADX indicator tests
│       │   ├── test_sar_indicator.py     # SAR indicator tests
│       │   ├── test_supertrend_indicator.py # SuperTrend indicator tests
│       │   └── test_wave_ind.py          # Wave indicator tests
│       ├── momentum/     # Tests for momentum indicators
│       ├── oscillators/  # Tests for oscillator indicators
│       ├── volatility/   # Tests for volatility indicators
│       ├── volume/       # Tests for volume indicators
│       ├── sentiment/    # Tests for sentiment indicators
│       ├── support-resistance/ # Tests for support/resistance indicators
│       ├── predictive/   # Tests for predictive indicators
│       └── probability/  # Tests for probability indicators
├── cli/                  # Tests for command-line interface
├── data/                 # Tests for data processing
├── eda/                  # Tests for exploratory data analysis
├── export/               # Tests for export functionality
├── plotting/             # Tests for visualization
├── scripts/              # Tests for utility scripts
│   ├── test_debug_wave_indicator.py      # Tests for wave indicator debug script
│   ├── test_debug_signals_analysis.py    # Tests for signals analysis debug script
│   └── test_check_mcp_status.py          # Tests for MCP status checking
├── workflow/             # Tests for workflow management
└── integration/          # Integration tests
```

## Test File Naming Conventions

- **`test_<module_name>.py`** - Tests for specific modules
- **`test_<feature>_<aspect>.py`** - Tests for specific features or aspects
- **`test_<indicator_type>_indicator.py`** - Tests for technical indicators

## Test Categories

### 1. Unit Tests
- **Import tests** - Verify modules can be imported without errors
- **Functionality tests** - Test core module functionality
- **Edge case tests** - Test boundary conditions and error handling
- **Performance tests** - Test execution time and resource usage

### 2. Integration Tests
- **Module interaction tests** - Test how modules work together
- **Data flow tests** - Test data processing pipelines
- **API integration tests** - Test external service integrations

### 3. Debug Script Tests
- **File existence tests** - Ensure debug scripts exist and are accessible
- **Syntax validation tests** - Verify scripts have no syntax errors
- **Import dependency tests** - Test script dependencies and imports
- **Basic functionality tests** - Test script execution (when possible)

## Test Coverage Requirements

- **100% coverage** for all source files
- **Automatic coverage analysis** after test execution
- **Missing test detection** and reporting
- **Coverage reports** generated for each test run

## Running Tests

### All Tests
```bash
uv run pytest tests -n auto
```

### Specific Test Categories
```bash
# Trend indicator tests
uv run pytest tests/calculation/indicators/trend/ -n auto

# Debug script tests
uv run pytest tests/scripts/ -n auto

# All calculation tests
uv run pytest tests/calculation/ -n auto
```

### Coverage Analysis
```bash
uv run pytest tests --cov=src --cov-report=html
```

## Test Dependencies

All tests use the following testing framework:
- **pytest** - Main testing framework
- **pytest-cov** - Coverage reporting
- **pytest-xdist** - Parallel test execution
- **unittest.mock** - Mocking and patching

## Recent Changes

### File Reorganization (Latest Update)

The following files have been moved to improve test organization:

1. **`test_ma_line.py`** → `tests/calculation/indicators/trend/`
   - Contains MA line indicator tests
   - Now properly organized with other trend indicator tests

2. **`debug_wave_indicator.py`** → `scripts/debug/`
   - Debug script for wave indicator analysis
   - Moved to appropriate debug scripts directory

3. **`debug_signals_analysis.py`** → `scripts/debug/`
   - Debug script for signals analysis
   - Moved to appropriate debug scripts directory

### Test File Updates

All corresponding test files have been updated with:
- Correct import paths
- Updated file references
- Proper directory structure
- Maintained test coverage

## Best Practices

1. **Keep tests focused** - Each test should test one specific aspect
2. **Use descriptive names** - Test names should clearly indicate what is being tested
3. **Maintain test isolation** - Tests should not depend on each other
4. **Mock external dependencies** - Use mocks for external services and file I/O
5. **Test edge cases** - Include tests for error conditions and boundary values
6. **Update documentation** - Keep this document updated when adding new test categories
