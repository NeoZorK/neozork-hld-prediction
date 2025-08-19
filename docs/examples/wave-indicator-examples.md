# Wave Indicator Examples

## Overview

This document provides practical examples of using the Wave indicator in the neozork-hld-prediction platform. The Wave indicator is a complex trend analysis tool that combines multiple components to identify wave patterns and generate trading signals.

## Basic Usage Examples

### Example 1: Default Parameters

```bash
# Use Wave indicator with default parameters
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,close
```

**Parameters Explained:**
- `339`: First long period
- `10`: First fast period  
- `2`: First trend period
- `fast`: First trend type
- `22`: Second long period
- `11`: Second fast period
- `4`: Second trend period
- `fast`: Second trend type
- `prime`: Global trend type
- `22`: SMA period for global trend
- `close`: Price type for calculation

### Example 2: Custom Parameters for Short-term Analysis

```bash
# Use Wave indicator for short-term analysis
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:50,5,10,slow,20,3,7,fast,secondary,15,open
```

**Parameters Explained:**
- `50`: Shorter first long period for faster response
- `5`: Very short first fast period
- `10`: Medium first trend period
- `slow`: First trend type for smoother signals
- `20`: Shorter second long period
- `3`: Very short second fast period
- `7`: Medium second trend period
- `fast`: Second trend type for responsiveness
- `secondary`: Global trend type for medium-term analysis
- `15`: Shorter SMA period
- `open`: Use Open prices instead of Close

### Example 3: Long-term Trend Analysis

```bash
# Use Wave indicator for long-term trend analysis
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:500,20,50,slow,100,15,30,slow,tertiary,50,close
```

**Parameters Explained:**
- `500`: Very long first period for major trends
- `20`: Longer fast period
- `50`: Long trend period
- `slow`: Slow trend type for stability
- `100`: Long second period
- `15`: Medium fast period
- `30`: Long trend period
- `slow`: Slow trend type
- `tertiary`: Global trend type for long-term analysis
- `50`: Long SMA period
- `close`: Use Close prices

## Real-World Scenarios

### Scenario 1: Stock Market Analysis (AAPL)

```bash
# Analyze Apple stock with Wave indicator
uv run python -m src.cli.cli --mode yfinance --ticker AAPL --period 1y --rule wave:200,10,20,fast,50,5,10,fast,prime,30,close --plot
```

**Use Case:** Identify medium-term trend changes in Apple stock with responsive signals.

### Scenario 2: Cryptocurrency Analysis (Bitcoin)

```bash
# Analyze Bitcoin with Wave indicator
uv run python -m src.cli.cli --mode binance --ticker BTCUSDT --start 2023-01-01 --end 2024-01-01 --point 0.1 --rule wave:300,15,30,medium,75,8,15,fast,secondary,25,close --plot
```

**Use Case:** Detect wave patterns in Bitcoin price movements with balanced responsiveness.

### Scenario 3: Forex Analysis (EUR/USD)

```bash
# Analyze EUR/USD with Wave indicator
uv run python -m src.cli.cli --mode csv --csv-file data/forex_data.csv --point 0.0001 --rule wave:150,8,15,fast,40,4,8,fast,prime,20,open --plot
```

**Use Case:** Short-term forex trading with quick signal generation.

## Parameter Optimization Examples

### Conservative Trading Strategy

```bash
# Conservative approach with longer periods and slow trends
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:400,25,50,slow,100,15,30,slow,tertiary,40,close
```

**Strategy:** Fewer but more reliable signals, suitable for position trading.

### Aggressive Trading Strategy

```bash
# Aggressive approach with shorter periods and fast trends
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:100,5,10,fast,25,3,5,fast,prime,15,close
```

**Strategy:** More frequent signals, suitable for day trading.

### Balanced Trading Strategy

```bash
# Balanced approach with mixed trend types
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:250,12,25,medium,60,6,12,fast,secondary,25,close
```

**Strategy:** Moderate signal frequency with good risk-reward balance.

## Advanced Usage Examples

### Example 1: Multiple Timeframe Analysis

```bash
# Compare different timeframes
# Daily analysis
uv run python -m src.cli.cli --mode csv --csv-file data/daily_data.csv --point 0.01 --rule wave:200,10,20,fast,50,5,10,fast,prime,25,close --plot

# Weekly analysis  
uv run python -m src.cli.cli --mode csv --csv-file data/weekly_data.csv --point 0.01 --rule wave:100,5,10,fast,25,3,5,fast,prime,12,close --plot
```

### Example 2: Different Market Conditions

```bash
# Bull market conditions - more responsive
uv run python -m src.cli.cli --mode csv --csv-file data/bull_market_data.csv --point 0.01 --rule wave:150,8,15,fast,40,4,8,fast,prime,20,close

# Bear market conditions - more conservative
uv run python -m src.cli.cli --mode csv --csv-file data/bear_market_data.csv --point 0.01 --rule wave:300,20,40,slow,75,10,20,slow,secondary,35,close
```

### Example 3: Sector-Specific Analysis

```bash
# Technology sector - fast-moving
uv run python -m src.cli.cli --mode csv --csv-file data/tech_sector_data.csv --point 0.01 --rule wave:120,6,12,fast,30,3,6,fast,prime,18,close

# Utility sector - slow-moving
uv run python -m src.cli.cli --mode csv --csv-file data/utility_sector_data.csv --point 0.01 --rule wave:400,25,50,slow,100,15,30,slow,tertiary,40,close
```

## Parameter Guidelines

### Trend Type Selection

| Trend Type | Use Case | Characteristics |
|------------|----------|-----------------|
| `fast` | Day trading, volatile markets | Quick signals, more noise |
| `medium` | Swing trading, balanced approach | Moderate responsiveness |
| `slow` | Position trading, stable markets | Fewer signals, more reliable |

### Global Trend Type Selection

| Global Trend Type | Use Case | Characteristics |
|-------------------|----------|-----------------|
| `prime` | Short to medium-term analysis | Standard responsiveness |
| `secondary` | Medium-term analysis | Moderate smoothing |
| `tertiary` | Long-term analysis | Maximum smoothing |

### Period Selection Guidelines

| Market Type | Long Period | Fast Period | Trend Period | SMA Period |
|-------------|-------------|-------------|--------------|------------|
| Day Trading | 50-100 | 3-8 | 5-15 | 10-20 |
| Swing Trading | 100-250 | 8-15 | 15-30 | 20-35 |
| Position Trading | 250-500 | 15-25 | 30-60 | 35-60 |

## Troubleshooting Examples

### Example 1: Insufficient Data Error

```bash
# Error: Not enough data for Wave calculation
# Solution: Use shorter periods or get more data
uv run python -m src.cli.cli --mode csv --csv-file data/short_data.csv --point 0.01 --rule wave:50,5,10,fast,20,3,5,fast,prime,15,close
```

### Example 2: Invalid Parameter Error

```bash
# Error: Invalid trend type parameter
# Solution: Use valid trend types (fast, slow, medium)
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:200,10,20,fast,50,5,10,fast,prime,25,close
```

### Example 3: Performance Optimization

```bash
# For large datasets, use longer periods to improve performance
uv run python -m src.cli.cli --mode csv --csv-file data/large_dataset.csv --point 0.01 --rule wave:300,20,40,slow,75,10,20,slow,secondary,35,close
```

## Best Practices

1. **Start with Default Parameters**: Begin with default parameters and adjust based on results
2. **Test Different Combinations**: Experiment with different trend type combinations
3. **Consider Market Conditions**: Adjust parameters based on market volatility
4. **Use Multiple Timeframes**: Combine different timeframes for confirmation
5. **Validate with Historical Data**: Test parameters on historical data before live trading
6. **Monitor Performance**: Track signal accuracy and adjust parameters accordingly

## Summary

The Wave indicator provides a powerful tool for trend analysis with multiple parameter options. By understanding the relationship between parameters and market conditions, you can optimize the indicator for your specific trading strategy and market environment.
