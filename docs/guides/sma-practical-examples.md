# SMA Indicator Practical Examples

## Overview

This guide provides practical examples of using the SMA (Simple Moving Average) indicator across all display modes with real-world scenarios.

## Example 1: Basic SMA Analysis

### Scenario: Stock Market Trend Analysis

**Goal**: Analyze Apple stock trend using 20-period SMA

```bash
# Basic analysis with fastest mode
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest

# Same analysis with interactive plotly
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d plotly

# Professional chart with mplfinance
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d mpl
```

**What to look for:**
- Price crossing above/below SMA line
- SMA slope direction (trend strength)
- Support/resistance levels near SMA

## Example 2: Multiple Timeframe Analysis

### Scenario: Cryptocurrency Trading Strategy

**Goal**: Compare short-term and long-term trends for Bitcoin

```bash
# Multiple SMAs for trend comparison
uv run run_analysis.py yfinance --ticker BTC-USD --period 6mo --point 0.01 --rule sma:10,close,sma:20,close,sma:50,close -d plotly

# Focus on short-term signals
uv run run_analysis.py yfinance --ticker BTC-USD --period 1mo --point 0.01 --rule sma:5,close,sma:10,close -d fastest

# Long-term trend analysis
uv run run_analysis.py yfinance --ticker BTC-USD --period 2y --point 0.01 --rule sma:50,close,sma:200,close -d mpl
```

**Trading signals:**
- **Golden Cross**: 10-period SMA crosses above 20-period SMA (bullish)
- **Death Cross**: 10-period SMA crosses below 20-period SMA (bearish)
- **Trend Strength**: All SMAs aligned in same direction

## Example 3: Day Trading Setup

### Scenario: Intraday Trading with SMA

**Goal**: Use SMA for day trading signals

```bash
# Short-term SMA for day trading
uv run run_analysis.py yfinance --ticker TSLA --period 1mo --point 0.01 --rule sma:5,close -d fastest

# Multiple short-term periods
uv run run_analysis.py yfinance --ticker TSLA --period 1mo --point 0.01 --rule sma:5,close,sma:10,close -d plotly

# With volume confirmation
uv run run_analysis.py yfinance --ticker TSLA --period 1mo --point 0.01 --rule sma:5,close,obv -d mpl
```

**Day trading strategy:**
- Use 5-10 period SMA for quick signals
- Look for price bounces off SMA
- Confirm with volume and other indicators

## Example 4: Forex Analysis

### Scenario: Currency Pair Trend Analysis

**Goal**: Analyze EUR/USD trend using SMA

```bash
# Standard forex analysis
uv run run_analysis.py yfinance --ticker EURUSD=X --period 1y --point 0.00001 --rule sma:20,close -d plotly

# Multiple timeframes for forex
uv run run_analysis.py yfinance --ticker EURUSD=X --period 1y --point 0.00001 --rule sma:20,close,sma:50,close -d fastest

# Short-term forex signals
uv run run_analysis.py yfinance --ticker EURUSD=X --period 1mo --point 0.00001 --rule sma:10,close -d mpl
```

**Forex considerations:**
- Use appropriate point size (0.00001 for major pairs)
- Consider different timeframes for entry/exit
- Watch for trend reversals at SMA levels

## Example 5: Portfolio Analysis

### Scenario: Multi-Asset Portfolio

**Goal**: Analyze multiple assets with SMA

```bash
# Analyze multiple stocks
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest
uv run run_analysis.py yfinance --ticker GOOGL --period 1y --point 0.01 --rule sma:20,close -d fastest
uv run run_analysis.py yfinance --ticker MSFT --period 1y --point 0.01 --rule sma:20,close -d fastest

# Compare different asset classes
uv run run_analysis.py yfinance --ticker SPY --period 1y --point 0.01 --rule sma:20,close -d plotly  # S&P 500 ETF
uv run run_analysis.py yfinance --ticker GLD --period 1y --point 0.01 --rule sma:20,close -d plotly  # Gold ETF
uv run run_analysis.py yfinance --ticker TLT --period 1y --point 0.01 --rule sma:20,close -d plotly  # Bonds ETF
```

## Example 6: Technical Analysis Combinations

### Scenario: SMA with Other Indicators

**Goal**: Combine SMA with complementary indicators

```bash
# SMA + RSI for trend and momentum
uv run run_analysis.py demo --rule sma:20,close,rsi:14 -d plotly

# SMA + MACD for trend confirmation
uv run run_analysis.py demo --rule sma:20,close,macd:12,26,9 -d fastest

# SMA + Bollinger Bands for volatility
uv run run_analysis.py demo --rule sma:20,close,bb:20,2 -d mpl

# SMA + Volume for confirmation
uv run run_analysis.py demo --rule sma:20,close,obv -d seaborn
```

## Example 7: Different Display Modes Comparison

### Scenario: Choose the Right Visualization

**Goal**: Compare different display modes for the same analysis

```bash
# 1. Fastest mode - Best performance
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest

# 2. Plotly mode - Interactive analysis
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d plotly

# 3. MPL mode - Professional charts
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d mpl

# 4. Seaborn mode - Statistical focus
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d seaborn

# 5. Terminal mode - Server/SSH access
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d term
```

## Example 8: Data Export and Analysis

### Scenario: Export Results for Further Analysis

**Goal**: Export SMA calculations for external analysis

```bash
# Export to Parquet format
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest --export-parquet

# Export to CSV format
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest --export-csv

# Export to JSON format
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest --export-json

# View exported data
uv run run_analysis.py show data/indicators/parquet/ --keywords AAPL
```

## Example 9: Custom Date Ranges

### Scenario: Specific Time Period Analysis

**Goal**: Analyze specific market events or time periods

```bash
# COVID-19 period analysis
uv run run_analysis.py yfinance --ticker SPY --start 2020-01-01 --end 2020-12-31 --point 0.01 --rule sma:20,close -d plotly

# Recent market analysis
uv run run_analysis.py yfinance --ticker AAPL --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule sma:20,close -d fastest

# Earnings season analysis
uv run run_analysis.py yfinance --ticker TSLA --start 2023-10-01 --end 2023-11-30 --point 0.01 --rule sma:10,close -d mpl
```

## Example 10: Demo Mode Testing

### Scenario: Test SMA with Demo Data

**Goal**: Test SMA functionality before using real data

```bash
# Basic demo test
uv run run_analysis.py demo --rule sma:20,close -d fastest

# Test different periods
uv run run_analysis.py demo --rule sma:10,close,sma:20,close,sma:50,close -d plotly

# Test with open prices
uv run run_analysis.py demo --rule sma:20,open -d mpl

# Test multiple indicators
uv run run_analysis.py demo --rule sma:20,close,rsi:14,macd:12,26,9 -d seaborn
```

## Example 11: Performance Comparison

### Scenario: Compare Different SMA Periods

**Goal**: Find optimal SMA period for specific asset

```bash
# Test multiple periods
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:5,close,sma:10,close,sma:20,close,sma:50,close -d plotly

# Focus on short periods
uv run run_analysis.py yfinance --ticker AAPL --period 6mo --point 0.01 --rule sma:5,close,sma:10,close,sma:15,close -d fastest

# Focus on long periods
uv run run_analysis.py yfinance --ticker AAPL --period 2y --point 0.01 --rule sma:50,close,sma:100,close,sma:200,close -d mpl
```

## Example 12: Market Conditions Analysis

### Scenario: Analyze Different Market Conditions

**Goal**: Understand SMA behavior in different markets

```bash
# Bull market analysis
uv run run_analysis.py yfinance --ticker SPY --start 2020-03-23 --end 2021-12-31 --point 0.01 --rule sma:20,close -d plotly

# Bear market analysis
uv run run_analysis.py yfinance --ticker SPY --start 2022-01-01 --end 2022-10-31 --point 0.01 --rule sma:20,close -d fastest

# Sideways market analysis
uv run run_analysis.py yfinance --ticker SPY --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule sma:20,close -d mpl
```

## Best Practices Summary

### 1. Period Selection
- **5-10 periods**: Day trading, scalping
- **10-20 periods**: Short-term trading
- **20-50 periods**: Medium-term analysis
- **50+ periods**: Long-term trend analysis

### 2. Price Type Selection
- **Close prices**: Most common, less noise
- **Open prices**: More volatile, earlier signals

### 3. Display Mode Selection
- **fastest**: Large datasets, best performance
- **plotly**: Interactive analysis, detailed inspection
- **mpl**: Professional charts, publication quality
- **seaborn**: Statistical analysis, research
- **term**: Server environments, quick checks

### 4. Confirmation Strategies
- Use multiple timeframes
- Combine with other indicators
- Consider volume confirmation
- Watch for trend reversals

## Troubleshooting Examples

### Problem: "Invalid SMA parameters"
```bash
# Wrong: Missing price_type
uv run run_analysis.py demo --rule sma:20 -d fastest

# Correct: Include price_type
uv run run_analysis.py demo --rule sma:20,close -d fastest
```

### Problem: "No SMA columns found"
```bash
# Check if calculation completed
uv run run_analysis.py show data/indicators/parquet/ --keywords SMA

# Recalculate with verbose output
uv run run_analysis.py demo --rule sma:20,close -d fastest --verbose
```

### Problem: Performance issues
```bash
# Use fastest mode for large datasets
uv run run_analysis.py yfinance --ticker SPY --period 5y --point 0.01 --rule sma:20,close -d fastest

# Reduce data period
uv run run_analysis.py yfinance --ticker SPY --period 1y --point 0.01 --rule sma:20,close -d plotly
```

## Next Steps

1. **Practice with demo mode** to understand SMA behavior
2. **Test with real data** using different assets
3. **Combine with other indicators** for confirmation
4. **Develop your own strategies** based on SMA signals
5. **Explore advanced features** like custom date ranges and exports

For more detailed information, see:
- [Complete SMA Tutorial](adding-sma-indicator-tutorial.md)
- [Quick Start Guide](sma-quick-start-guide.md)
- [CLI Interface Guide](cli-interface.md)
