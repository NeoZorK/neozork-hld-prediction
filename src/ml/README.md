# ML Module

This module provides comprehensive machine learning capabilities for the NeoZork HLD Prediction trading platform.

## 📚 Documentation

**Full documentation is available in [docs/ml/](../docs/ml/index.md)**

- [ML Module Overview](../docs/ml/ml-module-overview.md) - Complete architecture and roadmap
- [Feature Engineering Guide](../docs/ml/feature_engineering_guide.md) - Automated feature generation system
- [API Reference](../docs/ml/api-reference.md) - Technical documentation (planned)

## 🚀 Quick Start

```python
from ml.feature_engineering import FeatureGenerator, MasterFeatureConfig

# Configure and generate features
config = MasterFeatureConfig(
    max_features=200,
    min_importance=0.3,
    enable_proprietary=True,
    enable_technical=True
)

generator = FeatureGenerator(config)
df_features = generator.generate_features(your_ohlcv_data)
```

## 🧪 Testing

```bash
# Run all ML tests with UV (multithreaded)
uv run pytest tests/ml/ -n auto
```

## 📁 Structure

```
src/ml/
├── __init__.py                    # Module initialization
├── README.md                      # This file (see docs/ml/ for full docs)
├── feature_engineering/           # Feature Engineering System
│   ├── __init__.py               # Feature engineering exports
│   ├── base_feature_generator.py # Base class for all generators
│   ├── feature_generator.py      # Main orchestrator
│   ├── proprietary_features.py   # PHLD + Wave features
│   ├── technical_features.py     # Technical indicators
│   ├── statistical_features.py   # Statistical features
│   ├── temporal_features.py      # Time-based features
│   ├── cross_timeframe_features.py # Multi-scale features
│   └── feature_selector.py       # Feature selection & optimization
├── models/                        # ML Models (PLANNED)
├── validation/                    # Validation System (PLANNED)
├── risk_management/              # Risk Management (PLANNED)
└── automation/                    # Automation Pipeline (PLANNED)
```

---

**Status**: Phase 1 Complete ✅ | Phase 2 In Progress 🔄 | Phase 3-6 Planned 📋

For complete documentation, see [docs/ml/](../docs/ml/index.md) 
