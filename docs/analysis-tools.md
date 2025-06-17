# Analysis Tools Guide

Core analysis workflow tools and utilities for data processing and indicator calculations.

## Main Analysis Engine

### `run_analysis.py` - Core Analysis Pipeline
**Purpose:** Main analysis and prediction engine with multiple data source support

**Key Features:**
- Multiple data source integration
- Comprehensive indicator calculations
- Advanced plotting capabilities
- Automated data caching
- Show mode for data exploration

## Data Source Modes

### Demo Mode
**Purpose:** Testing and demonstration without external dependencies

```bash
# Basic demo
python run_analysis.py demo
nz demo

# With specific indicators
nz demo --rule PHLD
nz demo --rule PV --draw plotly
```

**Features:**
- Built-in sample data
- All indicator calculations available
- No API keys required
- Perfect for testing and learning

### CSV Mode
**Purpose:** Analyze MT5 exported data or custom CSV files

```bash
# Basic CSV analysis
nz csv --csv-file data/your_file.csv --point 0.01

# Advanced analysis
nz csv --csv-file data/EURUSD_M1.csv --point 0.00001 --rule PHLD -d mplfinance
```

**Features:**
- MT5 export format support
- Custom CSV format detection
- Automatic caching to Parquet
- Data validation against MQL5 results

### API Modes

#### Yahoo Finance Mode
```bash
# Forex
nz yf -t EURUSD=X --period 1mo --point 0.00001

# Stocks
nz yf -t AAPL --period 6mo --point 0.01

# Crypto
nz yf -t BTC-USD --start 2024-01-01 --end 2024-12-31 --point 0.01
```

#### Polygon.io Mode
```bash
# Professional market data
nz polygon --ticker AAPL --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01
nz polygon --ticker C:EURUSD --interval H1 --start 2024-01-01 --end 2024-03-01 --point 0.00001
```

#### Binance Mode
```bash
# Cryptocurrency data
nz binance --ticker BTCUSDT --interval H1 --start 2024-01-01 --end 2024-04-18 --point 0.01
nz binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01
```

### Show Mode - Data Exploration
**Purpose:** Interactive browsing and analysis of cached datasets

```bash
# List all cached data
nz show

# Filter by source and keywords
nz show yf aapl
nz show binance btc
nz show polygon eurusd

# Analyze specific cached file
nz show yf aapl --rule PV -d plotly
```

## Indicator Rules

### Available Trading Rules

| Rule Code | Full Name | Description |
|-----------|-----------|-------------|
| `PHLD` | Predict High Low Direction | Main prediction algorithm |
| `PV` | Pressure Vector | Core pressure calculations |
| `SR` | Support Resistance | Support/resistance levels |
| `PV_HighLow` | PV High/Low Analysis | PV-based high/low prediction |
| `Pressure_Vector` | Full Pressure Vector | Complete pressure analysis |
| `Support_Resistants` | Support/Resistance | Detailed S/R calculations |
| `Predict_High_Low_Direction` | Full PHLD | Complete PHLD algorithm |
| `OHLCV` | Basic OHLCV | Raw price data only |
| `AUTO` | Auto Detection | Show all available fields |

### Rule Usage Examples
```bash
# Main prediction rules
nz demo --rule PHLD
nz yf -t AAPL --period 1mo --point 0.01 --rule PV

# Support/Resistance analysis
nz csv --csv-file data.csv --point 0.01 --rule SR

# Show all data fields
nz show yf aapl --rule AUTO
```

## Plotting Backends

### Available Plotting Options

| Backend | Command | Best For | Features |
|---------|---------|----------|----------|
| `fastest` | `-d fastest` | Large datasets | Fast rendering, minimal features |
| `fast` | `-d fast` | Quick analysis | Basic plotting, good performance |
| `plotly` | `-d plotly` | Interactive analysis | Zoom, pan, interactive features |
| `mplfinance` | `-d mplfinance` | Professional charts | Financial chart standards |
| `seaborn` | `-d seaborn` | Statistical analysis | Statistical plot types |
| `matplotlib` | `-d mpl` | Custom plotting | Full matplotlib control |
| `terminal` | `-d term` | Docker/headless | ASCII terminal plots |

### Plotting Examples
```bash
# Interactive plotting
nz demo --rule PHLD -d plotly

# Professional financial charts
nz yf -t AAPL --period 1mo --point 0.01 -d mplfinance

# Statistical analysis plots
nz csv --csv-file data.csv --point 0.01 --rule PV -d seaborn

# Terminal plotting (for Docker)
nz demo -d term
```

## Data Caching System

### Automatic Caching
- **CSV Mode:** Cached in `data/cache/csv_converted/`
- **API Modes:** Cached in `data/raw_parquet/`
- **Incremental Updates:** Only fetch missing data ranges
- **Smart Detection:** Automatic cache validation

### Cache Management
```bash
# View cached data
nz show

# Clear specific cache
rm data/raw_parquet/yfinance_AAPL_*.parquet

# Clear all cache
rm data/cache/csv_converted/*.parquet
rm data/raw_parquet/*.parquet
```

### Cache Structure
```
data/
├── cache/
│   └── csv_converted/
│       ├── CSVExport_XAUUSD_MN1.parquet
│       └── custom_data.parquet
└── raw_parquet/
    ├── yfinance_AAPL_D1_2024.parquet
    ├── polygon_EURUSD_H1_2024.parquet
    └── binance_BTCUSDT_M15_2024.parquet
```

## Advanced Analysis Features

### Point Size Configuration
**Purpose:** Specify instrument point size for accurate calculations

```bash
# Forex majors (5 decimal places)
--point 0.00001  # EURUSD, GBPUSD, AUDUSD

# Forex cross pairs (3 decimal places)
--point 0.001    # USDJPY, USDCHF

# Stocks (2 decimal places)
--point 0.01     # Most stocks

# Cryptocurrency
--point 0.01     # BTC, ETH (high value)
--point 0.001    # Lower value altcoins
```

### Date Range Specifications
```bash
# Using periods
--period 1mo     # 1 month
--period 6mo     # 6 months
--period 1y      # 1 year
--period 5d      # 5 days

# Using specific dates
--start 2024-01-01 --end 2024-12-31
--start 2023-06-01 --end 2023-12-31
```

### Output Options
```bash
# Console output only
nz demo --no-plot

# Save plots to file
nz demo --save-plot

# Custom output directory
nz demo --output-dir results/
```

## Analysis Workflow Integration

### Standard Analysis Pipeline
```bash
# 1. Data quality check
python src/eda/eda_batch_check.py --data-quality-checks

# 2. Fix any issues
python src/eda/eda_batch_check.py --fix-files --fix-all

# 3. Run main analysis
nz yf -t AAPL --period 1mo --point 0.01 --rule PHLD

# 4. Explore results
nz show yf aapl --rule PHLD -d plotly

# 5. Statistical analysis
python src/eda/eda_batch_check.py --correlation-analysis
```

### Batch Processing Workflow
```bash
# Process multiple instruments
for symbol in AAPL MSFT GOOGL; do
    nz yf -t $symbol --period 6mo --point 0.01 --rule PHLD
done

# Process multiple timeframes
for interval in D1 H4 H1; do
    nz polygon --ticker AAPL --interval $interval --start 2024-01-01 --end 2024-12-31 --point 0.01
done
```

## Performance Optimization

### Memory Management
- **Streaming processing** for large datasets
- **Automatic cleanup** of temporary data
- **Efficient Parquet storage** format
- **Memory usage reporting** in output

### Processing Speed
- **Parallel calculations** where possible
- **Optimized pandas operations**
- **Smart caching** to avoid re-computation
- **Progress tracking** for long operations

### Resource Monitoring
```bash
# Monitor memory usage
nz yf -t AAPL --period 1y --point 0.01 --verbose

# Check processing time
time nz csv --csv-file large_file.csv --point 0.01

# Resource usage summary
nz demo --show-performance
```

## Error Handling and Validation

### Input Validation
- **Parameter validation** before processing
- **File existence checks**
- **API key validation**
- **Date range validation**

### Data Validation
- **Schema validation** for incoming data
- **Data quality checks** during processing
- **Calculation validation** against known results
- **Output validation** before saving

### Error Recovery
- **Graceful degradation** on partial failures
- **Retry mechanisms** for network issues
- **Cache fallback** for API failures
- **Detailed error reporting**

## Integration with Other Tools

### EDA Integration
```bash
# Combined workflow
python src/eda/eda_batch_check.py --data-quality-checks && \
nz yf -t AAPL --period 1mo --point 0.01 --rule PHLD && \
python src/eda/eda_batch_check.py --basic-stats
```

### Testing Integration
```bash
# Validate analysis results
pytest tests/calculation/test_indicator_accuracy.py

# Test API connections before analysis
python scripts/debug_scripts/debug_yfinance.py && \
nz yf -t AAPL --period 1mo --point 0.01
```

### Docker Integration
```bash
# Run analysis in container
docker compose run --rm neozork-hld nz demo --rule PHLD

# Background analysis
docker compose up -d
docker exec -it container_name nz yf -t AAPL --period 1mo --point 0.01
```

## Best Practices

### Analysis Workflow
1. **Start with demo mode** to understand the system
2. **Test data sources** with debug scripts
3. **Check data quality** before analysis
4. **Use appropriate point sizes** for instruments
5. **Choose suitable plotting backends** for your needs

### Performance Tips
1. **Use caching effectively** to avoid re-downloading data
2. **Choose appropriate date ranges** to balance detail and performance
3. **Monitor memory usage** with large datasets
4. **Use fastest plotting** for exploratory analysis

### Quality Assurance
1. **Validate inputs** before processing
2. **Check output consistency** across runs
3. **Compare results** with known benchmarks
4. **Document analysis parameters** for reproducibility
