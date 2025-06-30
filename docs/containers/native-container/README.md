# Native Container for NeoZork HLD Prediction

## Overview

The Native Container provides a complete Apple Silicon-optimized environment for the NeoZork HLD Prediction project with **full feature parity** to the Docker container. This container leverages macOS 26+ (Tahoe) native container technology for improved performance and better integration with Apple Silicon.

## 🚀 Full Docker Parity Features

The Native Container now provides **complete feature parity** with the Docker container, including:

### ✅ UV Package Manager Support
- **UV-only mode** enforced for consistent dependency management
- Automatic UV installation and configuration
- Command wrappers: `uv-install`, `uv-update`, `uv-test`, `uv-pytest`
- UV cache management and optimization

### ✅ MCP Server Integration
- **MCP server startup** with interactive prompts
- **MCP server status checking** and monitoring
- Command wrappers: `mcp-start`, `mcp-check`
- Automatic cleanup on container exit
- Enhanced LLM support integration

### ✅ Command Wrappers & Scripts
- **`nz`** - Main analysis command wrapper
- **`eda`** - EDA analysis command wrapper
- **`uv-*`** - UV package manager wrappers
- **`mcp-*`** - MCP server management wrappers
- All wrappers available in PATH for easy access

### ✅ Bash Environment & History
- **Interactive bash shell** with custom prompt
- **Command history** with useful pre-loaded commands
- **Readline configuration** for better navigation
- **History persistence** between sessions
- **Tab completion** and arrow key navigation

### ✅ External Data Feed Tests
- **Interactive prompts** for running data feed tests
- **Polygon.io API** testing
- **YFinance API** testing  
- **Binance API** testing
- **Parquet file operations** testing

### ✅ Usage Guide & Help
- **Comprehensive usage guide** on startup
- **Command reference** with examples
- **Tips for viewing plots** and results
- **Available commands list** in `/tmp/neozork_commands.txt`

### ✅ Directory Structure & Permissions
- **Complete directory structure** matching Docker
- **Proper permissions** for all directories
- **Volume mounts** for data persistence
- **Cache directories** for UV and other tools

## 🏗️ Architecture

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

### Environment Variables
```bash
# UV Configuration
USE_UV=true
UV_ONLY=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv

# Container Type
NATIVE_CONTAINER=true
DOCKER_CONTAINER=false

# Python Configuration
PYTHONPATH=/app
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
MPLCONFIGDIR=/tmp/matplotlib-cache

# MCP Server
MCP_SERVER_TYPE=pycharm_copilot
LOG_LEVEL=INFO
```

## 🚀 Quick Start

### Prerequisites
- macOS 26+ (Tahoe) or higher
- Native container application installed
- Python 3.11+ installed
- At least 4GB of available RAM
- 10GB of available disk space

### Setup and Run
```bash
# 1. Setup container (full Docker parity)
./scripts/native-container/setup.sh

# 2. Run container with interactive shell
./scripts/native-container/run.sh

# 3. Access interactive shell
./scripts/native-container/exec.sh --shell

# 4. Stop container
./scripts/native-container/stop.sh

# 5. Cleanup resources
./scripts/native-container/cleanup.sh --all --force
```

### Interactive Menu
```bash
# Use the simplified interactive menu
./scripts/native-container/native-container.sh
```

## 📋 Available Commands

### Analysis Commands
```bash
nz --interactive                    # Interactive analysis
nz demo --rule PHLD                # Demo analysis
nz yfinance AAPL --rule PHLD       # YFinance analysis
nz mql5 BTCUSD --interval H4 --rule PHLD  # MQL5 analysis
eda -dqc                           # Data quality checks
eda --descriptive-stats            # Descriptive statistics
```

### UV Package Manager Commands
```bash
uv-install                         # Install dependencies
uv-update                          # Update dependencies
uv-test                            # Run UV environment test
uv-pytest                          # Run pytest with UV
uv pip list                        # List installed packages
uv pip install <package>           # Install specific package
```

### MCP Server Commands
```bash
mcp-start                          # Start MCP server
mcp-check                          # Check MCP server status
python scripts/check_mcp_status.py # Detailed MCP status
python neozork_mcp_server.py       # Direct MCP server
```

### Testing Commands
```bash
uv run pytest tests -n auto        # Run all tests with UV
python tests/run_tests_docker.py   # Run external data feed tests
```

## 🔧 Configuration

### Container Configuration (container.yaml)
```yaml
apiVersion: v1
kind: Container
metadata:
  name: neozork-hld-prediction
spec:
  image: python:3.11-slim
  architecture: arm64
  resources:
    memory: "4Gi"
    cpu: "2"
    storage: "10Gi"
  environment:
    - USE_UV=true
    - UV_ONLY=true
    - NATIVE_CONTAINER=true
    - MCP_SERVER_TYPE=pycharm_copilot
  volumes:
    - name: data-volume
      mountPath: /app/data
      hostPath: ./data
    - name: uv-cache-volume
      mountPath: /app/.uv_cache
      hostPath: ./data/cache/uv_cache
```

### Entrypoint Features
The `container-entrypoint.sh` provides:

1. **UV Verification** - Ensures UV is available and working
2. **Bash Environment Setup** - Configures history, readline, and prompt
3. **Interactive Menu** - Guides users through setup and testing
4. **MCP Server Management** - Handles MCP server startup and monitoring
5. **Command Wrappers** - Provides convenient aliases for common tasks

## 📁 Native Container Scripts

The project includes comprehensive management scripts in `scripts/native-container/` for complete container lifecycle management:

| Script                | Purpose                                                                                   |
|-----------------------|------------------------------------------------------------------------------------------|
| setup.sh              | Setup native container environment, verify dependencies, create directory structure      |
| run.sh                | Start container, check status, manage launch modes (interactive/detached)                |
| stop.sh               | Stop container gracefully or forcefully, remove container, cleanup resources            |
| exec.sh               | Execute commands and launch interactive shell with automatic venv activation            |
| logs.sh               | View container, application, and system logs with filtering and real-time following     |
| cleanup.sh            | Clean containers, temporary files, caches, logs, and results with selective options     |
| native-container.sh   | Interactive menu for start, stop, shell access, and container status management        |
| force_restart.sh      | Force restart container and services with emergency recovery procedures                 |
| analyze_all_logs.sh   | Analyze all container and application logs for troubleshooting                         |
| test_smart_logic.sh   | Test smart container management logic and automated decision making                     |
| test_interactive.sh   | Test interactive scenarios and user experience workflows                                |

### Using Native Container Scripts

```bash
# Interactive container management
./scripts/native-container/native-container.sh

# Manual setup and run sequence
./scripts/native-container/setup.sh
./scripts/native-container/run.sh
./scripts/native-container/exec.sh --shell

# Container monitoring and maintenance
./scripts/native-container/logs.sh --follow
./scripts/native-container/cleanup.sh --all

# Emergency procedures
./scripts/native-container/force_restart.sh
./scripts/native-container/analyze_all_logs.sh
```

## 🔍 Troubleshooting

### Common Issues

1. **Container not starting**
   - Check macOS version (requires 26+)
   - Verify native container application is installed
   - Ensure sufficient disk space and memory

2. **UV installation issues**
   - Container automatically installs UV if missing
   - Check UV cache directory permissions
   - Verify Python 3.11+ is available

3. **MCP server problems**
   - Check MCP server logs: `./scripts/native-container/logs.sh mcp`
   - Verify MCP_SERVER_TYPE configuration
   - Ensure proper network connectivity

### Debug Mode

```bash
# Run with verbose logging
./scripts/native-container/run.sh --debug

# Analyze all logs for issues
./scripts/native-container/analyze_all_logs.sh

# Test container logic
./scripts/native-container/test_smart_logic.sh
```

## 🚀 Performance Benefits

### Apple Silicon Optimization
- **Native ARM64 execution** - No emulation overhead
- **Optimized memory usage** - Better cache utilization
- **Faster startup times** - Reduced initialization overhead
- **Better thermal management** - Efficient power consumption

### UV Package Manager
- **Faster dependency resolution** - Rust-based performance
- **Optimized caching** - Intelligent package caching
- **Parallel installation** - Concurrent package downloads
- **Reduced disk usage** - Efficient storage management

## 🔒 Security Features

- **Isolated environment** - Complete process isolation
- **Non-root execution** - Secure user permissions
- **Minimal attack surface** - Only essential packages
- **Environment variable isolation** - Secure configuration

## 📊 Monitoring and Logging

### Log Management
```bash
# View real-time logs
./scripts/native-container/logs.sh --follow

# Filter logs by type
./scripts/native-container/logs.sh mcp --follow
./scripts/native-container/logs.sh app --grep "ERROR"

# Analyze log patterns
./scripts/native-container/analyze_all_logs.sh
```

### Performance Monitoring
- **Resource usage tracking** - Memory, CPU, disk I/O
- **Startup time measurement** - Container initialization metrics
- **Command execution timing** - Performance profiling
- **Cache hit rates** - UV and system cache efficiency

## 🔄 Migration from Docker

### Feature Parity Checklist
- ✅ **UV package manager** - Full compatibility
- ✅ **MCP server integration** - Identical functionality
- ✅ **Command wrappers** - Same interface
- ✅ **Interactive shell** - Enhanced experience
- ✅ **Volume mounts** - Identical data persistence
- ✅ **Environment variables** - Same configuration
- ✅ **Logging system** - Compatible log formats
- ✅ **Testing framework** - Same test execution

### Migration Steps
1. **Stop Docker container** - `docker compose down`
2. **Setup native container** - `./scripts/native-container/setup.sh`
3. **Start native container** - `./scripts/native-container/run.sh`
4. **Verify functionality** - Run tests and analysis
5. **Update workflows** - Use native container scripts

## 📚 Additional Resources

### Documentation
- [Native Container Setup Guide](../native-container-setup.md)
- [Native vs Docker Comparison](../native-vs-docker-comparison.md)
- [UV-Only Mode Guide](../uv-only-mode.md)
- [Emergency Restart Service](../emergency-restart-service.md)

### Testing
- [Native Container Tests](../../tests/native-container/)
- [Full Functionality Tests](../../tests/native-container/test_native_container_full_functionality.py)
- [Smart Logic Tests](../../tests/native-container/test_smart_logic.sh)

## 🤝 Support

For issues and questions:

1. **Check logs** - `./scripts/native-container/logs.sh`
2. **Review documentation** - See Additional Resources above
3. **Run diagnostics** - `./scripts/native-container/analyze_all_logs.sh`
4. **Test functionality** - `./scripts/native-container/test_smart_logic.sh`
5. **Open GitHub issue** - Include logs and system information 