# Neozork HLD Prediction Documentation

Welcome to the comprehensive documentation for the Neozork HLD Prediction project. This documentation is organized into logical categories to help you find the information you need quickly.

## 📚 Documentation Categories

### 🚀 [Getting Started](getting-started/)
Essential documentation for new users to get up and running with the project.
- **Installation & Setup** - Quick installation and basic configuration
- **Project Structure** - Understanding the codebase organization
- **UV Setup** - Setting up UV package manager for dependency management

### 💡 [Examples](examples/)
Comprehensive examples for all project features and use cases.
- **Quick Examples** - Fast start examples for common use cases
- **Usage Examples** - Comprehensive usage examples and workflows
- **Feature-Specific Examples** - Technical indicators, MCP servers, testing, scripts, Docker, EDA
- **Examples Overview** - Complete overview of all available examples

### 📖 [Guides](guides/)
Detailed tutorials and guides for using the project effectively.
- **Core Guides** - Scripts, testing, Docker, analysis & EDA
- **Development Guides** - Debug scripts, utility scripts, Copilot integration
- **Feature Guides** - Indicator export, interactive mode fixes
- **Advanced Guides** - CLI interface, plotting, export functions, analysis tools, workflow utilities

### 📋 [Reference](reference/)
Technical reference documentation for the project.
- **Technical Indicators** - Complete reference for all indicators (trend, oscillators, momentum, volatility, volume, support/resistance, predictive, probability, sentiment)
- **MCP Servers** - Model Context Protocol server documentation
- **Core Calculation** - Core calculation components and mathematical foundations

### 🔧 [Development](development/)
Development and technical documentation for contributors and advanced users.
- **CI/CD Guide** - Continuous Integration and Deployment workflows
- **Development Best Practices** - Code quality and testing strategies

### 🌐 [API](api/)
API and integration documentation for external services and data sources.
- **Exchange Rate API** - Complete API integration guide with authentication, endpoints, and examples
- **Data Sources** - Comprehensive documentation for all data acquisition sources

### 📝 [Meta](meta/)
Documentation about documentation - history, organization, and maintenance.
- **Documentation Updates** - History of documentation changes
- **File Reorganization** - Summary of documentation structure changes

## 🎯 Quick Navigation by User Type

### 👶 **For Beginners**
1. Start with [Getting Started](getting-started/)
2. Try [Quick Examples](examples/quick-examples.md)
3. Review [Examples Overview](examples/examples-overview.md)

### 👨‍💻 **For Developers**
1. Read [Getting Started](getting-started/)
2. Check [Testing Examples](examples/testing-examples.md)
3. Explore [Script Examples](examples/script-examples.md)
4. Review [MCP Examples](examples/mcp-examples.md)
5. Study [Development](development/) guides
6. Master [CLI Interface](guides/cli-interface.md)
7. Understand [Core Calculation](reference/core-calculation.md)

### 📊 **For Analysts**
1. Start with [Getting Started](getting-started/)
2. Use [Indicator Examples](examples/indicator-examples.md)
3. Explore [EDA Examples](examples/eda-examples.md)
4. Review [Reference](reference/) for technical details
5. Master [Analysis Tools](guides/analysis-tools.md)
6. Learn [Plotting and Visualization](guides/plotting-visualization.md)

### 🐳 **For DevOps**
1. Check [Docker Examples](examples/docker-examples.md)
2. Review [Testing Examples](examples/testing-examples.md)
3. Study [Development](development/) CI/CD guides
4. Understand [Workflow and Utilities](guides/workflow-utilities.md)

### 🔍 **For Researchers**
1. Focus on [EDA Examples](examples/eda-examples.md)
2. Review [Indicator Examples](examples/indicator-examples.md)
3. Check [Reference](reference/) for mathematical details
4. Master [Analysis Tools](guides/analysis-tools.md)
5. Learn [Export Functions](guides/export-functions.md)

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd neozork-hld-prediction

# Install dependencies with UV
uv sync

# Run basic example
python -m src.cli.cli_examples --help
```

### Basic Usage
```bash
# Calculate RSI indicator
python -m src.cli.cli_examples --indicator rsi --data data/test_data.csv

# Run EDA analysis
python -m src.eda.basic_stats --data data/test_data.csv

# Export indicators
python -m src.export.csv_export --data data/test_data.csv --indicators rsi,ema
```

## 📊 Project Features

### Technical Indicators
- **Trend Indicators**: EMA, ADX, SAR
- **Oscillators**: RSI, Stochastic, CCI
- **Momentum**: MACD, Stochastic Oscillator
- **Volatility**: ATR, Bollinger Bands, Standard Deviation
- **Volume**: OBV, VWAP
- **Support/Resistance**: Donchian Channels, Fibonacci, Pivot Points
- **Predictive**: HMA, Time Series Forecast
- **Probability**: Kelly Criterion, Monte Carlo
- **Sentiment**: COT, Fear & Greed, Social Sentiment

### Data Sources
- **CSV Files** - Local CSV data files
- **Parquet Files** - High-performance columnar data
- **Binance API** - Real-time cryptocurrency data
- **Exchange Rate API** - Currency exchange rates
- **Yahoo Finance** - Stock and forex data
- **Polygon.io** - Professional market data

### Export Formats
- **CSV** - Comma-separated values
- **JSON** - JavaScript Object Notation
- **Parquet** - Columnar storage format

### Visualization Backends
- **Matplotlib** - Static plots
- **Plotly** - Interactive plots
- **Bokeh** - Web-based interactive plots
- **Seaborn** - Statistical plots
- **MPLFinance** - Financial charts
- **Terminal** - ASCII/Unicode plots

## 🧪 Testing

The project includes comprehensive testing:
- **Unit Tests** - Individual component testing
- **Integration Tests** - End-to-end workflow testing
- **Performance Tests** - Speed and efficiency testing
- **Edge Case Tests** - Boundary condition testing

Run tests with:
```bash
# Run all tests
pytest

# Run specific test category
pytest tests/calculation/indicators/

# Run with coverage
pytest --cov=src
```

## 🔧 Development

### Project Structure
```
neozork-hld-prediction/
├── src/                    # Source code
│   ├── calculation/        # Technical indicators
│   ├── cli/               # Command-line interface
│   ├── data/              # Data acquisition
│   ├── eda/               # Exploratory data analysis
│   ├── export/            # Data export
│   ├── plotting/          # Visualization
│   ├── utils/             # Utility functions
│   └── workflow/          # Workflow management
├── tests/                 # Test suite
├── docs/                  # Documentation
├── data/                  # Data files
├── logs/                  # Log files
└── scripts/               # Utility scripts
```

### Key Components
- **Technical Indicators** - Mathematical calculations for market analysis
- **Data Fetchers** - Data acquisition from various sources
- **CLI Interface** - Command-line tools for analysis
- **Export Modules** - Data export in multiple formats
- **Visualization** - Plotting and charting capabilities
- **Analysis Tools** - EDA and statistical analysis
- **Workflow Engine** - Automated pipeline orchestration
- **Utility Functions** - Common operations and helpers
- **Testing Suite** - Comprehensive test coverage

## 📈 Use Cases

### Financial Analysis
- Technical indicator calculation
- Market trend analysis
- Risk assessment
- Portfolio optimization

### Data Science
- Exploratory data analysis
- Feature engineering
- Model development
- Backtesting strategies

### Research
- Academic research
- Market studies
- Algorithm development
- Performance analysis

### Automation
- Automated data collection
- Scheduled analysis
- Report generation
- Alert systems

## 🤝 Contributing

We welcome contributions! Please see our development guides and testing documentation for details on how to contribute effectively.

## 📞 Support

For questions and support:
1. Check the [Examples](examples/) section for common use cases
2. Review the [Guides](guides/) for detailed tutorials
3. Consult the [Reference](reference/) for technical details
4. Check [Meta](meta/) for recent updates and changes

---

**Last Updated**: See [Documentation Updates](meta/DOCUMENTATION_UPDATES.md) for recent changes.