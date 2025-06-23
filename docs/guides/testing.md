# Testing Guide

Testing framework and validation tools.

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
python tests/run_tests.py
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
python tests/test_stdio.py

# With pytest (for CI and automation)
pytest tests/test_stdio.py -v
```

> This test ensures the server works perfectly in all environments, including GitHub Actions and Docker.