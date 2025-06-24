# CLI Interface Guide

Complete guide to the command-line interface for the Neozork HLD Prediction project.

## Overview

The CLI interface provides a powerful command-line tool for data analysis, indicator calculations, and automated workflows.

## Main CLI Entry Point

### `run_analysis.py`

The main entry point for all CLI operations.

```bash
python run_analysis.py [mode] [options]
```

## Available Modes

### 1. Demo Mode

Run analysis with demo data for testing and demonstration.

```bash
# Basic demo
python run_analysis.py demo

# Demo with specific rule
python run_analysis.py demo --rule RSI

# Demo with export
python run_analysis.py demo --rule PHLD --export-parquet --export-csv --export-json
```

#### Demo Mode Options
- **`--rule`** - Trading rule to apply (RSI, MACD, PHLD, PV, SR)
- **`--export-parquet`** - Export results to Parquet format
- **`--export-csv`** - Export results to CSV format
- **`--export-json`** - Export results to JSON format

### 2. Yahoo Finance Mode

Fetch and analyze data from Yahoo Finance.

```bash
# Stock analysis
python run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule RSI

# Forex analysis
python run_analysis.py yfinance --ticker EURUSD=X --period 6mo --point 0.00001 --rule MACD

# Multiple indicators
python run_analysis.py yfinance --ticker GOOGL --period 1y --point 0.01 --rule PHLD,PV,SR
```

#### Yahoo Finance Options
- **`--ticker`** - Stock/forex symbol (required)
- **`--period`** - Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- **`--point`** - Price precision (required)
- **`--rule`** - Trading rule(s) to apply
- **`--interval`** - Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo, 3mo)

### 3. Binance Mode

Analyze cryptocurrency data from Binance.

```bash
# BTC/USDT analysis
python run_analysis.py binance --symbol BTCUSDT --interval 1h --point 0.01 --rule RSI

# Multiple timeframes
python run_analysis.py binance --symbol ETHUSDT --interval 4h --point 0.01 --rule MACD,PHLD
```

#### Binance Options
- **`--symbol`** - Trading pair (required)
- **`--interval`** - Time interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
- **`--point`** - Price precision (required)
- **`--rule`** - Trading rule(s) to apply
- **`--limit`** - Number of data points (max 1000)

### 4. CSV Mode

Analyze local CSV files.

```bash
# Basic CSV analysis
python run_analysis.py csv --csv-file data/my_data.csv --point 0.01 --rule RSI

# Custom column mapping
python run_analysis.py csv --csv-file data/custom.csv --point 0.01 --rule MACD \
    --date-col timestamp --price-cols open,high,low,close --volume-col volume
```

#### CSV Options
- **`--csv-file`** - Path to CSV file (required)
- **`--point`** - Price precision (required)
- **`--rule`** - Trading rule(s) to apply
- **`--date-col`** - Column name for timestamps
- **`--price-cols`** - Comma-separated OHLC column names
- **`--volume-col`** - Column name for volume data

### 5. Exchange Rate Mode

Analyze forex data from Exchange Rate API.

```bash
# EUR/USD analysis
python run_analysis.py exrate --ticker EURUSD --interval D1 --point 0.00001 --rule PV

# Multiple currency pairs
python run_analysis.py exrate --ticker GBPUSD,USDJPY --interval D1 --point 0.00001 --rule SR
```

#### Exchange Rate Options
- **`--ticker`** - Currency pair(s) (required)
- **`--interval`** - Time interval (D1, W1, M1)
- **`--point`** - Price precision (required)
- **`--rule`** - Trading rule(s) to apply

### 6. Show Mode

Display and analyze existing data.

```bash
# Show available indicators
python run_analysis.py show ind

# Show specific indicator data
python run_analysis.py show ind parquet
python run_analysis.py show ind csv
python run_analysis.py show ind json

# Show with analysis
python run_analysis.py show yfinance AAPL --rule PHLD --export-parquet
```

#### Show Mode Options
- **`ind`** - Show indicator data
- **`yfinance`** - Show Yahoo Finance data with analysis
- **`csv`** - Show CSV data with analysis
- **`--rule`** - Trading rule(s) to apply
- **`--export-*`** - Export options (only in demo mode)

### 7. Interactive Mode

Guided interactive analysis session.

```bash
# Start interactive session
python run_analysis.py interactive

# Interactive with preset options
python run_analysis.py interactive --preset stock_analysis
```

#### Interactive Mode Features
- **Guided setup** - Step-by-step configuration
- **Data source selection** - Choose from available sources
- **Indicator selection** - Select technical indicators
- **Parameter configuration** - Set indicator parameters
- **Analysis execution** - Run analysis with selected options

## Trading Rules

### Available Rules

1. **RSI** - Relative Strength Index
2. **MACD** - Moving Average Convergence Divergence
3. **PHLD** - Price High Low Direction
4. **PV** - Pressure Vector
5. **SR** - Support Resistance

### Rule Combinations

```bash
# Single rule
python run_analysis.py demo --rule RSI

# Multiple rules
python run_analysis.py demo --rule RSI,MACD,PHLD

# All rules
python run_analysis.py demo --rule ALL
```

## Export Options

### Export Formats

- **Parquet** - High-performance columnar format
- **CSV** - Comma-separated values
- **JSON** - JavaScript Object Notation

### Export Usage

```bash
# Export to all formats
python run_analysis.py demo --rule PHLD --export-parquet --export-csv --export-json

# Export to specific format
python run_analysis.py demo --rule RSI --export-parquet
```

### Export Locations

- **Parquet**: `data/indicators/parquet/`
- **CSV**: `data/indicators/csv/`
- **JSON**: `data/indicators/json/`

## Advanced Options

### Data Processing

```bash
# Custom point size
python run_analysis.py yfinance --ticker AAPL --point 0.001 --rule RSI

# Specific time period
python run_analysis.py yfinance --ticker AAPL --period 6mo --rule MACD

# High-frequency data
python run_analysis.py yfinance --ticker AAPL --interval 1h --rule PHLD
```

### Analysis Configuration

```bash
# Verbose output
python run_analysis.py demo --rule RSI --verbose

# Quiet mode
python run_analysis.py demo --rule RSI --quiet

# Debug mode
python run_analysis.py demo --rule RSI --debug
```

## Examples

### Stock Analysis

```bash
# Apple stock with RSI
python run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule RSI

# Google stock with multiple indicators
python run_analysis.py yfinance --ticker GOOGL --period 6mo --point 0.01 --rule RSI,MACD,PHLD

# Export results
python run_analysis.py yfinance --ticker MSFT --period 1y --point 0.01 --rule PHLD --export-parquet
```

### Forex Analysis

```bash
# EUR/USD with Pressure Vector
python run_analysis.py exrate --ticker EURUSD --interval D1 --point 0.00001 --rule PV

# Multiple pairs
python run_analysis.py exrate --ticker EURUSD,GBPUSD,USDJPY --interval D1 --point 0.00001 --rule SR
```

### Cryptocurrency Analysis

```bash
# Bitcoin analysis
python run_analysis.py binance --symbol BTCUSDT --interval 1h --point 0.01 --rule RSI

# Ethereum with multiple timeframes
python run_analysis.py binance --symbol ETHUSDT --interval 4h --point 0.01 --rule MACD,PHLD
```

### Custom Data Analysis

```bash
# CSV file analysis
python run_analysis.py csv --csv-file data/my_data.csv --point 0.01 --rule RSI

# Custom column mapping
python run_analysis.py csv --csv-file data/custom.csv --point 0.01 --rule MACD \
    --date-col date --price-cols o,h,l,c --volume-col vol
```

## Error Handling

### Common Errors

```bash
# Invalid symbol
python run_analysis.py yfinance --ticker INVALID --period 1y --point 0.01 --rule RSI
# Error: Symbol not found

# Invalid period
python run_analysis.py yfinance --ticker AAPL --period invalid --point 0.01 --rule RSI
# Error: Invalid period

# Missing required parameter
python run_analysis.py yfinance --ticker AAPL --period 1y --rule RSI
# Error: Point size is required
```

### Troubleshooting

```bash
# Enable debug mode
python run_analysis.py demo --rule RSI --debug

# Check available options
python run_analysis.py --help

# Check specific mode help
python run_analysis.py yfinance --help
```

## Configuration

### Environment Variables

```bash
# API Keys
export POLYGON_API_KEY="your_polygon_api_key"
export BINANCE_API_KEY="your_binance_api_key"
export BINANCE_SECRET_KEY="your_binance_secret"

# Logging
export LOG_LEVEL="INFO"
export LOG_FILE="logs/cli.log"

# Cache settings
export CACHE_ENABLED="true"
export CACHE_TTL="3600"
```

### Configuration Files

```bash
# Create config file
cat > config.yaml << EOF
api_keys:
  polygon: "your_polygon_api_key"
  binance: "your_binance_api_key"

defaults:
  point_size: 0.01
  period: "1y"
  interval: "1d"

export:
  enabled: true
  formats: ["parquet", "csv"]
EOF
```

## Performance Tips

### Optimization

1. **Use appropriate point sizes** - Match your data precision
2. **Select relevant time periods** - Don't fetch unnecessary data
3. **Batch processing** - Process multiple symbols together
4. **Enable caching** - Reuse fetched data

### Memory Management

```bash
# Process large datasets in chunks
python run_analysis.py csv --csv-file large_data.csv --point 0.01 --rule RSI --chunk-size 10000

# Use streaming for very large files
python run_analysis.py csv --csv-file huge_data.csv --point 0.01 --rule RSI --stream
```

## Related Documentation

- **[Data Sources](../api/data-sources.md)** - Available data sources
- **[Trading Rules](../reference/trading-rules.md)** - Rule descriptions
- **[Export Functions](../guides/export-functions.md)** - Export capabilities
- **[Analysis Tools](../guides/analysis-tools.md)** - Analysis features

## Indicator Options

### Basic Indicators
```bash
--rule RSI          # Relative Strength Index
--rule MACD         # Moving Average Convergence Divergence
--rule EMA          # Exponential Moving Average
--rule BB           # Bollinger Bands
--rule ATR          # Average True Range
--rule VWAP         # Volume Weighted Average Price
```

### Advanced Indicators
```bash
--rule RSI_Momentum     # RSI with momentum analysis
--rule RSI_Divergence   # RSI with divergence detection
--rule MonteCarlo       # Monte Carlo simulation
--rule Kelly            # Kelly Criterion
--rule FearGreed        # Fear & Greed Index
--rule COT              # Commitments of Traders
```

### Pressure Vector Indicators
```bash
--rule PV              # Pressure Vector (alias)
--rule SR              # Support/Resistance (alias)
--rule PHLD            # Predict High/Low Direction (alias)
```

## Strategy Parameters

### New: --strategy Flag
The `--strategy` flag allows you to specify trading strategy parameters for advanced metrics calculation:

```bash
--strategy LOT,RISK_REWARD,FEE
```

**Parameters:**
- `LOT` - Position size (default: 1.0)
- `RISK_REWARD` - Risk to reward ratio (default: 2.0)
- `FEE` - Fee per trade in percentage (default: 0.07)

**Examples:**
```bash
# Default strategy (1.0 lot, 2:1 risk/reward, 0.07% fee)
python run_analysis.py demo --rule RSI --strategy 1,2,0.07

# Conservative strategy (0.5 lot, 1.5:1 risk/reward, 0.05% fee)
python run_analysis.py demo --rule RSI --strategy 0.5,1.5,0.05

# Aggressive strategy (2.0 lot, 3:1 risk/reward, 0.1% fee)
python run_analysis.py demo --rule RSI --strategy 2,3,0.1
```

## Advanced Metrics

When using the `--strategy` flag, the system calculates comprehensive trading metrics including:

### Basic Metrics
- **Buy/Sell Signals**: Count of buy and sell signals
- **Win Ratio**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profit to gross loss
- **Sharpe Ratio**: Risk-adjusted return measure
- **Sortino Ratio**: Downside risk-adjusted return
- **Maximum Drawdown**: Largest peak-to-trough decline

### Strategy-Specific Metrics
- **Position Size**: Current position size setting
- **Risk/Reward Setting**: Configured risk-to-reward ratio
- **Fee per Trade**: Transaction cost percentage
- **Kelly Fraction**: Optimal position sizing ratio
- **Net Return**: Returns after fees
- **Strategy Efficiency**: Fee-adjusted performance
- **Strategy Sustainability**: Overall strategy robustness score

### Machine Learning Metrics
- **Signal Frequency**: How often signals occur
- **Signal Stability**: Consistency of signal patterns
- **Signal Accuracy**: Percentage of correct signals
- **Timing Score**: Quality of signal timing
- **Pattern Consistency**: Reliability of patterns
- **Signal Clustering**: Concentration of signals

### Monte Carlo Metrics
- **Expected Return**: Average return from simulations
- **Value at Risk (VaR)**: Maximum expected loss
- **Conditional VaR**: Expected loss beyond VaR
- **Profit Probability**: Chance of positive returns
- **Strategy Robustness**: Consistency across simulations
- **Risk of Ruin**: Probability of account depletion

## Plotting Options

### Plot Types
```bash
-d fastest    # Plotly + Dask + Datashader (default)
-d fast       # Dask + Datashader + Bokeh
-d plotly     # Interactive Plotly charts
-d mpl        # Static matplotlib charts
-d seaborn    # Statistical seaborn plots
-d term       # Terminal-based charts
```

### Metrics Display
- **Main Metrics**: Displayed in bottom-right corner
- **Additional Metrics**: Displayed in separate panel (left side)
- **Color Coding**: Green (good), Yellow (average), Red (poor)
- **Strategy Info**: Position size, risk/reward, fees prominently displayed

## Examples

### Complete Analysis with Strategy
```bash
# Analyze RSI with custom strategy parameters
python run_analysis.py demo --rule RSI --strategy 1.5,2.5,0.08 -d fastest

# Show existing data with strategy analysis
python run_analysis.py show csv mn1 gbp --rule RSI_Divergence --strategy 1,2,0.07 -d fastest
```

### Export Options
```bash
--export-parquet    # Export to Parquet format
--export-csv        # Export to CSV format
--export-json       # Export to JSON format
```

## Help and Examples

```bash
# Show help
python run_analysis.py --help

# Show examples
python run_analysis.py --examples

# List available indicators
python run_analysis.py --indicators

# Interactive mode
python run_analysis.py --interactive
``` 