# Feature Engineering Guide

## Overview

The Feature Engineering system is the foundation of the NeoZork ML trading platform. It automatically generates 100+ features from your proprietary PHLD and Wave indicators, along with standard technical indicators, statistical features, and temporal patterns.

## Architecture

```
FeatureGenerator (Main Orchestrator)
├── ProprietaryFeatureGenerator (PHLD + Wave)
├── TechnicalFeatureGenerator (Standard Indicators)
├── StatisticalFeatureGenerator (Math Features)
├── TemporalFeatureGenerator (Time Patterns)
├── CrossTimeframeFeatureGenerator (Multi-scale)
└── FeatureSelector (Optimization)
```

## Quick Start

### Basic Usage

```python
from ml.feature_engineering import FeatureGenerator, MasterFeatureConfig

# Create configuration
config = MasterFeatureConfig(
    max_features=200,
    min_importance=0.3,
    enable_proprietary=True,
    enable_technical=True
)

# Initialize generator
generator = FeatureGenerator(config)

# Generate features
df_with_features = generator.generate_features(your_ohlcv_data)

# Get results
print(f"Generated {generator.get_feature_count()} features")
print(f"Feature categories: {generator.get_feature_categories()}")
```

### Demo Script

Run the complete demo to see the system in action:

```bash
# From project root
uv run python scripts/demo_feature_engineering.py
```

## Configuration

### Master Configuration

```python
from ml.feature_engineering import MasterFeatureConfig

config = MasterFeatureConfig(
    # Enable/disable feature types
    enable_proprietary=True,      # PHLD + Wave features
    enable_technical=True,        # Standard indicators
    enable_statistical=True,      # Math features
    enable_temporal=True,         # Time patterns
    enable_cross_timeframe=True,  # Multi-scale analysis
    
    # Feature selection
    max_features=200,             # Maximum features to keep
    min_importance=0.3,          # Minimum importance threshold
    correlation_threshold=0.95,   # Remove highly correlated features
    
    # Performance
    parallel_processing=False,    # Enable for large datasets
    memory_limit_gb=8.0          # Memory limit
)
```

### Proprietary Features Configuration

```python
from ml.feature_engineering import ProprietaryFeatureConfig

proprietary_config = ProprietaryFeatureConfig(
    # PHLD settings
    phld_point_size=0.00001,     # Forex point size
    phld_trading_rules=['PV_HighLow', 'PV_Momentum', 'PV_Divergence'],
    
    # Wave settings
    wave_parameter_sets=[
        # Conservative
        {'long1': 339, 'fast1': 10, 'trend1': 2, 'long2': 22, 'fast2': 11, 'trend2': 4, 'sma_period': 22},
        # Aggressive
        {'long1': 100, 'fast1': 5, 'trend1': 1, 'long2': 15, 'fast2': 8, 'trend2': 2, 'sma_period': 15}
    ],
    wave_trading_rules=['TR_Fast', 'TR_Zone', 'TR_StrongTrend'],
    
    # Feature combinations
    create_derivative_features=True,    # Rate of change features
    create_interaction_features=True,   # Feature interactions
    create_momentum_features=True       # Momentum patterns
)
```

### Technical Features Configuration

```python
from ml.feature_engineering import TechnicalFeatureConfig

technical_config = TechnicalFeatureConfig(
    # Moving averages
    ma_types=['sma', 'ema'],
    short_periods=[5, 10, 14],
    medium_periods=[20, 50, 100],
    long_periods=[200, 500],
    
    # Oscillators
    rsi_periods=[14, 21, 50],
    stoch_k_periods=[14, 21],
    stoch_d_periods=[3, 5],
    
    # Momentum
    macd_fast_periods=[12, 26],
    macd_slow_periods=[26, 52],
    macd_signal_periods=[9, 18],
    
    # Volatility
    bb_periods=[20, 50],
    bb_std_devs=[2.0, 2.5],
    atr_periods=[14, 20],
    
    # Price types
    price_types=['open', 'high', 'low', 'close']
)
```

## Feature Types

### 1. Proprietary Features (PHLD + Wave)

**PHLD Features:**
- `phld_PV_HighLow_hl` - High-Low range
- `phld_PV_HighLow_pressure` - Market pressure
- `phld_PV_HighLow_pv` - Pressure vector
- `phld_PV_HighLow_pprice1` - Predicted low
- `phld_PV_HighLow_pprice2` - Predicted high
- `phld_PV_HighLow_direction` - Trading direction

**Wave Features:**
- `wave_0_TR_Fast_value` - Wave indicator value
- `wave_0_TR_Fast_momentum` - Wave momentum
- `wave_0_TR_Fast_volatility` - Wave volatility
- `wave_0_TR_Fast_trend` - Wave trend
- `wave_0_TR_Fast_position` - Wave position

**Derivative Features:**
- `*_derivative` - First derivative (rate of change)
- `*_derivative2` - Second derivative (acceleration)
- `*_roc` - Rate of change percentage
- `*_ma*_ratio` - Moving average ratios

### 2. Technical Features

**Moving Averages:**
- `sma_20_close` - 20-period SMA on close
- `ema_50_open` - 50-period EMA on open
- `*_ratio` - Price vs MA ratio
- `*_distance` - Distance from MA

**Oscillators:**
- `rsi_14` - 14-period RSI
- `rsi_14_oversold` - RSI oversold zone
- `rsi_14_overbought` - RSI overbought zone
- `stoch_14_3_k` - Stochastic %K
- `stoch_14_3_d` - Stochastic %D

**Momentum:**
- `macd_12_26_9_line` - MACD line
- `macd_12_26_9_signal` - MACD signal
- `macd_12_26_9_histogram` - MACD histogram
- `macd_12_26_9_crossover` - MACD crossover

**Volatility:**
- `atr_14` - 14-period ATR
- `atr_14_ratio` - ATR to price ratio
- `bb_20_20_upper` - Bollinger Bands upper
- `bb_20_20_lower` - Bollinger Bands lower
- `bb_20_20_width` - Bollinger Bands width

### 3. Statistical Features

**Central Tendency:**
- `mean_close_20` - 20-period mean
- `median_open_50` - 50-period median
- `geometric_mean_high_100` - 100-period geometric mean

**Dispersion:**
- `std_close_20` - 20-period standard deviation
- `variance_low_50` - 50-period variance
- `range_open_100` - 100-period range
- `iqr_high_20` - 20-period interquartile range

**Distribution:**
- `skewness_close_50` - 50-period skewness
- `kurtosis_open_100` - 100-period kurtosis
- `jarque_bera_close_20` - Jarque-Bera test statistic

**Outliers:**
- `outlier_close_20_2` - Z-score outliers (2σ)
- `iqr_outlier_open_50` - IQR-based outliers

### 4. Temporal Features

**Time Features:**
- `hour` - Hour of day (0-23)
- `minute` - Minute of hour (0-59)
- `time_of_day` - Normalized time (0-1)
- `business_hours` - Business hours indicator
- `asian_session` - Asian trading session
- `london_session` - London trading session
- `ny_session` - New York trading session

**Date Features:**
- `day_of_week` - Day of week (0=Monday)
- `day_of_month` - Day of month (1-31)
- `month` - Month (1-12)
- `quarter` - Quarter (1-4)
- `is_weekend` - Weekend indicator
- `is_month_end` - Month end indicator

**Cyclical Features:**
- `hour_sin`, `hour_cos` - 24-hour cycle
- `day_sin`, `day_cos` - 7-day cycle
- `month_sin`, `month_cos` - 12-month cycle

### 5. Cross-Timeframe Features

**Ratio Features:**
- `ratio_close_current_short_20` - Current vs short-term average
- `ratio_close_current_long_50` - Current vs long-term average
- `ratio_close_short_long_100` - Short vs long-term average

**Difference Features:**
- `diff_close_current_short_20` - Current vs short-term difference
- `diff_close_current_long_50` - Current vs long-term difference
- `norm_diff_close_current_long_100` - Normalized difference

**Momentum Features:**
- `momentum_close_short_20` - Short-term momentum
- `momentum_close_long_50` - Long-term momentum
- `momentum_accel_close_100` - Momentum acceleration

## Feature Selection

The system automatically selects the best features using multiple methods:

1. **Correlation Analysis** - Removes highly correlated features
2. **Importance Scoring** - Uses your proprietary algorithms
3. **Mutual Information** - Measures feature-target relationships
4. **Lasso Regression** - Sparse feature selection
5. **Random Forest** - Tree-based importance

### Selection Configuration

```python
from ml.feature_engineering import FeatureSelectionConfig

selection_config = FeatureSelectionConfig(
    methods=['correlation', 'importance', 'mutual_info', 'lasso'],
    max_features=200,
    min_importance=0.3,
    correlation_threshold=0.95,
    cv_folds=5
)
```

## Performance Optimization

### Memory Management

```python
# Monitor memory usage
memory_info = generator.get_memory_usage()
print(f"Memory usage: {memory_info['rss_mb']:.1f} MB")

# Cleanup resources
generator.cleanup()
```

### Parallel Processing

```python
config = MasterFeatureConfig(
    parallel_processing=True,
    memory_limit_gb=16.0
)
```

### Feature Limits

```python
config = MasterFeatureConfig(
    max_features=100,        # Limit total features
    min_importance=0.5       # Higher threshold
)
```

## Output and Reports

### Feature Summary

```python
summary = generator.get_feature_summary()
print(f"Total features: {summary['total_features']}")
print(f"Categories: {summary['categories']}")
print(f"Importance: {summary['importance']}")
```

### Export Reports

```python
# Feature generation report
feature_report = generator.export_feature_report()

# Feature selection report
selection_report = generator.feature_selector.export_selection_report()
```

### Feature Categories

```python
categories = generator.get_feature_categories()
for category, features in categories.items():
    print(f"{category}: {len(features)} features")
```

## Advanced Usage

### Custom Feature Generators

```python
from ml.feature_engineering.base_feature_generator import BaseFeatureGenerator

class CustomFeatureGenerator(BaseFeatureGenerator):
    def generate_features(self, df):
        # Your custom logic here
        df['custom_feature'] = df['Close'].rolling(10).apply(your_function)
        return df
        
    def get_feature_names(self):
        return ['custom_feature']
```

### Integration with ML Pipeline

```python
# Generate features
df_features = generator.generate_features(df)

# Split features and target
feature_columns = [col for col in df_features.columns if col not in ['Open', 'High', 'Low', 'Close', 'Volume']]
X = df_features[feature_columns]
y = df_features['Close'].pct_change().shift(-1)  # Next period return

# Train ML model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X.fillna(0), y.dropna())
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Memory Issues**: Reduce `max_features` or enable `parallel_processing`
3. **Slow Performance**: Check data size and reduce feature complexity
4. **Missing Features**: Verify data has required OHLCV columns

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Check generator status
print(f"Generators: {list(generator.generators.keys())}")
print(f"Feature count: {generator.get_feature_count()}")
```

## Best Practices

1. **Start Simple**: Begin with basic configuration and add complexity
2. **Monitor Performance**: Track memory usage and processing time
3. **Validate Features**: Check feature importance and correlations
4. **Regular Cleanup**: Use `cleanup()` method to free resources
5. **Test Incrementally**: Test each generator separately first

## Examples

### Complete Example

```python
from ml.feature_engineering import FeatureGenerator, MasterFeatureConfig
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')

# Configure system
config = MasterFeatureConfig(
    max_features=150,
    min_importance=0.3,
    enable_proprietary=True,
    enable_technical=True,
    enable_statistical=True
)

# Generate features
generator = FeatureGenerator(config)
df_features = generator.generate_features(df)

# Results
print(f"Generated {generator.get_feature_count()} features")
print(f"Data shape: {df.shape} → {df_features.shape}")

# Export report
generator.export_feature_report()

# Cleanup
generator.cleanup()
```

This system provides a comprehensive foundation for your ML trading strategy, automatically creating the features needed for profitable and robust trading models.
