# Pressure Vector Negative Values - Fix Implementation

## Overview

This document describes the fix implemented to allow `pressure_vector` column to contain negative values without being automatically flagged as data quality issues or automatically corrected.

## Problem Description

**Issue**: The `pressure_vector` column was being treated like other OHLCV columns, where negative values were considered data quality issues and automatically corrected.

**Root Cause**: The data quality check and fix functions were treating all numeric columns equally, without considering that `pressure_vector` can legitimately contain negative values as part of its calculation logic.

## Solution Implemented

### 1. Modified Data Quality Check (`src/eda/data_quality.py`)

**Function**: `negative_check()`

**Changes**:
- Added special handling for `pressure_vector` column
- Negative values in `pressure_vector` are now displayed as "expected" rather than flagged as issues
- `pressure_vector` is excluded from the `negative_summary` list

**Code Changes**:
```python
# Skip pressure_vector as it can legitimately be negative
if col.lower() == 'pressure_vector':
    n_negatives_sample = (sample_df[col] < 0).sum()
    if n_negatives_sample > 0:
        estimated_negatives = int((n_negatives_sample / sample_size) * len(df))
        estimated_percent = 100 * estimated_negatives / len(df)
        print(f"    {Fore.CYAN}{col}{Style.RESET_ALL}: ~{estimated_negatives} negatives ({estimated_percent:.2f}%) [expected for pressure_vector]")
    continue
```

### 2. Modified Fix Functions (`src/eda/fix_files.py`)

**Function**: `fix_negatives()`

**Changes**:
- Added explicit check to skip `pressure_vector` column during automatic fixes
- `pressure_vector` negative values are preserved during data cleaning operations

**Code Changes**:
```python
# Skip pressure_vector as it can legitimately be negative
if col.lower() == 'pressure_vector':
    print(f"Skipping pressure_vector column as it can legitimately contain negative values")
    continue
```

### 3. Updated Memory Settings

**File**: `src/eda/data_quality.py`

**Changes**:
- Increased memory limits to match DataManager settings
- Updated thresholds for large dataset processing

```python
def _get_memory_settings() -> Dict[str, int]:
    return {
        'max_memory_mb': int(os.environ.get('MAX_MEMORY_MB', '4096')),  # Increased from 1024
        'chunk_size': int(os.environ.get('CHUNK_SIZE', '50000')),  # Increased from 25000
        'sample_size': int(os.environ.get('SAMPLE_SIZE', '10000')),
        'enable_memory_optimization': os.environ.get('ENABLE_MEMORY_OPTIMIZATION', 'true').lower() == 'true'
    }
```

## Results

### Before Fix
```
Data Quality Check: Negative Values
  pressure_vector: ~6114992 negatives (48.58%) [estimated from sample]
  
Fixing negative values...
Fixed 6114992 negative values in column 'pressure_vector' by taking absolute values
```

### After Fix
```
Data Quality Check: Negative Values
  pressure_vector: ~6114992 negatives (48.58%) [expected for pressure_vector]
  
Fixing negative values...
Skipping pressure_vector column as it can legitimately contain negative values
```

## Testing

Comprehensive tests were created in `tests/eda/test_pressure_vector_negative_values.py`:

### Test Coverage
- **Negative Value Detection**: Tests that `pressure_vector` negative values are not flagged as issues
- **Fix Function**: Tests that `pressure_vector` is skipped during automatic fixes
- **Data Preservation**: Tests that negative values are preserved in `pressure_vector`
- **Other Columns**: Tests that other columns still get proper negative value detection
- **Case Insensitivity**: Tests that the fix works regardless of column name case
- **Large Datasets**: Tests handling in large datasets with sampling

### Test Results
```
✅ Passed: 7
❌ Failed: 0
⏭️  Skipped: 0
💥 Errors: 0
📈 Total: 7
```

## Impact

### Positive Impact
1. **Data Integrity**: `pressure_vector` negative values are preserved
2. **Correct Analysis**: Trading algorithms can properly interpret negative pressure vector values
3. **User Experience**: No false warnings about expected negative values
4. **Performance**: Reduced unnecessary data corrections

### Backward Compatibility
- All existing functionality remains unchanged
- Other columns continue to be processed normally
- No breaking changes to public APIs

## Configuration

The fix is automatic and requires no configuration. However, users can still override memory settings via environment variables:

```bash
export MAX_MEMORY_MB=8192      # 8GB
export CHUNK_SIZE=100000       # 100k rows per chunk
export SAMPLE_SIZE=20000       # 20k rows for sampling
```

## Future Considerations

1. **Other Special Columns**: Consider if other columns might have similar legitimate negative value requirements
2. **Configuration**: Could add a configuration file to specify which columns can have negative values
3. **Documentation**: Update user documentation to explain that `pressure_vector` can be negative

## Related Files

- `src/eda/data_quality.py` - Main data quality check functions
- `src/eda/fix_files.py` - Data fixing functions
- `tests/eda/test_pressure_vector_negative_values.py` - Test suite
- `docs/development/pressure-vector-negative-values.md` - This documentation
