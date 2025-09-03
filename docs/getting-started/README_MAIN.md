# Neozork HLD Prediction System

A comprehensive financial analysis and prediction system for high-level decision making in financial markets.

## 🚀 Features

- **Advanced Data Processing**: Multi-source data acquisition and intelligent gap fixing
- **Technical Analysis**: Comprehensive suite of technical indicators and pattern recognition
- **Machine Learning**: State-of-the-art ML models for prediction and classification
- **Interactive CLI**: Powerful command-line interface with extensive options
- **Modular Architecture**: Well-structured, extensible codebase with clear separation of concerns
- **Comprehensive Testing**: 100% test coverage with parallel execution support

## 📁 Project Structure

```
neozork-hld-prediction/
├── src/                          # Source code
│   ├── core/                     # Core functionality and interfaces
│   │   ├── base.py              # Base classes and abstract interfaces
│   │   ├── config.py            # Configuration management
│   │   ├── exceptions.py        # Custom exceptions
│   │   └── interfaces.py        # Protocol definitions
│   ├── data/                     # Data handling
│   │   ├── sources/             # Data sources (CSV, API, Database)
│   │   ├── processors/          # Data processing and transformation
│   │   ├── storage/             # Data storage and caching
│   │   ├── validation/          # Data validation
│   │   └── pipeline/            # Data pipelines
│   ├── analysis/                 # Analysis engine
│   │   ├── indicators/          # Technical indicators
│   │   ├── statistics/          # Statistical analysis
│   │   ├── patterns/            # Pattern recognition
│   │   ├── pipeline/            # Analysis pipelines
│   │   └── metrics/             # Performance metrics
│   ├── ml/                      # Machine learning
│   │   ├── models/              # ML model implementations
│   │   ├── features/            # Feature engineering
│   │   ├── training/            # Model training
│   │   ├── evaluation/          # Model evaluation
│   │   └── pipeline/            # ML pipelines
│   ├── cli/                     # Command-line interface
│   │   ├── core/                # Core CLI functionality
│   │   ├── commands/            # Command implementations
│   │   ├── parsers/             # Argument parsing
│   │   └── formatters/          # Output formatting
│   └── utils/                   # Utility functions
│       ├── file_utils.py        # File operations
│       ├── math_utils.py        # Mathematical utilities
│       ├── time_utils.py        # Time handling
│       └── validation.py        # Validation utilities
├── tests/                        # Test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── performance/             # Performance tests
├── scripts/                      # Utility scripts
│   ├── tools/                   # Development tools
│   ├── automation/              # Automation scripts
│   └── maintenance/             # Maintenance utilities
├── docs/                        # Documentation
├── data/                        # Data files
├── logs/                        # Log files
└── results/                     # Output results
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- uv package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/neozork-hld-prediction.git
   cd neozork-hld-prediction
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Verify installation**
   ```bash
   uv run python -c "import src; print('Installation successful!')"
   ```

## 🚀 Usage

### Command Line Interface

The system provides a comprehensive CLI with multiple commands:

```bash
# Get help
neozork --help

# Analyze financial data
neozork analyze --data data.csv --indicators sma,rsi,bb

# Train ML model
neozork train --model random_forest --data train.csv

# Make predictions
neozork predict --model model.joblib --data test.csv

# Data operations
neozork data fetch --source api
neozork data process --input raw.csv --output processed.csv
neozork data validate --data data.csv
neozork data export --data results.json --format csv

# Get detailed help for specific topics
neozork help analysis
neozork help indicators
neozork help ml
```

### Python API

```python
from src.core import config
from src.data.sources import CSVDataSource
from src.analysis.indicators import SMAIndicator
from src.ml.models import RandomForestModel

# Load configuration
cfg = config.config

# Create data source
source = CSVDataSource("price_data", {"file_path": "data.csv"})

# Fetch data
data = source.fetch()

# Calculate indicators
sma = SMAIndicator("sma_20", {"period": 20})
sma_values = sma.calculate(data)

# Train model
model = RandomForestModel("price_predictor")
model.train({"features": features, "targets": targets})

# Make predictions
predictions = model.predict(test_features)
```

## 🧪 Testing

### Run All Tests

```bash
# Run all tests with coverage
uv run tests/run_all_tests.py

# Run specific test types
uv run tests/run_all_tests.py --type unit
uv run tests/run_all_tests.py --type integration
uv run tests/run_all_tests.py --type performance

# Run CLI tests only
uv run tests/run_all_tests.py --cli-only

# Run tests matching pattern
uv run tests/run_all_tests.py --pattern "test_cli"
```

### Test Configuration

- **Parallel Execution**: Tests run in parallel by default for faster execution
- **Coverage Reporting**: HTML and terminal coverage reports
- **Verbose Output**: Use `--verbose` for detailed test output
- **Pattern Matching**: Run specific tests using pattern matching

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Performance Tests**: Test system performance characteristics
- **CLI Tests**: Verify all command-line flags and options work correctly

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **Getting Started**: Quick start guides and tutorials
- **API Reference**: Complete API documentation
- **User Guides**: Step-by-step usage instructions
- **Developer Guide**: Development and contribution guidelines
- **Examples**: Practical examples and use cases

## 🔧 Development

### Code Structure

- **Modular Design**: Each module has a clear responsibility
- **Interface-First**: Abstract interfaces define component contracts
- **Configuration-Driven**: Flexible configuration management
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Logging**: Structured logging throughout the system

### Adding New Features

1. **Create Implementation**: Implement the feature following existing patterns
2. **Add Tests**: Write comprehensive tests with 100% coverage
3. **Update Documentation**: Document the new functionality
4. **Run Tests**: Ensure all tests pass
5. **Submit PR**: Create a pull request with detailed description

### Code Quality

- **Type Hints**: Full type annotation support
- **Docstrings**: Comprehensive documentation strings
- **Linting**: Code quality enforcement
- **Formatting**: Consistent code formatting
- **Testing**: Mandatory test coverage

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development/CONTRIBUTING.md) for details.

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests for new functionality**
5. **Ensure all tests pass**
6. **Submit a pull request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/your-username/neozork-hld-prediction/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/your-username/neozork-hld-prediction/discussions)

## 🏗️ Architecture

### Core Principles

- **Separation of Concerns**: Clear boundaries between components
- **Dependency Injection**: Loose coupling through interfaces
- **Configuration Management**: Centralized configuration handling
- **Error Handling**: Graceful error handling and recovery
- **Extensibility**: Easy to add new features and components

### Component Design

- **Base Classes**: Common functionality in base classes
- **Interfaces**: Protocol-based interfaces for flexibility
- **Factories**: Component creation and management
- **Pipelines**: Configurable processing pipelines
- **Registry**: Component registration and discovery

## 🔮 Roadmap

- [ ] Additional ML algorithms
- [ ] Real-time data streaming
- [ ] Web dashboard interface
- [ ] Advanced backtesting
- [ ] Risk management tools
- [ ] Portfolio optimization
- [ ] API server
- [ ] Docker containerization

## 📊 Performance

- **Parallel Processing**: Multi-threaded execution where possible
- **Memory Management**: Efficient memory usage and garbage collection
- **Caching**: Intelligent caching for frequently accessed data
- **Optimization**: Performance profiling and optimization
- **Scalability**: Designed for both small and large datasets

---

**Neozork HLD Prediction System** - Empowering financial decisions through advanced analytics and machine learning.