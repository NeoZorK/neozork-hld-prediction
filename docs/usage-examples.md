# Usage Examples

Common commands and use cases.

## Quick Reference

View all examples:
```bash
python run_analysis.py --examples
```

## Interactive Mode

The interactive mode provides a guided interface for selecting indicators and configuring analysis:

```bash
# Start interactive mode
python run_analysis.py --interactive
nz --interactive
```

### Interactive Mode Features

The interactive mode includes the following options:

1. **Select Analysis Mode** - Choose data source (demo, CSV, Yahoo Finance, etc.)
2. **Select Indicator** - Browse and select from available indicators
3. **Configure Data Source** - Set up data source parameters
4. **Configure Plotting** - Choose visualization method
5. **Configure Export** - Select export formats
6. **Show Current Configuration** - Review your settings
7. **Run Analysis** - Execute the analysis
8. **Help** - Show help information
9. **List Available Indicators** - Browse all available indicators with detailed information
0. **Exit** - Leave interactive mode

### List Available Indicators (Option 9)

The "List Available Indicators" option provides comprehensive information about all available indicators:

- **Category Overview**: Shows all indicator categories with counts
- **Detailed List**: Displays specific indicators in each category with descriptions
- **Visual Organization**: Uses emojis and colors for better readability
- **Quick Reference**: Shows indicator names and descriptions for easy selection

Example output:
```
🎯 Available Indicator Categories:
==================================================
⚡ momentum        - 2 indicators
🔄 oscillators     - 3 indicators
🔮 predictive      - 2 indicators
...

📋 Detailed Indicator List:
============================================================

⚡ Momentum Indicators:
────────────────────────────────────────
   1. MACD                 - Moving Average Convergence Divergence
   2. Stochastic Oscillator - Stochastic Oscillator
```

## Demo Mode

```bash
# Basic demo
python run_analysis.py demo
nz demo

# Specific rules
nz demo --rule PHLD
nz demo --rule PV_HighLow
nz demo --rule SR

# Different plot backends
nz demo -d plotly
nz demo -d seaborn
```

## Real Data Analysis

### Yahoo Finance
```bash
# Single ticker
nz yf -t AAPL --period 1mo --point 0.01

# Multiple timeframes
nz yf -t MSFT --period 3mo --interval 1h

# Show cached data
nz show yf aapl
```

### CSV Files
```bash
# Analyze CSV (MT5 export format)
nz csv --csv-file data/EURUSD_M1.csv --point 0.0001

# With specific rule
nz csv --csv-file data.csv --rule PHLD --point 0.01
```

### Exchange Rate API (Real-time FX)
```bash
# Free Plan - Current rates only
nz exrate -t EURUSD --interval D1 --point 0.00001

# Paid Plan - Historical data with indicators
nz exrate -t GBPJPY --interval D1 --start 2025-01-01 --end 2025-06-01 --point 0.01 --rule PV

# Free Plan - Different currency formats
nz exrate -t EUR/USD --interval D1 --point 0.00001
nz exrate -t EUR_USD --interval D1 --point 0.00001

# Free Plan - Terminal plotting (great for SSH/Docker)
nz exrate -t USDCAD --interval D1 --point 0.00001 -d term

# Show cached exchange rate data
nz show exrate
```

**Note:** Exchange Rate API provides current rates only (free plan). Date ranges are ignored.

### Binance Data
```bash
# Cryptocurrency analysis
nz binance -t BTCUSDT --period 1d --point 0.01
```

## Data Management

### Show Data
```bash
# List available data
nz show

# Show specific source
nz show yf
nz show binance
nz show exrate
```

### Cache Management
```bash
# Clear cache
nz clear-cache

# Force refresh
nz yf -t AAPL --period 1mo --force-refresh
```

## EDA and Analysis

```bash
# Run EDA batch processing
python -m src.eda.eda_batch_check

# Generate plots
python -m src.plotting.fastest_auto_plot data/file.parquet

# Data quality checks
python -m src.eda.data_quality
```

## Docker Usage

```bash
# Run in container
docker compose run --rm neozork-hld nz demo

# Interactive session
docker compose run --rm neozork-hld bash
```

For installation: [Getting Started](getting-started.md)  
For analysis tools: [Analysis & EDA](analysis-eda.md)

## Exporting Indicators: Usage Examples

Export flags (`--export-parquet`, `--export-csv`, `--export-json`) are only allowed in `demo` mode. They are forbidden in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, and `exrate` modes.

### Recommended Workflow

1. **Download or Convert Data**
   - Download with yfinance:
     ```bash
     python run_analysis.py yfinance --ticker BTCUSD --period 1y --point 0.01
     ```
   - Or convert from CSV:
     ```bash
     python run_analysis.py csv --csv-file mydata.csv --point 0.01
     ```
2. **Apply Indicator and Export**
   - Use show mode with a rule and export flags:
     ```bash
     python run_analysis.py show yfinance BTCUSD --rule PHLD --export-parquet --export-csv --export-json
     ```
3. **View Exported Indicators**
   - Use show ind to view the exported files:
     ```bash
     python run_analysis.py show ind parquet
     python run_analysis.py show ind csv
     python run_analysis.py show ind json
     ```

> Export flags are not available in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, or `exrate` modes. Use `demo` for direct export, or the above workflow for real data.