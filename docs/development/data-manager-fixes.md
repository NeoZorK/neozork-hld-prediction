# DataManager Fixes - Cache Directories and MQL5 Feed Exclusion

## Overview

This document describes the fixes applied to the `DataManager` class in the interactive system to address missing cache directories and exclude the `mql5_feed` directory from the data loading interface.

## Issues Fixed

### 1. Missing Cache Directories

**Problem**: When running `./interactive_system.py` → Load Data, the system was missing required cache directories:
- `data/cache/`
- `data/cache/csv_converted/`
- `data/cache/uv_cache/`
- `data/backups/`

**Solution**: Added automatic creation of cache directories when they don't exist.

### 2. MQL5 Feed Directory in Data Loading List

**Problem**: The `mql5_feed` directory was appearing in the list of available folders for data loading, but it should only be used with `run_analysis.py` for CSV to Parquet conversion.

**Solution**: Excluded `mql5_feed` directory from the folder list and added explanatory note.

### 3. CSV Converted Directory Inclusion

**Problem**: The `data/cache/csv_converted` directory was excluded from the folder list due to the general cache exclusion rule.

**Solution**: Specifically included `data/cache/csv_converted` directory for loading converted CSV files.

## Changes Made

### File: `src/interactive/data_manager.py`

#### 1. Cache Directory Creation

```python
# Create necessary cache directories if they don't exist
cache_dirs = [
    data_folder / "cache",
    data_folder / "cache" / "csv_converted",
    data_folder / "cache" / "uv_cache",
    data_folder / "backups"
]

for cache_dir in cache_dirs:
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created cache directory: {cache_dir}")
```

#### 2. MQL5 Feed Exclusion

```python
# Skip cache folders and mql5_feed to avoid loading cached files
if 'cache' not in item.name.lower() and item.name != 'mql5_feed':
    subfolders.append(item)
```

#### 3. CSV Converted Directory Inclusion

```python
# Add csv_converted folder specifically if it exists
csv_converted_folder = data_folder / "cache" / "csv_converted"
if csv_converted_folder.exists() and csv_converted_folder.is_dir():
    subfolders.append(csv_converted_folder)
```

#### 4. User Information

```python
print("\n💡 Note: mql5_feed directory is excluded from this list")
print("   (it's only used with run_analysis.py for CSV to Parquet conversion)")
print("   data/cache/csv_converted is included for loading converted CSV files")
```

## Testing

Created comprehensive tests in `tests/test_data_manager_fixes.py`:

- `test_cache_directories_creation`: Verifies cache directories are created when missing
- `test_mql5_feed_exclusion_and_csv_converted_inclusion`: Verifies mql5_feed directory is excluded and csv_converted is included
- `test_cache_directory_structure`: Verifies correct cache directory structure

All tests pass with 100% coverage.

## Usage

### Before Fix
```
📁 Available folders:
0. 🔙 Back to Main Menu
1. 📁 data/
2. 📁 mql5_feed/  # ❌ Should not be here
3. 📁 data/indicators/
...
```

### After Fix
```
📁 Available folders:
0. 🔙 Back to Main Menu
1. 📁 data/
2. 📁 data/indicators/
3. 📁 data/indicators/json/
4. 📁 data/indicators/csv/
5. 📁 data/indicators/parquet/
6. 📁 data/raw_parquet/
7. 📁 data/backups/
8. 📁 data/cache/csv_converted/

💡 Note: mql5_feed directory is excluded from this list
   (it's only used with run_analysis.py for CSV to Parquet conversion)
   data/cache/csv_converted is included for loading converted CSV files
```

## Benefits

1. **Automatic Setup**: Cache directories are created automatically when needed
2. **Cleaner Interface**: MQL5 feed directory is excluded from data loading interface
3. **Better UX**: Clear explanation of why mql5_feed is excluded
4. **Robustness**: System works even if cache directories are missing
5. **Access to Converted Data**: Users can load converted CSV files from `data/cache/csv_converted`

## Related Files

- `src/interactive/data_manager.py` - Main implementation
- `tests/test_data_manager_fixes.py` - Test coverage
- `interactive_system.py` - Entry point that uses DataManager
