# NeoZork HLD Scripts Documentation

## Overview

The NeoZork HLD project provides several command-line scripts for analysis, data exploration, and project maintenance:

- **`nz`** - Main analysis script for running indicator calculations and generating plots
- **`eda`** - Data exploration and analysis script for quality checks and statistical analysis
- **`fix_imports.py`** - Utility script for fixing import statements in test files
- **`analyze_test_coverage.py`** - Utility script for analyzing test coverage across the project

Both main scripts are designed to work seamlessly in both Docker and native environments.

## Scripts

### nz - Main Analysis Script

The `nz` script is the primary interface for running indicator analysis and generating visualizations.

#### Usage

```bash
# Basic usage
./nz [options]

# With uv (recommended for native environment)
uv run ./nz [options]

# Direct execution
./nz [options]
```

#### Environment Detection

The script automatically detects whether it's running in a Docker container or native environment:

- **Docker Environment**: Uses `python run_analysis.py` directly
- **Native Environment**: Uses `uv run python run_analysis.py` (with fallback to direct Python)

#### Examples

```bash
# Show version
./nz --version

# Show help
./nz --help

# Run demo analysis
./nz demo --rule PHLD

# Analyze YFinance data
./nz yfinance MSFT --rule PHLD

# Analyze MQL5 data
./nz mql5 EURUSD --interval H4 --rule PHLD

# Run with specific parameters
./nz --input-file data.csv --output-dir ./results --plot-type detailed
```

### eda - Data Exploration Script

The `eda` script provides comprehensive data quality checks and statistical analysis capabilities.

#### Usage

```bash
# Basic usage
./eda [options]

# With uv (recommended for native environment)
uv run ./eda [options]

# Direct execution
./eda [options]
```

#### Environment Detection

Similar to `nz`, the script automatically detects the environment:

- **Docker Environment**: Uses `python src/eda/eda_batch_check.py` directly
- **Native Environment**: Uses `uv run python src/eda/eda_batch_check.py` (with fallback to direct Python)

#### Examples

```bash
# Show help
./eda --help

# Run data quality checks
./eda --data-quality-checks

# Check for specific issues
./eda --nan-check --duplicate-check

# Fix data quality issues
./eda --fix-files --fix-all

# Run statistical analysis
./eda --descriptive-stats

# Analyze specific file
./eda --file mydata.parquet --nan-check

# Clean up logs and reports
./eda --clean-stats-logs --clean-reports
```

### fix_imports.py - Import Fixing Utility

The `fix_imports.py` script is a utility tool located in the `scripts/` directory that helps maintain proper import statements in test files.

#### Purpose

This script automatically fixes relative imports in test files by converting them to absolute imports. It's particularly useful when test files have incorrect import paths that prevent them from running properly.

#### Usage

```bash
# Run from project root
python scripts/fix_imports.py

# Or with uv
uv run python scripts/fix_imports.py
```

#### What it does

The script:
- Scans all Python files in `tests/calculation/indicators/` directory
- Replaces relative imports like `from ...src.` with absolute imports like `from src.`
- Handles multiple levels of relative imports (`.`, `..`, `...`, `....`)
- Updates files in-place

#### Example transformations

```python
# Before (relative imports)
from ...src.calculation.indicators.rsi_ind_calc import RSIIndicator
from ....src.data.fetchers.csv_fetcher import CSVFetcher

# After (absolute imports)
from src.calculation.indicators.rsi_ind_calc import RSIIndicator
from src.data.fetchers.csv_fetcher import CSVFetcher
```

#### When to use

- After restructuring project directories
- When test imports are broken
- As part of CI/CD pipeline maintenance
- Before running test suites

### analyze_test_coverage.py - Test Coverage Analysis

The `analyze_test_coverage.py` script is a utility tool located in the `scripts/` directory that analyzes test coverage across the entire project.

#### Purpose

This script provides comprehensive analysis of which source files are covered by tests and which ones are missing test coverage. It helps developers identify gaps in testing and maintain high test coverage standards.

#### Usage

```bash
# Run from project root
python tests/zzz_analyze_test_coverage.py

# Or with uv
uv run python tests/zzz_analyze_test_coverage.py
```

#### What it does

The script:
- Scans all Python files in `src/` directory and project root
- Identifies all test files in `tests/` directory
- Maps test files to their corresponding source files
- Calculates overall test coverage percentage
- Lists files without test coverage
- Groups missing tests by modules for better organization

#### Output example

```
📊 TEST COVERAGE ANALYSIS
==================================================
Total files in src/ and root: 105
Total tests: 124
Covered by tests: 80
Not covered by tests: 25
Coverage: 76.2%

📝 FILES WITHOUT TESTS:
------------------------------
❌ src/calculation/indicators/base_indicator.py
❌ src/plotting/fastest_auto_plot.py
...

📁 GROUPING BY MODULES:
------------------------------
🔸 calculation/ (1 files):
   - __init__.py
🔸 plotting/ (3 files):
   - __init__.py
   - fastest_auto_plot.py
   - fastest_plot.py
```

#### When to use

- During development to ensure adequate test coverage
- Before code reviews to identify testing gaps
- In CI/CD pipelines to enforce coverage standards
- When refactoring to ensure all code paths are tested
- For project maintenance and quality assurance

#### Exit codes

- **Exit code 0**: All files have test coverage
- **Exit code 1**: Some files are missing test coverage

## Environment Setup

### Native Environment

1. **Install uv** (recommended):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Add scripts to PATH** (optional):
   ```bash
   export PATH="/path/to/neozork-hld-prediction:$PATH"
   ```

### Docker Environment

1. **Build and run container**:
   ```bash
   docker-compose up -d
   ```

2. **Access container**:
   ```bash
   docker exec -it <container_name> bash
   ```

3. **Use scripts directly**:
   ```bash
   nz --version
   eda --help
   ```

## Script Behavior

### Environment Detection Logic

Both scripts use the following logic to determine the execution environment:

```bash
# Check if running inside a Docker container
IN_DOCKER=false
if [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup 2>/dev/null; then
    IN_DOCKER=true
fi
```

### Execution Path

1. **Docker Environment**:
   - Direct Python execution
   - No dependency management needed (pre-installed)

2. **Native Environment**:
   - Try `uv run` first (recommended)
   - Fallback to direct Python if `uv` unavailable

### Error Handling

- Graceful fallback from `uv run` to direct Python
- Clear environment detection messages
- Proper error reporting for missing dependencies

## Integration with Docker

### Docker Entrypoint

The `docker-entrypoint.sh` creates wrapper scripts in `/tmp/bin/`:

```bash
# nz wrapper
python /app/run_analysis.py "$@"

# eda wrapper  
python /app/src/eda/eda_batch_check.py "$@"
```

### Container Usage

Inside Docker containers, scripts work seamlessly:

```bash
# Direct execution
nz --version
eda --help

# Full analysis workflow
nz demo --rule PHLD
eda --data-quality-checks
```

## Best Practices

### Native Development

1. **Use uv for dependency management**:
   ```bash
   uv run ./nz --version
   ```

2. **Keep scripts in PATH**:
   ```bash
   export PATH="/path/to/project:$PATH"
   nz --help
   ```

3. **Use virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate
   ./nz --version
   ```

### Docker Development

1. **Use container scripts directly**:
   ```bash
   docker exec -it <container> nz --version
   ```

### MCP Server Stdio/Protocol Test

The MCP server now includes a fully automated stdio protocol test (`tests/test_stdio.py`). This test works with both pytest and standalone execution, and is suitable for CI/CD pipelines and local validation.

**Usage:**
```bash
# Standalone
python tests/test_stdio.py

# With pytest (recommended for CI)
pytest tests/test_stdio.py -v
```

This test validates all key LSP protocol methods (initialize, completion, shutdown, exit) and ensures correct JSON serialization and protocol compliance in all environments (including subprocess/PIPE).