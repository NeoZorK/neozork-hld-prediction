# AutoGluon Integration User Manual

## 📋 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Data Loading](#data-loading)
6. [Model Training](#model-training)
7. [Model Evaluation](#model-evaluation)
8. [Model Deployment](#model-deployment)
9. [Advanced Usage](#advanced-usage)
10. [Troubleshooting](#troubleshooting)

## 🎯 Overview

The AutoGluon integration provides a comprehensive solution for creating robust and profitable ML models for trading strategies. It leverages AutoGluon's powerful AutoML capabilities while providing specialized features for financial data analysis.

### Key Features

- **Universal Data Loading**: Support for Parquet, CSV, JSON, Excel, and HDF5 formats
- **Time Series Processing**: Proper chronological train/validation/test splitting
- **AutoGluon-First Architecture**: Minimal wrapper, maximum AutoGluon utilization
- **Value Scores Analysis**: Trading-specific metrics (Profit Factor, Sharpe Ratio, etc.)
- **Model Deployment**: Export for walk forward and Monte Carlo analysis
- **Drift Monitoring**: Automatic model drift detection
- **Auto Retraining**: Scheduled and drift-triggered retraining

## 🚀 Installation

### Prerequisites

```bash
# Install AutoGluon
uv add autogluon.tabular

# Install additional dependencies
uv add openpyxl
```

### Verify Installation

```python
from src.automl.gluon import GluonAutoML

# Test basic functionality
gluon = GluonAutoML()
print("✅ AutoGluon integration ready!")
```

## ⚡ Quick Start

### Basic Usage

```python
from src.automl.gluon import GluonAutoML
import pandas as pd

# Initialize AutoGluon
gluon = GluonAutoML()

# Load data from any location in data/ directory
data = gluon.load_data("data/cache/csv_converted/")

# Create time series split
train, val, test = gluon.create_time_series_split(
    data, 
    target_column="target",
    train_ratio=0.6,
    val_ratio=0.2,
    test_ratio=0.2
)

# Train models
model = gluon.train_models(train, "target", val)

# Make predictions
predictions = gluon.predict(model, test)
probabilities = gluon.predict_proba(model, test)

# Evaluate models
evaluation = gluon.evaluate_models(model, test, "target")

# Analyze value scores
value_scores = gluon.analyze_value_scores(predictions, test["target"])

print(f"Model accuracy: {evaluation['accuracy']:.3f}")
print(f"Profit factor: {value_scores['profit_factor']:.3f}")
```

## ⚙️ Configuration

### Gluon Configuration

Edit `src/automl/gluon/config/gluon_config.yaml`:

```yaml
# AutoGluon settings
presets: 'best_quality'  # Options: 'best_quality', 'high_quality', 'good_quality', 'medium_quality', 'fast_inference'
time_limit: 3600  # Training time limit in seconds
eval_metric: 'roc_auc'  # Evaluation metric
verbosity: 2  # Logging level (0-4)

# Hyperparameters (optional)
hyperparameters:
  GBM: {}
  XGB: {}
  RF: {}
  NN_TORCH: {}
  FASTAI: {}

# Ensemble settings
num_bag_folds: 0
num_bag_sets: 1
num_stack_levels: 0
auto_stack: false
refit_full: true
save_space: false
```

### Experiment Configuration

```python
from src.automl.gluon.config import ExperimentConfig

# Create experiment configuration
experiment_config = ExperimentConfig({
    'experiment_name': 'trading_strategy_v1',
    'target_column': 'target',
    'problem_type': 'binary',  # 'binary', 'multiclass', 'regression'
    'time_limit': 1800,  # 30 minutes
    'presets': 'high_quality'
})

# Initialize with custom config
gluon = GluonAutoML(experiment_config=experiment_config)
```

### Custom Features Configuration

Edit `src/automl/gluon/config/custom_features_config.yaml`:

```yaml
custom_features:
  - name: "SCHR_Trend_Direction"
    type: "categorical_prediction"
    description: "Probability of trend being up/down/hold based on SCHR Levels"
    
  - name: "Levels_Yellow_Breakout_Up"
    type: "binary_prediction"
    description: "Probability of breaking yellow line upwards or bouncing"
    
  - name: "Wave_Signal_5_Candles"
    type: "binary_prediction"
    description: "If Signal=1, probability of 5 candles up or reversal"
    
  # Add more custom features as needed
```

## 📊 Data Loading

### Supported Formats

- **Parquet**: `.parquet` files
- **CSV**: `.csv` files
- **JSON**: `.json` files
- **Excel**: `.xlsx`, `.xls` files
- **HDF5**: `.hdf5`, `.h5` files

### Loading from Different Sources

```python
# Load from specific file
data = gluon.load_data("data/cache/csv_converted/CSVExport.parquet")

# Load from directory (recursive)
data = gluon.load_data("data/indicators/")

# Load from multiple sources
data1 = gluon.load_data("data/cache/csv_converted/")
data2 = gluon.load_data("data/indicators/csv/")
combined_data = pd.concat([data1, data2], ignore_index=True)
```

### Data Validation

```python
# Check data quality
summary = gluon.data_loader.get_data_summary(data)
print(f"Data shape: {summary['shape']}")
print(f"Missing values: {summary['missing_values']}")
print(f"Quality issues: {summary['quality_issues']}")
print(f"Ready for AutoGluon: {summary['is_ready_for_gluon']}")
```

## 🤖 Model Training

### Basic Training

```python
# Train with default settings
model = gluon.train_models(train_data, "target")

# Train with validation data
model = gluon.train_models(train_data, "target", validation_data=val_data)

# Train with custom configuration
experiment_config = ExperimentConfig({
    'target_column': 'target',
    'problem_type': 'binary',
    'time_limit': 1800,
    'presets': 'high_quality'
})
gluon = GluonAutoML(experiment_config=experiment_config)
model = gluon.train_models(train_data, "target")
```

### Advanced Training Options

```python
# Custom hyperparameters
gluon_config = GluonConfig()
gluon_config.set('hyperparameters', {
    'GBM': {'num_leaves': 31, 'learning_rate': 0.05},
    'XGB': {'max_depth': 6, 'learning_rate': 0.1},
    'RF': {'n_estimators': 100, 'max_depth': 10}
})

# Ensemble settings
gluon_config.set('num_bag_folds', 5)
gluon_config.set('num_stack_levels', 2)
gluon_config.set('auto_stack', True)

gluon = GluonAutoML(gluon_config_path='custom_config.yaml')
model = gluon.train_models(train_data, "target")
```

## 📈 Model Evaluation

### Basic Evaluation

```python
# Evaluate model performance
evaluation = gluon.evaluate_models(model, test_data, "target")

print(f"Accuracy: {evaluation['accuracy']:.3f}")
print(f"ROC AUC: {evaluation['roc_auc']:.3f}")
print(f"Precision: {evaluation['precision']:.3f}")
print(f"Recall: {evaluation['recall']:.3f}")
```

### Value Scores Analysis

```python
# Analyze trading-specific metrics
predictions = gluon.predict(model, test_data)
probabilities = gluon.predict_proba(model, test_data)

value_scores = gluon.analyze_value_scores(
    predictions, 
    test_data["target"],
    returns=test_data["returns"],  # Optional: actual returns
    trade_signals=test_data["signals"]  # Optional: trade signals
)

print(f"Profit Factor: {value_scores['profit_factor']:.3f}")
print(f"Sharpe Ratio: {value_scores['sharpe_ratio']:.3f}")
print(f"Max Drawdown: {value_scores['max_drawdown']:.3f}")
print(f"Win Rate: {value_scores['win_rate']:.3f}")
```

### Model Information

```python
# Get model leaderboard
leaderboard = model.leaderboard()
print(leaderboard)

# Get feature importance
importance = model.feature_importance()
print(importance)

# Get model info
info = model.get_model_info()
print(f"Best model: {info['best_model']}")
print(f"Model type: {info['model_type']}")
```

## 🚀 Model Deployment

### Export for Walk Forward Analysis

```python
# Export model for walk forward analysis
export_paths = gluon.export_models(model, "models/walk_forward/")

print(f"Model exported to: {export_paths['model_path']}")
print(f"Metadata: {export_paths['metadata_path']}")
print(f"Config: {export_paths['config_path']}")
```

### Export for Monte Carlo Analysis

```python
# Export model for Monte Carlo analysis
export_paths = gluon.export_models(model, "models/monte_carlo/")

print(f"Model exported to: {export_paths['model_path']}")
print(f"Supports probability: {export_paths['supports_probability']}")
```

### Complete Deployment Package

```python
# Create complete deployment package
deployment_paths = gluon.export_models(model, "models/deployment/")

print(f"Model: {deployment_paths['model_path']}")
print(f"Requirements: {deployment_paths['requirements_path']}")
print(f"README: {deployment_paths['readme_path']}")
```

## 🔄 Model Retraining

### Automatic Retraining

```python
# Check if retraining is needed
should_retrain = gluon.retrainer.should_retrain(
    baseline_performance=0.85,
    current_performance=0.82,
    new_data_size=1000
)

if should_retrain:
    print("Retraining recommended")
    
    # Retrain model
    new_model = gluon.retrain_model(model, new_data, "target")
    print("Model retrained successfully")
```

### Drift Monitoring

```python
# Monitor for data drift
drift_results = gluon.monitor_drift(model, current_data, reference_data)

if drift_results['overall_drift_alert']:
    print("Data drift detected!")
    for feature, result in drift_results.items():
        if isinstance(result, dict) and result.get('drift_detected'):
            print(f"Drift in {feature}: PSI = {result['psi']:.3f}")
```

## 🔧 Advanced Usage

### Custom Feature Engineering

```python
# Add custom features before training
def add_custom_features(df):
    # Example: Add technical indicators
    df['rsi'] = calculate_rsi(df['close'])
    df['sma_20'] = df['close'].rolling(20).mean()
    df['price_change'] = df['close'].pct_change()
    return df

# Apply custom features
train_data = add_custom_features(train_data)
val_data = add_custom_features(val_data)
test_data = add_custom_features(test_data)

# Train with custom features
model = gluon.train_models(train_data, "target")
```

### Hyperparameter Optimization

```python
# Custom hyperparameter search
gluon_config = GluonConfig()
gluon_config.set('hyperparameters', {
    'GBM': {
        'num_leaves': [31, 63, 127],
        'learning_rate': [0.01, 0.05, 0.1],
        'feature_fraction': [0.8, 0.9, 1.0]
    },
    'XGB': {
        'max_depth': [4, 6, 8],
        'learning_rate': [0.05, 0.1, 0.2],
        'subsample': [0.8, 0.9, 1.0]
    }
})

gluon = GluonAutoML(gluon_config_path='custom_config.yaml')
model = gluon.train_models(train_data, "target")
```

### Model Ensemble

```python
# Configure ensemble settings
gluon_config = GluonConfig()
gluon_config.set('num_bag_folds', 5)
gluon_config.set('num_stack_levels', 2)
gluon_config.set('auto_stack', True)
gluon_config.set('refit_full', True)

gluon = GluonAutoML(gluon_config_path='ensemble_config.yaml')
model = gluon.train_models(train_data, "target")
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors

```python
# If you get import errors, check installation
try:
    from autogluon.tabular import TabularPredictor
    print("✅ AutoGluon installed correctly")
except ImportError:
    print("❌ AutoGluon not installed. Run: uv add autogluon.tabular")
```

#### 2. Memory Issues

```python
# For large datasets, use memory-efficient settings
gluon_config = GluonConfig()
gluon_config.set('save_space', True)
gluon_config.set('num_bag_folds', 0)  # Disable bagging for memory efficiency
gluon_config.set('time_limit', 1800)  # Limit training time
```

#### 3. Data Quality Issues

```python
# Check data quality before training
summary = gluon.data_loader.get_data_summary(data)

if not summary['is_ready_for_gluon']:
    print("Data quality issues detected:")
    for issue in summary['quality_issues']:
        print(f"- {issue}")
    
    # Clean data
    cleaned_data = gluon.data_loader.clean_data(data)
    summary = gluon.data_loader.get_data_summary(cleaned_data)
```

#### 4. Model Performance Issues

```python
# If model performance is poor, try:
# 1. Increase training time
gluon_config.set('time_limit', 3600)  # 1 hour

# 2. Use higher quality presets
gluon_config.set('presets', 'best_quality')

# 3. Add more data
# 4. Check feature engineering
# 5. Verify target variable quality
```

### Performance Optimization

```python
# For faster inference
gluon_config = GluonConfig()
gluon_config.set('presets', 'fast_inference')
gluon_config.set('save_space', True)

# For better accuracy
gluon_config.set('presets', 'best_quality')
gluon_config.set('time_limit', 7200)  # 2 hours
gluon_config.set('num_bag_folds', 5)
gluon_config.set('auto_stack', True)
```

### Logging and Debugging

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check model training progress
gluon_config.set('verbosity', 4)  # Maximum verbosity
gluon = GluonAutoML(gluon_config_path='debug_config.yaml')
model = gluon.train_models(train_data, "target")
```

## 📚 Examples

### Complete Trading Strategy Example

```python
from src.automl.gluon import GluonAutoML
import pandas as pd

# Initialize AutoGluon
gluon = GluonAutoML()

# Load trading data
data = gluon.load_data("data/cache/csv_converted/")

# Create time series split
train, val, test = gluon.create_time_series_split(
    data, 
    target_column="target",
    train_ratio=0.6,
    val_ratio=0.2,
    test_ratio=0.2
)

# Train model
model = gluon.train_models(train, "target", val)

# Evaluate on test set
evaluation = gluon.evaluate_models(model, test, "target")
print(f"Test accuracy: {evaluation['accuracy']:.3f}")

# Analyze value scores
predictions = gluon.predict(model, test)
value_scores = gluon.analyze_value_scores(predictions, test["target"])
print(f"Profit factor: {value_scores['profit_factor']:.3f}")

# Export for production
export_paths = gluon.export_models(model, "models/production/")
print(f"Model ready for production: {export_paths['model_path']}")
```

## 📞 Support

For additional support and examples, refer to:

- **Documentation**: `docs/automl/gluon/`
- **Examples**: `src/automl/gluon/examples/`
- **Configuration**: `src/automl/gluon/config/`
- **Tests**: `src/automl/gluon/tests/`

## 🎯 Best Practices

1. **Always use time series split** for financial data
2. **Monitor data drift** regularly
3. **Use appropriate presets** for your use case
4. **Validate data quality** before training
5. **Export models** for production use
6. **Monitor model performance** over time
7. **Retrain models** when drift is detected
8. **Use value scores** for trading strategy evaluation
