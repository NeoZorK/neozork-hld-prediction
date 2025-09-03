# Neozork HLD Prediction System

A comprehensive financial analysis and machine learning system for high-level data (HLD) prediction with advanced technical indicators, interactive visualization, and automated workflows.

## 🚀 Quick Start

- **[Installation Guide](docs/getting-started/INSTALLATION_GUIDE.md)** - Complete setup instructions
- **[Quick Start Guide](docs/getting-started/getting-started.md)** - Get up and running in minutes
- **[Project Structure](docs/getting-started/project-structure.md)** - Understand the codebase organization

## 📚 Documentation

### Core Guides
- **[Architecture Guide](docs/architecture/ARCHITECTURE_GUIDE.md)** - System design and architecture
- **[Development Guide](docs/development/DEVELOPMENT_GUIDE.md)** - Development workflow and standards
- **[CLI Guide](docs/cli/CLI_GUIDE.md)** - Command-line interface usage
- **[Testing Guide](docs/testing/TESTING_GUIDE.md)** - Testing strategies and procedures

### Reference Documentation
- **[API Reference](docs/reference/API_REFERENCE.md)** - Complete API documentation
- **[Configuration Guide](docs/reference/CONFIGURATION.md)** - System configuration options
- **[Deployment Guide](docs/deployment/DEPLOYMENT.md)** - Deployment and containerization

### User Guides
- **[Usage Guide](docs/guides/USAGE_GUIDE.md)** - Comprehensive usage instructions
- **[Interactive Mode](docs/interactive/)** - Interactive analysis features
- **[ML Models](docs/ml/)** - Machine learning capabilities

### Project Information
- **[Documentation Index](docs/meta/DOCUMENTATION_INDEX.md)** - Complete documentation overview
- **[Refactoring Summary](docs/refactoring/REFACTORING_SUMMARY.md)** - Recent refactoring changes

## 🛠️ Features

- **Multi-timeframe Analysis** - Support for M1, M5, H1, D1, W1 timeframes
- **Technical Indicators** - 50+ built-in indicators (SMA, RSI, MACD, Bollinger Bands, etc.)
- **Interactive Visualization** - Multiple plotting modes with real-time updates
- **Machine Learning** - Automated model training and prediction pipelines
- **Data Processing** - Automated data cleaning, gap fixing, and validation
- **Container Support** - Docker and native container deployment options
- **MCP Integration** - Model Context Protocol server for AI assistants

## 🔧 Installation

```bash
# Clone the repository
git clone <repository-url>
cd neozork-hld-prediction

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -r requirements.txt
```

## 📖 Usage Examples

```bash
# Run interactive analysis
python interactive_system.py

# Use CLI for analysis
neozork analyze --data data.csv --indicators sma,rsi

# Train ML model
neozork train --model random_forest --data features.csv --target price
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/ -n auto

# Run specific test categories
uv run pytest tests/unit/ -n auto
uv run pytest tests/integration/ -n auto
```

## 📁 Project Structure

```
neozork-hld-prediction/
├── src/                    # Source code
│   ├── analysis/          # Analysis engines
│   ├── calculation/       # Technical indicators
│   ├── cli/              # Command-line interface
│   ├── data/             # Data processing
│   ├── ml/               # Machine learning
│   └── plotting/         # Visualization
├── tests/                 # Test suite
├── docs/                  # Documentation
├── data/                  # Data files
├── scripts/               # Utility scripts
└── config.json           # Configuration
```

## 🤝 Contributing

Please read our [Development Guide](docs/development/DEVELOPMENT_GUIDE.md) for contribution guidelines and development standards.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

For detailed information, visit our [Documentation Index](docs/meta/DOCUMENTATION_INDEX.md) or start with the [Getting Started Guide](docs/getting-started/getting-started.md).
