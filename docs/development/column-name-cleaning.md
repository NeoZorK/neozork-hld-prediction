# Column Name Cleaning in DataManager

## Overview

The DataManager now includes automatic column name cleaning functionality to handle CSV files with dirty headers containing tabs (`\t`), trailing commas, and extra spaces. This is particularly useful for CSV files exported from MetaTrader 5 (MT5) which often contain these formatting artifacts.

## Problem Description

When loading CSV files from MT5 exports, column headers often contain:
- Tab characters (`\t`) at the beginning of column names
- Trailing commas (`,`) at the end of column names
- Extra whitespace around column names

### Example of Problematic Headers

```csv
DateTime,	TickVolume,	Open,	High,	Low,	Close,	predicted_low,predicted_high,pressure,pressure_vector,
```

This results in column names like:
- `'DateTime'` ✅ (clean)
- `'\tTickVolume'` ❌ (contains tab)
- `'\tOpen'` ❌ (contains tab)
- `'\tHigh'` ❌ (contains tab)
- `'\tLow'` ❌ (contains tab)
- `'\tClose'` ❌ (contains tab)
- `'\tpredicted_low'` ❌ (contains tab)
- `'predicted_high'` ✅ (clean)
- `'pressure'` ✅ (clean)
- `'pressure_vector'` ✅ (clean)

## Solution Implementation

### 1. New Method: `_clean_column_names()`

Added a new method to the DataManager class that automatically cleans column names:

```python
def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names by removing tabs, extra spaces, and trailing commas."""
    original_columns = df.columns.tolist()
    cleaned_columns = []
    
    for col in original_columns:
        # Remove tabs, extra spaces, and trailing commas
        cleaned_col = str(col).replace('\t', '').strip().rstrip(',')
        cleaned_columns.append(cleaned_col)
    
    # Check if any columns were actually cleaned
    if cleaned_columns != original_columns:
        print(f"✅ Cleaned column names (removed tabs and trailing commas)")
        print(f"   Before: {original_columns}")
        print(f"   After:  {cleaned_columns}")
        df.columns = cleaned_columns
    
    return df
```

### 2. Integration Points

The column cleaning is automatically applied in:

1. **`_load_csv_direct()`** - For direct CSV loading
2. **`_load_csv_in_chunks()`** - For chunked CSV loading (first chunk only)
3. **`_detect_datetime_columns()`** - For datetime column detection

### 3. Cleaning Process

The cleaning process removes:
- **Tab characters** (`\t`) from anywhere in column names
- **Trailing commas** (`,`) from the end of column names
- **Extra whitespace** from the beginning and end of column names

## Usage Examples

### Before Cleaning
```python
# Column names with artifacts
columns = ['DateTime', '\tTickVolume', '\tOpen', '\tHigh', '\tLow', '\tClose', '\tpredicted_low', 'predicted_high', 'pressure', 'pressure_vector']
```

### After Cleaning
```python
# Clean column names
columns = ['DateTime', 'TickVolume', 'Open', 'High', 'Low', 'Close', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
```

## Console Output

When column cleaning is performed, the system provides informative output:

```
✅ Cleaned column names (removed tabs and trailing commas)
   Before: ['DateTime', '\tTickVolume', '\tOpen', '\tHigh', '\tLow', '\tClose', '\tpredicted_low', 'predicted_high', 'pressure', 'pressure_vector', 'Unnamed: 10']
   After:  ['DateTime', 'TickVolume', 'Open', 'High', 'Low', 'Close', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector', 'Unnamed: 10']
```

## Testing

Comprehensive tests have been created in `tests/test_data_manager_column_cleaning.py` to verify:

1. **Tab removal** - Tests cleaning of column names containing `\t`
2. **Trailing comma removal** - Tests cleaning of column names ending with `,`
3. **Combined cleaning** - Tests cleaning of column names with both tabs and commas
4. **No changes needed** - Tests that clean column names remain unchanged
5. **Extra space removal** - Tests cleaning of column names with extra whitespace
6. **CSV loading integration** - Tests the complete CSV loading process with dirty headers

### Running Tests

```bash
# Run specific test file
uv run pytest tests/test_data_manager_column_cleaning.py -v

# Run all tests
uv run pytest tests -n auto
```

## Benefits

1. **Improved Data Quality** - Clean column names make data analysis easier
2. **Better User Experience** - No more confusing `\t` characters in column names
3. **Consistent Formatting** - All CSV files are standardized regardless of source
4. **Automatic Processing** - No manual intervention required
5. **Backward Compatibility** - Clean column names are not affected

## File Types Supported

This functionality works with:
- **CSV files** - Primary target for MT5 exports
- **Any pandas DataFrame** - The cleaning method can be applied to any DataFrame
- **Chunked loading** - Works with both direct and chunked CSV loading

## Future Enhancements

Potential improvements could include:
- Support for other special characters (e.g., `\n`, `\r`)
- Configurable cleaning rules
- Custom column name mapping
- Support for other file formats (Excel, JSON, etc.)
