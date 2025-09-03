# Data Module

This module provides comprehensive data handling capabilities for the neozork-hld-prediction project.

## Structure

### Gap Fixing (`gap_fixing/`)
Handles time series gap detection and fixing using various algorithms:
- **core.py** - Main GapFixer class and orchestration
- **algorithms.py** - Strategy selection and algorithm management
- **interpolation.py** - Various interpolation methods (linear, cubic, seasonal, etc.)
- **explanation.py** - Documentation and explanation functions
- **utils.py** - Utility functions for gap fixing operations

### Data Acquisition (`acquisition/`)
Manages data acquisition from various sources:
- **core.py** - Main acquisition orchestration
- **csv.py** - CSV data acquisition functionality
- **cache.py** - Data caching and management
- **ranges.py** - Date range calculations and validation
- **utils.py** - Acquisition utility functions
- **processing.py** - Data processing during acquisition

### Data Processing (`processing/`)
Handles data processing and transformation:
- **csv_processor.py** - Individual CSV file processing
- **csv_folder_processor.py** - Folder-level CSV processing orchestration

### Utilities (`utils/`)
Placeholder for future utility modules.

## Usage

### Basic Import
```python
from src.data import GapFixer, acquire_data, CSVFolderProcessor
```

### Gap Fixing
```python
from src.data.gap_fixing import GapFixer

fixer = GapFixer()
success, results = fixer.fix_file_gaps(file_path)
```

### Data Acquisition
```python
from src.data.acquisition import acquire_data

data = acquire_data('EURUSD', mode='csv', start_date='2024-01-01')
```

### CSV Processing
```python
from src.data.processing import process_csv_folder

results = process_csv_folder('path/to/csv/folder', rule='OHLCV')
```

## Features

- **Gap Detection**: Advanced algorithms for detecting time series gaps
- **Multiple Interpolation Methods**: Linear, cubic, seasonal, and ML-based approaches
- **Data Caching**: Efficient caching system for acquired data
- **Flexible Processing**: Support for various data formats and processing rules
- **Memory Management**: Built-in memory optimization for large datasets
- **Export Support**: Multiple export formats (CSV, Parquet, JSON)

## Requirements

- pandas
- numpy
- tqdm
- psutil

## Notes

- All files are kept under 300 lines for maintainability
- 100% backward compatibility maintained
- Comprehensive error handling and logging
- All functionality preserved during refactoring
