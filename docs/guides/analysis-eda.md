# Analysis & EDA Tools

Data analysis and exploratory data analysis utilities.

## Main Analysis Commands

### `run_analysis.py`
Main analysis pipeline:

```bash
# Demo mode
python run_analysis.py demo

# Analyze specific ticker
python run_analysis.py yf -t AAPL --period 1mo

# Process CSV file
python run_analysis.py csv --csv-file data.csv

# Get help
python run_analysis.py --help
```

## EDA (Exploratory Data Analysis)

### Batch EDA Processing
```bash
# Run comprehensive data quality checks
python -m src.eda.eda_batch_check --data-quality-checks

# Fix data issues automatically
python -m src.eda.eda_batch_check --fix-files

# Generate HTML reports
python -m src.eda.eda_batch_check --html-reports
```

### Individual EDA Tools

**Data Quality:**
```bash
python -m src.eda.data_quality
```

**Basic Statistics:**
```bash
python -m src.eda.basic_stats
```

**Correlation Analysis:**
```bash
python -m src.eda.correlation_analysis
```

**Feature Importance:**
```bash
python -m src.eda.feature_importance
```

## Plotting Tools

### Quick Plotting
```bash
# Auto-plot data
python -m src.plotting.fastest_auto_plot data/file.parquet

# Interactive plots
python -m src.plotting.plotly_plot data/file.parquet

# Financial charts
python -m src.plotting.mplfinance_plot data/file.parquet
```

## File Management

### Data Export
```bash
# Export to Parquet
python -m src.export.parquet_export
```

### File Information
```bash
# Get file details
python -m src.eda.file_info data/file.parquet

# Folder statistics
python -m src.eda.folder_stats data/
```

## Common Workflows

1. **Data Quality Check:** `python -m src.eda.eda_batch_check --data-quality-checks`
2. **Fix Issues:** `python -m src.eda.eda_batch_check --fix-files`
3. **Generate Reports:** `python -m src.eda.eda_batch_check --html-reports`
4. **Plot Results:** `python -m src.plotting.fastest_auto_plot`

For detailed debugging: [Debug Scripts](debug-scripts.md)
