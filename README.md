# Neozork Indicator ML Enhancement

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

## Tech Stack

* **Language:** Python 3.9+
* **Core Libraries:** `pandas`, `numpy`
* **ML / Deep Learning:** `scikit-learn`, `xgboost`, `lightgbm`, `tensorflow`/`keras` or `pytorch`
* **Data Feeds:** `yfinance` (or other API client), `MetaTrader5` (for initial data export only)
* **Backtesting:** `VectorBT` (recommended for M1 data speed), `Backtrader`
* **Environment:** `venv` (recommended) or `conda`
* **Version Control:** `git`

## Project Structure
