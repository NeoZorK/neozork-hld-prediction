# Batch CSV Processing Guide

Complete guide to batch processing CSV files in the Neozork HLD Prediction project.

## Overview

The batch CSV processing feature allows you to convert multiple CSV files in a folder simultaneously, making it ideal for processing MQL5 export folders or any collection of CSV data files.

## Features

- **Batch conversion** - Process entire folders of CSV files
- **Automatic caching** - Convert to Parquet format for performance
- **Progress tracking** - Detailed progress and summary information
- **Error handling** - Graceful handling of individual file failures
- **MQL5 format support** - Optimized for MQL5 export format

## Usage

### Basic Batch Processing

Convert all CSV files in a folder:

```bash
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001
```

### Example Output

```
Found 8 CSV files in folder: mql5_feed
  - CSVExport_EURUSD_PERIOD_D1.csv
  - CSVExport_EURUSD_PERIOD_H1.csv
  - CSVExport_EURUSD_PERIOD_H4.csv
  - CSVExport_EURUSD_PERIOD_M1.csv
  - CSVExport_EURUSD_PERIOD_M15.csv
  - CSVExport_EURUSD_PERIOD_M5.csv
  - CSVExport_EURUSD_PERIOD_MN1.csv
  - CSVExport_EURUSD_PERIOD_W1.csv

Starting batch conversion of 8 CSV files...
Processing file 1/8: CSVExport_EURUSD_PERIOD_D1.csv
Successfully converted: CSVExport_EURUSD_PERIOD_D1.csv (1000 rows)
Processing file 2/8: CSVExport_EURUSD_PERIOD_H1.csv
Successfully converted: CSVExport_EURUSD_PERIOD_H1.csv (2000 rows)
...

--- Batch Conversion Summary ---
Total files processed: 8
Successful conversions: 8
Failed conversions: 0

Successfully converted files:
  ✓ CSVExport_EURUSD_PERIOD_D1.csv
  ✓ CSVExport_EURUSD_PERIOD_H1.csv
  ✓ CSVExport_EURUSD_PERIOD_H4.csv
  ✓ CSVExport_EURUSD_PERIOD_M1.csv
  ✓ CSVExport_EURUSD_PERIOD_M15.csv
  ✓ CSVExport_EURUSD_PERIOD_M5.csv
  ✓ CSVExport_EURUSD_PERIOD_MN1.csv
  ✓ CSVExport_EURUSD_PERIOD_W1.csv
```

## Command Line Options

### Required Parameters

- **`--csv-folder`** - Path to folder containing CSV files
- **`--point`** - Price precision (e.g., 0.00001 for EURUSD, 0.01 for stocks)

### Example Commands

```bash
# Convert MQL5 export folder
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001

# Convert custom data folder
uv run run_analysis.py csv --csv-folder data/forex_exports --point 0.00001

# Convert stock data folder
uv run run_analysis.py csv --csv-folder data/stock_data --point 0.01
```

## File Processing

### Supported Formats

The batch processor automatically detects and processes CSV files with the following characteristics:

- **File extension**: `.csv` or `.CSV`
- **MQL5 format**: Standard MQL5 export format with header row
- **Column mapping**: Automatic mapping for standard OHLCV columns
- **DateTime format**: Standard MQL5 datetime format

### Processing Order

Files are processed in alphabetical order for consistent results:

1. Files are sorted alphabetically by filename
2. Each file is processed individually
3. Progress is reported for each file
4. Errors in individual files don't stop the batch process

### Caching

Each CSV file is automatically converted to Parquet format for caching:

- **Cache location**: `data/cache/csv_converted/`
- **Cache naming**: `{original_filename}.parquet`
- **Performance**: Subsequent runs use cached Parquet files
- **Validation**: Cached files are validated before use

## Error Handling

### Individual File Errors

If a single file fails to process:

- The error is logged with details
- Processing continues with the next file
- Failed files are reported in the summary
- The batch process completes successfully if any files were processed

### Common Error Scenarios

1. **Invalid CSV format** - File doesn't match expected structure
2. **Missing columns** - Required OHLCV columns not found
3. **Date parsing errors** - DateTime column format issues
4. **File access errors** - Permission or file system issues

### Error Recovery

- Check file format and column names
- Verify file permissions
- Review error messages in the output
- Re-run the batch process after fixing issues

## Performance Considerations

### Large Folders

For folders with many files:

- Processing is sequential to avoid memory issues
- Each file is processed independently
- Progress is reported for each file
- Memory usage is optimized per file

### Caching Benefits

- First run: CSV files are read and converted to Parquet
- Subsequent runs: Parquet files are used directly
- Significant performance improvement for repeated processing
- Automatic cache validation and refresh

## Integration with Analysis

### Post-Processing

After batch conversion, you can:

1. **View converted files**:
   ```bash
   uv run run_analysis.py show csv
   ```

2. **Analyze individual files**:
   ```bash
   uv run run_analysis.py csv --csv-file data/cache/csv_converted/CSVExport_EURUSD_PERIOD_D1.parquet --point 0.00001 --rule RSI
   ```

3. **Export indicators**:
   ```bash
   uv run run_analysis.py csv --csv-file data/cache/csv_converted/CSVExport_EURUSD_PERIOD_D1.parquet --point 0.00001 --rule PV --export-parquet
   ```

## Best Practices

### Folder Organization

- Keep CSV files in dedicated folders
- Use descriptive folder names
- Avoid mixing CSV files with other formats
- Ensure consistent point sizes within folders

### Point Size Selection

- **Forex pairs**: 0.00001 (5 decimal places)
- **Stocks**: 0.01 (2 decimal places)
- **Cryptocurrency**: 0.01 (2 decimal places)
- **Indices**: 0.01 (2 decimal places)

### File Naming

- Use consistent naming conventions
- Include timeframe information
- Avoid special characters in filenames
- Keep filenames descriptive but concise

## Troubleshooting

### Common Issues

1. **No files found**: Check folder path and file extensions
2. **Permission errors**: Verify read access to CSV files
3. **Format errors**: Ensure CSV files match MQL5 export format
4. **Point size errors**: Verify point size matches your data precision

### Debug Mode

For detailed debugging information:

```bash
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --verbose
```

### Validation

To validate converted files:

```bash
# Check cache directory
ls -la data/cache/csv_converted/

# Verify Parquet files
uv run run_analysis.py show csv
```

## Related Documentation

- [CLI Interface Guide](cli-interface.md) - Complete CLI reference
- [Data Sources API](api/data-sources.md) - Technical API documentation
- [Export Functions](export-functions.md) - Data export capabilities
- [Getting Started](getting-started/getting-started.md) - Project setup guide
