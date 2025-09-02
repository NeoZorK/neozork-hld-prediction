# UV Package Management Guide

## Overview

This guide covers the usage of UV package manager in the NeoZork HLD Prediction project, including local development and containerized environments.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## What is UV?

[UV](https://github.com/astral-sh/uv) is a modern Python package manager that provides:
- **10-100x faster** package installation than pip
- **Parallel dependency resolution**
- **Better dependency management**
- **Smaller Docker container sizes** (limited to v0.5.2 and earlier versions)
- **Improved package caching**

## Installation

### Automated Installation
```bash
# Use the provided setup script
chmod +x uv_setup/setup_uv.sh
./uv_setup/setup_uv.sh
```

### Manual Installation

**Linux/macOS:**
```bash
# Download installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
source $HOME/.local/bin/env
echo 'source $HOME/.local/bin/env' >> ~/.bashrc  # or ~/.zshrc
```

**Windows:**
```powershell
# Using PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

**Verify Installation:**
```bash
uv --version
```

## Basic Usage

### UV Commands (pip replacements)

| pip command | uv equivalent |
|-------------|---------------|
| `pip install package` | `uv pip install package` |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip uninstall package` | `uv pip uninstall package` |
| `pip list` | `uv pip list` |
| `pip freeze` | `uv pip freeze` |

### Virtual Environment Management
```bash
# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
uv pip install -r requirements.txt

# Deactivate
deactivate
```

## Project Integration

### Initial Setup
```bash
# Create project environment
cd neozork-hld-prediction
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Dependency Management
```bash
# Install new package
uv pip install pandas

# Install development dependencies
uv pip install pytest black flake8

# Update all dependencies
./uv_setup/update_deps.sh
```

## Docker Integration

> **Note**: Docker integration support is limited to v0.5.2 and earlier versions.

### UV-Only Mode in Docker
The project has been configured to use **UV package manager exclusively** within Docker containers:

```dockerfile
# Force UV usage - no fallback to pip
ARG USE_UV=true
ARG UV_ONLY=true

# Install uv - required for UV-only mode
RUN mkdir -p /tmp/uv-installer \
    && curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh -o /tmp/uv-installer/installer.sh \
    && chmod +x /tmp/uv-installer/installer.sh \
    && /tmp/uv-installer/installer.sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

# Install dependencies using UV only - no pip fallback
RUN uv pip install --no-cache -r requirements.txt
```

### Docker Environment Variables
```bash
# UV-only mode enforcement
USE_UV=true
UV_ONLY=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv
```

## Testing with UV

### Local Environment
```bash
# Run all tests (multithreaded)
uv run pytest tests -n auto

# Run specific test categories
uv run pytest tests/calculation/ -n auto
uv run pytest tests/cli/ -n auto

# Run with coverage
uv run pytest tests/ --cov=src -n auto
```

### Docker Environment
> **Note**: Docker testing is limited to v0.5.2 and earlier versions.

```bash
# Run all tests
pytest tests/ -v

# Run Docker-specific tests
pytest tests/docker/ -v

# Run UV-only mode tests
pytest tests/docker/test_uv_only_mode.py -v
```

## Performance Comparison

### UV vs Traditional pip
```bash
# Traditional pip (slower)
pip install -r requirements.txt  # ~30-60 seconds

# UV (much faster)
uv pip install -r requirements.txt  # ~3-10 seconds

# UV with caching (fastest)
uv pip install -r requirements.txt  # ~1-3 seconds (subsequent runs)
```

### Multithreaded Testing
```bash
# Single-threaded testing
pytest tests/  # ~2-5 minutes

# UV multithreaded testing
uv run pytest tests -n auto  # ~30-60 seconds
```

## Troubleshooting

### Common Issues
```bash
# Check UV status
python scripts/check_uv_mode.py --verbose

# Verify UV installation
uv --version

# Check environment
echo $PATH
which uv
```

### UV Cache Issues
```bash
# Clear UV cache
rm -rf ~/.cache/uv

# Reinstall dependencies
uv pip install --no-cache -r requirements.txt
```

## Configuration

### UV Configuration File (`uv.toml`)
```toml
[pip]
# Install packages without writing "*.pyc" files
compile-bytecode = false

# Dependency optimization
no-deps = false
only-binary = ["numpy", "pandas", "tensorflow", "torch"]

# Index configuration
index-url = "https://pypi.org/simple"
```

## Best Practices

1. **Use UV Exclusively**: No fallback to pip for consistency
2. **Leverage Caching**: UV cache provides significant performance improvements
3. **Multithreaded Testing**: Use `uv run pytest tests -n auto` for faster test execution
4. **Environment Isolation**: Use virtual environments for project isolation
5. **Regular Updates**: Keep UV and dependencies updated

## Related Documentation

- **[Getting Started](../getting-started/)** - Basic setup
- **[Development](../development/)** - Development workflow
- **[Testing](../testing/)** - Testing framework
- **[Containers](../containers/)** - Container documentation
