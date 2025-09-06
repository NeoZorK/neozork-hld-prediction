# 🚀 NeoZork Interactive ML Trading Strategy Development System

## 📋 Overview

The NeoZork Interactive ML Trading Strategy Development System is a comprehensive platform for developing robust, profitable machine learning models for trading on blockchains. This system supports deployment on both Centralized Exchanges (CEX) and Decentralized Exchanges (DEX) with real-time monitoring and automated retraining capabilities.

## 🎯 Key Features

### 🎨 **Modern Interactive Interface**
- Colorful, modern terminal-based menu system
- Progress bars with ETA indicators
- Smooth navigation and error handling
- Graceful exit with CTRL+C

### 📊 **Comprehensive Data Management**
- **CSV Converted Data**: Load .parquet files from `data/cache/csv_converted/`
- **Raw Parquet Data**: Load exchange data from `data/raw_parquet/`
- **Indicators Data**: Load technical indicators from `data/indicators/`
- **Cleaned Data**: Load processed data from `data/cleaned_data/`
- **Multiple Data Sources**: Binance, Bybit, Kraken, Web3, Polygon APIs

### 🔍 **Advanced EDA Analysis**
- Time series gaps analysis
- Duplicate detection
- Missing data analysis (NaN, Zero, Negative, Infinity)
- Outlier detection
- Basic statistics and correlation analysis
- Interactive data visualization

### ⚙️ **Feature Engineering**
- **Premium Indicators**: PHLD, PV, SR, WAVE
- **Technical Indicators**: RSI, MACD, Bollinger Bands, ATR
- **Statistical Features**: Rolling statistics, momentum, volatility
- **Temporal Features**: Time-based, seasonal, cyclical
- **Cross-Timeframe Features**: Multi-timeframe analysis
- **Feature Selection**: Automated optimization

### 🤖 **ML Model Development**
- **Model Selection**: Compare multiple algorithms
- **Hyperparameter Tuning**: Grid search, Bayesian optimization
- **Walk Forward Analysis**: Robust validation technique
- **Monte Carlo Simulation**: Risk assessment and scenario generation
- **Apple MLX Integration**: Native Apple Silicon ML framework
- **Model Evaluation**: Comprehensive performance metrics

### 📈 **Backtesting & Validation**
- Strategy backtesting with realistic conditions
- Portfolio analysis and optimization
- Risk analysis and management
- Monte Carlo portfolio simulation
- Performance metrics calculation

### 🚀 **Deployment & Monitoring**
- **Trading Bot**: Automated strategy execution
- **Order Management**: CEX and DEX order handling
- **Position Management**: Portfolio tracking
- **Risk Management**: Real-time risk control
- **Real-time Monitoring**: System health and performance
- **Alert System**: Customizable notifications

## 🏗️ Architecture

```
interactive/
├── neozork.py                 # Main entry point
├── menu_system/              # Interactive menu system
│   ├── main_menu.py          # Main menu controller
│   ├── data_loading_menu.py  # Data loading submenu
│   ├── eda_menu.py           # EDA analysis submenu
│   ├── feature_engineering_menu.py
│   ├── ml_development_menu.py
│   ├── backtesting_menu.py
│   ├── deployment_menu.py
│   ├── monitoring_menu.py
│   └── base_menu.py          # Base menu class
├── data_management/          # Data handling
│   ├── data_loader.py        # Data loading
│   ├── data_validator.py     # Data validation
│   ├── data_processor.py     # Data processing
│   └── data_sources/         # Exchange connectors
│       ├── binance_connector.py
│       ├── bybit_connector.py
│       ├── kraken_connector.py
│       ├── web3_connector.py
│       └── polygon_connector.py
├── eda_analysis/             # Exploratory data analysis
│   ├── data_quality_analyzer.py
│   ├── statistical_analyzer.py
│   ├── visualization_analyzer.py
│   └── report_generator.py
├── feature_engineering/      # Feature generation
│   ├── technical_indicators.py
│   ├── premium_indicators.py
│   ├── statistical_features.py
│   ├── temporal_features.py
│   ├── cross_timeframe_features.py
│   └── feature_selector.py
├── ml_development/           # Machine learning
│   ├── model_selector.py
│   ├── hyperparameter_tuner.py
│   ├── walk_forward_analyzer.py
│   ├── monte_carlo_simulator.py
│   ├── model_evaluator.py
│   └── model_retrainer.py
├── backtesting/              # Strategy validation
│   ├── strategy_backtester.py
│   ├── portfolio_analyzer.py
│   ├── risk_analyzer.py
│   └── performance_metrics.py
├── deployment/               # Trading deployment
│   ├── trading_bot.py
│   ├── order_manager.py
│   ├── position_manager.py
│   └── risk_manager.py
├── monitoring/               # System monitoring
│   ├── system_monitor.py
│   ├── performance_monitor.py
│   ├── alert_manager.py
│   └── dashboard_generator.py
└── utils/                    # Utility functions
    ├── config_manager.py
    ├── logger.py
    ├── data_utils.py
    └── math_utils.py
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- uv package manager
- Required dependencies (see `requirements.txt`)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd neozork-hld-prediction

# Install dependencies
uv sync

# Make the script executable
chmod +x interactive/neozork.py
```

### Running the System
```bash
# Run the interactive system
python interactive/neozork.py

# Or using uv
uv run interactive/neozork.py

# Or directly execute
./interactive/neozork.py
```

## 📖 Usage

### Main Menu
The system starts with a colorful main menu offering:

1. **📊 Load Data** - Load data from various sources
2. **🔍 EDA Analysis** - Comprehensive data analysis
3. **⚙️ Feature Engineering** - Generate and optimize features
4. **🤖 ML Model Development** - Develop and train ML models
5. **📈 Backtesting & Validation** - Test and validate strategies
6. **🚀 Deployment & Monitoring** - Deploy and monitor strategies
7. **📊 Data Visualization** - Interactive data visualization
8. **⚙️ System Configuration** - Configure system settings
9. **❓ Help & Documentation** - Access help and documentation
0. **🚪 Exit** - Exit the system

### Data Loading
The data loading menu supports:
- **CSV Converted**: Load processed .parquet files
- **Raw Parquet**: Load raw exchange data
- **Indicators**: Load technical indicators
- **Cleaned Data**: Load preprocessed data

Each option shows progress with ETA and displays:
- Symbol information
- Data size in MB
- Available timeframes
- Number of rows
- Start/end timestamps

### EDA Analysis
Comprehensive data quality analysis:
- **Time Series Gaps**: Detect missing time periods
- **Duplicates**: Find duplicate records
- **NaN Values**: Analyze missing data
- **Zero Values**: Check for zero values
- **Negative Values**: Analyze negative values
- **Infinity Values**: Detect infinite values
- **Outliers**: Identify statistical outliers
- **Basic Statistics**: Generate summary statistics
- **Correlation Analysis**: Calculate correlations
- **EDA Report**: Generate comprehensive reports

## 🔧 Configuration

The system uses a configuration file (`config.json`) for settings:
- Data source configurations
- Model parameters
- Trading settings
- Monitoring thresholds
- Alert configurations

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
uv run pytest tests/interactive/ -v

# Run specific test modules
uv run pytest tests/interactive/test_menu_system.py -v
uv run pytest tests/interactive/test_data_management.py -v
```

## 📊 Monitoring

The system includes comprehensive monitoring:
- **System Health**: CPU, memory, disk usage
- **Performance Metrics**: Strategy performance tracking
- **Error Monitoring**: Error detection and logging
- **Alert System**: Customizable notifications
- **Dashboard**: Real-time monitoring dashboard

## 🚀 Deployment

### CEX Deployment
- Binance integration
- Bybit integration
- Kraken integration
- Order management
- Position tracking

### DEX Deployment
- Web3 integration
- Uniswap support
- PancakeSwap support
- Token swapping
- Liquidity management

## 📈 Performance

The system is optimized for:
- **Speed**: Fast data processing and model training
- **Memory**: Efficient memory usage
- **Scalability**: Handle large datasets
- **Reliability**: Robust error handling
- **Security**: Secure API connections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation in `docs/interactive/`
- Review the strategic plans
- Open an issue on GitHub
- Contact the development team

## 🔮 Roadmap

### Phase 1: Core Infrastructure ✅
- [x] Interactive menu system
- [x] Data loading capabilities
- [x] Basic EDA analysis
- [x] Architecture foundation

### Phase 2: Feature Engineering (Next)
- [ ] Premium indicators implementation
- [ ] Technical indicators
- [ ] Statistical features
- [ ] Cross-timeframe features

### Phase 3: ML Development
- [ ] Model selection and training
- [ ] Hyperparameter optimization
- [ ] Walk forward analysis
- [ ] Monte Carlo simulation

### Phase 4: Deployment & Monitoring
- [ ] Trading bot implementation
- [ ] Real-time monitoring
- [ ] Alert system
- [ ] Dashboard generation

---

**🚀 Ready to develop profitable trading strategies? Start with `python interactive/neozork.py`!**
