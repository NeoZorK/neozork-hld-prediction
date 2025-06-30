# Automatic Dependency Installation

## Overview

The Native Container now automatically installs all dependencies using UV package manager when starting the container. This eliminates the need for manual dependency installation and ensures a consistent environment every time.

## 🚀 New Features

### Automatic Dependency Installation
- **No manual setup required** - Dependencies are installed automatically
- **UV package manager** - Fast and reliable dependency management
- **Virtual environment** - Isolated Python environment created automatically
- **Dependency verification** - Key packages are verified after installation

### Virtual Environment Management
- **Automatic creation** - `.venv` directory created if not exists
- **Auto-activation** - Virtual environment activated in all shells
- **Command wrappers** - All commands use the activated environment
- **Bash integration** - Automatic activation in interactive shells

## 🔧 How It Works

### Container Startup Sequence
1. **Directory creation** - All necessary directories created
2. **UV verification** - UV package manager availability checked
3. **Environment setup** - Virtual environment created/activated
4. **Dependency installation** - All packages from `requirements.txt` installed
5. **Verification** - Key dependencies verified
6. **Bash setup** - Interactive environment configured
7. **Command wrappers** - Utility commands created
8. **Shell launch** - Interactive bash shell started

### Dependency Installation Process
```bash
# 1. Check if venv exists
if [ ! -d "/app/.venv" ]; then
    uv venv /app/.venv
fi

# 2. Activate venv
source /app/.venv/bin/activate

# 3. Install dependencies
uv pip install -r /app/requirements.txt

# 4. Verify installation
verify_dependencies
```

## 📋 Key Dependencies Verified

The system automatically verifies these key packages:
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib** - Plotting
- **plotly** - Interactive plots
- **yfinance** - Financial data
- **pytest** - Testing framework

## 🎯 Usage

### Starting Container with Automatic Dependencies
```bash
# Use the interactive script
./scripts/native-container/native-container.sh

# Choose option 1: Start Container
# Dependencies will be installed automatically
```

### Manual Commands (if needed)
```bash
# Manual dependency installation (fallback)
uv-install

# Update dependencies
uv-update

# Check UV environment
uv-test

# Run tests with UV
uv-pytest
```

## 🔍 Verification

### Check Dependencies
```bash
# List installed packages
uv pip list

# Check specific package
uv pip show pandas

# Verify environment
python -c "import pandas, numpy, matplotlib, plotly, yfinance; print('All packages available')"
```

### Check Virtual Environment
```bash
# Verify venv is active
echo $VIRTUAL_ENV

# Check Python path
which python

# List venv packages
pip list
```

## 🛠️ Configuration

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
```

### Volume Mounts
```yaml
volumes:
  - name: uv-cache-volume
    mountPath: /app/.uv_cache
    hostPath: ./data/cache/uv_cache
```

## 🔧 Troubleshooting

### Dependency Installation Issues
```bash
# Check UV installation
uv --version

# Manual installation
uv-install

# Check requirements file
cat requirements.txt

# Verify Python version
python --version
```

### Virtual Environment Issues
```bash
# Check venv exists
ls -la /app/.venv

# Recreate venv
rm -rf /app/.venv
uv venv /app/.venv

# Activate manually
source /app/.venv/bin/activate
```

### Permission Issues
```bash
# Fix permissions
chmod -R 755 /app/.venv
chmod -R 755 /app/.uv_cache

# Check ownership
ls -la /app/.venv
```

## 📊 Performance Benefits

### vs Manual Installation
- **Faster startup** - Dependencies installed once, cached
- **Consistent environment** - Same packages every time
- **No manual intervention** - Fully automated process
- **Error handling** - Graceful fallbacks for failures

### UV Benefits
- **10-100x faster** than traditional pip
- **Reliable dependency resolution**
- **Caching** for faster subsequent installations
- **Lock file support** for reproducible builds

## 🧪 Testing

### Run Tests
```bash
# Test automatic dependency functionality
pytest tests/native-container/test_automatic_dependencies.py -v

# Test full container functionality
pytest tests/native-container/test_native_container_full_functionality.py -v
```

### Manual Testing
```bash
# Start container
./scripts/native-container/native-container.sh

# Verify dependencies are available
python -c "import pandas; print('pandas version:', pandas.__version__)"
python -c "import numpy; print('numpy version:', numpy.__version__)"
```

## 📈 Monitoring

### Log Files
```bash
# Container logs
./scripts/native-container/logs.sh

# Application logs
./scripts/native-container/logs.sh app

# UV cache information
ls -la data/cache/uv_cache/
```

### Status Commands
```bash
# Check container status
./scripts/native-container/run.sh --status

# Check UV environment
uv-test

# List installed packages
uv pip list
```

## 🔮 Future Enhancements

### Planned Features
- **Incremental updates** - Only install changed dependencies
- **Dependency profiling** - Track which packages are used most
- **Auto-cleanup** - Remove unused packages
- **Health checks** - Verify environment integrity

### Performance Optimizations
- **Parallel installation** - Install packages concurrently
- **Smart caching** - Intelligent cache management
- **Pre-built environments** - Cached container images
- **Delta updates** - Only download changed packages

## 📝 Migration Guide

### From Manual Installation
1. **No changes needed** - Automatic installation is backward compatible
2. **Existing venv** - Will be reused if compatible
3. **Manual commands** - Still available as fallbacks
4. **Configuration** - No changes to existing setup

### From Docker Container
1. **Same dependencies** - Uses same `requirements.txt`
2. **Same commands** - All commands work identically
3. **Better performance** - Native container advantages
4. **Automatic setup** - No manual dependency management

---

**Note**: The automatic dependency installation feature ensures that the Native Container provides a seamless experience with all dependencies ready to use immediately after startup. 