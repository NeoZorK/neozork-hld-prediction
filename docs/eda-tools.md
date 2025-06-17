# EDA Tools Guide

Exploratory Data Analysis utilities for data quality assessment and statistical analysis.

## Overview

The EDA (Exploratory Data Analysis) tools provide comprehensive data quality checks, statistical analysis, and automated fixing capabilities for Parquet files used in the project.

## Main EDA Tool

### `src/eda/eda_batch_check.py` - Batch EDA Processor
**Purpose:** Comprehensive data quality analysis and automated fixing

## Quick Commands

### Data Quality Checks
```bash
# Run all quality checks
python src/eda/eda_batch_check.py --data-quality-checks

# Or use the shortcut
./eda

# Specific checks
python src/eda/eda_batch_check.py --nan-check --duplicate-check
python src/eda/eda_batch_check.py --gap-check --zero-check
```

### Automated Fixing
```bash
# Fix all detected issues
python src/eda/eda_batch_check.py --fix-files --fix-all

# Fix specific issues
python src/eda/eda_batch_check.py --fix-files --fix-nan --fix-duplicates
python src/eda/eda_batch_check.py --fix-files --fix-zeros --fix-negatives
```

### Statistical Analysis
```bash
# Basic statistics
python src/eda/eda_batch_check.py --basic-stats

# Comprehensive analysis
python src/eda/eda_batch_check.py --all-stats

# Specific analyses
python src/eda/eda_batch_check.py --correlation-analysis --feature-importance
```

## Data Quality Checks

### Available Check Types

#### Missing Values Check (`--nan-check`)
Identifies NaN (Not a Number) values in all columns:
```bash
python src/eda/eda_batch_check.py --nan-check
```
- Reports percentage of missing values per column
- Identifies patterns in missing data
- Suggests appropriate filling strategies

#### Duplicate Check (`--duplicate-check`)
Finds duplicate rows and values:
```bash
python src/eda/eda_batch_check.py --duplicate-check
```
- Detects fully duplicated rows
- Identifies duplicated values in string columns
- Reports impact on data quality

#### Gap Check (`--gap-check`)
Detects gaps in time series data:
```bash
python src/eda/eda_batch_check.py --gap-check
```
- Finds abnormally large intervals in datetime columns
- Identifies missing time periods
- Reports data continuity issues

#### Zero Values Check (`--zero-check`)
Finds anomalous zero values:
```bash
python src/eda/eda_batch_check.py --zero-check
```
- Detects zero values in price/volume columns
- Uses heuristics to identify anomalies
- Reports potential data corruption

#### Negative Values Check (`--negative-check`)
Identifies negative values where they shouldn't exist:
```bash
python src/eda/eda_batch_check.py --negative-check
```
- Checks OHLCV columns for negative values
- Validates datetime columns
- Reports data integrity issues

#### Infinity Check (`--inf-check`)
Finds infinite values:
```bash
python src/eda/eda_batch_check.py --inf-check
```
- Detects +inf and -inf values
- Identifies calculation errors
- Reports numerical instability

### Comprehensive Quality Check
Run all checks at once:
```bash
python src/eda/eda_batch_check.py --data-quality-checks
# Equivalent to: --nan-check --duplicate-check --gap-check --zero-check --negative-check --inf-check
```

## Automated Data Fixing

### Fix Strategies

#### NaN Fixing (`--fix-nan`)
```bash
python src/eda/eda_batch_check.py --fix-files --fix-nan
```
**Strategy:**
- Numeric columns: Fill with median
- String columns: Fill with mode
- Datetime columns: Interpolate
- Boolean columns: Fill with mode

#### Duplicate Fixing (`--fix-duplicates`)
```bash
python src/eda/eda_batch_check.py --fix-files --fix-duplicates
```
**Strategy:**
- Remove fully duplicated rows
- Keep first occurrence
- Preserve data order

#### Gap Fixing (`--fix-gaps`)
```bash
python src/eda/eda_batch_check.py --fix-files --fix-gaps
```
**Strategy:**
- Interpolate missing time periods
- Reindex time series
- Fill gaps with appropriate values

#### Zero Fixing (`--fix-zeros`)
```bash
python src/eda/eda_batch_check.py --fix-files --fix-zeros
```
**Strategy:**
- Replace anomalous zeros in price columns
- Use interpolation for OHLCV data
- Preserve legitimate zero values

#### Negative Fixing (`--fix-negatives`)
```bash
python src/eda/eda_batch_check.py --fix-files --fix-negatives
```
**Strategy:**
- Convert to absolute values for price data
- Handle based on column type
- Log transformations for appropriate cases

#### Infinity Fixing (`--fix-infs`)
```bash
python src/eda/eda_batch_check.py --fix-files --fix-infs
```
**Strategy:**
- Replace with finite values
- Use column-specific limits
- Preserve data distribution

### Safety Features
- **Automatic backups:** Original files saved with `.bak` extension
- **Restore capability:** `--restore-backups` flag
- **Validation:** Post-fix integrity checks

### Backup Management
```bash
# Restore original files
python src/eda/eda_batch_check.py --restore-backups

# Manual backup check
ls data/**/*.bak
```

## Statistical Analysis

### Basic Statistics (`--basic-stats`)
```bash
python src/eda/eda_batch_check.py --basic-stats
```
**Provides:**
- File sizes and row counts
- Column types and memory usage
- Data date ranges
- Basic descriptive statistics

### Descriptive Statistics (`--descriptive-stats`)
```bash
python src/eda/eda_batch_check.py --descriptive-stats
```
**Detailed metrics:**
- Mean, median, mode
- Standard deviation, variance
- Min, max, quartiles
- Skewness, kurtosis

### Distribution Analysis (`--distribution-analysis`)
```bash
python src/eda/eda_batch_check.py --distribution-analysis
```
**Analyzes:**
- Data distributions
- Normality tests
- Skewness and kurtosis
- Distribution fitting

### Outlier Analysis (`--outlier-analysis`)
```bash
python src/eda/eda_batch_check.py --outlier-analysis
```
**Methods:**
- IQR (Interquartile Range) method
- Z-score method
- Modified Z-score
- Isolation Forest

### Time Series Analysis (`--time-series-analysis`)
```bash
python src/eda/eda_batch_check.py --time-series-analysis
```
**Features:**
- Trend analysis
- Seasonality detection
- Stationarity tests
- Autocorrelation analysis

### Correlation Analysis (`--correlation-analysis`)
```bash
python src/eda/eda_batch_check.py --correlation-analysis
```
**Provides:**
- Correlation matrices
- Feature correlation with targets
- Multicollinearity detection
- Correlation significance tests

### Feature Importance (`--feature-importance`)
```bash
python src/eda/eda_batch_check.py --feature-importance
```
**Analysis:**
- Mutual information scores
- Random forest importance
- Correlation-based ranking
- Variance analysis

### Comprehensive Analysis
```bash
python src/eda/eda_batch_check.py --all-stats
# Runs all statistical analyses
```

## File-Specific Analysis

### Single File Analysis
```bash
# Analyze specific file
python src/eda/eda_batch_check.py --file mydata.parquet --basic-stats
python src/eda/eda_batch_check.py --file mydata.parquet --correlation-analysis

# Fix specific file
python src/eda/eda_batch_check.py --file mydata.parquet --fix-files --fix-duplicates
```

## Output and Reporting

### Console Output
- Color-coded results
- Progress bars for long operations
- Summary statistics
- Recommendation suggestions

### Log Files
Analysis results are saved to `logs/` directory:
```
logs/
├── eda_basic_stats.log
├── eda_correlation.log
├── eda_quality_checks.log
└── eda_feature_importance.log
```

### HTML Reports
Detailed HTML reports are generated for comprehensive analyses:
```
logs/html_reports/
├── correlation_analysis/
├── feature_importance/
├── outlier_analysis/
└── time_series_analysis/
```

### Cleanup Commands
```bash
# Remove log files
python src/eda/eda_batch_check.py --clean-stats-logs

# Remove HTML reports
python src/eda/eda_batch_check.py --clean-reports
```

## Advanced Usage

### Batch Processing Workflow
```bash
# 1. Check data quality
python src/eda/eda_batch_check.py --data-quality-checks

# 2. Fix issues
python src/eda/eda_batch_check.py --fix-files --fix-all

# 3. Comprehensive analysis
python src/eda/eda_batch_check.py --all-stats

# 4. Generate reports
python src/eda/eda_batch_check.py --correlation-analysis --feature-importance
```

### Integration with Analysis Pipeline
```bash
# Before running main analysis
python src/eda/eda_batch_check.py --data-quality-checks --fix-files --fix-all

# Run main analysis
python run_analysis.py yf -t AAPL --period 1mo --point 0.01

# Post-analysis validation
python src/eda/eda_batch_check.py --basic-stats
```

## Performance Considerations

### Memory Efficiency
- Processes files one at a time
- Streaming operations for large files
- Automatic memory cleanup

### Processing Speed
- Optimized pandas operations
- Parallel processing where applicable
- Progress tracking for long operations

### Storage Impact
- Backup files created before modifications
- Compressed Parquet format maintained
- Minimal storage overhead

## Best Practices

### Regular Data Quality Checks
1. **Run quality checks** before analysis
2. **Fix issues** systematically
3. **Validate fixes** with post-processing checks
4. **Monitor trends** in data quality over time

### Workflow Integration
1. **Automate checks** in data pipelines
2. **Set quality thresholds** for acceptance
3. **Document issues** and resolutions
4. **Version control** data quality reports

### Troubleshooting
1. **Check backup files** if issues arise
2. **Review logs** for detailed error information
3. **Use single-file mode** for debugging
4. **Restore from backups** if needed
