# MCP Servers Setup Guide

🔧 **Detailed Setup and Configuration of MCP Servers**

## 📋 Requirements

### System Requirements
- Python 3.11+
- 4GB RAM (recommended)
- 1GB free disk space

### Dependencies
```bash
# Core dependencies
pip install -e .

# Additional MCP dependencies
pip install watchdog==4.0.0 psutil pytest pytest-cov pytest-mock
```

## 🚀 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd neozork-hld-prediction
```

### 2. Install Dependencies
```bash
# Install project
pip install -e .

# Verify installation
python scripts/run_cursor_mcp.py --test --report
```

### 3. Create Directories
```bash
# Create log directories
mkdir -p logs
mkdir -p data/cache
```

## 🔧 IDE Configuration

### PyCharm Setup

1. **Install MCP Plugin**:
   - Settings → Plugins
   - Search for "MCP" or "Model Context Protocol"
   - Install the plugin

2. **Configure MCP Server**:
   - Settings → Languages & Frameworks → MCP Servers
   - Add new server:

```json
{
  "name": "PyCharm GitHub Copilot MCP",
  "command": "python",
  "args": ["pycharm_github_copilot_mcp.py"],
  "cwd": "/path/to/neozork-hld-prediction",
  "env": {
    "PYTHONPATH": "/path/to/neozork-hld-prediction/src:/path/to/neozork-hld-prediction",
    "LOG_LEVEL": "INFO",
    "MCP_SERVER_TYPE": "pycharm_copilot",
    "ENABLE_GITHUB_COPILOT": "true",
    "ENABLE_FINANCIAL_DATA": "true",
    "ENABLE_INDICATORS": "true"
  }
}
```

3. **Configure GitHub Copilot**:
   - Settings → Tools → GitHub Copilot
   - Activate with GitHub account
   - Enable in project

### Cursor Setup

1. **Open Settings**:
   - `Cmd/Ctrl + ,`
   - AI Assistant section

2. **Add MCP Server**:
```json
{
  "mcpServers": {
    "neozork-cursor-mcp": {
      "command": "python",
      "args": ["cursor_mcp_server.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src:${workspaceFolder}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### VS Code Setup

1. **Install Extensions**:
   - MCP Extension
   - Python Extension
   - GitHub Copilot (optional)

2. **Configure settings.json**:
```json
{
  "mcp.servers": {
    "neozork-mcp": {
      "command": "python",
      "args": ["pycharm_github_copilot_mcp.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src:${workspaceFolder}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## ⚙️ Server Configuration

### PyCharm GitHub Copilot MCP Server

#### Basic Configuration
```json
{
  "server": {
    "name": "PyCharm GitHub Copilot MCP Server",
    "command": "python",
    "args": ["pycharm_github_copilot_mcp.py"],
    "env": {
      "PYTHONPATH": ".",
      "LOG_LEVEL": "INFO",
      "MCP_SERVER_TYPE": "pycharm_copilot",
      "ENABLE_FINANCIAL_DATA": "true",
      "ENABLE_INDICATORS": "true",
      "ENABLE_GITHUB_COPILOT": "true"
    },
    "cwd": ".",
    "transport": "stdio"
  }
}
```

#### Advanced Configuration
```json
{
  "features": {
    "financialData": {
      "enabled": true,
      "autoScan": true,
      "symbols": ["BTCUSD", "GBPUSD", "EURUSD", "USDJPY"],
      "timeframes": ["D1", "H1", "M15", "M5", "M1"],
      "scanInterval": 300000
    },
    "indicators": {
      "enabled": true,
      "available": [
        "SMA", "EMA", "RSI", "MACD", "Bollinger_Bands",
        "ATR", "Stochastic", "CCI", "ADX"
      ]
    },
    "githubCopilot": {
      "enabled": true,
      "contextAware": true,
      "suggestions": true,
      "snippets": true
    }
  },
  "performance": {
    "maxFiles": 15000,
    "maxFileSize": "10MB",
    "cacheEnabled": true,
    "cacheSize": "200MB",
    "indexingTimeout": 60
  }
}
```

### Auto-Start MCP Server

#### Auto-start Configuration
```json
{
  "auto_start": {
    "enabled": true,
    "check_interval": 30,
    "ide_detection": true,
    "project_detection": true,
    "restart_delay": 5
  },
  "servers": {
    "pycharm": {
      "enabled": true,
      "command": "python",
      "args": ["pycharm_github_copilot_mcp.py"],
      "conditions": ["pycharm_ide", "python_files"],
      "env": {
        "PYTHONPATH": "${PROJECT_ROOT}",
        "LOG_LEVEL": "INFO"
      }
    },
    "cursor": {
      "enabled": true,
      "command": "python",
      "args": ["cursor_mcp_server.py"],
      "conditions": ["cursor_ide", "python_files"],
      "env": {
        "PYTHONPATH": "${PROJECT_ROOT}",
        "LOG_LEVEL": "INFO"
      }
    }
  },
  "conditions": {
    "pycharm_ide": {
      "processes": ["pycharm", "PyCharm"],
      "files": [".idea", "pycharm_mcp_config.json"]
    },
    "cursor_ide": {
      "processes": ["Cursor", "cursor"],
      "files": [".cursor", "cursor_mcp_config.json"]
    },
    "python_files": {
      "extensions": [".py"],
      "min_files": 1
    }
  },
  "monitoring": {
    "max_memory_mb": 512,
    "max_cpu_percent": 80,
    "health_check_interval": 60
  }
}
```

## 🔍 Environment Variables

### Core Variables
```bash
# Logging level
export LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# MCP server type
export MCP_SERVER_TYPE=pycharm_copilot

# Enable features
export ENABLE_GITHUB_COPILOT=true
export ENABLE_FINANCIAL_DATA=true
export ENABLE_INDICATORS=true

# Paths
export PYTHONPATH=/path/to/project/src:/path/to/project
export PROJECT_ROOT=/path/to/project
```

### Performance Variables
```bash
# Timeouts
export MCP_TIMEOUT=30
export MCP_MAX_REQUESTS=100

# Caching
export MCP_CACHE_ENABLED=true
export MCP_CACHE_SIZE=200MB

# Indexing
export MCP_MAX_FILES=15000
export MCP_MAX_FILE_SIZE=10MB
```

## 🧪 Configuration Testing

### Installation Verification
```bash
# Basic testing
python scripts/run_cursor_mcp.py --test --report

# Performance testing
python scripts/run_cursor_mcp.py --test --performance --report

# GitHub Copilot testing
python scripts/run_cursor_mcp.py --test --github-copilot
```

### Server Testing
```bash
# PyCharm server test
pytest tests/mcp/test_pycharm_github_copilot_mcp.py -v

# Auto-Start server test
pytest tests/mcp/test_auto_start_mcp.py -v

# Complete testing
pytest tests/mcp/ -v --cov=pycharm_github_copilot_mcp --cov=scripts.auto_start_mcp
```

### Stdio Mode Testing
```bash
# Stdio communication test
python tests/test_stdio.py

# Manual server test
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | python pycharm_github_copilot_mcp.py
```

## 🔧 Advanced Configuration

### Custom Snippets
```json
{
  "snippets": {
    "backtest_strategy": {
      "prefix": "backtest",
      "body": [
        "def backtest_strategy(data, strategy_params):",
        "    results = {}",
        "    # Strategy implementation",
        "    return results"
      ],
      "description": "Backtest trading strategy"
    },
    "ml_pipeline": {
      "prefix": "ml_pipeline",
      "body": [
        "def create_ml_pipeline():",
        "    data = load_financial_data(symbol, timeframe)",
        "    features = engineer_features(data)",
        "    model = train_model(features, target)",
        "    return model"
      ],
      "description": "Complete ML pipeline"
    }
  }
}
```

### Custom Indicators
```json
{
  "indicators": {
    "custom_rsi": {
      "name": "Custom RSI",
      "function": "calculate_custom_rsi",
      "parameters": ["data", "period", "smoothing"],
      "description": "Custom RSI implementation"
    }
  }
}
```

### Monitoring and Logging
```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/mcp_server.log",
    "maxSize": "10MB",
    "maxFiles": 5,
    "format": "[%(asctime)s] %(levelname)s [%(name)s] %(message)s"
  },
  "monitoring": {
    "enabled": true,
    "metrics": ["memory", "cpu", "response_time"],
    "alerts": {
      "memory_threshold": 80,
      "cpu_threshold": 90,
      "response_time_threshold": 1000
    }
  }
}
```

## 🐛 Troubleshooting

### Installation Issues
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip list | grep -E "(pandas|numpy|watchdog|psutil)"

# Reinstall dependencies
pip install --force-reinstall -e .
```

### Configuration Issues
```bash
# Check configuration files
python -c "import json; json.load(open('cursor_mcp_config.json'))"

# Validate paths
python scripts/run_cursor_mcp.py --validate-config

# Test configuration
python scripts/run_cursor_mcp.py --test-config
```

### Performance Issues
```bash
# Monitor resources
python scripts/run_cursor_mcp.py --monitor 3600

# Check memory usage
ps aux | grep pycharm_github_copilot_mcp

# Clear cache
python scripts/run_cursor_mcp.py --clear-cache
```

## 📚 Additional Resources

- [README.md](README.md) - Main documentation
- [USAGE.md](USAGE.md) - Usage examples
- [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) - Change history

---

**Setup Guide** - Complete MCP server setup for optimal performance 