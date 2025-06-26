# NeoZork HLD Prediction - Complete Documentation

## 🚀 Quick Start

### Installation & Setup
- **[Getting Started](getting-started/getting-started.md)** - Installation and initial setup
- **[Project Structure](getting-started/project-structure.md)** - Understanding the codebase
- **[UV Setup](getting-started/uv-setup.md)** - Modern Python dependency management

### MCP Server Setup
- **[IDE Configuration](guides/ide-configuration.md)** - Multi-IDE MCP server setup
- **[MCP Servers Reference](reference/mcp-servers/README.md)** - Complete server documentation
- **[Detection Logic](development/mcp-server-detection.md)** - Environment detection implementation

## 📚 Documentation Categories

### 🎯 [Getting Started](getting-started/)
Essential guides for new users and developers.

- **[Installation & Setup](getting-started/getting-started.md)** - Complete installation guide
- **[Project Structure](getting-started/project-structure.md)** - Codebase organization
- **[UV Setup](getting-started/uv-setup.md)** - Modern Python package management

### 🤖 [MCP Servers & AI Integration](reference/mcp-servers/)
Model Context Protocol servers for intelligent development assistance.

- **[MCP Servers Reference](reference/mcp-servers/README.md)** - Complete server documentation
- **[IDE Configuration](guides/ide-configuration.md)** - Multi-IDE setup guide
- **[Detection Logic](development/mcp-server-detection.md)** - Environment detection implementation

#### Key Features
- **Multi-IDE Support**: Cursor, VS Code, PyCharm
- **Docker Integration**: Containerized development with ping-based detection
- **Environment Detection**: Automatic Docker vs host environment detection
- **GitHub Copilot**: Enhanced AI assistance for financial analysis
- **Real-time Monitoring**: Health checks and performance metrics

#### Quick Commands
```bash
# Setup all IDE configurations
python3 scripts/setup_ide_configs.py

# Check MCP server status
python scripts/check_mcp_status.py

# Test MCP connection
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

### 💡 [Examples](examples/)
Practical examples and use cases.

- **[Quick Examples](examples/quick-examples.md)** - Fast start examples
- **[Usage Examples](examples/usage-examples.md)** - Comprehensive workflows
- **[Indicator Examples](examples/indicator-examples.md)** - Technical analysis
- **[MCP Examples](examples/mcp-examples.md)** - AI integration examples
- **[Testing Examples](examples/testing-examples.md)** - Test coverage examples
- **[Script Examples](examples/script-examples.md)** - Utilities and debugging
- **[Docker Examples](examples/docker-examples.md)** - Containerized deployment
- **[EDA Examples](examples/eda-examples.md)** - Data analysis examples

### 📖 [Guides](guides/)
Step-by-step guides for specific tasks.

- **[IDE Configuration](guides/ide-configuration.md)** - Multi-IDE MCP setup
- **[Scripts Guide](guides/scripts.md)** - Automation tools
- **[Testing Guide](guides/testing.md)** - Test framework
- **[Docker Guide](guides/docker.md)** - Containerized development
- **[Analysis & EDA Guide](guides/analysis-eda.md)** - Data analysis tools
- **[Debug Scripts](guides/debug-scripts.md)** - Troubleshooting
- **[Utility Scripts](guides/utility-scripts.md)** - Data conversion utilities
- **[Indicator Export](guides/indicator-export.md)** - Export calculated indicators
- **[Copilot Instructions](guides/copilot-instructions.md)** - AI assistance setup

### 📋 [Reference](reference/)
Technical reference documentation.

#### [Technical Indicators](reference/indicators/)
Complete reference for all technical indicators.

- **[Momentum Indicators](reference/indicators/momentum/)** - MACD, Stochastic Oscillator
- **[Oscillators](reference/indicators/oscillators/)** - RSI, CCI, Stochastic
- **[Trend Indicators](reference/indicators/trend/)** - EMA, ADX, SAR
- **[Volatility Indicators](reference/indicators/volatility/)** - ATR, Bollinger Bands
- **[Volume Indicators](reference/indicators/volume/)** - OBV, VWAP
- **[Support & Resistance](reference/indicators/support-resistance/)** - Pivot Points, Fibonacci
- **[Predictive Indicators](reference/indicators/predictive/)** - HMA, Time Series Forecast
- **[Probability Indicators](reference/indicators/probability/)** - Monte Carlo, Kelly Criterion
- **[Sentiment Indicators](reference/indicators/sentiment/)** - Fear & Greed, COT

#### [MCP Servers](reference/mcp-servers/)
Server documentation and configuration.

- **[MCP Servers Reference](reference/mcp-servers/README.md)** - Complete server documentation
- **[Server Architecture](reference/mcp-servers/README.md#server-architecture)** - Technical details
- **[Detection Methods](reference/mcp-servers/README.md#detection-methods)** - Environment detection
- **[Configuration](reference/mcp-servers/README.md#configuration)** - Setup and configuration

### 🔧 [Development](development/)
Development and contribution guidelines.

- **[CI/CD Guide](development/ci-cd.md)** - GitHub Actions and deployment
- **[MCP Server Detection](development/mcp-server-detection.md)** - Detection logic implementation
- **[Detection Changes](development/MCP_DETECTION_CHANGES.md)** - Migration notes

### 🌐 [API](api/)
External API documentation.

- **[Exchange Rate API](api/exchange-rate-api-complete.md)** - Real-time FX data
- **[Data Sources](api/data-sources.md)** - Available data providers

## 🐳 Docker & Deployment

### Containerized Development
- **[Docker Setup](deployment/docker-setup.md)** - Containerized development environment
- **[Docker Examples](examples/docker-examples.md)** - Docker usage examples
- **[Docker Guide](guides/docker.md)** - Docker development guide

### Key Docker Features
- **MCP Server Integration**: Ping-based detection for on-demand servers
- **Environment Detection**: Automatic Docker vs host environment detection
- **Configuration Management**: `docker.env` file for environment variables
- **Multi-stage Builds**: Optimized container images

## 🧪 Testing

### Test Framework
```bash
# Run all tests
pytest tests/ -v

# Test MCP servers specifically
pytest tests/mcp/ -v

# Test IDE configurations
pytest tests/docker/test_ide_configs.py -v

# Test MCP server detection
pytest tests/scripts/test_check_mcp_status.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end functionality
- **Environment Tests**: Docker vs host detection
- **MCP Tests**: Server functionality and detection
- **IDE Tests**: Configuration validation

## 📊 Quick Navigation by User Type

### 👶 **For Beginners**
1. [Getting Started](getting-started/getting-started.md)
2. [Quick Examples](examples/quick-examples.md)
3. [Project Structure](getting-started/project-structure.md)

### 👨‍💻 **For Developers**
1. [Getting Started](getting-started/getting-started.md)
2. [IDE Configuration](guides/ide-configuration.md) - Setup MCP for your IDE
3. [MCP Servers Reference](reference/mcp-servers/README.md) - Server documentation
4. [Testing Examples](examples/testing-examples.md)
5. [Script Examples](examples/script-examples.md)
6. [Development](development/) guides

### 📊 **For Analysts**
1. [Getting Started](getting-started/getting-started.md)
2. [Indicator Examples](examples/indicator-examples.md)
3. [EDA Examples](examples/eda-examples.md)
4. [Technical Indicators](reference/indicators/) reference

### 🐳 **For DevOps**
1. [Docker Examples](examples/docker-examples.md)
2. [Docker Setup](deployment/docker-setup.md)
3. [Testing Examples](examples/testing-examples.md)
4. [Development](development/) CI/CD guides

## 🔄 Recent Updates

### MCP Server Detection (Latest)
- **Ping-based Detection**: Reliable server detection in Docker environments
- **Environment Detection**: Automatic Docker vs host environment detection
- **Docker Integration**: Containerized development with on-demand servers
- **Status Monitoring**: Comprehensive server status checking

### Key Improvements
- ✅ Always accurate detection
- ✅ Works with on-demand servers
- ✅ Tests actual functionality
- ✅ No false positives/negatives
- ✅ Automatic environment detection

## 📚 Additional Resources

- **[GitHub Repository](https://github.com/username/neozork-hld-prediction)** - Source code
- **[Issues](https://github.com/username/neozork-hld-prediction/issues)** - Bug reports and feature requests
- **[Discussions](https://github.com/username/neozork-hld-prediction/discussions)** - Community discussions