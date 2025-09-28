# SCHR Levels AutoML - Gluon Integration

Advanced AutoML platform for SCHR Levels financial data analysis with comprehensive CLI and web visualization capabilities.

## 🚀 Quick Start

### CLI Usage

```bash
# Show all available options
python schr_gluon_cli.py --help

# Train all models with web visualization
python schr_gluon_cli.py train --symbol BTCUSD --timeframe MN1 --web --browser

# Quick prediction
python schr_gluon_cli.py predict --symbol BTCUSD --timeframe MN1 --web

# Comprehensive backtest
python schr_gluon_cli.py backtest --symbol BTCUSD --timeframe MN1 --web --browser

# Walk-forward validation
python schr_gluon_cli.py validate --type walk-forward --symbol BTCUSD --web

# Monte Carlo validation
python schr_gluon_cli.py validate --type monte-carlo --symbol BTCUSD --web

# Launch web dashboard
python schr_gluon_cli.py web --port 8080 --browser
```

### Demo All Visualizations

```bash
# Launch complete demo with all web visualizations
python demo_schr_gluon.py
```

## 📁 Project Structure

```
src/automl/gluon/
├── __init__.py                 # Main module exports
├── cli/                        # Command-line interface
│   ├── __init__.py
│   ├── main.py                 # CLI controller (300 lines)
│   └── commands.py             # Command implementations (300 lines)
├── web/                        # Web dashboard
│   ├── __init__.py
│   ├── dashboard.py            # Main dashboard (300 lines)
│   ├── components.py           # Visualization components (300 lines)
│   └── templates/
│       └── index.html          # Dashboard template
├── analysis/                   # Analysis tools
│   ├── __init__.py
│   ├── pipeline.py             # Core pipeline (300 lines)
│   ├── backtest.py             # Backtesting engine (300 lines)
│   ├── validator.py            # Validation tools (300 lines)
│   └── evaluator.py            # Model evaluation (300 lines)
├── models/                     # Model management
│   ├── __init__.py
│   ├── manager.py              # Model lifecycle (300 lines)
│   └── persistence.py          # Save/load models (300 lines)
└── utils/                      # Utilities
    ├── __init__.py
    ├── data_loader.py          # Data loading utilities (300 lines)
    ├── feature_engineering.py  # Feature creation (300 lines)
    └── visualization.py        # Plot utilities (300 lines)
```

## 🎯 Features

### CLI Capabilities
- **Flexible Training**: Custom time limits, model exclusions, presets
- **Multiple Tasks**: pressure_vector_sign, price_direction_1period, level_breakout
- **Validation Options**: Walk-forward, Monte Carlo, Cross-validation
- **Backtesting**: Simple, Advanced, Ensemble strategies
- **Web Integration**: Automatic browser launching
- **Performance Tuning**: GPU support, parallel processing, memory limits

### Web Visualizations
- **Backtest Analysis**: Equity curves, drawdown, returns distribution
- **Forecast Predictions**: Price forecasts, confidence intervals, probability heatmaps
- **Walk-Forward Validation**: Fold-by-fold accuracy, stability analysis
- **Monte Carlo Analysis**: Distribution histograms, robustness assessment
- **Accuracy & Stability**: Model comparison, radar charts, recommendations
- **Probabilities Analysis**: Confidence levels, signal strength, risk insights

### Analysis Tools
- **Data Processing**: SCHR Levels data loading and preprocessing
- **Feature Engineering**: Technical indicators, volatility measures
- **Model Training**: AutoGluon integration with custom configurations
- **Validation**: Multiple validation strategies for time series
- **Backtesting**: Comprehensive trading strategy testing
- **Evaluation**: Performance metrics and model comparison

## 🔧 Configuration

### CLI Flags

#### Global Options
- `--verbose, -v`: Enable verbose logging
- `--quiet, -q`: Suppress output except errors
- `--config, -c`: Path to configuration file
- `--output-dir, -o`: Output directory for results
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

#### Data Options
- `--data-path`: Path to data directory
- `--symbol`: Trading symbol (BTCUSD, ETHUSD, EURUSD, etc.)
- `--timeframe`: Timeframe (MN1, W1, D1, H4, H1, M15, M5, M1)

#### Model Options
- `--tasks`: ML tasks to run (pressure_vector_sign, price_direction_1period, level_breakout, all)
- `--time-limit`: Training time limit in seconds
- `--presets`: AutoGluon presets (best_quality, high_quality, good_quality, medium_quality)
- `--exclude-models`: Models to exclude (NN_TORCH, FASTAI, etc.)

#### Validation Options
- `--test-size`: Test set size (0.0-1.0)
- `--cv-folds`: Cross-validation folds
- `--random-state`: Random state for reproducibility

#### Web Options
- `--web`: Enable web visualization
- `--browser`: Open browser automatically
- `--port`: Web server port
- `--host`: Web server host
- `--theme`: Dashboard theme (dark, light)

#### Backtest Options
- `--start-date`: Backtest start date (YYYY-MM-DD)
- `--end-date`: Backtest end date (YYYY-MM-DD)
- `--initial-capital`: Initial capital for backtesting
- `--commission`: Trading commission rate

#### Performance Options
- `--n-jobs`: Number of parallel jobs (-1 for all cores)
- `--memory-limit`: Memory limit for training
- `--gpu`: Enable GPU acceleration

## 📊 Web Dashboard Features

### Interactive Visualizations
- **Real-time Updates**: Auto-refresh capabilities
- **Responsive Design**: Mobile and desktop optimized
- **Dark Theme**: Professional financial interface
- **Multiple Tabs**: Organized by analysis type
- **Export Options**: Save charts and data

### Analysis Components
- **Equity Curves**: Portfolio performance over time
- **Drawdown Analysis**: Risk assessment and management
- **Returns Distribution**: Statistical analysis of returns
- **Probability Heatmaps**: Model confidence visualization
- **Validation Charts**: Model stability assessment
- **Accuracy Comparisons**: Performance benchmarking

## 🎯 Use Cases

### Trading Strategy Development
1. **Data Analysis**: Load and explore SCHR Levels data
2. **Feature Engineering**: Create technical indicators
3. **Model Training**: Train ML models for predictions
4. **Validation**: Test model performance with walk-forward
5. **Backtesting**: Simulate trading strategies
6. **Deployment**: Use models for live trading

### Research & Development
1. **Model Comparison**: Test different algorithms
2. **Parameter Tuning**: Optimize model settings
3. **Feature Selection**: Identify important indicators
4. **Performance Analysis**: Evaluate model stability
5. **Risk Assessment**: Analyze model confidence

### Educational & Demo
1. **Interactive Learning**: Visualize ML concepts
2. **Strategy Testing**: Experiment with different approaches
3. **Performance Tracking**: Monitor model evolution
4. **Results Sharing**: Export and present findings

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install autogluon plotly flask pandas numpy scikit-learn
   ```

2. **Prepare Data**:
   - Ensure SCHR Levels data is in `data/cache/csv_converted/`
   - Data should be in parquet format with required columns

3. **Run Demo**:
   ```bash
   python demo_schr_gluon.py
   ```

4. **Use CLI**:
   ```bash
   python schr_gluon_cli.py --help
   ```

## 📈 Performance

- **Training Speed**: Optimized for fast model training
- **Memory Usage**: Efficient data processing
- **Scalability**: Parallel processing support
- **GPU Acceleration**: CUDA support for compatible hardware
- **Web Performance**: Fast, responsive visualizations

## 🔒 Security

- **Local Processing**: All data stays on your machine
- **No External APIs**: No data sent to external services
- **Configurable Ports**: Choose your own web server ports
- **Access Control**: Localhost-only by default

## 📝 License

This project is part of the Neozork HLD Prediction system.
All rights reserved.

## 🤝 Contributing

1. Follow the 300-line file limit
2. Maintain clean, documented code
3. Add comprehensive tests
4. Update documentation
5. Follow the established project structure

## 📞 Support

For issues and questions:
- Check the CLI help: `python schr_gluon_cli.py --help`
- Review the demo: `python demo_schr_gluon.py`
- Examine the web dashboards for visual guidance