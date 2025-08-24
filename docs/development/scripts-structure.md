# Scripts Structure

This document describes the organization and structure of utility scripts in the neozork-hld-prediction project.

## Scripts Directory Organization

The scripts directory contains various utility scripts organized by functionality:

```
scripts/
├── __init__.py            # Package initialization
├── debug/                 # Debug and analysis scripts
│   ├── __init__.py        # Debug package initialization
│   ├── debug_wave_indicator.py      # Wave indicator debugging
│   ├── debug_signals_analysis.py    # Signals analysis debugging
│   ├── debug_binance.py             # Binance API debugging
│   ├── debug_binance_connection.py  # Binance connection testing
│   ├── debug_check_parquet.py       # Parquet file validation
│   ├── debug_csv_reader.py          # CSV reading debugging
│   ├── debug_polygon.py             # Polygon API debugging
│   ├── debug_polygon_connection.py  # Polygon connection testing
│   ├── debug_polygon_resolve.py     # Polygon data resolution
│   ├── debug_yfinance.py            # Yahoo Finance debugging
│   ├── debug_yfinance_v0.4.3.py    # Yahoo Finance v0.4.3 debugging
│   ├── debug_yfinance_v0.4.3_original.py # Original Yahoo Finance debugging
│   ├── examine_binance_parquet.py   # Binance parquet examination
│   ├── examine_parquet.py           # General parquet examination
│   ├── test_wave_colors.py          # Wave color testing
│   ├── test_wave_fix.py             # Wave fix testing
│   └── check_putcallratio_periods.py # Put-call ratio period checking
├── analysis/              # Analysis utilities
│   ├── __init__.py        # Analysis package initialization
│   ├── analyze_requirements.py      # Requirements analysis
│   ├── analyze_sar_command_results.py # SAR command results analysis
│   └── dead-code/         # Dead code analysis tools
├── docker/                # Docker-related scripts
│   ├── __init__.py        # Docker package initialization
│   ├── docker-test-workflows.sh     # Docker test workflows
│   └── test_docker_history.sh       # Docker history testing
├── mcp/                   # MCP server scripts
│   ├── __init__.py        # MCP package initialization
│   ├── check_mcp_status.py          # MCP status checking
│   ├── debug_mcp_detection.py       # MCP detection debugging
│   └── start_mcp_server.py          # MCP server startup
├── native-container/      # Native container scripts
│   ├── __init__.py        # Native container package initialization
│   ├── analyze_all_logs.sh         # Log analysis
│   ├── cleanup.sh                  # Container cleanup
│   ├── exec.sh                     # Container execution
│   └── test_container_setup.sh     # Container setup testing
├── utilities/             # General utility scripts
│   ├── __init__.py        # Utilities package initialization
│   ├── check_uv_mode.py            # UV mode checking
│   ├── create_test_parquet.py      # Test parquet creation
│   └── check_uv_mode.sh            # UV mode checking shell script
├── demos/                 # Demonstration scripts
│   ├── __init__.py        # Demos package initialization
│   └── demo_universal_metrics.py   # Universal metrics demonstration
├── run_tests.sh           # Test execution script
├── run_tests_safe.sh      # Safe test execution
├── run_all_tests.sh       # All tests execution
├── run_all_tests_safe.sh  # Safe all tests execution
├── run_tests_native_container.sh # Native container test execution
├── run_tests_with_timeout.sh      # Timeout-based test execution
├── debug_docker_processes.py      # Docker process debugging
├── debug_rsi_signals.py           # RSI signals debugging
├── demo_terminal_chunked.py       # Terminal chunked demonstration
└── check_mcp_status.py            # MCP status checking (root level)
```

## Script Categories

### 1. Debug Scripts (`scripts/debug/`)
- **Indicator debugging** - Scripts for debugging technical indicators
- **API debugging** - Scripts for debugging external API connections
- **Data validation** - Scripts for validating data files and formats
- **Connection testing** - Scripts for testing various service connections

### 2. Analysis Scripts (`scripts/analysis/`)
- **Requirements analysis** - Scripts for analyzing project requirements
- **Code analysis** - Scripts for analyzing code quality and structure
- **Dead code detection** - Tools for identifying unused code

### 3. Docker Scripts (`scripts/docker/`)
- **Test workflows** - Scripts for Docker-based testing workflows
- **History testing** - Scripts for testing Docker history functionality

### 4. MCP Scripts (`scripts/mcp/`)
- **Server management** - Scripts for managing MCP servers
- **Status checking** - Scripts for checking MCP server status
- **Detection debugging** - Scripts for debugging MCP detection

### 5. Native Container Scripts (`scripts/native-container/`)
- **Container management** - Scripts for managing native containers
- **Log analysis** - Scripts for analyzing container logs
- **Setup testing** - Scripts for testing container setup

### 6. Utility Scripts (`scripts/utilities/`)
- **Environment checking** - Scripts for checking environment setup
- **Data creation** - Scripts for creating test data
- **System validation** - Scripts for validating system configuration

### 7. Demo Scripts (`scripts/demos/`)
- **Feature demonstrations** - Scripts for demonstrating project features
- **Usage examples** - Examples of how to use various project components

## Script Naming Conventions

- **`debug_<feature>.py`** - Debug scripts for specific features
- **`test_<feature>.py`** - Test scripts for specific functionality
- **`examine_<data_type>.py`** - Data examination scripts
- **`check_<component>.py`** - Component checking scripts
- **`run_<action>.sh`** - Shell scripts for running specific actions
- **`demo_<feature>.py`** - Demonstration scripts

## Script Dependencies

Most scripts have the following common dependencies:
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **matplotlib** - Plotting and visualization
- **seaborn** - Statistical data visualization
- **requests** - HTTP library for API calls
- **pathlib** - Path manipulation utilities

## Running Scripts

### Python Scripts
```bash
# From project root
python scripts/debug/debug_wave_indicator.py

# Using uv
uv run python scripts/debug/debug_wave_indicator.py
```

### Shell Scripts
```bash
# Make executable first
chmod +x scripts/run_tests.sh

# Run from project root
./scripts/run_tests.sh
```

## Recent Changes

### File Reorganization (Latest Update)

The following files have been moved to improve script organization:

1. **`debug_wave_indicator.py`** → `scripts/debug/`
   - Debug script for wave indicator analysis
   - Now properly organized with other debug scripts

2. **`debug_signals_analysis.py`** → `scripts/debug/`
   - Debug script for signals analysis
   - Now properly organized with other debug scripts

### Benefits of Reorganization

- **Better organization** - Related scripts are grouped together
- **Easier maintenance** - Scripts are easier to find and update
- **Improved discoverability** - Developers can easily locate relevant scripts
- **Consistent structure** - All script categories follow the same pattern

## Best Practices

1. **Keep scripts focused** - Each script should have a single, clear purpose
2. **Use descriptive names** - Script names should clearly indicate functionality
3. **Include documentation** - Add docstrings and comments to explain script purpose
4. **Handle errors gracefully** - Include proper error handling and user feedback
5. **Follow naming conventions** - Use consistent naming patterns across all scripts
6. **Update this documentation** - Keep this document updated when adding new scripts

## Adding New Scripts

When adding new scripts:

1. **Choose appropriate category** - Place scripts in the most relevant subdirectory
2. **Follow naming conventions** - Use consistent naming patterns
3. **Update package files** - Ensure `__init__.py` files are updated if needed
4. **Update documentation** - Add new scripts to this document
5. **Include tests** - Create corresponding test files in `tests/scripts/`
