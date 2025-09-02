# 🍎 Quick Start: Native Apple Silicon Container

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## Prerequisites

> **Note**: Native Container support is limited to v0.5.2 and earlier versions.

- **macOS 26 Tahoe (Developer Beta)** or higher
- **Native container application** installed from Apple Developer Beta
- **Python 3.11+** installed
- **At least 4GB of available RAM**
- **10GB of available disk space**

## 🚀 Quick Start

### 1. Interactive Script (Recommended)

```bash
# Run the interactive container manager
./scripts/native-container/native-container.sh
```

This opens a user-friendly menu with all container operations:
- Setup and configuration
- Start/stop/remove containers
- Execute commands and run analysis
- View logs and status
- Run tests
- Cleanup resources

### 2. Individual Scripts

```bash
# Initial setup
./scripts/native-container/setup.sh

# Start container
./scripts/native-container/run.sh

# Execute commands
./scripts/native-container/exec.sh --shell

# View logs
./scripts/native-container/logs.sh --follow

# Stop container
./scripts/native-container/stop.sh

# Cleanup
./scripts/native-container/cleanup.sh --all --force
```

## 📊 Available Commands Inside Container

### Analysis Commands
```bash
# Demo analysis
nz demo --rule PHLD

# Apple stock analysis
nz yfinance AAPL --rule PHLD

# Bitcoin analysis
nz mql5 BTCUSD --interval H4 --rule PHLD

# EDA analysis
eda
```

### Testing
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

### UV Package Manager
```bash
# Install dependencies
uv-install

# Update dependencies
uv-update

# Test UV environment
uv-test
```

## 🧪 Testing

### Automated Testing
```bash
# Run all native container tests
pytest tests/native-container/ -v

# Run with coverage
pytest tests/native-container/ --cov=scripts/native-container
```

### Manual Testing
```bash
# Test interactive script
./scripts/native-container/native-container.sh

# Test individual scripts
./scripts/native-container/setup.sh
./scripts/native-container/run.sh
./scripts/native-container/exec.sh --shell
```

## 📚 Documentation

- **[Complete Setup Guide](docs/deployment/native-container-setup.md)** - Detailed setup instructions
- **[Interactive Script Guide](docs/containers/native-container/README.md)** - Interactive script documentation
- **[Performance Comparison](docs/deployment/native-vs-docker-comparison.md)** - Native vs Docker comparison

## 🔧 Troubleshooting

### Common Issues

1. **Native Container Application Not Found**
   - Install from: https://developer.apple.com/download/all/
   - Requires Apple Developer account

2. **macOS Version Incompatibility**
   - Update to macOS 26+ (Tahoe)
   - Some features may work on earlier versions

3. **Permission Issues**
   ```bash
   chmod +x scripts/native-container/*.sh
   ```

4. **Container Build Failures**
   - Check available disk space (10GB minimum)
   - Verify Python 3.11+ installation
   - Run cleanup: `./cleanup.sh --all`

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debug output
./scripts/native-container/run.sh
```

## 📈 Performance Benefits

- **30-50% performance improvement** over Docker
- **Lower memory usage**
- **Faster startup times**
- **Better macOS integration**
- **Native Apple Silicon optimizations**

## 🔄 Migration from Docker

### Benefits
- 30-50% performance improvement
- Lower resource usage
- Better macOS integration
- Native Apple Silicon optimizations

### Migration Steps
1. Install native container application
2. Run interactive script: `./native-container.sh`
3. Follow setup wizard
4. Test functionality
5. Update CI/CD pipelines if needed

### Rollback Plan
- Keep Docker setup as backup
- Both can run simultaneously
- Easy rollback to Docker if needed

## 🆘 Support

1. **Use interactive script**: `./native-container.sh`
2. **Check the logs**: `./logs.sh`
3. **Review documentation**: `docs/deployment/native-container-setup.md`
4. **Check main README**: `README.md`
5. **Open GitHub issue**

---

**Last Updated**: 2024  
**Version**: 2.0.0 (Native Container Support) 