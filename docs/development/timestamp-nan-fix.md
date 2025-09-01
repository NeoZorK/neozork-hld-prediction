# Timestamp NaN Issue Fix

## Problem Description

When running the interactive system and loading EURUSD data, users encountered NaN values in the Timestamp column:

```
Data Quality Check: Missing values (NaN)
    Timestamp: 12195313 missing (99.46%)
      Example rows with NaN in Timestamp:
      Low   Close    High    Open  Volume  predicted_low  predicted_high  pressure  pressure_vector                         source_file Timestamp
0  0.5369  0.5369  0.5369  0.5369     1.0            0.0             0.0       0.0              0.0  CSVExport_EURUSD_PERIOD_M5.parquet       NaT
1  0.5366  0.5366  0.5366  0.5366     1.0            0.0             0.0       0.0              0.0  CSVExport_EURUSD_PERIOD_M5.parquet       NaT
2  0.5365  0.5365  0.5365  0.5365     1.0            0.0             0.0       0.0              0.0  CSVExport_EURUSD_PERIOD_M5.parquet       NaT
```

## Root Cause Analysis

The issue was caused by inconsistent handling of DatetimeIndex during parquet file loading:

1. **Mixed File Structures**: Some parquet files had DatetimeIndex with name 'Timestamp', while others were loaded without preserving the index structure.

2. **Chunked Loading Issue**: When loading large parquet files in chunks using `pyarrow.parquet.ParquetFile.iter_batches()`, the DatetimeIndex was lost because each chunk was loaded as a regular DataFrame without index.

3. **Concatenation Logic**: The system detected mixed structures (some files with Timestamp column, others without) and created dummy Timestamp columns filled with `pd.NaT` for files that didn't have the column.

## Solution Implementation

### 1. Enhanced DatetimeIndex Detection

Modified `_load_parquet_with_optimization()` method to detect DatetimeIndex before loading:

```python
# First, check if the file has a datetime index by reading a small sample
first_row_group = parquet_file.read_row_group(0)
sample_df = first_row_group.to_pandas()
has_datetime_index = isinstance(sample_df.index, pd.DatetimeIndex)
datetime_index_name = sample_df.index.name if has_datetime_index else None
```

### 2. Preserved DatetimeIndex for Large Files

For files with DatetimeIndex, the system now loads the entire file to preserve the index structure:

```python
if has_datetime_index:
    print(f"📅 Detected DatetimeIndex: {datetime_index_name}, preserving during chunked loading...")
    
    # For files with DatetimeIndex, we need to load the entire file to preserve the index
    # This is because pyarrow chunks don't preserve the index structure
    if total_rows > 5000000:  # 5M rows threshold
        print(f"⚠️  Very large file with DatetimeIndex detected ({total_rows:,} rows).")
        print(f"   Loading entire file to preserve index structure (this may use significant memory)...")
    else:
        print(f"   Loading entire file to preserve index structure...")
    
    df = pd.read_parquet(file_path)
    return self._handle_datetime_index(df)
```

### 3. Improved Concatenation Logic

The concatenation logic now properly handles DatetimeIndex:

```python
if has_datetime_index:
    # Convert DatetimeIndex to 'Timestamp' column for consistent concatenation
    processed_data = []
    for df in all_data:
        df_copy = df.copy()
        if isinstance(df_copy.index, pd.DatetimeIndex):
            # Reset index to make datetime a column
            df_copy = df_copy.reset_index()
            # Rename the index column if it's unnamed
            if df_copy.columns[0] == 'index':
                df_copy = df_copy.rename(columns={'index': 'Timestamp'})
        processed_data.append(df_copy)
    
    # Combine DataFrames with consistent column structure
    combined_data = pd.concat(processed_data, ignore_index=True)
```

## Testing

Created comprehensive tests in `tests/interactive/test_timestamp_fix.py`:

1. **Unit Tests**: Test individual methods for handling DatetimeIndex
2. **Integration Tests**: Test loading parquet files with and without DatetimeIndex
3. **Mixed Data Tests**: Test concatenation of files with different structures
4. **Real Data Tests**: Test with actual EURUSD files

All tests pass and verify that:
- No NaN values are created in Timestamp column
- DatetimeIndex is properly preserved
- Mixed file structures are handled correctly

## Performance Considerations

- **Memory Usage**: Large files with DatetimeIndex are loaded entirely to preserve structure
- **Threshold**: 5M rows threshold for warning about memory usage
- **Fallback**: Chunked loading still used for files without DatetimeIndex

## Files Modified

- `src/interactive/data_manager.py`: Enhanced parquet loading logic
- `tests/interactive/test_timestamp_fix.py`: Added comprehensive tests

## Verification

The fix was verified by:

1. **Manual Testing**: Running interactive system with EURUSD data
2. **Automated Testing**: Running comprehensive test suite
3. **Real Data Validation**: Testing with actual EURUSD parquet files

## Result

✅ **Problem Solved**: No more NaN values in Timestamp column
✅ **Data Integrity**: All timestamp information preserved
✅ **Performance**: Maintained memory optimization for appropriate cases
✅ **Compatibility**: Works with both DatetimeIndex and regular column structures
