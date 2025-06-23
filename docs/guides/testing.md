# Testing Guide

Testing framework and validation tools.

## Test Directory Structure

All test files are organized in logical subfolders under `tests/`. General and summary tests (not belonging to a specific module) are now located in `tests/summary/`.

```
- tests/
    - conftest.py         # Global pytest hooks and fixtures (applies to all tests)
    - summary/           # General and summary tests (moved from root)
        - test_stdio.py
        - test_file_reorganization.py
        - zzz_analyze_test_coverage.py
        - run_tests.py
        - test_fix_imports.py
        - test_run_analysis.py
    - cli/
    - calculation/
    - common/
    - data/
    - docker/
    - eda/
    - export/
    - mcp/
    - plotting/
    - scripts/
    - src/
    - utils/
    - workflow/
    - ...
```

> **Note:** The `conftest.py` file is intentionally placed in the root of the `tests/` directory (not in `summary/`). This is because pytest only applies hooks and fixtures from `conftest.py` to the current directory and all its subdirectories. Placing it in `tests/` ensures that all tests in all subfolders (including `summary/`, `cli/`, `data/`, etc.) have access to global hooks and fixtures. If you put `conftest.py` in `summary/`, its contents would only apply to tests in `summary/` and its subfolders.

> All new and existing general-purpose test scripts should be placed in `tests/summary/`.

## Quick Test Commands

### Run All Tests
```bash
# Using pytest (recommended)
pytest tests/ -v

# Using unittest
python -m unittest discover tests

# Run specific test categories
pytest tests/cli/ -v
pytest tests/data/ -v
```

### Test Runners

**Main test script:**
```bash
python tests/summary/run_tests.py
```

**Local workflow testing:**
```bash
./test-workflow.sh
```

## Debug and Validate

### Data Validation
```bash
# Validate data sources
python scripts/debug_scripts/debug_yfinance.py
python scripts/debug_scripts/debug_polygon_connection.py

# Check file integrity
python scripts/debug_scripts/examine_parquet.py data/file.parquet
```

### Quick Validation
```bash
# Test basic functionality
python -c "import src; print('Import successful')"

# Run demo analysis
python run_analysis.py demo
```

## CI/CD Testing

The project uses GitHub Actions for automated testing. See [CI/CD Guide](ci-cd.md) for details.

**Test locally:**
```bash
./test-workflow.sh
```

For more debugging tools: [Debug Scripts](debug-scripts.md)

## MCP Server Stdio/Protocol Testing

The MCP server is fully compatible with both subprocess/PIPE and pytest/CI environments. The stdio protocol test checks all key LSP methods (initialize, completion, shutdown, exit) and validates correct JSON serialization and protocol compliance.

**Recommended usage:**
```bash
# Standalone (for local/manual check)
python tests/summary/test_stdio.py

# With pytest (for CI and automation)
pytest tests/summary/test_stdio.py -v
```

> This test ensures the server works perfectly in all environments, including GitHub Actions and Docker.