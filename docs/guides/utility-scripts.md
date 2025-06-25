# Utility Scripts

This document describes the utility scripts available in the `scripts/` folder for managing test data and indicator files.

## Overview

The project includes several utility scripts to help with data conversion, test file creation, and indicator file management. These scripts are primarily used for testing, development, and maintaining data consistency across different formats.

## Available Scripts

### 1. `recreate_csv.py` - JSON to CSV Converter

**Purpose**: Converts JSON indicator files to CSV format, specifically designed for recreating missing CSV test files from existing JSON sources.

**Location**: `scripts/recreate_csv.py`

**Usage**:
```bash
cd /workspaces/neozork-hld-prediction
python scripts/recreate_csv.py
```

**What it does**:
- Scans `data/indicators/json/` for files matching `*UNKNOWN*.json` pattern
- Converts each JSON file to a corresponding CSV file in `data/indicators/csv/`
- Handles datetime index conversion for proper CSV formatting
- Provides detailed output with row/column counts
- Creates the CSV directory if it doesn't exist

**When to use**:
- When CSV indicator files are missing or corrupted
- After creating new JSON test files that need CSV equivalents
- During testing when you need to ensure all three formats (parquet, CSV, JSON) are available
- When migrating or backing up indicator data

**Example output**:
```
Found 2 JSON files to convert:

📄 Processing: UNKNOWN_D1_PressureVector.json
✅ Created: data/indicators/csv/UNKNOWN_D1_PressureVector.csv
   Rows: 100, Columns: 5

📄 Processing: UNKNOWN_D1_SupportResistants.json
✅ Created: data/indicators/csv/UNKNOWN_D1_SupportResistants.csv
   Rows: 100, Columns: 4

🎉 Conversion complete!
📁 Check the CSV files in: data/indicators/csv
```

### 2. `create_test_parquet.py` - JSON to Parquet Converter

**Purpose**: Converts JSON indicator files to Parquet format for efficient storage and analysis.

**Location**: `scripts/create_test_parquet.py`

**Usage**:
```bash
cd /workspaces/neozork-hld-prediction
python scripts/create_test_parquet.py
```

**What it does**:
- Scans `data/indicators/json/` for all JSON files (`*.json`)
- Converts each JSON file to a corresponding Parquet file in `data/indicators/parquet/`
- Properly handles datetime index conversion and DataFrame indexing
- Optimizes data storage using Parquet's columnar format
- Creates the Parquet directory if it doesn't exist

**When to use**:
- When Parquet indicator files are missing or need regeneration
- After creating new JSON indicator files that need Parquet equivalents
- When optimizing storage space and read performance for large datasets
- During development when testing different data formats

**Example output**:
```
Found 2 JSON files to convert:

📄 Processing: UNKNOWN_D1_PressureVector.json
✅ Created: data/indicators/parquet/UNKNOWN_D1_PressureVector.parquet
   Rows: 100, Columns: 5

📄 Processing: UNKNOWN_D1_SupportResistants.json
✅ Created: data/indicators/parquet/UNKNOWN_D1_SupportResistants.parquet
   Rows: 100, Columns: 4

🎉 Conversion complete!
📁 Check the parquet files in: data/indicators/parquet
```

## Data Format Requirements

### JSON Source Files
The JSON files should contain structured data that can be converted to pandas DataFrame:
```json
{
  "index": ["2024-01-01", "2024-01-02", ...],
  "column1": [value1, value2, ...],
  "column2": [value1, value2, ...],
  ...
}
```

### Output Formats

**CSV Files**:
- Human-readable text format
- Suitable for terminal display and external tools
- Index column converted to string format (YYYY-MM-DD)
- No index column in output (index=False)

**Parquet Files**:
- Binary columnar format optimized for analytics
- Suitable for plotting and data analysis
- Datetime index properly preserved
- Compressed storage for better performance

## Integration with CLI

These utility scripts support the CLI testing workflow:

```bash
# View all indicator files
python run_analysis.py show ind

# View specific formats
python run_analysis.py show ind parquet
python run_analysis.py show ind csv  
python run_analysis.py show ind json

# Test with specific files
python run_analysis.py show ind parquet PressureVector
```

## Troubleshooting

### Common Issues

1. **Permission Errors**:
   ```bash
   chmod +x scripts/recreate_csv.py
   chmod +x scripts/create_test_parquet.py
   ```

2. **Missing Dependencies**:
   ```bash
   pip install pandas pyarrow
   ```

3. **Directory Not Found**:
   - The scripts automatically create missing directories
   - Ensure you're running from the project root directory

4. **JSON Format Issues**:
   - Verify JSON files are valid and contain expected structure
   - Check that 'index' column exists if datetime handling is needed

### Debugging

Add verbose output by modifying the scripts:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Development Notes

### Adding New Converters

To add new format converters:

1. Create a new script in `scripts/` folder
2. Follow the same pattern as existing scripts
3. Add error handling and progress reporting
4. Update this documentation

### Testing the Scripts

```bash
# Test CSV recreation
python scripts/recreate_csv.py

# Test Parquet creation  
python scripts/create_test_parquet.py

# Verify all formats exist
find data/indicators -name "*UNKNOWN*" -type f | sort
```

## Related Documentation

- [Project Structure](project-structure.md) - Overview of directory layout
- [Testing](testing.md) - How these scripts fit into testing workflow
- [Getting Started](getting-started.md) - Initial setup instructions
- [Scripts Documentation](scripts.md) - Other available scripts

## Version Control Notes

These utility scripts are designed to work with the project's git ignore patterns:
- `*UNKNOWN*` test files are explicitly tracked despite global ignore patterns
- Generated files are properly included in version control
- Scripts can be run safely without affecting git status
