# AutoGluon Integration for NeoZork HLDP

## 🎯 Overview

This module provides a comprehensive AutoGluon integration for the NeoZork HLDP project, implementing an AutoGluon-first approach with minimal wrapper code and maximum automation.

## 🚀 Key Features

### AutoGluon-First Philosophy
- ✅ **Maximum AutoGluon utilization** - AutoGluon handles 90% of the work
- ✅ **Minimal wrapper code** - Only coordination and configuration
- ✅ **Automatic everything** - Data cleaning, feature engineering, model selection
- ✅ **Universal data support** - Parquet, CSV, JSON from any `data/` folder

### Core Capabilities
- 🔄 **Universal data loading** - Support for all formats in `data/` folder
- 🎯 **Automatic feature engineering** - 200-300 features generated automatically
- 📊 **Time series split** - Proper 3-way chronological split
- 🧪 **100% pytest coverage** - Comprehensive testing with multi-threading
- 📈 **Value scores analysis** - Profit factor, Sharpe ratio, drawdown
- 🔍 **Drift monitoring** - PSI, feature drift detection
- 🚀 **Walk forward/Monte Carlo ready** - Export models for validation

## 📁 Project Structure

```
src/automl/gluon/
├── gluon.py                    # Main wrapper (≤200 lines)
├── config/                    # Configuration files
│   ├── gluon_config.yaml       # AutoGluon settings
│   ├── custom_features_config.yaml  # 13 custom features
│   └── experiment_config.yaml  # Experiment settings
├── data/                      # Data loading and preprocessing
│   ├── universal_loader.py      # Universal data loading
│   └── gluon_preprocessor.py   # Minimal preprocessing
├── features/                  # Feature engineering
│   ├── auto_feature_engineer.py # Automatic feature generation
│   ├── custom_feature_engineer.py # Custom 13 features
│   └── feature_combiner.py     # Combine custom + automatic
├── models/                    # Model training and evaluation
│   ├── gluon_trainer.py        # TabularPredictor wrapper
│   ├── gluon_predictor.py      # Prediction wrapper
│   └── gluon_evaluator.py      # Evaluation wrapper
├── deployment/                # Model export and monitoring
│   ├── gluon_exporter.py       # Model export
│   ├── auto_retrainer.py       # Auto-retraining
│   └── drift_monitor.py        # Drift monitoring
├── utils/                     # Utilities
│   ├── logger.py               # Logging
│   └── metrics.py              # Value scores analysis
├── tests/                     # Comprehensive testing
│   ├── test_gluon_integration.py
│   ├── test_data_loading.py
│   └── test_model_training.py
└── examples/                 # Usage examples
    ├── basic_usage.py
    └── advanced_usage.py
```

## 🛠️ Installation

### Prerequisites
```bash
pip install autogluon.tabular
pip install pandas numpy scikit-learn
```

### Dependencies
- AutoGluon >= 0.8.0
- Pandas >= 1.5.0
- NumPy >= 1.21.0
- Scikit-learn >= 1.0.0

## 📖 Quick Start

### Basic Usage

```python
from src.automl.gluon import GluonAutoML

# Initialize with experiment configuration
experiment_config = {
    'experiment_name': 'trading_strategy',
    'target_column': 'target',
    'problem_type': 'binary',
    'time_limit': 3600,  # 1 hour
    'train_ratio': 0.6,
    'validation_ratio': 0.2,
    'test_ratio': 0.2
}

gluon = GluonAutoML(experiment_config=experiment_config)

# Load data from any folder in data/
data = gluon.load_data("data/cache/csv_converted/")

# Create time series split
train, val, test = gluon.create_time_series_split(data)

# Train models (AutoGluon does everything)
gluon.train_models(train, 'target', val)

# Evaluate models
results = gluon.evaluate_models(test, 'target')

# Make predictions
predictions = gluon.predict(test)

# Export models for walk forward/Monte Carlo
export_paths = gluon.export_models("models/autogluon/")
```

### Advanced Usage

```python
# Custom configuration
experiment_config = {
    'experiment_name': 'advanced_strategy',
    'target_column': 'target',
    'problem_type': 'binary',
    'use_custom_features': True,
    'max_auto_features': 1000,
    'enable_drift_monitoring': True,
    'retrain_on_drift': True
}

gluon = GluonAutoML(experiment_config=experiment_config)

# Load and prepare data
data = gluon.load_data("data/")
train, val, test = gluon.create_time_series_split(data)

# Train with custom features
gluon.train_models(train, 'target', val)

# Monitor drift
drift_results = gluon.monitor_drift(test)

# Export for different use cases
wf_paths = gluon.exporter.export_for_walk_forward(gluon.predictor, "models/wf/")
mc_paths = gluon.exporter.export_for_monte_carlo(gluon.predictor, "models/mc/")
```

## 🧪 Testing

### Run All Tests
```bash
# Multi-threaded testing
uv run pytest src/automl/gluon/tests/ -n auto

# Specific test modules
uv run pytest src/automl/gluon/tests/test_gluon_integration.py
uv run pytest src/automl/gluon/tests/test_data_loading.py
uv run pytest src/automl/gluon/tests/test_model_training.py
uv run pytest src/automl/gluon/tests/test_deployment.py
```

### Test Coverage
- ✅ **100% pytest coverage** for all modules
- ✅ **Multi-threaded execution** with `-n auto`
- ✅ **Integration tests** for end-to-end workflows
- ✅ **Unit tests** for individual components
- ✅ **Error handling tests** for robustness

## 📊 Configuration

### AutoGluon Configuration (`config/gluon_config.yaml`)
```yaml
# AutoGluon presets for maximum quality
presets:
  - "best_quality"
  - "high_quality"

# Time limit for training (seconds)
time_limit: 3600

# Automatic data cleaning
auto_clean: true

# Feature generation settings
feature_generation: true
max_features: 1000

# Validation settings
holdout_frac: 0.1
num_bag_folds: 5
num_bag_sets: 1

# Model selection (empty list means use all models)
excluded_model_types: []

# Hyperparameter optimization
hyperparameter_tune_kwargs:
  num_trials: 10
  search_strategy: "auto"
```

### Custom Features Configuration (`config/custom_features_config.yaml`)
```yaml
custom_features:
  trend_probability:
    description: "Probability of trend up/down/hold"
    source_columns: ["SCHR_columns", "WAVE2_columns"]
    calculation: "custom_trend_logic"
    
  level_breakout_yellow:
    description: "Yellow line breakout up/retreat"
    source_columns: ["Levels_columns"]
    calculation: "custom_level_logic"
    
  # ... 11 more custom features
```

## 🎯 Custom Features (13 Types)

The system supports 13 custom feature types for trading strategies:

1. **Trend Probability** - up/down/hold trend probability
2. **Level Breakout Yellow** - yellow line breakout up/retreat
3. **Level Breakout Blue** - blue line breakout down/retreat
4. **PV Sign** - PV sign positive/negative
5. **Wave Signal 1** - Signal=1, 5 candles up/reversal
6. **Wave Signal 1 Distance** - Signal=1, price further 5%
7. **Wave Signal 1 MA** - Signal=1 & ma<open, 5 candles up/reversal
8. **Wave Signal 1 MA Distance** - Signal=1 & ma<open, price further 5%
9. **Short3 Signal 1** - Signal=1, price up 5%
10. **Short3 Signal 4** - Signal=4, price down 10% (global reversal)
11. **Short3 Direction Change** - direction 1,4 to 2,3 change (global reversal)
12. **Wave Reverse Peak Sign** - next peak sign positive/negative
13. **Wave Reverse Peak Time** - next peak within 10 candles

## 📈 Value Scores Analysis

The system provides comprehensive value scores analysis:

- **Profit Factor** - Ratio of gross profit to gross loss
- **Sharpe Ratio** - Risk-adjusted return measure
- **Maximum Drawdown** - Largest peak-to-trough decline
- **Win Rate** - Percentage of profitable trades
- **Average Trade Duration** - Average holding period
- **Total Return** - Cumulative return percentage
- **Volatility** - Price volatility measure

## 🔍 Drift Monitoring

Automatic drift detection and monitoring:

- **PSI (Population Stability Index)** - Feature distribution changes
- **Feature Drift Detection** - Individual feature monitoring
- **Performance Degradation Alerts** - Model performance tracking
- **Automatic Retraining** - Retrain on drift detection

## 🚀 Deployment

### Model Export Formats
- **Pickle** - Native Python serialization
- **JSON** - Metadata and configuration
- **ONNX** - Cross-platform inference (if supported)

### Export for Different Use Cases
- **Walk Forward Analysis** - Time series validation
- **Monte Carlo Simulation** - Probabilistic analysis
- **Production Deployment** - Real-time inference

### Deployment Package
Complete deployment package includes:
- Trained model files
- Configuration files
- Requirements.txt
- README with usage instructions
- Compatibility information

## 📚 Examples

### Basic Example
```python
# See examples/basic_usage.py
python src/automl/gluon/examples/basic_usage.py
```

### Advanced Example
```python
# See examples/advanced_usage.py
python src/automl/gluon/examples/advanced_usage.py
```

## 🔧 Integration Points

### Walk Forward Analysis
- Model export compatibility
- Time series validation support
- Integration with existing walk forward modules

### Monte Carlo Simulation
- Probabilistic prediction support
- Integration with existing Monte Carlo modules

### Existing ML Modules
- Complement existing models in `src/ml/`
- Seamless integration with current architecture

## 📋 Best Practices

### Data Preparation
1. Use time series split for proper validation
2. Ensure data quality before training
3. Monitor for data drift regularly

### Model Training
1. Start with automatic approach
2. Add custom features if needed
3. Monitor performance continuously

### Deployment
1. Export models in multiple formats
2. Test models before production
3. Set up drift monitoring

## 🐛 Troubleshooting

### Common Issues
1. **AutoGluon not available** - Install with `pip install autogluon.tabular`
2. **Data loading errors** - Check file formats and paths
3. **Memory issues** - Use batch processing for large datasets
4. **Training failures** - Check data quality and configuration

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug information
gluon = GluonAutoML(experiment_config=config)
```

## 📞 Support

For issues and questions:
1. Check the comprehensive test suite
2. Review the examples in `examples/`
3. Check the configuration files
4. Enable debug logging for detailed information

## 🎯 Success Metrics

- **Data Quality**: 100% coverage of all formats in `data/`
- **Feature Engineering**: Automatic generation of 200-300 features
- **Validation**: Proper train/validation/test split
- **Performance**: Robust models with high accuracy
- **Monitoring**: Automatic drift detection
- **Integration**: Seamless integration with walk forward/Monte Carlo

---

**Note**: This module follows the project's AutoGluon-first philosophy, maximizing AutoGluon capabilities while providing minimal, efficient wrapper code for coordination and configuration.
