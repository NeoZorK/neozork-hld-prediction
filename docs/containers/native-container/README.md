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
3. **Command Wrapper Creation** - Creates all utility commands
4. **Data Feed Tests** - Interactive external API testing
5. **MCP Server Management** - Startup, monitoring, and cleanup
6. **Usage Guide Display** - Comprehensive help and examples
7. **History Initialization** - Pre-loads useful commands
8. **Commands File Creation** - Creates reference file

## 🧪 Testing

### Run Native Container Tests
```bash
# Test full functionality
uv run pytest tests/native-container/test_native_container_full_functionality.py -v

# Test specific features
uv run pytest tests/native-container/ -k "uv" -v
uv run pytest tests/native-container/ -k "mcp" -v
```

### Test Coverage
The native container tests cover:
- ✅ Container setup and configuration
- ✅ Entrypoint script functionality
- ✅ UV package manager integration
- ✅ MCP server integration
- ✅ Command wrapper creation
- ✅ Bash environment setup
- ✅ Directory structure validation
- ✅ File permissions and existence
- ✅ Environment variable configuration

## 📊 Performance Benefits

### vs Docker Container
- **Faster startup** - Native container technology
- **Better Apple Silicon integration** - Optimized for ARM64
- **Lower resource usage** - More efficient memory management
- **Improved file system performance** - Native volume mounts
- **Better terminal integration** - Native macOS terminal support

### Resource Usage
- **Memory**: 4GB allocated (configurable)
- **CPU**: 2 cores allocated (configurable)
- **Storage**: 10GB allocated (configurable)
- **Network**: Native macOS networking

## 🔍 Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check native container service
container system status

# Start service if needed
container system start

# Check container logs
./scripts/native-container/logs.sh
```

#### UV Issues
```bash
# Check UV installation
uv --version

# Reinstall UV in container
uv-install

# Test UV environment
uv-test
```

#### MCP Server Issues
```bash
# Check MCP server status
mcp-check

# Restart MCP server
mcp-start

# Check MCP logs
tail -f logs/mcp_server.log
```

#### Permission Issues
```bash
# Fix script permissions
chmod +x scripts/native-container/*.sh
chmod +x container-entrypoint.sh

# Fix directory permissions
chmod -R 755 data/ logs/ results/
```

### Debug Mode
```bash
# Run with debug output
DEBUG=true ./scripts/native-container/run.sh

# Check container status
./scripts/native-container/run.sh --status

# Analyze all logs
./scripts/native-container/analyze_all_logs.sh
```

## 📚 Documentation

### Related Documentation
- [Native Container Setup](../docs/deployment/native-container-setup.md)
- [Docker vs Native Comparison](../docs/deployment/native-vs-docker-comparison.md)
- [UV Package Manager Guide](../docs/development/uv-package-manager.md)
- [MCP Server Integration](../docs/reference/mcp-servers/README.md)

### API Documentation
- [Data Sources](../docs/api/data-sources.md)
- [Exchange Rate API](../docs/api/exchange-rate-api-complete.md)
- [Indicators Reference](../docs/reference/indicators/)

## 🤝 Contributing

### Adding New Features
1. **Update entrypoint script** - Add functionality to `container-entrypoint.sh`
2. **Update setup script** - Add configuration to `setup.sh`
3. **Add tests** - Create tests in `tests/native-container/`
4. **Update documentation** - Update this README and related docs
5. **Test thoroughly** - Ensure Docker parity is maintained

### Testing Guidelines
- All new features must have corresponding tests
- Tests should verify Docker parity
- Performance tests should be included
- Documentation should be updated

## 📈 Roadmap

### Planned Features
- [ ] **Multi-container support** - Run multiple analysis containers
- [ ] **GPU acceleration** - Metal Performance Shaders integration
- [ ] **Advanced monitoring** - Real-time resource monitoring
- [ ] **Automated testing** - CI/CD integration for native containers
- [ ] **Plugin system** - Extensible command wrapper system

### Performance Optimizations
- [ ] **Memory optimization** - Dynamic memory allocation
- [ ] **Cache optimization** - Intelligent UV cache management
- [ ] **Network optimization** - Native macOS networking features
- [ ] **Storage optimization** - Efficient volume mount strategies

## 📄 License

This native container implementation is part of the NeoZork HLD Prediction project and follows the same licensing terms.

---

**Note**: This native container provides full feature parity with the Docker container while offering improved performance and better integration with Apple Silicon. All Docker container features are available, including UV package management, MCP server integration, command wrappers, bash history, and external data feed testing. 