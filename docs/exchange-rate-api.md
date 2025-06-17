# Exchange Rate API Data Source

This document describes the Exchange Rate API data source integration for the Shcherbyna Pressure Vector Indicator Analysis Tool.

## Overview

The Exchange Rate API (exchangerate-api.com) data source provides access to historical foreign exchange rates for currency pairs. This integration allows you to fetch and analyze exchange rate data for various currency pairs using the tool's indicator calculation and visualization capabilities.

## Features

- **Free tier**: 1,500 API requests per month (50 per day)
- **160+ currency symbols** supported  
- **Current exchange rates** (historical data requires paid plan)
- **Automatic caching** to minimize API requests
- **Rate limiting** to respect API limits

**Note**: The free plan only provides current exchange rates. Historical data access requires upgrading to a paid plan.

## Supported Currencies

The Exchange Rate API supports major world currencies including:
- **Major pairs**: USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD
- **Emerging markets**: CNY, INR, BRL, RUB, KRW, SGD, HKD, MXN
- **European**: NOK, SEK, DKK, PLN, CZK, HUF
- **Asian**: THB, MYR, PHP, IDR, VND
- **Others**: ZAR, TRY, ILS, AED, SAR, and many more

## Setup

### 1. API Key Configuration

1. Visit [exchangerate-api.com](https://exchangerate-api.com/) and sign up for a free account
2. Get your API key from the dashboard
3. Add your API key to the `.env` file in the project root:

```bash
# .env file
EXCHANGE_RATE_API_KEY=your_api_key_here
```

### 2. Required Dependencies

The Exchange Rate API fetcher requires the following Python packages:
- `requests` - For HTTP API calls
- `pandas` - For data manipulation
- `tqdm` - For progress bars

These are typically included in the project's requirements.

## Usage

### Basic Command Structure

```bash
python run_analysis.py exrate --ticker CURRENCY_PAIR --interval TIMEFRAME --start START_DATE --end END_DATE --point POINT_SIZE [options]
```

### Required Arguments

- `--ticker`: Currency pair (e.g., EURUSD, GBPJPY, EUR/USD)
- `--interval`: Timeframe (D1, W1, MN1 - all mapped to daily)
- `--start`: Start date in YYYY-MM-DD format
- `--end`: End date in YYYY-MM-DD format
- `--point`: Point size for the currency pair

### Ticker Format Options

The Exchange Rate API fetcher supports multiple ticker formats:

```bash
# 6-character format (recommended)
--ticker EURUSD
--ticker GBPJPY
--ticker AUDUSD

# Slash-separated format
--ticker EUR/USD
--ticker GBP/JPY
--ticker AUD/USD

# Underscore-separated format
--ticker EUR_USD
--ticker GBP_JPY
--ticker AUD_USD
```

### Examples

#### Basic Usage

```bash
# Fetch EUR/USD daily data for Q1 2024
python run_analysis.py exrate --ticker EURUSD --interval D1 --start 2024-01-01 --end 2024-03-31 --point 0.00001

# Fetch GBP/JPY daily data with PHLD indicator
python run_analysis.py exrate --ticker GBPJPY --interval D1 --start 2024-01-01 --end 2024-04-18 --point 0.01 --rule PHLD

# Fetch USD/CAD data with Pressure Vector indicator and Plotly visualization
python run_analysis.py exrate --ticker USDCAD --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.00001 --rule PV -d plotly
```

#### With Different Visualization Options

```bash
# Terminal visualization (great for SSH/Docker)
python run_analysis.py exrate --ticker EURUSD --interval D1 --start 2024-01-01 --end 2024-02-01 --point 0.00001 -d term

# Static image with mplfinance
python run_analysis.py exrate --ticker GBPJPY --interval D1 --start 2024-01-01 --end 2024-03-01 --point 0.01 -d mpl

# Interactive Plotly charts
python run_analysis.py exrate --ticker AUDUSD --interval D1 --start 2024-01-01 --end 2024-04-01 --point 0.00001 -d plotly
```

#### With Different Trading Rules

```bash
# Predict High Low Direction (PHLD)
python run_analysis.py exrate --ticker EURUSD --interval D1 --start 2024-01-01 --end 2024-04-18 --point 0.00001 --rule PHLD

# Pressure Vector (PV)
python run_analysis.py exrate --ticker GBPJPY --interval D1 --start 2024-01-01 --end 2024-04-18 --point 0.01 --rule PV

# Support & Resistance (SR)
python run_analysis.py exrate --ticker USDCAD --interval D1 --start 2024-01-01 --end 2024-04-18 --point 0.00001 --rule SR

# Raw OHLCV only
python run_analysis.py exrate --ticker AUDUSD --interval D1 --start 2024-01-01 --end 2024-04-18 --point 0.00001 --rule OHLCV
```

## Point Size Guidelines

Point sizes for common currency pairs:

- **Major pairs** (EURUSD, GBPUSD, USDCHF, USDJPY): `0.00001` (5 decimal places)
- **Yen pairs** (EURJPY, GBPJPY, AUDJPY): `0.01` (2 decimal places)
- **Exotic pairs**: Varies, typically `0.00001` or `0.0001`

## Data Characteristics

### What You Get

- **OHLC Data**: For Exchange Rate API, Open=High=Low=Close (single daily rate)
- **Volume**: Always 0 (volume data not available from this API)
- **DateTime Index**: Daily timestamps
- **Automatic Caching**: Data saved to `data/raw_parquet/exrate_TICKER_INTERVAL.parquet`

### Limitations

1. **Historical Data**: Requires paid plan (free plan only provides current rates)
2. **Daily Data Only**: No intraday (hourly, minute) data available
3. **No Volume**: Volume data is not provided by the API
4. **Rate Limits**: 50 requests per day on free plan
5. **Same OHLC**: Since it's one rate per day, Open=High=Low=Close
6. **Delayed Data**: Free plan has 24-hour delay (not real-time)

## Caching Mechanism

The Exchange Rate API fetcher implements intelligent caching:

- **File Location**: `data/raw_parquet/exrate_TICKER_INTERVAL.parquet`
- **Incremental Updates**: Only fetches missing date ranges
- **Rate Limit Friendly**: Minimizes API calls by reusing cached data
- **Automatic Merging**: Combines new data with existing cache

### Cache File Examples

```
data/raw_parquet/exrate_EURUSD_D1.parquet
data/raw_parquet/exrate_GBPJPY_D1.parquet
data/raw_parquet/exrate_AUDUSD_D1.parquet
```

## Show Mode Support

View cached Exchange Rate API files:

```bash
# List all Exchange Rate API files
python run_analysis.py show exrate

# Find specific currency pair files
python run_analysis.py show exrate eurusd

# View file with indicator calculation
python run_analysis.py show exrate eurusd --rule PV
```

## Error Handling

The fetcher handles various error conditions gracefully:

- **Missing API Key**: Clear error message with setup instructions
- **Invalid Currency Pairs**: Validation with supported currency list
- **API Rate Limits**: Graceful handling with retry logic
- **Network Issues**: Timeout handling and error reporting
- **Date Range Issues**: Validation and helpful error messages

## Troubleshooting

### Common Issues

1. **"EXCHANGE_RATE_API_KEY not found"**
   - Solution: Add your API key to the `.env` file

2. **"Invalid ticker format"**
   - Solution: Use supported currency codes (USD, EUR, GBP, etc.)

3. **"Rate limit exceeded"**
   - Solution: Wait until next day or upgrade to paid plan

4. **"No data returned"**
   - Solution: Check if the currency pair is supported and date range is valid

### Debug Tips

```bash
# Check available files
python run_analysis.py show exrate

# Use terminal mode for quick testing
python run_analysis.py exrate --ticker EURUSD --interval D1 --start 2024-01-01 --end 2024-01-05 --point 0.00001 -d term

# Check error logs in the terminal output
```

## Integration with Other Features

The Exchange Rate API data source is fully integrated with all tool features:

- **All Trading Rules**: PHLD, PV, SR, OHLCV
- **All Visualization Options**: fastest, plotly, mpl, seaborn, term
- **Export Capabilities**: Parquet export with indicators
- **Show Mode**: File listing and viewing
- **Date Filtering**: Flexible date range selection

## API Reference

For more information about the Exchange Rate API:
- **Website**: [exchangerate-api.com](https://exchangerate-api.com/)
- **Documentation**: [exchangerate-api.com/docs](https://exchangerate-api.com/docs)
- **Free Plan**: 1,500 requests/month, 160+ currencies
- **Paid Plans**: Higher limits, real-time data, additional features
