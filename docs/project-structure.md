# Project Structure

Detailed overview of the codebase organization and architecture.

## Root Directory

```
neozork-hld-prediction/
├── README.md                 # Main project overview and quick links
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Modern Python project configuration
├── uv.lock                  # UV package manager lock file
├── uv.toml                  # UV configuration
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore patterns
├── .dockerignore            # Docker ignore patterns
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Container image definition
├── docker-entrypoint.sh     # Container startup script
├── mcp.json                 # MCP server configuration
├── mcp_server.py            # MCP server implementation
├── run_analysis.py          # Main analysis engine
├── nz                       # Command shortcut script
├── eda                      # EDA shortcut script
└── test-workflow.sh         # GitHub Actions local testing
```

## Core Application Structure

### `src/` - Source Code
**Main application logic and modules**

```
src/
├── __init__.py              # Package initialization and version
├── calculation/             # Core indicator calculations
│   ├── __init__.py
│   ├── core_calculations.py # Basic mathematical operations
│   ├── indicator.py         # Main indicator class
│   ├── indicator_calculation.py # Indicator computation logic
│   └── rules.py            # Trading rules implementation
├── cli/                     # Command-line interface
│   ├── __init__.py
│   ├── cli.py              # Main CLI implementation
│   ├── cli_examples.py     # Usage examples
│   └── cli_show_mode.py    # Show mode functionality
├── common/                  # Shared utilities
│   ├── __init__.py
│   ├── constants.py        # Project constants
│   └── logger.py           # Logging configuration
├── data/                   # Data processing and acquisition
│   ├── __init__.py
│   ├── data_acquisition.py # Main data fetching logic
│   └── fetchers/           # Data source implementations
├── eda/                    # Exploratory Data Analysis
│   ├── __init__.py
│   ├── basic_stats.py      # Basic statistical analysis
│   ├── correlation_analysis.py # Correlation computations
│   ├── data_quality.py     # Data quality checks
│   ├── eda_batch_check.py  # Main EDA batch processor
│   ├── feature_importance.py # Feature analysis
│   ├── file_info.py        # File information utilities
│   ├── fix_files.py        # Data fixing utilities
│   ├── folder_stats.py     # Directory statistics
│   ├── html_report_generator.py # HTML report creation
│   └── stats_logger.py     # Statistics logging
├── export/                 # Data export functionality
│   ├── __init__.py
│   └── parquet_export.py   # Parquet export utilities
├── plotting/               # Visualization backends
│   ├── __init__.py
│   ├── plotting.py         # Main plotting interface
│   ├── fast_plot.py        # Fast plotting implementation
│   ├── fastest_auto_plot.py # Fastest plotting mode
│   ├── fastest_plot.py     # Optimized plotting
│   ├── mplfinance_plot.py  # MPLFinance backend
│   ├── plotly_plot.py      # Plotly backend
│   ├── seaborn_plot.py     # Seaborn backend
│   ├── plotting_generation.py # Plot generation utilities
│   └── term_auto_plot.py   # Terminal plotting
├── utils/                  # General utilities
│   ├── __init__.py
│   └── [various utility modules]
└── workflow/               # Analysis workflow management
    ├── __init__.py
    └── [workflow modules]
```

### `scripts/` - Automation Scripts
**Development and maintenance scripts**

```
scripts/
├── __init__.py
├── analyze_requirements.py  # Dependency analysis
├── auto_pyproject_from_requirements.py # Project file generation
├── init_dirs.sh            # Project initialization
├── run_tests.py            # Test runner
└── debug_scripts/          # Debug and validation tools
    ├── __init__.py
    ├── debug_binance_connection.py # Binance API testing
    ├── debug_check_parquet.py # Parquet validation
    ├── debug_csv_reader.py  # CSV processing testing
    ├── debug_polygon_connection.py # Polygon.io testing
    ├── debug_polygon_resolve.py # Symbol resolution testing
    ├── debug_yfinance.py    # Yahoo Finance testing
    ├── examine_binance_parquet.py # Binance data examination
    └── examine_parquet.py   # General Parquet examination
```

### `tests/` - Test Suite
**Comprehensive testing framework**

```
tests/
├── __init__.py
├── calculation/            # Calculation logic tests
│   ├── __init__.py
│   ├── test_core_calculations.py
│   ├── test_indicator.py
│   └── test_rules.py
├── cli/                   # CLI interface tests
│   ├── __init__.py
│   ├── test_cli_all_commands.py
│   ├── test_cli_examples.py
│   └── test_show_mode.py
├── common/                # Common utilities tests
│   ├── __init__.py
│   ├── test_constants.py
│   └── test_logger.py
├── data/                  # Data processing tests
│   ├── __init__.py
│   ├── test_data_acquisition.py
│   └── test_fetchers.py
├── docker/                # Docker functionality tests
│   ├── __init__.py
│   └── test_docker_build.py
├── eda/                   # EDA tools tests
│   ├── __init__.py
│   ├── test_basic_stats.py
│   ├── test_correlation_analysis.py
│   ├── test_data_quality.py
│   └── test_eda_batch_check.py
├── mcp/                   # MCP server tests
│   ├── __init__.py
│   ├── test_mcp_server.py
│   └── test_mcp_integration.py
├── plotting/              # Visualization tests
│   ├── __init__.py
│   ├── test_plotting.py
│   └── test_backends.py
├── scripts/               # Script functionality tests
│   ├── __init__.py
│   ├── test_analyze_requirements.py
│   ├── test_init_dirs.bats # BATS shell script tests
│   └── test_run_tests.py
├── utils/                 # Utility function tests
│   ├── __init__.py
│   └── [utility tests]
└── workflow/              # Workflow tests
    ├── __init__.py
    ├── test_full_pipeline.py
    └── test_workflow_steps.py
```

## Data Directories

### `data/` - Data Storage
**All data files and caches**

```
data/
├── cache/                 # Processed data cache
│   └── csv_converted/     # CSV to Parquet conversions
│       ├── CSVExport_XAUUSD_MN1.parquet
│       └── [other converted files]
├── raw_parquet/           # API-fetched raw data
│   ├── yfinance_AAPL_D1_2024.parquet
│   ├── polygon_EURUSD_H1_2024.parquet
│   ├── binance_BTCUSDT_M15_2024.parquet
│   └── [other API data files]
├── processed/             # Processed datasets for ML
│   └── [processed datasets]
├── mn1.csv                # Sample M1 data
├── test_data.csv          # Test dataset
└── CSVExport_GBPUSD_PERIOD_MN1.parquet # Sample Parquet data
```

### File Naming Conventions

**API Cache Files:**
```
{source}_{symbol}_{interval}_{date_range}.parquet

Examples:
- yfinance_AAPL_D1_2024-01-01_2024-12-31.parquet
- polygon_EURUSD_H1_2024-Q1.parquet
- binance_BTCUSDT_M15_2024-01.parquet
```

**CSV Converted Files:**
```
{original_filename}.parquet

Examples:
- CSVExport_XAUUSD_MN1.parquet
- MT5_EURUSD_M1_2024.parquet
```

## Configuration and Setup

### `docs/` - Documentation
**Comprehensive project documentation**

```
docs/
├── README.md              # Original comprehensive documentation
├── overview.md            # Project overview and goals
├── installation.md        # Setup instructions
├── quick-start.md         # Getting started guide
├── usage-examples.md      # Command examples
├── docker.md              # Docker guide
├── mcp-server.md          # MCP server documentation
├── uv-setup.md            # UV package manager guide
├── testing.md             # Testing framework
├── scripts.md             # Scripts overview
├── eda-tools.md           # EDA tools guide
├── debug-scripts.md       # Debug utilities
├── analysis-tools.md      # Analysis workflow
├── workflow.md            # Development workflow
├── ci-cd.md               # CI/CD setup
├── project-structure.md   # This file
├── copilot-instructions.md # Copilot configuration
└── [legacy documentation files]
```

### `uv_setup/` - UV Package Manager
**Fast dependency management setup**

```
uv_setup/
├── setup_uv.sh           # UV installation script
├── update_deps.sh        # Dependency update script
└── uv.toml               # UV configuration
```

### `.github/` - GitHub Actions
**CI/CD workflows and automation**

```
.github/
└── workflows/
    ├── docker-build.yml   # Main CI/CD workflow
    ├── test.yml          # Testing workflow
    └── deploy.yml        # Deployment workflow
```

## Build and Output Directories

### `build/` - Build Artifacts
**Generated during development**

```
build/
├── lib/                  # Compiled libraries
│   ├── __init__.py
│   ├── calculation/
│   ├── cli/
│   ├── common/
│   ├── data/
│   ├── eda/
│   ├── export/
│   ├── plotting/
│   ├── utils/
│   └── workflow/
└── [other build artifacts]
```

### `logs/` - Log Files
**Application and analysis logs**

```
logs/
├── app.log               # Main application log
├── analysis.log          # Analysis execution logs
├── mcp_server.log        # MCP server logs
├── eda_basic_stats.log   # EDA statistics logs
├── eda_correlation.log   # Correlation analysis logs
├── eda_quality_checks.log # Data quality logs
└── html_reports/         # HTML report outputs
    ├── correlation_analysis/
    ├── feature_importance/
    ├── outlier_analysis/
    └── time_series_analysis/
```

### `results/` - Analysis Results
**Generated analysis outputs**

```
results/
├── plots/                # Generated plot files
├── reports/              # Analysis reports
├── models/               # Saved ML models
└── exports/              # Data exports
```

## Code Organization Principles

### Modular Architecture
- **Separation of Concerns:** Each module has a specific responsibility
- **Loose Coupling:** Modules interact through well-defined interfaces
- **High Cohesion:** Related functionality grouped together
- **Dependency Injection:** Dependencies passed rather than hardcoded

### Package Structure
```python
# Example import structure
from src.calculation.indicator import Indicator
from src.data.data_acquisition import DataAcquisition
from src.plotting.plotting import PlottingEngine
from src.eda.eda_batch_check import EDABatchProcessor
```

### Configuration Management
- **Environment Variables:** Stored in `.env` file
- **Configuration Files:** TOML/JSON for structured config
- **Constants:** Centralized in `src/common/constants.py`
- **Defaults:** Sensible defaults with override capability

### Data Flow Architecture
```
Input Sources → Data Acquisition → Caching → Processing → Analysis → Visualization → Output
     ↓              ↓               ↓          ↓           ↓            ↓           ↓
CSV/API → data_acquisition.py → Parquet → calculation/ → eda/ → plotting/ → results/
```

## Development Workflow

### Adding New Features
1. **Create feature branch:** `git checkout -b feature/new-feature`
2. **Add to appropriate module:** Follow existing structure
3. **Write tests:** Add to corresponding `tests/` directory
4. **Update documentation:** Add to relevant `.md` files
5. **Test locally:** Run tests and debug scripts
6. **Submit PR:** Include tests and documentation

### File Naming Conventions
- **Python files:** `snake_case.py`
- **Classes:** `PascalCase`
- **Functions:** `snake_case`
- **Constants:** `UPPER_SNAKE_CASE`
- **Directories:** `lowercase` or `snake_case`

### Import Organization
```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import pandas as pd
import numpy as np
from rich.console import Console

# Local imports
from src.common.logger import get_logger
from src.calculation.indicator import Indicator
```

## Architecture Patterns

### Plugin Architecture
- **Data Sources:** Pluggable fetchers in `src/data/fetchers/`
- **Plotting Backends:** Interchangeable in `src/plotting/`
- **Analysis Rules:** Modular rules in `src/calculation/rules.py`

### Factory Pattern
- **Data Source Factory:** Create appropriate fetcher based on mode
- **Plotting Factory:** Select backend based on user preference
- **Calculation Factory:** Choose rule implementation

### Observer Pattern
- **Progress Tracking:** Monitor long-running operations
- **Event Logging:** Log important events across modules
- **Error Handling:** Centralized error reporting

## Performance Considerations

### Memory Management
- **Streaming Processing:** Handle large datasets efficiently
- **Caching Strategy:** Balance memory usage and performance
- **Garbage Collection:** Explicit cleanup of large objects

### I/O Optimization
- **Parquet Format:** Efficient storage and retrieval
- **Batch Processing:** Group operations for efficiency
- **Async Operations:** Non-blocking I/O where appropriate

### Scalability Design
- **Horizontal Scaling:** Design for distributed processing
- **Vertical Scaling:** Optimize for multi-core usage
- **Resource Monitoring:** Track and optimize resource usage
