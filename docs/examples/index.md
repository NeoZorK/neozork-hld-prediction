# Examples & Usage Patterns

This section provides comprehensive examples and usage patterns for the NeoZork HLD Prediction project, covering all major features and use cases.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## 🚀 Quick Start Examples

### [Quick Examples](quick-examples.md)
Essential examples to get started quickly.

**Includes:**
- Basic analysis commands
- Simple indicator usage
- Data source examples
- Common workflows
- Troubleshooting examples

### [Usage Examples](usage-examples.md)
Comprehensive usage examples for all features.

**Covers:**
- Command-line interface usage
- Data source integration
- Technical indicator analysis
- Visualization and plotting
- Export and reporting

## 📊 Analysis Examples

### [EDA Examples](eda-examples.md)
Exploratory Data Analysis examples and patterns.

**Features:**
- Data quality assessment
- Statistical analysis
- Pattern recognition
- Time series analysis
- Data visualization

### [Indicator Examples](indicator-examples.md)
Technical indicator usage examples.

**Indicators:**
- Momentum indicators (RSI, MACD)
- Trend indicators (SMA, EMA, SuperTrend)
- Oscillators (Stochastic, CCI)
- Volume indicators (OBV, VWAP)
- Support & Resistance (Pivot Points)
- Sentiment indicators (COT, Put/Call Ratio)

### [Wave Indicator Examples](wave-indicator-examples.md)
Advanced Wave indicator examples and patterns.

**Features:**
- Dual-wave system usage
- Multiple trading rules
- Fast mode examples
- Seaborn mode visualization
- Terminal mode usage
- Signal filtering examples

## 🐳 Container & Environment Examples

### [Docker Examples](docker-examples.md)
Docker container usage examples.

> **Note**: Docker examples are limited to v0.5.2 and earlier versions.

**Covers:**
- Container setup and management
- UV package management in Docker
- Service orchestration
- Environment configuration
- Performance optimization

### [Testing Examples](testing-examples.md)
Testing framework examples and patterns.

**Includes:**
- Unit test examples
- Integration test patterns
- UV-specific testing
- Adaptive testing examples
- Performance testing

## 🔧 Development Examples

### [Script Examples](script-examples.md)
Utility script usage examples.

**Scripts:**
- Data processing scripts
- Analysis automation
- Debugging utilities
- Environment setup
- Maintenance tools

### [MCP Examples](mcp-examples.md)
Model Context Protocol server examples.

**Features:**
- MCP server setup
- IDE integration examples
- Environment detection
- Server configuration
- Usage patterns

### [Interactive System Examples](interactive-system-data-loading.md)
Interactive system usage examples.

**Covers:**
- Interactive data loading
- Real-time analysis
- User interface patterns
- Data validation
- Error handling

## 📈 Advanced Examples

### [Examples Overview](examples-overview.md)
Comprehensive overview of all examples.

**Structure:**
- Example categorization
- Usage patterns
- Best practices
- Common workflows
- Performance considerations

### [Examples Summary](EXAMPLES_SUMMARY.md)
Summary of all examples and their purposes.

**Highlights:**
- Quick reference guide
- Example mapping
- Usage recommendations
- Implementation notes
- Troubleshooting tips

## 🎯 Example Categories

### Basic Usage
- **Data Sources**: Polygon, YFinance, Binance, MQL5
- **Indicators**: Simple and complex technical indicators
- **Visualization**: Different plotting modes and styles
- **Export**: Data and chart export options

### Advanced Features
- **Wave Indicator**: Dual-system implementation
- **Fast Mode**: Bokeh-based interactive charts
- **Seaborn Mode**: Scientific presentation style
- **Terminal Mode**: ASCII-based SSH-friendly charts

### Development
- **Testing**: Comprehensive test examples
- **Scripts**: Utility and automation scripts
- **MCP Server**: IDE integration examples
- **Docker**: Container management examples

## 📋 Example Usage Patterns

### Data Analysis Workflow
```bash
# 1. Load data
nz yfinance AAPL --period 1y

# 2. Apply indicators
nz yfinance AAPL --rule sma:20,close,RSI

# 3. Visualize results
nz yfinance AAPL --rule sma:20,close -d plotly

# 4. Export results
nz yfinance AAPL --rule sma:20,close --export-csv
```

### Batch Processing
```bash
# Process multiple files
nz csv --csv-folder data/ --rule RSI

# Process with mask filtering
nz csv --csv-folder data/ --csv-mask EURUSD --rule SMA

# Export batch results
nz csv --csv-folder data/ --rule RSI --export-parquet
```

### Advanced Analysis
```bash
# Wave indicator with custom parameters
nz csv mn1 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d sb

# Multiple indicators combination
nz csv mn1 --rule sma:20,close,RSI,MACD -d plotly

# Interactive analysis
nz interactive
```

## 🔍 Finding Examples

### By Feature
- **Data Sources**: Check specific data source examples
- **Indicators**: Look for indicator-specific examples
- **Visualization**: Find plotting and chart examples
- **Development**: See development and testing examples

### By Complexity
- **Basic**: Quick examples and usage patterns
- **Intermediate**: Feature-specific examples
- **Advanced**: Complex workflows and integrations

### By Environment
- **Docker**: Container-based examples
- **Local**: Local development examples
- **Production**: Production deployment examples

## 📚 Related Documentation

### Guides
- **[Guides Index](../guides/)** - Step-by-step tutorials
- **[Getting Started](../getting-started/)** - Setup and first steps

### Reference
- **[API Reference](../reference/)** - Technical documentation
- **[Testing Documentation](../testing/)** - Testing strategies

### Reports
- **[Development Reports](../reports/)** - Implementation reports

---

**Last Updated**: 2024
**Total Examples**: 13 comprehensive guides 