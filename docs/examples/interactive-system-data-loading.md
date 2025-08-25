# Interactive System Data Loading Examples

## 🚀 Quick Start

```bash
# Start interactive system
uv run ./interactive_system.py

# Navigate to Load Data menu
# Select option 1: Load Data
```

## 📁 Load Data Menu

When you select "Load Data" from the main menu, you'll see:

```
📁 LOAD DATA
------------------------------
Choose loading method:
0. 🔙 Back to Main Menu
1. 📄 Load single file
2. 📁 Load all files from folder
3. 🔍 Load files by mask (e.g., 'gbpusd' for all GBPUSD files)
------------------------------

💡 Examples for 'data' folder:
   Single file: data/sample_ohlcv_1000.csv
   Folder: data/
   Mask: 'sample' (finds sample_ohlcv_*.csv files)
   Mask: 'parquet' (finds *.parquet files)
   Mask: 'binance' (finds binance_*.parquet files)
------------------------------
```

## 📄 Method 1: Load Single File

### Available Files in 'data' folder:

```
📄 LOAD SINGLE FILE
------------------------------
💡 Available files in 'data' folder:
   • data/sample_ohlcv_1000.csv (1000 rows)
   • data/sample_ohlcv_2000.csv (2000 rows)
   • data/sample_ohlcv_1000.parquet (1000 rows)
   • data/sample_ohlcv_2000.parquet (2000 rows)
   • data/raw_parquet/binance_BTCUSDT_H1.parquet (420 rows)
   • data/raw_parquet/yfinance_AAPL_D1.parquet (11 rows)
------------------------------
```

### Example Usage:
```
Enter data file path (CSV, Parquet, etc.): data/sample_ohlcv_1000.csv
```

## 📁 Method 2: Load All Files from Folder

### Available Folders:

```
📁 LOAD ALL FILES FROM FOLDER
------------------------------
💡 Available folders:
   • data/ (main data folder with CSV and Parquet files)
   • data/raw_parquet/ (raw data files)
   • data/indicators/ (calculated indicators)
   • data/cache/csv_converted/ (converted CSV files)
------------------------------
```

### Example Usage:
```
Enter folder path: data/
```

This will load all CSV and Parquet files from the data folder.

## 🔍 Method 3: Load Files by Mask

### Example Combinations:

```
🔍 LOAD FILES BY MASK
------------------------------
💡 Example combinations:
   Folder: data/
   • Mask: 'sample' → finds sample_ohlcv_*.csv files
   • Mask: 'parquet' → finds *.parquet files
   • Mask: '1000' → finds *1000* files
   • Mask: '2000' → finds *2000* files

   Folder: data/raw_parquet/
   • Mask: 'binance' → finds binance_*.parquet files
   • Mask: 'yfinance' → finds yfinance_*.parquet files
   • Mask: 'BTC' → finds *BTC* files
   • Mask: 'AAPL' → finds *AAPL* files
------------------------------
```

### Example Usage:

#### Load all sample files:
```
Enter folder path: data/
Enter file mask: sample
```

#### Load all parquet files:
```
Enter folder path: data/
Enter file mask: parquet
```

#### Load Binance data:
```
Enter folder path: data/raw_parquet/
Enter file mask: binance
```

## 📊 Data Structure

### Main Data Folder (`data/`):
- `sample_ohlcv_1000.csv` - 1000 rows of sample OHLCV data
- `sample_ohlcv_2000.csv` - 2000 rows of sample OHLCV data
- `sample_ohlcv_1000.parquet` - 1000 rows in Parquet format
- `sample_ohlcv_2000.parquet` - 2000 rows in Parquet format

### Raw Data Folder (`data/raw_parquet/`):
- `binance_BTCUSDT_H1.parquet` - 420 rows of Binance BTC/USDT hourly data
- `yfinance_AAPL_D1.parquet` - 11 rows of Yahoo Finance AAPL daily data

### Indicators Folder (`data/indicators/`):
- Contains calculated technical indicators
- Subfolders: `csv/`, `json/`, `parquet/`

### Cache Folder (`data/cache/`):
- `csv_converted/` - Converted CSV files
- `uv_cache/` - UV package manager cache

## 🎯 Best Practices

### For Quick Testing:
```bash
# Load single file for quick testing
data/sample_ohlcv_1000.csv
```

### For Development:
```bash
# Load all sample files
Folder: data/
Mask: sample
```

### For Production Data:
```bash
# Load specific data source
Folder: data/raw_parquet/
Mask: binance
```

## 🔧 Supported File Formats

- **CSV**: `.csv` files
- **Parquet**: `.parquet` files  
- **Excel**: `.xlsx`, `.xls` files

## 📋 Data Preview

After loading data, you can choose to see a preview:
```
Show data preview? (y/n): y
```

This will display:
- First 5 rows of data
- Data types of each column
- Basic statistics

## 🚀 Next Steps

After loading data, you can:
1. **EDA Analysis** - Explore and analyze the data
2. **Feature Engineering** - Generate ML features
3. **Data Visualization** - Create charts and plots
4. **Model Development** - Build ML models

---

**Note**: All examples assume you're running the interactive system from the project root directory.
