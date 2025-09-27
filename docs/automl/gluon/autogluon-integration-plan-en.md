# AutoGluon Integration Plan for NeoZork HLDP

## 🎯 Project Overview

**Goal**: Create a robust, profitable ML model using AutoGluon framework for predicting 13 types of probabilities based on SCHR Levels, SHORT3, and WAVE2 indicators.

**Philosophy**: AutoGluon-first approach - maximize AutoGluon capabilities, minimize wrapper code.

## 📋 Architecture Overview

### Core Principle: AutoGluon Does Everything

- ✅ **Automatic data cleaning** - `TabularPredictor.fit()` with `auto_clean=True`
- ✅ **Automatic feature engineering** - built-in transformations
- ✅ **Automatic model selection** - ensemble of 20+ algorithms
- ✅ **Automatic hyperparameter optimization** - built-in
- ✅ **Automatic validation** - cross-validation
- ✅ **Automatic data type inference** - `infer_limit`
- ✅ **Automatic missing value handling** - built-in
- ✅ **Automatic scaling** - built-in

### Our Wrapper Does Only:
- 🔄 **Data loading** - file selection from `data/`
- 🔄 **Configuration** - AutoGluon parameter setup
- 🔄 **Coordination** - calling AutoGluon methods
- 🔄 **Export results** - model saving
- 🔄 **Monitoring** - process tracking

## 🗂️ Project Structure

```
src/automl/gluon/
├── __init__.py
├── gluon.py                    # Main wrapper (≤200 lines)
├── config/
│   ├── __init__.py
│   ├── gluon_config.yaml       # AutoGluon configuration
│   ├── custom_features_config.yaml  # 13 custom features (optional)
│   └── experiment_config.yaml  # Experiment configuration
├── data/
│   ├── __init__.py
│   ├── universal_loader.py      # Universal data loading
│   └── gluon_preprocessor.py   # Minimal wrapper for AutoGluon
├── features/
│   ├── __init__.py
│   ├── auto_feature_engineer.py # Automatic feature generation
│   ├── custom_feature_engineer.py # Custom 13 features (optional)
│   └── feature_combiner.py     # Combine custom + automatic
├── models/
│   ├── __init__.py
│   ├── gluon_trainer.py        # TabularPredictor wrapper
│   ├── gluon_predictor.py      # Prediction wrapper
│   ├── gluon_evaluator.py      # Evaluation wrapper
│   └── hybrid_trainer.py       # Hybrid training (if custom features)
├── deployment/
│   ├── __init__.py
│   ├── gluon_exporter.py       # Model export
│   ├── auto_retrainer.py       # Auto-retraining
│   └── drift_monitor.py        # Drift monitoring
├── utils/
│   ├── __init__.py
│   ├── logger.py               # Logging
│   └── metrics.py              # Additional metrics
└── tests/
    ├── __init__.py
    ├── test_gluon_integration.py
    ├── test_data_loading.py
    └── test_model_training.py
```

## 🔧 Key Components

### 1. Main Wrapper `gluon.py` (≤200 lines)

```python
class GluonAutoML:
    def __init__(self, config_path=None):
        # Initialize AutoGluon configuration
        pass
    
    def load_data(self, data_path):
        # Select and load data
        # AutoGluon will determine format and types
        pass
    
    def train_models(self, train_data, target_column):
        # TabularPredictor.fit() - AutoGluon does EVERYTHING
        pass
    
    def evaluate_models(self, test_data):
        # TabularPredictor.evaluate() - built-in evaluation
        pass
    
    def export_models(self, export_path):
        # TabularPredictor.save() - built-in export
        pass
    
    def retrain_models(self, new_data):
        # TabularPredictor.fit() with new data
        pass
```

### 2. AutoGluon Configuration

```yaml
# config/gluon_config.yaml
autogluon_config:
  # Maximum quality - AutoGluon creates hundreds of features
  presets: ['best_quality']
  time_limit: 3600
  
  # Automatic feature engineering
  feature_generation:
    enable: true
    max_features: 1000  # AutoGluon creates up to 1000 features
    
  # Automatic transformations
  transformations:
    - lag_features      # Lag features
    - rolling_features   # Rolling windows
    - interaction_features  # Interactions
    - polynomial_features    # Polynomial
    - statistical_features   # Statistical
    - temporal_features      # Temporal
    
  # Automatic feature selection
  feature_selection:
    enable: true
    method: 'auto'  # AutoGluon selects best features
    
  # Automatic model selection
  excluded_model_types: []  # Use all models
  
  # Automatic optimization
  hyperparameter_tune_kwargs:
    num_trials: 10
    search_strategy: 'auto'
```

### 3. Universal Data Loading

**Supports all formats in `data/` folder**:
- ✅ **Parquet files** - optimized loading
- ✅ **CSV files** - auto-detect separators
- ✅ **JSON files** - flat/nested structures
- ✅ **Excel files** - multiple sheets
- ✅ **HDF5 files** - large datasets

**Features**:
- Recursive search in `data/` folder
- Auto-format detection
- Minimal preprocessing for AutoGluon
- Time series validation

### 4. Time Series Split (3-way)

```python
# Time series split for train/validation/test
def create_time_series_split(data, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
    # Chronological split ensuring no data leakage
    # Train: 60%, Validation: 20%, Test: 20%
    # Test set is completely unknown to ML
    pass
```

## 🎯 Feature Engineering Strategy

### Option 1: Fully Automatic (Recommended)

**Let AutoGluon create all features automatically**:
- AutoGluon will create hundreds of features from your columns
- AutoGluon will find patterns matching your 13 types
- AutoGluon will create interactions between SCHR, SHORT3, WAVE2
- AutoGluon will create temporal features (lag, rolling, etc.)

**Advantages**:
- 🚀 **Maximum automation** - AutoGluon does everything
- 🎯 **Better quality** - AutoGluon finds better features than manual
- ⚡ **Fast development** - no need to code 13 features
- 🔄 **Automatic adaptation** - features adapt to new data

### Option 2: Hybrid (If control needed)

**Custom 13 features + AutoGluon**:

```yaml
# config/custom_features_config.yaml
custom_features:
  trend_probability:
    description: "Trend probability up/down/hold"
    source_columns: ["SCHR_columns", "WAVE2_columns"]
    calculation: "custom_trend_logic"
    
  level_breakout_yellow:
    description: "Yellow line breakout up/retreat"
    source_columns: ["Levels_columns"]
    calculation: "custom_level_logic"
    
  # ... remaining 11 features
  
  # AutoGluon adds automatic features
  autogluon_features:
    enable: true
    max_additional_features: 500
```

## 🚀 Workflow: AutoGluon-First

### Stage 1: Data Loading (Our wrapper)
1. Select data from `data/` (any file/folder)
2. Auto-detect format (parquet/csv/json)
3. Minimal preparation for AutoGluon

### Stage 2: Training (AutoGluon does EVERYTHING)
1. `TabularPredictor.fit()` - AutoGluon does everything
2. Automatic data cleaning
3. Automatic feature engineering
4. Automatic model selection
5. Automatic optimization

### Stage 3: Evaluation (AutoGluon does EVERYTHING)
1. `TabularPredictor.evaluate()` - built-in evaluation
2. Automatic metrics
3. Automatic plots
4. Automatic leaderboard

### Stage 4: Export (Our wrapper)
1. `TabularPredictor.save()` - built-in export
2. Save for walk forward/Monte Carlo
3. Log results

## 📊 Custom Features (13 Types)

### If Custom Features Needed:

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

## 🔧 Technical Implementation

### AutoGluon Configuration

```python
# Maximum feature engineering configuration
AUTOGLUON_CONFIG = {
    'presets': ['best_quality', 'high_quality'],
    'time_limit': 3600,  # 1 hour
    'auto_clean': True,
    'feature_generation': True,
    'holdout_frac': 0.1,
    'num_bag_folds': 5,
    'num_bag_sets': 1,
    'excluded_model_types': [],
    'hyperparameter_tune_kwargs': {
        'num_trials': 10,
        'search_strategy': 'auto'
    }
}
```

### Value Scores Analysis

- Profit Factor
- Sharpe Ratio
- Maximum Drawdown
- Win Rate
- Average Trade Duration

### Drift Monitoring

- PSI (Population Stability Index)
- Feature Drift Detection
- Performance Degradation Alerts

## 🧪 Testing Strategy

### 100% Pytest Coverage
- All modules covered with unit tests
- Multi-threaded execution: `uv run pytest tests -n auto`
- Tests for: data loading, feature engineering, training, deployment

### Test Structure
```
tests/
├── test_gluon_integration.py    # Integration tests
├── test_data_loading.py         # Data loading tests
├── test_feature_engineering.py  # Feature engineering tests
├── test_model_training.py       # Model training tests
└── test_deployment.py           # Deployment tests
```

## 📈 Integration with Existing Modules

### Walk Forward Analysis
- Export models in compatible format
- Support for time series validation
- Integration with existing walk forward modules

### Monte Carlo
- Support for probabilistic predictions
- Integration with existing Monte Carlo modules

### Existing ML
- Complement existing models in `src/ml/`
- Seamless integration with current architecture

## 🚀 Deployment

### Containerization
- Docker support
- Integration with existing container setup
- Production-ready deployment

### Scheduling
- Cron jobs for retraining
- Automatic retraining on drift detection
- Integration with existing monitoring

### API
- REST API for predictions
- Integration with existing API structure
- Real-time prediction capabilities

## 🎯 Success Metrics

1. **Data Quality**: 100% coverage of all formats in `data/`
2. **Feature Engineering**: Automatic generation of 200-300 features
3. **Validation**: Proper train/validation/test split
4. **Performance**: Robust models with high accuracy
5. **Monitoring**: Automatic drift detection
6. **Interpretability**: Explainable predictions

## 📋 Implementation Priority

### High Priority
1. Universal data loading - support all formats
2. Automatic feature generation - 200-300 features
3. Time series split - proper 3-way split
4. AutoGluon preprocessing - full cleaning through AutoGluon
5. Advanced validation - walk-forward, Monte Carlo

### Medium Priority
1. Ensemble methods - stacking, blending
2. Model monitoring - drift, performance
3. Feature optimization - automatic selection
4. Experiment tracking - logging experiments

### Low Priority
1. Model explainability - SHAP, feature importance
2. Online learning - incremental learning
3. Advanced visualization - charts and dashboards

## 🎯 Final Recommendation

**Start with Automatic Approach**:
1. **First try** - give AutoGluon complete freedom
2. **Analyze results** - see what was created
3. **If more control needed** - add custom features
4. **Iteratively improve** - combine approaches

**Result**: Maximum robust and profitable ML models with minimal code and maximum AutoGluon utilization.
