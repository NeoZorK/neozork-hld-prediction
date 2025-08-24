# Project Structure

This document describes the structure of the neozork-hld-prediction project.

## Directory Structure

```
neozork-hld-prediction/
├── src/                    # Source code
│   ├── calculation/        # Technical indicators and calculations
│   ├── cli/               # Command-line interface
│   ├── common/            # Common utilities and constants
│   ├── data/              # Data acquisition and processing
│   ├── eda/               # Exploratory data analysis
│   ├── export/            # Data export functionality
│   ├── plotting/          # Visualization and plotting
│   ├── utils/             # Utility functions
│   └── workflow/          # Workflow management
├── tests/                 # Test suite
│   ├── calculation/       # Tests for calculations
│   │   └── indicators/    # Tests for technical indicators
│   │       ├── trend/     # Tests for trend indicators (MA, EMA, ADX, etc.)
│   │       ├── momentum/  # Tests for momentum indicators
│   │       ├── oscillators/ # Tests for oscillator indicators
│   │       └── volatility/ # Tests for volatility indicators
│   ├── cli/              # Tests for CLI
│   ├── data/             # Tests for data processing
│   ├── eda/              # Tests for EDA
│   ├── export/           # Tests for export
│   ├── plotting/         # Tests for plotting
│   ├── scripts/          # Tests for utility scripts
│   └── workflow/         # Tests for workflow
├── data/                  # Data files
│   ├── cache/            # Cached data
│   ├── indicators/       # Calculated indicators
│   ├── processed/        # Processed data
│   └── raw_parquet/      # Raw data files
├── docs/                  # Documentation
├── logs/                  # Log files
├── results/               # Analysis results
└── scripts/               # Utility scripts
    ├── debug/             # Debug and analysis scripts
    ├── analysis/          # Analysis utilities
    ├── docker/            # Docker-related scripts
    ├── mcp/               # MCP server scripts
    ├── native-container/  # Native container scripts
    └── utilities/         # General utility scripts
```

## Python package initialization

All folders and subfolders in `src/` and `tests/` **must contain an `__init__.py` file**. This ensures proper package/module discovery and import behavior. The presence of these files is automatically checked by the test suite (`test_file_reorganization.py`).

## Test Coverage

The project maintains **100% test coverage** for all source files. This is automatically verified by the test coverage analysis script (`tests/zzz_analyze_test_coverage.py`).

### Test Structure

- **Unit tests** are located in `tests/` with a structure mirroring `src/`
- **Test files** follow the naming convention: `test_<module_name>.py`
- **Coverage analysis** runs automatically after test execution
- **Missing tests** are automatically detected and reported

### Test Categories

1. **Import tests** - Verify modules can be imported
2. **File existence tests** - Ensure source files exist
3. **Basic functionality tests** - Test core module functionality
4. **Module structure tests** - Verify module has expected attributes

### Automatic Coverage Checking

The test suite automatically:
- Analyzes all Python files in `src/` and project root
- Maps test files to source files
- Reports coverage percentage
- Identifies files without corresponding tests
- Ensures 100% coverage is maintained

## Key Files

- `pyproject.toml` - Project configuration and dependencies
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-container setup
- `README.md` - Project overview and quick start

## Recent File Reorganization

The project has been reorganized to improve structure and maintainability:

### Moved Files

- **`test_ma_line.py`** → `tests/calculation/indicators/trend/` - Test for MA line indicator
- **`debug_wave_indicator.py`** → `scripts/debug/` - Debug script for wave indicator analysis
- **`debug_signals_analysis.py`** → `scripts/debug/` - Debug script for signals analysis

### Test File Updates

- **`test_test_ma_line.py`** → `tests/calculation/indicators/trend/` - Tests for MA line functionality
- **`test_debug_wave_indicator.py`** → `tests/scripts/` - Tests for wave indicator debug script
- **`test_debug_signals_analysis.py`** → `tests/scripts/` - Tests for signals analysis debug script

All import paths and file references have been updated to reflect the new structure.