# Timestamp Column Case Sensitivity Fix

## Problem Description

When loading data through the interactive system, users encountered the issue where timestamp columns were not being recognized:

```
⚠️  No timestamp column found in OHLCV data. Data will be loaded without datetime index.
   Available columns: ['Timestamp', 'Low', 'Close', 'High', 'Open', 'Volume', ...]
```

**Root Cause**: The system was only looking for timestamp columns with lowercase names (`['timestamp', 'time', 'date', 'datetime', 'dt']`), but the actual data contained a column named `Timestamp` (with uppercase 'T').

## Solution Implemented

### Enhanced Timestamp Column Detection

**File**: `src/interactive/data_loader.py`

Updated the `handle_datetime_index()` method to perform case-insensitive timestamp column detection:

```python
def handle_datetime_index(self, df: pd.DataFrame) -> pd.DataFrame:
    """Handle datetime index conversion."""
    if df is None or df.empty:
        return df
        
    # Check if index is already datetime
    if isinstance(df.index, pd.DatetimeIndex):
        return df
        
    # Look for common datetime column names (case-insensitive)
    datetime_columns = ['timestamp', 'time', 'date', 'datetime', 'dt']
    
    # First try exact matches
    for col in datetime_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df.set_index(col, inplace=True)
                print(f"✅ Set '{col}' as datetime index")
                return df
            except Exception:
                continue
    
    # Then try case-insensitive matches
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in datetime_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df.set_index(col, inplace=True)
                print(f"✅ Set '{col}' as datetime index (case-insensitive match)")
                return df
            except Exception:
                continue
```

### Enhanced Parquet Loading Logic

Also improved the `load_parquet_with_optimization()` method to better detect timestamp columns:

```python
# Check if file has datetime index or timestamp column
first_row_group = parquet_file.read_row_group(0)
sample_df = first_row_group.to_pandas()
has_datetime_index = isinstance(sample_df.index, pd.DatetimeIndex)
datetime_index_name = sample_df.index.name if has_datetime_index else None

# Also check for timestamp column in the data
has_timestamp_column = any(col.lower() in ['timestamp', 'time', 'date', 'datetime', 'dt'] 
                         for col in sample_df.columns)

if has_datetime_index or has_timestamp_column:
    if has_datetime_index:
        print(f"📅 Detected DatetimeIndex: {datetime_index_name}, preserving during loading...")
    else:
        print(f"📅 Detected timestamp column, preserving during loading...")
    
    # Load entire file to preserve timestamp structure
    df = pd.read_parquet(file_path)
    return self.handle_datetime_index(df)
```

## Test Coverage

Created comprehensive tests in `tests/interactive/test_timestamp_case_sensitivity.py`:

- ✅ `test_timestamp_column_detection_uppercase`: Tests 'Timestamp' column detection
- ✅ `test_timestamp_column_detection_lowercase`: Tests 'timestamp' column detection  
- ✅ `test_timestamp_column_detection_mixed_case`: Tests 'TimeStamp' column detection
- ✅ `test_no_timestamp_column_handling`: Tests handling of data without timestamp
- ✅ `test_already_datetime_index`: Tests handling of existing DatetimeIndex
- ✅ `test_invalid_timestamp_data`: Tests handling of invalid timestamp values

## User Experience Improvement

### Before (Timestamp Column Not Recognized)

```
🔄 Loading Parquet: CSVExport_EURUSD_PERIOD_M1.parquet
📊 Loading CSVExport_EURUSD_PERIOD_M1.parquet in chunks of 50,000 rows...
   📈 Progress: 100.0% (28,558,844 rows loaded) ✅ [572 chunks] ⏱️ Total time: 12.0s 🚀 Avg speed: 2378543 rows/s
⚠️  No timestamp column found in OHLCV data. Data will be loaded without datetime index.
   Available columns: ['Timestamp', 'Low', 'Close', 'High', 'Open', 'Volume', ...]
```

### After (Timestamp Column Properly Recognized)

```
🔄 Loading Parquet: CSVExport_EURUSD_PERIOD_M1.parquet
📅 Detected timestamp column, preserving during loading...
   Loading entire file to preserve timestamp structure...
✅ Set 'Timestamp' as datetime index (case-insensitive match)
```

## Benefits

1. **Improved Data Loading**: Timestamp columns are now properly detected regardless of case
2. **Better User Experience**: No more confusing warnings about missing timestamp columns
3. **Consistent Behavior**: Both uppercase and lowercase timestamp column names are supported
4. **Backward Compatibility**: Existing functionality remains unchanged
5. **Enhanced Detection**: Better detection of timestamp data in parquet files

## Files Modified

- `src/interactive/data_loader.py`: Enhanced timestamp column detection logic
- `tests/interactive/test_timestamp_case_sensitivity.py`: New comprehensive test suite

## Testing

All tests pass successfully:

```bash
✅ Passed: 6
❌ Failed: 0
⏭️  Skipped: 0
💥 Errors: 0
📈 Total: 6
```

## Future Improvements

Consider implementing:

1. **Configurable Timestamp Formats**: Allow users to specify custom timestamp formats
2. **Multiple Timestamp Columns**: Handle cases where multiple timestamp columns exist
3. **Automatic Timezone Detection**: Detect and handle timezone information in timestamps
4. **Performance Optimization**: Further optimize timestamp parsing for large datasets
