# NeoZorK Indicator ML Enhancement

## Overview

This project focuses on the **professional enhancement of a proprietary trading indicator's predictive capabilities** using advanced Machine Learning (ML) techniques implemented in Python. The original indicator logic, initially developed in MQL5, is replicated within this Python framework.

The primary goal is to significantly improve the accuracy and robustness of forecasts for the next period's **High, Low, and Direction (HLD)** for financial instruments (e.g., Forex pairs). The system leverages historical Minute-level (M1) OHLCV data and the output of the Python-replicated proprietary indicator as inputs for sophisticated ML models.

The workflow involves an initial one-time data export from MetaTrader 5 (MT5), followed by the use of live data feeds (e.g., Yahoo Finance via `yfinance`, CSV files, Polygon.io API) for ongoing analysis and prediction generation. The ultimate aim is to create a highly accurate forecasting system suitable for potentially profitable automated trading strategies.

## Core Goals

* **Indicator Replication:** Accurately translate and validate the core logic of the original MQL5 HLD indicator into a pure Python implementation.
* **ML-Powered Enhancement:** Develop a robust ML pipeline that takes features derived from OHLCV data *and* the Python indicator's output to generate significantly improved HLD predictions.
* **High-Resolution Data Utilization:** Leverage 5-10 years of historical M1 OHLCV data for comprehensive feature engineering and training of potentially complex ML models (e.g., sequence models).
* **Rigorous Validation:** Employ state-of-the-art validation techniques (e.g., walk-forward validation, strict time-series splits) to ensure model robustness and avoid overfitting.
* **Performance Evaluation:** Quantify the improvement over the baseline Python-replicated indicator using statistical metrics and realistic backtesting simulations.
* **Profitability Focus:** Structure the project towards creating forecasts that provide a demonstrable statistical edge for potential trading profitability.

## Features
* Supports multiple data sources: Demo data, CSV files (MT5 export format), Yahoo Finance, Polygon.io, and Binance Spot.
* Calculates the core "Pressure Vector" indicator components and derived rules (`PV_HighLow`, `Support_Resistants`, `Pressure_Vector`, `Predict_High_Low_Direction`).
* Provides validation of Python calculations against original MQL5 results when using CSV mode.
* Generates plots using `mplfinance` to visualize OHLCV data, indicator lines, and signals.
* **NEW:** Advanced data cleaning capabilities with `data_cleaner_v2.py`:
  - Handles duplicates and NaN values in CSV and Parquet files
  - Supports multiple NaN handling strategies (ffill, dropna_rows, none)
  - Preserves directory structure when cleaning multiple files
  - Detailed logging of cleaning operations
* **NEW:** Batch EDA checking with `eda_batch_check.py`:
  - Performs comprehensive data quality checks on CSV and Parquet files
  - Checks for missing values, duplicates, and data types
  - Provides statistical summaries and detailed logging
  - Optionally runs data cleaner to fix identified issues
  - Supports custom target folders and output directories
* **NEW:** Automatically saves raw OHLCV data fetched from API sources (Yahoo Finance, Polygon.io, Binance) to efficient `.parquet` files in the `data/raw_parquet/` directory for later use or analysis.
* **NEW:** Displays enhanced execution summary in the console, including DataFrame shape, memory usage, data fetch duration, and API request latency.
* Includes utility scripts for debugging connections to various APIs (`debug_*.py`).
* Modular structure with clear separation of concerns (data fetching, calculation, plotting, workflow).
* Includes unit tests for key components.

## Core Methodology (ML Emphasis)

1.  **Indicator Logic Replication (Python):** Translate the mathematical and logical steps of the MQL5 indicator into an equivalent Python function or class. Validate its output against the original MQL5 version using the exported historical predictions.
2.  **Data Ingestion & Management:**
    * **Initial Load:** Process the one-time export of M1 OHLCV and original MQL5 indicator predictions from MT5.
    * **Data Feeds:** Implement functionality to fetch and update OHLCV data from sources like Yahoo Finance (`yfinance`), CSV files, Polygon.io API, or other chosen data providers.
3.  **Feature Engineering (ML-Centric):**
    * Derive features primarily from M1 OHLCV data (e.g., price transformations, volatility measures, time-based patterns, candlestick patterns).
    * Crucially, incorporate the outputs (predicted H/L/D, internal states) of the **Python-replicated indicator** as key features for the ML model.
    * **Avoid reliance on standard external technical indicators** (like pre-built RSI, MACD from libraries) unless their specific calculations prove highly valuable during feature importance analysis *after* model training. The focus is on enhancing the *proprietary* indicator's signals.
4.  **Advanced ML Modeling:**
    * Train sophisticated ML models suited for time-series forecasting (e.g., Gradient Boosting Machines like XGBoost/LightGBM, Deep Learning models like LSTMs, GRUs, or Transformers if sequential patterns in M1 data are critical).
    * Experiment with different prediction targets: directly predicting H/L/D, predicting the *error* of the Python indicator's forecast, or predicting the confidence/probability of the indicator's signal being correct.
5.  **Strict Validation & Tuning:**
    * Implement walk-forward validation or use anchored time-series splits for training, validation (hyperparameter tuning), and final testing.
    * Utilize hyperparameter optimization libraries (e.g., Optuna, Hyperopt) to find optimal model configurations based on validation set performance.
6.  **Backtesting Enhanced Predictions:**
    * Develop trading strategies that utilize the **ML-enhanced predictions**.
    * Perform realistic backtests using libraries like `VectorBT` (optimized for speed) or `Backtrader`, incorporating estimated transaction costs (spread, commission).
7.  **Stress-Testing (Monte Carlo):** Apply Monte Carlo simulations to assess the strategy's robustness and risk profile under various simulated market conditions.

## Validation Notes (Python vs MQL5 CSV)

Based on comparisons using the `mql5_feed/CSVExport_XAUUSD_PERIOD_MN1.csv` file:

* **Core Calculations (Pressure/PV):** Validation shows that the Python implementation of `Pressure` and `PV` (Pressure Vector) calculations is **highly accurate**, matching the `pressure` and `pressure_vector` columns from the CSV very closely (Correlation=1.0, minimal Mean Absolute Difference, <5% mismatches beyond float tolerance).
* **Predicted Low/High (PHLD/SR Rules):** The current Python implementation for `PPrice1` (plotted green) and `PPrice2` (plotted red) in rules `PHLD` and `SR`. Comparison with `predicted_low` and `predicted_high` columns from the sample MQL5 CSV shows a **systematic difference** (approx. 6.8 points Mean Absolute Difference in the sample XAUUSD MN1 data, although Correlation > 0.999).

### Data Caching Mechanism

To speed up subsequent runs and reduce API load, the script utilizes data caching in Parquet format:

* **CSV Mode (`--mode csv`):**
    * On the first run with a specific CSV file, the processed data (after cleaning, column standardization, and type conversion) is saved to a `.parquet` file in the `data/cache/csv_converted/` directory.
    * The cache filename corresponds to the original CSV filename (e.g., `CSVExport_XAUUSD_PERIOD_MN1.parquet`).
    * On subsequent runs with the same CSV file, the script will load data directly from this Parquet cache, skipping the CSV reading and processing steps.
* **API Modes (`polygon`, `binance`, `yfinance`):**
    * Data fetched from APIs is cached in the `data/raw_parquet/` directory.
    * A separate file is created for each instrument (ticker + interval + mode), e.g., `polygon_XAUUSD_M1.parquet`.
    * The script automatically identifies missing date ranges compared to the requested period and fetches only the missing data, updating the cache file incrementally.
    * *Note:* The `yfinance` mode, when using the `--period` argument (instead of `--start`/`--end`), always re-downloads the data for that period and does not use the cache for incremental fetching logic. It will, however, overwrite the cache file for that instrument.

* **Important:** If you make changes to the code responsible for **data loading or initial processing** (e.g., files in `src/data/fetchers/` or the logic in `src/data/data_acquisition.py`, especially concerning type conversions or column handling), the **existing cache might become outdated**. To see the effects of your code changes, you may need to **manually delete** the relevant `.parquet` cache files from the `data/cache/csv_converted/` or `data/raw_parquet/` directories before running the script again.

## Tech Stack

* **Language:** Python 3.12+
* **Core Libraries:** `pandas`, `numpy`
* **ML / Deep Learning:** `scikit-learn`, `xgboost`, `lightgbm`, `tensorflow` or `pytorch`
* **Feature Engineering:** `ta` (or `TA-Lib`)
* **Data Feeds:** `yfinance`, CSV reader (implemented), `polygon-api-client` (implemented)
* **Backtesting:** `VectorBT`, `Backtrader`
* **Plotting:** `mplfinance`, `matplotlib`, `seaborn`, `rich`, `colorama`
* **Environment:** `venv`
* **Version Control:** `git`
* **Package Installation Speedup (Optional):** `uv`


# Project Structure
├── data/  
│   ├── cache/  
│   │   └── csv_converted/  
│   ├── processed/  
│   └── raw_parquet/  
├── mql5_feed/  
├── notebooks/  
├── scripts/
│   ├── data_processing/
│   │   ├── data_cleaner_v2.py
│   │   └── __init__.py
│   ├── log_analysis/
│   └── debug_scripts/
├── src/  
│   ├── cli/  
│   │   └── cli.py  
│   ├── calculation/  
│   ├── data/  
│   ├── feature_engineering.py  
│   └── __init__.py  
├── tests/  
├── .env  
├── .gitignore  
├── init_dirs.sh  
├── README.md  
├── requirements.txt  
└── run_analysis.py  

## Directory and File Descriptions

`data/`: Central storage for all data-related files.  
`cache/`: Holds temporary intermediate data.  
`csv_converted/`: Stores CSV files converted from other formats.  


`processed/`: Contains processed data ready for analysis.  
`raw_parquet/`: Stores raw data in Parquet format for efficient storage and querying.  


`mql5_feed/`: Directory for CSV files exported from MQL5/MT5 platforms.  
`notebooks/`: Contains Jupyter notebooks used for exploratory data analysis (EDA) and experimental workflows.  
`scripts/`: Contains utility scripts for data processing and analysis.
`data_processing/`: Scripts for data cleaning and preprocessing.
`log_analysis/`: Scripts for analyzing log files and generating reports.
`debug_scripts/`: Scripts for debugging and testing various components.

`src/`: Main source code directory for the project.  
`cli/`: Command-line interface scripts.  
`cli.py`: Primary script for running CLI commands.  



`calculation/`: Modules for performing calculations and computations.  
`data/`: Modules for data loading, cleaning, and preprocessing.  
`feature_engineering.py`: Script for creating and transforming features for analysis or modeling.  
`init.py`: Initializes the src directory as a Python package.  



`tests/`: Directory for unit tests to ensure code reliability.  
`.env`: Stores environment variables, such as API keys and configuration settings.  
`.gitignore`: Specifies files and directories to be ignored by Git version control.  
`init_dirs.sh`: Shell script to set up project directories and initialize the .env file.  
`README.md:` This file, providing an overview and documentation of the project.  
`requirements.txt`: Lists Python dependencies required for the project.  
`run_analysis.py`: Main entry point script to execute the data analysis pipeline.  



## Installation

## Quick Start: Directory and Environment Setup

Before running the project, create all required folders by executing the initialization script:

```bash
./init_dirs.sh
```
This script will set up the directory structure for data, cache, and source files.

### Testing init_dirs.sh

The project includes unit tests for the initialization script using BATS (Bash Automated Testing System).

1. Install BATS:
   ```bash
   # macOS
   brew install bats-core
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install bats
   
   # From source
   git clone https://github.com/bats-core/bats-core.git
   cd bats-core
   ./install.sh /usr/local
   ```

2. Run the tests:
   ```bash
   bats tests/scripts/test_init_dirs.bats
   ```

The tests verify that:
- All required directories are created correctly
- The `.env` file is created with necessary fields
- Existing `.env` files are not overwritten
- The script works when run from different directories
- Directories have correct permissions
- Error handling works as expected
- The script is idempotent (can be run multiple times safely)

## Environment Variables (.env)

The `.env` file must be located in the project root (next to `README.md` and `requirements.txt`).  
It stores API keys and other sensitive configuration values required for data sources.

**Example `.env` content:**
```env
# Polygon.io API key
POLYGON_API_KEY=your_polygon_api_key_here

# Binance API keys
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# Add other environment variables as needed
```
* The .env file is created automatically by the init_dirs.sh script if it does not exist.
* Do not commit .env to version control; it is already listed in .gitignore.
* Update the values with your actual API keys before running the scripts.



1.  **Install Python 3.12+**: Ensure you have Python 3.12 or higher installed on your system. You can download it from the official Python website: [python.org](https://www.python.org/downloads/).

* macOS:
Install Homebrew if not already installed, then run:
  ```bash
  brew install python@3.12
  ```
* Windows:
Download and install Python 3.12 from the official website.
* Linux:
Use your package manager, for example:
    ```bash
    sudo apt-get update
    sudo apt-get install python3.12 python3.12-venv
    ```


2. **Clone Repository:**
    ```bash
    git clone <your_repository_url>
    cd <project-root>
    ```

3. **Create & Activate Virtual Environment (Recommended: Python 3.12):**
    ```bash
    # Make sure Python 3.12 is installed and accessible
    python3.12 -m venv venv
    source .venv/bin/activate # On Linux/macOS
    pip install --upgrade pip
    # venv\Scripts\activate # On Windows
    ```

4. **Install Dependencies:**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    # Or using uv (optional, faster):
    # pip install uv
    # uv pip install -r requirements.txt
    ```

5. **(If needed) Install TA-Lib C Library:** (Only if using `TA-Lib` python package)
    * macOS: `brew install ta-lib`
    * Linux: Check package manager (e.g., `sudo apt-get install libta-lib-dev`)
    * Windows: Download binaries or build from source.
    * Then install the Python wrapper: `pip install TA-Lib`

6. **Install Testing Dependencies:**
    ```bash
    pip install pytest  # Required for running unit tests
    ```

## Project Workflow / Detailed Plan (Status Updated 2025-04-18)

### Phase 0: Setup & Foundation
* [x] 0.1. Version Control Setup (Local Git, GitHub Remote, `.gitignore`)
* [x] 0.2. Development Environment Setup (PyCharm, Python 3.12+, `venv`, Base Libraries)

### Phase 1: Indicator Replication & Validation (Python)
* [~] 1.1. Understand Original MQL5 Logic (Inputs, Calculations, Outputs) & Document. *(Partially understood via CSV analysis)*
* [x] 1.2. Python Implementation (`src/calculation/...`): Core logic translated.
* [~] 1.3. Unit Testing: Basic tests exist, need expansion.
* [x] 1.4. Plan Replication Validation Strategy: Comparison implemented for CSV mode.
* [x] 1.5. Add Project Versioning (`src/__init__.py`, Git Tag).

### Phase 2: Data Ingestion & Preparation
* [x] 2.1. Export Original MQL5 Indicator Predictions (CSV from MT5, M1, 5-10 years). *(Sample MN1 provided)*
* [x] 2.2. Export M1 OHLCV Data (CSV from MT5, same period/instrument). *(Sample MN1 provided)*
* [x] 2.3. Load Data in Python: Implemented for CSV, yfinance, Polygon.
* [~] 2.4. Merge & Align Data (Handle timestamps, missing values). *(Basic handling in fetch functions)*
* [x] 2.5. Calculate Python Indicator Predictions on historical data (Done within workflow).
* [X] 2.6. Define Ground Truth (Actual future H/L/D).
* [x] 2.7. Clean & Save Final Processed Data (`data/processed/`, e.g., Parquet format).
* *Note: Added CSV & Polygon data source integration (CLI, data_acquisition, point_size).*

### Phase 3: Exploratory Data Analysis (EDA)
* [ ] 3.1. Load Processed Data (`notebooks/`).
* [ ] 3.2. Analyze Distributions & Statistics.
* [ ] 3.3. Visualize Time Series.
* [ ] 3.4. Calculate **Baseline Performance** (Python indicator vs Ground Truth).
* [ ] 3.5. Analyze Indicator Errors.

### Phase 4: Feature Engineering & Unit Testing
* [ ] 4.1. Develop Feature Ideas.
* [ ] 4.2. Implement Feature Generation (`src/feature_engineering.py`).
* [ ] 4.3. Feature Scaling/Normalization Plan.
* [ ] 4.4. Save Final Feature Set.
* [ ] 4.5. **Write Unit Tests** for data loading/processing (`fetch_csv_data`, `fetch_polygon_data`, `resolve_polygon_ticker`, `data_acquisition`, `point_size_determination`).

### Phase 5: ML Model Development & Training
* [ ] 5.1. Define ML Problem & Targets.
* [ ] 5.2. Select Candidate Models.
* [ ] 5.3. Establish Validation Strategy.
* [ ] 5.4. Create Training Pipeline.
* [ ] 5.5. Train Initial Models & Tune Hyperparameters.
* [ ] 5.6. Save Best Tuned Models & Scalers.

### Phase 6: Evaluation & Selection
* [ ] 6.1. Final Evaluation on Test Set.
* [ ] 6.2. Compare ML vs. Baseline.
* [ ] 6.3. Analyze Feature Importance & Explainability.
* [ ] 6.4. Select Best Production Model.

### Phase 7: Backtesting
* [ ] 7.1. Define Trading Strategy Logic.
* [ ] 7.2. Implement Backtesting Engine.
* [ ] 7.3. Run Backtest.
* [ ] 7.4. Analyze Backtest Results.

### Phase 8: Strategy Stress-Testing & Robustness Analysis (Monte Carlo Simulation)
* [ ] 8.1. Select & Calibrate Simulation Model.
* [ ] 8.2. Implement Simulation Engine.
* [ ] 8.3. Define Test Scenarios.
* [ ] 8.4. Integrate Strategy & Run Simulations.
* [ ] 8.5. Collect & Analyze Simulation Results.
* [ ] 8.6. Document Robustness Findings.

### Phase 9: Live Data Integration & Forward Testing
* [ ] 9.1. Adapt Prediction Pipeline for live data.
* [ ] 9.2. Setup Forward Testing (Paper Trading).
* [ ] 9.3. Monitor Forward Test.

### Phase 10: Monitoring & Maintenance
* [ ] 10.1. Continuous Performance Monitoring.
* [ ] 10.2. Model Drift Detection.
* [ ] 10.3. Periodic Retraining Schedule/Trigger.
* [ ] 10.4. Ongoing Maintenance.

## Usage Examples

### Quick Reference: Show All CLI Examples

You can view a comprehensive list of usage examples for all modes and options by running:

```bash
python run_analysis.py --examples
```

This will print a categorized, multi-line list of real-world command-line examples for `demo, CSV, yfinance, polygon, binance, show, plotting, rules`, cache, and error cases.

### Most Useful Examples

# 1. DEMO DATA MODES
```bash
python run_analysis.py demo
python run_analysis.py demo -d mpl
python run_analysis.py demo --rule PV_HighLow
python run_analysis.py demo --rule PHLD -d plotly
```

# 2. CSV FILE MODES
```bash
python run_analysis.py csv --csv-file data.csv --point 0.01
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule SR
python run_analysis.py csv --csv-file data.csv --point 0.01 -d mplfinance
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV --draw fastest
```

# 3. YAHOO FINANCE (YF) MODES
```bash
python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001
python run_analysis.py yfinance -t AAPL --period 6mo --point 0.01
python run_analysis.py yf -t BTC-USD --start 2023-01-01 --end 2023-12-31 --point 0.01
python run_analysis.py yf -t EURUSD=X --start 2024-01-01 --end 2024-04-18 --point 0.00001 -d mpl
python run_analysis.py yf -t AAPL --period 1y --rule SR
```

# 4. POLYGON.IO MODES
```bash
python run_analysis.py polygon --ticker AAPL --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01
python run_analysis.py polygon --ticker EURUSD --interval H1 --start 2022-01-01 --end 2022-06-01 --point 0.00001 --rule PV
```

# 5. BINANCE MODES
```bash
python run_analysis.py binance --ticker BTCUSDT --interval H1 --start 2024-01-01 --end 2024-04-18 --point 0.01
python run_analysis.py binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule SR
```

# 6. SHOW MODE (CACHE/FILES)
```bash
python run_analysis.py show yf
python run_analysis.py show yf aapl mn1
python run_analysis.py show binance btc
python run_analysis.py show csv EURUSD MN1
python run_analysis.py show polygon AAPL 2023
python run_analysis.py show yf --show-rule PV
python run_analysis.py show yf --show-start 2023-01-01 --show-end 2023-12-31
```

# 7. ADVANCED/EDGE CASES
```bash
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PHLD --draw plotly
python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 --rule PV --draw fastest
python run_analysis.py polygon --ticker EURUSD --interval D1 --start 2022-01-01 --end 2022-12-31 --point 0.00001 --rule SR --draw mpl
python run_analysis.py binance --ticker BTCUSDT --interval M1 --start 2023-01-01 --end 2023-01-31 --point 0.01 --rule PHLD
```

# 8. HELP, VERSION, EXAMPLES
```bash
python run_analysis.py -h
python run_analysis.py --version
python run_analysis.py --examples
```

# 9. CACHE/DEBUG
```bash
# Remove cache and rerun
rm data/cache/csv_converted/*.parquet
python run_analysis.py csv --csv-file data.csv --point 0.01
```

# 10. ERROR CASES (will show error/help)
```bash
python run_analysis.py csv --csv-file data.csv   # (missing --point)
python run_analysis.py yf -t EURUSD=X            # (missing --period or --start/--end)
```

**Note:**
- For all API modes (yfinance, polygon, binance), the `--point` parameter is required to specify the instrument's point size (e.g., 0.00001 for EURUSD, 0.01 for stocks/crypto).
- Use `-d/--draw` to select plotting backend: `fastest, fast, plotly, mplfinance`, etc.
- Use `--rule` to select trading rule: `PV_HighLow`, `Support_Resistants`, `Pressure_Vector`, `Predict_High_Low_Direction`, `PHLD`, `PV`, `SR`.
- `SHOW` mode allows filtering cached files by `source, keywords, date, and rule`.
- For more details, see `python run_analysis.py -h` for full help.

## Show Mode

The `show` mode is designed for interactive browsing, analysis, and visualization of locally cached datasets in Parquet format, which are used for indicator calculations. It allows you to quickly find needed files, filter them by data source and keywords, and instantly calculate an indicator on the selected data—without querying an API or re-downloading data.

**Key features of `show` mode:**
- Lists all cached Parquet data files in the `data/raw_parquet` and `data/cache/csv_converted` directories.
- Allows filtering files by data source (`yfinance`, `polygon`, `binance`, `csv`) and by keywords (such as ticker, timeframe).
- For each found file, it displays a summary: filename, size, number of rows, date range, column structure, first/last rows.
- If only one file matches the filter, the indicator is calculated on this data and the result is printed in the console (or a chart is displayed if indicator calculation is not explicitly requested).
- **Note:** Indicator values are _always calculated on the fly_ and are **never saved** anywhere.  
  Each time you run an indicator calculation in `show` mode, the indicator is recomputed from scratch on the selected data.

### How to use `show` mode

Example commands for `show` mode:

```bash
# Show help and statistics for all cached data
python run_analysis.py show

# List all files received from Yahoo Finance (YF)
python run_analysis.py show yf

# Find all YF files containing 'aapl' in the name
python run_analysis.py show yf aapl

# Find Binance files containing 'btc' and 'MN1' in the name
python run_analysis.py show binance btc MN1

# Restrict the date range for indicator calculation
python run_analysis.py show yf aapl --show-start 2024-01-01 --show-end 2024-04-01

# Specify a particular indicator rule (default is Predict_High_Low_Direction)
python run_analysis.py show yf aapl --rule PV

# Specify a particular indicator date, rule, drawing style (mplfinance, mpl, plotly, plt, fast, fastest (default))
python run_analysis.py show yf aapl --start 2024-01-01 --end 2024-06-01 --rule SR -d mpl
```

### How it works

- If multiple files are found, the CLI suggests refining the filter or shows a brief summary for each file.
- If exactly one file is found, `show` mode:
    - computes the selected indicator for the loaded data;
    - prints a table with main indicator values directly to the console;
    - indicator values are **never saved**—they are always shown in the current session only.
- For visualization, you can use the `--draw` parameter to select the charting style.
- The default drawing style is `fastest`, which is the fastest mode for large datasets (millions of rows). It uses `mplfinance` for fast rendering of `OHLCV` data and indicator lines.

### Features

- The `show` mode never modifies or overwrites cached parquet files.
- All indicator calculations and visualizations are temporary and do not affect the original data.
- It is a fast way for interactive inspection and analysis of your data and indicator results, without re-downloading or storing intermediate computations.

---

For more information about parameters, see the "EXAMPLES" section or run:
```bash
python run_analysis.py show --help
```

## The script produces the following outputs:

1.  **Console Summary:** Detailed summary printed to the console at the end of execution, including selected parameters, timing metrics for different steps, data shape, memory usage, API latency (if applicable), and overall success status.
2.  **Plots (Optional):** If not disabled via CLI arguments, generates plots displaying `OHLCV` data along with the calculated indicator lines and signals using `mplfinance`. Plots are typically shown interactively or saved if configured.
3.  **NEW: Raw Data Parquet Files:** When run with API data sources (`yfinance`, `polygon`, `binance`), the script automatically saves the downloaded raw `OHLCV` data into a `.parquet` file within the `data/raw_parquet/` directory. The filename typically includes the `source`, `ticker`, `interval`, and `date range`. This allows for easy reloading and reuse of the fetched data without hitting the APIs again.

### Running Tests

This project uses Python's built-in `unittest` framework.

1.  **Activate Environment:** `source venv/bin/activate` (or equivalent).
2.  **Run all tests:** From the project root directory:
    ```bash
    python -m unittest discover tests
    ```

3.  **To run all tests in a folder:
    ```bash
    python -m unitest discover tests/cli  
    ```
    
4.  **To run a specific test file:
    ```bash
    python -m unittest tests.cli.test_cli_all_commands
    ```
    
5.  **To run a specific test case:
    ```bash
    python -m unittest tests.cli.test_cli_all_commands.TestCliAllCommands.test_help
    ```
    
6.  **To Test All CLI Commands:**
    ```bash
    python tests/cli/test_cli_all_commands.py
    ```

Delayed between tests is set to 2 seconds to avoid overwhelming the API with requests.




## EDA Tools

The project includes several tools for exploratory data analysis and data quality checking:

### Batch EDA Checker (`eda_batch_check.py`)
`eda_batch_check.py` is a tool for performing batch Exploratory Data Analysis (EDA) on `CSV` and `Parquet` files. It helps identify data quality issues such as missing values, duplicates, and incorrect data types, while also providing statistical summaries. Optionally, it can clean the data automatically.


#### **Key Features**
- **Data Quality Checks**:
  - Detects missing values `(NaN)`.
  - Removes duplicates.
  - Validates data types.
  - Generates statistical summaries.
- **File Format Support**: Works with `CSV` and `Parquet` files.
- **Logging**: Logs all operations to a file.
- **Data Cleaning**: Optionally cleans data using `data_cleaner_v2.py`.
- **Comparison**: Compares data before and after cleaning.
- **Customizable**: Supports user-defined folders and output directories.

Usage examples:
```bash
# Basic EDA check
python eda_batch_check.py

# Run EDA check and clean data
python eda_batch_check.py --clean

# Specify custom output directory and NaN handling
python eda_batch_check.py --clean --output-dir data/cleaned --handle-nan ffill

# Check specific folders
python eda_batch_check.py --target-folders data/raw_parquet mql5_feed
```

Available options:
- `--clean`: Run data cleaner after analysis
- `--output-dir`: Output directory for cleaned files
- `--csv-delimiter`: Delimiter for CSV files (default: tab)
- `--csv-header`: CSV header row (0 or 'infer')
- `--handle-nan`: NaN handling strategy (ffill, dropna_rows, none)
- `--skip-verification`: Skip verification of cleaned files
- `--log-file`: Custom log file name
- `--target-folders`: List of folders to check

For more information, run:
```bash
python eda_batch_check.py --help,-h
```
Log Example
After running the script, the log file (e.g., `test.log`) contains details about processed files, detected issues, and actions taken.  
Example:

Processing file: `data/raw_parquet/sample.parquet`  
`NaN` values detected: `15 ` 
Duplicates removed: `3`  
File processed successfully.  

Comparison Before and After Cleaning  
The script compares data statistics before and after cleaning. Example output:  

=== EDA Summary Change (Before → After Cleaning) ===  
Total Files: 10 → 10 `(+0)`  
NaN Values: 150 → 0 `(-150)`  
Duplicates: 30 → 0 `(-30)`  
====================================================  
Integration  
`eda_batch_check.py` is part of the `src.eda` module and uses the following components:  
`eda_logging:` Logging setup.  
`eda_batch_processor:` File and folder processing.  
`eda_file_utils:` File search and sorting.  
`eda_log_analysis:` Log analysis.  
`eda_data_cleaner:` Data cleaning.  
Recommendations  
Use `--clean` to automatically clean data.  
Ensure the target folders contain `CSV` or `Parquet` files.  
For large datasets, use `tqdm` to track progress.  