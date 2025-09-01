# CSV Loading Fix for Metadata Headers

## Problem Description

When loading CSV files with metadata headers (common in MT5 exports), the DataManager was incorrectly interpreting the metadata row as data, causing all timestamp values to become NaN (missing values >90%).

### Example of Problematic CSV Format

```csv
2025.04.22 12:42	TF = PERIOD_D1	EURUSD
DateTime,	TickVolume,	Open,	High,	Low,	Close,	predicted_low,predicted_high,pressure,pressure_vector,
1971.01.04 00:00,1,0.53690000,0.53690000,0.53690000,0.53690000,0.00000,0.00000,0.00000,0.00000,
1971.01.05 00:00,1,0.53660000,0.53660000,0.53660000,0.53660000,0.00000,0.00000,0.00000,0.00000,
```

### Issue Details

- **First row**: Metadata information (not data)
- **Second row**: Actual column headers
- **Third row onwards**: Data rows

The original code was using `pd.read_csv(file_path)` without specifying the correct header row, causing:
- First row (metadata) to be treated as data
- All timestamp values to become NaN
- Data quality check showing "99.46% missing timestamps"

## Solution Implementation

### 1. Header Detection Logic

Added intelligent header detection in `DataManager`:

```python
def _determine_header_row(self, file_path: Path) -> int:
    """Determine the correct header row for CSV file."""
    # Check if second line contains 'DateTime' (indicating it's the header)
    if 'DateTime' in second_line:
        # First line is metadata, second line is header
        return 1
    elif 'DateTime' in first_line:
        # First line is header
        return 0
    else:
        # Try to detect by checking if first line looks like data
        if any(char.isdigit() for char in first_line[:20]):
            return None  # No header
        else:
            return 0  # Default to first row as header
```

### 2. Refactored CSV Loading Methods

- **`_load_csv_with_datetime_handling`**: Now determines header row first, then detects datetime columns
- **`_load_csv_direct`**: Uses determined header row for loading
- **`_load_csv_in_chunks`**: Uses determined header row for chunked loading
- **`_detect_datetime_columns`**: Detects datetime columns with correct header

### 3. Improved Error Handling

- Better detection of different CSV formats
- Graceful fallback for edge cases
- Clear logging of header detection decisions

## Testing

### Test Cases Created

1. **`test_load_csv_with_metadata_header`**: Tests MT5 format with metadata
2. **`test_load_csv_without_metadata_header`**: Tests standard CSV format
3. **`test_load_csv_no_header`**: Tests CSV without headers

### Test Results

```bash
✅ Test passed: CSV with metadata header loaded correctly
✅ Test passed: Standard CSV without metadata header loaded correctly
✅ Test passed: CSV without header loaded correctly
```

### Real File Testing

Tested with actual EURUSD file:
- **DateTime column type**: datetime64[ns] ✅
- **DateTime null count**: 0 ✅
- **Total rows**: 13,996 ✅
- **First few DateTime values**: 1971-01-04, 1971-01-05, etc. ✅

## Files Modified

1. **`src/interactive/data_manager.py`**:
   - Added `_determine_header_row()` method
   - Added `_detect_datetime_columns()` method
   - Updated `_load_csv_with_datetime_handling()` method
   - Updated `_load_csv_direct()` method
   - Updated `_load_csv_in_chunks()` method

2. **`tests/interactive/test_data_manager_fix.py`**:
   - Created comprehensive test suite
   - Tests all CSV format variations
   - Validates datetime parsing

## Usage

The fix is automatically applied when using the interactive system:

```bash
./interactive_system.py
# Menu Load Data -> "3 eurusd"
```

### Before Fix
```
🔍 COMPREHENSIVE DATA QUALITY CHECK
==================================================
  Data Quality Check: Missing values (NaN)
    Timestamp: 12195313 missing (99.46%)
```

### After Fix
```
✅ Detected metadata header, using row 1 as column headers
✅ Parsed datetime column: DateTime
DataFrame shape: (13996, 11)
DateTime null count: 0
```

## Compatibility

The fix maintains backward compatibility with:
- Standard CSV files (no metadata)
- CSV files without headers
- Existing parquet files
- All other data formats

## Performance Impact

- Minimal performance impact
- Header detection only reads first 2 lines
- No changes to memory optimization
- Maintains chunked loading for large files

## Future Enhancements

1. Support for more metadata formats
2. Automatic detection of different CSV dialects
3. Enhanced logging for debugging
4. Support for custom header patterns
