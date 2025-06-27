# Native Apple Silicon Container Setup

This guide covers the setup and usage of the native Apple Silicon container for the NeoZork HLD Prediction project, providing **30-50% performance improvement** over Docker.

## Overview

The native Apple Silicon container is specifically optimized for macOS 26+ (Tahoe) and provides significant performance benefits:

- **30-50% performance improvement** over Docker
- **Lower resource usage** and faster startup times
- **Native Apple Silicon optimization**
- **Interactive management interface**
- **Seamless UV integration**

## Prerequisites

### System Requirements

- **macOS 26 Tahoe (Developer Beta)** or higher
- **Apple Silicon Mac** (M1, M2, M3, or newer)
- **Python 3.11+** installed
- **At least 4GB of available RAM**
- **10GB of available disk space**

### Required Software

1. **Native Container Application**
   - Download from: https://developer.apple.com/download/all/
   - Requires valid Apple Developer account
   - Install the native container application

2. **Python 3.11+**
   ```bash
   # Check Python version
   python3 --version
   
   # Install if needed (using Homebrew)
   brew install python@3.11
   ```

## Quick Start

### Interactive Setup (Recommended)

The easiest way to get started is using the interactive script:

```bash
# Run the interactive container manager
./scripts/native-container/native-container.sh
```

The interactive script provides a user-friendly menu system:

1. **Setup container** - Initial setup and configuration
2. **Start container** - Start the running container
3. **Stop container** - Stop the running container
4. **Remove container** - Remove the container completely
5. **Show container status** - Display current container status
6. **Show container logs** - View container logs
7. **Execute command in container** - Run specific commands
8. **Start interactive shell** - Open bash shell in container
9. **Run analysis** - Execute analysis commands
10. **Run tests** - Execute test suites
11. **Show available commands** - List all available commands
12. **Cleanup resources** - Clean up files and caches
13. **System check** - Verify system requirements
14. **Exit** - Exit the script

### Manual Setup

If you prefer to use individual scripts:

```bash
# 1. Initial setup
./scripts/native-container/setup.sh

# 2. Start container
./scripts/native-container/run.sh

# 3. Execute commands
./scripts/native-container/exec.sh --shell
```

## Interactive Script Features

### Analysis Commands

The interactive script provides easy access to common analysis commands:

- **Demo analysis**: `nz demo --rule PHLD`
- **Apple stock analysis**: `nz yfinance AAPL --rule PHLD`
- **Bitcoin analysis**: `nz mql5 BTCUSD --interval H4 --rule PHLD`
- **EDA analysis**: `eda`
- **Custom commands**: Enter your own commands

### Test Execution

Run tests with different options:

- **All tests**: `pytest`
- **Multithreaded tests**: `pytest tests/ -n auto`
- **Calculation tests**: `pytest tests/calculation/`
- **CLI tests**: `pytest tests/cli/`
- **Data tests**: `pytest tests/data/`
- **Custom test commands**: Enter your own test commands

### Container Management

- **Setup**: Automatic system checks and container creation
- **Start/Stop**: Simple container lifecycle management
- **Status**: Real-time container status monitoring
- **Logs**: View and follow container logs
- **Cleanup**: Remove containers and clean up resources

## Configuration

### Container Configuration

The container uses a YAML configuration file (`container.yaml`):

```yaml
apiVersion: v1
kind: Container
metadata:
  name: neozork-hld-prediction
  labels:
    platform: apple-silicon
spec:
  image: python:3.11-slim
  architecture: arm64
  resources:
    memory: "4Gi"
    cpu: "2"
    storage: "10Gi"
  volumes:
    - name: data-volume
      mountPath: /app/data
      hostPath: ./data
    - name: logs-volume
      mountPath: /app/logs
      hostPath: ./logs
    - name: results-volume
      mountPath: /app/results
      hostPath: ./results
  environment:
    - PYTHONPATH=/app
    - USE_UV=true
    - UV_ONLY=true
    - NATIVE_CONTAINER=true
```

### Environment Variables

Key environment variables for the native container:

```bash
# Package manager configuration
USE_UV=true
UV_ONLY=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv

# Container identification
NATIVE_CONTAINER=true
DOCKER_CONTAINER=false

# Python configuration
PYTHONPATH=/app
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# MCP Server configuration
MCP_SERVER_TYPE=pycharm_copilot

# Logging
LOG_LEVEL=INFO
```

## Usage Examples

### Basic Workflow

```bash
# 1. Start interactive script
./scripts/native-container/native-container.sh

# 2. Choose option 1 (Setup container)
# 3. Choose option 2 (Start container)
# 4. Choose option 9 (Run analysis)
# 5. Choose option 1 (Demo analysis)
```

### Command Line Usage

```bash
# Setup and start
./scripts/native-container/setup.sh
./scripts/native-container/run.sh

# Execute analysis
./scripts/native-container/exec.sh --analysis 'nz demo --rule PHLD'

# Run tests
./scripts/native-container/exec.sh --test

# View logs
./scripts/native-container/logs.sh --follow

# Stop and cleanup
./scripts/native-container/stop.sh
./scripts/native-container/cleanup.sh --all
```

### Available Commands Inside Container

#### Analysis Commands
```bash
# Main analysis command
nz demo --rule PHLD
nz yfinance AAPL --rule PHLD
nz mql5 BTCUSD --interval H4 --rule PHLD

# EDA analysis
eda
```

#### UV Package Manager
```bash
# Install dependencies
uv-install

# Update dependencies
uv-update

# Test UV environment
uv-test
```

#### Testing
```bash
# Run all tests
pytest

# Run tests with multithreading
pytest tests/ -n auto

# Run specific test categories
pytest tests/calculation/
pytest tests/cli/
pytest tests/data/
```

#### Development
```bash
# Show help
python run_analysis.py -h

# Test UV environment
python scripts/test_uv_docker.py

# Check MCP server
python scripts/check_mcp_status.py
```

## Testing

### Running Tests

```bash
# Run all native container tests
pytest tests/native-container/

# Run specific test file
pytest tests/native-container/test_native_container_script.py

# Run with coverage
pytest tests/native-container/ --cov=scripts/native-container
```

### Test Coverage

The native container scripts are fully tested with:
- Unit tests for all functions
- Integration tests for workflows
- Error handling tests
- Performance tests
- Syntax validation tests

## Troubleshooting

### Common Issues

#### 1. Native Container Application Not Found

```bash
Error: Native container application not found
```

**Solution:**
- Install the native container application from macOS Developer Beta
- Download from: https://developer.apple.com/download/all/
- Ensure you have a valid Apple Developer account

#### 2. macOS Version Incompatibility

```bash
Warning: macOS version X.X detected
Warning: Native container is designed for macOS 26+ (Tahoe)
```

**Solution:**
- Update to macOS 26 Tahoe (Developer Beta) or higher
- Some features may work on earlier versions but with reduced performance

#### 3. Container Build Failures

```bash
Error: Failed to build container image
```

**Solution:**
- Check available disk space (minimum 10GB required)
- Verify Python 3.11+ installation
- Ensure all required files are present in project root
- Run cleanup and retry: `./cleanup.sh --all`

#### 4. Permission Issues

```bash
Error: Permission denied
```

**Solution:**
- Ensure script files are executable: `chmod +x *.sh`
- Check file ownership and permissions
- Run setup with elevated privileges if needed

#### 5. UV Package Manager Issues

```bash
Error: UV is not available
```

**Solution:**
- Container will automatically install UV if not available
- Check UV installation: `uv --version`
- Reinstall UV manually if needed: `curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh | bash`

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# Set debug log level
export LOG_LEVEL=DEBUG

# Run container with debug output
./run.sh
```

### Log Analysis

View detailed logs for troubleshooting:

```bash
# View all logs
./logs.sh --list

# Follow container logs
./logs.sh --follow

# Filter for errors
./logs.sh --grep 'ERROR'
```

## CI/CD Integration

### GitHub Actions Workflow

Create `.github/workflows/native-container.yml`:

```yaml
name: Native Container Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-native-container:
    runs-on: macos-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install UV
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
    
    - name: Install dependencies
      run: |
        uv pip install -r requirements.txt
        uv pip install -r requirements-dev.txt
    
    - name: Run native container tests
      run: |
        pytest tests/native-container/ --tb=short -m "not skip_if_docker"
    
    - name: Run non-interactive tests
      run: |
        pytest tests/native-container/ -k "not interactive" --tb=short
```

### CI Best Practices

1. **Skip Interactive Tests**: Use `-m "not skip_if_docker"` to skip tests requiring tty
2. **Short Tracebacks**: Use `--tb=short` for cleaner CI output
3. **Environment Detection**: Tests automatically detect CI environment
4. **Resource Limits**: Set appropriate resource limits for CI runners

### Local CI Testing

Test CI workflow locally:

```bash
# Simulate CI environment
export CI=true
export GITHUB_ACTIONS=true

# Run CI-style tests
pytest tests/native-container/ --tb=short -m "not skip_if_docker"
```

## Script Development and Maintenance

### Adding New Scripts

1. **Create Script**: `scripts/native-container/new_script.sh`
2. **Add Tests**: `tests/native-container/test_new_script.py`
3. **Update Interactive Script**: Add menu option to `native-container.sh`
4. **Update Documentation**: Update README and this guide

### Script Template

```bash
#!/bin/bash

# Script Description
# This script provides [functionality] for the native Apple Silicon container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    # Add other options
    echo
    echo "Examples:"
    echo "  $0              # Basic usage"
    echo "  $0 --help       # Show help"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    echo -e "${BLUE}=== Script Name ===${NC}"
    echo
    
    # Main logic here
    
    print_success "Script completed successfully"
}

# Run main function
main "$@"
```

### Test Template

```python
import pytest
import subprocess
from pathlib import Path
from tests.conftest import skip_if_docker

class TestNewScript:
    """Test cases for new_script.sh"""
    
    @skip_if_docker
    def test_script_exists(self):
        """Test that the script file exists"""
        script_path = Path("scripts/native-container/new_script.sh")
        assert script_path.exists()
        assert script_path.is_file()
    
    @skip_if_docker
    def test_script_executable(self):
        """Test that the script is executable"""
        script_path = Path("scripts/native-container/new_script.sh")
        assert script_path.stat().st_mode & 0o111 != 0
    
    @skip_if_docker
    def test_script_help(self):
        """Test that the script shows help"""
        result = subprocess.run(
            ["./scripts/native-container/new_script.sh", "--help"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        assert result.returncode == 0
        assert "Usage:" in result.stdout
    
    @skip_if_docker
    def test_script_basic_functionality(self):
        """Test basic script functionality"""
        result = subprocess.run(
            ["./scripts/native-container/new_script.sh"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        # Add assertions based on expected behavior
        assert result.returncode == 0
    
    @pytest.mark.skip(reason="Requires interactive terminal (tty)")
    def test_script_interactive_mode(self):
        """Test interactive mode (requires tty)"""
        # This test will be skipped in CI environments
        pass
```

## Documentation Updates

### When to Update Documentation

Update documentation when:
- Adding new scripts or features
- Changing script behavior or options
- Updating prerequisites or requirements
- Fixing bugs or issues
- Adding new test cases

### Documentation Files to Update

1. **`scripts/native-container/README.md`** - Script-specific documentation
2. **`docs/deployment/native-container-setup.md`** - This setup guide
3. **`README.md`** - Main project README
4. **`docs/deployment/native-vs-docker-comparison.md`** - Performance comparison

### Documentation Standards

- Use clear, concise language
- Include code examples
- Provide troubleshooting sections
- Keep examples up-to-date
- Use consistent formatting

## Manual Testing Guide

### Interactive Script Testing

```bash
# Start interactive script
./scripts/native-container/native-container.sh

# Test each menu option systematically:
# 1. Setup container - Should create container successfully
# 2. Start container - Should start without errors
# 3. Stop container - Should stop gracefully
# 4. Remove container - Should remove completely
# 5. Show container status - Should display current status
# 6. Show container logs - Should show log output
# 7. Execute command - Should run commands in container
# 8. Start interactive shell - Should open bash shell
# 9. Run analysis - Should execute analysis commands
# 10. Run tests - Should run test suites
# 11. Show available commands - Should list commands
# 12. Cleanup resources - Should clean specified resources
# 13. System check - Should verify requirements
# 14. Exit - Should exit cleanly
```

### Individual Script Testing

```bash
# Test setup script
./scripts/native-container/setup.sh
./scripts/native-container/setup.sh --help

# Test run script
./scripts/native-container/run.sh
./scripts/native-container/run.sh --status
./scripts/native-container/run.sh --help

# Test exec script
./scripts/native-container/exec.sh --shell
./scripts/native-container/exec.sh --command 'ls -la'
./scripts/native-container/exec.sh --help

# Test logs script
./scripts/native-container/logs.sh
./scripts/native-container/logs.sh --follow
./scripts/native-container/logs.sh --list
./scripts/native-container/logs.sh --help

# Test stop script
./scripts/native-container/stop.sh
./scripts/native-container/stop.sh --force
./scripts/native-container/stop.sh --help

# Test cleanup script
./scripts/native-container/cleanup.sh --all --force
./scripts/native-container/cleanup.sh --help
```

### Error Condition Testing

```bash
# Test with missing container
./scripts/native-container/run.sh

# Test with missing dependencies
./scripts/native-container/setup.sh

# Test with invalid commands
./scripts/native-container/exec.sh --command 'invalid_command'

# Test with missing files
rm container.yaml
./scripts/native-container/setup.sh

# Test with insufficient permissions
chmod -x scripts/native-container/setup.sh
./scripts/native-container/setup.sh
```

### Performance Testing

```bash
# Measure startup time
time ./scripts/native-container/run.sh

# Compare with Docker
time docker-compose up -d

# Test analysis performance
time ./scripts/native-container/exec.sh --analysis 'nz demo --rule PHLD'

# Monitor resource usage
./scripts/native-container/logs.sh system
```

## Folder Structure

### Complete Directory Structure

```
neozork-hld-prediction/
├── scripts/
│   └── native-container/
│       ├── native-container.sh    # Interactive container manager
│       ├── setup.sh               # Initial setup and configuration
│       ├── run.sh                 # Start the container
│       ├── stop.sh                # Stop the container
│       ├── logs.sh                # View container logs
│       ├── exec.sh                # Execute commands in container
│       ├── cleanup.sh             # Clean up resources
│       ├── README.md              # Script documentation
│       └── __init__.py            # Python package marker
├── tests/
│   └── native-container/
│       ├── test_native_container_script.py  # Interactive script tests
│       ├── test_setup_script.py             # Setup script tests
│       ├── test_run_script.py               # Run script tests
│       ├── test_stop_script.py              # Stop script tests
│       ├── test_logs_script.py              # Logs script tests
│       ├── test_exec_script.py              # Exec script tests
│       ├── test_cleanup_script.py           # Cleanup script tests
│       └── __init__.py                      # Test package marker
├── docs/
│   └── deployment/
│       ├── native-container-setup.md        # This setup guide
│       ├── native-vs-docker-comparison.md   # Performance comparison
│       └── docker-setup.md                  # Docker setup guide
├── container.yaml                           # Container configuration
├── container-entrypoint.sh                  # Container entrypoint
├── requirements.txt                         # Python dependencies
├── run_analysis.py                          # Main analysis script
└── README.md                                # Main project README
```

### File Descriptions

- **`native-container.sh`**: Main interactive script with menu system
- **`setup.sh`**: Initial setup, validation, and container creation
- **`run.sh`**: Container startup and status management
- **`stop.sh`**: Graceful container shutdown and cleanup
- **`logs.sh`**: Log viewing and filtering capabilities
- **`exec.sh`**: Command execution and interactive shell access
- **`cleanup.sh`**: Resource cleanup and maintenance
- **`container.yaml`**: Native container configuration
- **`container-entrypoint.sh`**: Container initialization script

## Version History

### v2.0.0 (Current)
- Added native Apple Silicon container support
- Interactive script with menu system
- Comprehensive test suite
- Performance improvements (30-50% over Docker)
- Complete documentation

### v1.0.0 (Previous)
- Docker-only support
- Basic UV integration
- Initial test framework

## Support and Maintenance

### Getting Help

1. **Check Documentation**: Review this guide and README files
2. **Run Tests**: Execute test suite to identify issues
3. **Check Logs**: Use `./logs.sh` to view detailed logs
4. **Interactive Script**: Use `./native-container.sh` for guided troubleshooting
5. **GitHub Issues**: Report bugs and request features

### Maintenance Schedule

- **Weekly**: Run test suite to ensure functionality
- **Monthly**: Update dependencies and check for updates
- **Quarterly**: Review and update documentation
- **As Needed**: Update scripts based on user feedback

### Contributing

To contribute to native container support:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/native-container-improvement`
3. **Make changes**: Update scripts, tests, or documentation
4. **Test thoroughly**: Run all tests and manual testing
5. **Update documentation**: Ensure all changes are documented
6. **Submit pull request**: Include detailed description of changes

## Conclusion

The native Apple Silicon container provides significant performance improvements and better integration with macOS. The interactive script makes it easy to manage containers, while the comprehensive test suite ensures reliability.

For the best experience:
- Use the interactive script for daily operations
- Run tests regularly to ensure functionality
- Keep documentation updated
- Monitor performance and resource usage
- Report issues and contribute improvements

The native container represents the future of containerization on Apple Silicon, providing native performance with the convenience of containerized applications. 