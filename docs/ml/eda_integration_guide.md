# EDA Integration Guide

Complete guide to using the integrated EDA and Feature Engineering system in NeoZork HLD Prediction.

## 🚀 Quick Start

### 1. Integrated Pipeline (Recommended)
```bash
# Run complete EDA + Feature Engineering pipeline
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

# EDA mode
./nz_interactive --eda
```

### 3. Direct Python Scripts
```bash
# Integrated pipeline
python scripts/eda_feature_engineering.py --file data.csv --full-pipeline

# Interactive system
python scripts/interactive_system.py

# Feature engineering demo
python scripts/demo_feature_engineering.py
```

## 🔧 System Architecture

### Integration Components

```
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATED SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│  📊 EDA Analysis          │  ⚙️ Feature Engineering        │
│  ├─ Data Quality          │  ├─ Proprietary Features      │
│  ├─ Basic Statistics      │  ├─ Technical Indicators     │
│  ├─ Correlation Analysis  │  ├─ Statistical Features     │
│  └─ Time Series Analysis  │  ├─ Temporal Features        │
│                           │  └─ Cross-Timeframe Features  │
├─────────────────────────────────────────────────────────────┤
│  📈 Visualization         │  🎯 Feature Selection         │
│  ├─ Interactive Charts    │  ├─ Correlation Analysis     │
│  ├─ Distribution Plots    │  ├─ Importance Scoring       │
│  ├─ Correlation Maps      │  ├─ Mutual Information       │
│  └─ Export Capabilities   │  ├─ Lasso Regression         │
│                           │  └─ Random Forest            │
├─────────────────────────────────────────────────────────────┤
│  📋 Reporting             │  🔄 Pipeline Management      │
│  ├─ HTML Reports          │  ├─ Configuration Management │
│  ├─ JSON Exports          │  ├─ Memory Optimization      │
│  ├─ Summary Reports       │  ├─ Error Handling           │
│  └─ Logging               │  └─ Cleanup                  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Input Data → EDA Analysis → Feature Engineering → Feature Selection → Output
     ↓              ↓              ↓                    ↓           ↓
   Validation   Quality Check   Feature Gen        Optimization  Reports
     ↓              ↓              ↓                    ↓           ↓
   OHLCV Data   Statistics     150+ Features     150 Features   HTML/JSON
```

## 📊 EDA Analysis Capabilities

### 1. Data Quality Assessment
- **Missing Values Analysis**: Identify and quantify missing data
- **Duplicate Detection**: Find and analyze duplicate records
- **Data Type Analysis**: Understand column types and distributions
- **Outlier Detection**: Statistical and ML-based outlier identification

### 2. Statistical Analysis
- **Descriptive Statistics**: Mean, median, standard deviation, percentiles
- **Distribution Analysis**: Skewness, kurtosis, normality tests
- **Time Series Analysis**: Trends, seasonality, stationarity
- **Correlation Analysis**: Pearson, Spearman, high-correlation pairs

### 3. Data Validation
- **Format Validation**: Ensure OHLCV structure
- **Range Validation**: Check for logical price/volume ranges
- **Consistency Checks**: Validate time series continuity
- **Business Rules**: Apply domain-specific validation rules

## ⚙️ Feature Engineering System

### 1. Proprietary Features
- **PHLD Indicators**: High-Low Direction prediction features
- **Wave Indicators**: Wave pattern recognition features
- **Derivative Features**: Rate of change and acceleration
- **Interaction Features**: Cross-indicator relationships

### 2. Technical Indicators
- **Moving Averages**: SMA, EMA, WMA with multiple periods
- **Momentum Indicators**: RSI, MACD, Stochastic, CCI
- **Volatility Indicators**: ATR, Bollinger Bands, VWAP
- **Volume Indicators**: OBV, Volume SMA ratios
- **Trend Indicators**: ADX, SAR, SuperTrend

### 3. Statistical Features
- **Central Tendency**: Mean, median, mode, geometric mean
- **Dispersion**: Standard deviation, variance, range, IQR
- **Distribution**: Skewness, kurtosis, percentiles
- **Outlier Detection**: Z-score, IQR-based methods
- **Correlation Features**: Rolling correlations, lagged relationships

### 4. Temporal Features
- **Time Components**: Hour, minute, second, day of week
- **Seasonal Patterns**: Monthly, quarterly, yearly cycles
- **Business Hours**: Market open/close indicators
- **Cyclical Encoding**: Sine/cosine transformations
- **Holiday Effects**: Market holiday indicators

### 5. Cross-Timeframe Features
- **Price Ratios**: Short vs long-term price relationships
- **Momentum Ratios**: Acceleration and deceleration patterns
- **Volatility Ratios**: Risk-adjusted measures
- **Volume Ratios**: Trading activity patterns
- **Correlation Ratios**: Inter-timeframe relationships

## 🎯 Feature Selection & Optimization

### Selection Methods
1. **Correlation Analysis**: Remove highly correlated features
2. **Importance Scoring**: Rank features by predictive value
3. **Mutual Information**: Measure feature-target relationships
4. **Lasso Regression**: Sparse feature selection
5. **Random Forest**: Tree-based importance ranking

### Optimization Process
```
Initial Features → Correlation Filter → Importance Filter → Final Selection
     (800+)           (600+)            (300+)           (150)
```

### Configuration Options
```python
FeatureSelectionConfig(
    max_features=150,           # Maximum features to keep
    min_importance=0.2,         # Minimum importance threshold
    correlation_threshold=0.95, # Maximum correlation allowed
    methods=['correlation', 'importance', 'mutual_info', 'lasso', 'random_forest']
)
```

## 📈 Usage Examples

### Example 1: Complete Pipeline
```bash
# Run complete analysis
./eda_fe --file data/AAPL.csv --full-pipeline --output-dir reports/

# This will:
# 1. Load AAPL data
# 2. Run EDA analysis (quality, stats, correlation)
# 3. Generate 150+ features
# 4. Select optimal feature set
# 5. Generate comprehensive report
```

### Example 2: EDA Only
```bash
# Run EDA analysis only
./eda_fe --file data/BTC-USD.csv --eda-only

# This will:
# 1. Load Bitcoin data
# 2. Run data quality checks
# 3. Generate basic statistics
# 4. Perform correlation analysis
# 5. Export EDA report
```

### Example 3: Feature Engineering Only
```bash
# Run feature engineering only
./eda_fe --file data/ETH-USD.csv --features-only

# This will:
# 1. Load Ethereum data
# 2. Generate all feature types
# 3. Apply feature selection
# 4. Export feature report
```

### Example 4: Interactive Mode
```bash
# Start interactive system
./nz_interactive --full

# Navigate through menus:
# 1. Load Data → Select your CSV/Parquet file
# 2. EDA Analysis → Run quality checks and statistics
# 3. Feature Engineering → Generate and analyze features
# 4. Export Results → Save reports and data
```

## 🔧 Configuration

### Feature Engineering Configuration
```python
MasterFeatureConfig(
    max_features=150,              # Maximum features to generate
    min_importance=0.2,            # Minimum importance threshold
    correlation_threshold=0.95,    # Maximum correlation allowed
    enable_proprietary=True,       # Enable PHLD/Wave features
    enable_technical=True,         # Enable technical indicators
    enable_statistical=True,       # Enable statistical features
    enable_temporal=True,          # Enable temporal features
    enable_cross_timeframe=True    # Enable cross-timeframe features
)
```

### EDA Configuration
```python
# Data quality thresholds
quality_config = {
    'max_missing_percentage': 5.0,    # Maximum 5% missing values
    'max_duplicate_percentage': 1.0,  # Maximum 1% duplicates
    'min_data_points': 500,           # Minimum rows required
    'required_columns': ['Open', 'High', 'Low', 'Close', 'Volume']
}
```

## 📋 Output & Reports

### Generated Files
1. **HTML Report**: Comprehensive analysis report
2. **JSON Results**: Structured data export
3. **Feature Summary**: Feature importance and categories
4. **Data Export**: Enhanced data with features
5. **Log Files**: Detailed execution logs

### Report Contents
- **Executive Summary**: Key findings and recommendations
- **Data Quality Report**: Issues and fixes applied
- **Statistical Analysis**: Descriptive and inferential statistics
- **Feature Engineering Report**: Features generated and selected
- **Visualization Gallery**: Charts and plots
- **Export Options**: Download links for all outputs

## 🚨 Troubleshooting

### Common Issues

#### 1. Insufficient Data
```bash
Error: "Insufficient data: X rows, need at least 500"
Solution: The system will automatically pad your data to 500 rows
```

#### 2. Memory Issues
```bash
Error: "Memory usage too high"
Solution: Reduce max_features in configuration or use smaller datasets
```

#### 3. Import Errors
```bash
Error: "Module not found"
Solution: Ensure you're running from project root with correct PYTHONPATH
```

#### 4. Data Format Issues
```bash
Error: "Unsupported file format"
Solution: Convert to CSV, Parquet, or Excel format
```

### Performance Optimization
- **Large Datasets**: Use chunked processing
- **Memory Management**: Enable automatic cleanup
- **Parallel Processing**: Use multi-core feature generation
- **Caching**: Enable result caching for repeated runs

## 🔗 Integration with Existing Tools

### EDA Script Integration
```bash
# Use existing EDA script
./eda --data-quality-checks

# Then run integrated pipeline
./eda_fe --file data.csv --full-pipeline
```

### Analysis Script Integration
```bash
# Run existing analysis
./nz demo --rule PHLD

# Then enhance with feature engineering
./eda_fe --file data.csv --features-only
```

### Docker Integration
```bash
# Run in Docker container
docker compose run --rm neozork-hld ./eda_fe --file data.csv --full-pipeline

# Run interactive system in Docker
docker compose run --rm neozork-hld ./nz_interactive --full
```

## 📚 Additional Resources

### Documentation
- [Feature Engineering Guide](feature_engineering_guide.md)
- [ML Module Overview](ml-module-overview.md)
- [Testing Guide](../testing/testing-guide.md)
- [Deployment Guide](../deployment/deployment-guide.md)

### Examples
- [Usage Examples](../examples/usage-examples.md)
- [EDA Examples](../examples/eda-examples.md)
- [Script Examples](../examples/script-examples.md)

### Support
- [Issue Tracker](https://github.com/username/neozork-hld-prediction/issues)
- [Discussions](https://github.com/username/neozork-hld-prediction/discussions)
- [Wiki](https://github.com/username/neozork-hld-prediction/wiki)

---

**Next Steps**: After mastering the integrated EDA and Feature Engineering system, proceed to [ML Model Development](ml_model_development.md) for the next phase of the project.
