# NeoZorK Indicator ML Enhancement

## Overview

This project focuses on the **professional enhancement of a proprietary trading indicator's predictive capabilities** using advanced Machine Learning (ML) techniques implemented in Python. The original indicator logic, initially developed in MQL5, is replicated within this Python framework.

The primary goal is to significantly improve the accuracy and robustness of forecasts for the next period's **High, Low, and Direction (HLD)** for financial instruments (e.g., Forex pairs). The system leverages historical Minute-level (M1) OHLCV data and the output of the Python-replicated proprietary indicator as inputs for sophisticated ML models.

The workflow involves an initial one-time data export from MetaTrader 5 (MT5), followed by the use of live data feeds (e.g., Yahoo Finance via `yfinance`) for ongoing analysis and prediction generation. The ultimate aim is to create a highly accurate forecasting system suitable for potentially profitable automated trading strategies.

## Core Goals

* **Indicator Replication:** Accurately translate and validate the core logic of the original MQL5 HLD indicator into a pure Python implementation (`src/indicator_logic.py`).
* **ML-Powered Enhancement:** Develop a robust ML pipeline that takes features derived from OHLCV data *and* the Python indicator's output to generate significantly improved HLD predictions.
* **High-Resolution Data Utilization:** Leverage 5-10 years of historical M1 OHLCV data for comprehensive feature engineering and training of potentially complex ML models (e.g., sequence models).
* **Rigorous Validation:** Employ state-of-the-art validation techniques (e.g., walk-forward validation, strict time-series splits) to ensure model robustness and avoid overfitting.
* **Performance Evaluation:** Quantify the improvement over the baseline Python-replicated indicator using statistical metrics and realistic backtesting simulations.
* **Profitability Focus:** Structure the project towards creating forecasts that provide a demonstrable statistical edge for potential trading profitability.

## Core Methodology (ML Emphasis)

1.  **Indicator Logic Replication (Python):** Translate the mathematical and logical steps of the MQL5 indicator into an equivalent Python function or class. Validate its output against the original MQL5 version using the exported historical predictions.
2.  **Data Ingestion & Management:**
    * **Initial Load:** Process the one-time export of M1 OHLCV and original MQL5 indicator predictions from MT5.
    * **Live Feed:** Implement functionality to fetch and update OHLCV data from sources like Yahoo Finance (`yfinance`) or other chosen data providers.
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

## Tech Stack

* **Language:** Python 3.12+ (Recommended based on current compatibility findings)
* **Core Libraries:** `pandas`, `numpy`
* **ML / Deep Learning:** `scikit-learn`, `xgboost`, `lightgbm`, `tensorflow` (`tensorflow-macos` potentially) or `pytorch` (`torch`, `torchvision`, `torchaudio`)
* **Feature Engineering:** `ta` (or `TA-Lib` with C library installed)
* **Data Feeds:** `yfinance` (or other API client), `MetaTrader5` (for initial data export only)
* **Backtesting:** `VectorBT` (recommended for M1 data speed), `Backtrader`
* **Plotting:** `mplfinance`, `matplotlib`, `seaborn`
* **Environment:** `venv` (recommended) or `conda`
* **Version Control:** `git`
* **Package Installation Speedup (Optional):** `uv`

## Project Structure

* project-root/
* ├── .git/                 # Git directory (usually hidden)
* ├── .idea/                # PyCharm directory (usually hidden, add to .gitignore)
* ├── venv/                 # Python virtual environment (add to .gitignore)
* ├── data/
* │   ├── raw/              # Raw data exports (e.g., from MT5)
* │   └── processed/        # Processed data ready for use
* ├── notebooks/            # Jupyter notebooks for exploration and analysis
* ├── src/                  # Source code package
* │   ├── __init__.py         # Marks src as package, contains version
* │   │
* │   ├── cli/                # Command Line Interface logic
* │   │   ├── __init__.py     # Marks cli as subpackage
* │   │   └── cli.py          # Argument parsing (using argparse, RichHelpFormatter)
* │   │
* │   ├── common/             # Common utilities, constants, logging
* │   │   ├── __init__.py
* │   │   └── constants.py    # Signal constants, TradingRule enum
* │   │   └── logger.py       # Colored logging utility (using colorama)
* │   │
* │   ├── data/               # Data fetching and preparation utilities
* │   │   ├── __init__.py
* │   │   └── data_utils.py   # Low-level fetch (yfinance), demo data, mapping functions
* │   │   └── data_acquisition.py # Workflow Step 1: acquire_data function
* │   │
* │   ├── calculation/        # Indicator calculation logic
* │   │   ├── __init__.py
* │   │   └── core_calculations.py # Base calculations (HL, PV, Pressure, SMA...)
* │   │   └── rules.py        # Rule implementations (apply_rule_...) & dispatcher
* │   │   └── indicator.py    # Main calculation function (calculate_pressure_vector)
* │   │   └── indicator_calculation.py # Workflow Step 3: calculate_indicator function
* │   │
* │   ├── plotting/           # Plotting related modules
* │   │   ├── __init__.py
* │   │   └── plotting.py     # Low-level plotting function (plot_indicator_results using mplfinance)
* │   │   └── plotting_generation.py # Workflow Step 4: generate_plot function
* │   │
* │   ├── utils/              # General utilities
* │   │   ├── __init__.py
* │   │   └── utils.py        # Point size estimation core (determine_point_size)
* │   │   └── point_size_determination.py # Workflow Step 2: get_point_size function
* │   │
* │   └── workflow/           # Workflow orchestration and reporting
* │       ├── __init__.py
* │       └── workflow.py     # Main orchestrator function (run_indicator_workflow)
* │       └── reporting.py    # Summary printing function (print_summary)
* │
* ├── models/               # Saved ML models, scalers, etc. (consider adding to .gitignore)
* ├── results/              # Output results (metrics, plots, reports)
* ├── config/               # Configuration files (if any)
* ├── .gitignore            # Specifies intentionally untracked files that Git should ignore
* ├── requirements.txt      # Project dependencies
* ├── run_analysis.py       # Main entry point script for running analysis
* └── README.md             # Project documentation (this file)

## Installation

1.  **Clone Repository:**
    ```bash
    git clone <your_repository_url>
    cd neozork-hld-prediction
    ```

2.  **Create & Activate Virtual Environment (Recommended: Python 3.12):**
    * Using `venv`:
        ```bash
        # Make sure Python 3.12 is installed and accessible
        python3.12 -m venv venv
        source venv/bin/activate
        # Or configure via PyCharm's interpreter settings, selecting Python 3.12 as base
        ```
    * Using `conda`:
        ```bash
        conda create -n neozork_ml python=3.12
        conda activate neozork_ml
        ```

3.  **Install Dependencies:**
    * Upgrade pip: `pip install --upgrade pip`
    * *(Optional but recommended for speed):* Install uv: `pip install uv`
    * Install requirements (use `uv pip install` or `uv sync` if using uv):
        ```bash
        pip install -r requirements.txt
        # Or using uv:
        # uv pip install -r requirements.txt
        ```
        *(Note: Ensure `requirements.txt` lists all necessary packages identified in the Tech Stack. Create it initially with `pip freeze > requirements.txt` after installing manually)*

4.  **Install TA-Lib C Library (if using `TA-Lib` Python package instead of `ta`):**
    * On macOS with Homebrew:
        ```bash
        brew install ta-lib
        ```
    * Then install the Python wrapper (it should be listed in `requirements.txt`): `pip install TA-Lib`

## Data Flow

1.  **Initial Setup:**
    * Export 5-10 years of M1 OHLCV data and the corresponding original MQL5 indicator predictions from MT5 to CSV files.
    * Place these files in `data/raw/`.
    * Run data processing scripts (e.g., via `src/data_ingestion.py --mode initial_load`) to load, merge, clean, run the Python indicator replica, validate replication, calculate ground truth, and save to `data/processed/`.
2.  **Ongoing Operation:**
    * Use data ingestion scripts (e.g., `src/data_ingestion.py --mode fetch_live`) to get the latest OHLCV data from the chosen feed (e.g., `yfinance`).
    * The prediction pipeline (`src/prediction_pipeline.py`) uses this new data to run the Python indicator, generate features, and apply the trained ML model for enhanced HLD forecasts.

## Project Workflow / Detailed Plan

### Phase 0: Setup & Foundation
* [x] 0.1. Version Control Setup (Local Git, GitHub Remote, `.gitignore`)
* [x] 0.2. Development Environment Setup (PyCharm, Python 3.12+, `venv`, Base Libraries)

### Phase 1: Indicator Replication & Validation (Python)
* [ ] 1.1. Understand Original MQL5 Logic (Inputs, Calculations, Outputs) & Document.
* [ ] 1.2. Python Implementation (`src/indicator_logic.py`): Translate MQL5 logic using Pandas/NumPy.
* [ ] 1.3. Unit Testing (Recommended): Write tests for core calculation components.
* [ ] 1.4. Plan Replication Validation Strategy (Comparison method, tolerance).
* [x] 1.5. Add Project Versioning (`src/__init__.py` with `__version__`, Git Tag).

### Phase 2: Data Ingestion & Preparation (Initial MT5 Export)
* [ ] 2.1. Export Original MQL5 Indicator Predictions (CSV from MT5, M1, 5-10 years).
* [ ] 2.2. Export M1 OHLCV Data (CSV from MT5, same period/instrument).
* [ ] 2.3. Load Data in Python (`src/data_ingestion.py`).
* [ ] 2.4. Merge & Align Data (Handle timestamps, missing values).
* [ ] 2.5. Calculate Python Indicator Predictions on historical data.
* [ ] 2.6. **Validate Python Replication:** Compare Python vs MQL5 outputs. Debug `src/indicator_logic.py` until sufficient match achieved. Document results.
* [ ] 2.7. Define Ground Truth (Actual future H/L/D).
* [ ] 2.8. Clean & Save Final Processed Data (`data/processed/`, e.g., Parquet format).

### Phase 3: Exploratory Data Analysis (EDA)
* [ ] 3.1. Load Processed Data (`notebooks/`).
* [ ] 3.2. Analyze Distributions & Statistics (Prices, Indicator outputs, Targets).
* [ ] 3.3. Visualize Time Series (Price, Indicator, Errors).
* [ ] 3.4. Calculate **Baseline Performance** (Python-replicated indicator vs Ground Truth). Document metrics.
* [ ] 3.5. Analyze Indicator Errors (Correlations with volatility, time, etc.).

### Phase 4: Feature Engineering
* [ ] 4.1. Develop Feature Ideas (OHLCV transformations, Indicator outputs/lags, Time features).
* [ ] 4.2. Implement Feature Generation (`src/feature_engineering.py`).
* [ ] 4.3. Feature Scaling/Normalization Plan (`StandardScaler`, `MinMaxScaler`).
* [ ] 4.4. Save Final Feature Set (`data/processed/featured_data.parquet`).

### Phase 5: ML Model Development & Training
* [ ] 5.1. Define ML Problem & Targets (HLD prediction, Error correction, etc.).
* [ ] 5.2. Select Candidate Models (Boosting, NNs like LSTM/GRU/Transformer).
* [ ] 5.3. Establish Validation Strategy (Walk-Forward or Time-Series Splits: Train/Validation/Test). Define metrics.
* [ ] 5.4. Create Training Pipeline (`src/model_training.py`) including scaling, training, tuning.
* [ ] 5.5. Train Initial Models & Tune Hyperparameters (using Validation set/folds). Use cloud resources if needed for speed.
* [ ] 5.6. Save Best Tuned Models & Scalers (`models/`). Document validation scores.

### Phase 6: Evaluation & Selection
* [ ] 6.1. Final Evaluation on **Test Set**. Calculate performance metrics.
* [ ] 6.2. Compare ML vs. Baseline: Quantify improvement. Statistical significance?
* [ ] 6.3. Analyze Feature Importance & Explainability (SHAP).
* [ ] 6.4. Select Best Production Model based on test performance and robustness.

### Phase 7: Backtesting
* [ ] 7.1. Define Trading Strategy Logic (Entries, Exits, Stops, Sizing based on ML predictions).
* [ ] 7.2. Implement Backtesting Engine (`src/backtesting.py` using `VectorBT` or `Backtrader`).
* [ ] 7.3. Run Backtest (incorporating ML model, costs).
* [ ] 7.4. Analyze Backtest Results (Equity Curve, Sharpe, Sortino, Max Drawdown, etc.). Compare vs baseline indicator strategy.

### Phase 8: Strategy Stress-Testing & Robustness Analysis (Monte Carlo Simulation)
* [ ] 8.1. Select & Calibrate Simulation Model (GBM, GARCH, Bootstrap).
* [ ] 8.2. Implement Simulation Engine (`src/mc_simulation.py`? Generate N paths).
* [ ] 8.3. Define Test Scenarios (Parameter sensitivity, volatility shocks).
* [ ] 8.4. Integrate Strategy & Run Simulations over paths.
* [ ] 8.5. Collect & Analyze Simulation Results (Distribution of KPIs, VaR, CVaR).
* [ ] 8.6. Document Robustness Findings. Refine strategy/risk rules if needed.

### Phase 9: Live Data Integration & Forward Testing
* [ ] 9.1. Implement Live Data Feed (`src/data_ingestion.py` using `yfinance` etc.).
* [ ] 9.2. Adapt Prediction Pipeline (`src/prediction_pipeline.py`) for live data.
* [ ] 9.3. Setup Forward Testing (Paper Trading): Generate live predictions, simulate trades, log results. **No real capital.**
* [ ] 9.4. Monitor Forward Test: Compare live simulated performance vs. backtest expectations.

### Phase 10: Monitoring & Maintenance
* [ ] 10.1. Continuous Performance Monitoring (Predictions, Paper Trading PnL).
* [ ] 10.2. Model Drift Detection.
* [ ] 10.3. Periodic Retraining Schedule/Trigger. Implement retraining pipeline.
* [ ] 10.4. Ongoing Maintenance (Library updates, refactoring, documentation).

## Usage Examples

### Running Analysis (`run_analysis.py`)

Replace ticker symbols, intervals, dates, and point sizes as needed.

* **Run with demo data using the default rule (Predict_High_Low_Direction):**
    ```bash
    python run_analysis.py demo
    ```

* **Run with demo data using a specific rule (e.g., Pressure_Vector alias 'PV'):**
    ```bash
    python run_analysis.py demo --rule PV
    ```

* **Fetch Yahoo Finance data for a Forex pair, specific interval, last 3 months, estimated point size, specific rule:**
    ```bash
    python run_analysis.py yf --ticker "EURUSD=X" --interval H1 --period 3mo --rule PV_HighLow
    ```

* **Fetch Yahoo Finance data for a stock, specific date range, user-provided point size, specific rule alias 'SR':**
    ```bash
    python run_analysis.py yfinance --ticker AAPL --start 2024-01-01 --end 2024-04-15 --point 0.01 --rule SR
    ```

* **Fetch Yahoo Finance data for crypto, default interval (D1), specific period, overriding point size:**
    ```bash
    python run_analysis.py yf --ticker "BTC-USD" --period 6mo --point 0.01 --rule PHLD
    ```

### Testing Yahoo Finance Connection (`test_yfinance.py`)

This script performs a minimal download test using `yfinance` for a default ticker ('GOOG').

```bash
python test_yfinance.py

## Usage Examples

(Illustrative command-line examples; implement using `argparse` in scripts)

```bash
# Run data processing after initial export
# python src/data_ingestion.py --mode initial_load ...

# Generate features
# python src/feature_engineering.py ...

# Train a model
# python src/model_training.py --config config/model_lgbm_v1.yaml ...

# Run backtest with a specific model and strategy
# python src/backtesting.py --model models/lgbm_v1/model.joblib --strategy config/strategy_v1.yaml ...

# Run Monte Carlo simulation for the strategy
# python src/mc_simulation.py --strategy config/strategy_v1.yaml --model models/lgbm_v1/model.joblib ...

# Get latest prediction using live feed
# python src/prediction_pipeline.py --ticker "EURUSD=X" --model models/lgbm_v1/model.joblib ...

Evaluation Strategy
Baseline: Performance metrics (Accuracy, MAE, RMSE, F1-score etc.) of the pure Python-replicated indicator (src/indicator_logic.py) on the test set.
ML Model Performance: The same metrics applied to the ML-enhanced predictions on the identical test set. Focus on statistically significant improvement over the baseline.
Out-of-Sample Testing: All final model evaluations and primary backtesting must be performed on data strictly held out from training and hyperparameter tuning (the Test Set).
Backtesting Metrics: Sharpe Ratio, Sortino Ratio, Max Drawdown, Calmar Ratio, Profit Factor, Win Rate, Average Win/Loss size, Trade frequency. Comparison of strategies using baseline vs. ML-enhanced predictions.
Monte Carlo Analysis: Distribution of potential outcomes, drawdown analysis, parameter sensitivity assessment.
TODO / Future Work
Implement core Python scripts (indicator_logic, data_ingestion, feature_engineering, model_training, backtesting, mc_simulation, prediction_pipeline).
Conduct thorough EDA and baseline evaluation.
Train and rigorously evaluate multiple ML models.
Perform detailed backtesting and Monte Carlo analysis.
Refine feature set based on importance analysis.
Optimize hyperparameters using advanced techniques (Optuna/Hyperopt).
Explore more complex model architectures (if warranted).
Develop robust live prediction and (potentially) execution system.