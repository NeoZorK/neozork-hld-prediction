# Sequential Test Runner for Docker

## Overview

The Sequential Test Runner is a specialized test execution system designed for Docker environments to run tests folder by folder sequentially, avoiding worker crashes and resource issues that can occur with parallel test execution.

## Features

- **Sequential Execution**: Runs tests one folder at a time to prevent resource conflicts
- **Configurable Order**: YAML-based configuration for test folder execution order
- **Docker Optimized**: Specifically designed for Docker container environments
- **Resource Management**: Built-in cleanup between test folder executions
- **Timeout Management**: Per-folder timeout configuration
- **Dependency Support**: Configurable dependencies between test folders
- **Comprehensive Logging**: Detailed logging of test execution progress

## Usage

### Basic Usage

```bash
# Run all tests sequentially by folder
python scripts/run_sequential_tests_docker.py

# Test the runner functionality
python scripts/test_sequential_runner.py
```

### Docker Integration

The sequential test runner is integrated into the Docker entrypoint and will be offered as an option when starting the container:

```bash
# When starting Docker container, you'll be prompted:
Would you like to run tests? [y/N]:
  - 'y' or 'Y': Run all tests sequentially by folder (recommended for Docker)
  - 'n' or 'N': Skip tests
```

## Configuration

### Configuration File

The test execution order and settings are configured via `tests/test_execution_order.yaml`:

```yaml
# Test Execution Order Configuration
test_folders:
  # Phase 1: Basic utilities and common functions
  - name: "common"
    description: "Basic utilities and common functions"
    timeout: 30
    required: true
    
  - name: "unit"
    description: "Unit tests for individual components"
    timeout: 60
    required: true
    
  # Phase 2: Data processing and calculations
  - name: "data"
    description: "Data processing and acquisition tests"
    timeout: 90
    required: true
    
  - name: "calculation"
    description: "Mathematical calculations and indicators"
    timeout: 120
    required: true

# Global settings
global_settings:
  max_total_time: 3600  # 1 hour
  stop_on_failure: true
  skip_empty_folders: true
  cleanup_between_folders: true
  
  environment:
    PYTHONPATH: "/app"
    PYTHONUNBUFFERED: "1"
    DOCKER_CONTAINER: "true"
    MPLBACKEND: "Agg"
    DISPLAY: ""
    UV_SYSTEM_PYTHON: "1"

# Folder-specific overrides
folder_overrides:
  calculation:
    timeout: 180  # Longer timeout for complex calculations
    maxfail: 3    # Allow more failures in calculation tests

# Dependencies between folders
dependencies:
  calculation:
    - "common"
    - "utils"
    - "data"
```

### Configuration Options

#### Test Folders

Each test folder can be configured with:

- `name`: Folder name (required)
- `description`: Human-readable description
- `timeout`: Maximum execution time in seconds
- `required`: Whether the folder is required (true/false)

#### Global Settings

- `max_total_time`: Maximum total execution time for all tests
- `stop_on_failure`: Stop execution on first folder failure
- `skip_empty_folders`: Skip folders with no test files
- `cleanup_between_folders`: Clean up resources between folders
- `environment`: Environment variables to set

#### Folder Overrides

Override settings for specific folders:

- `timeout`: Custom timeout for the folder
- `maxfail`: Maximum number of failures allowed

#### Dependencies

Define which folders must complete successfully before others can run.

## Test Execution Order

The default execution order is designed to run tests from basic to complex:

1. **common** - Basic utilities and common functions
2. **unit** - Unit tests for individual components
3. **utils** - Utility function tests
4. **data** - Data processing and acquisition tests
5. **calculation** - Mathematical calculations and indicators
6. **eda** - Exploratory data analysis tests
7. **cli** - Command line interface tests
8. **interactive** - Interactive mode tests
9. **plotting** - Plotting and visualization tests
10. **export** - Data export functionality tests
11. **integration** - Integration tests
12. **ml** - Machine learning tests
13. **mcp** - MCP server tests
14. **docker** - Docker-specific tests
15. **native-container** - Native container tests
16. **pocket_hedge_fund** - Pocket hedge fund application tests
17. **saas** - SaaS application tests
18. **scripts** - Script execution tests
19. **workflow** - Workflow tests
20. **e2e** - End-to-end tests

## Output and Logging

The sequential test runner provides detailed logging:

```
2024-01-15 10:30:00 - INFO - Starting sequential test execution in Docker environment
2024-01-15 10:30:00 - INFO - Test folders to run: common, unit, utils, data, calculation, cli, plotting, export, eda, interactive, integration, mcp, ml, docker, native-container, pocket_hedge_fund, saas, scripts, workflow, e2e

============================================================
Running folder 1/20: common
Description: Basic utilities and common functions
Timeout: 30s
============================================================
2024-01-15 10:30:01 - INFO - Running tests in folder: common (2 files)
2024-01-15 10:30:01 - INFO - Command: uv run pytest /app/tests/common -c pytest-docker.ini --tb=short --disable-warnings --no-header --no-summary --maxfail=1 --timeout=30 --timeout-method=thread -v
2024-01-15 10:30:05 - INFO - ✅ Folder common completed successfully in 4.23s
2024-01-15 10:30:05 - INFO -    Passed: 5, Failed: 0, Skipped: 0
```

## Benefits

### For Docker Environments

1. **Resource Stability**: Avoids worker crashes common in parallel execution
2. **Memory Management**: Sequential execution prevents memory exhaustion
3. **Predictable Behavior**: Consistent test execution order
4. **Better Debugging**: Easier to identify which folder caused issues

### For Development

1. **Dependency Management**: Ensures tests run in logical order
2. **Configurable Timeouts**: Per-folder timeout settings
3. **Flexible Configuration**: Easy to modify execution order
4. **Comprehensive Reporting**: Detailed progress and results

## Troubleshooting

### Common Issues

1. **Configuration File Not Found**
   - The runner will use default configuration if YAML file is missing
   - Check that `tests/test_execution_order.yaml` exists

2. **Folder Timeout**
   - Increase timeout in configuration for slow folders
   - Check for infinite loops or resource leaks in tests

3. **Docker Environment Detection**
   - Ensure running in Docker container
   - Check for `/.dockerenv` file or `DOCKER_CONTAINER` environment variable

4. **Permission Issues**
   - Ensure proper file permissions in Docker container
   - Check that test files are readable

### Debug Mode

Run the test script to verify functionality:

```bash
python scripts/test_sequential_runner.py
```

This will test:
- Configuration loading
- Environment setup
- Docker detection
- Folder discovery
- Configuration validation

## Integration with Existing Workflows

The sequential test runner integrates seamlessly with existing test workflows:

- **Docker Entrypoint**: Automatically offered when starting container
- **CI/CD Pipelines**: Can be used in automated testing
- **Development**: Available as command in interactive shell
- **Manual Testing**: Can be run independently for specific test scenarios

## Future Enhancements

Potential improvements for future versions:

1. **Parallel Folder Execution**: Run independent folders in parallel
2. **Test Result Caching**: Cache results to skip unchanged tests
3. **Dynamic Timeout Adjustment**: Adjust timeouts based on historical data
4. **Test Prioritization**: Prioritize critical tests
5. **Resource Monitoring**: Monitor resource usage during execution
