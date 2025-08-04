# Technical Indicator Examples

Comprehensive examples for all available technical indicators.

## Overview

The project supports multiple categories of technical indicators:

- **Trend Indicators** - EMA, ADX, SAR
- **Oscillators** - RSI, Stochastic, CCI
- **Momentum Indicators** - MACD, Stochastic Oscillator
- **Volatility Indicators** - ATR, Bollinger Bands, Standard Deviation
- **Volume Indicators** - OBV, VWAP
- **Support/Resistance** - Donchian Channels, Fibonacci, Pivot Points
- **Predictive Indicators** - HMA, Time Series Forecast
- **Probability Indicators** - Kelly Criterion, Monte Carlo
- **Sentiment Indicators** - COT, Fear & Greed, Social Sentiment

## Trend Indicators

### EMA (Exponential Moving Average)
```bash
# Basic EMA
python run_analysis.py demo --rule EMA

# EMA with custom period
python run_analysis.py demo --rule EMA --ema-period 20

# EMA with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule EMA
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule EMA
```

### ADX (Average Directional Index)
```bash
# Basic ADX
python run_analysis.py demo --rule ADX

# ADX with custom period
python run_analysis.py demo --rule ADX --adx-period 14

# ADX with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule ADX
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule ADX
```

### SAR (Parabolic SAR)
```bash
# Basic SAR
python run_analysis.py demo --rule SAR

# SAR with custom parameters
python run_analysis.py demo --rule SAR --sar-acceleration 0.02 --sar-maximum 0.2

# SAR with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule SAR
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule SAR
```

## Oscillators

### RSI (Relative Strength Index)
```bash
# Basic RSI
python run_analysis.py demo --rule RSI

# RSI with custom period
python run_analysis.py demo --rule RSI --rsi-period 21

# RSI with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule RSI
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule RSI
```

### Stochastic Oscillator
```bash
# Basic Stochastic
python run_analysis.py demo --rule STOCH

# Stochastic with custom parameters
python run_analysis.py demo --rule STOCH --stoch-k-period 14 --stoch-d-period 3

# Stochastic with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule STOCH
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule STOCH
```

### CCI (Commodity Channel Index)
```bash
# Basic CCI
python run_analysis.py demo --rule CCI

# CCI with custom period
python run_analysis.py demo --rule CCI --cci-period 20

# CCI with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule CCI
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule CCI
```

## Momentum Indicators

### MACD (Moving Average Convergence Divergence)
```bash
# Basic MACD
python run_analysis.py demo --rule MACD

# MACD with custom parameters
python run_analysis.py demo --rule MACD --macd-fast 8 --macd-slow 21 --macd-signal 5

# MACD with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule MACD
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule MACD
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule MACD
```

## Volatility Indicators

### ATR (Average True Range)
```bash
# Basic ATR
python run_analysis.py demo --rule ATR

# ATR with custom period
python run_analysis.py demo --rule ATR --atr-period 14

# ATR with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule ATR
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule ATR
```

### Bollinger Bands
```bash
# Basic Bollinger Bands
python run_analysis.py demo --rule BB

# Bollinger Bands with custom parameters
python run_analysis.py demo --rule BB --bb-period 20 --bb-std 2

# Bollinger Bands with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule BB
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule BB
```

### Standard Deviation
```bash
# Basic Standard Deviation
python run_analysis.py demo --rule STD

# Standard Deviation with custom period
python run_analysis.py demo --rule STD --std-period 20

# Standard Deviation with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule STD
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule STD
```

## Volume Indicators

### OBV (On-Balance Volume)
```bash
# Basic OBV
python run_analysis.py demo --rule OBV

# OBV with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule OBV
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule OBV
```

### VWAP (Volume Weighted Average Price)
```bash
# Basic VWAP
python run_analysis.py demo --rule VWAP

# VWAP with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule VWAP
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule VWAP
```

## Support/Resistance Indicators

### Donchian Channels
```bash
# Basic Donchian Channels
python run_analysis.py demo --rule DONCH

# Donchian Channels with custom period
python run_analysis.py demo --rule DONCH --donch-period 20

# Donchian Channels with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule DONCH
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule DONCH
```

### Fibonacci Retracements
```bash
# Basic Fibonacci Retracements
python run_analysis.py demo --rule FIB

# Fibonacci with custom levels
python run_analysis.py demo --rule FIB --fib-levels 0.236,0.382,0.5,0.618,0.786

# Fibonacci with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule FIB
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule FIB
```

### Pivot Points
```bash
# Basic Pivot Points
python run_analysis.py demo --rule PIVOT

# Pivot Points with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule PIVOT
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule PIVOT
```

## Predictive Indicators

### HMA (Hull Moving Average)
```bash
# Basic HMA
python run_analysis.py demo --rule HMA

# HMA with custom period
python run_analysis.py demo --rule HMA --hma-period 20

# HMA with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule HMA
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule HMA
```

### Time Series Forecast
```bash
# Basic Time Series Forecast
python run_analysis.py demo --rule TSF

# TSF with custom parameters
python run_analysis.py demo --rule TSF --tsf-period 20 --tsf-forecast 5

# TSF with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule TSF
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule TSF
```

## Probability Indicators

### Kelly Criterion
```bash
# Basic Kelly Criterion
python run_analysis.py demo --rule KELLY

# Kelly with custom parameters
python run_analysis.py demo --rule KELLY --kelly-period 20

# Kelly with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule KELLY
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule KELLY
```

### Monte Carlo Simulation
```bash
# Basic Monte Carlo
python run_analysis.py demo --rule MONTE

# Monte Carlo with custom parameters
python run_analysis.py demo --rule MONTE --monte-simulations 1000 --monte-period 252

# Monte Carlo with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule MONTE
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule MONTE
```

## Sentiment Indicators

### Commitment of Traders (COT)
```bash
# Basic COT
python run_analysis.py demo --rule COT

# COT with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule COT
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule COT
```

### Fear & Greed Index
```bash
# Basic Fear & Greed Index
python run_analysis.py demo --rule FNG

# FNG with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule FNG
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule FNG
```

### Social Sentiment
```bash
# Basic Social Sentiment
python run_analysis.py demo --rule SENT

# Social Sentiment with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule SENT
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule SENT
```

## Multiple Indicators

### Combining Multiple Indicators
```bash
# Multiple indicators in one command
python run_analysis.py demo --rule RSI,MACD,EMA

# Multiple indicators with custom parameters
python run_analysis.py demo --rule RSI,MACD,EMA --rsi-period 21 --macd-fast 8 --ema-period 20

# Multiple indicators with different data sources
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI,MACD,EMA
```

### Comparing Indicators
```bash
# Compare different indicators
python run_analysis.py demo --rule RSI --rule MACD --rule EMA

# Compare with custom parameters
python run_analysis.py demo --rule RSI --rsi-period 21 --rule MACD --macd-fast 8
```

## Export and Visualization

### Exporting Indicator Results
```bash
# Export to multiple formats
python run_analysis.py demo --rule RSI --export-parquet --export-csv --export-json

# Export with custom filenames
python run_analysis.py demo --rule RSI --export-parquet --output rsi_results.parquet

# Export multiple indicators
python run_analysis.py demo --rule RSI,MACD,EMA --export-parquet
```

### Different Visualization Backends
```bash
# Interactive plots with Plotly
python run_analysis.py demo --rule RSI -d plotly

# Static plots with Seaborn
python run_analysis.py demo --rule RSI -d seaborn

# Terminal plots for SSH/Docker
python run_analysis.py demo --rule RSI -d term

# Fastest backend for large datasets
python run_analysis.py demo --rule RSI -d fastest
```

## Advanced Usage

### Custom Indicator Parameters
```bash
# RSI with custom period and overbought/oversold levels
python run_analysis.py demo --rule RSI --rsi-period 21 --rsi-overbought 70 --rsi-oversold 30

# MACD with custom parameters
python run_analysis.py demo --rule MACD --macd-fast 8 --macd-slow 21 --macd-signal 5

# Bollinger Bands with custom parameters
python run_analysis.py demo --rule BB --bb-period 20 --bb-std 2
```

### Data Filtering with Indicators
```bash
# Filter data by date range and apply indicator
python run_analysis.py yf -t AAPL --period 1y --point 0.01 --start-date 2024-01-01 --end-date 2024-06-30 --rule RSI

# Filter by volume and apply indicator
python run_analysis.py yf -t AAPL --period 1y --point 0.01 --min-volume 1000000 --rule MACD
```

### Performance Optimization
```bash
# Use fastest backend for large datasets
python run_analysis.py yf -t AAPL --period 5y --point 0.01 --rule RSI -d fastest

# Use terminal backend for SSH/Docker
python run_analysis.py yf -t AAPL --period 1y --point 0.01 --rule RSI -d term
```

## Testing Indicators

### Testing Specific Indicators
```bash
# Test RSI calculations
python -m pytest tests/calculation/indicators/oscillators/test_rsi_ind_calc.py -v

# Test MACD calculations
python -m pytest tests/calculation/indicators/momentum/test_macd_indicator.py -v

# Test EMA calculations
python -m pytest tests/calculation/indicators/trend/test_ema_indicator.py -v
```

### Testing All Indicators
```bash
# Test all indicators
python -m pytest tests/calculation/indicators/ -v

# Test with coverage
python -m pytest tests/calculation/indicators/ --cov=src.calculation.indicators --cov-report=html
```

## Troubleshooting

### Common Indicator Issues
```bash
# Check indicator calculations
python scripts/debug_scripts/debug_indicators.py

# Check data quality for indicators
python scripts/debug_scripts/debug_check_parquet.py

# Test specific indicator
python -c "from src.calculation.indicators.oscillators.rsi_ind_calc import RSI; print('RSI OK')"
```

### Performance Issues
```bash
# Use fastest backend for large datasets
python run_analysis.py demo --rule RSI -d fastest

# Use smaller timeframes
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI

# Export results to free memory
python run_analysis.py demo --rule RSI --export-parquet
```

---

📚 **Additional Resources:**
- **[Usage Examples](usage-examples.md)** - Comprehensive usage examples
- **[Quick Examples](quick-examples.md)** - Fast start examples
- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Testing Examples](testing-examples.md)** - Testing examples
- **[Script Examples](script-examples.md)** - Utility script examples
- **[Docker Examples](docker-examples.md)** - Docker examples
- **[EDA Examples](eda-examples.md)** - EDA examples 