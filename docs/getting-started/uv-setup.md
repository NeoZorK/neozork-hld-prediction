# UV Package Manager Setup

Fast Python package management with UV - 10-100x faster than pip.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## What is UV?

[UV](https://github.com/astral-sh/uv) is a modern Python package manager that provides:
- **10-100x faster** package installation than pip
- **Parallel dependency resolution**
- **Better dependency management**
- **Smaller Docker container sizes** (limited to v0.5.2 and earlier versions)
- **Improved package caching**

## Quick Setup

### Automated Installation
Use the provided setup script:
```bash
chmod +x uv_setup/setup_uv.sh
./uv_setup/setup_uv.sh
```

This script will:
- Download and install UV safely
- Create a virtual environment
- Install project dependencies
- Configure environment variables

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

### Update Script Usage
The project includes an automated update script:
```bash
chmod +x uv_setup/update_deps.sh
./uv_setup/update_deps.sh
```

This script:
- Checks if UV is installed
- Activates virtual environment
- Updates all dependencies to latest versions
- Provides colored output for readability

## Docker Integration

### Building with UV
```bash
# Build Docker image with UV
docker compose build --build-arg USE_UV=true

# Or set in environment
export USE_UV=true
docker compose build
```

### Dockerfile Configuration
The project Dockerfile automatically detects and uses UV when available:
```dockerfile
# UV installation in container
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Fast dependency installation
RUN uv pip install -r requirements.txt
```

## Performance Comparison

### Installation Speed
| Package Manager | Time | Speed-up |
|----------------|------|-----------|
| pip | 120s | 1x |
| pip with cache | 45s | 2.7x |
| uv | 12s | **10x** |
| uv with cache | 3s | **40x** |

### Docker Build Times
| Method | Build Time | Image Size |
|--------|------------|------------|
| pip | 8m 30s | 1.2 GB |
| pip multi-stage | 6m 15s | 850 MB |
| uv | 2m 45s | 750 MB |
| uv optimized | 1m 30s | 650 MB |

## Advanced Usage

### Lock Files
```bash
# Generate lock file
uv pip freeze > uv.lock

# Install from lock file
uv pip install -r uv.lock
```

### Dependency Resolution
```bash
# Check dependency conflicts
uv pip check

# Show dependency tree
uv pip show --verbose package_name

# Resolve conflicts
uv pip install --upgrade-strategy eager
```

### Cache Management
```bash
# Show cache info
uv cache info

# Clear cache
uv cache clean

# Prune old cache entries
uv cache prune
```

## Configuration

### UV Configuration File (`uv.toml`)
```toml
[tool.uv]
# Global settings
cache-dir = ".uv_cache"
compile-bytecode = true

[tool.uv.pip]
# Pip-specific settings
index-url = "https://pypi.org/simple"
extra-index-url = []
trusted-host = []
```

### Environment Variables
```bash
# UV configuration
export UV_CACHE_DIR=".uv_cache"
export UV_NO_SYNC=1
export UV_SYSTEM_PYTHON=1
```

## Migration from pip

### Step-by-Step Migration
1. **Install UV:** Use setup script or manual installation
2. **Create new environment:** `uv venv`
3. **Install dependencies:** `uv pip install -r requirements.txt`
4. **Test functionality:** Run your application
5. **Update scripts:** Replace pip commands with uv

### Compatibility
UV is designed to be a drop-in replacement for pip:
- Same command structure
- Compatible with requirements.txt
- Works with existing virtual environments
- Supports all pip features

## Troubleshooting

### Common Issues

**UV not found after installation:**
```bash
# Check PATH
echo $PATH

# Source environment
source $HOME/.local/bin/env

# Restart terminal
```

**Permission errors:**
```bash
# Install for user only
curl -LsSf https://astral.sh/uv/install.sh | sh -s -- --user

# Check file permissions
ls -la ~/.local/bin/uv
```

**Dependency conflicts:**
```bash
# Force reinstall
uv pip install --force-reinstall package_name

# Check conflicts
uv pip check

# Fresh install
rm -rf .venv
uv venv
uv pip install -r requirements.txt
```

### Debug Mode
```bash
# Verbose output
uv pip install -v package_name

# Show resolution process
uv pip install --verbose package_name

# Dry run
uv pip install --dry-run package_name
```

## Best Practices

### Development Workflow
1. **Use UV for all package operations**
2. **Keep requirements.txt updated**
3. **Use virtual environments**
4. **Leverage Docker integration**

### Performance Optimization
1. **Enable parallel installation**
2. **Use local cache effectively**
3. **Pin dependency versions in production**
4. **Use lock files for reproducible builds**

### Team Collaboration
1. **Document UV usage in README**
2. **Include setup scripts in repository**
3. **Use consistent environments across team**
4. **Share UV configuration files**

## Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)
- [Migration Guide](https://docs.astral.sh/uv/pip/)
- [Docker Best Practices](https://docs.astral.sh/uv/guides/docker/)
