# Gap Analysis Integration

## Overview

This document describes the integration of time series gap analysis functionality into the interactive system, specifically for the "8 eurusd" scenario.

## Background

The user requested to add functionality to show which files have time series gaps and where when using the command "8 eurusd" in the interactive system. Instead of creating new functionality from scratch, we leveraged the existing gap analysis capabilities in `eda_batch_check.py`.

## Implementation

### Files Modified

1. **`src/interactive/data_manager.py`**
   - Added import for `data_quality` module
   - Added `gap_analysis_enabled` flag
   - Implemented `analyze_time_series_gaps()` method
   - Implemented `_show_detailed_gap_info_from_eda()` method
   - Updated `load_data()` method to include gap analysis option

### Key Features

#### 1. Automatic Gap Detection
- Uses existing `data_quality.gap_check()` functionality
- Automatically detects datetime columns and DatetimeIndex
- Handles large datasets with memory optimization
- Supports both CSV and Parquet files

#### 2. Intelligent Frequency Detection
- Automatically determines expected frequency based on data patterns
- Supports various frequencies: 1T (minute), 15T (15 minutes), 1H (hour), 1D (day), 1W (week)

#### 3. Comprehensive Reporting
- Shows gap summary for all files
- Provides detailed gap information on request
- Groups gaps by file for better organization
- Shows gap count, largest gap, and analysis method

#### 4. User-Friendly Interface
- Integrates seamlessly with existing interactive system
- Asks user if they want to analyze gaps after loading data
- Provides option to see detailed gap information
- Uses colored output for better readability

## Usage

### Interactive System

1. Start the interactive system:
   ```bash
   ./interactive_system.py
   ```

2. Select option 1 (Load Data)

3. Enter "8 eurusd" to load EURUSD files

4. When prompted, choose "y" to analyze time series gaps

5. Optionally view detailed gap information

### Programmatic Usage

```python
from src.interactive.data_manager import DataManager

# Initialize data manager
data_manager = DataManager()

# Load files
data_files = [Path("data/EURUSD_file1.parquet"), Path("data/EURUSD_file2.csv")]

# Analyze gaps
result = data_manager.analyze_time_series_gaps(
    data_files, 
    datetime_column='Timestamp', 
    expected_frequency='1H'
)
```

## Example Output

```
🔍 ANALYZING TIME SERIES GAPS
----------------------------------------
📊 Analyzing 8 files for gaps...
📅 Using datetime column: 'Timestamp'
⏱️  Expected frequency: 1T

📁 Analyzing file 1/8: CSVExport_EURUSD_PERIOD_M1.parquet
  📅 Converting DatetimeIndex to column for gap analysis...
  Data Quality Check: Gaps
    Gaps detected in Timestamp: 8576 gaps
      Largest gap: 10 days 00:00:00

Gap Summary for all files (grouped by file):
  File: CSVExport_EURUSD_PERIOD_M1.parquet | Total gaps: 1
    Gap in 'Timestamp': from 2024-01-01 11:00:00 to 2024-01-01 13:00:00 (delta: 2 hours)

Show detailed gap information? (y/n): y

📋 DETAILED GAP INFORMATION
==================================================
📁 CSVExport_EURUSD_PERIOD_M1.parquet
   📊 Summary:
      • Total gaps: 1
   ⏰ Gap 1:
      • Column: Timestamp
      • Gaps count: 8576
      • Largest gap: 10 days 00:00:00
      • Analysis method: direct
```

## Technical Details

### Gap Detection Algorithm

The gap detection uses the existing algorithm from `data_quality.gap_check()`:

1. **Data Preparation**: Converts DatetimeIndex to column if needed
2. **Sorting**: Sorts data by datetime column
3. **Gap Calculation**: Calculates time differences between consecutive rows
4. **Threshold Detection**: Uses mean + 2*std as threshold for gap detection
5. **Memory Optimization**: Uses sampling for large datasets

### Memory Management

- Automatically detects large datasets (>200MB)
- Uses sampling for very large datasets
- Implements chunked processing for memory efficiency
- Provides progress indicators for long operations

### Error Handling

- Gracefully handles missing datetime columns
- Continues processing if individual files fail
- Provides clear error messages
- Maintains system stability

## Testing

### Unit Tests

Tests are located in `tests/interactive/test_data_manager_gap_analysis.py`:

- `test_analyze_time_series_gaps()`: Tests basic gap analysis functionality
- `test_determine_expected_frequency()`: Tests frequency detection
- `test_show_detailed_gap_info_from_eda()`: Tests detailed information display
- `test_real_user_scenario_with_gap_analysis()`: Tests complete user scenario

### Demo Script

A demo script `test_gap_analysis_demo.py` is provided to test the functionality with real EURUSD data.

## Benefits

1. **Reuses Existing Code**: Leverages proven gap analysis functionality
2. **Maintains Consistency**: Uses same algorithms and output formats
3. **Memory Efficient**: Handles large datasets without memory issues
4. **User Friendly**: Integrates seamlessly with existing interface
5. **Comprehensive**: Provides both summary and detailed views

## Future Enhancements

1. **Gap Visualization**: Add plots showing gap distribution
2. **Gap Classification**: Categorize gaps by type (weekend, holiday, etc.)
3. **Automatic Fixing**: Integrate with existing gap fixing functionality
4. **Export Reports**: Generate gap analysis reports in various formats

## Related Files

- `src/eda/data_quality.py`: Core gap analysis functionality
- `src/eda/eda_batch_check.py`: Batch processing script
- `tests/interactive/test_data_manager_gap_analysis.py`: Unit tests
- `tests/interactive/test_gap_analysis_demo.py`: Demo test script
