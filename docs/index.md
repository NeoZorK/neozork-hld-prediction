# Neozork HLD Prediction - Documentation

## Overview

Neozork HLD Prediction is a comprehensive machine learning system for financial market analysis and prediction using proprietary trading indicators. The system provides advanced technical analysis, data processing, and visualization capabilities.

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd neozork-hld-prediction

# Install dependencies using uv
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### Basic Usage

```bash
# Run analysis with demo data
python run_analysis.py demo --rule RSI

# Analyze CSV data
python run_analysis.py csv --csv-file data/sample.csv --point 0.01

# Get data from yfinance
python run_analysis.py yfinance --ticker AAPL --period 1mo --point 0.01
```

## Documentation Sections

### Getting Started
- [Getting Started Guide](getting-started/getting-started.md) - Complete setup and first steps
- [Project Structure](getting-started/project-structure.md) - Understanding the codebase
- [Installation Guide](getting-started/installation.md) - Detailed installation instructions

### Development
- [Development Guide](development/development.md) - Development setup and guidelines
- [Testing Guide](development/testing.md) - **NEW: Comprehensive testing with parallel execution**
- [CLI Interface](development/cli-interface.md) - Command-line interface documentation
- [API Reference](development/api-reference.md) - API documentation

### Analysis Tools
- [Analysis Tools](guides/analysis-tools.md) - Available analysis tools and features
- [EDA Guide](guides/analysis-eda.md) - Exploratory Data Analysis
- [Technical Indicators](guides/technical-indicators.md) - Available indicators

### Reference
- [Core Calculations](reference/core-calculation.md) - Mathematical foundations
- [Trading Rules](reference/trading-rules.md) - Rule descriptions and parameters
- [Advanced Metrics](reference/advanced-metrics.md) - ML and Monte Carlo metrics
- [Indicators](reference/indicators/) - Detailed indicator documentation

### Data Sources
- [Data Sources](api/data-sources.md) - Supported data sources and formats
- [Exchange Rate API](api/exchange-rate-api-complete.md) - Exchange rate data integration

### Deployment
- [Docker Setup](deployment/docker-setup.md) - Containerized deployment
- [CI/CD Pipeline](deployment/ci-cd.md) - Continuous integration and deployment

### Examples
- [Examples Overview](examples/EXAMPLES_SUMMARY.md) - Complete examples collection
- [Docker Examples](examples/docker-examples.md) - Docker usage examples
- [EDA Examples](examples/eda-examples.md) - EDA workflow examples

## Key Features

### 🚀 **NEW: Optimized Testing System**
- **Parallel Test Execution**: Run tests with `pytest-xdist` for faster execution
- **Comprehensive Coverage**: 100% test coverage with organized test structure
- **Performance Monitoring**: Built-in performance tracking and memory monitoring
- **Optimized Test Runner**: Custom test runner with detailed reporting

### 📊 Technical Analysis
- **Multiple Indicators**: RSI, EMA, MACD, Bollinger Bands, and more
- **Custom Calculations**: Proprietary HLD prediction algorithms
- **Real-time Data**: Integration with multiple data sources
- **Visualization**: Advanced plotting and charting capabilities

### 🔧 Development Tools
- **CLI Interface**: Comprehensive command-line interface
- **Data Processing**: Efficient data handling and validation
- **Export Options**: Multiple export formats (CSV, JSON, Parquet)
- **Logging**: Comprehensive logging and debugging

### 🐳 Deployment
- **Docker Support**: Containerized deployment
- **CI/CD Integration**: Automated testing and deployment
- **Environment Management**: Flexible configuration management

## Testing

### Quick Test Run

```bash
# Run all tests with parallel execution
uv run pytest tests -n auto

# Use optimized test runner
python tests/run_optimized_tests.py

# Run specific test categories
python tests/run_optimized_tests.py --categories cli calculation
```

### Test Categories

- **Unit Tests**: Individual function and class testing
- **Integration Tests**: Component interaction testing
- **CLI Tests**: Command-line interface testing
- **Performance Tests**: Performance and stress testing
- **Data Tests**: Data processing and validation testing

For detailed testing information, see [Testing Guide](development/testing.md).

## Project Structure

```
neozork-hld-prediction/
├── src/                          # Source code
│   ├── calculation/              # Technical indicators
│   ├── cli/                      # Command-line interface
│   ├── data/                     # Data processing
│   ├── eda/                      # Exploratory data analysis
│   ├── export/                   # Data export functionality
│   ├── plotting/                 # Visualization tools
│   └── workflow/                 # Workflow management
├── tests/                        # Test suite
│   ├── conftest.py              # Global test configuration
│   ├── run_optimized_tests.py   # Optimized test runner
│   ├── calculation/             # Calculation tests
│   ├── cli/                     # CLI tests
│   └── ...                      # Other test categories
├── docs/                         # Documentation
├── data/                         # Data files
├── scripts/                      # Utility scripts
└── docker/                       # Docker configuration
```

## Contributing

### Development Setup

1. **Fork and clone** the repository
2. **Install dependencies** using `uv sync`
3. **Run tests** to ensure everything works
4. **Create feature branch** for your changes
5. **Write tests** for new functionality
6. **Submit pull request** with comprehensive description

### Testing Requirements

- **100% test coverage** for all new code
- **Parallel test compatibility** for all tests
- **Performance monitoring** for resource-intensive operations
- **Documentation updates** for new features

### Code Quality

- **Type hints** for all functions
- **Docstrings** for all classes and methods
- **Error handling** for all external operations
- **Logging** for debugging and monitoring

## Support

### Getting Help

- **Documentation**: Check the relevant documentation sections
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Testing**: Run tests to verify your setup

### Common Issues

- **Import errors**: Ensure virtual environment is activated
- **Test failures**: Check test requirements and dependencies
- **Performance issues**: Monitor resource usage and optimize
- **Data issues**: Verify data format and source connectivity

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Financial Data Providers**: yfinance, polygon.io, Binance
- **Technical Analysis**: pandas, numpy, scikit-learn
- **Visualization**: matplotlib, plotly, seaborn
- **Testing**: pytest, pytest-xdist
- **Development Tools**: uv, Docker, GitHub Actions