# Time Series Gaps Analysis

## Overview

The Time Series Gaps Analysis functionality has been enhanced to automatically analyze multiple timeframe files for time series gaps. This feature is now the first option in the EDA Analysis menu, providing comprehensive gap detection across all available data files.

## Features

### Multi-File Analysis
- **Automatic Discovery**: Scans all data files in the `data/` directory and subdirectories
- **File Type Support**: Handles both CSV and Parquet files
- **Smart Filtering**: Excludes backup and cache directories automatically
- **Memory Efficient**: Processes files individually to avoid memory issues

### Gap Detection
- **Timestamp Column Detection**: Automatically identifies timestamp columns in data
- **Frequency Analysis**: Determines expected data frequency (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
- **Gap Threshold**: Uses 1.5x expected frequency as threshold for gap detection
- **Comprehensive Reporting**: Shows gap count, frequency, and row count for each file

### Output Format
- **File-by-File Analysis**: Individual analysis results for each file
- **Summary Report**: Comprehensive overview of all findings
- **Gap Statistics**: Detailed information about detected gaps

## Usage

### Menu Navigation
1. Select **2. 🔍 EDA Analysis** from main menu
2. Select **1. ⏱️ Time Series Gaps Analysis** from EDA menu
3. System automatically analyzes all available data files

### Example Output
```
⏱️ TIME SERIES GAPS ANALYSIS
--------------------------------------------------
📁 Found 35 data files for analysis
--------------------------------------------------

📊 File 1/35: sample_ohlcv_2000.csv
   📅 Analyzing 1 timestamp columns for gaps...
      • Date: No gaps found
   ✅ No gaps found

📊 COMPREHENSIVE TIME SERIES GAPS SUMMARY
============================================================
📁 Total files analyzed: 35
🔍 Total gap issues found: 1

📋 Files with gaps: 1

📁 UNKNOWN_D1_RSI.parquet:
   📅 DateTime:
      • Gaps: 2,897
      • Frequency: 1D
      • Rows: 13,996
```

## Technical Details

### File Processing
- **CSV Files**: Reads with multiple encoding support (UTF-8, Latin-1, CP1252)
- **Parquet Files**: Direct reading with error handling
- **Sample Loading**: Uses first 10,000 rows for CSV files to improve performance
- **Memory Management**: Automatic cleanup after each file analysis

### Gap Detection Algorithm
1. **Timestamp Conversion**: Converts timestamp columns to datetime format
2. **Sorting**: Sorts data chronologically
3. **Interval Calculation**: Computes time differences between consecutive rows
4. **Frequency Estimation**: Determines expected frequency from median interval
5. **Gap Identification**: Flags intervals > 1.5x expected frequency

### Supported Timeframes
- **Minutes**: M1, M5, M15, M30
- **Hours**: H1, H4
- **Days**: D1
- **Weeks**: W1
- **Months**: MN1

## Benefits

### For Data Quality
- **Comprehensive Coverage**: Analyzes all data files automatically
- **Early Detection**: Identifies data quality issues before analysis
- **Standardized Process**: Consistent gap detection across all timeframes

### For Users
- **No Manual Selection**: Automatically finds and analyzes relevant files
- **Clear Reporting**: Easy-to-understand gap summaries
- **Time Savings**: Single command analyzes entire dataset

### For System Performance
- **Memory Efficient**: Processes files individually
- **Error Resilient**: Continues analysis even if individual files fail
- **Scalable**: Handles large numbers of files efficiently

## Error Handling

### File Loading Errors
- **Encoding Issues**: Tries multiple encodings for CSV files
- **Missing Timestamps**: Skips files without timestamp columns
- **Corrupted Files**: Continues with next file on error

### Analysis Errors
- **Invalid Data**: Handles malformed timestamp data gracefully
- **Memory Issues**: Automatic cleanup after each file
- **Partial Failures**: Reports successful analyses even if some files fail

## Future Enhancements

### Planned Features
- **Gap Visualization**: Charts showing gap patterns over time
- **Automatic Fixing**: Integration with gap fixing algorithms
- **Performance Metrics**: Analysis timing and resource usage
- **Export Options**: Save gap analysis results to files

### Integration Opportunities
- **Data Pipeline**: Automatic gap detection in data processing workflows
- **Quality Monitoring**: Regular gap analysis for data quality monitoring
- **Alert System**: Notifications when significant gaps are detected
