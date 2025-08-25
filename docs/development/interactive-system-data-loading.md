# Interactive System Data Loading

## Overview

The interactive system (`scripts/ml/interactive_system.py`) provides a user-friendly interface for loading and analyzing financial data. The data loading functionality has been updated to provide a more intuitive and secure approach to accessing data files.

## Data Loading Options

### P1: Load Single File from Data Folder

**Purpose**: Load a single data file from the `data` folder or its subfolders.

**How it works**:
1. The system automatically scans the `data` folder and all its subfolders
2. Displays a list of available files (up to 10 files shown)
3. User enters the file name (e.g., `sample_ohlcv_1000.csv`)
4. System validates the file exists and loads it

**Example**:
```
📄 LOAD SINGLE FILE FROM DATA FOLDER
------------------------------
💡 Available files in 'data' folder:
   1. sample_ohlcv_2000.csv
   2. sample_ohlcv_with_issues.csv
   3. mn1.csv
   4. sample_ohlcv_300.csv
   5. sample_ohlcv_1000.csv
   ... and 112 more files
------------------------------
Enter file name (e.g., sample_ohlcv_1000.csv): sample_ohlcv_1000.csv
```

**Supported file formats**:
- CSV files (`.csv`)
- Parquet files (`.parquet`)
- Excel files (`.xlsx`, `.xls`)

### P2: Load All Files from Folder (with Optional Mask)

**Purpose**: Load multiple files from a folder with optional filtering by file name pattern.

**How it works**:
1. User enters folder path (e.g., `data`)
2. Optionally adds a mask to filter files (e.g., `data gbpusd`)
3. System finds all matching files and loads them
4. All loaded files are combined into a single dataset

**Input format**: `folder_path [mask]`

**Examples**:

| Input | Description |
|-------|-------------|
| `data` | Loads all data files from the `data` folder |
| `data gbpusd` | Loads all files with "gbpusd" in the filename |
| `data parquet` | Loads all `.parquet` files |
| `data binance` | Loads all files with "binance" in the filename |
| `data/raw_parquet` | Loads all files from the `data/raw_parquet` subfolder |
| `data/indicators csv` | Loads all CSV files from the `data/indicators` folder |

**Case-insensitive matching**: The mask search is case-insensitive, so `data GBPUSD` and `data gbpusd` will find the same files.

## File Discovery

The system automatically discovers files in the following locations:

```
data/
├── *.csv, *.parquet, *.xlsx, *.xls (root files)
├── raw_parquet/
│   ├── binance_BTCUSDT_H1.parquet
│   └── yfinance_AAPL_D1.parquet
├── indicators/
│   ├── csv/
│   │   ├── UNKNOWN_D1_PressureVector.csv
│   │   └── UNKNOWN_D1_SupportResistants.csv
│   └── parquet/
│       ├── UNKNOWN_D1_SupportResistants.parquet
│       └── DEMO_RSI.parquet
└── cache/
    └── csv_converted/
        ├── CSVExport_GBPUSD_PERIOD_MN1.parquet
        └── CSVExport_XAUUSD_PERIOD_MN1.parquet
```

## Security Features

- **Restricted access**: Files can only be loaded from the `data` folder and its subfolders
- **File validation**: System validates file existence before attempting to load
- **Error handling**: Graceful error messages for missing files or invalid formats
- **Path sanitization**: Prevents directory traversal attacks

## Usage Examples

### Example 1: Load a specific sample file
```
Select option (0-2): 1
Enter file name: sample_ohlcv_1000.csv
```

### Example 2: Load all GBPUSD files
```
Select option (0-2): 2
Enter folder path (with optional mask): data gbpusd
```

### Example 3: Load all parquet files from indicators
```
Select option (0-2): 2
Enter folder path (with optional mask): data/indicators parquet
```

## Technical Implementation

### Key Methods

- `load_data()`: Main entry point for data loading
- `_load_single_file()`: Handles single file loading with folder scanning
- `_load_folder_files()`: Handles folder loading with mask support
- `load_data_from_file()`: Core file loading functionality

### File Discovery Logic

```python
# Scan data folder for available files
data_folder = Path("data")
data_files = []
for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
    data_files.extend(data_folder.rglob(f"*{ext}"))
```

### Mask Filtering Logic

```python
if mask:
    # Apply mask filter with case-insensitive search
    pattern = f"*{mask}*{ext}"
    data_files.extend(folder_path.glob(pattern))
    pattern = f"*{mask.upper()}*{ext}"
    data_files.extend(folder_path.glob(pattern))
    pattern = f"*{mask.lower()}*{ext}"
    data_files.extend(folder_path.glob(pattern))
```

## Testing

The functionality is tested by `tests/scripts/test_interactive_system_data_loading.py` which verifies:

1. Data folder scanning
2. Single file loading
3. Folder loading with masks
4. File discovery in subfolders

Run tests with:
```bash
uv run python tests/scripts/test_interactive_system_data_loading.py
```

## Migration from Previous Version

### Changes Made

1. **Removed P3 option**: The separate "Load files by mask" option was removed
2. **Enhanced P2**: Folder loading now supports optional mask parameter
3. **Restricted P1**: Single file loading now only works from `data` folder
4. **Improved UX**: Better file discovery and user guidance

### Backward Compatibility

- Existing workflows using folder loading will continue to work
- The mask functionality is now more intuitive with the `folder mask` format
- Single file loading is more secure and user-friendly

## Future Enhancements

Potential improvements for future versions:

1. **File preview**: Show file size and row count before loading
2. **Smart suggestions**: Suggest files based on recent usage
3. **Batch operations**: Load files from multiple folders at once
4. **Data validation**: Pre-validate file format and structure
5. **Caching**: Cache file lists for faster discovery
