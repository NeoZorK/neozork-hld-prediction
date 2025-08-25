# ML Module Usage Instructions

Quick guide to using the NeoZork HLD Prediction ML module and integrated EDA system.

## 🚀 Quick Start Commands

### 1. Integrated Pipeline (Recommended for most users)

```bash
# Complete EDA + Feature Engineering pipeline with single file
python scripts/main/eda_fe --file your_data.csv --full-pipeline

# Complete EDA + Feature Engineering pipeline with multiple files
python scripts/main/eda_fe --folder data/ --full-pipeline

# Complete EDA + Feature Engineering pipeline with files by mask
python scripts/main/eda_fe --folder data/ --mask gbpusd --full-pipeline

# EDA analysis only with single file
python scripts/main/eda_fe --file your_data.csv --eda-only

# Feature engineering only with multiple files
python scripts/main/eda_fe --folder data/ --features-only
```
```

### 2. Interactive System (Best for exploration)

```bash
# Start full interactive system
python scripts/ml/interactive_system.py

# Demo mode
python scripts/ml/interactive_system.py --demo
```

### 3. Direct Scripts (For developers)

```bash
# Feature engineering demo
python scripts/ml/demo_feature_engineering.py

# Integrated pipeline
python scripts/ml/eda_feature_engineering.py --file data.csv --full-pipeline

# Interactive system
python scripts/ml/interactive_system.py

# Test data generation
python scripts/eda/create_test_data.py
```

## 📁 File Structure

```
scripts/
├── main/
│   └── eda_fe                    # EDA + Feature Engineering pipeline
├── ml/
│   ├── eda_feature_engineering.py    # Integrated EDA + Feature Engineering
│   ├── interactive_system.py         # Interactive menu system
│   ├── demo_feature_engineering.py   # Feature engineering demo
│   └── test_system.py                # System testing script
├── eda/
│   └── create_test_data.py           # Test data generation
├── testing/                           # Test execution scripts
├── debug/                             # Debugging utilities
├── mcp/                               # MCP server scripts
├── utilities/                         # Utility scripts
├── analysis/                          # Analysis tools
├── docker/                            # Docker utilities
└── native-container/                  # Native container scripts

src/ml/
├── feature_engineering/          # Feature generation system
│   ├── feature_generator.py      # Main orchestrator
│   ├── proprietary_features.py   # PHLD/Wave indicators
│   ├── technical_features.py     # Technical indicators
│   ├── statistical_features.py   # Statistical features
│   ├── temporal_features.py      # Temporal patterns
│   ├── cross_timeframe_features.py # Multi-timeframe features
│   └── feature_selector.py       # Feature selection & optimization
└── __init__.py                   # Module initialization

docs/ml/
├── index.md                      # Main documentation index
├── eda_integration_guide.md      # EDA integration guide
├── feature_engineering_guide.md  # Feature engineering guide
└── ml-module-overview.md         # Technical overview
```

## 🎯 Common Use Cases

### Use Case 1: First-Time User
```bash
# 1. Start interactive system
python scripts/ml/interactive_system.py

# 2. Follow menu prompts:
#    - Load Data → Choose loading method (single file, folder, or mask)
#    - EDA Analysis → Run quality checks
#    - Feature Engineering → Generate features
#    - Export Results → Save reports
```

### Use Case 2: Batch Processing with Single File
```bash
# 1. Run complete pipeline with single file
python scripts/main/eda_fe --file data/AAPL.csv --full-pipeline --output-dir reports/

# 2. Check results in reports/ directory
ls reports/
# eda_feature_engineering_report.html
# eda_feature_engineering_results.json
```

### Use Case 3: Batch Processing with Multiple Files
```bash
# 1. Run complete pipeline with all files in folder
python scripts/main/eda_fe --folder data/ --full-pipeline --output-dir reports/

# 2. Run complete pipeline with files by mask
python scripts/main/eda_fe --folder data/ --mask gbpusd --full-pipeline --output-dir reports/

# 3. Check results in reports/ directory
ls reports/
# eda_feature_engineering_report.html
# eda_feature_engineering_results.json
```

### Use Case 4: EDA Only
```bash
# Run EDA analysis without feature engineering (single file)
python scripts/main/eda_fe --file data/BTC-USD.csv --eda-only

# Run EDA analysis without feature engineering (multiple files)
python scripts/main/eda_fe --folder data/ --mask btc --eda-only

# This generates:
# - Data quality report
# - Statistical analysis
# - Correlation analysis
# - HTML report
```

### Use Case 5: Feature Engineering Only
```bash
# Generate features from existing clean data (single file)
python scripts/main/eda_fe --file data/ETH-USD.csv --features-only

# Generate features from existing clean data (multiple files)
python scripts/main/eda_fe --folder data/ --mask eth --features-only

# This generates:
# - 150+ engineered features
# - Feature importance ranking
# - Optimized feature set
# - Feature report
```

## 🔧 Configuration Options

### Basic Configuration
```bash
# Use default settings (recommended for most users)
python scripts/main/eda_fe --file data.csv --full-pipeline

# Use default settings with multiple files
python scripts/main/eda_fe --folder data/ --full-pipeline

# Use default settings with files by mask
python scripts/main/eda_fe --folder data/ --mask gbpusd --full-pipeline

# Custom output directory
python scripts/main/eda_fe --file data.csv --full-pipeline --output-dir ./my_reports

# Custom configuration file
python scripts/main/eda_fe --file data.csv --config my_config.json --full-pipeline
```

### Advanced Configuration
```python
# Create custom configuration file: my_config.json
{
    "max_features": 200,
    "min_importance": 0.15,
    "correlation_threshold": 0.90,
    "enable_proprietary": true,
    "enable_technical": true,
    "enable_statistical": true,
    "enable_temporal": true,
    "enable_cross_timeframe": true
}
```

## 📊 Expected Outputs

### Generated Files
1. **HTML Report**: `eda_feature_engineering_report.html`
   - Executive summary
   - Data quality analysis
   - Statistical analysis
   - Feature engineering results
   - Visualizations

2. **JSON Results**: `eda_feature_engineering_results.json`
   - Structured data export
   - Feature importance scores
   - Configuration used
   - Performance metrics

3. **Data Export**: `data_with_features_[timestamp].parquet`
   - Original data + engineered features
   - Ready for ML model training

4. **Summary Report**: `summary_report_[timestamp].txt`
   - Text-based summary
   - Key findings
   - Recommendations

### Console Output
```
================================================================================
EDA FEATURE ENGINEERING INTEGRATED PIPELINE
================================================================================
Input file: data.csv
Output directory: ./reports
Run EDA: True
Run Feature Engineering: True
================================================================================

📁 LOAD DATA
Loading data from: data.csv
Data loaded: 1000 rows × 5 columns
Columns: ['Open', 'High', 'Low', 'Close', 'Volume']

================================================================================
RUNNING DATA QUALITY ANALYSIS
================================================================================
Data Quality Analysis Results:
  - Total missing values: 0
  - Missing percentage: 0.00%
  - Total duplicates: 0
  - Duplicate percentage: 0.00%
  - Numeric columns: 5
  - Categorical columns: 0
  - Datetime columns: 0

✅ Data quality check completed and saved!

================================================================================
RUNNING FEATURE ENGINEERING PIPELINE
================================================================================
  - Generating features...
✅ Feature generation completed!
   Original data: 1000 rows × 5 columns
   Final data: 1000 rows × 155 columns
   Features generated: 150
   Generation time: 45.23 seconds
   Memory usage: 245.8 MB

✅ Pipeline completed successfully!
```

## 🚨 Troubleshooting

### Common Issues & Solutions

#### Issue 1: "File not found"
```bash
Error: File not found: data.csv
Solution: Ensure file exists and use correct path
# Check current directory
ls -la *.csv
# Use absolute path if needed
python scripts/main/eda_fe --file /full/path/to/data.csv --full-pipeline
```

#### Issue 2: "Insufficient data"
```bash
Warning: Data has only 300 rows, minimum recommended is 500
Solution: System automatically pads data to 500 rows
# For better results, use datasets with 500+ rows
```

#### Issue 3: "Memory usage too high"
```bash
Solution: Reduce feature count or use smaller datasets
# Create custom config with fewer features
{
    "max_features": 100,
    "min_importance": 0.3
}
```

#### Issue 4: "Import errors"
```bash
Error: Module not found
Solution: Ensure you're running from project root
# Check current directory
pwd
# Should show: /path/to/neozork-hld-prediction
```

### Performance Tips
- **Large datasets**: Use chunked processing or reduce feature count
- **Memory optimization**: Enable automatic cleanup in configuration
- **Parallel processing**: Use multi-core systems for faster processing
- **Caching**: Results are cached for repeated runs

## 🔗 Integration with Existing Tools

### Existing EDA Script
```bash
# Use existing EDA capabilities
./eda --data-quality-checks

# Then run integrated pipeline
python scripts/main/eda_fe --file data.csv --full-pipeline
```

### Existing Analysis Script
```bash
# Run existing analysis
./nz demo --rule PHLD

# Then enhance with feature engineering
python scripts/main/eda_fe --file data.csv --features-only
```

### Docker Environment
```bash
# Run in Docker container
docker compose run --rm neozork-hld python scripts/main/eda_fe --file data.csv --full-pipeline

# Run interactive system in Docker
docker compose run --rm neozork-hld python scripts/ml/interactive_system.py
```

## 📚 Next Steps

### After Feature Engineering
1. **Review Results**: Check generated reports and feature importance
2. **Validate Features**: Ensure features make sense for your use case
3. **Export Data**: Save enhanced dataset for ML model training
4. **Iterate**: Adjust configuration and regenerate if needed

### ML Model Development (Coming Soon)
- **Phase 2**: XGBoost, LightGBM, LSTM models
- **Phase 3**: Walk Forward Analysis and validation
- **Phase 4**: Risk management and portfolio optimization
- **Phase 5**: Automated training pipelines
- **Phase 6**: Real-time trading deployment

## 💡 Pro Tips

1. **Start Simple**: Use default configuration first, then customize
2. **Data Quality**: Ensure clean OHLCV data for best results
3. **Feature Review**: Always review generated features for relevance
4. **Iterative Process**: Start with EDA, then add feature engineering
5. **Documentation**: Keep track of configurations and results
6. **Testing**: Use test datasets before running on production data

---

**Need Help?** Check the [EDA Integration Guide](eda_integration_guide.md) for detailed information or use the interactive system with `python scripts/ml/interactive_system.py`.
