# Multi-Timeframe Data Loading Strategy

## Overview

The NeoZorK HLD Prediction system now supports proper multi-timeframe data loading strategy specifically designed for robust ML trading models. Instead of mixing data from different timeframes (M1, M5, H1, D1, MN1) into a single DataFrame, this approach treats each timeframe as a separate dataset and creates cross-timeframe features.

## Why Multi-Timeframe Strategy is Important

### Problems with Standard Approach

When you simply combine data from different timeframes:

1. **Time Inconsistency**: M1 data has 1440 points per day, while D1 data has 1 point per day
2. **Signal Confusion**: ML model receives conflicting signals from different time scales
3. **Data Leakage**: Future information from higher timeframes can leak into lower timeframes
4. **Poor Performance**: Mixed timeframe data often leads to overfitting and poor generalization

### Benefits of Multi-Timeframe Strategy

1. **Proper Time Hierarchy**: Each timeframe maintains its natural frequency
2. **Cross-Timeframe Features**: Higher timeframes provide context for lower timeframes
3. **No Data Leakage**: Proper temporal alignment prevents future information leakage
4. **Better ML Performance**: Models can learn multi-scale patterns effectively

## How It Works

### 1. Timeframe Detection

The system automatically detects timeframes from filename patterns:

```
Supported Patterns:
- M1: _M1_, _M1., PERIOD_M1, _1M_, _1M.
- M5: _M5_, _M5., PERIOD_M5, _5M_, _5M.
- H1: _H1_, _H1., PERIOD_H1, _1H_, _1H.
- D1: _D1_, _D1., PERIOD_D1, _1D_, _1D., _DAILY_
- MN1: _MN1_, _MN1., PERIOD_MN1, _1MN_, _1MN., _MONTHLY_
```

### 2. Base Timeframe Selection

User selects the primary timeframe for ML model training:

```
🎯 SELECT BASE TIMEFRAME
------------------------------
1. M1 (2 files)
2. H1 (1 files)  
3. D1 (3 files)
4. MN1 (1 files)

Select base timeframe (number): 2
```

### 3. Cross-Timeframe Features

Higher timeframes are used to generate additional features:

- **D1 features for H1 model**: Daily trends, support/resistance levels
- **H1 features for M5 model**: Hourly momentum, volatility patterns
- **MN1 features for D1 model**: Monthly cycles, long-term trends

## Usage

### Interactive Mode

1. Start the interactive system:
```bash
python interactive_system.py
```

2. Select "Load Data" from main menu

3. Choose "Multi-Timeframe Loading" strategy:
```
🎯 DATA LOADING STRATEGY
------------------------------
1. 📊 Standard Loading - Combine all files into single dataset
2. 🚀 Multi-Timeframe Loading - Proper ML strategy for multiple timeframes
0. 🔙 Back to Main Menu

Select loading strategy (1/2/0): 2
```

4. Select base timeframe and configure cross-timeframe features

### Programmatic Usage

```python
from src.interactive.data_manager import DataManager

# Initialize data manager
data_manager = DataManager()

# Load with multi-timeframe strategy
system = Mock()  # Your system instance
success = data_manager.load_multi_timeframe_data(system)

if success:
    print(f"Base timeframe: {system.timeframe_info['base_timeframe']}")
    print(f"Available timeframes: {list(system.timeframe_info['available_timeframes'].keys())}")
    
    # Access cross-timeframe data
    if hasattr(system, 'cross_timeframe_data'):
        for tf, data in system.cross_timeframe_data.items():
            print(f"{tf} features: {data.shape}")
```

## Data Structure

### Before (Standard Loading)
```
Combined DataFrame:
- Mixed M1, H1, D1 data
- Inconsistent time intervals
- Conflicting signals
- Poor ML performance
```

### After (Multi-Timeframe Loading)
```
system.current_data:          # Base timeframe (e.g., H1)
- Consistent H1 intervals
- Primary ML training data

system.timeframe_info:        # Metadata
- base_timeframe: 'H1'
- available_timeframes: {...}
- cross_timeframes: {...}

system.cross_timeframe_data:  # Cross-timeframe features
- D1_sma_20: Daily SMA features
- D1_rsi_14: Daily RSI features
- M5_momentum_5: 5-minute momentum
```

## Best Practices

### 1. Base Timeframe Selection

Choose base timeframe based on trading strategy:

- **M1/M5**: Scalping, high-frequency trading
- **H1/H4**: Intraday trading, swing trading
- **D1**: Daily trading, position trading
- **W1/MN1**: Long-term investing

### 2. Cross-Timeframe Strategy

Use higher timeframes for context:

- **For M1 base**: Use M5, H1, D1 for context
- **For H1 base**: Use H4, D1, W1 for context  
- **For D1 base**: Use W1, MN1 for context

### 3. Feature Engineering

Generate appropriate features for each timeframe:

- **Lower timeframes**: Momentum, volatility, short-term patterns
- **Higher timeframes**: Trends, support/resistance, long-term cycles

## Memory Management

The system includes aggressive memory optimization:

```
Memory Settings:
- Max memory: 6GB (configurable)
- Chunk size: 50,000 rows
- File size threshold: 200MB
- Sample size: 10,000 rows
```

### Environment Variables

```bash
export MAX_MEMORY_MB=6144
export CHUNK_SIZE=50000
export MAX_FILE_SIZE_MB=200
export ENABLE_MEMORY_OPTIMIZATION=true
```

## File Organization

### Recommended Structure

```
data/
├── raw_parquet/
│   ├── EURUSD_M1.parquet
│   ├── EURUSD_M5.parquet
│   ├── EURUSD_H1.parquet
│   ├── EURUSD_D1.parquet
│   └── EURUSD_MN1.parquet
├── indicators/
│   └── parquet/
│       ├── EURUSD_M1_RSI.parquet
│       ├── EURUSD_H1_MACD.parquet
│       └── EURUSD_D1_SMA.parquet
└── cache/
    └── csv_converted/
        └── (cached converted files)
```

### Naming Conventions

Use clear timeframe indicators in filenames:

- **Good**: `EURUSD_PERIOD_H1.csv`, `BTCUSDT_H1.parquet`
- **Bad**: `data.csv`, `prices.parquet`

## Integration with ML Pipeline

### 1. Feature Engineering

After loading multi-timeframe data:

```python
# Generate features for base timeframe
from src.ml.feature_engineering import FeatureGenerator

feature_gen = FeatureGenerator()
features_df = feature_gen.generate_features(system.current_data)

# Add cross-timeframe features
for tf, cross_data in system.cross_timeframe_data.items():
    cross_features = feature_gen.generate_features(cross_data)
    # Align and merge features (implementation needed)
```

### 2. Model Training

Use base timeframe for training with cross-timeframe features as additional inputs:

```python
# Prepare training data
X = features_df.drop(['target'], axis=1)  # Features
y = features_df['target']  # Target variable

# Train model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, y)
```

## Troubleshooting

### Common Issues

1. **No timeframes detected**: Check filename patterns
2. **Memory issues**: Reduce chunk size or enable streaming
3. **Missing files**: Verify file paths and permissions
4. **Import errors**: Ensure all dependencies are installed

### Debug Commands

```bash
# Test timeframe detection
python -c "
from src.interactive.data_manager import DataManager
dm = DataManager()
print(dm._detect_timeframe_from_filename('EURUSD_H1.csv'))
"

# Check memory usage
python -c "
from src.interactive.data_manager import DataManager
dm = DataManager()
print(dm._get_memory_info())
"
```

## Future Enhancements

### Planned Features

1. **Automatic Time Alignment**: Intelligent alignment of different timeframes
2. **Feature Synchronization**: Automatic feature alignment across timeframes
3. **Timeframe Optimization**: Automatic selection of optimal timeframe combinations
4. **Real-time Updates**: Support for real-time multi-timeframe data feeds

### Configuration Options

Future configuration options will include:

- Custom timeframe detection patterns
- Automatic feature alignment strategies
- Memory optimization profiles
- Timeframe hierarchy definitions

## Examples

### Example 1: Forex Trading Model

```bash
# Load EURUSD data with multiple timeframes
python interactive_system.py
# Select: Load Data -> Multi-Timeframe Loading
# Base timeframe: H1
# Cross-timeframes: M5, D1, W1
```

### Example 2: Crypto Trading Model

```bash
# Load BTCUSDT data
# Base timeframe: M5
# Cross-timeframes: M1, H1, D1
```

### Example 3: Stock Trading Model

```bash
# Load AAPL data  
# Base timeframe: D1
# Cross-timeframes: H1, W1, MN1
```

## Conclusion

The multi-timeframe data loading strategy provides a solid foundation for building robust ML trading models. By properly separating different timeframes and creating meaningful cross-timeframe features, the system can learn complex multi-scale patterns while avoiding common pitfalls of mixed timeframe data.
