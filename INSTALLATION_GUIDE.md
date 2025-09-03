# Installation Guide

## Overview

This guide provides comprehensive installation instructions for the Neozork HLD Prediction system across different platforms and environments.

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS (10.15+), Windows (10+)
- **Python**: 3.9+ (3.11+ recommended)
- **Memory**: 4GB+ RAM (8GB+ for production)
- **Storage**: 10GB+ free space
- **Network**: Internet access for package installation

### Software Dependencies
- **UV**: Python package manager (recommended)
- **Git**: Version control
- **Build Tools**: Compiler and development headers
- **System Packages**: Platform-specific dependencies

## Quick Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction
```

### 2. Install UV
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 3. Install Dependencies
```bash
# Install all dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### 4. Verify Installation
```bash
# Run tests
uv run pytest tests/ -v

# Test CLI
uv run python -m src.cli.core.cli --help

# Check imports
uv run python -c "import src; print('Import successful')"
```

## Platform-Specific Installation

### Ubuntu/Debian Linux
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    python3-dev \
    git \
    curl

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Clone and install
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction
uv sync
```

### CentOS/RHEL/Fedora
```bash
# Update system packages
sudo dnf update -y  # or sudo yum update -y

# Install system dependencies
sudo dnf install -y \
    python3 \
    python3-pip \
    python3-devel \
    gcc \
    gcc-c++ \
    make \
    git \
    curl

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Clone and install
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction
uv sync
```

### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install python3 git curl

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Clone and install
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction
uv sync
```

### Windows
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install system dependencies
choco install python git curl -y

# Install UV
irm https://astral.sh/uv/install.ps1 | iex

# Add UV to PATH (restart PowerShell after this)
$env:PATH += ";$env:USERPROFILE\.cargo\bin"

# Clone and install
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction
uv sync
```

## Alternative Installation Methods

### Using pip
```bash
# Clone repository
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Using conda
```bash
# Clone repository
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction

# Create conda environment
conda create -n neozork python=3.11 -y
conda activate neozork

# Install dependencies
conda install --file requirements-conda.txt -y
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Development Installation

### Full Development Setup
```bash
# Clone repository
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies including development tools
uv sync --group dev

# Install pre-commit hooks
uv run pre-commit install

# Install additional development tools
uv add --dev black isort mypy flake8 ruff pytest-cov pytest-xdist

# Verify development setup
uv run black --check src/
uv run isort --check-only src/
uv run mypy src/
uv run pytest tests/ --cov=src
```

### Development Dependencies
```bash
# Install specific development groups
uv sync --group dev      # Development tools
uv sync --group ml       # Machine learning dependencies
uv sync --group data     # Data processing dependencies
uv sync --group viz      # Visualization dependencies
uv sync --group test     # Testing dependencies
```

## Configuration Setup

### Initial Configuration
```bash
# Copy configuration template
cp config.example.json config.json

# Edit configuration
nano config.json  # or use your preferred editor

# Set environment-specific configuration
export NEOZORK_ENV=development
export NEOZORK_CONFIG_PATH=config.json
```

### Configuration File Structure
```json
{
  "system": {
    "name": "Neozork HLD Prediction System",
    "version": "1.0.0",
    "environment": "development"
  },
  "data": {
    "cache_dir": "data/cache",
    "raw_dir": "data/raw",
    "processed_dir": "data/processed"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/system.log"
  }
}
```

### Environment Variables
```bash
# Basic configuration
export NEOZORK_ENV=development
export NEOZORK_LOG_LEVEL=INFO
export NEOZORK_CONFIG_PATH=config.json

# Data configuration
export NEOZORK_DATA_CACHE_DIR=data/cache
export NEOZORK_DATA_RAW_DIR=data/raw

# Analysis configuration
export NEOZORK_ANALYSIS_DEFAULT_TIMEFRAME=1H
export NEOZORK_ANALYSIS_MAX_LOOKBACK_PERIODS=1000
```

## Directory Structure Setup

### Create Required Directories
```bash
# Create main directories
mkdir -p data/{raw,processed,cache}
mkdir -p logs
mkdir -p models
mkdir -p results/{plots,reports}
mkdir -p tests/{unit,integration,performance}

# Set permissions
chmod 755 data logs models results tests
chmod 644 config.json
```

### Directory Permissions
```bash
# Set appropriate permissions
chmod 755 data/
chmod 755 logs/
chmod 755 models/
chmod 755 results/

# Make sure user can write to these directories
chown -R $USER:$USER data/ logs/ models/ results/
```

## Verification Steps

### Basic Verification
```bash
# Check Python version
uv run python --version

# Check package installation
uv run python -c "import src; print('Package imported successfully')"

# Check CLI availability
uv run python -m src.cli.core.cli --help

# Check configuration loading
uv run python -c "
from src.core.config import Config
config = Config()
print('Configuration loaded:', config._config)
"
```

### Test Verification
```bash
# Run basic tests
uv run pytest tests/unit/ -v

# Run with coverage
uv run pytest tests/unit/ --cov=src --cov-report=term

# Run specific test categories
uv run pytest tests/unit/core/ -v
uv run pytest tests/unit/cli/ -v
```

### Performance Verification
```bash
# Check import performance
time uv run python -c "import src"

# Check test execution performance
time uv run pytest tests/unit/ -q

# Check memory usage
uv run python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

## Troubleshooting

### Common Installation Issues

#### Python Version Issues
```bash
# Check Python version
python3 --version

# Install specific Python version
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv python3.11-dev

# macOS
brew install python@3.11

# Windows
# Download from python.org
```

#### UV Installation Issues
```bash
# Check UV installation
which uv
uv --version

# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH manually
export PATH="$HOME/.cargo/bin:$PATH"
```

#### Dependency Issues
```bash
# Clear UV cache
uv cache clean

# Reinstall dependencies
uv sync --reinstall

# Check for conflicts
uv sync --dry-run
```

#### Permission Issues
```bash
# Check file permissions
ls -la

# Fix permissions
chmod 644 config.json
chmod 755 data/ logs/ models/ results/

# Check directory ownership
ls -la | grep -E "(data|logs|models|results)"
```

### Platform-Specific Issues

#### Linux Issues
```bash
# Install missing system packages
sudo apt install -y build-essential python3-dev

# Fix SSL issues
sudo apt install -y ca-certificates

# Fix locale issues
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
```

#### macOS Issues
```bash
# Install Xcode command line tools
xcode-select --install

# Fix SSL issues
brew install openssl
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"

# Fix locale issues
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

#### Windows Issues
```powershell
# Install Visual Studio Build Tools
choco install visualstudio2019buildtools -y

# Fix PATH issues
$env:PATH += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC\14.29.30133\bin\Hostx64\x64"

# Fix SSL issues
# Download and install certificates
```

## Performance Optimization

### UV Configuration
```bash
# Optimize UV settings
export UV_CACHE_DIR="$HOME/.cache/uv"
export UV_CONFIG_FILE="$HOME/.config/uv/config.toml"

# Create optimized UV config
mkdir -p ~/.config/uv
cat > ~/.config/uv/config.toml <<EOF
[global]
cache-dir = "$HOME/.cache/uv"
index-url = "https://pypi.org/simple/"
extra-index-url = []

[install]
no-cache = false
upgrade = false
EOF
```

### Python Optimization
```bash
# Set Python optimization flags
export PYTHONOPTIMIZE=2
export PYTHONDONTWRITEBYTECODE=1

# Use optimized Python builds
# Consider using pyenv for Python version management
```

## Security Considerations

### File Permissions
```bash
# Secure configuration files
chmod 600 config.json
chmod 600 .env

# Secure directories
chmod 700 data/
chmod 700 logs/
chmod 700 models/

# Check for sensitive files
find . -name "*.key" -o -name "*.pem" -o -name ".env*"
```

### Environment Security
```bash
# Use .env file for sensitive data
echo "NEOZORK_API_KEY=your_secret_key" > .env
echo ".env" >> .gitignore

# Set secure environment variables
export NEOZORK_SECURE_MODE=true
export NEOZORK_DEBUG_MODE=false
```

## Updating Installation

### Update Dependencies
```bash
# Update all dependencies
uv sync --upgrade

# Update specific groups
uv sync --group dev --upgrade
uv sync --group ml --upgrade

# Check for outdated packages
uv sync --outdated
```

### Update Application
```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
uv sync

# Run tests to ensure compatibility
uv run pytest tests/ -v

# Update configuration if needed
# Compare config.example.json with your config.json
```

## Uninstallation

### Remove Application
```bash
# Remove virtual environment
rm -rf .venv

# Remove installed packages
uv cache clean

# Remove application files
cd ..
rm -rf neozork-hld-prediction
```

### Remove System Dependencies
```bash
# Ubuntu/Debian
sudo apt remove -y build-essential python3-dev

# macOS
brew uninstall python3

# Windows
choco uninstall python git curl
```

## Support and Resources

### Getting Help
- **Documentation**: Check `docs/` directory
- **Issues**: GitHub Issues repository
- **Discussions**: GitHub Discussions
- **Wiki**: Project wiki for common problems

### Installation Resources
- **UV Documentation**: https://docs.astral.sh/uv/
- **Python Installation**: https://docs.python.org/3/using/
- **Platform Guides**: Check platform-specific documentation

### Troubleshooting Resources
- **Common Issues**: Review troubleshooting section
- **Error Messages**: Search for specific error messages
- **Community**: Ask questions on GitHub Discussions
