# Examples Overview

Overview of all usage examples for the Neozork HLD Prediction project.

## 📚 Examples Catalog

### 🚀 Quick Start
- **[Quick Examples](quick-examples.md)** - Quick examples to get started
  - Installation and setup
  - First steps
  - Basic data analysis
  - Interactive mode

### 📊 Main Examples
- **[Usage Examples](usage-examples.md)** - Complete usage examples
  - Comprehensive workflows
  - Advanced scenarios
  - Component integration
  - Performance optimization

### 🎯 Specialized Examples
- **[Indicator Examples](indicator-examples.md)** - Examples of using indicators
  - All indicator categories
  - Combining indicators
  - Exporting results
  - Various chart backends

- **[MCP Examples](mcp-examples.md)** - Examples of using MCP servers
  - Auto-starting MCP servers
  - GitHub Copilot integration
  - Usage patterns
  - Debugging and monitoring

- **[Testing Examples](testing-examples.md)** - Testing examples
  - Running tests
  - Coverage analysis
  - Test debugging
  - Continuous integration

- **[Script Examples](script-examples.md)** - Examples of using scripts
  - Utility scripts
  - Debugging scripts
  - Automation
  - Workflows

- **[Docker Examples](docker-examples.md)** - Examples of using Docker
  - Container deployment
  - Docker development
  - Scaling
  - Container debugging

- **[EDA Examples](eda-examples.md)** - Examples of Exploratory Data Analysis
  - Basic statistical analysis
  - Correlation analysis
  - Data visualization
  - Data quality analysis

## 🎯 Usage Recommendations

### For Beginners
1. Start with **[Quick Examples](quick-examples.md)**
2. Study **[Getting Started](getting-started.md)**
3. Try interactive mode
4. Study **[Indicator Examples](indicator-examples.md)**

### For Developers
1. Study **[Testing Examples](testing-examples.md)**
2. Set up **[MCP Examples](mcp-examples.md)**
3. Use **[Script Examples](script-examples.md)**
4. Consider **[Docker Examples](docker-examples.md)**

### For Analysts
1. Study **[Usage Examples](usage-examples.md)**
2. Master **[Indicator Examples](indicator-examples.md)**
3. Use **[EDA Examples](eda-examples.md)**
4. Set up automation through scripts
5. Consider Docker for reproducibility

### For DevOps
1. Study **[Docker Examples](docker-examples.md)**
2. Set up **[Testing Examples](testing-examples.md)**
3. Automate through **[Script Examples](script-examples.md)**
4. Integrate MCP servers

### For Data Researchers
1. Study **[EDA Examples](eda-examples.md)**
2. Master **[Indicator Examples](indicator-examples.md)**
3. Use **[Usage Examples](usage-examples.md)**
4. Consider **[Docker Examples](docker-examples.md)** for reproducibility

## 🔄 Workflows

### Complete Analysis Pipeline
```bash
# 1. Quick start
python run_analysis.py demo --rule RSI

# 2. Load real data
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 3. EDA analysis
python run_analysis.py eda -f data.csv

# 4. Analysis with indicators
python run_analysis.py show csv mn1 -d fastest --rule rsi:14,30,70,close

# 5. View results
python run_analysis.py show csv mn1 -d fastest

# 6. Testing
uv run pytest tests/ -v

# 7. Coverage analysis
uv run pytest tests/ --cov=src --cov-report=html
```

### Development with MCP
```bash
# 1. Start MCP servers
python start_mcp_server.py

# 2. Test MCP
python scripts/check_mcp_status.py

# 3. Development with AI help
# Use GitHub Copilot in IDE

# 4. Fix imports
python scripts/utilities/fix_imports.py

# 5. Run tests
uv run pytest tests/ -v
```

### EDA Pipeline
```bash
# 1. Load data
python run_analysis.py yf -t BTC-USD --period 6mo

# 2. Basic EDA
python run_analysis.py eda -f data.csv

# 3. Data quality analysis
python run_analysis.py eda -f data.csv --quality

# 4. Correlation analysis
python run_analysis.py eda -f data.csv --correlation

# 5. Visualization
python run_analysis.py eda -f data.csv --plot

# 6. Export results
python run_analysis.py export -f data.csv --format parquet
```

### Docker Deployment
```bash
# 1. Build container
docker build -t neozork-hld .

# 2. Run analysis
docker run -v $(pwd)/data:/app/data neozork-hld python run_analysis.py demo

# 3. EDA in container
docker run -v $(pwd)/data:/app/data neozork-hld python run_analysis.py eda -f data.csv

# 4. Testing in container
docker run neozork-hld uv run pytest tests/ -v

# 5. MCP servers in container
docker run -p 8000:8000 neozork-hld python start_mcp_server.py
```

## 📊 Example Categories

### Data Analysis
- **Demo data**: Quick start with sample data
- **Yahoo Finance**: Real market data
- **Binance**: Cryptocurrency data
- **CSV files**: Custom data import
- **Exchange Rate API**: Currency data
- **EDA analysis**: Exploratory data analysis

### Technical Indicators
- **Trend indicators**: EMA, ADX, SAR
- **Oscillators**: RSI, Stochastic, CCI
- **Momentum**: MACD
- **Volatility**: ATR, Bollinger Bands, Standard Deviation
- **Volume**: OBV, VWAP
- **Support/Resistance**: Donchian, Fibonacci, Pivot Points
- **Predictive**: HMA, Time Series Forecast
- **Probability**: Kelly Criterion, Monte Carlo
- **Sentiment**: COT, Fear & Greed, Social Sentiment

### Export and Visualization
- **Formats**: Parquet, CSV, JSON
- **Backends**: Plotly, Seaborn, Matplotlib, Terminal
- **Performance**: Optimized rendering
- **Interactive**: Hover tools, zoom, pan

### Testing
- **Unit tests**: Individual component testing
- **Integration tests**: End-to-end testing
- **Coverage analysis**: Code coverage reports
- **Test debugging**: Troubleshooting test issues
- **Continuous integration**: Automated testing

### MCP Servers
- **Auto-start**: Automatic server startup
- **GitHub Copilot**: AI integration
- **Stdio mode**: Standard input/output communication
- **Monitoring**: Server health monitoring
- **Debugging**: Server troubleshooting

### Scripts
- **Import fixes**: Automatic import corrections
- **Debugging scripts**: Problem diagnosis
- **Dependency analysis**: Package dependency checking
- **Test data creation**: Sample data generation
- **Workflow automation**: Process automation

## 🎯 Usage Scenarios

### Exploratory Analysis
```bash
# Interactive mode for exploration
python run_analysis.py demo --interactive

# EDA analysis
python run_analysis.py eda -f data.csv --plot

# Quick indicator testing
python run_analysis.py show csv mn1 -d fastest --rule rsi:14,30,70,close
```

### Production Analysis
```bash
# Load and analyze real data
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# EDA analysis
python run_analysis.py eda -f data.csv --quality

# Analysis with indicators
python run_analysis.py show csv mn1 -d fastest --rule macd:12,26,9,close

# Export results
python run_analysis.py export -f results.csv --format parquet
```

### Development of New Indicators
```bash
# Create test data
python scripts/utilities/create_test_parquet.py

# Run tests
uv run pytest tests/calculation/indicators/ -v

# Check coverage
uv run pytest tests/ --cov=src/calculation/indicators --cov-report=html

# Debug issues
python scripts/debug/debug_indicator_calculation.py
```

## 💡 Key Features

### Structured Organization
- Logical organization by categories
- Gradual complexity from basic to advanced
- Cross-references between examples

### Practicality
- Ready-to-use commands
- Real application scenarios
- Step-by-step instructions

### Complete Coverage
- All main project functions
- Various usage scenarios
- Debugging and troubleshooting

### Adaptability
- Examples for different user levels
- Various deployment environments
- Flexible configurations

## 🚀 Next Steps

### For Users
1. Study examples in recommended sequence
2. Adapt to your needs
3. Create your own workflows
4. Contribute to documentation improvement

### For Developers
1. Use examples for testing
2. Integrate into CI/CD pipelines
3. Create additional examples
4. Improve existing examples

### For Community
1. Share usage experience
2. Report issues
3. Suggest improvements
4. Create additional examples

---

📚 **Additional Resources:**
- **[Complete Documentation](index.md)** - Overview of all documentation
- **[Getting Started Guide](getting-started.md)** - Installation and setup
- **[Project Structure](project-structure.md)** - Code organization
- **[Testing Guide](testing.md)** - Detailed testing guide 