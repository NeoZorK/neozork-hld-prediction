# EDA (Exploratory Data Analysis) Examples

Examples for exploratory data analysis with the project.

## Overview

The project includes comprehensive EDA capabilities for:

- **Data Quality Analysis** - Validate and clean data
- **Statistical Analysis** - Basic statistics and distributions
- **Correlation Analysis** - Feature relationships and dependencies
- **Feature Importance** - Identify key predictive features
- **Data Visualization** - Interactive and static plots
- **Automated EDA** - Batch processing and reporting

## Basic EDA

### Run EDA Script
```bash
# Run EDA script
bash eda

# EDA with UV
uv run ./eda

# EDA with verbose output
bash eda --verbose

# EDA with export results
bash eda --export-results

# EDA with specific data file
bash eda --file data.csv
```

### EDA in Docker
```bash
# Run EDA in container
docker compose run --rm neozork-hld bash eda

# EDA with UV in container
docker compose run --rm neozork-hld uv run ./eda

# EDA with data mounting
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld bash eda

# EDA with results mounting
docker compose run --rm -v $(pwd)/results:/app/results neozork-hld bash eda --export-results
```

## Data Quality Analysis

### Basic Data Quality
```bash
# Run data quality analysis
python -m src.eda.data_quality

# Data quality with specific file
python -m src.eda.data_quality --file data.csv

# Data quality with output
python -m src.eda.data_quality --output quality_report.txt

# Data quality with verbose output
python -m src.eda.data_quality --verbose
```

### Data Quality Tests
```bash
# Test data quality
python -m pytest tests/eda/test_data_quality.py -v

# Test with specific data
python -m pytest tests/eda/test_data_quality.py::test_missing_values -v

# Test with coverage
python -m pytest tests/eda/test_data_quality.py --cov=src.eda --cov-report=html
```

### Data Validation
```bash
# Validate data structure
python -m src.eda.data_validation

# Validate with schema
python -m src.eda.data_validation --schema schema.json

# Validate with rules
python -m src.eda.data_validation --rules strict

# Validate with output
python -m src.eda.data_validation --output validation_report.txt
```

## Statistical Analysis

### Basic Statistics
```bash
# Run basic statistics
python -m src.eda.basic_stats

# Basic stats with specific file
python -m src.eda.basic_stats --file data.csv

# Basic stats with output
python -m src.eda.basic_stats --output stats_report.txt

# Basic stats with specific columns
python -m src.eda.basic_stats --columns open,high,low,close,volume
```

### Statistical Tests
```bash
# Run statistical tests
python -m src.eda.statistical_tests

# Tests with specific data
python -m src.eda.statistical_tests --file data.csv

# Tests with output
python -m src.eda.statistical_tests --output tests_report.txt

# Tests with specific tests
python -m src.eda.statistical_tests --tests normality,stationarity
```

### Distribution Analysis
```bash
# Analyze distributions
python -m src.eda.distribution_analysis

# Distribution with specific file
python -m src.eda.distribution_analysis --file data.csv

# Distribution with plots
python -m src.eda.distribution_analysis --plots

# Distribution with output
python -m src.eda.distribution_analysis --output distribution_report.txt
```

## Correlation Analysis

### Basic Correlation
```bash
# Run correlation analysis
python -m src.eda.correlation_analysis

# Correlation with specific file
python -m src.eda.correlation_analysis --file data.csv

# Correlation with output
python -m src.eda.correlation_analysis --output correlation_report.txt

# Correlation with plots
python -m src.eda.correlation_analysis --plots
```

### Advanced Correlation
```bash
# Run advanced correlation
python -m src.eda.advanced_correlation

# Advanced correlation with specific file
python -m src.eda.advanced_correlation --file data.csv

# Advanced correlation with methods
python -m src.eda.advanced_correlation --methods pearson,spearman,kendall

# Advanced correlation with output
python -m src.eda.advanced_correlation --output advanced_correlation_report.txt
```

### Correlation Tests
```bash
# Test correlation analysis
python -m pytest tests/eda/test_correlation_analysis.py -v

# Test with specific data
python -m pytest tests/eda/test_correlation_analysis.py::test_pearson_correlation -v

# Test with coverage
python -m pytest tests/eda/test_correlation_analysis.py --cov=src.eda --cov-report=html
```

## Feature Importance

### Feature Importance Analysis
```bash
# Run feature importance analysis
python -m src.eda.feature_importance

# Feature importance with specific file
python -m src.eda.feature_importance --file data.csv

# Feature importance with target
python -m src.eda.feature_importance --target close

# Feature importance with methods
python -m src.eda.feature_importance --methods mutual_info,correlation,random_forest
```

### Feature Selection
```bash
# Run feature selection
python -m src.eda.feature_selection

# Feature selection with specific file
python -m src.eda.feature_selection --file data.csv

# Feature selection with target
python -m src.eda.feature_selection --target close

# Feature selection with output
python -m src.eda.feature_selection --output selected_features.txt
```

### Feature Engineering
```bash
# Run feature engineering
python -m src.eda.feature_engineering

# Feature engineering with specific file
python -m src.eda.feature_engineering --file data.csv

# Feature engineering with methods
python -m src.eda.feature_engineering --methods technical_indicators,time_features

# Feature engineering with output
python -m src.eda.feature_engineering --output engineered_features.csv
```

## Data Visualization

### Basic Visualization
```bash
# Run basic visualization
python -m src.eda.basic_visualization

# Basic visualization with specific file
python -m src.eda.basic_visualization --file data.csv

# Basic visualization with plots
python -m src.eda.basic_visualization --plots

# Basic visualization with output
python -m src.eda.basic_visualization --output plots/
```

### Advanced Visualization
```bash
# Run advanced visualization
python -m src.eda.advanced_visualization

# Advanced visualization with specific file
python -m src.eda.advanced_visualization --file data.csv

# Advanced visualization with plots
python -m src.eda.advanced_visualization --plots

# Advanced visualization with output
python -m src.eda.advanced_visualization --output advanced_plots/
```

### Interactive Visualization
```bash
# Run interactive visualization
python -m src.eda.interactive_visualization

# Interactive visualization with specific file
python -m src.eda.interactive_visualization --file data.csv

# Interactive visualization with backend
python -m src.eda.interactive_visualization --backend plotly

# Interactive visualization with output
python -m src.eda.interactive_visualization --output interactive_plots/
```

## Automated EDA

### Batch EDA Processing
```bash
# Run batch EDA processing
python -m src.eda.eda_batch_check

# Batch processing with directory
python -m src.eda.eda_batch_check --directory data/

# Batch processing with pattern
python -m src.eda.eda_batch_check --pattern "*.csv"

# Batch processing with output
python -m src.eda.eda_batch_check --output batch_eda_report.txt
```

### Automated Reports
```bash
# Generate automated EDA report
python -m src.eda.automated_report

# Automated report with specific file
python -m src.eda.automated_report --file data.csv

# Automated report with template
python -m src.eda.automated_report --template comprehensive

# Automated report with output
python -m src.eda.automated_report --output eda_report.html
```

### EDA Pipeline
```bash
# Run EDA pipeline
python -m src.eda.eda_pipeline

# EDA pipeline with specific file
python -m src.eda.eda_pipeline --file data.csv

# EDA pipeline with steps
python -m src.eda.eda_pipeline --steps quality,stats,correlation,importance

# EDA pipeline with output
python -m src.eda.eda_pipeline --output pipeline_report.txt
```

## Time Series Analysis

### Time Series EDA
```bash
# Run time series EDA
python -m src.eda.time_series_eda

# Time series EDA with specific file
python -m src.eda.time_series_eda --file data.csv

# Time series EDA with date column
python -m src.eda.time_series_eda --date-column date

# Time series EDA with output
python -m src.eda.time_series_eda --output time_series_report.txt
```

### Seasonality Analysis
```bash
# Run seasonality analysis
python -m src.eda.seasonality_analysis

# Seasonality analysis with specific file
python -m src.eda.seasonality_analysis --file data.csv

# Seasonality analysis with periods
python -m src.eda.seasonality_analysis --periods daily,weekly,monthly

# Seasonality analysis with output
python -m src.eda.seasonality_analysis --output seasonality_report.txt
```

### Trend Analysis
```bash
# Run trend analysis
python -m src.eda.trend_analysis

# Trend analysis with specific file
python -m src.eda.trend_analysis --file data.csv

# Trend analysis with methods
python -m src.eda.trend_analysis --methods linear,polynomial,moving_average

# Trend analysis with output
python -m src.eda.trend_analysis --output trend_report.txt
```

## Financial Data Analysis

### Financial EDA
```bash
# Run financial EDA
python -m src.eda.financial_eda

# Financial EDA with specific file
python -m src.eda.financial_eda --file data.csv

# Financial EDA with indicators
python -m src.eda.financial_eda --indicators rsi,macd,bb

# Financial EDA with output
python -m src.eda.financial_eda --output financial_report.txt
```

### Volatility Analysis
```bash
# Run volatility analysis
python -m src.eda.volatility_analysis

# Volatility analysis with specific file
python -m src.eda.volatility_analysis --file data.csv

# Volatility analysis with methods
python -m src.eda.volatility_analysis --methods garch,ewma,rolling

# Volatility analysis with output
python -m src.eda.volatility_analysis --output volatility_report.txt
```

### Returns Analysis
```bash
# Run returns analysis
python -m src.eda.returns_analysis

# Returns analysis with specific file
python -m src.eda.returns_analysis --file data.csv

# Returns analysis with methods
python -m src.eda.returns_analysis --methods simple,log,adjusted

# Returns analysis with output
python -m src.eda.returns_analysis --output returns_report.txt
```

## Performance Analysis

### EDA Performance
```bash
# Run EDA performance analysis
python -m src.eda.performance_analysis

# Performance analysis with specific file
python -m src.eda.performance_analysis --file data.csv

# Performance analysis with metrics
python -m src.eda.performance_analysis --metrics execution_time,memory_usage

# Performance analysis with output
python -m src.eda.performance_analysis --output performance_report.txt
```

### Benchmarking
```bash
# Run EDA benchmarking
python -m src.eda.benchmarking

# Benchmarking with specific file
python -m src.eda.benchmarking --file data.csv

# Benchmarking with methods
python -m src.eda.benchmarking --methods pandas,numpy,polars

# Benchmarking with output
python -m src.eda.benchmarking --output benchmark_report.txt
```

## Testing EDA

### EDA Tests
```bash
# Run EDA tests
python -m pytest tests/eda/ -v

# Test basic stats
python -m pytest tests/eda/test_basic_stats.py -v

# Test correlation analysis
python -m pytest tests/eda/test_correlation_analysis.py -v

# Test feature importance
python -m pytest tests/eda/test_feature_importance.py -v

# Test with coverage
python -m pytest tests/eda/ --cov=src.eda --cov-report=html
```

### EDA Script Tests
```bash
# Test EDA script
python -m pytest tests/scripts/test_eda_script.py -v

# Test init directories
python -m pytest tests/scripts/test_init_dirs.bats -v
```

## Integration with Analysis

### EDA with Analysis
```bash
# Run EDA with analysis
python run_analysis.py demo --eda

# EDA with specific indicator
python run_analysis.py demo --rule RSI --eda

# EDA with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --eda

# EDA with export
python run_analysis.py demo --eda --export-results
```

### EDA Workflow
```bash
# Complete EDA workflow
# 1. Load data
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 2. Run EDA
bash eda

# 3. Analyze with indicators
python run_analysis.py show yf AAPL --rule RSI --export-parquet

# 4. Generate EDA report
python -m src.eda.automated_report --file data/AAPL.parquet
```

## Troubleshooting

### Common EDA Issues
```bash
# Issue: Data loading problems
python scripts/debug_scripts/debug_check_parquet.py

# Issue: Memory problems
python scripts/debug_scripts/debug_system_resources.py --memory

# Issue: Performance problems
python -m src.eda.performance_analysis --file data.csv

# Issue: Visualization problems
python scripts/debug_scripts/debug_plotting.py --backend plotly
```

### EDA Debug Mode
```bash
# Enable EDA debug mode
export EDA_DEBUG=1
bash eda

# Run with verbose output
bash eda --verbose

# Run with debug logging
python -m src.eda.basic_stats --debug
```

---

📚 **Additional Resources:**
- **[Usage Examples](usage-examples.md)** - Comprehensive usage examples
- **[Quick Examples](quick-examples.md)** - Fast start examples
- **[Indicator Examples](indicator-examples.md)** - Technical indicator examples
- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Testing Examples](testing-examples.md)** - Testing examples
- **[Script Examples](script-examples.md)** - Utility script examples
- **[Docker Examples](docker-examples.md)** - Docker examples 