# SMA Indicator Quick Start Guide

## Quick Overview

The **SMA (Simple Moving Average)** indicator is fully implemented across all display modes in the neozork-hld-prediction platform. This guide shows you how to use SMA quickly and effectively.

## Basic Usage

### 1. Demo Mode (Recommended for Testing)

```bash
# Basic SMA with default settings
uv run run_analysis.py demo --rule sma:20,close -d fastest

# Custom period
uv run run_analysis.py demo --rule sma:50,close -d plotly

# Different price type
uv run run_analysis.py demo --rule sma:20,open -d mpl
```

### 2. Real Data Analysis

```bash
# Stock analysis
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest

# Cryptocurrency analysis
uv run run_analysis.py yfinance --ticker BTC-USD --period 6mo --point 0.01 --rule sma:50,close -d plotly

# Forex analysis
uv run run_analysis.py yfinance --ticker EURUSD=X --period 1y --point 0.00001 --rule sma:20,close -d mpl
```

## Display Modes

| Mode | Command | Best For |
|------|---------|----------|
| `fastest` | `-d fastest` | Large datasets, best performance |
| `fast` | `-d fast` | Quick visualization |
| `plotly` | `-d plotly` | Interactive analysis |
| `mpl` | `-d mpl` | Professional charts |
| `seaborn` | `-d seaborn` | Statistical analysis |
| `term` | `-d term` | Terminal/SSH |

## Parameter Format

```
sma:period,price_type
```

### Parameters
- **period**: SMA calculation period (default: 20)
- **price_type**: Price type (open/close, default: close)

### Examples

```bash
# Standard 20-period SMA with close prices
uv run run_analysis.py demo --rule sma:20,close -d fastest

# Long-term 50-period SMA with open prices
uv run run_analysis.py demo --rule sma:50,open -d plotly

# Short-term 10-period SMA for day trading
uv run run_analysis.py demo --rule sma:10,close -d mpl

# Multiple SMAs for comparison
uv run run_analysis.py demo --rule sma:20,close,sma:50,close -d fastest
```

## Getting Help

```bash
# General help
uv run run_analysis.py --help

# SMA-specific help
uv run run_analysis.py demo --rule sma --help

# Show mode help
uv run run_analysis.py show --help
```

## Testing All Modes

```bash
# Test SMA across all display modes
for mode in fastest fast plotly mpl seaborn term; do
    echo "Testing $mode mode..."
    uv run run_analysis.py demo --rule sma:20,close -d $mode
done
```

## Common Use Cases

### 1. Trend Analysis
```bash
# Long-term trend with 50-period SMA
uv run run_analysis.py yfinance --ticker AAPL --period 2y --point 0.01 --rule sma:50,close -d plotly
```

### 2. Day Trading
```bash
# Short-term signals with 10-period SMA
uv run run_analysis.py yfinance --ticker BTC-USD --period 1mo --point 0.01 --rule sma:10,close -d fastest
```

### 3. Multiple Timeframes
```bash
# Compare different periods
uv run run_analysis.py demo --rule sma:10,close,sma:20,close,sma:50,close -d plotly
```

## Troubleshooting

### Common Errors

1. **"Invalid SMA parameters"**
   ```bash
   # Correct format
   uv run run_analysis.py demo --rule sma:20,close -d fastest
   
   # Wrong format
   uv run run_analysis.py demo --rule sma:20 -d fastest  # Missing price_type
   ```

2. **"No SMA columns found"**
   - Check if indicator calculation completed successfully
   - Verify data format and availability

3. **Performance issues**
   - Use `fastest` mode for large datasets
   - Consider reducing data period

### Debug Commands

```bash
# Debug mode
uv run run_analysis.py demo --rule sma:20,close -d term --debug

# Verbose output
uv run run_analysis.py demo --rule sma:20,close -d fastest --verbose

# Check data structure
uv run run_analysis.py show data/your_file.parquet
```

## Advanced Features

### 1. Multiple Indicators
```bash
# SMA + RSI
uv run run_analysis.py demo --rule sma:20,close,rsi:14 -d plotly

# SMA + MACD
uv run run_analysis.py demo --rule sma:20,close,macd:12,26,9 -d fastest
```

### 2. Export Results
```bash
# Export to different formats
uv run run_analysis.py demo --rule sma:20,close -d fastest --export-parquet
uv run run_analysis.py demo --rule sma:20,close -d fastest --export-csv
uv run run_analysis.py demo --rule sma:20,close -d fastest --export-json
```

### 3. Date Filtering
```bash
# Filter by date range
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d plotly --start 2023-01-01 --end 2023-12-31
```

## Best Practices

1. **Start with demo mode** to test your setup
2. **Use appropriate periods**:
   - 10-20 for short-term trading
   - 20-50 for medium-term analysis
   - 50+ for long-term trends
3. **Choose the right display mode** for your use case
4. **Test with real data** after demo mode
5. **Use multiple timeframes** for comprehensive analysis

## Next Steps

- Read the [Complete SMA Tutorial](adding-sma-indicator-tutorial.md)
- Explore other indicators (RSI, MACD, EMA)
- Learn about [Custom Indicator Development](adding-custom-indicators.md)
- Check the [CLI Interface Guide](cli-interface.md)

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the complete tutorial
- Run tests: `uv run pytest tests/ -k "sma" -v`
- Check logs in the `logs/` directory
