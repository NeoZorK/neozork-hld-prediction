# Complete MCP Servers Guide for Neozork HLD Prediction

🚀 **Comprehensive Guide to Model Context Protocol (MCP) Servers**

## 📋 Table of Contents

1. [What are MCP Servers?](#what-are-mcp-servers)
2. [Why Use MCP Servers?](#why-use-mcp-servers)
3. [Available MCP Servers](#available-mcp-servers)
4. [Installation & Setup](#installation--setup)
5. [Usage Guide](#usage-guide)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Performance & Optimization](#performance--optimization)
9. [Advanced Features](#advanced-features)

## 🤔 What are MCP Servers?

**Model Context Protocol (MCP) Servers** are intelligent language servers that provide enhanced code completion, context-aware suggestions, and project-specific features for IDEs. They act as middleware between your IDE and AI assistants, providing rich context about your project structure, code patterns, and domain-specific knowledge.

### Key Benefits:
- **Intelligent Code Completion** - Context-aware suggestions based on your project
- **Domain-Specific Knowledge** - Financial analysis, technical indicators, data patterns
- **AI Integration** - Enhanced GitHub Copilot and other AI assistants
- **Project Analysis** - Deep understanding of your codebase
- **Performance** - Fast, local processing with minimal latency

## 🎯 Why Use MCP Servers?

### For Financial Analysis Projects:
1. **Domain Expertise** - Built-in knowledge of financial symbols, timeframes, and indicators
2. **Code Patterns** - Recognition of common financial analysis patterns
3. **Data Integration** - Automatic scanning and indexing of financial data
4. **AI Enhancement** - Better AI suggestions with project context
5. **Productivity** - Faster development with intelligent autocompletion

### For Development Teams:
1. **Consistency** - Standardized code patterns across the team
2. **Onboarding** - New developers get immediate context about the project
3. **Quality** - Reduced errors with intelligent suggestions
4. **Documentation** - Automatic extraction and presentation of code documentation
5. **Maintenance** - Easier code navigation and refactoring

## 🚀 Available MCP Servers

### 1. PyCharm GitHub Copilot MCP Server
- **File**: `pycharm_github_copilot_mcp.py`
- **Primary Use**: PyCharm IDE with GitHub Copilot integration
- **Features**: 
  - GitHub Copilot enhancement
  - Advanced financial data analysis
  - Technical indicators with specialized completions
  - Code snippets for common tasks
  - Project-specific context for AI

### 2. Cursor MCP Server
- **File**: `cursor_mcp_server.py`
- **Primary Use**: Cursor IDE optimization
- **Features**:
  - Cursor IDE-specific optimizations
  - Project analysis and statistics
  - Financial data integration
  - Code indexing and search
  - Performance monitoring

## 🔧 Installation & Setup

### Prerequisites

```bash
# Python 3.11+ required
python --version

# Install project dependencies
pip install -e .

# Install additional MCP dependencies
pip install pytest pytest-cov pytest-mock
```

### Quick Installation

```bash
# Clone repository
git clone <repository-url>
cd neozork-hld-prediction

# Install dependencies
pip install -e .

# Verify installation
python scripts/run_cursor_mcp.py --test --report
```

## 🚀 Usage Guide

### Starting MCP Servers

#### Direct Launch
```bash
# PyCharm GitHub Copilot MCP Server
python pycharm_github_copilot_mcp.py

# Cursor MCP Server
python cursor_mcp_server.py
```

#### Using Runner Script
```bash
# Start PyCharm server
python scripts/run_cursor_mcp.py --mode stdio

# Start Cursor server
python scripts/run_cursor_mcp.py --mode stdio --server cursor

# Start with monitoring
python scripts/run_cursor_mcp.py --monitor 3600
```

### IDE Configuration

#### PyCharm Setup

1. **Install MCP Plugin**:
   - Go to Settings → Plugins
   - Search for "MCP" or "Model Context Protocol"
   - Install the plugin

2. **Configure MCP Server**:
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
       "ENABLE_GITHUB_COPILOT": "true"
     }
   }
   ```

#### Cursor Setup

1. **Open Settings**:
   - Press `Cmd/Ctrl + ,`
   - Navigate to AI Assistant settings

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

#### VS Code Setup

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

### Usage Examples

#### Financial Data Analysis

```python
# Auto-completion for financial symbols and timeframes
def analyze_market_data():
    symbol = "BTCUSD"  # Auto-completion available
    timeframe = "D1"   # Auto-completion available
    
    data = load_financial_data(symbol, timeframe)
    indicators = calculate_technical_indicators(data)
    
    return data, indicators
```

#### Technical Indicators

```python
# Auto-completion for technical indicators
def calculate_indicators(data):
    sma_20 = calculate_sma(data, period=20)      # Auto-completion
    ema_50 = calculate_ema(data, period=50)      # Auto-completion
    rsi_14 = calculate_rsi(data, period=14)      # Auto-completion
    macd = calculate_macd(data)                  # Auto-completion
    
    return sma_20, ema_50, rsi_14, macd
```

#### Code Snippets

```python
# Type 'load_data' and get auto-completion
load_financial_data  # Expands to: load_financial_data(symbol, timeframe)

# Type 'calculate_indicators' and get auto-completion
calculate_indicators  # Expands to: calculate_indicators(data)

# Type 'plot_analysis' and get auto-completion
plot_analysis  # Expands to: plot_analysis(data, indicators)
```

#### GitHub Copilot Integration

```python
# Copilot will suggest based on project context
def create_trading_strategy():
    """
    Create a complete trading strategy
    Copilot suggests: data loading, indicator calculation, signal generation
    """
    data = load_financial_data("BTCUSD", "D1")
    indicators = calculate_technical_indicators(data)
    signals = generate_trading_signals(data, indicators)
    results = backtest_strategy(data, signals)
    
    return results
```

## 🧪 Testing

### Run All Tests

```bash
# Run MCP server tests
pytest tests/mcp/ -v

# Run specific server tests
pytest tests/mcp/test_pycharm_github_copilot_mcp.py -v
pytest tests/mcp/test_cursor_mcp_server.py -v

# Run with coverage
pytest tests/mcp/ --cov=pycharm_github_copilot_mcp --cov=cursor_mcp_server --cov-report=html
```

### Using Runner Script

```bash
# Run all tests with report
python scripts/run_cursor_mcp.py --test --report

# Run performance tests
python scripts/run_cursor_mcp.py --test --performance --report

# Run specific test categories
python scripts/run_cursor_mcp.py --test --github-copilot
```

### Test stdio Mode

```bash
# Test stdio communication
python scripts/test_stdio.py
```

### Performance Testing

```bash
# Memory usage test
python -c "
import psutil
from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer

process = psutil.Process()
initial_memory = process.memory_info().rss / 1024 / 1024

server = PyCharmGitHubCopilotMCPServer()

final_memory = process.memory_info().rss / 1024 / 1024
print(f'Memory usage: {final_memory - initial_memory:.2f} MB')
"
```

### Integration Testing

```bash
# Test server communication
python -c "
import json
import subprocess
import time

server_process = subprocess.Popen(
    ['python', 'pycharm_github_copilot_mcp.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

time.sleep(2)

init_request = {
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'initialize',
    'params': {'processId': 12345, 'rootUri': 'file:///test', 'capabilities': {}}
}

server_process.stdin.write(json.dumps(init_request) + '\\n')
server_process.stdin.flush()

response = server_process.stdout.readline()
print('Server response:', response)

server_process.terminate()
server_process.wait()
"
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
ls -la cursor_mcp_server.py
```

#### No Completions
1. Verify server is running
2. Check log files for errors
3. Ensure project files are accessible
4. Verify IDE MCP configuration

#### Performance Issues
```bash
# Check memory usage
ps aux | grep pycharm_github_copilot_mcp
ps aux | grep cursor_mcp_server

# Check log files
tail -f logs/pycharm_copilot_mcp_*.log
tail -f logs/cursor_mcp_*.log

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

### Error Messages

| Error | Solution |
|-------|----------|
| "Server file not found" | Check file paths and permissions |
| "Invalid JSON response" | Verify MCP protocol implementation |
| "No completions" | Check server initialization and indexing |
| "Memory error" | Restart server or increase system memory |
| "Timeout" | Check server responsiveness and network |

## 📈 Performance & Optimization

### Benchmarks

| Operation | PyCharm Server | Cursor Server |
|-----------|----------------|---------------|
| Server Startup | < 3s | < 2s |
| File Indexing | 50ms/file | 30ms/file |
| Completion | 5-15ms | 3-10ms |
| Code Search | 10-30ms | 8-25ms |
| Memory Usage | 25-50MB | 20-40MB |

### Optimization Tips

1. **Exclude unnecessary directories** in configuration
2. **Use caching** for frequently accessed data
3. **Limit file size** for large projects
4. **Monitor memory usage** regularly
5. **Restart server** if performance degrades
6. **Use SSD storage** for faster file access
7. **Optimize Python imports** in server code

### Configuration Optimization

```json
{
  "performance": {
    "maxFiles": 10000,
    "maxFileSize": "10MB",
    "cacheEnabled": true,
    "cacheSize": "100MB",
    "indexingTimeout": 30,
    "excludePatterns": [
      "**/__pycache__/**",
      "**/.git/**",
      "**/node_modules/**",
      "**/*.log"
    ]
  }
}
```

## 🔍 Advanced Features

### Custom Completions

You can extend the MCP servers with custom completions:

```python
# Add custom completion items
def get_custom_completions(self):
    return [
        CompletionItem(
            label="my_custom_function",
            kind=CompletionItemKind.FUNCTION,
            detail="Custom function for my project",
            documentation="This is a custom function I added",
            insert_text="my_custom_function()"
        )
    ]
```

### Project-Specific Configuration

```json
{
  "projectSpecific": {
    "financialData": {
      "autoScan": true,
      "scanInterval": 300000,
      "supportedFormats": ["csv", "parquet"],
      "defaultSymbols": ["BTCUSD", "GBPUSD", "EURUSD"],
      "defaultTimeframes": ["D1", "H1", "M15"]
    },
    "indicators": {
      "autoIndex": true,
      "categories": [
        "momentum",
        "trend",
        "volatility",
        "volume",
        "oscillators"
      ]
    }
  }
}
```

### Monitoring and Metrics

```bash
# Monitor server performance
python scripts/run_cursor_mcp.py --monitor 3600

# Check server health
curl -X POST http://localhost:8080/health

# View performance metrics
python -c "
from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer
import time

start_time = time.time()
server = PyCharmGitHubCopilotMCPServer()
init_time = time.time() - start_time

print(f'Initialization time: {init_time:.2f}s')
print(f'Files indexed: {len(server.project_files)}')
print(f'Functions found: {len(server.code_index[\"functions\"])}')
"
```

## 🔄 CI/CD Integration

### GitHub Actions

The project includes comprehensive CI/CD workflows:

```yaml
name: MCP Servers CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e .
        pip install pytest pytest-cov pytest-mock
    
    - name: Run tests
      run: |
        python scripts/run_cursor_mcp.py --test --report
    
    - name: Generate coverage report
      run: |
        pytest tests/mcp/ --cov=pycharm_github_copilot_mcp --cov=cursor_mcp_server --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Local Development

```bash
# Run CI checks locally
python scripts/run_cursor_mcp.py --test --performance --report

# Check code quality
black --check pycharm_github_copilot_mcp.py cursor_mcp_server.py
flake8 pycharm_github_copilot_mcp.py cursor_mcp_server.py
mypy pycharm_github_copilot_mcp.py cursor_mcp_server.py

# Security checks
bandit -r .
safety check
```

## 📚 Additional Resources

### Documentation Files

- [pycharm-github-copilot-mcp.md](pycharm-github-copilot-mcp.md) - Detailed PyCharm MCP server documentation
- [README_CURSOR_MCP.md](README_CURSOR_MCP.md) - Cursor MCP server documentation
- [examples.md](examples.md) - Comprehensive usage examples
- [auto-start-guide.md](auto-start-guide.md) - Automatic startup guide
- [MCP_SERVERS_MIGRATION_SUMMARY.md](MCP_SERVERS_MIGRATION_SUMMARY.md) - Migration and changes summary

### External Resources

- [MCP Protocol Specification](https://microsoft.github.io/language-server-protocol/)
- [PyCharm Plugin Development](https://plugins.jetbrains.com/docs/intellij/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Cursor IDE Documentation](https://cursor.sh/docs)
- [VS Code MCP Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.mcp)

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
- Update documentation

### Testing Guidelines

- Write unit tests for all new features
- Include integration tests for server communication
- Test performance impact of changes
- Verify backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## 🆘 Support

For support and questions:

- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation files
- Contact the development team

---

**MCP Servers** - Enhancing your financial analysis development experience with intelligent code assistance and AI integration. 🚀 