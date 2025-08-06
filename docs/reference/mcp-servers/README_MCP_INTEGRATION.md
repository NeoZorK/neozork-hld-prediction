# Neozork MCP Server - Cursor IDE Integration

## 🚀 Quick Start

### 1. Check Server Status
```bash
uv run python scripts/mcp/check_mcp_status.py
```

### 2. Manual Server Start
```bash
uv run python neozork_mcp_server.py
```

### 3. Cursor IDE Integration

#### Option A: Automatic Setup (Recommended)
```bash
# macOS
cp cursor_mcp_config.json ~/Library/Application\ Support/Cursor/User/globalStorage/

# Windows  
copy cursor_mcp_config.json %APPDATA%\Cursor\User\globalStorage\

# Linux
cp cursor_mcp_config.json ~/.config/Cursor/User/globalStorage/
```

#### Option B: Manual Setup
1. Open Cursor IDE
2. Go to Settings (Cmd/Ctrl + ,)
3. Search for "MCP" or "Model Context Protocol"
4. Add the configuration from `cursor_mcp_config.json`

### 4. Restart Cursor IDE

## 📊 Available Commands

| Command | Description |
|---------|-------------|
| `neozork/status` | Server status and uptime |
| `neozork/health` | Health check with issues |
| `neozork/ping` | Simple ping/pong test |
| `neozork/metrics` | Performance metrics |
| `neozork/diagnostics` | System diagnostics |
| `neozork/version` | Version information |
| `neozork/capabilities` | Server capabilities |
| `neozork/restart` | Restart server |
| `neozork/reload` | Reload project data |

## 🎯 Features

- **Financial Data Integration**: Access to financial symbols, timeframes, and data files
- **Technical Indicators**: Auto-completion for RSI, MACD, EMA, Bollinger Bands, and more
- **Code Snippets**: Pre-built snippets for common financial analysis tasks
- **Project Analysis**: Intelligent suggestions based on project structure
- **AI Integration**: GitHub Copilot-style suggestions for financial code
- **Real-time Monitoring**: Server status, health checks, and performance metrics

## 🔧 Troubleshooting

### Server Won't Start
```bash
# Check Python version
python --version

# Check dependencies
uv pip list

# Check file permissions
ls -la neozork_mcp_server.py
```

### Cursor IDE Not Connecting
```bash
# Check Cursor configuration
cat ~/Library/Application\ Support/Cursor/User/globalStorage/cursor_mcp_config.json

# Restart Cursor IDE
# Check Cursor logs
```

### No Code Completion
```bash
# Check server status
uv run python scripts/mcp/check_mcp_status.py

# Verify project structure
ls -la src/ data/ tests/
```

## 📁 Files

- `neozork_mcp_server.py` - Main MCP server
- `cursor_mcp_config.json` - Cursor IDE configuration
- `scripts/mcp/check_mcp_status.py` - Status checker script
- `docs/guides/cursor-mcp-integration.md` - Detailed documentation

## 🔍 Monitoring

### Check Server Health
```bash
uv run python scripts/mcp/check_mcp_status.py
```

### View Logs
```bash
# Server logs
tail -f logs/neozork_mcp_server.log

# Status check results
cat logs/mcp_status_check.json
```

### Debug Mode
```bash
uv run python neozork_mcp_server.py --debug
```

## 📈 Performance

The server automatically:
- Indexes all Python files in your project
- Scans financial data files
- Provides real-time code completion
- Monitors system resources
- Caches frequently accessed data

## 🔒 Security

- Server runs locally (no network ports)
- No data sent externally
- All financial data remains on your machine
- No API keys or sensitive data transmitted

## 📚 Documentation

For detailed documentation, see:
- `docs/guides/cursor-mcp-integration.md` - Complete integration guide
- `docs/reference/mcp-servers/` - MCP server reference

---

**Note**: This MCP server is specifically designed for financial analysis projects and provides domain-specific assistance for trading, backtesting, and financial data analysis tasks. 