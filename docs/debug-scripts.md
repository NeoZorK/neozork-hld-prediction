# Debug Scripts Guide

Debugging utilities for testing connections, validating data, and troubleshooting issues.

## Overview

Debug scripts are located in `scripts/debug_scripts/` and provide specialized testing and validation tools for different components of the system.

## API Connection Testing

### Yahoo Finance Debug (`debug_yfinance.py`)
**Purpose:** Test Yahoo Finance API connectivity and data fetching

```bash
python scripts/debug_scripts/debug_yfinance.py
```

**What it tests:**
- Yahoo Finance API accessibility
- Data fetching for common symbols
- Response format validation
- Error handling

**Output example:**
```
🔍 Testing Yahoo Finance Connection...
✅ AAPL: Successfully fetched 252 rows
✅ EURUSD=X: Successfully fetched 252 rows
✅ BTC-USD: Successfully fetched 252 rows
⚠️  Some connection warnings detected
📊 Overall: Yahoo Finance API is functional
```

### Polygon.io Debug (`debug_polygon_connection.py`)
**Purpose:** Test Polygon.io API connection and authentication

```bash
python scripts/debug_scripts/debug_polygon_connection.py
```

**Requirements:**
- `POLYGON_API_KEY` in `.env` file

**What it tests:**
- API key validation
- Rate limit handling
- Data format consistency
- Error responses

**Output example:**
```
🔍 Testing Polygon.io Connection...
✅ API Key: Valid
✅ Stock data: AAPL fetched successfully
✅ Forex data: C:EURUSD fetched successfully
✅ Crypto data: X:BTCUSD fetched successfully
📊 Overall: Polygon.io API is operational
```

### Polygon Resolution Debug (`debug_polygon_resolve.py`)
**Purpose:** Test Polygon.io symbol resolution and data access

```bash
python scripts/debug_scripts/debug_polygon_resolve.py
```

**What it tests:**
- Symbol format validation
- Ticker resolution
- Market access permissions
- Data availability

### Binance Debug (`debug_binance_connection.py`)
**Purpose:** Test Binance API connectivity and permissions

```bash
python scripts/debug_scripts/debug_binance_connection.py
```

**Requirements:**
- `BINANCE_API_KEY` and `BINANCE_API_SECRET` in `.env` file

**What it tests:**
- API credentials validation
- Spot market access
- Historical data fetching
- Rate limit compliance

**Output example:**
```
🔍 Testing Binance Connection...
✅ API Credentials: Valid
✅ Account access: Permitted
✅ BTCUSDT data: Fetched 1000 rows
✅ ETHUSDT data: Fetched 1000 rows
📊 Overall: Binance API is accessible
```

## Data Validation Scripts

### CSV Reader Debug (`debug_csv_reader.py`)
**Purpose:** Test CSV file reading and processing logic

```bash
python scripts/debug_scripts/debug_csv_reader.py
```

**What it tests:**
- CSV file format detection
- Column mapping accuracy
- Data type conversions
- Encoding handling

**Features:**
- Tests various CSV formats
- Validates MT5 export compatibility
- Checks data integrity
- Reports processing issues

### Parquet Check (`debug_check_parquet.py`)
**Purpose:** Validate integrity of cached Parquet files

```bash
python scripts/debug_scripts/debug_check_parquet.py
```

**What it validates:**
- File structure integrity
- Schema consistency
- Data corruption detection
- Metadata verification

**Output example:**
```
🔍 Checking Parquet Files...

📁 data/raw_parquet/
✅ yfinance_AAPL_D1_2024.parquet (1.2 MB, 252 rows)
✅ polygon_EURUSD_H1_2024.parquet (3.1 MB, 8760 rows)
⚠️  binance_BTCUSDT_M15_2024.parquet (corrupted metadata)

📁 data/cache/csv_converted/
✅ CSVExport_XAUUSD_MN1.parquet (45 MB, 120000 rows)

📊 Summary: 3/4 files are healthy
```

## Data Examination Tools

### Parquet Examiner (`examine_parquet.py`)
**Purpose:** Detailed examination of Parquet file structure and content

```bash
# Examine specific file
python scripts/debug_scripts/examine_parquet.py data/file.parquet

# Examine all files in directory
python scripts/debug_scripts/examine_parquet.py data/raw_parquet/
```

**Analysis provided:**
- File metadata and schema
- Column statistics
- Data type distribution
- Memory usage
- Date range coverage
- Sample data preview

**Output example:**
```
📊 Parquet File Analysis: yfinance_AAPL_D1_2024.parquet

📋 Basic Info:
   Size: 1.2 MB
   Rows: 252
   Columns: 7
   Date Range: 2024-01-01 to 2024-12-31

📊 Schema:
   datetime: timestamp[ns]
   open: float64
   high: float64
   low: float64
   close: float64
   volume: int64
   adj_close: float64

📈 Statistics:
   Missing values: 0
   Duplicate rows: 0
   Memory usage: 14.1 KB

🔍 Sample Data:
        datetime    open    high     low   close      volume
   0  2024-01-01  185.64  186.95  184.32  185.85  45_234_567
   1  2024-01-02  186.12  187.43  185.78  186.89  42_156_789
   ...
```

### Binance Parquet Examiner (`examine_binance_parquet.py`)
**Purpose:** Specialized examination of Binance-sourced data files

```bash
python scripts/debug_scripts/examine_binance_parquet.py
```

**Binance-specific analysis:**
- Kline data format validation
- Timestamp consistency
- Volume accuracy
- Trading pair verification

## Automated Debug Execution

### Docker Container Debug
When Docker container starts, all debug scripts are automatically executed:
```bash
docker compose up
# Automatically runs all debug_*.py scripts
```

### Manual Batch Execution
```bash
# Run all debug scripts
for script in scripts/debug_scripts/debug_*.py; do
    echo "Running $script..."
    python "$script"
    echo "---"
done
```

### Selective Debugging
```bash
# Test only API connections
python scripts/debug_scripts/debug_yfinance.py
python scripts/debug_scripts/debug_polygon_connection.py
python scripts/debug_scripts/debug_binance_connection.py

# Test only data validation
python scripts/debug_scripts/debug_csv_reader.py
python scripts/debug_scripts/debug_check_parquet.py
```

## Common Debugging Workflows

### API Connection Issues
```bash
# 1. Check basic connectivity
python scripts/debug_scripts/debug_yfinance.py

# 2. Verify API keys (if using paid APIs)
python scripts/debug_scripts/debug_polygon_connection.py
python scripts/debug_scripts/debug_binance_connection.py

# 3. Test specific symbols
python run_analysis.py yf -t TEST --period 5d --point 0.01
```

### Data Quality Issues
```bash
# 1. Check file integrity
python scripts/debug_scripts/debug_check_parquet.py

# 2. Examine suspicious files
python scripts/debug_scripts/examine_parquet.py data/suspicious_file.parquet

# 3. Validate CSV processing
python scripts/debug_scripts/debug_csv_reader.py

# 4. Run comprehensive EDA
python src/eda/eda_batch_check.py --data-quality-checks
```

### Performance Issues
```bash
# 1. Check file sizes and structure
python scripts/debug_scripts/examine_parquet.py data/raw_parquet/

# 2. Validate processing efficiency
python scripts/debug_scripts/debug_csv_reader.py

# 3. Test memory usage
python scripts/debug_scripts/examine_binance_parquet.py
```

## Custom Debug Scripts

### Creating New Debug Scripts

**Template for API debug script:**
```python
#!/usr/bin/env python3
"""
Debug Custom API

Test connectivity and data fetching for custom API.
"""

import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_api_connection():
    """Test basic API connectivity."""
    try:
        # API connection logic
        print("✅ API connection successful")
        return True
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def test_data_fetching():
    """Test data fetching functionality."""
    try:
        # Data fetching logic
        print("✅ Data fetching successful")
        return True
    except Exception as e:
        print(f"❌ Data fetching failed: {e}")
        return False

def main():
    print("🔍 Testing Custom API Connection...")
    
    results = []
    results.append(test_api_connection())
    results.append(test_data_fetching())
    
    if all(results):
        print("📊 Overall: Custom API is operational")
    else:
        print("⚠️ Overall: Custom API has issues")

if __name__ == "__main__":
    main()
```

**Template for data validation script:**
```python
#!/usr/bin/env python3
"""
Debug Custom Data Format

Validate custom data format and processing.
"""

import pandas as pd
from pathlib import Path

def validate_file_format(file_path):
    """Validate file format and structure."""
    try:
        df = pd.read_parquet(file_path)
        print(f"✅ {file_path.name}: {df.shape[0]} rows, {df.shape[1]} columns")
        return True
    except Exception as e:
        print(f"❌ {file_path.name}: {e}")
        return False

def main():
    print("🔍 Validating Custom Data Format...")
    
    data_dir = Path("data/custom_format/")
    if not data_dir.exists():
        print("❌ Custom data directory not found")
        return
    
    files = list(data_dir.glob("*.parquet"))
    if not files:
        print("❌ No Parquet files found")
        return
    
    results = [validate_file_format(f) for f in files]
    
    success_rate = sum(results) / len(results) * 100
    print(f"📊 Overall: {success_rate:.1f}% files are valid")

if __name__ == "__main__":
    main()
```

### Adding to Automated Testing
```bash
# Make script executable
chmod +x scripts/debug_scripts/debug_custom.py

# Add to container startup (if needed)
# Edit docker-entrypoint.sh to include your script
```

## Troubleshooting Guide

### Common Issues and Solutions

**Script not found:**
```bash
# Check script exists and is executable
ls -la scripts/debug_scripts/
chmod +x scripts/debug_scripts/debug_*.py
```

**Import errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**API key issues:**
```bash
# Check .env file configuration
cat .env
# Verify API keys are correctly set
echo $POLYGON_API_KEY
```

**Permission errors:**
```bash
# Fix file permissions
chmod +x scripts/debug_scripts/*.py
sudo chown -R $USER:$USER data/
```

**Connection timeouts:**
```bash
# Check network connectivity
ping api.polygon.io
curl -I https://query1.finance.yahoo.com/

# Test with reduced timeout
export REQUEST_TIMEOUT=10
python scripts/debug_scripts/debug_yfinance.py
```

### Debug Output Interpretation

**Success indicators:**
- ✅ Green checkmarks
- Successful data fetching
- No error messages
- Expected file counts/sizes

**Warning signs:**
- ⚠️ Yellow warnings
- Partial failures
- Timeout messages
- Reduced data quality

**Error conditions:**
- ❌ Red X marks
- Exception tracebacks
- Connection failures
- File corruption messages
