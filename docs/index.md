# Documentation Index

Complete guide to NeoZork HLD Prediction project with AI-powered development assistance.

## 🚀 Quick Start

- **[Getting Started](getting-started.md)** - Project overview, installation, and quick setup
- **[Usage Examples](usage-examples.md)** - Common commands and use cases

## 🤖 AI-Powered Development

- **[MCP Servers](mcp-servers/README.md)** - Model Context Protocol servers for intelligent development
  - **[Setup Guide](mcp-servers/SETUP.md)** - Detailed configuration and installation
  - **[Usage Guide](mcp-servers/USAGE.md)** - Examples and API documentation
  - **[Changes Summary](mcp-servers/CHANGES_SUMMARY.md)** - Updates and improvements

## 📊 Core Documentation

- **[Docker](docker.md)** - Containerized development
- **[Exchange Rate API](exchange-rate-api-complete.md)** - Real-time forex data integration
- **[Indicator Export](indicator-export.md)** - Export calculated indicators to multiple formats
- **[UV Setup](uv-setup.md)** - Fast package manager

## 🔧 Tools & Analysis

- **[Analysis & EDA](analysis-eda.md)** - Data analysis and exploration tools
- **[Scripts](scripts.md)** - Available scripts and automation
- **[Utility Scripts](utility-scripts.md)** - Data conversion and test file management utilities
- **[Debug Scripts](debug-scripts.md)** - Testing and debugging tools

## 💻 Development

- **[Testing](testing.md)** - Testing framework and validation
- **[CI/CD](ci-cd.md)** - GitHub Actions and local testing
- **[Project Structure](project-structure.md)** - Directory organization

## 📈 MCP Server Features

### PyCharm GitHub Copilot MCP Server
- **Smart Autocompletion:** Financial symbols, timeframes, technical indicators
- **Context-Aware Suggestions:** AI-powered code completion
- **GitHub Copilot Integration:** Enhanced AI assistance

### Auto-Start MCP Server
- **Intelligent Detection:** Automatically detects running IDEs
- **Condition-Based Startup:** Starts servers based on project conditions
- **Health Monitoring:** Continuous monitoring and automatic restart

### Quick MCP Setup
```bash
# Test MCP servers
python scripts/run_cursor_mcp.py --test --report

# Start auto-start server
python scripts/auto_start_mcp.py start

# Manual server start
python pycharm_github_copilot_mcp.py
```

## 📝 Export Flags: Allowed Modes

Export flags (`--export-parquet`, `--export-csv`, `--export-json`) are only available in `demo` mode. They are not allowed in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, or `exrate` modes.

### Example Workflow

1. **Download or Convert Data**
   - Download with yfinance:
     ```bash
     python run_analysis.py yfinance --ticker EURUSD=X --period 1y --point 0.00001
     ```
   - Or convert from CSV:
     ```bash
     python run_analysis.py csv --csv-file mydata.csv --point 0.01
     ```
2. **Apply Indicator and Export**
   - Use show mode with a rule and export flags:
     ```bash
     python run_analysis.py show yfinance EURUSD=X --rule PHLD --export-parquet --export-csv --export-json
     ```
3. **View Exported Indicators**
   - Use show ind to view the exported files:
     ```bash
     python run_analysis.py show ind parquet
     python run_analysis.py show ind csv
     python run_analysis.py show ind json
     ```

> Export flags are not available in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, or `exrate` modes. Use `demo` for direct export, or the above workflow for real data.

## 👥 Navigation by Role

### New Users
1. [Getting Started](getting-started.md)
2. [Usage Examples](usage-examples.md)
3. [MCP Servers](mcp-servers/README.md) - For AI assistance

### Developers
1. [Project Structure](project-structure.md)
2. [Testing](testing.md)
3. [CI/CD](ci-cd.md)
4. [Debug Scripts](debug-scripts.md)
5. [MCP Servers Setup](mcp-servers/SETUP.md) - IDE configuration

### Data Scientists
1. [Exchange Rate API](exchange-rate-api-complete.md)
2. [Analysis & EDA](analysis-eda.md)
3. [Usage Examples](usage-examples.md)
4. [Scripts](scripts.md)
5. [MCP Servers Usage](mcp-servers/USAGE.md) - Advanced examples

### DevOps
1. [Docker](docker.md)
2. [CI/CD](ci-cd.md)
3. [UV Setup](uv-setup.md)
4. [MCP Servers](mcp-servers/README.md) - Server deployment

## 🎯 By Task

**Setup:**
- [Getting Started](getting-started.md) (includes installation)
- [MCP Servers Setup](mcp-servers/SETUP.md) (AI assistance setup)

**Usage:**
- [Usage Examples](usage-examples.md) → [Exchange Rate API](exchange-rate-api-complete.md) → [Analysis & EDA](analysis-eda.md)
- [MCP Servers Usage](mcp-servers/USAGE.md) (AI-powered development)

**Development:**
- [Project Structure](project-structure.md) → [Testing](testing.md) → [CI/CD](ci-cd.md)
- [MCP Servers](mcp-servers/README.md) (AI assistance)

**Deployment:**
- [Docker](docker.md) → [CI/CD](ci-cd.md) → [MCP Servers](mcp-servers/README.md)

## 📊 Performance Metrics

| Feature | Performance |
|---------|-------------|
| MCP Server Startup | < 3s |
| Autocompletion Response | 5-15ms |
| File Indexing | 50ms/file |
| Memory Usage | 25-50MB |
| Test Coverage | 100% |

## 🔧 IDE Integration

### Supported IDEs
- **PyCharm:** MCP plugin with GitHub Copilot integration
- **Cursor:** AI Assistant with MCP server support
- **VS Code:** MCP extension with Copilot enhancement

### Quick IDE Setup
1. Install MCP plugin/extension for your IDE
2. Configure server settings
3. Enable GitHub Copilot (optional)
4. Restart IDE for changes to take effect

## 🐛 Troubleshooting

### MCP Server Issues
- Check server status: `python scripts/run_cursor_mcp.py --test --report`
- Enable debug mode: `export LOG_LEVEL=DEBUG`
- Verify dependencies: `pip list | grep -E "(watchdog|psutil)"`

### General Issues
- Ensure Python 3.12+ is installed
- Check all dependencies: `pip install -e .`
- Verify API keys for live data sources
- Check logs in `logs/` directory