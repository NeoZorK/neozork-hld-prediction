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

## Indicator Discovery and Help

### List All Indicators
```bash
# Show all available indicators
python run_analysis.py --indicators

# Show indicators by category
python run_analysis.py --indicators oscillators
python run_analysis.py --indicators trend
python run_analysis.py --indicators momentum
python run_analysis.py --indicators volatility
python run_analysis.py --indicators volume
python run_analysis.py --indicators predictive
python run_analysis.py --indicators probability
python run_analysis.py --indicators sentiment
python run_analysis.py --indicators suportresist

# Get detailed info about specific indicator
python run_analysis.py --indicators oscillators rsi
python run_analysis.py --indicators momentum macd
python run_analysis.py --indicators trend ema
```

### Indicator Usage Examples

```bash
# RSI (Relative Strength Index)
python run_analysis.py demo --rule RSI
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI

# MACD (Moving Average Convergence Divergence)
python run_analysis.py demo --rule MACD
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule MACD

# EMA (Exponential Moving Average)
python run_analysis.py demo --rule EMA
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule EMA

# Bollinger Bands
python run_analysis.py demo --rule BB
python run_analysis.py yf -t EURUSD=X --period 3mo --point 0.00001 --rule BB

# ATR (Average True Range)
python run_analysis.py demo --rule ATR
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule ATR

# Stochastic Oscillator
python run_analysis.py demo --rule STOCH
python run_analysis.py yf -t BTC-USD --period 1y --point 0.01 --rule STOCH

# VWAP (Volume Weighted Average Price)
python run_analysis.py demo --rule VWAP
python run_analysis.py binance -t ETHUSDT --interval H1 --point 0.001 --rule VWAP
```

## Testing Examples

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/calculation/
python -m pytest tests/cli/
python -m pytest tests/data/
python -m pytest tests/eda/

# Run specific test files
python -m pytest tests/test_stdio.py
python -m pytest tests/mcp/test_auto_start_mcp.py
python -m pytest tests/calculation/indicators/test_coverage_summary.py

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html
python -m pytest tests/ --cov=src --cov-report=term-missing

# Run tests in parallel
python -m pytest tests/ -n auto

# Run tests with verbose output
python -m pytest tests/ -v

# Run tests and stop on first failure
python -m pytest tests/ -x

# Run tests and show local variables on failure
python -m pytest tests/ -l
```

### Test Coverage Analysis

```bash
# Run coverage analysis
python tests/zzz_analyze_test_coverage.py

# Run tests with coverage report
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# Generate coverage badge
python -m pytest tests/ --cov=src --cov-report=html --cov-branch
```

### Specific Test Examples

```bash
# Test MCP server stdio mode
python tests/test_stdio.py

# Test CLI functionality
python -m pytest tests/cli/test_cli_examples.py -v

# Test indicator calculations
python -m pytest tests/calculation/indicators/ -v

# Test data fetchers
python -m pytest tests/data/fetchers/ -v

# Test export functionality
python -m pytest tests/export/test_export_functionality.py -v

# Test interactive mode
python -m pytest tests/cli/test_interactive_mode.py -v
```

### Debugging Tests

```bash
# Run tests with debug output
python -m pytest tests/ -s -v

# Run specific test with debugger
python -m pytest tests/test_stdio.py::test_stdio_mode -s --pdb

# Run tests and show print statements
python -m pytest tests/ -s

# Run tests with maximum verbosity
python -m pytest tests/ -vvv
```

## MCP Server Examples

### Auto-Start MCP Server

```bash
# Start MCP server automatically
python scripts/auto_start_mcp.py

# Start with specific configuration
python scripts/auto_start_mcp.py --config mcp_auto_config.json

# Start in debug mode
python scripts/auto_start_mcp.py --debug

# Start with custom project path
python scripts/auto_start_mcp.py --project-path /path/to/project

# Show server status
python scripts/auto_start_mcp.py --status

# Stop all servers
python scripts/auto_start_mcp.py --stop
```

### Manual MCP Server Control

```bash
# Start PyCharm GitHub Copilot MCP server
python pycharm_github_copilot_mcp.py

# Start with specific configuration
python pycharm_github_copilot_mcp.py --config mcp_auto_config.json

# Start in stdio mode for testing
python pycharm_github_copilot_mcp.py --stdio

# Start with debug logging
python pycharm_github_copilot_mcp.py --debug
```

### MCP Server Testing

```bash
# Test stdio mode
python tests/test_stdio.py

# Test MCP auto-start functionality
python -m pytest tests/mcp/test_auto_start_mcp.py -v

# Test PyCharm MCP server
python -m pytest tests/mcp/test_pycharm_github_copilot_mcp.py -v

# Test MCP server integration
python scripts/run_cursor_mcp.py --test
```

## Script Usage Examples

### Utility Scripts

```bash
# Initialize project directories
bash scripts/init_dirs.sh

# Fix import statements
python scripts/fix_imports.py

# Analyze requirements
python scripts/analyze_requirements.py

# Create test parquet file
python scripts/create_test_parquet.py

# Recreate CSV from parquet
python scripts/recreate_csv.py

# Run EDA analysis
bash eda

# Run analysis with different backends
python run_analysis.py demo -d fastest
python run_analysis.py demo -d plotly
python run_analysis.py demo -d seaborn
python run_analysis.py demo -d term
```

### Debug Scripts

```bash
# Debug Binance connection
python scripts/debug_scripts/debug_binance_connection.py

# Check parquet files
python scripts/debug_scripts/debug_check_parquet.py

# Debug data processing
python scripts/debug_scripts/debug_data_processing.py

# Debug plotting
python scripts/debug_scripts/debug_plotting.py

# Debug indicators
python scripts/debug_scripts/debug_indicators.py

# Debug CLI
python scripts/debug_scripts/debug_cli.py

# Debug MCP servers
python scripts/debug_scripts/debug_mcp_servers.py
```

## Advanced Usage Examples

### Custom Indicator Development

```python
# Example: Creating a custom indicator
from src.calculation.indicators.base_indicator import BaseIndicator
import pandas as pd
import numpy as np

class CustomIndicator(BaseIndicator):
    """Custom technical indicator example."""
    
    def calculate(self, data: pd.DataFrame, point: float = 0.01) -> pd.DataFrame:
        """Calculate custom indicator."""
        result = data.copy()
        
        # Your custom calculation logic here
        result['custom_signal'] = (
            data['close'].rolling(window=20).mean() - 
            data['close'].rolling(window=50).mean()
        )
        
        return result

# Usage in CLI
# python run_analysis.py demo --rule CustomIndicator
```

### Batch Processing

```bash
# Process multiple symbols
for symbol in AAPL MSFT GOOGL; do
    python run_analysis.py yf -t $symbol --period 1mo --point 0.01 --rule RSI
done

# Process multiple timeframes
for timeframe in D1 H1 M15; do
    python run_analysis.py binance -t BTCUSDT --interval $timeframe --point 0.01 --rule MACD
done

# Process multiple indicators
for indicator in RSI MACD EMA BB; do
    python run_analysis.py demo --rule $indicator --export-parquet
done
```

### Data Pipeline Examples

```bash
# Complete data pipeline: Download → Analyze → Export
# 1. Download data
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 2. Analyze with multiple indicators
python run_analysis.py show yf AAPL --rule RSI --export-parquet
python run_analysis.py show yf AAPL --rule MACD --export-parquet
python run_analysis.py show yf AAPL --rule EMA --export-parquet

# 3. View results
python run_analysis.py show ind parquet
```

### Performance Optimization

```bash
# Use fastest plotting backend for large datasets
python run_analysis.py csv --csv-file large_data.csv --point 0.01 -d fastest

# Use terminal backend for SSH/Docker environments
python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 -d term

# Use specific rules for faster processing
python run_analysis.py demo --rule OHLCV  # Candlestick only
python run_analysis.py demo --rule AUTO   # Auto-detect columns
```

## Troubleshooting Examples

### Common Issues and Solutions

```bash
# Issue: Missing dependencies
pip install -r requirements.txt
# or
uv sync

# Issue: Cache problems
rm -rf data/cache/*
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --force-refresh

# Issue: Permission errors
chmod +x scripts/*.sh
chmod +x nz
chmod +x eda

# Issue: Docker problems
docker compose down
docker compose build --no-cache
docker compose up -d

# Issue: Test failures
python -m pytest tests/ --tb=short
python -m pytest tests/ -x --pdb

# Issue: MCP server not starting
python scripts/auto_start_mcp.py --stop
python scripts/auto_start_mcp.py --debug
```

### Debug Mode Examples

```bash
# Enable debug logging
export DEBUG=1
python run_analysis.py demo

# Run with verbose output
python run_analysis.py demo -v

# Check system information
python -c "import sys; print(sys.version)"
python -c "import pandas; print(pandas.__version__)"

# Test specific components
python -c "from src.calculation.indicators.oscillators.rsi_ind_calc import RSI; print('RSI OK')"
python -c "from src.data.fetchers.binance_fetcher import BinanceFetcher; print('Binance OK')"
```

## Integration Examples

### CI/CD Pipeline

```yaml
# Example GitHub Actions workflow
name: Test and Deploy
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: |
          python -m pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Docker Integration

```dockerfile
# Example Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv sync

EXPOSE 8000
CMD ["python", "run_analysis.py", "demo"]
```

### API Integration

```python
# Example: Using the analysis tool as a library
from src.calculation.indicator_calculation import IndicatorCalculation
from src.data.data_acquisition import DataAcquisition

# Initialize components
data_acq = DataAcquisition()
indicator_calc = IndicatorCalculation()

# Load data
data = data_acq.load_yfinance_data("AAPL", "1mo", 0.01)

# Calculate indicators
indicators = indicator_calc.calculate_indicators(data, "RSI")

# Export results
indicator_calc.export_indicators(indicators, "parquet")
```

## Quick Start Workflow

### For New Users

1. **Install and Setup**
   ```bash
   git clone <repository>
   cd neozork-hld-prediction
   pip install uv && uv sync
   ```

2. **Discover Indicators**
   ```bash
   python run_analysis.py --indicators
   ```

3. **Try Interactive Mode**
   ```bash
   python run_analysis.py interactive
   ```

4. **Run Demo Analysis**
   ```bash
   python run_analysis.py demo --rule RSI
   ```

5. **Download Real Data**
   ```bash
   python run_analysis.py yf -t AAPL --period 1mo --point 0.01
   ```

6. **Analyze Downloaded Data**
   ```bash
   python run_analysis.py show yf AAPL --rule RSI
   ```

### For Advanced Users

1. **Setup MCP Servers**
   ```bash
   python scripts/auto_start_mcp.py
   ```

2. **Run Comprehensive Tests**
   ```bash
   python -m pytest tests/ --cov=src --cov-report=html
   ```

3. **Analyze Test Coverage**
   ```bash
   python tests/zzz_analyze_test_coverage.py
   ```

4. **Custom Development**
   ```bash
   # Create custom indicator
   # Test custom indicator
   python -m pytest tests/calculation/indicators/ -v
   ```

5. **Performance Testing**
   ```bash
   python run_analysis.py demo --rule AUTO -d fastest
   ```

## Environment-Specific Examples

### SSH/Docker Environment

```bash
# Use terminal plotting backend
python run_analysis.py demo -d term
python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 -d term

# Use Docker container
docker compose run --rm neozork-hld python run_analysis.py demo -d term
```

### Local Development

```bash
# Use interactive plotting backends
python run_analysis.py demo -d plotly
python run_analysis.py demo -d seaborn

# Enable debug mode
export DEBUG=1
python run_analysis.py demo
```

### Production Environment

```bash
# Use fastest backend for performance
python run_analysis.py demo -d fastest

# Use specific rules for efficiency
python run_analysis.py demo --rule OHLCV

# Enable logging
python run_analysis.py demo --log-level INFO
```

---

For more detailed information, see:
- [Getting Started](getting-started.md)
- [Project Structure](project-structure.md)
- [Testing Guide](testing.md)
- [MCP Servers Setup](mcp-servers/SETUP.md)
- [Scripts Documentation](scripts.md)