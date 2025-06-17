# Project Overview

## Core Goals

The NeoZork HLD Prediction project focuses on **professional enhancement of a proprietary trading indicator's predictive capabilities** using advanced Machine Learning (ML) techniques implemented in Python.

### Primary Objectives

* **Indicator Replication:** Accurately translate and validate the core logic of the original MQL5 HLD indicator into a pure Python implementation
* **ML-Powered Enhancement:** Develop a robust ML pipeline that takes features derived from OHLCV data and the Python indicator's output to generate significantly improved HLD predictions
* **High-Resolution Data Utilization:** Leverage 5-10 years of historical M1 OHLCV data for comprehensive feature engineering and training
* **Rigorous Validation:** Employ state-of-the-art validation techniques (walk-forward validation, strict time-series splits) to ensure model robustness
* **Performance Evaluation:** Quantify the improvement over the baseline Python-replicated indicator using statistical metrics
* **Profitability Focus:** Structure the project towards creating forecasts that provide a demonstrable statistical edge for potential trading profitability

## Key Features

* **Multiple Data Sources:** Demo data, CSV files (MT5 export format), Yahoo Finance, Polygon.io, and Binance Spot
* **Core Calculations:** Pressure Vector indicator components and derived rules (`PV_HighLow`, `Support_Resistants`, `Pressure_Vector`, `Predict_High_Low_Direction`)
* **Data Validation:** Python calculations against original MQL5 results when using CSV mode
* **Advanced Plotting:** Multiple visualization backends including `mplfinance`, `plotly`, `seaborn`, and terminal plotting
* **Automatic Data Caching:** Raw OHLCV data fetched from API sources saved to efficient `.parquet` files
* **Comprehensive Testing:** Unit tests for key components and validation scripts
* **Modular Structure:** Clear separation of concerns (data fetching, calculation, plotting, workflow)

## Core Methodology

### 1. Indicator Logic Replication
Translate the mathematical and logical steps of the MQL5 indicator into an equivalent Python function. Validate output against the original MQL5 version using exported historical predictions.

### 2. Data Management
- **Initial Load:** Process one-time export of M1 OHLCV and original MQL5 indicator predictions from MT5
- **Data Feeds:** Fetch and update OHLCV data from Yahoo Finance, CSV files, Polygon.io API, or other data providers

### 3. Feature Engineering (ML-Centric)
- Derive features primarily from M1 OHLCV data (price transformations, volatility measures, time-based patterns)
- Incorporate outputs of the Python-replicated indicator as key features for ML models
- Focus on enhancing the proprietary indicator's signals rather than standard external technical indicators

### 4. Advanced ML Modeling
- Train sophisticated ML models suited for time-series forecasting (XGBoost, LightGBM, LSTMs, GRUs, Transformers)
- Experiment with different prediction targets: H/L/D prediction, error prediction, confidence prediction

### 5. Validation & Testing
- Implement walk-forward validation or anchored time-series splits
- Use hyperparameter optimization libraries (Optuna, Hyperopt) for optimal model configurations
- Perform realistic backtests with transaction costs using VectorBT or Backtrader

### 6. Stress-Testing
Apply Monte Carlo simulations to assess strategy robustness and risk profile under various market conditions.

## Data Caching System

### CSV Mode Caching
- Processed data saved to `.parquet` files in `data/cache/csv_converted/`
- Cache filename corresponds to original CSV filename
- Subsequent runs load directly from Parquet cache

### API Mode Caching
- Data cached in `data/raw_parquet/` directory
- Separate file for each instrument (ticker + interval + mode)
- Automatic identification of missing date ranges for incremental fetching
- Smart cache updates to minimize API calls

**Important:** Delete relevant cache files when modifying data loading or processing code to ensure changes take effect.

## Validation Results

Based on comparisons using MQL5 CSV export data:

* **Core Calculations:** Python implementation of `Pressure` and `PV` calculations shows high accuracy (Correlation=1.0, minimal Mean Absolute Difference)
* **Predicted Low/High:** Current Python implementation shows systematic differences (~6.8 points MAD in sample XAUUSD MN1 data, though Correlation > 0.999)

## Tech Stack

* **Core:** Python 3.12+, pandas, numpy
* **ML/DL:** scikit-learn, xgboost, lightgbm, tensorflow/pytorch
* **Data Feeds:** yfinance, CSV reader, polygon-api-client
* **Backtesting:** VectorBT, Backtrader
* **Visualization:** mplfinance, matplotlib, seaborn, plotly, rich
* **Environment:** Docker, uv package manager
