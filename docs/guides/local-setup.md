# Local Development Setup

## Overview

This guide covers setting up a local development environment for the NeoZork HLD Prediction project, including UV package manager installation and configuration.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## Prerequisites

- **Python 3.11+** installed
- **Git** for version control
- **UV package manager** (recommended) or pip
- **At least 4GB of available RAM**
- **10GB of available disk space**

## Installation

### 1. Clone Repository
```bash
# Clone the repository
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction
```

### 2. Install UV Package Manager (Recommended)

**Automated Installation:**
```bash
# Use the provided setup script
chmod +x uv_setup/setup_uv.sh
./uv_setup/setup_uv.sh
```

**Manual Installation:**

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

### 3. Alternative: Use pip
```bash
# Install with pip (slower)
pip install -r requirements.txt
```

## Environment Setup

### Create Virtual Environment
```bash
# Create virtual environment with UV
uv venv

# Activate environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

### Install Dependencies
```bash
# Install with UV (recommended)
uv pip install -r requirements.txt

# Or install with pip
pip install -r requirements.txt
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```bash
# API Keys (optional)
POLYGON_API_KEY=your_key_here
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
EXCHANGE_RATE_API_KEY=your_key_here

# Python Configuration
PYTHONPATH=.
LOG_LEVEL=INFO
```

### UV Configuration
The project uses `uv.toml` for UV configuration:

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

## Development Workflow

### Running the Application
```bash
# Demo analysis
python run_analysis.py demo --rule PHLD

# Interactive mode
python interactive_system.py

# CLI interface
python run_analysis.py --help
```

### Testing
```bash
# Run all tests with UV (multithreaded)
uv run pytest tests -n auto

# Run specific test categories
uv run pytest tests/calculation/ -n auto
uv run pytest tests/cli/ -n auto

# Run with coverage
uv run pytest tests/ --cov=src -n auto
```

### Development Tools
```bash
# Check UV status
python scripts/check_uv_mode.py --verbose

# Run debug scripts
python scripts/debug/debug_yfinance.py
python scripts/debug/debug_polygon_connection.py
```

## IDE Configuration

### VS Code
1. Open the project folder in VS Code
2. Select the Python interpreter from `.venv/bin/python`
3. Install Python extension if not already installed

### PyCharm
1. Open the project in PyCharm
2. Configure project interpreter to use `.venv/bin/python`
3. Set PYTHONPATH to include project root

### Cursor IDE
1. Open the project in Cursor
2. Configure MCP server integration
3. Set Python interpreter to `.venv/bin/python`

## Troubleshooting

### Common Issues

**UV not found:**
```bash
# Check PATH
echo $PATH
which uv

# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Import errors:**
```bash
# Check PYTHONPATH
echo $PYTHONPATH

# Set PYTHONPATH
export PYTHONPATH=.
```

**Permission errors:**
```bash
# Fix script permissions
chmod +x scripts/*.sh
chmod +x uv_setup/*.sh
```

### Performance Issues
```bash
# Clear UV cache
rm -rf ~/.cache/uv

# Reinstall dependencies
uv pip install --no-cache -r requirements.txt
```

## Best Practices

1. **Use UV Package Manager**: 10-100x faster than pip
2. **Virtual Environment**: Always use virtual environments for isolation
3. **Multithreaded Testing**: Use `uv run pytest tests -n auto` for faster execution
4. **Regular Updates**: Keep dependencies updated
5. **Environment Variables**: Use `.env` file for configuration

## Comparison with Container Setup

| Aspect | Local Setup | Container Setup |
|--------|-------------|-----------------|
| **Performance** | Native performance | Container overhead |
| **Setup Time** | 5-10 minutes | 15-30 minutes |
| **Resource Usage** | Lower | Higher |
| **Platform Support** | All platforms | Limited to v0.5.2 and earlier |
| **Maintenance** | Easier | More complex |

> **Note**: Container setup is limited to v0.5.2 and earlier versions. Local setup is currently recommended for all users.

## Related Documentation

- **[Getting Started](../getting-started/)** - Basic setup
- **[UV Package Management](uv-package-management.md)** - UV usage guide
- **[Testing](../testing/)** - Testing framework
- **[Development](../development/)** - Development workflow
- **[IDE Configuration](ide-configuration.md)** - IDE setup
