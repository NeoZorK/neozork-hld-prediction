# Time Series Gap Fixing

## Overview

The NeoZorK HLD Prediction system now includes automatic time series gap fixing functionality that runs before data combination during the "Load Data" process. This feature helps ensure data quality and consistency by detecting and fixing gaps in time series data.

## What are Time Series Gaps?

Time series gaps occur when there are missing data points in a time series. Common causes include:

- **Market holidays** - When markets are closed
- **Data collection issues** - Network problems, system failures
- **Missing records** - Incomplete data collection
- **Irregular intervals** - Inconsistent time sampling

## How It Works

### 1. Automatic Detection

The system automatically detects gaps by:

1. **Identifying timestamp columns** - Looks for columns like 'Timestamp', 'time', 'date', 'datetime'
2. **Analyzing time intervals** - Calculates expected frequency from existing data
3. **Finding gaps** - Identifies intervals larger than expected frequency (with 50% tolerance)

### 2. Smart Algorithm Selection

The system automatically selects the best algorithm based on gap characteristics:

- **Linear interpolation** - For ≤1% gaps (fast, simple)
- **Cubic interpolation** - For ≤5% gaps (smooth, accurate)
- **Advanced interpolation** - For ≤10% gaps (robust)
- **Seasonal forecasting** - For >10% gaps (handles complex patterns)

### 3. Gap Fixing Process

For each detected gap:

1. **Create complete time series** - Generate expected time points
2. **Apply selected algorithm** - Fill missing values using interpolation/forecasting
3. **Validate results** - Check for remaining NaN values
4. **Memory management** - Optimize memory usage during processing

## Usage

### Interactive Mode

When loading data through the interactive system:

```
📁 LOAD DATA
...

🔧 Time Series Gap Fixing
------------------------------
💡 This will detect and fix gaps in time series data before combining files.
   Gaps can occur due to missing data points, market holidays, or data collection issues.
   Fixing gaps ensures consistent time intervals for better analysis.
------------------------------

Fix time series gaps before combining data? (y/n, default: y): y

🔧 Fixing time series gaps...
📁 Processing dataframe 1/2...
   📅 Found timestamp column: Timestamp
   ⚠️  Found 4 gaps, fixing...
   🔧 Using algorithm: linear
   ✅ Gaps fixed successfully!
      • Algorithm used: linear
      • Gaps fixed: 4
      • Processing time: 1.23s
      • Memory used: 8.2MB

🔄 Combining data...
```

### Programmatic Usage

```python
from src.interactive.data_manager import DataManager

# Initialize data manager
data_manager = DataManager()

# Load and fix data
dataframes = [df1, df2, df3]
fixed_dataframes = data_manager._fix_time_series_gaps(dataframes)
```

## Supported Data Formats

- **Parquet** (.parquet) - Recommended for large datasets
- **CSV** (.csv) - Standard text format
- **JSON** (.json) - Structured data format

## Memory Optimization

The gap fixing process includes aggressive memory management:

- **Chunked processing** - For datasets >10M rows
- **Garbage collection** - Automatic memory cleanup
- **Memory monitoring** - Prevents out-of-memory errors
- **Configurable limits** - Adjustable via environment variables

## Configuration

Environment variables for memory management:

```bash
# Memory limits
MAX_MEMORY_MB=6144          # Maximum memory usage (default: 6GB)
CHUNK_SIZE=50000            # Rows per chunk (default: 50k)
ENABLE_MEMORY_OPTIMIZATION=true  # Enable memory optimization

# File size thresholds
MAX_FILE_SIZE_MB=200        # Maximum file size (default: 200MB)
SAMPLE_SIZE=10000           # Sample size for analysis (default: 10k)
```

## Benefits

### Data Quality
- **Consistent intervals** - Regular time sampling
- **Complete datasets** - No missing data points
- **Better analysis** - Reliable statistical calculations

### Performance
- **Faster processing** - No need to handle gaps during analysis
- **Memory efficient** - Optimized for large datasets
- **Parallel processing** - Multi-threaded gap detection

### Analysis Accuracy
- **Reliable indicators** - Technical indicators work correctly
- **Consistent features** - Feature engineering produces stable results
- **Better models** - ML models trained on complete data

## Troubleshooting

### Common Issues

1. **No timestamp column found**
   - Ensure your data has a timestamp column
   - Check column names: 'Timestamp', 'time', 'date', 'datetime'

2. **Memory errors during processing**
   - Reduce `MAX_MEMORY_MB` environment variable
   - Enable memory optimization: `ENABLE_MEMORY_OPTIMIZATION=true`

3. **Gaps not fully fixed**
   - Some complex gaps may require manual intervention
   - Check gap verification results for remaining issues

### Performance Tips

- **Use Parquet format** - Better compression and faster I/O
- **Enable memory optimization** - Automatic memory management
- **Monitor memory usage** - Check system resources during processing

## Examples

### Sample Data with Gaps

```python
import pandas as pd
import numpy as np

# Create sample data with gaps
dates = pd.date_range('2023-01-01', '2023-01-10', freq='1H')
dates_with_gaps = dates.drop([
    pd.Timestamp('2023-01-02 12:00:00'),
    pd.Timestamp('2023-01-03 06:00:00'),
    pd.Timestamp('2023-01-05 18:00:00')
])

df = pd.DataFrame({
    'Timestamp': dates_with_gaps,
    'Value': np.random.randn(len(dates_with_gaps))
})

print(f"Original data: {len(df)} rows")
print(f"Expected complete: {len(dates)} rows")
print(f"Gaps: {len(dates) - len(df)} missing points")
```

### After Gap Fixing

```python
# After processing through DataManager
print(f"Fixed data: {len(fixed_df)} rows")
print(f"Gaps filled: {len(fixed_df) - len(df)} points")
print(f"Complete time series: {fixed_df['Timestamp'].is_monotonic_increasing}")
```

## Best Practices

1. **Always backup data** - Original data is preserved
2. **Verify results** - Check gap verification output
3. **Monitor memory** - Ensure sufficient system resources
4. **Use appropriate formats** - Parquet for large datasets
5. **Test on samples** - Verify gap fixing on small datasets first

## Related Documentation

- [Data Loading Guide](../data/loading-data.md)
- [Memory Optimization](../development/memory-optimization.md)
- [Data Quality Checks](../eda/data-quality.md)
- [Gap Analysis](../eda/gap-analysis.md)
