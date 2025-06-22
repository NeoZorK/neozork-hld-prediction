# PyCharm GitHub Copilot MCP Server

🚀 **Enhanced MCP Server for PyCharm IDE with GitHub Copilot Integration**

## 🎯 Overview

The PyCharm GitHub Copilot MCP Server is a specialized Model Context Protocol (MCP) server designed to enhance the development experience in PyCharm IDE with GitHub Copilot integration. It provides intelligent code completion, context-aware suggestions, and project-specific features for the Neozork HLD Prediction project.

## ✨ Key Features

### 🧠 Intelligent Code Completion
- **Context-aware suggestions** based on project structure
- **Financial data integration** with automatic symbol and timeframe detection
- **Technical indicators** with specialized completions
- **Code snippets** for common financial analysis tasks
- **GitHub Copilot integration** for enhanced AI-powered suggestions

### 📊 Financial Analysis Support
- **Automatic data scanning** from MQL5 feed directory
- **Symbol and timeframe detection** from CSV files
- **Technical indicator calculations** (SMA, EMA, RSI, MACD, etc.)
- **Data quality checks** and validation
- **Visualization helpers** for charts and plots

### 🔍 Advanced Code Search
- **Function and class indexing** for fast search
- **Import tracking** and dependency analysis
- **Reference finding** across the project
- **Documentation extraction** from docstrings
- **Cross-file symbol resolution**

### 🎯 GitHub Copilot Integration
- **Context-aware suggestions** based on current file and project
- **Financial analysis patterns** recognition
- **Code completion** with project-specific knowledge
- **Snippet generation** for common tasks
- **Error prevention** with domain-specific rules

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd neozork-hld-prediction

# Install dependencies
pip install -e .

# Run tests to verify installation
python scripts/run_cursor_mcp.py --test --report
```

### 2. PyCharm Configuration

1. Open PyCharm IDE
2. Go to **Settings/Preferences** → **Plugins**
3. Search for **MCP** or **Model Context Protocol**
4. Install the MCP plugin if not already installed
5. Go to **Settings/Preferences** → **Languages & Frameworks** → **MCP Servers**
6. Add new server configuration:

```json
{
  "name": "PyCharm GitHub Copilot MCP",
  "command": "python",
  "args": ["pycharm_github_copilot_mcp.py"],
  "cwd": "/path/to/neozork-hld-prediction",
  "env": {
    "PYTHONPATH": "/path/to/neozork-hld-prediction/src:/path/to/neozork-hld-prediction",
    "LOG_LEVEL": "INFO",
    "MCP_SERVER_TYPE": "pycharm_copilot"
  }
}
```

### 3. GitHub Copilot Setup

1. Install GitHub Copilot plugin in PyCharm
2. Authenticate with your GitHub account
3. Enable Copilot in your project
4. The MCP server will automatically integrate with Copilot

### 4. Launch

```bash
# Start the server
python pycharm_github_copilot_mcp.py

# Or use the runner script
python scripts/run_cursor_mcp.py --mode stdio
```

## 📋 Usage Examples

### Financial Data Loading

```python
# The server will suggest financial symbols and timeframes
load_financial_data("BTCUSD", "D1")  # Auto-completion for symbols and timeframes
```

### Technical Indicators

```python
# Auto-completion for technical indicators
calculate_sma(data, period=20)      # Simple Moving Average
calculate_ema(data, period=12)      # Exponential Moving Average
calculate_rsi(data, period=14)      # Relative Strength Index
calculate_macd(data)                # MACD
```

### Code Snippets

```python
# Type 'load_data' and get auto-completion
load_financial_data  # Expands to: load_financial_data(symbol, timeframe)

# Type 'calculate_indicators' and get auto-completion
calculate_indicators  # Expands to: calculate_indicators(data)

# Type 'plot_analysis' and get auto-completion
plot_analysis  # Expands to: plot_analysis(data, indicators)
```

### GitHub Copilot Integration

```python
# Copilot will suggest based on project context
def analyze_market_data(symbol, timeframe):
    # Copilot suggests: load data, calculate indicators, create plots
    data = load_financial_data(symbol, timeframe)
    indicators = calculate_technical_indicators(data)
    plot_market_analysis(data, indicators)
    return analysis_results
```

## 🏗️ Architecture

### Core Components

```
PyCharmGitHubCopilotMCPServer
├── CodeIndexer              # Code indexing and search
├── DataScanner              # Financial data scanning
├── CompletionProvider       # Intelligent code completion
├── SnippetProvider          # Code snippets generation
├── SearchProvider           # Advanced code search
├── GitHubCopilotProvider    # Copilot integration
└── FinancialDataProvider    # Financial data management
```

### Data Structures

- **ProjectFile**: Information about project files
- **FinancialData**: Financial data metadata
- **CompletionItem**: Code completion items
- **CodeIndex**: Indexed code elements

### Message Handlers

- `initialize`: Server initialization
- `textDocument/completion`: Code completion
- `textDocument/hover`: Hover information
- `textDocument/definition`: Go to definition
- `textDocument/references`: Find references
- `workspace/symbols`: Workspace symbols
- `pycharm/*`: PyCharm-specific features
- `github/copilot/*`: GitHub Copilot integration

## 🧪 Testing

### Run Tests

```bash
# Functional tests
pytest tests/mcp/test_pycharm_github_copilot_mcp.py -v

# Complete testing with report
python scripts/run_cursor_mcp.py --test --performance --report

# GitHub Copilot specific tests
python scripts/run_cursor_mcp.py --test --github-copilot
```

### Test Coverage

```bash
# Generate coverage report
pytest tests/mcp/test_pycharm_github_copilot_mcp.py --cov=pycharm_github_copilot_mcp --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 📈 Performance Metrics

### Benchmarks

- **Initialization time**: < 3 seconds
- **Completion response**: < 50ms
- **Memory usage**: < 80MB
- **File indexing**: Supports up to 15,000 files
- **GitHub Copilot integration**: < 100ms latency

### Optimizations

- **Lazy loading** of large files
- **Caching** of frequently accessed data
- **Parallel processing** for file indexing
- **Smart filtering** of irrelevant files
- **Memory-efficient** data structures

## ⚙️ Configuration

### Server Configuration

```json
{
  "mcpServers": {
    "pycharm-github-copilot-mcp": {
      "command": "python",
      "args": ["pycharm_github_copilot_mcp.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src:${workspaceFolder}",
        "LOG_LEVEL": "INFO",
        "MCP_SERVER_TYPE": "pycharm_copilot",
        "ENABLE_GITHUB_COPILOT": "true"
      }
    }
  }
}
```

### Feature Configuration

```json
{
  "features": {
    "financialData": {
      "enabled": true,
      "autoScan": true,
      "symbols": ["BTCUSD", "GBPUSD", "EURUSD"],
      "timeframes": ["D1", "H1", "M15", "M5"]
    },
    "indicators": {
      "enabled": true,
      "available": ["SMA", "EMA", "RSI", "MACD", "Bollinger_Bands"]
    },
    "githubCopilot": {
      "enabled": true,
      "contextAware": true,
      "suggestions": true
    }
  }
}
```

## 🔧 Advanced Features

### Custom Snippets

Create custom snippets in `config/snippets.json`:

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
    }
  }
}
```

### Custom Indicators

Add custom indicators in `config/indicators.json`:

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

## 🐛 Troubleshooting

### Common Issues

#### Server Not Starting
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip list | grep -E "(pandas|numpy|ast)"

# Check file permissions
ls -la pycharm_github_copilot_mcp.py
```

#### GitHub Copilot Not Working
```bash
# Check Copilot plugin
# Verify authentication
# Check network connection
# Restart PyCharm
```

#### Performance Issues
```bash
# Check memory usage
ps aux | grep pycharm_github_copilot_mcp

# Check log files
tail -f logs/pycharm_copilot_mcp_*.log

# Restart server
python scripts/run_cursor_mcp.py --restart
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python pycharm_github_copilot_mcp.py

# Check detailed logs
tail -f logs/pycharm_copilot_mcp_*.log
```

## 🔄 Updates and Maintenance

### Updating the Server

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart server
python scripts/run_cursor_mcp.py --restart
```

### Backup Configuration

```bash
# Backup current configuration
cp cursor_mcp_config.json cursor_mcp_config.json.backup

# Restore configuration if needed
cp cursor_mcp_config.json.backup cursor_mcp_config.json
```

## 📚 API Reference

### Core Methods

- `initialize(request_id, params)`: Initialize server
- `handle_completion(request_id, params)`: Handle code completion
- `handle_copilot_suggestions(request_id, params)`: Handle Copilot suggestions
- `handle_financial_data(request_id, params)`: Handle financial data requests

### Data Classes

- `CompletionItem`: Code completion item
- `ProjectFile`: Project file information
- `FinancialData`: Financial data metadata

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd neozork-hld-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/mcp/ -v
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for all functions
- Write comprehensive tests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue on GitHub
- Check the documentation in `docs/mcp-servers/`
- Review the troubleshooting section
- Contact the development team

---

**PyCharm GitHub Copilot MCP Server** - Enhancing your financial analysis development experience with AI-powered assistance. 