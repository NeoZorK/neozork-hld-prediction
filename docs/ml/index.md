# Machine Learning (ML) Documentation

This section provides comprehensive documentation for the NeoZork ML trading platform, including feature engineering, model development, and automated trading strategies.

## 🚀 Overview

The ML module provides comprehensive machine learning capabilities for the NeoZork HLD Prediction trading platform. This module is designed to automatically create profitable and robust trading strategies using your proprietary PHLD and Wave indicators.

## 📚 Documentation Sections

### [ML Module Overview](ml-module-overview.md) ⭐ **NEW**
Complete overview of the ML module architecture, features, and roadmap.

**Covers:**
- Module architecture and components
- Feature engineering system
- ML models and validation
- Risk management and automation
- Development roadmap and status

### [Feature Engineering Guide](feature_engineering_guide.md)
Comprehensive guide for the automated feature engineering system.

**Includes:**
- Feature generation architecture
- Configuration and customization
- Performance optimization
- Testing and validation
- Practical examples and use cases

### [EDA Integration Guide](eda_integration_guide.md) ⭐ **NEW**
Complete guide to using the integrated EDA and Feature Engineering system.

**Includes:**
- Unified EDA + Feature Engineering pipeline
- Interactive system interface
- Configuration and optimization
- Troubleshooting and best practices
- Integration with existing tools

### [System Status Report](../SYSTEM_STATUS_REPORT.md) 📊 **NEW**
Comprehensive status report of the current system state, including:
- Phase 1 completion status
- Performance metrics
- Known issues and solutions
- Next steps for Phase 2

### [ML Documentation Reorganization](../ML_DOCUMENTATION_REORGANIZATION_COMPLETE.md) 📚
Complete overview of the ML documentation restructuring and improvements.

### [Usage Instructions](USAGE_INSTRUCTIONS.md) ⭐ **NEW**
Complete guide for navigating and using ML documentation.

**Includes:**
- Quick navigation paths
- File descriptions and usage
- Common use cases
- Support and troubleshooting

### [Changes Summary](CHANGES_SUMMARY.md) ⭐ **NEW**
User-friendly summary of recent documentation changes.

**Includes:**
- What changed and why
- New structure overview
- Benefits and improvements
- Quick access information

### [API Reference](api-reference.md) 📋 **PLANNED**
Technical API documentation for all ML components.

**Will Include:**
- Class and method documentation
- Configuration options
- Error handling
- Performance benchmarks
- Integration examples

### [Examples and Tutorials](examples/) 📋 **PLANNED**
Practical examples and step-by-step tutorials.

**Will Include:**
- Feature engineering examples
- Model training tutorials
- Backtesting scenarios
- Risk management examples
- Deployment guides

## 🏗️ Architecture

```
ML Module
├── Feature Engineering (COMPLETE ✅)
│   ├── Proprietary Features (PHLD + Wave)
│   ├── Technical Features (50+ indicators)
│   ├── Statistical Features (Math + Stats)
│   ├── Temporal Features (Time patterns)
│   ├── Cross-Timeframe Features (Multi-scale)
│   └── Feature Selector (Optimization)
├── ML Models (IN PROGRESS 🔄)
│   ├── Classification Models
│   ├── Regression Models
│   ├── Deep Learning Models
│   └── Ensemble Models
├── Validation (PLANNED 📋)
│   ├── Walk Forward Analysis
│   ├── Time Series CV
│   └── Performance Metrics
├── Risk Management (PLANNED 📋)
│   ├── Monte Carlo Simulations
│   ├── Backtesting Engine
│   └── Risk Metrics
└── Automation (PLANNED 📋)
    ├── Training Pipeline
    ├── Monitoring System
    └── Deployment Engine
```

## 🚀 Quick Start

### 1. Integrated EDA + Feature Engineering (Recommended)

```bash
# Run complete pipeline
./eda_fe --file data.csv --full-pipeline

# EDA only
./eda_fe --file data.csv --eda-only

# Feature Engineering only
./eda_fe --file data.csv --features-only
```

### 2. Interactive System

```bash
# Start full interactive system
./nz_interactive --full

# Demo mode
./nz_interactive --demo
```

### 3. Direct Scripts

```bash
# Feature Engineering Demo
uv run python scripts/demo_feature_engineering.py

# Integrated Pipeline
python scripts/eda_feature_engineering.py --file data.csv --full-pipeline

# Interactive System
python scripts/interactive_system.py
```

### 4. Basic Usage (Python API)

```python
from src.ml.feature_engineering import FeatureGenerator, MasterFeatureConfig

# Configure system
config = MasterFeatureConfig(
    max_features=150,
    min_importance=0.2,
    enable_proprietary=True,
    enable_technical=True
)

# Generate features
generator = FeatureGenerator(config)
df_features = generator.generate_features(your_ohlcv_data)

print(f"Generated {len(generator.get_feature_summary())} features")
```

## 🧪 Testing

### Run All Tests

```bash
# Run all ML tests with UV (multithreaded)
uv run pytest tests/ml/ -n auto

# Run specific test categories
uv run pytest tests/ml/test_feature_engineering.py -v
```

### Test Coverage

The ML module maintains 100% test coverage:

- ✅ Unit tests for all classes
- ✅ Integration tests for complete pipeline
- ✅ Error handling and edge cases
- ✅ Performance and memory tests
- ✅ Configuration validation tests

## 🔮 Roadmap

### Phase 2: ML Models (Current)
- [ ] XGBoost and LightGBM models
- [ ] LSTM and Transformer models
- [ ] Ensemble and stacking models
- [ ] Model training pipeline

### Phase 3: Validation System
- [ ] Walk Forward Analysis
- [ ] Time series cross-validation
- [ ] Performance metrics
- [ ] Model comparison tools

### Phase 4: Risk Management
- [ ] Monte Carlo simulations
- [ ] Backtesting engine
- [ ] Risk metrics calculation
- [ ] Portfolio optimization

### Phase 5: Automation
- [ ] Automated training pipeline
- [ ] Model monitoring system
- [ ] Performance tracking
- [ ] Alert system

### Phase 6: Deployment
- [ ] AWS deployment
- [ ] MT5 integration
- [ ] Blockchain integration
- [ ] Real-time trading

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone <your-repo>
cd neozork-hld-prediction

# Install dependencies
uv pip install -r requirements.txt

# Run tests
uv run pytest tests/ml/ -n auto

# Run demo
uv run python scripts/demo_feature_engineering.py
```

### Code Standards

- **Python 3.11+** - Modern Python features
- **Type Hints** - Full type annotation
- **Docstrings** - Comprehensive documentation
- **Testing** - 100% test coverage
- **Performance** - Optimized for speed and memory

## 📞 Support

### Getting Help

- **Documentation**: Check the guides and examples
- **Tests**: Run tests to verify functionality
- **Demo**: Use the demo script as reference
- **Issues**: Report bugs and feature requests

### Common Issues

1. **Import Errors** - Ensure all dependencies installed
2. **Memory Issues** - Reduce feature count or enable parallel processing
3. **Slow Performance** - Check data size and configuration
4. **Missing Features** - Verify data has required OHLCV columns

---

**Status**: Phase 1 Complete ✅ | Phase 2 In Progress 🔄 | Phase 3-6 Planned 📋

**Next Milestone**: ML Models and Training Pipeline
