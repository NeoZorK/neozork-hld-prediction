# Data Cleaning API Reference

## DataValidator Class

### Methods

#### `validate_file_path(filename: str, supported_dirs: List[str]) -> Optional[Dict[str, Any]]`

Validates if file exists in supported directories and extracts metadata.

**Parameters:**
- `filename`: Name of the file to validate
- `supported_dirs`: List of supported directory paths

**Returns:**
- Dictionary with file metadata if valid, None otherwise

**Example:**
```python
validator = DataValidator()
file_info = validator.validate_file_path("BTCUSD_1h.parquet", supported_dirs)
if file_info:
    print(f"Symbol: {file_info['symbol']}")
    print(f"Format: {file_info['format']}")
```

#### `get_supported_directories() -> List[str]`

Get list of supported data directories.

**Returns:**
- List of supported directory paths

#### `validate_directory_structure(base_path: str = ".") -> Dict[str, bool]`

Validate that all required directories exist.

**Parameters:**
- `base_path`: Base path to check directories from

**Returns:**
- Dictionary mapping directory names to existence status

## FileOperations Class

### Methods

#### `load_data(file_path: str, format_type: str) -> Optional[pd.DataFrame]`

Load data from file in specified format.

**Parameters:**
- `file_path`: Path to the data file
- `format_type`: Format of the file (parquet, json, csv)

**Returns:**
- DataFrame with loaded data or None if error

**Example:**
```python
file_ops = FileOperations()
data = file_ops.load_data("data.parquet", "parquet")
```

#### `save_data(data: pd.DataFrame, file_path: str, format_type: str) -> None`

Save data to file in specified format.

**Parameters:**
- `data`: DataFrame to save
- `file_path`: Path where to save the file
- `format_type`: Format to save in (parquet, json, csv)

#### `get_file_info(file_path: str) -> Dict[str, Any]`

Get basic file information.

**Parameters:**
- `file_path`: Path to the file

**Returns:**
- Dictionary with file information

#### `backup_file(file_path: str, backup_suffix: str = '.backup') -> str`

Create a backup of the file.

**Parameters:**
- `file_path`: Path to the file to backup
- `backup_suffix`: Suffix to add to backup filename

**Returns:**
- Path to the backup file

#### `validate_data_integrity(data: pd.DataFrame) -> Dict[str, Any]`

Validate data integrity and return statistics.

**Parameters:**
- `data`: DataFrame to validate

**Returns:**
- Dictionary with validation results

#### `optimize_dataframe(data: pd.DataFrame) -> pd.DataFrame`

Optimize DataFrame memory usage.

**Parameters:**
- `data`: DataFrame to optimize

**Returns:**
- Optimized DataFrame

## CleaningProcedures Class

### Detection Methods

#### `detect_gaps(data: pd.DataFrame) -> List[Dict[str, Any]]`

Detect gaps in time series data.

**Parameters:**
- `data`: DataFrame with time series data

**Returns:**
- List of gap information dictionaries

#### `detect_duplicates(data: pd.DataFrame) -> List[Dict[str, Any]]`

Detect duplicate rows in the data.

**Parameters:**
- `data`: DataFrame to analyze

**Returns:**
- List of duplicate information dictionaries

#### `detect_nan(data: pd.DataFrame) -> List[Dict[str, Any]]`

Detect NaN values in the data.

**Parameters:**
- `data`: DataFrame to analyze

**Returns:**
- List of NaN information dictionaries

#### `detect_zeros(data: pd.DataFrame) -> List[Dict[str, Any]]`

Detect zero values in numeric columns.

**Parameters:**
- `data`: DataFrame to analyze

**Returns:**
- List of zero values information dictionaries

#### `detect_negative(data: pd.DataFrame) -> List[Dict[str, Any]]`

Detect negative values in numeric columns.

**Parameters:**
- `data`: DataFrame to analyze

**Returns:**
- List of negative values information dictionaries

#### `detect_infinity(data: pd.DataFrame) -> List[Dict[str, Any]]`

Detect infinite values in numeric columns.

**Parameters:**
- `data`: DataFrame to analyze

**Returns:**
- List of infinity values information dictionaries

#### `detect_outliers(data: pd.DataFrame) -> List[Dict[str, Any]]`

Detect outliers in numeric columns using multiple methods.

**Parameters:**
- `data`: DataFrame to analyze

**Returns:**
- List of outliers information dictionaries

### Fixing Methods

#### `fix_issues(data: pd.DataFrame, procedure: str, issues: List[Dict[str, Any]]) -> pd.DataFrame`

Fix detected issues based on the procedure type.

**Parameters:**
- `data`: DataFrame to fix
- `procedure`: Type of procedure (gaps, duplicates, nan, etc.)
- `issues`: List of detected issues

**Returns:**
- Fixed DataFrame

## ProgressTracker Class

### Methods

#### `run_with_progress(func: Callable, *args, **kwargs) -> Any`

Run a function with progress tracking.

**Parameters:**
- `func`: Function to run
- `*args`: Arguments for the function
- `**kwargs`: Keyword arguments for the function

**Returns:**
- Result of the function execution

#### `start_operation(total_steps: int, operation_name: str = "Operation")`

Start a multi-step operation.

**Parameters:**
- `total_steps`: Total number of steps
- `operation_name`: Name of the operation

#### `update_step(step_name: str, step_number: Optional[int] = None)`

Update current step.

**Parameters:**
- `step_name`: Name of the current step
- `step_number`: Step number (if None, increments current step)

#### `finish_operation()`

Finish the current operation.

#### `create_detailed_progress(data: pd.DataFrame, operation_name: str) -> DetailedProgressTracker`

Create a detailed progress tracker for data operations.

**Parameters:**
- `data`: DataFrame being processed
- `operation_name`: Name of the operation

**Returns:**
- DetailedProgressTracker instance

## DetailedProgressTracker Class

### Methods

#### `update(processed_rows: int)`

Update progress.

**Parameters:**
- `processed_rows`: Number of rows processed so far

#### `finish()`

Finish the detailed progress tracking.

## BatchProgressTracker Class

### Methods

#### `start_batch(batch_number: int, batch_info: str = "")`

Start a new batch.

**Parameters:**
- `batch_number`: Batch number
- `batch_info`: Additional batch information

#### `finish()`

Finish batch processing.

## CleaningReporter Class

### Methods

#### `show_detailed_results(procedure_name: str, issues: List[Dict[str, Any]], data: pd.DataFrame) -> None`

Show detailed results for a specific cleaning procedure.

**Parameters:**
- `procedure_name`: Name of the cleaning procedure
- `issues`: List of detected issues
- `data`: Original DataFrame

#### `show_final_report(file_info: Dict[str, Any], cleaning_results: Dict[str, Any]) -> None`

Show comprehensive final report of the cleaning process.

**Parameters:**
- `file_info`: Original file metadata
- `cleaning_results`: Results from all cleaning procedures

#### `save_report(file_info: Dict[str, Any], cleaning_results: Dict[str, Any], output_path: str) -> None`

Save detailed report to file.

**Parameters:**
- `file_info`: Original file metadata
- `cleaning_results`: Results from all cleaning procedures
- `output_path`: Path to save the report

#### `generate_summary_stats(cleaning_results: Dict[str, Any]) -> Dict[str, Any]`

Generate summary statistics for the cleaning process.

**Parameters:**
- `cleaning_results`: Results from all cleaning procedures

**Returns:**
- Dictionary with summary statistics

## DataCleaningTool Class

### Methods

#### `validate_file_path(filename: str) -> Optional[Dict[str, Any]]`

Validate if the file exists in supported directories.

**Parameters:**
- `filename`: Name of the file to validate

**Returns:**
- Dictionary with file metadata if valid, None otherwise

#### `display_file_info(file_info: Dict[str, Any]) -> None`

Display comprehensive file information.

**Parameters:**
- `file_info`: Dictionary containing file metadata

#### `display_cleaning_procedures() -> None`

Display information about cleaning procedures.

#### `run_cleaning_procedures(file_info: Dict[str, Any]) -> Dict[str, Any]`

Run all cleaning procedures on the data.

**Parameters:**
- `file_info`: Dictionary containing file metadata

**Returns:**
- Dictionary with cleaning results

#### `save_cleaned_data(file_info: Dict[str, Any], cleaning_results: Dict[str, Any]) -> str`

Save cleaned data to the specified path structure.

**Parameters:**
- `file_info`: Original file metadata
- `cleaning_results`: Results from cleaning procedures

**Returns:**
- Path where data was saved

#### `run(filename: str) -> None`

Main execution method.

**Parameters:**
- `filename`: Name of the file to process

## Error Handling

### Common Exceptions

#### `FileNotFoundError`
Raised when trying to load a file that doesn't exist.

#### `ValueError`
Raised when using unsupported file formats or invalid parameters.

#### `Exception`
General exceptions during data processing are caught and logged.

### Error Recovery

The system includes comprehensive error handling:

- **File Loading Errors**: Graceful fallback with informative messages
- **Data Processing Errors**: Continues with other procedures if one fails
- **User Input Errors**: Clear error messages with retry prompts
- **System Errors**: Comprehensive logging and error reporting

## Configuration

### Environment Variables

No environment variables are required. The system uses default configurations.

### File Naming Conventions

The system automatically detects file types based on naming patterns:

- **CSV Converted**: `SYMBOL_PERIOD_TIMEFRAME.parquet`
- **Raw Parquet**: `source_SYMBOL_TIMEFRAME.parquet`
- **Indicators**: `source_SYMBOL_TIMEFRAME_indicator.format`

### Supported Formats

- **Parquet**: `.parquet` files using PyArrow
- **JSON**: `.json` files with automatic orientation detection
- **CSV**: `.csv` files with automatic delimiter detection

## Performance Considerations

### Memory Usage

- Data is loaded in chunks when possible
- Memory usage is optimized through data type downcasting
- Large datasets are processed efficiently

### Processing Speed

- Progress tracking adds minimal overhead
- Parallel processing where applicable
- Efficient algorithms for data cleaning

### Storage

- Backup files are created before modifications
- Optimized file formats for storage
- Compressed output when possible
