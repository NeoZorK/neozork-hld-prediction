# Indicator Export Feature

This document describes the new indicator export functionality added to the Shcherbyna Pressure Vector Indicator Analysis Tool.

## Overview

The new export feature allows you to calculate indicators and save the calculated data to files in multiple formats:
- **Parquet** (`.parquet`): For efficient storage and further analysis
- **CSV** (`.csv`): For terminal display and external program integration  
- **JSON** (`.json`): For terminal display and web applications

## Export Directories

All exported indicator files are saved to organized directories:
- `data/indicators/parquet/` - Parquet format files
- `data/indicators/csv/` - CSV format files  
- `data/indicators/json/` - JSON format files

## Export Flags

Three new command-line flags are available:

### `--export-parquet`
Exports calculated indicator data to a Parquet file.
```bash
python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 --rule PV --export-parquet
```

### `--export-csv` 
Exports calculated indicator data to a CSV file.
```bash
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule SR --export-csv
```

### `--export-json`
Exports calculated indicator data to a JSON file.
```bash
python run_analysis.py binance -t BTCUSDT --interval H1 --start 2024-01-01 --end 2024-02-01 --point 0.01 --rule PHLD --export-json
```

### Multiple Exports
You can export to multiple formats simultaneously:
```bash
python run_analysis.py polygon -t AAPL --interval D1 --start 2024-01-01 --end 2024-02-01 --point 0.01 --rule PV --export-parquet --export-csv --export-json
```

## File Naming Convention

Exported files follow a consistent naming pattern:
```
{source_name}_{interval}_{rule_name}.{extension}
```

Examples:
- `EURUSD_D1_PressureVector.parquet`
- `BTCUSDT_H1_SupportResistants.csv`
- `AAPL_D1_PredictHighLowDirection.json`

## Show Indicator Files

A new `show ind` command allows you to browse and view calculated indicator files:

### List All Indicator Files
```bash
python run_analysis.py show ind
```

### List by Format
```bash
python run_analysis.py show ind parquet    # Show all parquet files
python run_analysis.py show ind csv        # Show all CSV files  
python run_analysis.py show ind json       # Show all JSON files
```

### Filter by Keywords
```bash
python run_analysis.py show ind parquet mn1     # Parquet files containing 'mn1'
python run_analysis.py show ind csv EURUSD      # CSV files containing 'EURUSD'
```

### Display Behavior

- **Single Parquet File**: Automatically opens interactive chart with calculated indicators
- **CSV Files**: Displays first 10 rows in terminal
- **JSON Files**: Displays first 5 records in terminal
- **Multiple Files**: Shows file list with metadata

## Data Content

Exported files contain:
- **OHLCV Data**: Open, High, Low, Close, Volume columns
- **Timestamp**: Date/time index or column
- **Indicator Columns**: Calculated indicator values (varies by rule)
  - PV rule: Pressure, PV columns
  - SR rule: Support, Resistance columns  
  - PHLD rule: Direction prediction columns

## Use Cases

### For Analysis
Use parquet files for:
- Loading into data analysis tools
- Further indicator calculations
- Chart visualization with tools like Python/pandas

### For Integration
Use CSV/JSON files for:
- Terminal inspection
- Integration with external programs
- Web applications and APIs
- Database imports

## Examples

### Complete Workflow
```bash
# 1. Calculate and export PV indicator for EURUSD
python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 --rule PV --export-parquet --export-csv

# 2. List exported files
python run_analysis.py show ind

# 3. View specific parquet file with chart
python run_analysis.py show ind parquet EURUSD

# 4. View CSV file content in terminal
python run_analysis.py show ind csv EURUSD
```

### Batch Processing
```bash
# Export multiple indicators for the same data
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV --export-parquet
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule SR --export-parquet  
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PHLD --export-parquet

# View all exported indicators
python run_analysis.py show ind parquet
```

## Technical Notes

- Export functionality works with all data sources (CSV, Yahoo Finance, Polygon, Binance, Exchange Rate API)
- Directory structure is automatically created if it doesn't exist
- Files are named to avoid conflicts using rule and data source information
- JSON files use pretty formatting for readability
- All formats preserve timestamp information appropriately

## Docker Support

The export functionality works seamlessly in Docker environments. The `data/indicators/` directory is included in the Docker volume mounts for persistent storage.
