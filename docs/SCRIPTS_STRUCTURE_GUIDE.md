# 📁 Scripts Directory Structure Guide

**Date:** August 24, 2025  
**Status:** ✅ ORGANIZED  
**Scope:** Complete scripts directory organization and categorization

---

## 🎯 Organization Goals

The scripts directory has been reorganized to provide:
1. **Logical grouping** of related functionality
2. **Clear separation** of concerns
3. **Easy navigation** for developers
4. **Maintainable structure** for future additions

---

## 📂 Directory Structure

```
scripts/
├── main/                           # Main entry point scripts
│   ├── eda_fe                     # EDA + Feature Engineering pipeline
│   └── nz_interactive             # Interactive system launcher
├── ml/                            # Machine Learning scripts
│   ├── eda_feature_engineering.py # Integrated EDA + Feature Engineering
│   ├── interactive_system.py      # Interactive menu system
│   ├── demo_feature_engineering.py # Feature engineering demo
│   └── test_system.py             # System testing script
├── eda/                           # EDA and data analysis scripts
│   └── create_test_data.py        # Test data generation
├── testing/                       # Test execution and validation
│   ├── run_all_tests.sh           # Run all tests
│   ├── run_all_tests_safe.sh      # Safe test execution
│   ├── run_tests_safe.sh          # Individual safe test runner
│   ├── run_tests_with_timeout.sh  # Tests with timeout
│   ├── run_tests_native_container.sh # Native container tests
│   └── test_docker_history.sh     # Docker test history
├── debug/                         # Debugging and troubleshooting
│   ├── debug_docker_processes.py  # Docker process debugging
│   ├── debug_rsi_signals.py       # RSI signal debugging
│   ├── debug_wave_indicator.py    # Wave indicator debugging
│   ├── debug_yfinance.py          # YFinance debugging
│   ├── debug_binance.py           # Binance debugging
│   ├── debug_polygon.py           # Polygon debugging
│   ├── examine_parquet.py         # Parquet file examination
│   └── ...                        # Additional debug scripts
├── mcp/                           # MCP server and management
│   ├── check_mcp_status.py        # MCP status checker
│   ├── neozork_mcp_manager.py     # MCP server manager
│   ├── start_mcp_server_daemon.py # MCP daemon starter
│   └── ...                        # Additional MCP scripts
├── utilities/                     # Utility and helper scripts
│   ├── check_uv_mode.py           # UV mode checker
│   ├── create_test_parquet.py     # Test parquet creator
│   ├── fix_imports.py             # Import fixer
│   └── ...                        # Additional utilities
├── analysis/                      # Analysis and optimization
│   ├── dead-code/                 # Dead code analysis
│   ├── analyze_requirements.py    # Requirements analysis
│   └── ...                        # Additional analysis tools
├── docker/                        # Docker-related utilities
│   └── ...                        # Docker scripts
├── native-container/              # Native container scripts
│   └── ...                        # Native container utilities
└── __init__.py                    # Package initialization
```

---

## 🚀 Main Scripts (Entry Points)

### **`scripts/main/` - User-Facing Scripts**

These scripts are accessible from the project root via symbolic links:

#### `eda_fe` - EDA + Feature Engineering Pipeline
```bash
# From project root
python scripts/main/eda_fe --file data.csv --full-pipeline
```

**Features:**
- Complete EDA analysis
- Feature engineering pipeline
- Automated reporting
- Environment detection (Docker/UV/Native)

#### `nz_interactive` - Interactive System
```bash
# From project root
./nz_interactive --full

# Direct access
scripts/main/nz_interactive --full
```

**Features:**
- Interactive menu system
- Data loading and analysis
- Feature engineering
- Results export

---

## 🤖 Machine Learning Scripts

### **`scripts/ml/` - Core ML Functionality**

#### `eda_feature_engineering.py`
- **Purpose**: Integrated EDA + Feature Engineering pipeline
- **Usage**: `python scripts/ml/eda_feature_engineering.py --file data.csv --full-pipeline`
- **Features**: Complete feature generation and selection

#### `interactive_system.py`
- **Purpose**: Interactive menu-driven system
- **Usage**: `python scripts/ml/interactive_system.py`
- **Features**: User-friendly interface for all operations

#### `demo_feature_engineering.py`
- **Purpose**: Feature engineering demonstration
- **Usage**: `python scripts/ml/demo_feature_engineering.py`
- **Features**: Showcase of feature generation capabilities

#### `test_system.py`
- **Purpose**: System testing and validation
- **Usage**: `python scripts/ml/test_system.py`
- **Features**: Automated system testing

---

## 📊 EDA and Data Analysis

### **`scripts/eda/` - Data Analysis Tools**

#### `create_test_data.py`
- **Purpose**: Generate test datasets
- **Usage**: `python scripts/eda/create_test_data.py`
- **Features**: Create various OHLCV datasets for testing

---

## 🧪 Testing and Validation

### **`scripts/testing/` - Test Execution**

#### Shell Scripts
- `run_all_tests.sh` - Execute all tests
- `run_all_tests_safe.sh` - Safe test execution with error handling
- `run_tests_safe.sh` - Individual safe test runner
- `run_tests_with_timeout.sh` - Tests with timeout protection
- `run_tests_native_container.sh` - Native container test execution
- `test_docker_history.sh` - Docker test history analysis

---

## 🐛 Debugging and Troubleshooting

### **`scripts/debug/` - Debug Utilities**

#### Data Source Debugging
- `debug_yfinance.py` - YFinance connection and data issues
- `debug_binance.py` - Binance API debugging
- `debug_polygon.py` - Polygon API debugging

#### Indicator Debugging
- `debug_rsi_signals.py` - RSI signal analysis
- `debug_wave_indicator.py` - Wave indicator debugging

#### File Debugging
- `examine_parquet.py` - Parquet file examination
- `debug_check_parquet.py` - Parquet validation

---

## 🔌 MCP Server Management

### **`scripts/mcp/` - Model Context Protocol**

#### Core MCP Scripts
- `check_mcp_status.py` - Check MCP server status
- `neozork_mcp_manager.py` - MCP server manager
- `start_mcp_server_daemon.py` - Start MCP daemon

---

## 🛠️ Utilities and Helpers

### **`scripts/utilities/` - Helper Scripts**

#### Development Utilities
- `check_uv_mode.py` - UV package manager mode checker
- `create_test_parquet.py` - Test parquet file creation
- `fix_imports.py` - Import statement fixes
- `setup_ide_configs.py` - IDE configuration setup

---

## 📈 Analysis and Optimization

### **`scripts/analysis/` - Analysis Tools**

#### Dead Code Analysis
- `dead-code/` - Dead code detection and removal
- `analyze_requirements.py` - Requirements analysis
- `fix_test_coverage.py` - Test coverage fixes

---

## 🐳 Container Management

### **`scripts/docker/` - Docker Utilities**
- Docker-specific scripts and utilities

### **`scripts/native-container/` - Native Container**
- Apple Silicon native container scripts

---

## 🔗 Symbolic Links

### **Project Root Access**

For user convenience, main scripts are accessible from the project root:

```bash
# Symbolic links in project root
# Removed symbolic link - use direct path
# Removed symbolic link - use direct path
```

### **Usage Examples**

```bash
# From project root (recommended)
python scripts/main/eda_fe --file data.csv --full-pipeline
python scripts/ml/interactive_system.py

# Direct access (for developers)
python scripts/main/eda_fe --file data.csv --full-pipeline
python scripts/ml/interactive_system.py
```

---

## 📋 File Naming Conventions

### **Script Categories**
- **Main scripts**: Simple names (`eda_fe`, `nz_interactive`)
- **ML scripts**: Descriptive names (`eda_feature_engineering.py`)
- **Debug scripts**: `debug_*` prefix
- **Test scripts**: `test_*` prefix or `run_*` prefix
- **Utility scripts**: Action-oriented names (`fix_imports.py`)

### **File Extensions**
- **Python scripts**: `.py`
- **Shell scripts**: `.sh`
- **Configuration**: `.py`, `.json`, `.yaml`

---

## 🚀 Quick Reference

### **Most Common Commands**
```bash
# EDA + Feature Engineering
python scripts/main/eda_fe --file data.csv --full-pipeline

# Interactive System
python scripts/ml/interactive_system.py

# Feature Engineering Demo
python scripts/ml/demo_feature_engineering.py

# Test Data Generation
python scripts/eda/create_test_data.py
```

### **Development Commands**
```bash
# Run all tests
./scripts/testing/run_all_tests.sh

# Debug specific component
python scripts/debug/debug_wave_indicator.py

# Check MCP status
python scripts/mcp/check_mcp_status.py
```

---

## 🔧 Maintenance Notes

### **Adding New Scripts**
1. **Categorize** the script by functionality
2. **Place** in appropriate subdirectory
3. **Update** this guide if adding new categories
4. **Test** the script from its new location

### **Moving Scripts**
1. **Update** symbolic links if moving main scripts
2. **Update** documentation references
3. **Test** functionality from new location
4. **Update** import paths if needed

---

**Structure Guide Created:** August 24, 2025  
**Status:** ✅ COMPLETE  
**Next Update:** As needed for new scripts or reorganization
