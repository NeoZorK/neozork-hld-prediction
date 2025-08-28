# Comprehensive Data Quality Check

## Overview

The Comprehensive Data Quality Check is an enhanced version of the basic data quality check that integrates all functionality from `src/eda/eda_batch_check.py`. This feature provides a complete data quality assessment with automatic fixing capabilities.

## Features

### Data Quality Checks

The comprehensive check performs the following quality assessments:

1. **NaN Check** - Identifies missing values in all columns
2. **Duplicate Check** - Finds fully duplicated rows and duplicated values in string columns
3. **Gap Check** - Detects gaps in time series (abnormally large intervals in datetime columns)
4. **Zero Check** - Identifies zero values in numeric columns with anomaly heuristics
5. **Negative Check** - Finds negative values in OHLCV and datetime columns
6. **Infinity Check** - Detects +inf and -inf values in numeric columns

### DateTime Column Detection

The system automatically:
- Detects existing DateTime columns in the dataset
- Warns if no DateTime columns are found
- Provides recommendations for converting timestamp columns to datetime format

### Automatic Fixing

When issues are detected, the system offers three options:

1. **Fix All Issues Automatically** - Applies all available fixes
2. **Review and Fix Individually** - Shows manual fix options
3. **Skip Fixing** - Continues without making changes

### Fix Capabilities

The system can automatically fix:

- **NaN Values** - Uses median for numeric, mode for string, forward/backward fill for datetime
- **Duplicate Rows** - Removes fully duplicated rows
- **Time Series Gaps** - Interpolates missing values
- **Zero Values** - Applies appropriate strategies based on column type
- **Negative Values** - Takes absolute values for OHLCV columns
- **Infinity Values** - Replaces with appropriate finite values

## Usage

### Interactive System

1. Start the interactive system: `./interactive_system.py`
2. Load your data (Option 1)
3. Select "EDA Analysis" (Option 2)
4. Choose "Comprehensive Data Quality Check" (Option 1)

### Programmatic Usage

```python
from src.interactive import InteractiveSystem

system = InteractiveSystem()
system.current_data = your_dataframe
system.run_comprehensive_data_quality_check()
```

## Integration Details

### Menu Integration

The new functionality is integrated into the EDA menu as the first option:

```
🔍 EDA ANALYSIS MENU:
0. 🔙 Back to Main Menu
1. 🧹 Comprehensive Data Quality Check ✅
2. 🔍 Basic Data Quality Check
3. 📊 Basic Statistics
...
```

### Backward Compatibility

- The original basic data quality check remains available as option 2
- All existing functionality is preserved
- Menu tracking works for both options

### Dependencies

The comprehensive check uses the following modules:
- `src.eda.data_quality` - Core quality check functions
- `src.eda.fix_files` - Data fixing functions
- `src.eda.file_info` - File information utilities

## Output

### Console Output

The system provides detailed console output including:

- Individual check results for each quality issue
- Summary of all detected issues
- DateTime column detection status
- Fix progress and results
- Backup file location

### Results Storage

Results are stored in `system.current_results['comprehensive_data_quality']`:

```python
{
    'nan_issues': [...],
    'duplicate_issues': [...],
    'gap_issues': [...],
    'zero_issues': [...],
    'negative_issues': [...],
    'infinity_issues': [...],
    'total_issues': 6,
    'datetime_columns': ['datetime'],
    'data_shape': (99, 6)
}
```

## Backup System

When fixing issues, the system automatically:

1. Creates a backup of the original data
2. Saves it to `data/backups/data_backup_{timestamp}.parquet`
3. Displays the backup file location
4. Shows before/after data shapes

## Error Handling

The system includes comprehensive error handling:

- Graceful handling of missing dependencies
- Safe input handling with EOF protection
- Detailed error messages with tracebacks
- Fallback options when fixes fail

## Testing

The functionality has been tested with:

- Synthetic test data with various quality issues
- Menu integration verification
- Import and dependency checks
- Error handling scenarios

## Future Enhancements

Potential improvements:

1. **Selective Fixing** - Choose which specific issues to fix
2. **Custom Fix Strategies** - User-defined fixing approaches
3. **Quality Score** - Overall data quality rating
4. **Batch Processing** - Handle multiple files simultaneously
5. **Export Reports** - Generate detailed quality reports

## Related Documentation

- [Basic Data Quality Check](../reference/data-quality-check.md)
- [EDA Batch Check](../reference/eda-batch-check.md)
- [Data Fixing Strategies](../reference/data-fixing.md)
- [Interactive System Guide](../getting-started/interactive-system.md)
