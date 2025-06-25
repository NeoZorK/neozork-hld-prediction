# IDE Configuration Guide

This guide covers the setup and configuration of MCP (Model Context Protocol) servers for different IDEs in the Neozork HLD Prediction project.

## Overview

The project supports three major IDEs with full MCP server integration:

- **Cursor IDE** - Primary IDE with advanced AI integration
- **VS Code** - Popular open-source editor
- **PyCharm** - Professional Python IDE

All configurations support:
- Docker containerization
- UV package manager
- Financial data analysis
- Technical indicators
- AI-powered suggestions

## Quick Setup

### Automatic Setup

Run the automated setup script to configure all IDEs:

```bash
python3 scripts/setup_ide_configs.py
```

This script will:
1. Detect system capabilities (Docker, UV)
2. Create/update configuration files for all IDEs
3. Generate a setup summary report
4. Validate configurations

### Manual Setup

If you prefer manual configuration, follow the IDE-specific sections below.

## Cursor IDE Configuration

### Configuration File
- **Location**: `cursor_mcp_config.json`
- **Auto-generated**: Yes (via setup script)

### Features
- **MCP Servers**: 
  - `neozork` - Local Python server
  - `neozork-docker` - Docker containerized server
- **AI Integration**: GitHub Copilot support
- **Financial Data**: Real-time data analysis
- **Technical Indicators**: 20+ indicators supported
- **Code Completion**: Context-aware suggestions

### Configuration Structure

```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${PROJECT_ROOT}",
        "LOG_LEVEL": "INFO",
        "DOCKER_CONTAINER": "false",
        "USE_UV": "true",
        "UV_PYTHON": "python3"
      },
      "cwd": "${PROJECT_ROOT}"
    },
    "neozork-docker": {
      "command": "docker",
      "args": [
        "compose", "run", "--rm", "-T",
        "-e", "PYTHONPATH=/app",
        "-e", "LOG_LEVEL=INFO",
        "-e", "DOCKER_CONTAINER=true",
        "-e", "USE_UV=true",
        "neozork-hld",
        "python3", "neozork_mcp_server.py"
      ],
      "env": {
        "DOCKER_HOST": "unix:///var/run/docker.sock"
      },
      "cwd": "${PROJECT_ROOT}"
    }
  },
  "serverSettings": {
    "neozork": {
      "enabled": true,
      "autoStart": true,
      "features": {
        "financial_data": true,
        "technical_indicators": true,
        "github_copilot": true,
        "code_completion": true,
        "project_analysis": true,
        "ai_suggestions": true,
        "docker_integration": true,
        "real_time_monitoring": true,
        "uv_integration": true
      }
    }
  }
}
```

### Usage

1. **Start Cursor IDE**
2. **Open the project folder**
3. **MCP server will auto-start** (if `autoStart: true`)
4. **Test connection**: Check status in Cursor's MCP panel

## VS Code Configuration

### Configuration File
- **Location**: `.vscode/settings.json`
- **Auto-generated**: Yes (via setup script)

### Features
- **MCP Extension**: Built-in MCP support
- **Python Integration**: UV package manager
- **Financial Data**: CSV, Parquet, JSON support
- **Testing**: Pytest integration
- **Linting**: Pylint configuration

### Configuration Structure

```json
{
  "mcp.servers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "LOG_LEVEL": "INFO",
        "DOCKER_CONTAINER": "false",
        "USE_UV": "true",
        "UV_PYTHON": "python3"
      },
      "cwd": "${workspaceFolder}"
    }
  },
  "mcp.serverSettings": {
    "neozork": {
      "enabled": true,
      "autoStart": true,
      "features": {
        "financial_data": true,
        "technical_indicators": true,
        "github_copilot": true,
        "code_completion": true,
        "project_analysis": true,
        "ai_suggestions": true,
        "docker_integration": true,
        "real_time_monitoring": true,
        "uv_integration": true
      }
    }
  },
  "python.defaultInterpreterPath": "python3",
  "python.packageManager": "uv",
  "python.terminal.activateEnvironment": true,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"]
}
```

### Required Extensions

Install these VS Code extensions:

```bash
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension ms-python.pylint
code --install-extension ms-python.pytest-adapter
```

### Usage

1. **Open VS Code**
2. **Open the project folder**
3. **Install required extensions**
4. **MCP server will auto-start**
5. **Test connection**: Check MCP status in VS Code

## PyCharm Configuration

### Configuration File
- **Location**: `pycharm_mcp_config.json`
- **Auto-generated**: Yes (via setup script)

### Features
- **Professional IDE**: Full Python development environment
- **MCP Integration**: Custom MCP server support
- **UV Support**: Modern package management
- **Docker Integration**: Containerized development
- **Testing**: Integrated test runner

### Configuration Structure

```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${PROJECT_ROOT}",
        "LOG_LEVEL": "INFO",
        "DOCKER_CONTAINER": "false",
        "USE_UV": "true",
        "UV_PYTHON": "python3"
      },
      "cwd": "${PROJECT_ROOT}"
    }
  },
  "serverSettings": {
    "neozork": {
      "enabled": true,
      "autoStart": true,
      "features": {
        "financial_data": true,
        "technical_indicators": true,
        "github_copilot": true,
        "code_completion": true,
        "project_analysis": true,
        "ai_suggestions": true,
        "docker_integration": true,
        "real_time_monitoring": true,
        "uv_integration": true
      }
    }
  },
  "pycharm": {
    "python": {
      "interpreter": "python3",
      "packageManager": "uv",
      "uvPath": "uv",
      "autoInstallDependencies": true
    },
    "mcp": {
      "autoStart": true,
      "logLevel": "info",
      "features": {
        "completion": true,
        "hover": true,
        "definition": true,
        "references": true,
        "workspaceSymbols": true,
        "diagnostics": true
      }
    }
  }
}
```

### Setup Steps

1. **Open PyCharm**
2. **Open the project folder**
3. **Configure Python interpreter** (UV recommended)
4. **Install MCP plugin** (if available)
5. **Load configuration**: Import `pycharm_mcp_config.json`

## Docker Integration

### Docker Support

All IDE configurations support Docker containerization:

```json
{
  "neozork-docker": {
    "command": "docker",
    "args": [
      "compose", "run", "--rm", "-T",
      "-e", "PYTHONPATH=/app",
      "-e", "LOG_LEVEL=INFO",
      "-e", "DOCKER_CONTAINER=true",
      "-e", "USE_UV=true",
      "neozork-hld",
      "python3", "neozork_mcp_server.py"
    ],
    "env": {
      "DOCKER_HOST": "unix:///var/run/docker.sock"
    },
    "cwd": "${PROJECT_ROOT}"
  }
}
```

### Docker Requirements

- **Docker Desktop**: Installed and running
- **Docker Compose**: Available
- **Container**: `neozork-hld` service defined in `docker-compose.yml`

### Usage

1. **Start Docker Desktop**
2. **Build container**: `docker compose build`
3. **Select Docker server** in IDE configuration
4. **MCP server runs in container**

## UV Package Manager Integration

### UV Support

All configurations support UV package manager:

```json
{
  "env": {
    "USE_UV": "true",
    "UV_PYTHON": "python3"
  },
  "python": {
    "packageManager": "uv",
    "uvPath": "uv",
    "autoInstallDependencies": true
  }
}
```

### UV Commands

Common UV commands for the project:

```bash
# Install dependencies
uv pip install -r requirements.txt

# Sync dependencies
uv sync

# Run script with UV
uv run python3 script.py

# Run tests with UV
uv run python -m pytest tests/ -v
```

## Financial Data Features

### Supported Data Formats

- **CSV**: Comma-separated values
- **Parquet**: Columnar storage format
- **JSON**: JavaScript Object Notation

### Data Directories

- `data/` - Main data directory
- `mql5_feed/` - MQL5 data feed
- `financial_data/` - Additional financial data

### Symbol Patterns

- `*_*` - General symbol pattern
- `*USD*` - USD pairs
- `*EUR*` - EUR pairs
- `*GBP*` - GBP pairs

### Timeframe Patterns

- `*D1*` - Daily
- `*H1*` - Hourly
- `*M15*` - 15-minute
- `*M5*` - 5-minute
- `*M1*` - 1-minute

## Technical Indicators

### Available Indicators

#### Trend Indicators
- **SMA** - Simple Moving Average
- **EMA** - Exponential Moving Average
- **ADX** - Average Directional Index
- **SAR** - Parabolic SAR
- **HMA** - Hull Moving Average

#### Oscillators
- **RSI** - Relative Strength Index
- **Stochastic** - Stochastic Oscillator
- **CCI** - Commodity Channel Index

#### Momentum
- **MACD** - Moving Average Convergence Divergence
- **Stochastic Oscillator** - Enhanced stochastic

#### Volatility
- **ATR** - Average True Range
- **Bollinger Bands** - Volatility bands
- **Standard Deviation** - Statistical volatility

#### Volume
- **OBV** - On-Balance Volume
- **VWAP** - Volume Weighted Average Price

#### Support/Resistance
- **Donchian Channels** - Price channels
- **Fibonacci Retracements** - Fibonacci levels
- **Pivot Points** - Support/resistance levels

#### Predictive
- **Time Series Forecast** - ML-based forecasting

#### Probability
- **Kelly Criterion** - Position sizing
- **Monte Carlo** - Risk simulation

#### Sentiment
- **COT** - Commitments of Traders
- **Fear & Greed** - Market sentiment
- **Social Sentiment** - Social media sentiment

## Code Snippets

### Import Snippets

```python
# Import pandas
import pandas as pd

# Import numpy
import numpy as np

# Import matplotlib
import matplotlib.pyplot as plt
```

### Data Loading Snippets

```python
# Read CSV file
df = pd.read_csv('data.csv')

# Read Parquet file
df = pd.read_parquet('data.parquet')
```

### Analysis Snippets

```python
# Calculate RSI indicator
rsi = calculate_rsi(df['close'], period=14)

# Calculate MACD indicator
macd = calculate_macd(df['close'])

# Backtest trading strategy
results = backtest_strategy(data, strategy_params)
```

### Docker Snippets

```bash
# Start Docker services
docker compose up -d

# Run MCP server in Docker
docker compose run --rm neozork-hld python3 neozork_mcp_server.py
```

### UV Snippets

```bash
# Install dependencies with UV
uv pip install -r requirements.txt

# Sync dependencies with UV
uv sync

# Run script with UV
uv run python3 script.py
```

### Testing Snippets

```bash
# Run tests
uv run python -m pytest tests/ -v
```

## Troubleshooting

### Common Issues

#### MCP Server Not Starting

1. **Check Python path**:
   ```bash
   which python3
   ```

2. **Check dependencies**:
   ```bash
   uv pip list
   ```

3. **Check logs**:
   ```bash
   tail -f logs/neozork_mcp.log
   ```

#### Docker Issues

1. **Check Docker status**:
   ```bash
   docker --version
   docker compose version
   ```

2. **Check container status**:
   ```bash
   docker compose ps
   ```

3. **Rebuild container**:
   ```bash
   docker compose build --no-cache
   ```

#### UV Issues

1. **Check UV installation**:
   ```bash
   uv --version
   ```

2. **Reinstall dependencies**:
   ```bash
   uv sync --reinstall
   ```

### Log Files

- **MCP Server**: `logs/neozork_mcp.log`
- **IDE Setup**: `logs/ide_setup.log`
- **Setup Summary**: `logs/ide_setup_summary.json`

### Performance Tuning

#### Memory Limits

```json
{
  "performance": {
    "max_files": 15000,
    "max_file_size": "10MB",
    "cache_enabled": true,
    "cache_size": "200MB",
    "memory_limit_mb": 512
  }
}
```

#### Monitoring

```json
{
  "monitoring": {
    "enable_monitoring": true,
    "health_check_interval": 60,
    "max_memory_mb": 512,
    "max_cpu_percent": 80
  }
}
```

## Testing

### Run IDE Configuration Tests

```bash
python3 -m pytest tests/docker/test_ide_configs.py -v
```

### Test Coverage

The IDE configuration system has comprehensive test coverage:

- **Configuration Creation**: Tests for all IDE configs
- **Structure Validation**: JSON schema validation
- **System Detection**: Docker and UV availability
- **Integration Testing**: End-to-end setup testing

### Test Results

```bash
============================================ 15 passed in 0.12s ============================================
```

## Summary

The IDE configuration system provides:

- ✅ **Multi-IDE Support**: Cursor, VS Code, PyCharm
- ✅ **Docker Integration**: Containerized development
- ✅ **UV Package Manager**: Modern Python dependency management
- ✅ **Financial Data**: Real-time data analysis
- ✅ **Technical Indicators**: 20+ indicators
- ✅ **AI Integration**: GitHub Copilot support
- ✅ **Automated Setup**: One-command configuration
- ✅ **Comprehensive Testing**: 100% test coverage
- ✅ **Documentation**: Complete setup guide

For additional support, check the logs or run the setup script with verbose output:

```bash
python3 scripts/setup_ide_configs.py --verbose
``` 