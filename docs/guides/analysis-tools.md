# Analysis Tools Guide

Complete guide to Exploratory Data Analysis (EDA) and analysis tools in the Neozork HLD Prediction project.

## Overview

The EDA module provides comprehensive tools for data exploration, quality assessment, statistical analysis, and automated reporting.

## Core Analysis Components

### 1. Basic Statistics (`basic_stats.py`)

Comprehensive statistical analysis of financial data.

#### Features
- **Descriptive statistics** - Mean, median, standard deviation, percentiles
- **Distribution analysis** - Histograms, probability plots, skewness, kurtosis
- **Time series analysis** - Trends, seasonality, stationarity tests
- **Correlation analysis** - Price correlations, indicator relationships
- **Volatility analysis** - Rolling volatility, GARCH models
- **Return analysis** - Log returns, cumulative returns, drawdowns

#### Usage Example

```python
from src.batch_eda.basic_stats import BasicStatsAnalyzer

# Initialize analyzer
analyzer = BasicStatsAnalyzer()

# Comprehensive analysis
results = analyzer.analyze_data(
    data=price_data,
    indicators={'rsi': rsi_data, 'macd': macd_data},
    analysis_types=['descriptive', 'distribution', 'correlation', 'volatility']
)

# Print summary
analyzer.print_summary(results)

# Generate detailed report
analyzer.generate_report(results, output_path='reports/basic_stats_report.html')
```

#### Analysis Types
- **`descriptive`** - Basic descriptive statistics
- **`distribution`** - Distribution analysis and normality tests
- **`correlation`** - Correlation matrices and heatmaps
- **`volatility`** - Volatility analysis and modeling
- **`returns`** - Return analysis and risk metrics
- **`trends`** - Trend analysis and decomposition

### 2. Data Quality Assessment (`data_quality.py`)

Comprehensive data quality analysis and validation.

#### Features
- **Missing data analysis** - Identify and quantify missing values
- **Outlier detection** - Statistical and ML-based outlier detection
- **Data consistency** - Check for logical inconsistencies
- **Format validation** - Validate data types and formats
- **Range validation** - Check for reasonable value ranges
- **Time series validation** - Validate chronological order and gaps

#### Usage Example

```python
from src.batch_eda.data_quality import DataQualityAnalyzer

# Initialize analyzer
analyzer = DataQualityAnalyzer()

# Comprehensive quality check
quality_report = analyzer.analyze_quality(
    data=price_data,
    checks=['missing', 'outliers', 'consistency', 'format', 'range', 'timeline']
)

# Print quality summary
analyzer.print_quality_summary(quality_report)

# Generate quality report
analyzer.generate_quality_report(quality_report, output_path='reports/quality_report.html')

# Fix common issues
cleaned_data = analyzer.fix_common_issues(data=price_data, report=quality_report)
```

#### Quality Checks
- **`missing`** - Missing value analysis
- **`outliers`** - Outlier detection and analysis
- **`consistency`** - Logical consistency checks
- **`format`** - Data format validation
- **`range`** - Value range validation
- **`timeline`** - Time series validation

### 3. Correlation Analysis (`correlation_analysis.py`)

Advanced correlation and relationship analysis.

#### Features
- **Pearson correlation** - Linear correlation analysis
- **Spearman correlation** - Rank-based correlation
- **Kendall correlation** - Ordinal correlation
- **Cross-correlation** - Time-lagged correlations
- **Correlation networks** - Network analysis of correlations
- **Correlation stability** - Time-varying correlation analysis

#### Usage Example

```python
from src.batch_eda.correlation_analysis import CorrelationAnalyzer

# Initialize analyzer
analyzer = CorrelationAnalyzer()

# Comprehensive correlation analysis
correlation_results = analyzer.analyze_correlations(
    data=price_data,
    indicators={'rsi': rsi_data, 'macd': macd_data},
    methods=['pearson', 'spearman', 'kendall'],
    include_lags=True,
    max_lag=10
)

# Generate correlation heatmap
analyzer.plot_correlation_heatmap(
    correlation_results,
    output_path='plots/correlation_heatmap.png'
)

# Analyze correlation stability
stability_analysis = analyzer.analyze_correlation_stability(
    data=price_data,
    window_size=252,  # 1 year
    step_size=21      # 1 month
)
```

### 4. Feature Importance (`feature_importance.py`)

Feature importance and selection analysis.

#### Features
- **Statistical importance** - Statistical significance tests
- **ML-based importance** - Random Forest, XGBoost importance
- **Information gain** - Mutual information analysis
- **Feature selection** - Automated feature selection
- **Importance stability** - Cross-validation importance
- **Feature interactions** - Interaction analysis

#### Usage Example

```python
from src.batch_eda.feature_importance import FeatureImportanceAnalyzer

# Initialize analyzer
analyzer = FeatureImportanceAnalyzer()

# Analyze feature importance
importance_results = analyzer.analyze_importance(
    features=indicator_data,
    target=price_data['close'],
    methods=['statistical', 'random_forest', 'xgboost', 'mutual_info']
)

# Generate importance plot
analyzer.plot_importance(
    importance_results,
    output_path='plots/feature_importance.png'
)

# Select top features
top_features = analyzer.select_top_features(
    importance_results,
    n_features=10,
    method='random_forest'
)
```

## Advanced Analysis Tools

### 1. Batch Analysis (`eda_batch_check.py`)

Automated batch processing for multiple datasets.

#### Features
- **Batch processing** - Process multiple files/datasets
- **Parallel execution** - Multi-threaded analysis
- **Progress tracking** - Real-time progress monitoring
- **Error handling** - Robust error management
- **Summary reports** - Consolidated batch reports

#### Usage Example

```python
from src.batch_eda.eda_batch_check import BatchAnalyzer

# Initialize batch analyzer
batch_analyzer = BatchAnalyzer()

# Analyze multiple files
results = batch_analyzer.analyze_batch(
    file_pattern='data/*.csv',
    analysis_types=['basic_stats', 'quality', 'correlation'],
    parallel=True,
    max_workers=4
)

# Generate batch report
batch_analyzer.generate_batch_report(
    results,
    output_path='reports/batch_analysis_report.html'
)
```

### 2. HTML Report Generator (`html_report_generator.py`)

Professional HTML report generation.

#### Features
- **Interactive reports** - Interactive HTML reports
- **Multiple sections** - Comprehensive report sections
- **Customizable templates** - Custom report templates
- **Export options** - PDF, HTML, email export
- **Embedded plots** - Interactive charts and graphs

#### Usage Example

```python
from src.batch_eda.html_report_generator import HTMLReportGenerator

# Initialize generator
generator = HTMLReportGenerator()

# Generate comprehensive report
generator.generate_report(
    data=price_data,
    indicators=indicator_data,
    analysis_results=analysis_results,
    output_path='reports/comprehensive_analysis.html',
    template='financial_analysis',
    include_plots=True,
    interactive=True
)
```

### 3. Statistics Logger (`stats_logger.py`)

Comprehensive statistics logging and tracking.

#### Features
- **Time series logging** - Track statistics over time
- **Multiple metrics** - Various statistical metrics
- **Database storage** - Store results in database
- **Trend analysis** - Analyze metric trends
- **Alerting** - Statistical alerts and notifications

#### Usage Example

```python
from src.batch_eda.stats_logger import StatsLogger

# Initialize logger
logger = StatsLogger()

# Log daily statistics
logger.log_daily_stats(
    data=price_data,
    indicators=indicator_data,
    date=datetime.now().date()
)

# Analyze trends
trends = logger.analyze_trends(
    metric='volatility',
    period='30d',
    threshold=0.05
)

# Generate trend report
logger.generate_trend_report(trends, output_path='reports/trend_analysis.html')
```

## CLI Integration

### EDA Commands

```bash
# Basic statistics analysis
python -m src.eda.basic_stats --data data/aapl.csv --output reports/basic_stats.html

# Data quality analysis
python -m src.eda.data_quality --data data/aapl.csv --output reports/quality_report.html

# Correlation analysis
python -m src.eda.correlation_analysis --data data/aapl.csv --indicators rsi,macd --output plots/correlation.png

# Batch analysis
python -m src.eda.eda_batch_check --pattern "data/*.csv" --output reports/batch_report.html

# Feature importance
python -m src.eda.feature_importance --features data/indicators.csv --target data/prices.csv --output plots/importance.png
```

### CLI Options

- **`--data`** - Input data file
- **`--indicators`** - Indicator data files
- **`--output`** - Output file path
- **`--analysis-types`** - Types of analysis to perform
- **`--parallel`** - Enable parallel processing
- **`--template`** - Report template to use

## Analysis Workflows

### 1. Complete EDA Workflow

```python
from src.batch_eda.basic_stats import BasicStatsAnalyzer
from src.batch_eda.data_quality import DataQualityAnalyzer
from src.batch_eda.correlation_analysis import CorrelationAnalyzer
from src.batch_eda.html_report_generator import HTMLReportGenerator

# Load data
data = load_data('data/aapl.csv')
indicators = load_indicators('data/indicators.csv')

# Data quality check
quality_analyzer = DataQualityAnalyzer()
quality_report = quality_analyzer.analyze_quality(data)

# Basic statistics
stats_analyzer = BasicStatsAnalyzer()
stats_results = stats_analyzer.analyze_data(data, indicators)

# Correlation analysis
corr_analyzer = CorrelationAnalyzer()
corr_results = corr_analyzer.analyze_correlations(data, indicators)

# Generate comprehensive report
report_generator = HTMLReportGenerator()
report_generator.generate_report(
    data=data,
    indicators=indicators,
    analysis_results={
        'quality': quality_report,
        'statistics': stats_results,
        'correlation': corr_results
    },
    output_path='reports/complete_eda.html'
)
```

### 2. Automated Analysis Pipeline

```python
from src.batch_eda.eda_batch_check import BatchAnalyzer

# Automated pipeline
pipeline = BatchAnalyzer()

# Run complete analysis pipeline
results = pipeline.run_pipeline(
    data_sources=['yfinance', 'csv', 'binance'],
    symbols=['AAPL', 'GOOGL', 'MSFT'],
    analysis_types=['quality', 'statistics', 'correlation', 'importance'],
    output_dir='reports/automated/',
    parallel=True
)
```

### 3. Real-time Analysis

```python
import time
from src.batch_eda.stats_logger import StatsLogger

# Real-time monitoring
logger = StatsLogger()

while True:
    # Fetch latest data
    data = fetch_latest_data('AAPL')
    
    # Log statistics
    logger.log_daily_stats(data)
    
    # Check for anomalies
    anomalies = logger.check_anomalies(data)
    if anomalies:
        send_alert(anomalies)
    
    # Wait for next update
    time.sleep(3600)  # Update every hour
```

## Report Templates

### Available Templates

1. **`financial_analysis`** - Complete financial analysis report
2. **`data_quality`** - Data quality assessment report
3. **`correlation_analysis`** - Correlation analysis report
4. **`feature_importance`** - Feature importance report
5. **`batch_summary`** - Batch analysis summary report

### Custom Templates

```python
# Custom template
custom_template = {
    'title': 'Custom Analysis Report',
    'sections': [
        'executive_summary',
        'data_overview',
        'quality_assessment',
        'statistical_analysis',
        'correlation_analysis',
        'recommendations'
    ],
    'style': 'dark',
    'interactive': True
}

# Use custom template
generator.generate_report(
    data=data,
    template=custom_template,
    output_path='reports/custom_analysis.html'
)
```

## Performance Optimization

### Analysis Performance Tips

1. **Use appropriate methods** - Choose efficient analysis methods
2. **Parallel processing** - Enable parallel execution for large datasets
3. **Sampling** - Use sampling for very large datasets
4. **Caching** - Cache intermediate results

### Performance Configuration

```python
# Performance-optimized analysis
config = {
    'parallel': True,
    'max_workers': 4,
    'chunk_size': 10000,
    'use_sampling': True,
    'sample_size': 10000,
    'cache_results': True
}

analyzer = BasicStatsAnalyzer(config=config)
```

## Error Handling

### Analysis Error Recovery

```python
from src.batch_eda.basic_stats import BasicStatsAnalyzer

try:
    analyzer = BasicStatsAnalyzer()
    results = analyzer.analyze_data(data=price_data)
except ValueError as e:
    print(f"Data validation error: {e}")
    # Clean and validate data
except MemoryError as e:
    print(f"Memory error: {e}")
    # Use sampling or chunking
except Exception as e:
    print(f"Unexpected error: {e}")
    # Log error and continue
```

## Testing

### Analysis Testing

```bash
# Run EDA tests
pytest tests/eda/ -v

# Test specific components
pytest tests/eda/test_basic_stats.py -v
pytest tests/eda/test_data_quality.py -v
pytest tests/eda/test_correlation_analysis.py -v

# Test performance
pytest tests/eda/test_performance.py -v
```

### Report Testing

```bash
# Test report generation
pytest tests/eda/test_html_report_generator.py -v

# Test batch processing
pytest tests/eda/test_eda_batch_check.py -v
```

## Related Documentation

- **[Data Sources](../api/data-sources.md)** - Data acquisition
- **[Core Calculations](../reference/core-calculation.md)** - Data processing
- **[Plotting and Visualization](plotting-visualization.md)** - Visualization tools
- **[Export Functions](export-functions.md)** - Data export capabilities 