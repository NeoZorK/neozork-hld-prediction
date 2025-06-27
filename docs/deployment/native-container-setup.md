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

## Performance Benefits

### Native Apple Silicon Optimization

- **30-50% performance improvement** compared to Docker
- **Lower memory usage** due to native virtualization
- **Faster startup times** with optimized container initialization
- **Better integration** with macOS system resources

### Resource Efficiency

- **Reduced CPU overhead** from native containerization
- **Optimized memory management** for Apple Silicon
- **Efficient file system access** with native volume mounts
- **Lower power consumption** during idle periods

## Migration from Docker

### Benefits of Migration

- **30-50% performance improvement**
- **Lower resource usage**
- **Better macOS integration**
- **Native Apple Silicon optimizations**

### Migration Steps

1. **Install native container application**
2. **Run interactive script**: `./native-container.sh`
3. **Follow setup wizard**
4. **Test functionality**
5. **Update CI/CD pipelines** if needed

### Rollback Plan

- **Keep Docker setup as backup**
- **Both can run simultaneously**
- **Easy rollback to Docker if needed**

## Best Practices

1. **Use interactive script** for easiest experience
2. **Monitor resource usage** with native tools
3. **Leverage native logging** for debugging
4. **Use volume mounts** for data persistence
5. **Keep container updated** with latest macOS

## Support

For issues and questions:

1. **Use interactive script**: `./native-container.sh`
2. **Check the logs**: `./logs.sh`
3. **Review the documentation**: `docs/deployment/native-container-setup.md`
4. **Check the main project README**
5. **Open an issue on GitHub**

## Comparison with Docker

| Feature | Native Container | Docker |
|---------|------------------|--------|
| Performance | 30-50% faster | Baseline |
| Memory Usage | Lower | Higher |
| Startup Time | Faster | Slower |
| macOS Integration | Native | Virtualized |
| Cross-platform | No (macOS 26+) | Yes |
| Resource Overhead | Minimal | Higher |
| Apple Silicon | Optimized | Generic |

For detailed comparison, see: `docs/deployment/native-vs-docker-comparison.md` 