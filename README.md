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
* **NEW:** Automatically saves raw OHLCV data fetched from API sources (Yahoo Finance, Polygon.io, Binance) to efficient `.parquet` files in the `data/raw_parquet/` directory for later use or analysis.
* **NEW:** Displays enhanced execution summary in the console, including DataFrame shape, memory usage, data fetch duration, and API request latency.
* Includes utility scripts for debugging connections to various APIs (`debug_*.py`).
* Modular structure with clear separation of concerns (data fetching, calculation, plotting, workflow).
* Includes unit tests for key components.

## Core Methodology (ML Emphasis)

1.  **Indicator Logic Replication (Python):** Translate the mathematical and logical steps of the MQL5 indicator into an equivalent Python function or class. Validate its output against the original MQL5 version using the exported historical predictions.
2.  **Data Ingestion & Management:**
    * **Initial Load:** Process the one-time export of M1 OHLCV and original MQL5 indicator predictions from MT5.
    * **Data Feeds:** Implement functionality to fetch and update OHLCV data from sources like Yahoo Finance (`yfinance`), CSV files, Polygon.io API, or other chosen data providers (Oanda planned).
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
* **Predicted Low/High (PHLD/SR Rules):** The current Python implementation for `PPrice1` (plotted green) and `PPrice2` (plotted red) in rules `PHLD` and `SR` uses a formula based on `Current Open +/- (Previous_High - Previous_Low) / 2`. Comparison with `predicted_low` and `predicted_high` columns from the sample MQL5 CSV shows a **systematic difference** (approx. 6.8 points Mean Absolute Difference in the sample XAUUSD MN1 data, although Correlation > 0.999). This indicates that the original MQL5 indicator uses a **different formula** for these specific predictions. Achieving an exact match would require implementing the original MQL5 formula in `src/calculation/rules.py`.

## Tech Stack

* **Language:** Python 3.12+
* **Core Libraries:** `pandas`, `numpy`
* **ML / Deep Learning:** `scikit-learn`, `xgboost`, `lightgbm`, `tensorflow` or `pytorch`
* **Feature Engineering:** `ta` (or `TA-Lib`)
* **Data Feeds:** `yfinance`, CSV reader (implemented), `polygon-api-client` (implemented), `oandapyV20` (planned)
* **Backtesting:** `VectorBT`, `Backtrader`
* **Plotting:** `mplfinance`, `matplotlib`, `seaborn`, `rich`, `colorama`
* **Environment:** `venv`
* **Version Control:** `git`
* **Package Installation Speedup (Optional):** `uv`

## Project Structure


## Installation

1.  **Clone Repository:**
    ```bash
    git clone <your_repository_url>
    cd <project-root>
    ```

2.  **Create & Activate Virtual Environment (Recommended: Python 3.12):**
    ```bash
    # Make sure Python 3.12 is installed and accessible
    python3.12 -m venv venv
    source venv/bin/activate # On Linux/macOS
    # venv\Scripts\activate # On Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    # Or using uv (optional, faster):
    # pip install uv
    # uv pip install -r requirements.txt
    ```

4.  **(If needed) Install TA-Lib C Library:** (Only if using `TA-Lib` python package)
    * macOS: `brew install ta-lib`
    * Linux: Check package manager (e.g., `sudo apt-get install libta-lib-dev`)
    * Windows: Download binaries or build from source.
    * Then install the Python wrapper: `pip install TA-Lib`

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
* [ ] 2.1. Export Original MQL5 Indicator Predictions (CSV from MT5, M1, 5-10 years). *(Sample MN1 provided)*
* [ ] 2.2. Export M1 OHLCV Data (CSV from MT5, same period/instrument). *(Sample MN1 provided)*
* [x] 2.3. Load Data in Python: Implemented for CSV, yfinance, Polygon.
* [~] 2.4. Merge & Align Data (Handle timestamps, missing values). *(Basic handling in fetch functions)*
* [x] 2.5. Calculate Python Indicator Predictions on historical data (Done within workflow).
* [~] 2.6. **Validate Python Replication:** Done for `Pressure`/`PV` (good match). Known difference for `predicted_low`/`high` due to different formulas in current Python rules (`PHLD`/`SR`).
* [ ] 2.7. Define Ground Truth (Actual future H/L/D).
* [ ] 2.8. Clean & Save Final Processed Data (`data/processed/`, e.g., Parquet format).
* *Note: Added CSV & Polygon data source integration (CLI, data_acquisition, point_size).*
* *Note: Oanda fetch logic pending API key.*

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
* [ ] 9.1. Implement Live Data Feed (Oanda pending).
* [ ] 9.2. Adapt Prediction Pipeline for live data.
* [ ] 9.3. Setup Forward Testing (Paper Trading).
* [ ] 9.4. Monitor Forward Test.

### Phase 10: Monitoring & Maintenance
* [ ] 10.1. Continuous Performance Monitoring.
* [ ] 10.2. Model Drift Detection.
* [ ] 10.3. Periodic Retraining Schedule/Trigger.
* [ ] 10.4. Ongoing Maintenance.

## Usage Examples

### Running Analysis (`run_analysis.py`)

* **Run with demo data using the default rule (Predict_High_Low_Direction):**
    ```bash
    python run_analysis.py demo
    ```

* **Run with demo data using a specific rule (e.g., Pressure_Vector alias 'PV'):**
    ```bash
    python run_analysis.py demo --rule PV
    ```
  
* ** Run with demo data using a specific rule with point size (e.g., Pressure_Vector_HighLow alias 'PV_HighLow'):**
    ```bash
    python run_analysis.py demo --rule PV_HighLow --point 0.01
    ```


* **  Fetch Binance data for BTC/USDT, M1 interval, specific dates
* ** (Requires --point specified, API keys optional for public data)
  ```bash
    python run_analysis.py binance --ticker BTCUSDT --interval M1 --start 2024-04-01 --end 2024-04-18 --point 0.01
  ```

* ** Or using the ticker format 'btc/usdt'
  ```bash
  python run_analysis.py binance --ticker btc/usdt --interval M1 --start 2024-04-01 --end 2024-04-18 --point 0.01
  ```

* **Run using data from a CSV file:**
    ```bash
    # Replace path/to/your/data.csv and provide the correct point size
    python run_analysis.py csv --csv-file path/to/your/data.csv --rule PHLD --point 0.01
    ```
    * `--csv-file`: Specifies the path to your input CSV file.
    * `--point`: **Required** for CSV mode. You must provide the correct point size for the instrument in the CSV file (e.g., 0.01 or 0.1 for XAUUSD).
    * `--rule`: Select the calculation rule (e.g., `PHLD`, `SR`, `PV`, `PV_HighLow`).

* **Run with CSV file:
    ```bash
    # Example with a specific CSV file and rule
    python run_analysis.py csv --csv-file mql5_feed/CSVExport_XAUUSD_PERIOD_MN1.csv --rule Predict_High_Low_Direction --point 0.01 
    ```


* **Run using data from Polygon.io API:**
    ```bash
    # Replace ticker, dates, and point size as needed. API key must be in .env
    # Use base tickers like AAPL, EURUSD, BTCUSD
    python run_analysis.py polygon --ticker AAPL --interval D1 --start 2024-04-10 --end 2024-04-17 --point 0.01
    python run_analysis.py polygon --ticker EURUSD --interval H1 --start 2024-04-10 --end 2024-04-17 --point 0.00001
    ```
    * `--ticker`: Base ticker symbol (e.g., `AAPL`, `EURUSD`, `BTCUSD`). The script will try to resolve the correct prefixed ticker.
    * `--interval`, `--start`, `--end`: Specify the desired timeframe and date range.
    * `--point`: **Required** for Polygon mode. Provide the correct point size.
    * Ensure `POLYGON_API_KEY` is set in your `.env` file.

* **Run with Polygon.io (requires API key in .env):**
* Fetches Forex EUR/USD minute data
    ```bash
    # Fetches Forex EUR/USD minute data
    python run_analysis.py polygon --ticker C:EURUSD --interval M1 --start 2024-04-15 --end 2024-04-19 --rule Support_Resistants --point 0.00001
    # Note: This will also save raw data to data/raw_parquet/polygon_C_EURUSD_M1_2024-04-15_2024-04-19.parquet
    ```


* **Fetch Yahoo Finance data for a Forex pair, specific interval, last 3 months, estimated point size, specific rule:**
    ```bash
    python run_analysis.py yf --ticker "EURUSD=X" --interval H1 --period 3mo --rule PV_HighLow
    ```

* **Fetch Yahoo Finance data for a stock, specific date range, user-provided point size, specific rule alias 'SR':**
    ```bash
    python run_analysis.py yfinance --ticker AAPL --start 2024-01-01 --end 2024-04-15 --point 0.01 --rule SR
    ```


## The script produces the following outputs:

1.  **Console Summary:** Detailed summary printed to the console at the end of execution, including selected parameters, timing metrics for different steps, data shape, memory usage, API latency (if applicable), and overall success status.
2.  **Plots (Optional):** If not disabled via CLI arguments, generates plots displaying OHLCV data along with the calculated indicator lines and signals using `mplfinance`. Plots are typically shown interactively or saved if configured.
3.  **NEW: Raw Data Parquet Files:** When run with API data sources (`yfinance`, `polygon`, `binance`), the script automatically saves the downloaded raw OHLCV data into a `.parquet` file within the `data/raw_parquet/` directory. The filename typically includes the source, ticker, interval, and date range. This allows for easy reloading and reuse of the fetched data without hitting the APIs again.

### Running Tests

This project uses Python's built-in `unittest` framework.

1.  **Activate Environment:** `source venv/bin/activate` (or equivalent).
2.  **Run all tests:** From the project root directory:
    ```bash
    python -m unittest discover tests
    ```