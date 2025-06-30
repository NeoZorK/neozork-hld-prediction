# Native Container Documentation

This section contains detailed documentation for the Native Container implementation, which provides Apple Silicon-optimized container functionality with full Docker parity.

## Overview

The Native Container leverages macOS 26+ (Tahoe) native container technology to provide superior performance and better integration with Apple Silicon while maintaining complete feature parity with the Docker container.

## Quick Navigation

### Core Documentation
- [README](README.md) - Complete native container documentation
- [Full Docker Parity Summary](FULL_DOCKER_PARITY_SUMMARY.md) - Feature parity implementation details
- [Smart Container Logic](SMART_CONTAINER_LOGIC.md) - Intelligent container state management
- [Smart Container Logic Summary](SMART_CONTAINER_LOGIC_SUMMARY.md) - Logic implementation summary

## Key Features

### ✅ Full Docker Parity
- **UV Package Manager Support**: UV-only mode enforcement
- **MCP Server Integration**: Interactive MCP server management
- **Command Wrappers**: `nz`, `eda`, `uv-*`, `mcp-*` commands
- **Bash Environment**: Interactive shell with history and completion
- **External Data Feed Tests**: Polygon.io, YFinance, Binance API testing
- **Usage Guide**: Comprehensive help and command reference

### 🚀 Performance Benefits
- **30-50% faster startup** times compared to Docker
- **Lower memory usage** and resource consumption
- **Better Apple Silicon integration** and optimization
- **Native macOS terminal** support
- **Improved file system** performance

### 🔧 Technical Features
- **Smart Container Logic**: Automatic state management
- **UV Verification**: Environment validation
- **MCP Server Management**: Process monitoring and cleanup
- **Directory Structure**: Complete Docker parity
- **Volume Mounts**: Data persistence and caching

## Architecture

### Container Structure
```
neozork-hld-prediction/
├── container.yaml              # Native container configuration
├── container-entrypoint.sh     # Full-featured entrypoint script
├── scripts/native-container/   # Management scripts
│   ├── setup.sh               # Setup with full Docker parity
│   ├── run.sh                 # Container execution
│   ├── stop.sh                # Container stopping
│   ├── exec.sh                # Interactive shell access
│   ├── logs.sh                # Log viewing
│   └── cleanup.sh             # Resource cleanup
└── tests/native-container/    # Native container tests
    └── test_native_container_full_functionality.py
```

### Environment Configuration
- **UV Configuration**: `USE_UV=true`, `UV_ONLY=true`
- **Container Type**: `NATIVE_CONTAINER=true`
- **MCP Server**: `MCP_SERVER_TYPE=pycharm_copilot`
- **Resource Allocation**: 4GB RAM, 2 CPU cores, 10GB storage

## Implementation Details

### Smart Container Logic
The native container implements intelligent state management:

1. **Container Already Running**: Skip setup, open shell directly
2. **Container Exists But Stopped**: Start existing container, then open shell
3. **Container Doesn't Exist**: Run full setup sequence

### Docker Parity Features
- **23 test cases** covering all functionality
- **100% pass rate** after implementation
- **Complete functionality** validation
- **File and permission** verification
- **Configuration validation**

## Usage Examples

### Basic Commands
```bash
# Start container with interactive shell
./scripts/native-container/run.sh

# Access interactive shell
./scripts/native-container/exec.sh --shell

# Stop container
./scripts/native-container/stop.sh

# Cleanup resources
./scripts/native-container/cleanup.sh --all --force
```

### Analysis Commands
```bash
nz --interactive                    # Interactive analysis
nz demo --rule PHLD                # Demo analysis
nz yfinance AAPL --rule PHLD       # YFinance analysis
eda -dqc                           # Data quality checks
```

### UV Package Manager
```bash
uv-install                         # Install dependencies
uv-update                          # Update dependencies
uv-test                            # Run UV environment test
uv-pytest                          # Run pytest with UV
```

### MCP Server
```bash
mcp-start                          # Start MCP server
mcp-check                          # Check MCP server status
```

## Testing

### Test Coverage
- **23 comprehensive test cases**
- **Complete functionality validation**
- **File existence and permission verification**
- **Configuration validation**
- **Performance verification**

### Test Categories
- ✅ Container setup and configuration
- ✅ Entrypoint script functionality
- ✅ UV package manager integration
- ✅ MCP server integration
- ✅ Command wrapper creation
- ✅ Bash environment setup
- ✅ Directory structure validation
- ✅ File permissions and existence
- ✅ Environment variable configuration

## Troubleshooting

### Common Issues
- **Container state conflicts**: Handled by smart logic
- **UV environment issues**: Automatic verification and setup
- **MCP server problems**: Status checking and restart procedures
- **Permission issues**: Automatic directory and file permission setup

### Performance Optimization
- **Resource allocation**: Configurable memory, CPU, and storage
- **UV cache management**: Optimized package caching
- **File system optimization**: Native macOS file system integration

## Related Documentation

- [Container Overview](../index.md) - General container documentation
- [Native Container Setup](../native-container-setup.md) - Setup guide
- [Native Container Features](../native-container-features.md) - Feature overview
- [Development Testing](../../development/testing.md) - Testing procedures
- [Deployment Guides](../../deployment/) - Production deployment 