# PyCharm GitHub Copilot MCP Server - Usage Guide

## 🚀 Quick Start

### Direct server launch
```bash
python pycharm_github_copilot_mcp.py
```

**Output:**
```
🚀 Starting PyCharm GitHub Copilot MCP Server...
📁 Project root: /path/to/project
🐍 Python version: 3.12.7
📅 Started at: 2025-06-22 23:22:08
📊 Scanning project files...
🔍 Indexing code...
✅ PyCharm GitHub Copilot MCP Server initialized successfully
📈 Server Statistics:
   - Project files: 281
   - Financial symbols: 2
   - Timeframes: 2
   - Functions indexed: 1143
   - Classes indexed: 129
🔄 Server is ready to accept connections...
💡 Press Ctrl+C to stop the server
🔄 Starting MCP server communication...
```

### Launch via script
```bash
python scripts/run_cursor_mcp.py --mode stdio
```

**Output:**
```
🚀 Starting PyCharm GitHub Copilot MCP Server in stdio mode...
📁 Working directory: .
🐍 Command: python pycharm_github_copilot_mcp.py
✅ PyCharm GitHub Copilot MCP Server started successfully
✅ PyCharm GitHub Copilot MCP Server started in stdio mode
💡 Press Ctrl+C to stop
```

## 🧪 Testing

### Run all tests
```bash
python scripts/run_cursor_mcp.py --test --report
```

**Result:**
```
🧪 Running PyCharm GitHub Copilot MCP Server tests...
✅ Server startup test passed
✅ Basic functionality test passed
✅ Completion tests passed
✅ Performance tests passed
✅ Coverage tests passed
✅ GitHub Copilot tests passed

============================================================
PyCharm GitHub Copilot MCP Server Test Report
============================================================
Total Tests: 6
Passed: 6
Failed: 0
Success Rate: 100.0%
============================================================
```

### Test stdio mode
```bash
python test_stdio.py
```

## 🛑 Stopping the server

### Ctrl+C (KeyboardInterrupt)
```
🛑 Received signal SIGINT
🧹 Cleaning up resources...
✅ PyCharm GitHub Copilot MCP Server stopped
📅 Stopped at: 2025-06-22 23:22:37
```

### Ctrl+D (EOF)
```
📤 Received EOF (Ctrl+D), shutting down...
🧹 Cleaning up resources...
✅ PyCharm GitHub Copilot MCP Server stopped
📅 Stopped at: 2025-06-22 23:22:37
```

## 🔧 Configuration

### Main configuration file
`cursor_mcp_config.json`:
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

## 📊 Monitoring

### Start monitoring
```bash
python scripts/run_cursor_mcp.py --monitor 3600
```

**Output:**
```
📊 Starting server monitoring for 3600 seconds...
📈 Memory: 45.2 MB, CPU: 2.1%
📈 Memory: 45.3 MB, CPU: 1.8%
...
```

## 🛠️ Creating IDE configurations

### Cursor
```bash
python scripts/run_cursor_mcp.py --create-config cursor
```

### VS Code
```bash
python scripts/run_cursor_mcp.py --create-config vscode
```

### PyCharm
```bash
python scripts/run_cursor_mcp.py --create-config pycharm
```

## 📝 Logs

Logs are saved in the `logs/` directory:
- `pycharm_copilot_mcp_YYYYMMDD.log` - server logs
- `pycharm_copilot_mcp_runner_YYYYMMDD.log` - runner logs
- `server_state.json` - server state

## 🔍 Features

### Supported MCP methods:
- `initialize` - server initialization
- `shutdown` - graceful shutdown
- `exit` - forced termination
- `textDocument/completion` - autocompletion
- `textDocument/hover` - hover hints
- `textDocument/definition` - definition search
- `textDocument/references` - reference search
- `workspace/symbols` - workspace symbols
- `workspace/files` - project files
- `pycharm/projectInfo` - project information
- `pycharm/financialData` - financial data
- `pycharm/indicators` - technical indicators
- `pycharm/codeSearch` - code search
- `pycharm/snippets` - code snippets
- `pycharm/analysis` - project analysis
- `github/copilot/suggestions` - GitHub Copilot suggestions
- `github/copilot/context` - GitHub Copilot context

### Autocompletion includes:
- Project functions and classes
- Financial symbols and timeframes
- Technical indicators
- Ready-to-use code snippets
- GitHub Copilot integration

## 🚨 Troubleshooting

### Server won't start
1. Check if `pycharm_github_copilot_mcp.py` file exists
2. Ensure Python 3.7+ is installed
3. Check file permissions

### No responses in stdio mode
1. Ensure all print messages go to stderr
2. Check JSON message format
3. Ensure server doesn't terminate prematurely

### Test issues
1. Run `python scripts/run_cursor_mcp.py --test --report`
2. Check logs in `logs/`
3. Ensure all dependencies are installed

## 📈 Performance Statistics

- **Initialization time**: < 10 seconds
- **Completion response time**: < 1 second
- **Memory usage**: ~45-50 MB
- **CPU usage**: < 5% in idle mode
- **Indexing**: 280+ files, 1143+ functions, 129+ classes 