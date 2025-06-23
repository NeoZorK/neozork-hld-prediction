# Script Examples

Examples for using utility scripts and debugging tools.

## Overview

The project includes various utility scripts for:

- **Import Management** - Fix import statements automatically
- **Debug Scripts** - Troubleshoot and debug issues
- **Data Management** - Create and manage test data
- **System Analysis** - Analyze requirements and dependencies
- **Development Tools** - Development workflow automation

## Import Management

### Fix Imports Script
```bash
# Fix imports automatically
python scripts/fix_imports.py

# Fix with verbose output
python scripts/fix_imports.py --verbose

# Fix specific file
python scripts/fix_imports.py --file src/calculation/indicators/rsi_ind.py

# Fix specific directory
python scripts/fix_imports.py --directory src/calculation/indicators/

# Fix with backup
python scripts/fix_imports.py --backup

# Fix with dry run (no changes)
python scripts/fix_imports.py --dry-run
```

### Import Analysis
```bash
# Analyze import issues
python scripts/fix_imports.py --analyze

# Show import statistics
python scripts/fix_imports.py --stats

# Check import dependencies
python scripts/fix_imports.py --check-deps
```

## Debug Scripts

### Debug Binance Connection
```bash
# Debug Binance connection
python scripts/debug_scripts/debug_binance_connection.py

# Debug with specific symbol
python scripts/debug_scripts/debug_binance_connection.py --symbol BTCUSDT

# Debug with specific interval
python scripts/debug_scripts/debug_binance_connection.py --interval D1

# Debug with verbose output
python scripts/debug_scripts/debug_binance_connection.py --verbose
```

### Debug Parquet Files
```bash
# Check Parquet files
python scripts/debug_scripts/debug_check_parquet.py

# Check specific file
python scripts/debug_scripts/debug_check_parquet.py --file data/file.parquet

# Check with data validation
python scripts/debug_scripts/debug_check_parquet.py --validate

# Check with statistics
python scripts/debug_scripts/debug_check_parquet.py --stats
```

### Debug Indicators
```bash
# Debug indicators
python scripts/debug_scripts/debug_indicators.py

# Debug specific indicator
python scripts/debug_scripts/debug_indicators.py --indicator RSI

# Debug with test data
python scripts/debug_scripts/debug_indicators.py --test-data

# Debug with verbose output
python scripts/debug_scripts/debug_indicators.py --verbose
```

### Debug CLI
```bash
# Debug CLI
python scripts/debug_scripts/debug_cli.py

# Debug specific command
python scripts/debug_scripts/debug_cli.py --command "demo --rule RSI"

# Debug with test mode
python scripts/debug_scripts/debug_cli.py --test-mode

# Debug with verbose output
python scripts/debug_scripts/debug_cli.py --verbose
```

### Debug MCP Servers
```bash
# Debug MCP servers
python scripts/debug_scripts/debug_mcp_servers.py

# Debug server status
python scripts/debug_scripts/debug_mcp_status.py

# Debug MCP connections
python scripts/debug_scripts/debug_mcp_connections.py

# Debug with restart
python scripts/debug_scripts/debug_mcp_servers.py --restart
```

### Debug Data Processing
```bash
# Debug data processing
python scripts/debug_scripts/debug_data_processing.py

# Debug with specific file
python scripts/debug_scripts/debug_data_processing.py --file data.csv

# Debug with validation
python scripts/debug_scripts/debug_data_processing.py --validate

# Debug with performance metrics
python scripts/debug_scripts/debug_data_processing.py --performance
```

### Debug Plotting
```bash
# Debug plotting
python scripts/debug_scripts/debug_plotting.py

# Debug specific backend
python scripts/debug_scripts/debug_plotting.py --backend plotly

# Debug with test data
python scripts/debug_scripts/debug_plotting.py --test-data

# Debug with performance metrics
python scripts/debug_scripts/debug_plotting.py --performance
```

### Debug System Resources
```bash
# Debug system resources
python scripts/debug_scripts/debug_system_resources.py

# Debug memory usage
python scripts/debug_scripts/debug_system_resources.py --memory

# Debug CPU usage
python scripts/debug_scripts/debug_system_resources.py --cpu

# Debug disk usage
python scripts/debug_scripts/debug_system_resources.py --disk

# Debug network usage
python scripts/debug_scripts/debug_system_resources.py --network
```

## Data Management

### Create Test Parquet File
```bash
# Create test Parquet file
python scripts/create_test_parquet.py

# Create with specific size
python scripts/create_test_parquet.py --size 1000

# Create with specific columns
python scripts/create_test_parquet.py --columns open,high,low,close,volume

# Create with specific date range
python scripts/create_test_parquet.py --start-date 2024-01-01 --end-date 2024-12-31

# Create with custom filename
python scripts/create_test_parquet.py --output test_data.parquet
```

### Recreate CSV from Parquet
```bash
# Recreate CSV from Parquet
python scripts/recreate_csv.py

# Recreate specific file
python scripts/recreate_csv.py --file data.parquet

# Recreate with custom output
python scripts/recreate_csv.py --output recreated.csv

# Recreate with specific columns
python scripts/recreate_csv.py --columns open,high,low,close,volume

# Recreate with date filtering
python scripts/recreate_csv.py --start-date 2024-01-01 --end-date 2024-06-30
```

### Clear Cache
```bash
# Clear cache
python scripts/clear_cache.py

# Clear specific cache type
python scripts/clear_cache.py --type data

# Clear with confirmation
python scripts/clear_cache.py --confirm

# Clear with backup
python scripts/clear_cache.py --backup
```

## System Analysis

### Analyze Requirements
```bash
# Analyze requirements
python scripts/analyze_requirements.py

# Analyze with output file
python scripts/analyze_requirements.py --output requirements_analysis.txt

# Analyze with verbose output
python scripts/analyze_requirements.py --verbose

# Analyze with dependency tree
python scripts/analyze_requirements.py --tree

# Analyze with security check
python scripts/analyze_requirements.py --security
```

### Auto PyProject from Requirements
```bash
# Auto generate pyproject.toml from requirements
python scripts/auto_pyproject_from_requirements.py

# Generate with specific requirements file
python scripts/auto_pyproject_from_requirements.py --requirements requirements.txt

# Generate with custom output
python scripts/auto_pyproject_from_requirements.py --output pyproject_custom.toml

# Generate with project metadata
python scripts/auto_pyproject_from_requirements.py --name "My Project" --version "1.0.0"
```

## Development Tools

### Initialize Directories
```bash
# Initialize project directories
bash scripts/init_dirs.sh

# Initialize with specific directories
bash scripts/init_dirs.sh --dirs data,logs,results

# Initialize with permissions
bash scripts/init_dirs.sh --permissions 755

# Initialize with verbose output
bash scripts/init_dirs.sh --verbose
```

### Run Analysis Script
```bash
# Run analysis script
bash eda

# Run with UV
uv run ./eda

# Run with verbose output
bash eda --verbose

# Run with export results
bash eda --export-results

# Run with specific data file
bash eda --file data.csv
```

## Log Analysis

### Analyze Logs
```bash
# Analyze logs
python scripts/log_analysis/analyze_logs.py

# Analyze specific log file
python scripts/log_analysis/analyze_logs.py --file logs/app.log

# Analyze with error filtering
python scripts/log_analysis/analyze_logs.py --errors-only

# Analyze with time range
python scripts/log_analysis/analyze_logs.py --start-time "2024-01-01" --end-time "2024-12-31"

# Analyze with statistics
python scripts/log_analysis/analyze_logs.py --stats
```

### Log Statistics
```bash
# Generate log statistics
python scripts/log_analysis/log_stats.py

# Generate with specific log file
python scripts/log_analysis/log_stats.py --file logs/app.log

# Generate with time period
python scripts/log_analysis/log_stats.py --period daily

# Generate with output file
python scripts/log_analysis/log_stats.py --output stats.json
```

## Performance Scripts

### Performance Analysis
```bash
# Analyze performance
python scripts/performance/analyze_performance.py

# Analyze with specific component
python scripts/performance/analyze_performance.py --component indicators

# Analyze with benchmarking
python scripts/performance/analyze_performance.py --benchmark

# Analyze with memory profiling
python scripts/performance/analyze_performance.py --memory-profile
```

### Memory Profiling
```bash
# Profile memory usage
python scripts/performance/memory_profile.py

# Profile specific function
python scripts/performance/memory_profile.py --function calculate_rsi

# Profile with output file
python scripts/performance/memory_profile.py --output memory_profile.txt

# Profile with visualization
python scripts/performance/memory_profile.py --visualize
```

## Testing Scripts

### Test Runner
```bash
# Run tests with script
python scripts/test_runner.py

# Run specific test category
python scripts/test_runner.py --category calculation

# Run with coverage
python scripts/test_runner.py --coverage

# Run with parallel execution
python scripts/test_runner.py --parallel

# Run with output file
python scripts/test_runner.py --output test_results.json
```

### Test Coverage Analysis
```bash
# Analyze test coverage
python tests/zzz_analyze_test_coverage.py

# Analyze with verbose output
python tests/zzz_analyze_test_coverage.py --verbose

# Analyze with output file
python tests/zzz_analyze_test_coverage.py --output coverage_report.txt

# Analyze with HTML report
python tests/zzz_analyze_test_coverage.py --html
```

## Workflow Scripts

### Development Workflow
```bash
# Run development workflow
bash scripts/dev_workflow.sh

# Workflow with specific steps
bash scripts/dev_workflow.sh --steps test,coverage,deploy

# Workflow with verbose output
bash scripts/dev_workflow.sh --verbose

# Workflow with dry run
bash scripts/dev_workflow.sh --dry-run
```

### CI/CD Scripts
```bash
# Run CI pipeline
bash scripts/ci_pipeline.sh

# Run with specific environment
bash scripts/ci_pipeline.sh --env production

# Run with parallel execution
bash scripts/ci_pipeline.sh --parallel

# Run with notification
bash scripts/ci_pipeline.sh --notify
```

## Utility Scripts

### File Operations
```bash
# Clean temporary files
python scripts/utils/clean_temp.py

# Clean with specific patterns
python scripts/utils/clean_temp.py --pattern "*.tmp"

# Clean with confirmation
python scripts/utils/clean_temp.py --confirm

# Clean with backup
python scripts/utils/clean_temp.py --backup
```

### Configuration Management
```bash
# Validate configuration
python scripts/utils/validate_config.py

# Validate specific config file
python scripts/utils/validate_config.py --file config.json

# Validate with schema
python scripts/utils/validate_config.py --schema schema.json

# Validate with fix
python scripts/utils/validate_config.py --fix
```

## Advanced Scripts

### Custom Scripts
```bash
# Run custom analysis
python scripts/custom/run_custom_analysis.py

# Run with parameters
python scripts/custom/run_custom_analysis.py --param1 value1 --param2 value2

# Run with configuration
python scripts/custom/run_custom_analysis.py --config custom_config.json

# Run with output
python scripts/custom/run_custom_analysis.py --output results.json
```

### Batch Processing
```bash
# Process batch of files
python scripts/batch/process_batch.py

# Process with specific directory
python scripts/batch/process_batch.py --directory data/

# Process with file pattern
python scripts/batch/process_batch.py --pattern "*.csv"

# Process with parallel execution
python scripts/batch/process_batch.py --parallel
```

## Troubleshooting

### Common Issues
```bash
# Issue: Import errors
python scripts/fix_imports.py --verbose

# Issue: Data problems
python scripts/debug_scripts/debug_check_parquet.py

# Issue: Connection problems
python scripts/debug_scripts/debug_binance_connection.py

# Issue: Performance problems
python scripts/debug_scripts/debug_system_resources.py
```

### Debug Mode
```bash
# Enable debug mode
export DEBUG=1
python scripts/fix_imports.py

# Run with debug logging
python scripts/debug_scripts/debug_indicators.py --debug

# Run with verbose output
python scripts/create_test_parquet.py --verbose
```

### Script Validation
```bash
# Validate script syntax
python -m py_compile scripts/fix_imports.py

# Check script dependencies
python scripts/analyze_requirements.py --script scripts/fix_imports.py

# Test script functionality
python scripts/fix_imports.py --dry-run
```

---

📚 **Additional Resources:**
- **[Usage Examples](usage-examples.md)** - Comprehensive usage examples
- **[Quick Examples](quick-examples.md)** - Fast start examples
- **[Indicator Examples](indicator-examples.md)** - Technical indicator examples
- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Testing Examples](testing-examples.md)** - Testing examples
- **[Docker Examples](docker-examples.md)** - Docker examples
- **[EDA Examples](eda-examples.md)** - EDA examples 