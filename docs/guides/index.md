# Guides & Tutorials

This section provides comprehensive guides and tutorials for using the NeoZork HLD Prediction project, including setup, configuration, analysis, and development.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## 🚀 Quick Start Guides

### [Getting Started Guide](getting-started.md)
Complete step-by-step guide for setting up the project.

**Covers:**
- System requirements and prerequisites
- Installation methods (Docker and local)
- Initial configuration
- First analysis run
- Troubleshooting common issues

### [UV Package Management Guide](uv-package-management.md)
Comprehensive guide for UV package manager usage.

**Highlights:**
- **UV Installation**: Installing and configuring UV
- **Docker Integration**: UV usage in containers
- **Local Development**: UV for local environments
- **Adaptive Testing**: Tests that work in both environments
- **Performance Optimization**: UV vs traditional pip

## 🔧 Setup and Configuration

### [Docker Setup](docker-setup.md)
Complete guide for containerized development and deployment.

> **Note**: Docker support is limited to v0.5.2 and earlier versions.

**Features:**
- Docker installation and configuration
- Container management
- UV integration in Docker
- Environment variables
- Service orchestration

### [Local Development Setup](local-setup.md)
Setting up a local development environment.

**Includes:**
- Python environment setup
- UV package manager installation
- Virtual environment configuration
- Development tools setup
- Testing environment

### [IDE Configuration](ide-configuration.md)
Configuring your IDE for optimal development experience.

**Covers:**
- VS Code configuration
- PyCharm setup
- Vim/Neovim configuration
- MCP server integration
- Debugging setup

## 🧪 Testing and Quality Assurance

### [Testing Guide](testing-guide.md)
Comprehensive testing framework and guidelines.

**Includes:**
- Test structure and organization
- Running tests in different environments
- UV-specific testing
- Adaptive testing patterns
- Test coverage and quality

### [UV Testing Guide](uv-testing-guide.md)
Specialized guide for UV package manager testing.

**Highlights:**
- **Docker Testing**: UV tests in containers (limited to v0.5.2 and earlier versions)
- **Local Testing**: UV tests in local environment
- **Adaptive Testing**: Environment-aware tests
- **Performance Testing**: UV vs pip comparison
- **Integration Testing**: End-to-end UV validation

### [Code Quality Guide](code-quality.md)
Maintaining high code quality standards.

**Covers:**
- Linting and formatting
- Type checking
- Security scanning
- Code review process
- Best practices

## 📊 Analysis and Data

### [Data Sources Guide](data-sources.md)
Working with different financial data sources.

**Includes:**
- Polygon API integration
- YFinance data access
- Binance cryptocurrency data
- MQL5 MetaTrader data
- CSV and Parquet file processing

### [Analysis Tools Guide](analysis-tools.md)
Comprehensive guide to analysis tools and techniques.

**Features:**
- Exploratory Data Analysis (EDA)
- Technical indicator analysis
- Visualization tools
- Statistical analysis
- Performance metrics

### [CLI Interface Guide](cli-interface.md)
Command-line interface usage and reference.

**Covers:**
- Basic commands and syntax
- Advanced options and flags
- Interactive mode
- Batch processing
- Output formats

## 📈 Technical Indicators

### [Adding Custom Indicators](adding-custom-indicators.md)
Guide for adding new technical indicators to the system.

**Includes:**
- Indicator development workflow
- Code structure and patterns
- Testing requirements
- Documentation standards
- Integration process

### [SMA Indicator Tutorial](adding-sma-indicator-tutorial.md) ⭐ **COMPLETE**
Complete tutorial for SMA (Simple Moving Average) indicator implementation.

**Features:**
- Full implementation across all display modes
- Parameter configuration
- Testing framework
- Performance optimization
- Real-world examples

### [Wave Indicator Tutorial](adding-wave-indicator-tutorial.md) ⭐ **ADVANCED**
Advanced tutorial for Wave indicator implementation with dual-system architecture.

**Highlights:**
- Dual-wave system implementation
- Multiple trading rules
- Fast mode support
- Seaborn and terminal mode integration
- Signal filtering and optimization

### [Wave Indicator Fast Mode](adding-wave-indicator-fast-mode-tutorial.md)
Specialized guide for Wave indicator fast mode implementation.

**Covers:**
- Fast mode architecture
- Performance optimization
- Visual parity implementation
- Discontinuous line handling
- Mode-specific features

## 🎨 Visualization and Plotting

### [Plotting and Visualization Guide](plotting-visualization.md)
Comprehensive guide to visualization tools and techniques.

**Includes:**
- Multiple plotting backends (Plotly, Matplotlib, Seaborn)
- Interactive charts
- Static visualizations
- Custom styling
- Export options

### [Plotting Modes Comparison](plotting-modes-comparison.md)
Detailed comparison of different plotting modes and their features.

**Modes Covered:**
- **Fastest**: Minimal overhead, basic charts
- **Fast**: Bokeh-based interactive charts
- **Plotly**: Rich interactive visualizations
- **MPL**: Matplotlib static charts
- **Seaborn**: Scientific presentation style
- **Terminal**: ASCII-based SSH-friendly charts

## 🔧 Development and Debugging

### [Debug Scripts Guide](debug-scripts.md)
Guide to debugging tools and scripts.

**Tools:**
- API debugging scripts
- Data validation tools
- Performance profiling
- Error diagnosis
- Log analysis

### [Utility Scripts Guide](utility-scripts.md)
Overview of utility scripts and their usage.

**Scripts:**
- Data processing utilities
- File conversion tools
- Environment setup scripts
- Maintenance utilities
- Automation scripts

### [Workflow Utilities Guide](workflow-utilities.md)
Guide to workflow automation and utilities.

**Features:**
- Automated analysis pipelines
- Batch processing
- Data preprocessing
- Result aggregation
- Report generation

## 📊 Advanced Features

### [Parameterized Indicators Guide](parameterized-indicators.md)
Guide to creating and using parameterized indicators.

**Covers:**
- Parameter configuration
- Dynamic indicator creation
- Custom parameter sets
- Optimization techniques
- Performance considerations

### [Export Functions Guide](export-functions.md)
Guide to data export and reporting features.

**Formats:**
- CSV export
- Parquet export
- JSON export
- Chart export
- Report generation

### [Enhanced Error Handling Guide](enhanced-error-handling.md)
Guide to error handling and recovery mechanisms.

**Features:**
- Graceful error recovery
- User-friendly error messages
- Debug information
- Error logging
- Recovery strategies

## 🚀 Performance and Optimization

### [Performance Optimization Guide](performance-optimization.md)
Guide to optimizing performance and resource usage.

**Areas:**
- Data processing optimization
- Memory management
- CPU utilization
- I/O optimization
- Caching strategies

### [UV Performance Guide](uv-performance-guide.md)
Specialized guide for UV package manager performance optimization.

**Optimizations:**
- Dependency resolution speed
- Installation optimization
- Cache management
- Parallel processing
- Resource usage

## 📋 Reference Guides

### [Trading Metrics Encyclopedia](trading-metrics-encyclopedia.md)
Comprehensive reference for trading metrics and indicators.

**Metrics:**
- Technical indicators
- Performance metrics
- Risk measures
- Statistical measures
- Custom metrics

### [Quant Encyclopedia](quant-encyclopedia.md)
Quantitative analysis reference guide.

**Topics:**
- Mathematical concepts
- Statistical methods
- Financial models
- Risk management
- Portfolio theory

## 🔍 Troubleshooting

### [Common Issues Guide](common-issues-guide.md)
Guide to common problems and their solutions.

**Issues:**
- Installation problems
- Configuration issues
- Performance problems
- Data access issues
- Testing failures

### [Debugging Guide](debugging-guide.md)
Comprehensive debugging guide and techniques.

**Techniques:**
- Log analysis
- Error tracing
- Performance profiling
- Memory debugging
- Network debugging

## 📚 Additional Resources

### [Examples and Demos](examples/)
Practical examples and demonstration scripts.

### [API Reference](../reference/)
Complete API documentation and reference.

### [Testing Documentation](../testing/)
Comprehensive testing documentation and examples.

---

**Last Updated**: 2024
**Total Guides**: 50+ 
