# Installation Guide

Complete setup instructions for the NeoZork HLD Prediction project.

## Prerequisites

### Python 3.12+
Ensure you have Python 3.12 or higher installed:

**macOS:**
```bash
brew install python@3.12
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/)

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv
```

## Quick Setup

### 1. Clone Repository
```bash
git clone <your_repository_url>
cd neozork-hld-prediction
```

### 2. Initialize Project Structure
```bash
./scripts/init_dirs.sh
```
This creates all required directories and the `.env` file.

### 3. Create Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### 4. Install Dependencies

**Standard installation:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Fast installation with uv:**
```bash
pip install uv
uv pip install -r requirements.txt
```

### 5. Configure Environment Variables
Edit the `.env` file created by `init_dirs.sh`:

```env
# Polygon.io API key
POLYGON_API_KEY=your_polygon_api_key_here

# Binance API keys
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here
```

## Optional Components

### TA-Lib Installation
If using TA-Lib features:

**macOS:**
```bash
brew install ta-lib
pip install TA-Lib
```

**Linux:**
```bash
sudo apt-get install libta-lib-dev
pip install TA-Lib
```

**Windows:**
Download binaries or build from source, then:
```bash
pip install TA-Lib
```

### Testing Dependencies
```bash
pip install pytest
```

### BATS for Shell Testing
**macOS:**
```bash
brew install bats-core
```

**Linux:**
```bash
sudo apt-get install bats
```

## Verify Installation

Test your setup:
```bash
# Run demo analysis
python run_analysis.py demo

# Run tests
python -m pytest tests/ -v

# Test shell scripts
bats tests/scripts/test_init_dirs.bats
```

## Using UV Package Manager

For faster package management, see [UV Setup Guide](uv-setup.md).

## Docker Installation

For containerized environment, see [Docker Guide](docker.md).

## Troubleshooting

### Common Issues

**Import errors:** Ensure virtual environment is activated and all dependencies are installed.

**API connection issues:** Check your `.env` file configuration and API keys.

**Permission errors:** Make sure scripts have execute permissions:
```bash
chmod +x scripts/init_dirs.sh
chmod +x nz
```

### Getting Help

Run the help command to see all available options:
```bash
python run_analysis.py --help
```
