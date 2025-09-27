# AutoGluon Integration Documentation

## 📁 Documentation Structure

This folder contains the detailed implementation plan for integrating AutoGluon into the NeoZork HLDP project.

### Files:

- **`autogluon-integration-plan-en.md`** - Complete implementation plan in English
- **`autogluon-integration-plan-ru.md`** - Complete implementation plan in Russian
- **`README.md`** - This overview file

## 🎯 Project Goals

**Primary Goal**: Create robust, profitable ML models using AutoGluon framework for predicting 13 types of probabilities based on SCHR Levels, SHORT3, and WAVE2 indicators.

**Philosophy**: AutoGluon-first approach - maximize AutoGluon capabilities, minimize wrapper code.

## 📋 Key Features

### AutoGluon Capabilities
- ✅ Automatic data cleaning
- ✅ Automatic feature engineering (200-300 features)
- ✅ Automatic model selection (20+ algorithms)
- ✅ Automatic hyperparameter optimization
- ✅ Automatic validation
- ✅ Universal data format support (parquet/csv/json)

### Our Wrapper Responsibilities
- 🔄 Data loading from `data/` folder
- 🔄 AutoGluon configuration
- 🔄 Process coordination
- 🔄 Model export for walk forward/Monte Carlo
- 🔄 Drift monitoring

## 🗂️ Implementation Structure

```
src/automl/gluon/
├── gluon.py                    # Main wrapper (≤200 lines)
├── config/                    # Configuration files
├── data/                      # Data loading and preprocessing
├── features/                  # Feature engineering
├── models/                    # Model training and evaluation
├── deployment/                # Model export and monitoring
├── utils/                     # Utilities and logging
└── tests/                     # Comprehensive testing
```

## 🚀 Implementation Strategy

### Phase 1: Automatic Approach (Recommended)
1. Let AutoGluon create all features automatically
2. Analyze results and compare with custom 13 features
3. Evaluate if additional control is needed

### Phase 2: Hybrid Approach (If needed)
1. Implement custom 13 features configuration
2. Combine custom features with AutoGluon automatic features
3. Train hybrid models

## 📊 Success Metrics

1. **Data Quality**: 100% coverage of all formats in `data/`
2. **Feature Engineering**: Automatic generation of 200-300 features
3. **Validation**: Proper train/validation/test split
4. **Performance**: Robust models with high accuracy
5. **Monitoring**: Automatic drift detection
6. **Integration**: Seamless integration with walk forward/Monte Carlo

## 🧪 Testing Strategy

- **100% Pytest Coverage** for all modules
- **Multi-threaded execution**: `uv run pytest tests -n auto`
- **Comprehensive testing**: data loading, feature engineering, training, deployment

## 📈 Integration Points

- **Walk Forward Analysis**: Model export compatibility
- **Monte Carlo**: Probabilistic prediction support
- **Existing ML**: Complement current `src/ml/` modules
- **API**: REST API for real-time predictions

## 🎯 Next Steps

1. Review detailed plans in language-specific files
2. Implement core AutoGluon wrapper
3. Set up universal data loading
4. Configure AutoGluon for maximum feature engineering
5. Implement testing framework
6. Deploy and monitor

---

**Note**: This documentation follows the project's rule of creating documentation in `docs/` subfolders and maintaining bilingual support (English/Russian).
