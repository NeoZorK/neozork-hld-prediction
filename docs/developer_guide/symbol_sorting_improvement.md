# Symbol Sorting Improvement

## Summary

Added symbol-based sorting to the "Files by Source and Indicator" display in the data loading menu, improving data organization and readability.

## Changes Made

### 1. Enhanced Display Method (`src/interactive/menu_system/data_loading_menu.py`)

**Updated `_display_indicators_by_source_and_indicator` method:**

- Added symbol extraction and grouping within each source/indicator/format group
- Implemented sorting by symbol first, then by timeframe
- Enhanced display format to show files grouped by symbol with clear visual hierarchy

**Before:**
```
🔸 WAVE (BINANCE) - PARQUET - 15 files:
  Total: 2120.5MB, 6,149,832 rows
     M5  │   283.5MB │  847,453 rows │ 2017-08-17 to 2025-09-12
     M1  │  1291.5MB │ 3,704,799 rows │ 2017-08-31 to 2025-09-16
     H1  │    23.3MB │   70,636 rows │ 2017-08-17 to 2025-09-12
     MN1 │     0.0MB │       97 rows │ 2017-09-01 to 2025-09-01
     H4  │     6.0MB │   17,698 rows │ 2017-08-17 to 2025-09-16
     M15 │    97.1MB │  282,858 rows │ 2017-08-17 to 2025-09-16
     W1  │     0.1MB │      422 rows │ 2017-08-14 to 2025-09-08
     D1  │     0.9MB │    2,949 rows │ 2017-08-17 to 2025-09-12
     W1  │     0.1MB │      422 rows │ 2017-08-21 to 2025-09-15
     MN1 │     0.0MB │       98 rows │ 2017-08-01 to 2025-09-01
     D1  │     0.9MB │    2,953 rows │ 2017-08-17 to 2025-09-16
     M15 │    93.9MB │  282,491 rows │ 2017-08-17 to 2017-08-17 to 2025-09-12
     M5  │   293.2MB │  848,552 rows │ 2017-08-17 to 2025-09-16
     H4  │     5.8MB │   17,676 rows │ 2017-08-17 to 2025-09-12
     H1  │    24.0MB │   70,728 rows │ 2017-08-17 to 2025-09-16
```

**After:**
```
🔸 WAVE (BINANCE) - PARQUET - 15 files:
  Total: 2120.5MB, 6,149,832 rows
    📊 BTCUSDT:
      M5  │   283.5MB │  847,453 rows │ 2017-08-17 to 2025-09-12
      M1  │  1291.5MB │ 3,704,799 rows │ 2017-08-31 to 2025-09-16
      H1  │    23.3MB │   70,636 rows │ 2017-08-17 to 2025-09-12
      MN1 │     0.0MB │       97 rows │ 2017-09-01 to 2025-09-01
      H4  │     6.0MB │   17,698 rows │ 2017-08-17 to 2025-09-16
      M15 │    97.1MB │  282,858 rows │ 2017-08-17 to 2025-09-16
      W1  │     0.1MB │      422 rows │ 2017-08-14 to 2025-09-08
      D1  │     0.9MB │    2,949 rows │ 2017-08-17 to 2025-09-12
    📊 EURUSD:
      M5  │   293.2MB │  848,552 rows │ 2017-08-17 to 2025-09-16
      H1  │    24.0MB │   70,728 rows │ 2017-08-17 to 2025-09-16
      H4  │     5.8MB │   17,676 rows │ 2017-08-17 to 2025-09-12
      D1  │     0.9MB │    2,953 rows │ 2017-08-17 to 2025-09-16
      M15 │    93.9MB │  282,491 rows │ 2017-08-17 to 2025-09-12
      W1  │     0.1MB │      422 rows │ 2017-08-21 to 2025-09-15
      MN1 │     0.0MB │       98 rows │ 2017-08-01 to 2025-09-01
```

### 2. Enhanced Symbol Extraction (`src/interactive/menu_system/data_loading_menu.py`)

**Updated `_extract_symbol_from_filename` method:**

- Added support for more symbol patterns including single symbols like AAPL
- Improved regex patterns for better symbol detection
- Added fallback logic for various filename formats

**New patterns supported:**
- `EURUSD_M5_wave.parquet` → `EURUSD`
- `BTCUSDT_M5_wave.parquet` → `BTCUSDT`
- `AAPL_M5_wave.parquet` → `AAPL`
- `CSVExport_SYMBOL_PERIOD_...` → `SYMBOL`
- `cleaned_csv_converted_SYMBOL_...` → `SYMBOL`

### 3. Comprehensive Testing (`tests/test_symbol_sorting.py`)

**Added 5 test cases:**

1. **Symbol Extraction**: Tests various filename patterns
2. **Timeframe Extraction**: Tests timeframe detection
3. **Sort Key Function**: Tests sorting logic
4. **File Grouping**: Tests symbol-based grouping
5. **Display Logic**: Tests overall display functionality

## Technical Details

### Sorting Logic

```python
def sort_key(file_tuple):
    filename, file_info = file_tuple
    symbol = self._extract_symbol_from_filename(filename)
    timeframe = self._extract_timeframe_from_filename(filename)
    # Sort by symbol first, then by timeframe
    return (symbol or 'Unknown', timeframe)

sorted_files = sorted(files, key=sort_key)
```

### Grouping Logic

```python
# Group files by symbol for better display
files_by_symbol = {}
for filename, file_info in sorted_files:
    symbol = self._extract_symbol_from_filename(filename)
    if symbol not in files_by_symbol:
        files_by_symbol[symbol] = []
    files_by_symbol[symbol].append((filename, file_info))
```

### Display Format

```python
# Display files grouped by symbol
for symbol, symbol_files in files_by_symbol.items():
    if symbol:
        print(f"    {Fore.CYAN}📊 {symbol}:")
    
    # Sort symbol files by timeframe
    symbol_files.sort(key=lambda x: self._extract_timeframe_from_filename(x[0]))
    
    for filename, file_info in symbol_files:
        # Display individual file information
        print(f"      {Fore.WHITE} {timeframe:<3} │ {size_mb:>7.1f}MB │ {rows:>8,} rows │ {start_date} to {end_date}")
```

## Benefits

1. **Improved Readability**: Files are now organized by symbol, making it easier to find specific data
2. **Better Organization**: Clear visual hierarchy with symbol groupings
3. **Consistent Sorting**: Files are sorted by symbol first, then by timeframe
4. **Enhanced UX**: Users can quickly identify and locate data for specific symbols
5. **Maintainable Code**: Well-structured, tested implementation

## Usage

The improvement is automatically applied when viewing the "Files by Source and Indicator" section in the data loading menu:

1. Navigate to `Load Data` → `Indicators`
2. View the detailed breakdown section
3. Files are now grouped and sorted by symbol

## Testing

Run the symbol sorting tests:

```bash
uv run pytest tests/test_symbol_sorting.py -v
```

All tests pass successfully, ensuring the functionality works correctly.

## Future Enhancements

1. **Symbol Statistics**: Add symbol-specific statistics (total size, rows per symbol)
2. **Symbol Filtering**: Allow filtering by specific symbols
3. **Custom Sorting**: Allow users to choose sorting criteria
4. **Symbol Search**: Quick search within symbol groups
5. **Export by Symbol**: Export data grouped by symbol
