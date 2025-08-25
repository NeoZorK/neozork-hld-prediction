# CSV Folder Processing Guide

## Overview

The CSV folder processing feature allows you to process multiple CSV files in a folder with progress bars, ETA calculation, and comprehensive error handling. This is particularly useful for batch processing large datasets or multiple instruments.

## Features

- **Batch Processing**: Process all CSV files in a folder automatically
- **Progress Bars**: Two-level progress tracking (overall + per file)
- **ETA Calculation**: Estimated time remaining for completion
- **File Information**: Size and processing time per file
- **Error Handling**: Continue processing even if some files fail
- **Default Point Value**: Automatically uses 0.00001 for folder processing
- **Export Support**: Export results in multiple formats (parquet, CSV, JSON)
- **Mask Filtering**: Filter files by name using case-insensitive patterns

## Basic Usage

### Process All CSV Files in a Folder

```bash
# Basic folder processing with default settings
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001

# Process folder with specific rule
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --rule RSI

# Process folder with fastest backend
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 -d fastest

# Process folder with export
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --export-parquet
```

### Process CSV Files with Mask Filtering ⭐ **NEW**

Filter files by name using mask patterns:

```bash
# Using positional argument (recommended)
uv run run_analysis.py csv --csv-folder mql5_feed EURUSD --point 0.00001

# Using --csv-mask flag
uv run run_analysis.py csv --csv-folder mql5_feed --csv-mask AAPL --point 0.00001

# With trading rule
uv run run_analysis.py csv --csv-folder mql5_feed EURUSD --point 0.00001 --rule RSI

# With export
uv run run_analysis.py csv --csv-folder mql5_feed EURUSD --point 0.00001 --export-parquet

# Case-insensitive filtering
uv run run_analysis.py csv --csv-folder mql5_feed eurusd --point 0.00001
```

### Advanced Usage

#### Mask Filtering

Filter files by name using mask patterns:

```bash
# Filter by currency pair
uv run run_analysis.py csv --csv-folder mql5_feed EURUSD --point 0.00001

# Filter by stock symbol
uv run run_analysis.py csv --csv-folder mql5_feed --csv-mask AAPL --point 0.00001

# Filter by time period
uv run run_analysis.py csv --csv-folder mql5_feed D1 --point 0.00001

# Filter by multiple criteria (files containing both EURUSD and D1)
uv run run_analysis.py csv --csv-folder mql5_feed EURUSD_D1 --point 0.00001
```

#### Export and Processing Options

```bash
# Process folder with multiple export formats
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --export-parquet --export-csv --export-json

# Process folder with custom rule and plotting backend
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --rule PV -d plotly

# Process folder with terminal backend for SSH/remote connections
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --rule RSI -d term

# Combine mask filtering with export
uv run run_analysis.py csv --csv-folder mql5_feed EURUSD --point 0.00001 --export-parquet
```

## Command Line Options

### Required Arguments

- **`--csv-folder`**: Path to folder containing CSV files
- **`--point`**: Price precision (optional, defaults to 0.00001 for folder processing)

### Optional Arguments

- **`--csv-mask`**: Filter CSV files by name (case-insensitive, used with --csv-folder)
- **`--rule`**: Trading rule to apply (default: OHLCV)
- **`-d`** or **`--draw`**: Drawing backend (fastest, fast, plotly, mpl, seaborn, term)
- **`--export-parquet`**: Export results to Parquet format
- **`--export-csv`**: Export results to CSV format
- **`--export-json`**: Export results to JSON format

## Progress Display

The folder processing shows two progress bars:

1. **Overall Progress**: Shows progress across all files
   - Displays current file being processed
   - Shows total files processed/failed
   - Shows total data size processed

2. **File Progress**: Shows progress for current file
   - Displays file name and number
   - Shows file size and processing time
   - Updates in real-time

## Example Output

```
Found 95 CSV files in folder: mql5_feed
Total estimated processing time: 47.5 seconds
Total data size: 6831.5 MB

# With mask filtering:
Found 12 CSV files in folder 'mql5_feed' matching mask 'EURUSD'
Total estimated processing time: 6.0 seconds
Total data size: 864.0 MB

Processing: CSVExport_AAPL.NAS_PERIOD_D1.csv...: 100%|██████████| 95/95 [00:45<00:00, 2.1file/s, processed=93, failed=2, size=6831.5MB]

📊 Processing Summary:
   Files processed: 93
   Files failed: 2
   Total time: 45.2 seconds
   Average time per file: 0.5 seconds
   Failed files: CSVExport_USDCHF_PERIOD_M1.csv, CSVExport_USDJPY_PERIOD_M1.csv
```

## Error Handling

The folder processor continues processing even if individual files fail:

- **File Not Found**: Skips file and continues
- **Invalid CSV Format**: Logs error and continues
- **Processing Errors**: Logs error and continues
- **Memory Issues**: Logs error and continues

Failed files are listed in the summary at the end.

## Performance Considerations

### File Size Estimation

The processor estimates processing time based on file size:
- Rough estimate: 1MB = ~0.5 seconds processing time
- Actual time may vary based on data complexity and system performance

### Memory Usage

- Each file is processed individually to minimize memory usage
- Results are saved immediately after processing
- No accumulation of large datasets in memory

### Caching

- CSV files are automatically cached as Parquet files
- Subsequent runs will use cached data for faster processing
- Cache is stored in `data/cache/csv_converted/`

## Supported File Formats

The folder processor supports standard CSV files with the following requirements:

- **Header Row**: Must have column headers
- **Required Columns**: DateTime, Open, High, Low, Close, Volume
- **DateTime Format**: YYYY.MM.DD HH:MM or similar
- **Numeric Data**: All price and volume data must be numeric

## File Naming Convention

The processor works with any CSV files in the folder, but common naming patterns include:

- `CSVExport_SYMBOL_PERIOD_TIMEFRAME.csv`
- `SYMBOL_TIMEFRAME.csv`
- `data_SYMBOL.csv`

## Integration with Existing Workflow

The CSV folder processing integrates seamlessly with the existing workflow:

- **Same Rules**: All trading rules work with folder processing
- **Same Backends**: All plotting backends are supported
- **Same Export**: All export formats are supported
- **Same Metrics**: Universal trading metrics are calculated for each file

## Troubleshooting

### Common Issues

1. **No CSV files found**
   - Ensure the folder contains `.csv` files
   - Check file permissions

2. **All files fail**
   - Verify CSV format matches requirements
   - Check for missing required columns

3. **Slow processing**
   - Consider using `-d fastest` for faster processing
   - Check system resources

4. **Memory errors**
   - Process smaller batches of files
   - Ensure sufficient system memory

### Debug Information

Enable debug mode for detailed information:

```bash
# Set debug environment variable
export DEBUG=1

# Run with debug output
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001
```

## Best Practices

1. **Organize Files**: Keep related CSV files in dedicated folders
2. **Test First**: Process a small subset before running on large folders
3. **Monitor Resources**: Watch system memory and CPU usage
4. **Use Caching**: Let the system cache files for faster subsequent runs
5. **Export Results**: Use export flags to save results for later analysis

## Examples

### Basic Batch Processing

```bash
# Process all forex data
uv run run_analysis.py csv --csv-folder forex_data --point 0.00001 --rule RSI

# Process all stock data
uv run run_analysis.py csv --csv-folder stock_data --point 0.01 --rule MACD

# Process all crypto data
uv run run_analysis.py csv --csv-folder crypto_data --point 0.01 --rule PV
```

### Advanced Batch Processing

```bash
# Process with multiple rules and export
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 \
    --rule RSI,MACD,PV \
    --export-parquet --export-csv \
    -d fastest

# Process with custom analysis
uv run run_analysis.py csv --csv-folder mql5_feed --point 0.00001 \
    --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open \
    -d plotly
```

## Related Documentation

- [CLI Interface Guide](cli-interface.md)
- [Trading Rules Reference](../reference/indicators/)
- [Export Functions Guide](export-functions.md)
- [Plotting Modes Comparison](plotting-modes-comparison.md)
